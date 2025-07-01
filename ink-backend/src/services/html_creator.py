import os
import json
import re
import asyncio
import random
import logging
import dotenv
dotenv.load_dotenv()
from pathlib import Path
import httpx
from src.services.ai_providers import AIProviderFactory

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 提示词模板 - 复用main_optimized.py中的定义
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

    "css_style": """生成一个适合小红书笔记配图的CSS样式表，要求：
1. 主题色使用柔和、符合现代设计的颜色，背景色使用高级白色。
2. 使用优美、清晰的Web字体进行排版。
3. 添加简单的装饰性元素样式，提升设计感。
4. 宽度固定为700px，左右内边距80px左右。
5. 所有内容垂直居中，排版合理。
6. 整体风格符合：“{style}”。
只返回纯净的CSS代码，不要包含```css标记或其他额外文本。""",

    "image_html": """根据以下标题和内容描述以及CSS样式，生成一个适合用作小红书笔记配图的HTML代码。
标题："{title}"
描述："{description}"
CSS样式："{css_style}"
要求：
1. 使用 div 布局，宽度固定为700px，左右内边距80px左右。
2. 必须使用提供的CSS样式。
3. 适当增加emoji表情。
4. 内容完整，排序合理。
5. 所有内容垂直居中。
6. 只返回纯净的HTML代码，不要包含任何解释或标记。"""
}

import logging

