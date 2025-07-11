import asyncio
from .base_generator import BaseGenerator
from .constants import PROMPTS
import re

class HTMLBuilder(BaseGenerator):
    async def generate_image_html(self, title: str, description: str, style: str, css_style: str = "") -> str:
        """生成HTML代码"""
        prompt = PROMPTS["image_html"].format(
            title=title,
            description=description,
            style=style,
            css_style=css_style
        )
        html = await self.call_ai_service(prompt)
        # 只去除开头和结尾的 markdown 代码块标记
        html = re.sub(r'^```html\s*', '', html, flags=re.IGNORECASE)
        html = re.sub(r'^```\s*', '', html, flags=re.IGNORECASE)
        html = re.sub(r'```\s*$', '', html, flags=re.IGNORECASE)
        return html.strip()

    async def generate_question_html(self, title: str, question: str, style: str, css_style: str = "") -> str:
        """生成问题类型的HTML代码"""
        prompt = PROMPTS["question_html"].format(
            title=title,
            description=question,
            style=style,
            css_style=css_style
        )
        html = await self.call_ai_service(prompt)
        # 去除开头和结尾的 markdown 代码块标记
        html = re.sub(r'^```html\s*', '', html, flags=re.IGNORECASE)
        html = re.sub(r'^```\s*', '', html, flags=re.IGNORECASE)
        html = re.sub(r'```\s*$', '', html, flags=re.IGNORECASE)
        return html.strip()

    async def generate_section_html(self, content, section_num):
        """生成单个内容区块的HTML"""
        return f'<section class="content-section section-{section_num}">{content}</section>'

    async def stream_final_html(self, title: str, css_style: str, sections: list):
        """流式输出最终的HTML结构"""
        yield f'<html><head><meta charset="UTF-8"><title>{title}</title><style>{css_style}</style></head><body>'
        yield f'<header><h1>{title}</h1></header><main>'

        for i, section in enumerate(sections):
            # Here we assume 'section' is already the HTML for that section
            # If not, you might need to call generate_image_html for each section
            yield section # Or await self.generate_image_html(title, section, css_style) if generating HTML per section
            await asyncio.sleep(0.1) # Control stream speed

        yield '</main></body></html>'
