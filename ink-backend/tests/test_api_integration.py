import sys
import os
# Add parent directory to Python path to import src module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)

# 确保测试输出目录存在
os.makedirs('test_outputs', exist_ok=True)


def test_generate_html_real_request():
    # 发送真实请求到HTML生成接口
    response = client.post(
        '/api/generate-html',
        json={
            'theme': '旅行',
            'style': '清新',
            'audience': '年轻人'
        }
    )
    
    # 验证响应状态码
    assert response.status_code == 200, f'API请求失败，状态码: {response.status_code}'
    
    # 获取响应数据
    result = response.json()
    assert 'html' in result, '响应中缺少html字段'
    html_content = result['html']
    
    # 输出到控制台
    print('\n=== HTML生成结果 ===')
    print(html_content[:500] + '...' if len(html_content) > 500 else html_content)
    
    # 保存到文件
    output_path = os.path.join('test_outputs', 'generated_html.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f'HTML内容已保存到: {output_path}')


def test_generate_image_real_request():
    # 先生成HTML内容
    html_response = client.post(
        '/api/generate-html',
        json={
            'theme': '科技',
            'style': '现代',
            'audience': '专业人士'
        }
    )
    assert html_response.status_code == 200
    html_content = html_response.json()['html']
    
    # 发送真实请求到图片生成接口
    response = client.post(
        '/api/generate-image',
        json={'html': html_content}
    )
    
    # 验证响应状态码
    assert response.status_code == 200, f'API请求失败，状态码: {response.status_code}'
    
    # 验证响应内容类型
    assert response.headers['content-type'] == 'image/png', '响应不是PNG图片'
    
    # 输出到控制台
    print('\n=== 图片生成结果 ===')
    print(f'图片大小: {len(response.content)} bytes')
    
    # 保存到文件
    output_path = os.path.join('test_outputs', 'generated_image.png')
    with open(output_path, 'wb') as f:
        f.write(response.content)
    print(f'图片已保存到: {output_path}')


if __name__ == '__main__':
    # 运行所有测试
    test_generate_html_real_request()
    test_generate_image_real_request()
    print('\n所有集成测试完成')