#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命令行工具：将HTML文件转为图片
"""
import argparse
import asyncio
from src.services.screenshot_generator import ScreenshotGenerator

def main():
    parser = argparse.ArgumentParser(description='将HTML文件转为图片')
    parser.add_argument('html_path', help='HTML文件路径')
    parser.add_argument('-o', '--output', help='输出图片路径')
    parser.add_argument('-w', '--width', type=int, default=375, help='视口宽度')
    parser.add_argument('--height', type=int, default=667, help='视口高度')
    parser.add_argument('--full-page', action='store_true', help='截取整页')
    parser.add_argument('--wait-time', type=float, default=1.0, help='等待时间（秒）')
    args = parser.parse_args()

    generator = ScreenshotGenerator()
    async def run():
        result = await generator.take_screenshot(
            html_file=args.html_path,
            output_path=args.output,
            width=args.width,
            height=args.height,
            headless=True,
            full_page=args.full_page,
            wait_time=args.wait_time
        )
        if result:
            print(f"图片已保存: {args.output or args.html_path.replace('.html', '.png')}")
        else:
            print("截图失败")
    asyncio.run(run())

if __name__ == "__main__":
    main() 