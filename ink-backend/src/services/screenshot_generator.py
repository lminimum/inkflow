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
from typing import Optional
import traceback

# 设置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ScreenshotGenerator:
    """独立的截图生成器"""
    
    def __init__(self):
        pass
    
    async def take_screenshot(
        self, 
        html_file: str, 
        output_path: Optional[str] = None,
        width: int = 800,
        height: Optional[int] = None,
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
        
        try:
            # 使用异步 API 生成截图
            logger.debug("调用异步截图方法")
            return await self._take_screenshot_async(file_url, output_path, width, height, headless, full_page, wait_time)
        except Exception as e:
            logger.error(f"截图生成失败:")
            logger.error(f"错误详情:\n{str(e)}")
            logger.error(f"堆栈跟踪:\n{traceback.format_exc()}")
            return False
    
    async def _take_screenshot_async(self, file_url, output_path, width, height, headless, full_page, wait_time):
        """使用异步 API 生成截图"""
        logger.debug(f"异步截图开始: {file_url} -> {output_path}")
        logger.debug(f"参数: width={width}, height={height}, headless={headless}, full_page={full_page}, wait_time={wait_time}")
        
        try:
            logger.debug("初始化 async_playwright")
            async with async_playwright() as p:
                logger.debug("启动浏览器")
                browser = await p.chromium.launch(headless=headless)
                try:
                    logger.debug("创建新页面")
                    page = await browser.new_page(viewport={"width": width, "height": height})
                    
                    logger.debug(f"导航到 URL: {file_url}")
                    await page.goto(file_url)
                    
                    logger.debug(f"等待 {wait_time} 秒")
                    await page.wait_for_timeout(int(wait_time * 1000))  # 毫秒
                    
                    logger.debug(f"截图保存到: {output_path}")
                    await page.screenshot(path=output_path, full_page=full_page)
                    
                    logger.debug("截图成功")
                    return True
                except Exception as e:
                    logger.error(f"页面操作失败: {str(e)}")
                    logger.error(traceback.format_exc())
                    return False
                finally:
                    logger.debug("关闭浏览器")
                    await browser.close()
        except Exception as e:
            logger.error(f"Playwright 初始化失败: {str(e)}")
            logger.error(traceback.format_exc())
            return False
    
    async def batch_screenshot(
        self,
        html_files: list,
        output_dir: Optional[str] = None,
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
