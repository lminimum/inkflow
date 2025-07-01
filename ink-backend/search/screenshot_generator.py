#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
独立的截图生成器
通过命令行参数运行，在单独进程中生成截图
"""

import os
import sys
import argparse
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ScreenshotGenerator:
    """独立的截图生成器"""
    
    def __init__(self):
        pass
    
    async def take_screenshot(
        self, 
        html_file: str, 
        output_path: str = None,
        width: int = 375,
        height: int = 667,
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
            html_path = Path(html_file)
            if not html_path.exists():
                logger.error(f"HTML文件不存在: {html_file}")
                return False
            
            # 确定输出路径
            if output_path is None:
                screenshot_path = html_path.with_suffix(".png")
            else:
                screenshot_path = Path(output_path)
            
            logger.info(f"开始生成截图: {html_file} -> {screenshot_path}")
            
            async with async_playwright() as p:
                # 启动浏览器
                browser = await p.chromium.launch(headless=headless)
                page = await browser.new_page(viewport={"width": width, "height": height})
                
                # 加载HTML文件
                file_url = f"file:///{html_path.absolute()}"
                await page.goto(file_url)
                
                # 等待页面加载完成
                await page.wait_for_load_state("networkidle")
                await asyncio.sleep(wait_time)  # 额外等待确保样式加载完成
                
                # 截图配置
                screenshot_options = {
                    "path": screenshot_path,
                    "full_page": full_page
                }
                
                # 如果不是全页截图，设置裁剪区域
                if not full_page:
                    screenshot_options["clip"] = {
                        "x": 0, 
                        "y": 0, 
                        "width": width, 
                        "height": height
                    }
                
                # 生成截图
                await page.screenshot(**screenshot_options)
                
                await browser.close()
                
                logger.info(f"截图生成成功: {screenshot_path}")
                return True
                
        except Exception as e:
            logger.error(f"截图生成失败: {e}")
            import traceback
            logger.error(f"错误详情:\n{traceback.format_exc()}")
            return False
    
    async def batch_screenshot(
        self,
        html_files: list,
        output_dir: str = None,
        width: int = 375,
        height: int = 667,
        headless: bool = True,
        full_page: bool = False,
        wait_time: float = 1.0
    ) -> dict:
        """批量生成截图
        
        Args:
            html_files: HTML文件路径列表
            output_dir: 输出目录，如果为None则在各自的目录生成
            width: 视口宽度
            height: 视口高度
            headless: 是否无头模式
            full_page: 是否截取整页
            wait_time: 等待时间（秒）
            
        Returns:
            dict: 结果统计
        """
        results = {
            "success": [],
            "failed": [],
            "total": len(html_files)
        }
        
        logger.info(f"开始批量生成截图，共{len(html_files)}个文件")
        
        for i, html_file in enumerate(html_files, 1):
            logger.info(f"处理第{i}/{len(html_files)}个文件: {html_file}")
            
            # 确定输出路径
            output_path = None
            if output_dir:
                html_path = Path(html_file)
                output_path = Path(output_dir) / f"{html_path.stem}.png"
                # 确保输出目录存在
                output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 生成截图
            success = await self.take_screenshot(
                html_file=html_file,
                output_path=str(output_path) if output_path else None,
                width=width,
                height=height,
                headless=headless,
                full_page=full_page,
                wait_time=wait_time
            )
            
            if success:
                results["success"].append(html_file)
            else:
                results["failed"].append(html_file)
        
        logger.info(f"批量截图完成: 成功{len(results['success'])}个，失败{len(results['failed'])}个")
        return results


def main():
    """命令行主函数"""
    parser = argparse.ArgumentParser(description='独立的截图生成器')
    
    # 基本参数
    parser.add_argument('html_file', nargs='?', help='HTML文件路径')
    parser.add_argument('-o', '--output', help='输出图片路径')
    parser.add_argument('-w', '--width', type=int, default=375, help='视口宽度 (默认: 375)')
    parser.add_argument('--height', type=int, default=667, help='视口高度 (默认: 667)')
    parser.add_argument('--headless', action='store_true', default=True, help='无头模式 (默认: True)')
    parser.add_argument('--no-headless', action='store_false', dest='headless', help='禁用无头模式')
    parser.add_argument('--full-page', action='store_true', help='截取整页')
    parser.add_argument('--wait-time', type=float, default=1.0, help='等待时间（秒）')
    
    # 批量处理参数
    parser.add_argument('--batch', help='批量处理模式，传入包含HTML文件路径的JSON文件')
    parser.add_argument('--output-dir', help='批量处理时的输出目录')
    
    # 解析参数
    args = parser.parse_args()
    
    # 验证参数
    if not args.batch and not args.html_file:
        parser.error("必须提供 html_file 或使用 --batch 参数")
    
    # 创建截图生成器
    generator = ScreenshotGenerator()
    
    async def run_generator():
        if args.batch:
            # 批量处理模式
            try:
                with open(args.batch, 'r', encoding='utf-8') as f:
                    html_files = json.load(f)
                
                results = await generator.batch_screenshot(
                    html_files=html_files,
                    output_dir=args.output_dir,
                    width=args.width,
                    height=args.height,
                    headless=args.headless,
                    full_page=args.full_page,
                    wait_time=args.wait_time
                )
                
                # 输出结果
                print(json.dumps(results, ensure_ascii=False, indent=2))
                
                # 设置退出码
                exit_code = 0 if len(results["failed"]) == 0 else 1
                sys.exit(exit_code)
                
            except Exception as e:
                logger.error(f"批量处理失败: {e}")
                sys.exit(1)
        else:
            # 单文件处理模式
            success = await generator.take_screenshot(
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
    
    # 运行异步函数
    try:
        asyncio.run(run_generator())
    except KeyboardInterrupt:
        logger.info("用户中断操作")
        sys.exit(1)
    except Exception as e:
        logger.error(f"程序执行失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
