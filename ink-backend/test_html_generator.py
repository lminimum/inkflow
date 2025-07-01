import pytest
from unittest.mock import patch, MagicMock
from html_generator import HTMLGenerator
from ai_providers import AIProviderFactory
import json


# 测试HTMLGenerator初始化
def test_html_generator_initialization(monkeypatch):
    # 模拟配置文件加载
    def mock_load_config():
        return {
            'defaults': {
                'content_theme': '旅行攻略',
                'style': '清新',
                'target_audience': '年轻人',
                'ai_service': 'deepseek',
                'ai_model': 'deepseek-chat'
            }
        }
    monkeypatch.setattr(AIProviderFactory, 'load_config', mock_load_config)
    
    # 模拟AI服务提供商
    mock_provider = MagicMock()
    mock_provider.generate_content.return_value = '测试响应'
    monkeypatch.setattr(AIProviderFactory, 'get_provider', lambda *args: mock_provider)
    
    generator = HTMLGenerator()
    assert generator.content_theme == '旅行攻略'
    assert generator.style == '清新'
    assert generator.target_audience == '年轻人'

# 测试API调用方法（模拟成功响应）
@patch('ai_providers.AIProviderFactory.get_provider')
def test_call_deepseek_api_success(mock_get_provider):
    # 模拟AI服务提供商
    mock_provider = MagicMock()
    mock_provider.generate_content.return_value = '测试响应'
    mock_get_provider.return_value = mock_provider

    generator = HTMLGenerator()
    result = generator.generate_content('测试提示')
    assert result == '测试响应'
    mock_provider.generate_content.assert_called_once_with('测试提示')

# 测试标题生成
@patch.object(HTMLGenerator, 'call_deepseek_api')
def test_generate_note_title(mock_api):
    mock_api.return_value = '📚 测试标题示例'
    generator = HTMLGenerator()
    title = generator.generate_note_title()
    assert '📚' in title
    assert len(title) <= 20

# 测试内容分割
@patch.object(HTMLGenerator, 'call_deepseek_api')
def test_split_content_into_sections(mock_api):
    mock_api.return_value = '["第一部分内容", "第二部分内容"]'
    generator = HTMLGenerator()
    content = '这是一段需要分割的长文本内容'
    sections = generator.split_content_into_sections(content, 2)
    assert len(sections) == 2
    assert sections[0] == '第一部分内容'

# 测试HTML生成
@patch.object(HTMLGenerator, 'call_deepseek_api')
def test_generate_image_html(mock_api):
    mock_api.return_value = '<div>测试HTML内容</div>'
    generator = HTMLGenerator()
    html = generator.generate_image_html('测试标题', '测试描述', '测试CSS')
    assert '<div>' in html
    assert '</div>' in html