from .base_generator import BaseGenerator
from .constants import PROMPTS
import logging # 导入 logging 模块

logger = logging.getLogger(__name__) # 获取 logger 实例

class TitleGenerator(BaseGenerator):
    async def generate_note_title(self, theme: str, style: str, audience: str) -> str:
        """生成小红书风格标题"""
        prompt = PROMPTS["title"].format(
            theme=theme,
            style=style,
            audience=audience
        )
        logger.info(f"生成标题的Prompt: {prompt}") # 记录生成的 prompt
        ai_output = await self.call_ai_service(prompt) # 获取 AI 服务的原始输出
        logger.info(f"AI服务生成标题的原始输出: {ai_output}") # 记录 AI 服务的原始输出
        
        # 检查 ai_output 是否为字符串类型，如果不是，尝试转换为字符串
        if not isinstance(ai_output, str):
            try:
                ai_output = str(ai_output)
                logger.warning(f"AI服务返回的原始输出不是字符串，已尝试转换为字符串: {ai_output}")
            except Exception as e:
                logger.error(f"无法将 AI 服务返回的原始输出转换为字符串: {e}", exc_info=True)
                raise ValueError("AI服务返回了无法处理的输出格式") from e

        # 在进行 strip 操作前再次检查是否为空字符串，避免对 None 或非字符串类型调用 strip
        if not ai_output:
             logger.warning("AI服务返回的原始输出为空或处理后为空。")
             return "" # 返回空字符串，与前端期望一致

        # 进行 strip 操作
        processed_title = ai_output.strip().strip('"')
        logger.info(f"处理后的标题: {processed_title}") # 记录处理后的标题

        return processed_title
