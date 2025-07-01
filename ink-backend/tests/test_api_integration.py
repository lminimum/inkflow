import sys
import os
# Add parent directory to Python path to import src module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
from fastapi.testclient import TestClient
from src.app.main import app
import pytest

client = TestClient(app)

# 确保测试输出目录存在
os.makedirs('test_outputs', exist_ok=True)

# Add a new integration test for the full HTML generation flow
def test_full_html_generation_flow():
    """集成测试：测试完整的HTML生成流程"""
    theme = '旅行'
    style = '清新'
    audience = '年轻人'
    num_sections = 2 # Test with splitting into 2 sections

    # 1. Generate Title
    title_response = client.post('/api/generate-html/title', json={'theme': theme, 'style': style, 'audience': audience})
    assert title_response.status_code == 200, f"Title generation failed: {title_response.text}"
    title = title_response.json()['title']
    print(f"\nGenerated Title: {title}")
    assert isinstance(title, str) and len(title) > 0

    # 2. Generate CSS
    css_response = client.post('/api/generate-html/css', json={'theme': theme, 'style': style, 'audience': audience}) # theme and audience are not used by css_generator but required by the model
    assert css_response.status_code == 200, f"CSS generation failed: {css_response.text}"
    css_style = css_response.json()['css_style']
    print(f"Generated CSS: {css_style[:100]}...")
    assert isinstance(css_style, str) and len(css_style) > 0

    # 3. Generate Content
    content_response = client.post('/api/generate-html/content', json={'title': title, 'theme': theme, 'style': style, 'audience': audience})
    assert content_response.status_code == 200, f"Content generation failed: {content_response.text}"
    content = content_response.json()['content']
    print(f"Generated Content: {content[:100]}...")
    assert isinstance(content, str) and len(content) > 0

    # 4. Split Content
    sections_response = client.post('/api/generate-html/sections', json={'content': content, 'num_sections': num_sections})
    assert sections_response.status_code == 200, f"Content splitting failed: {sections_response.text}"
    sections_content = sections_response.json()['sections']
    print(f"Split Content into {len(sections_content)} section(s).")
    assert isinstance(sections_content, list)
    assert len(sections_content) == num_sections
    for section in sections_content:
        assert isinstance(section, str) and len(section) > 0

    # 5. Generate HTML for each section
    html_sections = []
    for i, section_content in enumerate(sections_content):
        section_html_response = client.post(
            '/api/generate-html/section_html',
            json={
                'title': title,
                'description': section_content,
                'css_style': css_style
            }
        )
        assert section_html_response.status_code == 200, f"Generating HTML for section failed: {section_html_response.text}"
        html_sections.append(section_html_response.json()['html'])
        print(f"Generated HTML for section {i+1}.")


    # 6. Build Final HTML
    build_response = client.post(
        '/api/generate-html/build',
        json={
            'title': title,
            'css_style': css_style,
            'sections': html_sections # Pass the list of generated HTML snippets
        }
    )
    assert build_response.status_code == 200, f"HTML build failed: {build_response.text}"
    
    # Collect streamed HTML
    full_html_content = ""
    for line in build_response.iter_lines():
        line_str = line.decode() if isinstance(line, bytes) else line
        if line_str.startswith('data:'):
            json_string = line_str[len('data:'):].strip()
            try:
                json_data = json.loads(json_string)
                if json_data.get('type') == 'chunk':
                    full_html_content += json_data.get('content', '')
                elif json_data.get('type') == 'error':
                    pytest.fail(f"Streamed error during HTML build: {json_data.get('content', 'Unknown error')}")
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON from line: {line_str}. Error: {e}")
        elif line_str == 'data: {"type": "done", "content": ""}\n\n':
            break # Stop when done signal is received


    print(f"\nFull HTML Content (first 500 chars):\n{full_html_content[:500]}...")
    assert isinstance(full_html_content, str)
    assert len(full_html_content) > 0
    assert title in full_html_content # Basic check if title is in the final HTML
    assert css_style in full_html_content # Basic check if css is in the final HTML
    for section_html in html_sections:
         assert section_html in full_html_content # Basic check if section HTML is in the final HTML

    # Save the generated HTML to a file
    output_path = os.path.join('test_outputs', 'generated_html.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html_content)
    print(f'Generated HTML saved to: {output_path}')


if __name__ == '__main__':
    # Running tests directly might not work as expected with pytest
    # Use 'pytest' command in the terminal instead.
    # For demonstration, keeping the direct calls but with a warning.
    print("Running integration tests directly. Consider using 'pytest' command.")
    # test_generate_html_real_request() # Commented out
    test_full_html_generation_flow() # Run the new test
    print('\n所有集成测试完成')