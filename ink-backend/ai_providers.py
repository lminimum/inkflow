from abc import ABC, abstractmethod
from fastapi import HTTPException
import os
import json
import requests
from openai import OpenAI, AuthenticationError, APIError
from langchain_ollama import OllamaLLM

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

        # Convert messages to prompt format
        prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        
        try:
            llm = OllamaLLM(
                base_url=self.base_url,
                model=model,
                timeout=30
            )
            return llm.invoke(prompt)
        except Exception as e:
            raise ValueError(f"Ollama API error: {str(e)}")

class DeepSeekProvider(AIProvider):
    def __init__(self, config):
        self.models = config['models']
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable not set")
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=config['base_url']
        )

    def generate_content(self, messages: list, model: str) -> str:
        if model not in self.models:
            raise ValueError(f"Model {model} not supported by DeepSeek provider")

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7
            )
            return response.choices[0].message.content
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
        self.api_key = os.getenv('SILICONFLOW_API_KEY')
        if not self.api_key:
            raise ValueError("SILICONFLOW_API_KEY environment variable not set")

    def generate_content(self, messages: list, model: str) -> str:
        if model not in self.models:
            raise ValueError(f"Model {model} not supported by SiliconFlow provider")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

        payload = {
            'model': model,
            'messages': messages,
            'temperature': 0.7
        }

        try:
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except requests.exceptions.HTTPError as e:
            error_detail = response.json().get('detail', str(e))
            raise ValueError(f"SiliconFlow API error: {error_detail}")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"SiliconFlow request failed: {str(e)}")
        except KeyError as e:
            raise ValueError(f"Invalid response format from SiliconFlow: {str(e)}")

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