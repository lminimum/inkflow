from .base_generator import BaseGenerator
from .constants import PROMPTS

class TitleGenerator(BaseGenerator):
    async def generate_note_title(self, theme: str, style: str, audience: str) -> str:
        """生成小红书风格标题"""
        prompt = PROMPTS["title"].format(
            theme=theme,
            style=style,
            audience=audience
        )
        return (await self.call_ai_service(prompt)).strip().strip('"')
