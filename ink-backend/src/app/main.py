import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field,ConfigDict
from src.services.ai_providers import AIProviderFactory, AIProvider
import requests
from dotenv import load_dotenv
from src.services.html_generator import HTMLGenerator

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
class Message(BaseModel):
    role: str
    content: str

class GenerateRequest(BaseModel):
    messages: list[Message]
    model: str = Field(default="llama3")
    service: str = Field(default="ollama")

class HTMLGenerateRequest(BaseModel):
    theme: str
    style: str
    audience: str

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
    if not request.messages or not request.model:
        raise HTTPException(status_code=400, detail="Messages and model are required")

    try:
        # 获取AI服务提供商
        provider = AIProviderFactory.get_provider(request.service)
        
        # 调用模型生成内容
        content = provider.generate_content([msg.model_dump() for msg in request.messages], request.model)
        return {"content": content}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate content: {type(e).__name__}: {str(e)}")

@app.post("/api/generate-html")
async def generate_html(request: HTMLGenerateRequest):
    try:
        generator = HTMLGenerator()
        html_content = generator.generate_html_content(
            theme=request.theme,
            style=request.style,
            audience=request.audience
        )
        return {"html": html_content}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate HTML: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.app.main:app", host="0.0.0.0", port=port, reload=True)