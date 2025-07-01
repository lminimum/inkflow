import json
import logging
from pathlib import Path
import httpx # Keep httpx for potential future use or if BaseGenerator still needs it
from src.services.ai_providers import AIProviderFactory
from .html_generation.title_generator import TitleGenerator
from .html_generation.css_generator import CSSGenerator
from .html_generation.content_generator import ContentGenerator
from .html_generation.content_splitter import ContentSplitter
from .html_generation.html_builder import HTMLBuilder

class HTMLCreator:
    """
    HTML生成器工厂类，负责加载配置和初始化AI服务提供商，
    并提供创建各种生成器实例的方法。
    """
    logger = logging.getLogger(__name__)

    def __init__(self):
        """初始化工厂，加载配置并初始化AI服务提供商"""
        # 加载配置文件
        config_path = Path(__file__).parent.parent.parent / 'config.json'
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        defaults = self.config.get('defaults', {})

        # 从配置文件加载配置
        self.service_name = defaults.get('ai_service', 'deepseek')
        self.model = defaults.get('ai_model', 'deepseek-chat')
        self.max_retries = self.config.get('max_retries', 3)
        self.retry_base_delay = self.config.get('retry_base_delay', 1)

        # 初始化AI服务提供商
        try:
            self.ai_provider = AIProviderFactory.get_provider(self.service_name, self.config)
        except Exception as e:
            raise ValueError(f"初始化AI服务提供商失败: {str(e)}")

        # Note: We no longer need the HTTP client here as it's in BaseGenerator

    def get_title_generator(self) -> TitleGenerator:
        """获取标题生成器实例"""
        return TitleGenerator(
            config=self.config,
            service_name=self.service_name,
            model=self.model,
            max_retries=self.max_retries,
            retry_base_delay=self.retry_base_delay
        )

    def get_css_generator(self) -> CSSGenerator:
        """获取CSS生成器实例"""
        return CSSGenerator(
            config=self.config,
            service_name=self.service_name,
            model=self.model,
            max_retries=self.max_retries,
            retry_base_delay=self.retry_base_delay
        )

    def get_content_generator(self) -> ContentGenerator:
        """获取内容生成器实例"""
        return ContentGenerator(
            config=self.config,
            service_name=self.service_name,
            model=self.model,
            max_retries=self.max_retries,
            retry_base_delay=self.retry_base_delay
        )

    def get_content_splitter(self) -> ContentSplitter:
        """获取内容分割器实例"""
        return ContentSplitter(
            config=self.config,
            service_name=self.service_name,
            model=self.model,
            max_retries=self.max_retries,
            retry_base_delay=self.retry_base_delay
        )

    def get_html_builder(self) -> HTMLBuilder:
        """获取HTML构建器实例"""
        return HTMLBuilder(
            config=self.config,
            service_name=self.service_name,
            model=self.model,
            max_retries=self.max_retries,
            retry_base_delay=self.retry_base_delay
        )