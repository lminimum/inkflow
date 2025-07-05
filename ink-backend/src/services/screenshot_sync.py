#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
同步截图生成器
在单独进程中运行，避免异步环境问题
"""

import os
import sys
import argparse
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
import logging
from typing import Optional

# 设置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def take_screenshot(
    html_file: str,
    output_path: Optional[str] = None,
    width: int = 800,
    height: int = 600,
    headless: bool = True,
    full_page: bool = False,
    wait_time: float = 1.0
) -> bool:
    """生成截图
    
    Args:
        html_file: HTML文件路径
        output_path: 输出图片路径，如果为None则使用html文件名替换扩展名为.png
        width: 视口宽度
        height: 视口高度
        headless: 是否无头模式
        full_page: 是否截取整页
        wait_time: 等待时间（秒）
        
    Returns:
        bool: 是否成功生成截图
    """
    try:
        # 规范化路径，去除可能的空格
        html_file = html_file.strip() if isinstance(html_file, str) else html_file
        
        # 如果未指定输出路径，使用HTML文件名+.png
        if output_path is None:
            output_path = html_file.replace('.html', '.png')
        
        # 确保路径是绝对路径
        if not os.path.isabs(html_file):
            html_file = os.path.abspath(html_file)
            logger.debug(f"转换为绝对路径: {html_file}")
        
        if not os.path.isabs(output_path):
            output_path = os.path.abspath(output_path)
            logger.debug(f"转换为绝对路径: {output_path}")
        
        # 确保输出路径存在
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)
        logger.debug(f"确保输出目录存在: {output_dir}")
        
        # 检查HTML文件是否存在
        if not os.path.exists(html_file):
            logger.error(f"HTML文件不存在: {html_file}")
            return False
        
        # 使用file://协议加载本地文件
        file_url = f"file://{os.path.abspath(html_file)}"
        logger.debug(f"文件URL: {file_url}")
        
        logger.info(f"开始生成截图: {html_file} -> {output_path}")
        
        # 使用同步 API 生成截图
        with sync_playwright() as p:
            logger.debug("启动浏览器")
            browser = p.chromium.launch(headless=headless)
            try:
                logger.debug("创建新页面")
                page = browser.new_page(viewport={"width": width, "height": height})
                
                logger.debug(f"导航到 URL: {file_url}")
                page.goto(file_url)
                
                logger.debug(f"等待 {wait_time} 秒")
                page.wait_for_timeout(int(wait_time * 1000))  # 毫秒
                
                logger.debug(f"截图保存到: {output_path}")
                page.screenshot(path=output_path, full_page=full_page)
                
                logger.debug("截图成功")
                return True
            except Exception as e:
                logger.error(f"页面操作失败: {str(e)}")
                return False
            finally:
                logger.debug("关闭浏览器")
                browser.close()
                
    except Exception as e:
        logger.error(f"截图生成失败: {str(e)}")
        return False

def main():
    """命令行主函数"""
    parser = argparse.ArgumentParser(description='同步截图生成器')
    
    # 基本参数
    parser.add_argument('html_file', help='HTML文件路径')
    parser.add_argument('-o', '--output', help='输出图片路径')
    parser.add_argument('-w', '--width', type=int, default=375, help='视口宽度 (默认: 375)')
    parser.add_argument('--height', type=int, default=667, help='视口高度 (默认: 667)')
    parser.add_argument('--headless', action='store_true', default=True, help='无头模式 (默认: True)')
    parser.add_argument('--no-headless', action='store_false', dest='headless', help='禁用无头模式')
    parser.add_argument('--full-page', action='store_true', help='截取整页')
    parser.add_argument('--wait-time', type=float, default=1.0, help='等待时间（秒）')
    
    # 解析参数
    args = parser.parse_args()
    
    # 生成截图
    success = take_screenshot(
        html_file=args.html_file,
        output_path=args.output,
        width=args.width,
        height=args.height,
        headless=args.headless,
        full_page=args.full_page,
        wait_time=args.wait_time
    )
    
    # 输出结果
    result = {
        "success": success,
        "html_file": args.html_file,
        "output_path": args.output or str(Path(args.html_file).with_suffix(".png"))
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 设置退出码
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 