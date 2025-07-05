import os
import json
import logging
import tempfile
import subprocess
import sys
import re
from pathlib import Path
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

class XHSPublisher:
    """小红书自动发布服务 (项目合并后版本)"""

    def __init__(self):
        """初始化小红书发布服务"""
        # 项目合并后，路径变得简单
        self.project_root = Path(__file__).resolve().parent.parent.parent
        self.temp_images_dir = self.project_root / "temp_images"
        self.temp_images_dir.mkdir(exist_ok=True)
        
        # 定位 xhs_toolkit.py
        self.xhs_toolkit_script = self.project_root / "xhs_toolkit.py"
        if not self.xhs_toolkit_script.exists():
            raise FileNotFoundError(f"无法找到发布脚本: {self.xhs_toolkit_script}")
        logger.info(f"发布脚本路径: {self.xhs_toolkit_script}")

    def _get_local_file_path(self, url: str) -> Optional[str]:
        """从URL获取本地文件路径"""
        if not url.startswith(('http://', 'https://')):
            return url
        
        if '/api/images/' in url:
            match = re.search(r'/api/images/([^/?]+)', url)
            if match:
                filename = match.group(1)
                # 项目合并后，静态文件路径是固定的
                local_path = self.project_root / "static/image_outputs" / filename
                if local_path.exists():
                    logger.info(f"找到本地图片文件: {local_path}")
                    return str(local_path)
        return None

    def _create_publish_config_and_get_args(self,
                                        title: str,
                                        content: str,
                                        topics: Optional[List[str]] = None,
                                        location: Optional[str] = None,
                                        images: Optional[List[str]] = None,
                                        videos: Optional[List[str]] = None) -> List[str]:
        """准备发布参数，必要时下载图片"""
        image_paths = []
        if images:
            for img_url in images:
                local_path = self._get_local_file_path(img_url)
                if local_path:
                    image_paths.append(local_path)
                else:
                    logger.info(f"无法找到本地路径，尝试下载: {img_url}")
                    downloaded_path = self._download_image(img_url)
                    if downloaded_path:
                        image_paths.append(downloaded_path)

        cmd_args = [
            "publish",
            title,
            content,
        ]
        
        if topics:
            cmd_args.extend(["--topics", ",".join(topics)])
        if location:
            cmd_args.extend(["--location", location])
        if image_paths:
            cmd_args.extend(["--images", ",".join(image_paths)])
        if videos:
            cmd_args.extend(["--videos", ",".join(videos)])
            
        return cmd_args

    def _download_image(self, url: str) -> Optional[str]:
        """下载单个网络图片到本地临时文件"""
        try:
            import requests
            from urllib.parse import urlparse
            
            if not url.startswith(('http://', 'https://')):
                return url
            
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path) or f"image_{hash(url)}.jpg"
            save_path = self.temp_images_dir / filename
            
            logger.info(f"下载图片: {url} -> {save_path}")
            response = requests.get(url, stream=True, timeout=20)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                return str(save_path)
            else:
                logger.warning(f"下载图片失败: {url}, 状态码: {response.status_code}")
                return None
        except ImportError:
            logger.warning("未安装requests库，无法下载网络图片")
            return None
        except Exception as e:
            logger.error(f"下载图片时出错: {url}, 错误: {e}")
            return None

    def publish_note(self,
                     title: str,
                     content: str,
                     topics: Optional[List[str]] = None,
                     location: Optional[str] = None,
                     images: Optional[List[str]] = None,
                     videos: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        发布小红书笔记
        """
        try:
            args = self._create_publish_config_and_get_args(
                title, content, topics, location, images, videos
            )
            
            cmd = [sys.executable, str(self.xhs_toolkit_script)] + args
            
            logger.info(f"准备执行发布命令: {' '.join(cmd)}")
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.project_root,
                env=os.environ.copy()
            )
            
            stdout, stderr = process.communicate()
            exit_code = process.returncode
            
            if exit_code == 0:
                logger.info(f"笔记 '{title}' 发布成功。")
                return {
                    "success": True,
                    "message": "发布成功",
                    "output": stdout
                }
            else:
                logger.error(f"笔记 '{title}' 发布失败 (Exit code: {exit_code})")
                logger.error(f"错误信息: {stderr}")
                return {
                    "success": False,
                    "message": f"发布失败: {stderr or stdout}",
                    "error": stderr,
                    "output": stdout
                }
                
        except Exception as e:
            logger.exception("发布小红书笔记时发生严重错误")
            return {
                "success": False,
                "message": f"发布过程出错: {str(e)}"
            }

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