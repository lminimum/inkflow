import unittest
import json
import os
import sys
from unittest.mock import patch, MagicMock
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.xhs_publisher import XHSPublisher

class TestXHSPublisher(unittest.TestCase):
    """测试小红书发布服务"""
    
    def test_create_publish_config(self):
        """测试创建发布配置文件"""
        publisher = XHSPublisher()
        
        # 测试参数
        title = "测试标题"
        content = "测试内容"
        topics = ["测试", "Python"]
        
        # 调用方法
        config_path = publisher.create_publish_config(
            title=title,
            content=content,
            topics=topics
        )
        
        # 验证配置文件是否存在
        self.assertTrue(os.path.exists(config_path))
        
        # 验证配置文件内容
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        self.assertEqual(config_data['title'], title)
        self.assertEqual(config_data['content'], content)
        self.assertEqual(config_data['topics'], "测试,Python")
        
        # 清理文件
        os.unlink(config_path)
    
    @patch('src.services.xhs_publisher.subprocess.Popen')
    def test_publish_note_success(self, mock_popen):
        """测试发布笔记成功的情况"""
        # 配置 mock
        process_mock = MagicMock()
        process_mock.communicate.return_value = ("发布成功！", "")
        process_mock.returncode = 0
        mock_popen.return_value = process_mock
        
        # 创建发布者并调用方法
        publisher = XHSPublisher()
        result = publisher.publish_note(
            title="测试标题",
            content="测试内容",
            topics=["测试", "Python"]
        )
        
        # 验证结果
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "发布成功")
    
    @patch('src.services.xhs_publisher.subprocess.Popen')
    def test_publish_note_failure(self, mock_popen):
        """测试发布笔记失败的情况"""
        # 配置 mock
        process_mock = MagicMock()
        process_mock.communicate.return_value = ("", "发布失败")
        process_mock.returncode = 1
        mock_popen.return_value = process_mock
        
        # 创建发布者并调用方法
        publisher = XHSPublisher()
        result = publisher.publish_note(
            title="测试标题",
            content="测试内容"
        )
        
        # 验证结果
        self.assertFalse(result['success'])
        self.assertTrue("发布失败" in result['message'])
    
    def test_invalid_path(self):
        """测试无效路径的情况"""
        # 创建带无效路径的发布者
        publisher = XHSPublisher(xhs_toolkit_path="/invalid/path")
        
        # 调用方法
        result = publisher.publish_note(
            title="测试标题",
            content="测试内容"
        )
        
        # 验证结果
        self.assertFalse(result['success'])
        self.assertTrue("小红书工具包未配置或不可用" in result['message'])

if __name__ == '__main__':
    unittest.main() 