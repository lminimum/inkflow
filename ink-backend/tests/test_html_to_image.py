import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.services.screenshot_generator import ScreenshotGenerator
import pytest
import asyncio

def test_take_screenshot(tmp_path):
    # 创建一个简单的html文件
    html_content = """
    <html><body><h1>测试截图</h1></body></html>
    """
    html_file = tmp_path / "test.html"
    html_file.write_text(html_content, encoding="utf-8")
    output_path = tmp_path / "test.png"
    generator = ScreenshotGenerator()
    result = asyncio.run(generator.take_screenshot(str(html_file), str(output_path)))
    assert result is True
    assert output_path.exists()

def test_xhs_html_to_image():
    # 测试将xhs_part1/2/3.html转为图片
    base_dir = os.path.dirname(__file__)
    html_dir = os.path.join(base_dir, "test_outputs")
    files = ["xhs_part1.html", "xhs_part2.html", "xhs_part3.html"]
    generator = ScreenshotGenerator()
    for fname in files:
        html_path = os.path.join(html_dir, fname)
        output_path = os.path.join(html_dir, fname.replace(".html", ".png"))
        result = asyncio.run(generator.take_screenshot(html_path, output_path))
        assert result is True
        assert os.path.exists(output_path) 