import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai_providers import AIProviderFactory, AIProvider
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()
port = int(os.getenv("PORT", 3000))

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 请求模型定义
class GenerateRequest(BaseModel):
    prompt: str
    model: str
    service: str = 'ollama'

@app.get("/")
async def read_root():
    return {"message": "AI Content Creation Backend is running!"}

@app.get("/api/models")
async def get_models():
    config = AIProviderFactory.load_config()
    services = config.get('services', [])
    return {service['name']: service['models'] for service in services}

@app.post("/api/generate")
async def generate_content(request: GenerateRequest):
    if not request.prompt or not request.model:
        raise HTTPException(status_code=400, detail="Prompt and model are required")

    try:
        # 获取AI服务提供商
        provider = AIProviderFactory.get_provider(request.service)
        
        # 调用模型生成内容
        result = provider.generate_content(request.prompt, request.model)
        return {"content": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate content: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)