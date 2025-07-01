# main_optimized.py
import os
import asyncio
import random
import logging
from pathlib import Path

import httpx
from playwright.async_api import async_playwright

# 从配置文件导入设置
import config

# --- 日志配置 ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# --- Prompts 定义 ---
# 将所有prompt模板集中管理，便于修改和维护
PROMPTS = {
    "title": """请为小红书生成一个关于“{theme}”的爆款标题，要求：
1. 包含1-2个相关的 emoji 表情。
2. 长度不超过20个字。
3. 风格为“{style}”。
4. 目标受众是“{audience}”。
请直接返回标题内容，不要包含任何解释或修饰。""",

    "content": """根据以下标题为小红书生成一篇完整的笔记文案：
标题：{title}
要求：
1. 文案风格为“{style}”。
2. 目标受众是“{audience}”。
3. 包含适当的表情符号，让内容更生动。
4. 段落分明，排版清晰，易于阅读。
5. 在文末添加3-5个相关的话题标签（例如：#{theme} #{style}探店）。
请直接返回文案内容，不需要任何解释或修修饰。""",

    "image_html": """根据以下内容描述，生成一个适合用作小红书笔记配图的HTML代码。
描述："{description}"
要求：
1.杂志画报风，这种风格模仿高端美食杂志的排版，具有强烈的视觉冲击力和故事性。
2.设计理念：精致、叙事感、版式多变。
3.网页结构布局：顶部导航 (Header)设计感强的Logo。导航菜单可能会使用更艺术化的字体。
4.动态头图 (Dynamic Hero)可以是一张带有视差滚动效果的背景图。
5.标题使用衬线字体（如思源宋体、Playfair Display），营造经典、优雅的感觉。
6.多栏布局 (Multi-Column Layout)打破单调的单栏布局。采用两栏或三栏的不对称网格系统。
7.引文（Pull Quote）：将正文中有趣或重要的句子，用大号字体或特殊样式单独展示在侧边，吸引读者注意。
8.首字下沉 (Drop Cap)：文章的第一个字母使用放大、艺术化的设计。
9.图文融合 (Integrated Imagery)图片不再是简单地上下排列，而是与文字块环绕或重叠，创造出丰富的层次感。
10.一张大图作为背景，上面覆盖一个半透明的文字框。可以设计成一个独特的模块，例如：左图右文：左边是菜品特写，右边是名称、用料、口感描述。滚动展示：一个横向滚动的卡片列表，每张卡片介绍一道菜。
11.全屏图片过渡 (Full-Screen Image Break)在文章的不同部分之间，用一张震撼的全屏图片作为过渡，让页面节奏张弛有度。
12.视觉元素：色调：深邃、饱和的色彩，如深蓝、墨绿、酒红，搭配金色或白色文字，营造高级感。字体：标题用优雅的衬线字体，正文用清晰的无衬线字体，形成对比。
13. 整体风格要符合：“{style}”。
14. 只返回纯净的HTML代码，不要包含任何解释、```html标记或其他额外文本。"""
}


