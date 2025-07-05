from .base_generator import BaseGenerator
from .constants import PROMPTS

class CSSGenerator(BaseGenerator):
    async def generate_css_style(self, style: str) -> str:
        """生成HTML所需的CSS样式"""
        prompt = PROMPTS["css_style"].format(
            style=style
        )
        return (await self.call_ai_service(prompt)).strip()