class HTMLCreator:
    logger = logging.getLogger(__name__)
    
    def __init__(self, ai_provider, model="deepseek-chat", max_retries=3):
        self.ai_provider = ai_provider
        self.model = model
        self.max_retries = max_retries
        self.ai_provider = ai_provider
        self.model = model
        self.max_retries = max_retries

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass
    """
    异步HTML生成器，专注于内容生成逻辑
    """
    def __init__(self):
        """初始化生成器，加载配置"""
        # 加载配置文件
        config_path = Path(__file__).parent.parent.parent / 'config.json'
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        defaults = self.config.get('defaults', {})

        # 从配置文件加载配置
        self.content_theme = defaults.get('content_theme', '')
        self.style = defaults.get('style', '')
        self.target_audience = defaults.get('target_audience', '')
        self.service_name = defaults.get('ai_service', 'deepseek')
        self.model = defaults.get('ai_model', 'deepseek-chat')
        self.max_retries = self.config.get('max_retries', 3)
        self.retry_base_delay = self.config.get('retry_base_delay', 1)

        # 初始化AI服务提供商
        try:
            self.ai_provider = AIProviderFactory.get_provider(self.service_name, self.config)
        except Exception as e:
            raise ValueError(f"初始化AI服务提供商失败: {str(e)}")

        # 检查必要的配置项
        if not all([self.content_theme, self.style, self.target_audience]):
            raise ValueError("主题、风格和受众必须在配置文件中设置")

        # 初始化HTTP客户端
        self.client = httpx.AsyncClient(
            timeout=30.0
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()
        logging.info("HTMLCreator资源已清理")

    async def call_ai_service(self, prompt: str) -> str:
        """异步调用AI服务生成内容，包含重试逻辑"""
        messages = [{"role": "user", "content": prompt}]

        for i in range(self.max_retries):
            try:
                return self.ai_provider.generate_content(messages, self.model)
            except Exception as e:
                if i < self.max_retries - 1:
                    delay = self.retry_base_delay * (2 **i) + random.uniform(0, 1)
                    logging.warning(f"AI请求失败，将在{delay:.1f}秒后重试: {str(e)}")
                    await asyncio.sleep(delay)
                else:
                    logging.error(f"AI请求失败，已达到最大重试次数: {str(e)}")
                    raise

        raise Exception("AI服务调用失败，所有重试均告失败")

    async def generate_note_title(self) -> str:
        """生成小红书风格标题"""
        prompt = PROMPTS["title"].format(
            theme=self.content_theme,
            style=self.style,
            audience=self.target_audience
        )
        return (await self.call_ai_service(prompt)).strip().strip('"')

    async def generate_note_content(self, title: str) -> str:
        """生成笔记文案"""
        prompt = PROMPTS["content"].format(
            title=title,
            style=self.style,
            audience=self.target_audience,
            theme=self.content_theme
        )
        return await self.call_ai_service(prompt)

    async def generate_css_style(self) -> str:
        """生成HTML所需的CSS样式"""
        prompt = PROMPTS["css_style"].format(
            style=self.style
        )
        return (await self.call_ai_service(prompt)).strip()

    async def generate_image_html(self, title: str, description: str, css_style: str) -> str:
        """生成HTML代码"""
        prompt = PROMPTS["image_html"].format(
            title=title,
            description=description,
            css_style=css_style
        )
        return await self.call_ai_service(prompt)

    async def split_content_into_sections(self, content: str, num_sections: int) -> list:
        """将内容分割成指定数量的部分"""
        prompt = f"""请将以下内容严格分割成{num_sections}个连贯的部分，每个部分适合作为小红书笔记配图的描述。
        必须返回格式正确的JSON数组，数组长度必须恰好为{num_sections}。
        即使内容过短或过长，也必须严格按照指定数量分割。
        示例：
        - 如果需要1个部分，返回：["完整内容作为一个部分"]
        - 如果需要2个部分，返回：["第一部分内容","第二部分内容"]
        不要包含任何额外解释、文字说明或markdown格式（如```json）。
        内容：{content}"""

        response = await self.call_ai_service(prompt)

        # 清理可能的markdown标记
        if response.startswith("```json"):
            response = response[7:]
        if response.endswith("```"):
            response = response[:-3]
        response = response.strip()
        HTMLCreator.logger.debug(f"AI内容分割响应: {response}")

        try:
            # 清理响应中的无效控制字符
            cleaned_response = re.sub(r'[\x00-\x1F\x7F]', '', response)
            sections = json.loads(cleaned_response)
            # 处理AI返回单个字符串而非列表的情况
            if not isinstance(sections, list):
                if num_sections == 1 and isinstance(sections, str):
                    sections = [sections]
                else:
                    raise ValueError(f"分割结果不是有效的列表，期望{num_sections}个部分")
            elif len(sections) != num_sections:
                # 当期望1个部分但得到多个时，合并所有部分
                if num_sections == 1:
                    HTMLCreator.logger.warning(f"期望1个部分但得到{len(sections)}个，自动合并为一个部分")
                    sections = [' '.join(sections)]
                else:
                    raise ValueError(f"分割结果格式不正确，期望{num_sections}个部分，实际内容: {sections}")
            return sections
        except json.JSONDecodeError as e:
            raise Exception(f"内容分割失败，无法解析JSON: {e}")

    async def generate_html_content(self, theme: str = None, style: str = None, audience: str = None) -> str:
        """异步生成完整的HTML内容，使用并发提升性能"""
        # 允许动态覆盖配置
        if theme:
            self.content_theme = theme
        if style:
            self.style = style
        if audience:
            self.target_audience = audience

        if not all([self.content_theme, self.style, self.target_audience]):
            raise ValueError("主题、风格和受众必须设置")

        # 并发执行多个AI生成任务
        title_task = self.generate_note_title()
        css_task = self.generate_css_style()

        # 等待标题生成后再生成内容
        title = await title_task
        content_task = self.generate_note_content(title)

        # 并发等待内容和CSS生成
        content, css_style = await asyncio.gather(content_task, css_task)

        # 分割内容并生成HTML
        sections = await self.split_content_into_sections(content, 1)
        html_content = await self.generate_image_html(title, sections[0], css_style)

        return html_content

    @classmethod
    async def create_and_generate(cls, theme: str = None, style: str = None, audience: str = None) -> str:
        """便捷方法：创建实例并生成HTML内容"""
        async with cls() as creator:
            return await creator.generate_html_content(theme, style, audience)