import os
import json
import logging
import tempfile
import subprocess
import sys
import re
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Union, Any

logger = logging.getLogger(__name__)

class XHSPublisher:
    """小红书自动发布服务"""
    
    def __init__(self, xhs_toolkit_path: Optional[str] = None):
        """
        初始化小红书发布服务
        
        Args:
            xhs_toolkit_path: 小红书工具包路径，如果为None则使用环境变量或默认路径
        """
        # 获取XHS工具包路径
        self.xhs_toolkit_path = xhs_toolkit_path or os.environ.get("XHS_TOOLKIT_PATH")
        
        # 如果未指定路径，尝试使用默认路径
        if not self.xhs_toolkit_path:
            # 尝试常见位置
            possible_paths = [
                Path("./xhs-toolkit-main"),               # 相对于当前目录
                Path("../xhs-toolkit-main"),              # 相对于上级目录
                Path("../../xhs-toolkit-main"),           # 相对于上上级目录
                Path.home() / "xhs-toolkit-main",         # 用户目录
                Path("/opt/xhs-toolkit-main"),            # Linux常见位置
                Path("C:/xhs-toolkit-main"),              # Windows常见位置
            ]
            
            for path in possible_paths:
                if path.exists() and (path / "xhs.bat").exists():
                    self.xhs_toolkit_path = str(path.resolve())  # 转换为绝对路径
                    break
        
        # 验证路径
        if not self.xhs_toolkit_path or not Path(self.xhs_toolkit_path).exists():
            logger.warning("未找到小红书工具包路径，发布功能可能不可用")
        else:
            # 转换为绝对路径
            self.xhs_toolkit_path = str(Path(self.xhs_toolkit_path).resolve())
            logger.info(f"小红书工具包路径: {self.xhs_toolkit_path}")
            
        # 验证xhs.bat存在
        self.xhs_bat_path = Path(self.xhs_toolkit_path) / "xhs.bat" if self.xhs_toolkit_path else None
        if not self.xhs_bat_path or not self.xhs_bat_path.exists():
            logger.warning("未找到xhs.bat文件，发布功能可能不可用")
        else:
            logger.info(f"xhs.bat路径: {self.xhs_bat_path}")
            
        # 检查和修复xhs.bat
        if self.xhs_bat_path and self.xhs_bat_path.exists():
            self._fix_xhs_bat()
    
    def _fix_xhs_bat(self):
        """检查并修复xhs.bat文件中的问题"""
        try:
            bat_path = self.xhs_bat_path
            if not bat_path:
                return
                
            # 读取原始内容
            with open(bat_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # 创建备份
            backup_path = str(bat_path) + '.bak'
            if not os.path.exists(backup_path):
                shutil.copy2(bat_path, backup_path)
                logger.info(f"已创建xhs.bat备份: {backup_path}")
                
            # 修复常见问题
            # 1. 直接指定python解释器路径
            python_path = sys.executable.replace('\\', '\\\\')
            fixed_content = re.sub(
                r'python xhs_toolkit\.py %\*.*?\|\| python3 xhs_toolkit\.py %\*.*?\|\| py xhs_toolkit\.py',
                f'"{python_path}" xhs_toolkit.py %*',
                content, 
                flags=re.DOTALL
            )
            
            # 2. 同样修复交互式部分
            fixed_content = re.sub(
                r'python xhs_toolkit_interactive\.py.*?\|\| python3 xhs_toolkit_interactive\.py.*?\|\| py xhs_toolkit_interactive\.py',
                f'"{python_path}" xhs_toolkit_interactive.py',
                fixed_content, 
                flags=re.DOTALL
            )
            
            # 如果内容有变化，写回文件
            if content != fixed_content:
                with open(bat_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                logger.info("已修复xhs.bat文件中的Python路径问题")
                
        except Exception as e:
            logger.error(f"修复xhs.bat文件时出错: {e}")
    
    def _get_local_file_path(self, url: str) -> Optional[str]:
        """从URL获取本地文件路径，如果是API URL则直接获取文件系统路径"""
        try:
            # 如果不是URL，直接返回
            if not url.startswith(('http://', 'https://')):
                return url
                
            # 检查是否是本地API URL
            if '/api/images/' in url:
                # 从URL提取文件名
                match = re.search(r'/api/images/([^/?]+)', url)
                if match and self.xhs_toolkit_path:
                    filename = match.group(1)
                    # 构建可能的本地路径
                    toolkit_dir = os.path.dirname(self.xhs_toolkit_path)
                    possible_paths = [
                        os.path.join(toolkit_dir, 'ink-backend/static/image_outputs', filename),
                        os.path.join(os.path.dirname(toolkit_dir), 'ink-backend/static/image_outputs', filename),
                        os.path.join(self.xhs_toolkit_path, '../ink-backend/static/image_outputs', filename),
                        os.path.join(self.xhs_toolkit_path, '../../ink-backend/static/image_outputs', filename)
                    ]
                    
                    for path in possible_paths:
                        if os.path.exists(path):
                            logger.info(f"找到本地图片文件: {path}")
                            return path
                            
            return None
        except Exception as e:
            logger.error(f"解析本地文件路径出错: {e}")
            return None
    
    def create_publish_config(self, 
                            title: str,
                            content: str,
                            topics: Optional[List[str]] = None,
                            location: Optional[str] = None,
                            images: Optional[List[str]] = None,
                            videos: Optional[List[str]] = None) -> str:
        """
        创建发布配置文件
        
        Args:
            title: 笔记标题
            content: 笔记内容
            topics: 话题列表
            location: 位置信息
            images: 图片路径列表
            videos: 视频路径列表
            
        Returns:
            配置文件路径
        """
        # 创建配置数据
        config_data = {
            "title": title,
            "content": content,
            "topics": ",".join(topics) if topics else "",
            "location": location or "",
            "images": "",
            "videos": ",".join(videos) if videos else ""
        }
        
        # 处理图片路径 - 首先尝试直接获取本地文件路径
        if images:
            local_image_paths = []
            for img_url in images:
                local_path = self._get_local_file_path(img_url)
                if local_path:
                    local_image_paths.append(local_path)
                    logger.info(f"使用本地图片路径: {local_path}")
            
            if local_image_paths:
                config_data["images"] = ",".join(local_image_paths)
            else:
                # 如果找不到本地路径，则尝试下载
                logger.info("未找到本地图片路径，尝试下载图片")
                downloaded_images = self._download_images(images)
                if downloaded_images:
                    config_data["images"] = ",".join(downloaded_images)
        
        # 创建临时配置文件 - 保存到工具包目录以避免路径问题
        config_dir = self.xhs_toolkit_path if self.xhs_toolkit_path else tempfile.gettempdir()
        config_file = os.path.join(config_dir, f"publish_config_{os.getpid()}_{id(self)}.json")
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"已创建发布配置文件: {config_file}")
        return config_file
    
    def _download_images(self, image_urls: List[str]) -> List[str]:
        """下载网络图片到本地临时文件"""
        try:
            import requests
            from urllib.parse import urlparse
            
            local_images = []
            for url in image_urls:
                if not url.startswith(('http://', 'https://')):
                    local_images.append(url)
                    continue
                
                try:
                    # 从URL解析文件名
                    parsed_url = urlparse(url)
                    filename = os.path.basename(parsed_url.path)
                    if not filename or '.' not in filename:
                        filename = f"image_{len(local_images)}.jpg"
                    
                    # 创建保存路径
                    save_dir = os.path.join(self.xhs_toolkit_path, "temp_images") if self.xhs_toolkit_path else os.path.join(tempfile.gettempdir(), "xhs_images")
                    os.makedirs(save_dir, exist_ok=True)
                    save_path = os.path.join(save_dir, filename)
                    
                    # 下载图片 - 减少超时时间，避免卡住
                    logger.info(f"下载图片: {url} -> {save_path}")
                    response = requests.get(url, stream=True, timeout=10)
                    if response.status_code == 200:
                        with open(save_path, 'wb') as f:
                            for chunk in response.iter_content(1024):
                                f.write(chunk)
                        local_images.append(save_path)
                    else:
                        logger.warning(f"下载图片失败: {url}, 状态码: {response.status_code}")
                except Exception as e:
                    logger.error(f"下载图片出错: {url}, 错误: {e}")
            
            return local_images
        except ImportError:
            logger.warning("未安装requests库，无法下载图片")
            return []
    
    def _create_direct_publish_script(self, config_path: str) -> str:
        """创建直接发布脚本，避免使用xhs.bat"""
        try:
            script_dir = os.path.dirname(config_path)
            script_path = os.path.join(script_dir, f"publish_script_{os.getpid()}.py")
            
            script_content = f"""#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import os

# 确保使用UTF-8编码
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer)
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# 设置Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
xhs_toolkit_path = {repr(self.xhs_toolkit_path)}
sys.path.insert(0, xhs_toolkit_path)

# 加载配置文件
config_file = {repr(config_path)}
with open(config_file, 'r', encoding='utf-8') as f:
    config = json.load(f)
    
# 准备参数
title = config.get('title', '')
content = config.get('content', '')
topics = config.get('topics', '')
location = config.get('location', '')
images = config.get('images', '')
videos = config.get('videos', '')

# 直接调用底层命令
print(f"正在直接调用发布命令...")

# 导入xhs_toolkit
try:
    from xhs_toolkit import main
    sys.argv = ['xhs_toolkit.py', 'publish', title, content, 
                '--topics', topics,
                '--location', location,
                '--images', images,
                '--videos', videos]
    exit_code = main()
    sys.exit(exit_code if isinstance(exit_code, int) else 0)
except Exception as e:
    print(f"发布失败: {{e}}")
    sys.exit(1)
"""
            
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(script_content)
                
            logger.info(f"已创建直接发布脚本: {script_path}")
            return script_path
            
        except Exception as e:
            logger.error(f"创建直接发布脚本时出错: {e}")
            return ""
    
    def publish_note(self, 
                    title: str,
                    content: str,
                    topics: Optional[List[str]] = None,
                    location: Optional[str] = None,
                    images: Optional[List[str]] = None,
                    videos: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        发布小红书笔记
        
        Args:
            title: 笔记标题
            content: 笔记内容
            topics: 话题列表
            location: 位置信息
            images: 图片路径列表
            videos: 视频路径列表
            
        Returns:
            发布结果
        """
        # 验证工具包路径
        if not self.xhs_toolkit_path or not self.xhs_bat_path or not self.xhs_bat_path.exists():
            return {
                "success": False,
                "message": "小红书工具包未配置或不可用"
            }
        
        config_path = None
        script_path = None
        try:
            # 创建配置文件
            config_path = self.create_publish_config(
                title, content, topics, location, images, videos
            )
            
            # 设置环境变量
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'  # 确保Python输出使用UTF-8编码
            
            # 如果是Windows，确保Python在PATH中
            if sys.platform == 'win32':
                python_path = Path(sys.executable).parent
                if 'PATH' in env:
                    env['PATH'] = f"{python_path};{env['PATH']}"
                else:
                    env['PATH'] = str(python_path)
                
            # 方法1: 创建并使用直接发布脚本
            script_path = self._create_direct_publish_script(config_path)
            if script_path:
                logger.info(f"使用直接发布脚本: {script_path}")
                cmd = [sys.executable, script_path]
                logger.info(f"执行命令: {' '.join(cmd)}")
                
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=self.xhs_toolkit_path,
                    env=env
                )
                
                stdout, stderr = process.communicate()
                exit_code = process.returncode
                
                if exit_code == 0:
                    logger.info("小红书笔记发布成功 (直接脚本)")
                    return {
                        "success": True,
                        "message": "发布成功",
                        "output": stdout
                    }
                else:
                    logger.error(f"小红书笔记发布失败 (直接脚本, Exit code: {exit_code}): {stderr}")
                    # 继续尝试方法2
            
            # 方法2: 直接调用Python脚本而不是xhs.bat
            # 从配置文件中读取参数
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                
            # 构建直接调用参数
            cmd = [
                sys.executable,
                os.path.join(self.xhs_toolkit_path, "xhs_toolkit.py"),
                "publish",
                config_data["title"],
                config_data["content"],
            ]
            
            # 添加可选参数
            if config_data.get("topics"):
                cmd.extend(["--topics", config_data["topics"]])
            if config_data.get("location"):
                cmd.extend(["--location", config_data["location"]])
            if config_data.get("images"):
                cmd.extend(["--images", config_data["images"]])
            if config_data.get("videos"):
                cmd.extend(["--videos", config_data["videos"]])
                
            logger.info(f"执行直接命令: {' '.join(cmd)}")
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.xhs_toolkit_path,
                env=env
            )
            
            stdout, stderr = process.communicate()
            exit_code = process.returncode
            
            # 处理结果
            if exit_code == 0:
                logger.info("小红书笔记发布成功 (直接调用Python)")
                return {
                    "success": True,
                    "message": "发布成功",
                    "output": stdout
                }
            else:
                logger.error(f"小红书笔记发布失败 (直接调用Python, Exit code: {exit_code}): {stderr}")
                # 所有方法都失败
                return {
                    "success": False,
                    "message": f"发布失败: {stderr or stdout}",
                    "error": stderr,
                    "output": stdout
                }
                
        except Exception as e:
            logger.exception("发布小红书笔记时出错")
            return {
                "success": False,
                "message": f"发布过程出错: {str(e)}"
            }
        finally:
            # 清理临时文件
            for path in [config_path, script_path]:
                if path and os.path.exists(path):
                    try:
                        os.unlink(path)
                        logger.info(f"已清理临时文件: {path}")
                    except Exception as e:
                        logger.warning(f"清理临时文件失败: {e}")

# 测试代码
if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(level=logging.INFO)
    
    # 测试发布
    publisher = XHSPublisher()
    result = publisher.publish_note(
        title="测试笔记",
        content="这是一个测试笔记内容",
        topics=["测试", "Python"]
    )
    
    print(f"发布结果: {json.dumps(result, ensure_ascii=False, indent=2)}") 