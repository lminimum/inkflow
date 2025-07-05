"""
小红书多账号Cookie管理服务

封装了对xhs-toolkit-main中CookieManager的调用，以支持多账号管理。
"""

import os
import json
import shutil
import sys
import logging
from pathlib import Path
from typing import Dict, Any

# 将xhs-toolkit-main添加到系统路径中，以便导入其模块
XHS_TOOLKIT_PATH = Path(__file__).resolve().parent.parent.parent.parent / "xhs-toolkit-main"
if str(XHS_TOOLKIT_PATH) not in sys.path:
    sys.path.insert(0, str(XHS_TOOLKIT_PATH))

try:
    from src.core.config import XHSConfig
    from src.auth.cookie_manager import CookieManager
    from src.core.exceptions import AuthenticationError
except ImportError as e:
    raise ImportError(
        "无法从xhs-toolkit-main导入模块。请确保xhs-toolkit-main目录与ink-backend在同一级。"
    ) from e


logger = logging.getLogger(__name__)

class CookieService:
    """
    一个用于管理多个小红书账号Cookie的服务
    """
    def __init__(self):
        # 使用xhs-toolkit的默认配置作为基础
        base_config = XHSConfig()
        # 在ink-backend项目的数据目录中为不同账号创建独立的存储空间
        self.accounts_dir = Path(base_config.data_dir) / "accounts"
        self.accounts_dir.mkdir(parents=True, exist_ok=True)
        # 用于记录当前活动账号的文件
        self.active_account_file = self.accounts_dir / ".active_account"
        logger.info(f"多账号Cookie服务初始化，账号目录: {self.accounts_dir}")

    def _get_account_cookie_path(self, account_name: str) -> Path:
        """根据账户名获取安全的cookie文件路径"""
        # 过滤掉不安全的文件名字符
        safe_name = "".join(c for c in account_name if c.isalnum() or c in ('_', '-')).strip()
        if not safe_name:
            raise ValueError("无效的账号名称")
        return self.accounts_dir / f"{safe_name}.json"

    def _get_manager_for_account(self, account_name: str) -> CookieManager:
        """为指定账号创建一个配置好路径的CookieManager实例"""
        config = XHSConfig()
        # 动态覆盖cookie文件路径，使其指向特定账号的文件
        config.cookies_file = str(self._get_account_cookie_path(account_name))
        return CookieManager(config)

    def list_accounts(self) -> list[Dict[str, Any]]:
        """列出所有已保存的账号及其状态"""
        accounts = []
        active_account = self.get_active_account()
        for f in self.accounts_dir.glob("*.json"):
            account_name = f.stem
            accounts.append({
                "name": account_name,
                "is_active": account_name == active_account
            })
        return accounts

    def add_account(self, account_name: str) -> Dict[str, Any]:
        """
        启动浏览器会话以添加新账号。
        这是一个阻塞操作，会等待用户在浏览器中完成登录。
        """
        logger.info(f"开始为账号 '{account_name}' 添加cookie...")
        manager = self._get_manager_for_account(account_name)
        try:
            # 使用自动模式，启动浏览器等待用户扫码登录
            success = manager.save_cookies_auto(timeout_seconds=300)
            if success:
                logger.info(f"账号 '{account_name}' 的cookie保存成功。")
                # 新添加的账号自动设为活动账号
                self.set_active_account(account_name)
                return {"success": True, "message": "Cookie已成功保存。"}
            else:
                logger.warning(f"为账号 '{account_name}' 保存cookie失败。")
                return {"success": False, "message": "保存Cookie失败，可能是登录超时或未完成登录。"}
        except AuthenticationError as e:
            logger.error(f"添加账号 '{account_name}' 时认证失败: {e}", exc_info=True)
            return {"success": False, "message": f"认证失败: {e}"}
        except Exception as e:
            logger.error(f"添加账号 '{account_name}' 时发生未知错误: {e}", exc_info=True)
            return {"success": False, "message": "发生未知错误，请查看后端日志。"}

    def delete_account(self, account_name: str) -> Dict[str, Any]:
        """删除指定账号的cookie文件"""
        logger.info(f"请求删除账号: {account_name}")
        cookie_path = self._get_account_cookie_path(account_name)
        if cookie_path.exists():
            cookie_path.unlink()
            logger.info(f"已删除账号 '{account_name}' 的cookie文件: {cookie_path}")
            # 如果删除的是当前活动账号，则清除活动账号设置
            if self.get_active_account() == account_name:
                if self.active_account_file.exists():
                    self.active_account_file.unlink()
                logger.info(f"已清除活动账号设置，因为 '{account_name}' 被删除。")
            return {"success": True, "message": f"账号 '{account_name}' 已删除。"}
        logger.warning(f"尝试删除一个不存在的账号: {account_name}")
        return {"success": False, "message": "账号未找到。"}

    def validate_account(self, account_name: str) -> Dict[str, Any]:
        """验证指定账号的cookie是否有效"""
        logger.info(f"开始验证账号: {account_name}")
        manager = self._get_manager_for_account(account_name)
        try:
            is_valid = manager.validate_cookies()
            logger.info(f"账号 '{account_name}' 验证结果: {'有效' if is_valid else '无效'}")
            return {"account": account_name, "is_valid": is_valid}
        except Exception as e:
            logger.error(f"验证账号 '{account_name}' 时出错: {e}", exc_info=True)
            return {"account": account_name, "is_valid": False, "error": str(e)}

    def set_active_account(self, account_name: str) -> Dict[str, Any]:
        """设置当前活动的账号"""
        cookie_path = self._get_account_cookie_path(account_name)
        if not cookie_path.exists():
            return {"success": False, "message": "无法激活一个不存在的账号。"}
        
        logger.info(f"设置活动账号为: {account_name}")
        with open(self.active_account_file, "w", encoding="utf-8") as f:
            f.write(account_name)

        # 关键步骤：将选定的活动账号cookie复制到xhs-toolkit期望的默认位置
        default_cookie_path = self.get_default_cookie_path()
        shutil.copy(cookie_path, default_cookie_path)
        logger.info(f"已将 '{account_name}' 的cookie复制到默认路径: {default_cookie_path}")
        
        return {"success": True, "message": f"账号 '{account_name}' 已被激活。"}

    def get_active_account(self) -> str | None:
        """获取当前活动的账号名"""
        if self.active_account_file.exists():
            return self.active_account_file.read_text(encoding="utf-8").strip()
        return None

    def get_default_cookie_path(self) -> Path:
        """获取xhs-toolkit使用的默认cookie文件路径"""
        config = XHSConfig()
        return Path(config.cookies_file) 