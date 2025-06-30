from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "AI Content Creation Backend is running!"}

def test_generate_ollama():
    response = client.post("/api/generate",
        json={"messages": [{"role": "user", "content": "Hello"}], "model": "huihui_ai/gemma3-abliterated:latest", "service": "ollama"}
    )
    assert response.status_code == 200
    assert "content" in response.json()

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
