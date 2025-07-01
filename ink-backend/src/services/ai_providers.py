from abc import ABC, abstractmethod
from fastapi import HTTPException
import os
import json
from openai import AuthenticationError, APIError
from langchain_ollama import OllamaLLM
from langchain_openai import ChatOpenAI

class AIProvider(ABC):
    @abstractmethod
    def generate_content(self, messages: list, model: str) -> str:
        pass

class OllamaProvider(AIProvider):
    def __init__(self, config):
        self.base_url = config['base_url']
        self.models = config['models']

    def generate_content(self, messages: list, model: str) -> str:
        if model not in self.models:
            raise ValueError(f"Model {model} not supported by Ollama provider")
        prompt = "\n".join(f"{m['role']}: {m['content']}" for m in messages)
        try:
            llm = OllamaLLM(
                base_url=self.base_url,
                model=model,
                request_timeout=30
            )
            return llm.invoke(prompt)
        except Exception as e:
            raise ValueError(f"Ollama API error: {str(e)}. Check if base_url '{self.base_url}' and model '{model}' are correct.")

class DeepSeekProvider(AIProvider):
    def __init__(self, config):
        self.models = config['models']
        self.api_key = config.get('api_key')
        if not self.api_key:
            raise ValueError("DeepSeek API key not found in configuration")
        self.client = ChatOpenAI(
            api_key=self.api_key,
            openai_api_base=config['base_url'],
            temperature=0.7
        )

    def generate_content(self, messages: list, model: str) -> str:
        if model not in self.models:
            raise ValueError(f"Model {model} not supported by DeepSeek provider")

        try:
            response = self.client.invoke(messages, model=model)
            return response.content
        except AuthenticationError as e:
            raise HTTPException(status_code=401, detail=f"DeepSeek authentication failed: {str(e)}")
        except APIError as e:
            raise HTTPException(status_code=500, detail=f"DeepSeek API error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error with DeepSeek: {str(e)}")

class SiliconFlowProvider(AIProvider):
    def __init__(self, config):
        self.base_url = config['base_url']
        self.models = config['models']
        self.api_key = config.get('api_key')
        if not self.api_key:
            raise ValueError("SiliconFlow API key not found in configuration")
        self.client = ChatOpenAI(
            api_key=self.api_key,
            openai_api_base=self.base_url,
            temperature=0.7
        )

    def generate_content(self, messages: list, model: str) -> str:
        if model not in self.models:
            raise ValueError(f"Model {model} not supported by SiliconFlow provider")

        try:
            response = self.client.invoke(messages, model=model)
            return response.content
        except AuthenticationError as e:
            raise HTTPException(status_code=401, detail=f"SiliconFlow authentication failed: {str(e)}")
        except APIError as e:
            raise HTTPException(status_code=500, detail=f"SiliconFlow API error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error with SiliconFlow: {str(e)}")

class AliyunBailianProvider(AIProvider):
    def __init__(self, config):
        self.models = config['models']
        self.api_key = config.get('api_key')
        if not self.api_key:
            raise ValueError("Aliyun Bailian API key not found in configuration")
        self.client = ChatOpenAI(
            api_key=self.api_key,
            openai_api_base=config['base_url'],
            temperature=0.7
        )

    def generate_content(self, messages: list, model: str) -> str:
        if model not in self.models:
            raise ValueError(f"Model {model} not supported by Aliyun Bailian provider")

        try:
            response = self.client.invoke(messages, model=model)
            return response.content
        except AuthenticationError as e:
            raise HTTPException(status_code=401, detail=f"Aliyun Bailian authentication failed: {str(e)}")
        except APIError as e:
            raise HTTPException(status_code=500, detail=f"Aliyun Bailian API error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error with Aliyun Bailian: {str(e)}")


class AIProviderFactory:
    _providers = {
        'ollama': OllamaProvider,
        'deepseek': DeepSeekProvider,
        'siliconflow': SiliconFlowProvider,
        'aliyun_bailian': AliyunBailianProvider
    }

    @staticmethod
    def load_config(config_path: str = 'config.json') -> dict:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def get_provider(service_name: str, config: dict = None) -> AIProvider:
        if not config:
            config = AIProviderFactory.load_config()

        service_config = next((s for s in config['services'] if s['name'] == service_name), None)
        if not service_config:
            raise ValueError(f"Service {service_name} not found in configuration")

        provider_class = AIProviderFactory._providers.get(service_config['type'])
        if not provider_class:
            raise ValueError(f"No provider class found for type {service_config['type']}")

        return provider_class(service_config)