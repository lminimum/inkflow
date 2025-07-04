import json
import re
from .base_generator import BaseGenerator

class ContentSplitter(BaseGenerator):
    async def split_content_into_sections(self, content: str, num_sections: int) -> list:
        """将内容分割成指定数量的部分"""
        prompt = f"""请将以下内容严格分割成{num_sections}个连贯的部分，每个部分适合作为小红书笔记配图的描述。
        必须返回格式正确的JSON数组，数组长度必须恰好为{num_sections}。
        即使内容过短或过长，也必须严格按照指定数量分割。
        示例：
        - 如果需要1个部分，返回：["完整内容作为一个部分"]
        - 如果需要2个部分，返回：["标题部分内容","正文部分内容"]
        - 如果需要3个部分，返回：["标题部分内容","正文部分内容","正文部分内容"]
        不要包含任何额外解释、文字说明或markdown格式（如```json）。
        内容：{content}"""

        response = await self.call_ai_service(prompt)

        # 清理可能的markdown标记
        if response.startswith("```json"):
            response = response[7:]
        if response.endswith("```"):
            response = response[:-3]
        response = response.strip()
        self.logger.debug(f"AI内容分割原始响应: {response}")  # Log raw response

        try:
            # 清理响应中的无效控制字符
            cleaned_response = re.sub(r'[\x00-\x1F\x7F]', '', response)
            sections = json.loads(cleaned_response)
            self.logger.debug(f"AI内容分割解析后结果 (类型: {type(sections)}, 内容: {sections})")  # Log parsed result

            # 验证结果是一个列表并且只包含非空字符串
            if not isinstance(sections, list):
                raise ValueError(f"分割结果不是有效的列表，实际类型: {type(sections)}")

            # 处理列表长度不正确的情况，优先考虑num_sections=1的合并
            if len(sections) != num_sections:
                 if num_sections == 1:
                    self.logger.warning(f"期望1个部分但得到{len(sections)}个，自动合并为一个部分")
                    # 确保所有元素都是字符串后再进行合并
                    sections = [' '.join([str(item) for item in sections if isinstance(item, (str, int, float, bool))])]
                 else:
                    raise ValueError(f"分割结果数量不正确，期望{num_sections}个部分，实际{len(sections)}个")

            # 最终验证每个部分
            validated_sections = []
            for i, section in enumerate(sections):
                if not isinstance(section, str) or not section.strip():
                    raise ValueError(f"分割结果包含无效部分，第{i+1}部分不是非空字符串: {section}")
                validated_sections.append(section.strip())

            return validated_sections

        except json.JSONDecodeError as e:
            raise Exception(f"内容分割失败，无法解析JSON: {e}. 原始响应: {response}")
        except ValueError as e:
            # 重新引发ValueError并附上原始响应以便调试
            raise ValueError(f"{e}. 原始响应: {response}")
