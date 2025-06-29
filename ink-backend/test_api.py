import requests
import json

# 后端API基础URL
BASE_URL = "http://localhost:3000"

def test_get_models():
    """测试获取模型列表接口"""
    url = f"{BASE_URL}/api/models"
    try:
        response = requests.get(url)
        assert response.status_code == 200, f"请求失败，状态码: {response.status_code}"
        data = response.json()
        assert isinstance(data, dict), "返回数据不是JSON对象"
        assert "models" in data, "返回数据中不包含models字段"
        print("✅ 模型列表获取成功")
        print("可用模型:", [model["name"] for model in data["models"]])
        return data
    except Exception as e:
        print(f"❌ 获取模型列表失败: {str(e)}")
        return None

def test_generate_content(model_name):
    """测试生成回答接口"""
    url = f"{BASE_URL}/api/generate"
    payload = {
        "prompt": "请简要介绍一下你自己",
        "model": model_name
    }
    try:
        response = requests.post(url, json=payload)
        assert response.status_code == 200, f"请求失败，状态码: {response.status_code}"
        data = response.json()
        assert "content" in data, "返回数据中不包含content字段"
        print("✅ 回答生成成功")
        print("模型回答:", data["content"])
        return data
    except Exception as e:
        print(f"❌ 生成回答失败: {str(e)}")
        return None

if __name__ == "__main__":
    print("=== 开始测试后端API ===")
    # 先测试获取模型列表
    models_data = test_get_models()
    # 如果模型列表获取成功，使用第一个模型测试生成功能
    if models_data and models_data["models"]:
        first_model = models_data["models"][0]["name"]
        print(f"\n使用模型: {first_model} 测试生成功能")
        test_generate_content(first_model)
    print("=== 测试结束 ===")