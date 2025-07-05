"""
小红书多账号Cookie管理服务 (项目合并后版本)

封装了对CookieManager的调用，以支持多账号管理。
"""

import json
import shutil
import logging
from pathlib import Path
from typing import Dict, Any

from src.core.config import XHSConfig
from src.auth.cookie_manager import CookieManager
from src.core.exceptions import AuthenticationError

logger = logging.getLogger(__name__)

class CookieService:
    """
    一个用于管理多个小红书账号Cookie的服务
    """
    def __init__(self):
        # 使用xhs-toolkit的默认配置作为基础
        base_config = XHSConfig()
        # 从cookie文件路径推断出数据目录
        data_dir = Path(base_config.cookies_file).parent
        # 在数据目录中为不同账号创建独立的存储空间
        self.accounts_dir = data_dir / "accounts"
        self.accounts_dir.mkdir(parents=True, exist_ok=True)

        # 自动迁移旧的cookie文件
        self._migrate_default_cookie()

        # 用于记录当前活动账号的文件
        self.active_account_file = self.accounts_dir / ".active_account"
        logger.info(f"多账号Cookie服务初始化，账号目录: {self.accounts_dir}")

    def _migrate_default_cookie(self):
        """如果存在一个默认的、未被管理的cookie，则将其导入到账号系统"""
        default_path = self.get_default_cookie_path()
        imported_name = "default_imported"
        imported_path = self._get_account_cookie_path(imported_name)

        # 如果默认cookie存在，且我们还未导入过它
        if default_path.exists() and not imported_path.exists():
            try:
                # 再次检查，确保它不是一个已被激活的文件的副本
                active_account = self.get_active_account()
                if active_account:
                    active_path = self._get_account_cookie_path(active_account)
                    if active_path.exists() and default_path.stat().st_mtime == active_path.stat().st_mtime:
                        logger.info("默认cookie是当前活动账号的副本，跳过导入。")
                        return

                logger.info(f"检测到默认cookie文件，将作为 '{imported_name}' 导入...")
                shutil.copy2(default_path, imported_path)
                logger.info(f"'{imported_name}' 导入成功。现在可以在账号列表中看到它。")
            except Exception as e:
                logger.error(f"导入默认cookie时出错: {e}")

    def _get_account_cookie_path(self, account_name: str) -> Path:
        """根据账户名获取安全的cookie文件路径"""
        safe_name = "".join(c for c in account_name if c.isalnum() or c in ('_', '-')).strip()
        if not safe_name:
            raise ValueError("无效的账号名称")
        return self.accounts_dir / f"{safe_name}.json"

    def _get_manager_for_account(self, account_name: str) -> CookieManager:
        """为指定账号创建一个配置好路径的CookieManager实例"""
        config = XHSConfig()
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
        """启动浏览器会话以添加新账号。"""
        logger.info(f"开始为账号 '{account_name}' 添加cookie...")
        manager = self._get_manager_for_account(account_name)
        try:
            success = manager.save_cookies_auto(timeout_seconds=300)
            if success:
                self.set_active_account(account_name)
                return {"success": True, "message": "Cookie已成功保存。"}
            else:
                return {"success": False, "message": "保存Cookie失败，可能是登录超时或未完成登录。"}
        except AuthenticationError as e:
            return {"success": False, "message": f"认证失败: {e}"}
        except Exception as e:
            logger.error(f"添加账号时发生未知错误: {e}", exc_info=True)
            return {"success": False, "message": "发生未知错误，请查看后端日志。"}

    def delete_account(self, account_name: str) -> Dict[str, Any]:
        """删除指定账号的cookie文件"""
        cookie_path = self._get_account_cookie_path(account_name)
        if cookie_path.exists():
            cookie_path.unlink()
            if self.get_active_account() == account_name and self.active_account_file.exists():
                self.active_account_file.unlink()
            return {"success": True, "message": f"账号 '{account_name}' 已删除。"}
        return {"success": False, "message": "账号未找到。"}

    def validate_account(self, account_name: str) -> Dict[str, Any]:
        """验证指定账号的cookie是否有效"""
        manager = self._get_manager_for_account(account_name)
        try:
            is_valid = manager.validate_cookies()
            return {"account": account_name, "is_valid": is_valid}
        except Exception as e:
            logger.error(f"验证账号时出错: {e}", exc_info=True)
            return {"account": account_name, "is_valid": False, "error": str(e)}

    def set_active_account(self, account_name: str) -> Dict[str, Any]:
        """设置当前活动的账号"""
        cookie_path = self._get_account_cookie_path(account_name)
        if not cookie_path.exists():
            return {"success": False, "message": "无法激活一个不存在的账号。"}
        
        with open(self.active_account_file, "w", encoding="utf-8") as f:
            f.write(account_name)

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
        """获取默认的cookie文件路径"""
        config = XHSConfig()
        return Path(config.cookies_file) 