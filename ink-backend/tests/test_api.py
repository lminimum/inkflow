import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
import sys
from pathlib import Path
import json # Import json for parsing streamed responses

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.app.main import app
from src.services.html_creator import HTMLCreator

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

# def test_generate_deepseek():
#     response = client.post("/api/generate",
#         json={"messages": [{"role": "user", "content": "Hello"}], "model": "deepseek-chat", "service": "deepseek"}
#     )
#     assert response.status_code == 200, f"DeepSeek API failed with status {response.status_code}: {response.text}"
#     assert "content" in response.json()

# def test_generate_siliconflow():
#     response = client.post("/api/generate",
#         json={"messages": [{"role": "user", "content": "Hello"}], "model": "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B", "service": "siliconflow"}
#     )
#     assert response.status_code == 200

# def test_generate_aliyun_bailian():
#     response = client.post("/api/generate",
#         json={"messages": [{"role": "user", "content": "Hello"}], "model": "qwen-turbo", "service": "aliyun_bailian"}
#     )
#     assert response.status_code == 200
#     assert "content" in response.json()
    
# @patch('src.services.html_generation.base_generator.BaseGenerator.call_ai_service')
# def test_generate_html_title_success(mock_call_ai_service):
#     """测试 /api/generate-html/title 端点"""
#     mock_call_ai_service.return_value = "测试标题 ✨"
#     response = client.post(
#         '/api/generate-html/title',
#         json={'theme': '美食', 'style': '探店', 'audience': '吃货'}
#     )
#     assert response.status_code == 200
#     assert response.json() == {"title": "测试标题 ✨"}
#     mock_call_ai_service.assert_awaited_once()

# @patch('src.services.html_generation.base_generator.BaseGenerator.call_ai_service')
# def test_generate_html_css_success(mock_call_ai_service):
#     """测试 /api/generate-html/css 端点"""
#     mock_call_ai_service.return_value = "body { font-family: sans-serif; }"
#     response = client.post(
#         '/api/generate-html/css',
#         json={'theme': '科技', 'style': '现代', 'audience': '开发者'} # theme and audience are not used by css_generator but required by the model
#     )
#     assert response.status_code == 200
#     assert response.json() == {"css_style": "body { font-family: sans-serif; }"}
#     mock_call_ai_service.assert_awaited_once()

# @patch('src.services.html_generation.base_generator.BaseGenerator.call_ai_service')
# def test_generate_html_content_success(mock_call_ai_service):
#     """测试 /api/generate-html/content 端点"""
#     mock_call_ai_service.return_value = "这是一篇测试笔记内容。\n#测试 #笔记"
#     response = client.post(
#         '/api/generate-html/content',
#         json={'title': '测试标题', 'theme': '测试', 'style': '测试', 'audience': '测试'}
#     )
#     assert response.status_code == 200
#     assert response.json() == {"content": "这是一篇测试笔记内容。\n#测试 #笔记"}
#     mock_call_ai_service.assert_awaited_once()

# @patch('src.services.html_generation.base_generator.BaseGenerator.call_ai_service')
# def test_split_html_content_success(mock_call_ai_service):
#     """测试 /api/generate-html/sections 端点"""
#     mock_call_ai_service.return_value = '["第一部分", "第二部分"]'
#     response = client.post(
#         '/api/generate-html/sections',
#         json={'content': '这是一篇需要分割的内容。', 'num_sections': 2}
#     )
#     assert response.status_code == 200
#     assert response.json() == {"sections": ["第一部分", "第二部分"]}
#     mock_call_ai_service.assert_awaited_once()

# @patch('src.services.html_generation.base_generator.BaseGenerator.call_ai_service')
# def test_generate_html_section_success(mock_call_ai_service):
#     """测试 /api/generate-html/section_html 端点"""
#     mock_call_ai_service.return_value = "<section>Section HTML</section>"
#     response = client.post(
#         '/api/generate-html/section_html',
#         json={'title': 'Test Title', 'description': 'Section content', 'css_style': 'body {}'}
#     )
#     assert response.status_code == 200
#     assert response.json() == {"html": "<section>Section HTML</section>"}
#     mock_call_ai_service.assert_awaited_once()


