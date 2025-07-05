from .base_generator import BaseGenerator
from .constants import PROMPTS

class ContentGenerator(BaseGenerator):
    async def generate_note_content(self, title: str, style: str, audience: str, theme: str) -> str:
        """生成笔记文案"""
        prompt = PROMPTS["content"].format(
            title=title,
            style=style,
            audience=audience,
            theme=theme
        )
        return await self.call_ai_service(prompt)