class XiaohongshuAutoGenerator:
    """
    使用 DeepSeek API 和 Playwright 异步生成小红书图文笔记。
    """
    def __init__(self):
        """初始化，加载配置并创建输出目录。"""
        logging.info("正在初始化生成器...")
        self._validate_config()
        self.output_path = Path(config.OUTPUT_DIR)
        self.notes_path = self.output_path / "notes"
        self.images_path = self.output_path / "images"
        self.notes_path.mkdir(parents=True, exist_ok=True)
        self.images_path.mkdir(parents=True, exist_ok=True)
        logging.info(f"配置加载完成：将使用 '{config.MODEL}' 模型生成 {config.NOTES_COUNT} 篇关于 '{config.CONTENT_THEME}' 的笔记。")
        logging.info(f"输出目录 '{self.notes_path}' 和 '{self.images_path}' 已准备就绪。")

    def _validate_config(self):
        """验证关键配置是否存在。"""
        if not config.DEEPSEEK_API_KEY or "sk-" not in config.DEEPSEEK_API_KEY:
            raise ValueError("请在 config.py 文件中设置有效的 DeepSeek API 密钥 (DEEPSEEK_API_KEY)。")

    async def __aenter__(self):
        """异步上下文管理器入口，初始化 Playwright 和 httpx 客户端。"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch()
        self.page = await self.browser.new_page()
        await self.page.set_viewport_size({"width": config.VIEWPORT_WIDTH, "height": config.VIEWPORT_HEIGHT})
        
        self.client = httpx.AsyncClient(
            base_url=config.DEEPSEEK_API_BASE,
            headers={
                "Authorization": f"Bearer {config.DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            },
            timeout=config.API_TIMEOUT
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口，安全关闭资源。"""
        await self.browser.close()
        await self.playwright.stop()
        await self.client.aclose()
        logging.info("浏览器和网络客户端已安全关闭。")

    async def call_deepseek_api(self, prompt: str) -> str:
        """异步调用 DeepSeek API 并返回结果，包含重试逻辑。"""
        payload = {
            "model": config.MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }

        for i in range(config.MAX_RETRIES):
            try:
                response = await self.client.post("/chat/completions", json=payload)
                if response.status_code == 429:
                    delay = config.RETRY_BASE_DELAY * (2 ** i) + random.uniform(0, 1)
                    logging.warning(f"API速率限制(429)。将在 {delay:.1f} 秒后进行第 {i+1}/{config.MAX_RETRIES} 次重试...")
                    await asyncio.sleep(delay)
                    continue
                
                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"]

            except httpx.RequestError as e:
                if i < config.MAX_RETRIES - 1:
                    delay = config.RETRY_BASE_DELAY * (2 ** i)
                    logging.warning(f"API请求失败: {e}。将在 {delay} 秒后重试...")
                    await asyncio.sleep(delay)
                else:
                    logging.error(f"DeepSeek API 请求失败，已达到最大重试次数。")
                    raise
        
        raise Exception("DeepSeek API 请求失败，所有重试均告失败。")

    async def _generate_text(self, prompt_key: str, **kwargs) -> str:
        """通用文本生成函数。"""
        prompt_template = PROMPTS[prompt_key]
        prompt = prompt_template.format(**kwargs)
        result = await self.call_deepseek_api(prompt)
        return result.strip().strip('"')

    async def render_html_to_image(self, html: str, filename: Path):
        """使用复用的浏览器页面将HTML渲染成图片。"""
        clean_html = html.strip()
        if clean_html.startswith("```html"):
            clean_html = clean_html[7:]
        if clean_html.endswith("```"):
            clean_html = clean_html[:-3]
        clean_html = clean_html.strip()

        await self.page.set_content(clean_html)
        await asyncio.sleep(2)  # 等待页面可能存在的动画或JS加载
        await self.page.screenshot(path=filename, full_page=True)
        logging.info(f"    - 图片已保存到: {filename}")

    async def generate_single_note_assets(self, index: int):
        """
        异步生成单篇笔记的所有素材（文案和图片）。
        这是性能优化的核心，所有网络请求和渲染会并发执行。
        """
        logging.info("-" * 50)
        logging.info(f"开始生成笔记 {index + 1}/{config.NOTES_COUNT} 的素材...")

        # 1. 生成标题和内容
        title = await self._generate_text("title", theme=config.CONTENT_THEME, style=config.STYLE, audience=config.TARGET_AUDIENCE)
        logging.info(f"  - 标题生成: {title}")
        content = await self._generate_text("content", title=title, style=config.STYLE, audience=config.TARGET_AUDIENCE, theme=config.CONTENT_THEME)
        logging.info(f"  - 文案已生成。")

        # 2. 并发生成所有图片
        logging.info(f"  - 开始并发生成 {config.IMAGES_PER_NOTE} 张配图...")
        image_tasks = []
        for i in range(config.IMAGES_PER_NOTE):
            description = content[0:150]  # 使用文案开头部分作为图片描述
            image_filename = self.images_path / f"note_{index+1}_img_{i+1}.png"
            # 创建生成HTML和渲染图片的任务
            task = asyncio.create_task(self.generate_and_render_image(description, image_filename))
            image_tasks.append(task)
        
        # 等待所有图片生成任务完成
        image_filenames = await asyncio.gather(*image_tasks)

        # 3. 整理并保存笔记文件
        note_filename = self.notes_path / f"note_{index+1}.txt"
        with open(note_filename, "w", encoding="utf-8") as f:
            f.write(f"标题: {title}\n\n")
            f.write(f"文案:\n{content}\n\n")
            f.write("配图文件:\n")
            for img in image_filenames:
                f.write(f"{img.name}\n")
        logging.info(f"  - 笔记内容已保存到: {note_filename}")
        logging.info(f"成功生成笔记 {index + 1}/{config.NOTES_COUNT}\n")

    async def generate_and_render_image(self, description: str, filename: Path) -> Path:
        """辅助函数：生成HTML并渲染为图片。"""
        html_content = await self._generate_text("image_html", description=description, style=config.STYLE)
        await self.render_html_to_image(html_content, filename)
        return filename

    async def generate_all_notes(self):
        """主流程：循环创建所有笔记的生成任务。"""
        logging.info("开始批量生成小红书笔记...")
        # 为了避免瞬间请求过多导致429，可以分批处理，但对于少量笔记，直接并发也可以
        tasks = [self.generate_single_note_assets(i) for i in range(config.NOTES_COUNT)]
        await asyncio.gather(*tasks, return_exceptions=True) # return_exceptions=True 确保一个失败不影响其他


async def main():
    """程序主入口。"""
    try:
        async with XiaohongshuAutoGenerator() as generator:
            await generator.generate_all_notes()
        logging.info("-" * 50)
        logging.info("所有笔记生成完成！请到 'output' 目录查看成果。")
    except (ValueError, httpx.RequestError, Exception) as e:
        logging.error(f"\n程序执行过程中发生严重错误: {e}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())