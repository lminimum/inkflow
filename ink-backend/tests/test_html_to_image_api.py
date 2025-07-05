#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 HTML 转图片 API
"""
import os
import sys
import requests
import json

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_html_to_image_api():
    """测试 HTML 转图片 API"""
    # API 端点
    url = "http://localhost:3000/api/html-to-image"
    
    # 测试 HTML 文件路径 - 使用绝对路径
    html_path = os.path.abspath("tests/test_html.html")
    output_path = os.path.abspath("tests/api_test_output.png")
    
    # 构建请求数据
    data = {
        "html_path": html_path,
        "output_path": output_path,
        "width": 800,
        "height": 600,
        "full_page": False,
        "wait_time": 1.0
    }
    
    print(f"发送请求到 {url}")
    print(f"请求数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
    
    try:
        # 发送 POST 请求
        response = requests.post(url, json=data)
        
        # 检查响应
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"截图结果: {'成功' if result.get('success') else '失败'}")
            if result.get('success'):
                print(f"输出路径: {result.get('output_path')}")
                if os.path.exists(result.get('output_path')):
                    print(f"文件大小: {os.path.getsize(result.get('output_path'))} 字节")
                else:
                    print(f"文件不存在: {result.get('output_path')}")
            else:
                print(f"失败原因: {result.get('msg')}")
        else:
            print(f"API 请求失败: {response.status_code} - {response.text}")
    
    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    test_html_to_image_api() 