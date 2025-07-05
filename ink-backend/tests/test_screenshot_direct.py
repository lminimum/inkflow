#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接测试截图生成器
"""
import os
import sys
import asyncio
import logging

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入截图生成器
from src.services.screenshot_generator import ScreenshotGenerator

# 配置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_screenshot():
    """测试截图生成器"""
    # 测试 HTML 文件路径
    html_file = os.path.abspath("tests/test_html.html")
    output_path = os.path.abspath("tests/direct_test_output.png")
    
    logger.info(f"HTML 文件: {html_file}")
    logger.info(f"输出路径: {output_path}")
    
    # 检查文件是否存在
    if not os.path.exists(html_file):
        logger.error(f"HTML 文件不存在: {html_file}")
        return
    
    # 创建截图生成器
    generator = ScreenshotGenerator()
    
    # 生成截图
    logger.info("开始生成截图")
    success = await generator.take_screenshot(
        html_file=html_file,
        output_path=output_path,
        width=800,
        height=600,
        headless=True,
        full_page=False,
        wait_time=1.0
    )
    
    # 检查结果
    if success:
        logger.info(f"截图成功: {output_path}")
        if os.path.exists(output_path):
            logger.info(f"文件大小: {os.path.getsize(output_path)} 字节")
        else:
            logger.error(f"文件不存在: {output_path}")
    else:
        logger.error("截图失败")

if __name__ == "__main__":
    asyncio.run(test_screenshot()) 