# @patch('src.services.html_generation.html_builder.HTMLBuilder.stream_final_html')
# def test_build_final_html_success(mock_stream):
#     """测试 /api/generate-html/build 端点 (流式响应)"""
#     async def async_generator():
#         # Define strings with non-ASCII characters
#         chunk1_str = "data: {\"type\": \"chunk\", \"content\": \"<html><head>...\"}\n\n"
#         chunk2_str = "data: {\"type\": \"chunk\", \"content\": \"<h1>测试标题</h1>\"}\n\n"
#         chunk3_str = "data: {\"type\": \"chunk\", \"content\": \"<section>部分1</section>\"}\n\n"
#         chunk4_str = "data: {\"type\": \"chunk\", \"content\": \"<section>部分2</section>\"}\n\n"
#         chunk5_str = "data: {\"type\": \"chunk\", \"content\": \"</main></body></html>\"}\n\n"
#         done_signal_str = "data: {\"type\": \"done\", \"content\": \"\"}\n\n"

#         # Yield encoded bytes using bytes() constructor
#         yield bytes(chunk1_str, 'utf-8')
#         yield bytes(chunk2_str, 'utf-8')
#         yield bytes(chunk3_str, 'utf-8')
#         yield bytes(chunk4_str, 'utf-8')
#         yield bytes(chunk5_str, 'utf-8')
#         yield bytes(done_signal_str, 'utf-8')

#     mock_stream.return_value = async_generator()

#     response = client.post(
#         '/api/generate-html/build',
#         json={
#             'title': '测试标题',
#             'css_style': 'body {}',
#             'sections': ['<section>部分1</section>', '<section>部分2</section>'] # Pass pre-built section HTML
#         }
#     )        
#     assert response.status_code == 200
#     assert response.headers['content-type'].startswith('text/event-stream')

#     # Collect streamed data
#     data_chunks = []
#     for line in response.iter_lines():
#         line_str = line.decode() if isinstance(line, bytes) else line
#         if line_str.startswith('data:'):
#             json_string = line_str[len('data:'):].strip()
#             # Slice the string, remove 'data: ' prefix
#             json_string = line[len('data:'):].strip() # Use strip() to remove potential trailing whitespace/newlines
#             if json_string: # Ensure there's content after 'data:'
#                  try:
#                      json_data = json.loads(json_string) # Load json from string
#                      data_chunks.append(json_data)
#                  except json.JSONDecodeError as e:
#                      print(f"Failed to decode JSON from line: {line}. Error: {e}") # Debugging


#     # Verify chunks
#     assert len(data_chunks) > 0
#     # Find the 'done' chunk
#     done_chunk_found = any(chunk.get('type') == 'done' for chunk in data_chunks)
#     assert done_chunk_found, "Did not find the 'done' signal in streamed data"

#     # Optional: Check content chunks
#     content_chunks = [chunk['content'] for chunk in data_chunks if chunk.get('type') == 'chunk']
#     full_content = "".join(content_chunks)
#     assert "<html><head>..." in full_content
#     assert "<h1>测试标题</h1>" in full_content
#     assert "<section>部分1</section>" in full_content
#     assert "<section>部分2</section>" in full_content
#     assert "</main></body></html>" in full_content

def test_get_hotspots():
    response = client.get("/api/hotspots")
    assert response.status_code == 200
    data = response.json()
    assert "hotspots" in data
    assert isinstance(data["hotspots"], list)
    # 热点内容结构校验
    if data["hotspots"]:
        assert "title" in data["hotspots"][0]
        assert "source" in data["hotspots"][0]

def test_analyze_hotspots():
    response = client.post("/api/hotspots/analyze", json={})
    assert response.status_code == 200
    data = response.json()
    assert "report" in data
    assert isinstance(data["report"], str)
