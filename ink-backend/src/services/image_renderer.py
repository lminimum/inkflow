import os
import asyncio
import logging
import tempfile
from pathlib import Path
from playwright.async_api import async_playwright, Page, Browser

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class ImageRenderer:
    """
    异步图片渲染器，专注于将HTML内容转换为图片
    """
    def __init__(self, width: int = 700, height: int = 1000, quality: int = 90):
        """
        初始化图片渲染器
        :param width: 图片宽度
        :param height: 图片高度
        :param quality: 图片质量 (0-100)
        """
        self.width = width
        self.height = height
        self.quality = quality
        self.browser: Browser = None
        self.page: Page = None

    async def __aenter__(self):
        """异步上下文管理器入口，初始化Playwright浏览器"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--single-process'
            ]
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口，清理资源"""
        if self.page:
            await self.page.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        logging.info("ImageRenderer资源已清理")

    async def render_html_to_image(self, html_content: str) -> bytes:
        """
        将HTML内容渲染为图片
        :param html_content: HTML内容字符串
        :return: 图片字节数据
        """
        if not html_content:
            raise ValueError("HTML内容不能为空")

        try:
            # 创建临时HTML文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                f.write(html_content)
                temp_file_path = f.name

            # 创建新页面
            self.page = await self.browser.new_page(
                viewport={'width': self.width, 'height': self.height}
            )

            # 加载HTML文件
            await self.page.goto(f"file://{temp_file_path}")

            # 等待页面加载完成
            await self.page.wait_for_load_state('networkidle')
            await asyncio.sleep(1)  # 额外等待以确保渲染完成

            # 获取页面实际高度并调整
            actual_height = await self.page.evaluate('document.body.scrollHeight')
            if actual_height > self.height:
                await self.page.set_viewport_size({'width': self.width, 'height': actual_height})

            # 截取全屏图片
            image_bytes = await self.page.screenshot(
                full_page=True,
                type='png',
                quality=self.quality,
                omit_background=True
            )

            logging.info(f"成功生成图片，大小: {len(image_bytes)} bytes")
            return image_bytes

        except Exception as e:
            logging.error(f"HTML转图片失败: {str(e)}")
            raise
        finally:
            # 清理临时文件
            if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
                try:
                    os.unlink(temp_file_path)
                except Exception as e:
                    logging.warning(f"清理临时文件失败: {str(e)}")

    @classmethod
    async def render(cls, html_content: str, width: int = 700, height: int = 1000, quality: int = 90) -> bytes:
        """
        便捷方法：创建实例并渲染HTML为图片
        :param html_content: HTML内容字符串
        :param width: 图片宽度
        :param height: 图片高度
        :param quality: 图片质量
        :return: 图片字节数据
        """
        async with cls(width=width, height=height, quality=quality) as renderer:
            return await renderer.render_html_to_image(html_content)