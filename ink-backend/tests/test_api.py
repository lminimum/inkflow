import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.app.main import app
from src.services.html_creator import HTMLCreator
from src.services.image_renderer import ImageRenderer

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

@patch('src.app.main.HTMLCreator')
def test_generate_html_endpoint_success(mock_html_class):
    # 导入 AsyncMock 并创建模拟实例
    from unittest.mock import AsyncMock
    mock_instance = AsyncMock()
    
    # 配置异步上下文管理器
    mock_html_class.return_value.__aenter__ = AsyncMock(return_value=mock_instance)
    mock_html_class.return_value.__aexit__ = AsyncMock(return_value=False)
    mock_instance.create_and_generate = AsyncMock(return_value='<html>测试内容</html>')

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
    mock_instance.create_and_generate.assert_awaited_once_with(theme='旅行', style='清新', audience='年轻人')


@patch('src.app.main.HTMLCreator.generate_html_content')
def test_generate_html_endpoint_validation_error(mock_html_generator):
    # 发送缺少参数的请求
    response = client.post(
        '/api/generate-html',
        json={}
    )

    assert response.status_code == 422

@patch('src.app.main.ImageRenderer.render')
def test_generate_image_endpoint_success(mock_render):
    # 配置模拟返回值
    mock_render.return_value = b'fake_image_data'
    
    # 发送请求
    response = client.post(
        '/api/generate-image',
        json={'html': '<html>test</html>'}
    )
    
    # 验证响应
    assert response.status_code == 200
    assert response.headers['content-type'] == 'image/png'
    assert response.content == b'fake_image_data'
    mock_render.assert_called_once_with('<html>test</html>')

def test_generate_image_endpoint_validation_error():
    # 发送缺少参数的请求
    response = client.post(
        '/api/generate-image',
        json={}
    )
    
    assert response.status_code == 422
