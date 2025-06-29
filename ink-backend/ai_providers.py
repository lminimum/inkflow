from abc import ABC, abstractmethod
import os
import json
import requests
from langchain_ollama import OllamaLLM

class AIProvider(ABC):
    @abstractmethod
    def generate_content(self, prompt: str, model: str) -> str:
        pass

class OllamaProvider(AIProvider):
    def __init__(self, config):
        self.base_url = config['base_url']
        self.models = config['models']

    def generate_content(self, prompt: str, model: str) -> str:
        if model not in self.models:
            raise ValueError(f"Model {model} not supported by Ollama provider")

        llm = OllamaLLM(
            base_url=self.base_url,
            model=model,
            timeout=30
        )
        return llm.invoke(prompt)

class DeepSeekProvider(AIProvider):
    def __init__(self, config):
        self.base_url = config['base_url']
        self.models = config['models']
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable not set")

    def generate_content(self, prompt: str, model: str) -> str:
        if model not in self.models:
            raise ValueError(f"Model {model} not supported by DeepSeek provider")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

        payload = {
            'model': model,
            'messages': [{'role': 'user', 'content': prompt}],
            'temperature': 0.7
        }

        response = requests.post(self.base_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']

class SiliconFlowProvider(AIProvider):
    def __init__(self, config):
        self.base_url = config['base_url']
        self.models = config['models']
        self.api_key = os.getenv('SILICONFLOW_API_KEY')
        if not self.api_key:
            raise ValueError("SILICONFLOW_API_KEY environment variable not set")

    def generate_content(self, prompt: str, model: str) -> str:
        if model not in self.models:
            raise ValueError(f"Model {model} not supported by SiliconFlow provider")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

        payload = {
            'model': model,
            'messages': [{'role': 'user', 'content': prompt}],
            'temperature': 0.7
        }

        response = requests.post(self.base_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']

class AIProviderFactory:
    _providers = {
        'ollama': OllamaProvider,
        'deepseek': DeepSeekProvider,
        'siliconflow': SiliconFlowProvider
    }

    @staticmethod
    def load_config(config_path: str = 'ai_services.json') -> dict:
        with open(config_path, 'r') as f:
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