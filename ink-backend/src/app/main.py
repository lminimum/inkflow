import os
import logging
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field,ConfigDict
from src.services.ai_providers import AIProviderFactory, AIProvider
import requests
from dotenv import load_dotenv
from src.services.html_creator import HTMLCreator
from src.services.image_renderer import ImageRenderer

# 加载环境变量
load_dotenv()
port = int(os.getenv("PORT", 3000))

# 配置日志
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'app.log')

# 设置日志格式
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 创建RotatingFileHandler，限制文件大小并备份
file_handler = RotatingFileHandler(
    log_file,
    maxBytes=1024*1024*5,  # 5MB
    backupCount=5,
    encoding='utf-8'
)
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.ERROR)

# 控制台处理器
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
console_handler.setLevel(logging.INFO)

# 配置根日志器
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

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
    theme: str = Field(..., min_length=1, description="主题不能为空")
    style: str = Field(..., min_length=1, description="风格不能为空")
    audience: str = Field(..., min_length=1, description="受众不能为空")

class ImageGenerateRequest(BaseModel):
    html: str = Field(..., description="HTML内容，用于生成图片")

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
        logger.error(f"Value error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to generate content: {type(e).__name__}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate content: {type(e).__name__}: {str(e)}")

@app.post("/api/generate-html")
async def generate_html(request: HTMLGenerateRequest):
    try:
        async with HTMLCreator() as creator:
            html_content = await creator.create_and_generate(
                theme=request.theme, style=request.style, audience=request.audience
            )
            return {"html": html_content}
    except Exception as e:
        logger.error(f"Error generating HTML: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate HTML: {str(e)}")

@app.post("/api/generate-image")
async def generate_image(request: ImageGenerateRequest):
    try:
        # 生成图片
        image_bytes = await ImageRenderer.render(request.html)
        return Response(content=image_bytes, media_type="image/png")
    except Exception as e:
        logger.error(f"Error generating image: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate image: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.app.main:app", host="0.0.0.0", port=port, reload=True)