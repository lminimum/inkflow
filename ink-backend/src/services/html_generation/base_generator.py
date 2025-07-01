import asyncio
import random
import logging
import httpx
from src.services.ai_providers import AIProviderFactory

class BaseGenerator:
    def __init__(self, config, service_name, model, max_retries, retry_base_delay):
        self.config = config
        self.service_name = service_name
        self.model = model
        self.max_retries = max_retries
        self.retry_base_delay = retry_base_delay
        self.ai_provider = AIProviderFactory.get_provider(self.service_name, self.config)
        self.client = httpx.AsyncClient(timeout=30.0)
        self.logger = logging.getLogger(self.__class__.__name__)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()
        self.logger.info(f"{self.__class__.__name__} resources cleaned up.")

    async def call_ai_service(self, prompt: str) -> str:
        """异步调用AI服务生成内容，包含重试逻辑"""
        messages = [{"role": "user", "content": prompt}]

        for i in range(self.max_retries):
            try:
                return self.ai_provider.generate_content(messages, self.model)
            except Exception as e:
                if i < self.max_retries - 1:
                    delay = self.retry_base_delay * (2 **i) + random.uniform(0, 1)
                    self.logger.warning(f"AI request failed, retrying in {delay:.1f} seconds: {str(e)}")
                    await asyncio.sleep(delay)
                else:
                    self.logger.error(f"AI request failed, max retries reached: {str(e)}")
                    raise

        raise Exception("AI service call failed, all retries failed")
