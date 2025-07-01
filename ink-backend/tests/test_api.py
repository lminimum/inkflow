import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.app.main import app
from src.services.html_generator import HTMLGenerator

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "AI Content Creation Backend is running!"}

# def test_generate_ollama():
#     response = client.post("/api/generate",
#         json={"messages": [{"role": "user", "content": "Hello"}], "model": "huihui_ai/gemma3-abliterated:latest", "service": "ollama"}
#     )
#     assert response.status_code == 200
#     assert "content" in response.json()

def test_generate_deepseek():
    response = client.post("/api/generate",
        json={"messages": [{"role": "user", "content": "Hello"}], "model": "deepseek-chat", "service": "deepseek"}
    )
    assert response.status_code == 200, f"DeepSeek API failed with status {response.status_code}: {response.text}"
    assert "content" in response.json()

def test_generate_siliconflow():
    response = client.post("/api/generate",
        json={"messages": [{"role": "user", "content": "Hello"}], "model": "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B", "service": "siliconflow"}
    )
    assert response.status_code == 200

def test_generate_aliyun_bailian():
    response = client.post("/api/generate",
        json={"messages": [{"role": "user", "content": "Hello"}], "model": "qwen-turbo", "service": "aliyun_bailian"}
    )
    assert response.status_code == 200
    assert "content" in response.json()

@patch('src.app.main.HTMLGenerator')
def test_generate_html_endpoint_success(mock_html_class):
    # 配置模拟实例的返回值
    mock_instance = mock_html_class.return_value
    mock_instance.generate_html_content.return_value = '<html>测试内容</html>'

    # 发送请求
    response = client.post(
        '/api/generate-html',
        json={
            'theme': '旅行',
            'style': '清新',
            'audience': '年轻人'
        }
    )

    # 验证响应
    assert response.status_code == 200
    assert 'html' in response.json()
    assert response.json()['html'] == '<html>测试内容</html>'
    mock_instance.generate_html_content.assert_called_once_with(theme='旅行', style='清新', audience='年轻人')


@patch('src.app.main.HTMLGenerator.generate_html_content')
def test_generate_html_endpoint_validation_error(mock_html_generator):
    # 发送缺少参数的请求
    response = client.post(
        '/api/generate-html',
        json={}
    )

    assert response.status_code == 422
