import os
import json
import dotenv
dotenv.load_dotenv()
import requests
from playwright.sync_api import sync_playwright
import time
import random
from src.services.ai_providers import AIProviderFactory

class HTMLGenerator:
    """
    一个使用 DeepSeek API 生成HTML内容的工具类
    """
    def __init__(self):
        """初始化生成器，加载配置"""
        # 加载配置文件
        config_path = os.path.join(os.path.dirname(__file__), '../../config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        defaults = config.get('defaults', {})

        # 从配置文件加载配置
        self.content_theme = defaults.get('content_theme', '')
        self.style = defaults.get('style', '')
        self.target_audience = defaults.get('target_audience', '')
        self.service_name = defaults.get('ai_service', 'deepseek')
        self.model = defaults.get('ai_model', 'deepseek-chat')

        # 初始化AI服务提供商
        try:
            self.ai_provider = AIProviderFactory.get_provider(self.service_name, config)
        except Exception as e:
            raise ValueError(f"初始化AI服务提供商失败: {str(e)}")

        # 检查必要的配置项
        if not all([self.content_theme, self.style, self.target_audience]):
            raise ValueError("主题、风格和受众必须在配置文件中设置")



    def call_ai_service(self, prompt: str) -> str:
        """调用AI服务生成内容"""
        messages = [{"role": "user", "content": prompt}]
        try:
            return self.ai_provider.generate_content(messages, self.model)
        except Exception as e:
            raise Exception(f"AI内容生成失败: {str(e)}")

    def generate_note_title(self) -> str:
        """生成小红书风格标题"""
        prompt = f"""请为小红书生成一个关于“{self.content_theme}”的爆款标题，要求：
        1. 包含1-2个相关的 emoji 表情。
        2. 长度不超过20个字。
        3. 风格为“{self.style}”。
        4. 目标受众是“{self.target_audience}”。
        请直接返回标题内容，不要包含任何解释或修饰。"""
        return self.call_ai_service(prompt).strip().strip('"')

    def generate_note_content(self, title: str) -> str:
        """生成笔记文案"""
        prompt = f"""根据以下标题为小红书生成一篇完整的笔记文案：
        标题：{title}
        要求：
        1. 文案风格为“{self.style}”。
        2. 目标受众是“{self.target_audience}”。
        3. 包含适当的表情符号。
        4. 段落分明，排版清晰。
        5. 在文末添加3-5个相关的话题标签。
        请直接返回文案内容，不需要任何解释或修饰。"""
        return self.call_ai_service(prompt)

    def generate_css_style(self) -> str:
        """生成HTML所需的CSS样式"""
        prompt = f"""生成一个适合小红书笔记配图的CSS样式表，要求：
        1. 主题色使用柔和、符合现代设计的颜色，背景色使用高级白色。
        2. 使用优美、清晰的Web字体进行排版。
        3. 添加简单的装饰性元素样式，提升设计感。
        4. 宽度固定为700px，左右内边距80px左右。
        5. 所有内容垂直居中，排版合理。
        6. 整体风格符合：“{self.style}”。
        只返回纯净的CSS代码，不要包含```css标记或其他额外文本。"""
        return self.call_ai_service(prompt).strip()

    def generate_image_html(self, title: str, description: str, css_style: str) -> str:
        """生成HTML代码"""
        prompt = f"""根据以下标题和内容描述以及CSS样式，生成一个适合用作小红书笔记配图的HTML代码。
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
        return self.call_ai_service(prompt)

    def split_content_into_sections(self, content: str, num_sections: int) -> list:
        """将内容分割成指定数量的部分"""
        prompt = f"""请将以下内容分割成{num_sections}个连贯的部分，每个部分适合作为小红书笔记配图的描述。
        返回一个JSON数组，不要包含任何额外解释。
        内容：{content}"""

        response = self.call_ai_service(prompt)

        # 清理可能的markdown标记
        if response.startswith("```json"):
            response = response[7:]
        if response.endswith("```"):
            response = response[:-3]
        response = response.strip()

        try:
            sections = json.loads(response)
            if not isinstance(sections, list) or len(sections) != num_sections:
                raise ValueError(f"分割结果格式不正确，期望{num_sections}个部分")
            return sections
        except json.JSONDecodeError as e:
            raise Exception(f"内容分割失败，无法解析JSON: {e}")

    def render_html_to_image(self, html: str, filename: str):
        """将HTML渲染为图片"""
        clean_html = html.strip()
        if clean_html.startswith("```html"):
            clean_html = clean_html[7:]
        if clean_html.endswith("```"):
            clean_html = clean_html[:-3]
        clean_html = clean_html.strip()

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.set_viewport_size({"width": 750, "height": 1000})
            page.set_content(clean_html)
            time.sleep(2)
            page.screenshot(path=filename, full_page=True)
            browser.close()

    def generate_html_content(self, theme: str = None, style: str = None, audience: str = None) -> str:
        """生成完整的HTML内容"""
        # 允许动态覆盖配置
        if theme:
            self.content_theme = theme
        if style:
            self.style = style
        if audience:
            self.target_audience = audience

        if not all([self.content_theme, self.style, self.target_audience]):
            raise ValueError("主题、风格和受众必须设置")

        title = self.generate_note_title()
        content = self.generate_note_content(title)
        css_style = self.generate_css_style()
        sections = self.split_content_into_sections(content, 1)  # 生成一个部分

        return self.generate_image_html(title, sections[0], css_style)
