import sys
import os
import pytest
from fastapi.testclient import TestClient
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.app.main import app

def test_html_to_image_api(tmp_path):
    # 创建一个简单的html文件
    html_content = """
    <html><body><h1>测试截图</h1></body></html>
    """
    html_file = tmp_path / "test.html"
    html_file.write_text(html_content, encoding="utf-8")
    output_path = tmp_path / "test.png"
    client = TestClient(app)
    payload = {
        "html_path": str(html_file),
        "output_path": str(output_path),
        "width": 400,
        "height": 300
    }
    response = client.post("/api/html-to-image", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert os.path.exists(data["output_path"])

def test_xhs_html_to_image_api():
    # 测试将xhs_part1/2/3.html转为图片
    base_dir = os.path.dirname(__file__)
    html_dir = os.path.join(base_dir, "test_outputs")
    files = ["xhs_part1.html", "xhs_part2.html", "xhs_part3.html"]
    client = TestClient(app)
    for fname in files:
        html_path = os.path.join(html_dir, fname)
        output_path = os.path.join(html_dir, fname.replace(".html", ".png"))
        payload = {
            "html_path": html_path,
            "output_path": output_path,
            "width": 400,
            "height": 300
        }
        response = client.post("/api/html-to-image", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert os.path.exists(data["output_path"]) 