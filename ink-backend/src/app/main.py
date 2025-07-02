import os
import logging
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import Response, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ConfigDict
from src.services.ai_providers import AIProviderFactory, AIProvider
import requests
import asyncio
import json
from dotenv import load_dotenv
from src.services.html_creator import HTMLCreator # Keep HTMLCreator factory
import uuid

# Import new generator classes
from src.services.html_generation.title_generator import TitleGenerator
from src.services.html_generation.css_generator import CSSGenerator
from src.services.html_generation.content_generator import ContentGenerator
from src.services.html_generation.content_splitter import ContentSplitter
from src.services.html_generation.html_builder import HTMLBuilder
from src.services.screenshot_generator import ScreenshotGenerator

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

# Reuse HTMLGenerateRequest for title, css, and content generation initial parameters
class HTMLGenerateRequest(BaseModel):
    theme: str = Field(..., min_length=1, description="主题不能为空")
    style: str = Field(..., min_length=1, description="风格不能为空")
    audience: str = Field(..., min_length=1, description="受众不能为空")

# New request models for split and build steps
class ContentRequest(BaseModel):
    title: str = Field(..., min_length=1, description="标题不能为空")
    theme: str = Field(..., min_length=1, description="主题不能为空")
    style: str = Field(..., min_length=1, description="风格不能为空")
    audience: str = Field(..., min_length=1, description="受众不能为空")

class SectionsRequest(BaseModel):
    content: str = Field(..., min_length=1, description="内容不能为空")
    num_sections: int = Field(1, ge=1, description="分割的段落数量")

class BuildRequest(BaseModel):
    title: str = Field(..., min_length=1, description="标题不能为空")
    css_style: str = Field(..., min_length=1, description="CSS样式不能为空")
    sections: list[str] = Field(..., min_length=1, description="HTML内容片段列表")

# Add new request model for section HTML generation
class SectionHTMLRequest(BaseModel):
    title: str = Field(..., min_length=1, description="标题不能为空")
    description: str = Field(..., min_length=1, description="内容描述不能为空")
    css_style: str = Field(..., min_length=1, description="CSS样式不能为空")

from typing import Optional
class HtmlToImageRequest(BaseModel):
    html_path: str
    output_path: Optional[str] = None
    width: int = 375
    height: int = 667
    full_page: bool = False
    wait_time: float = 1.0

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

# Add new endpoints for HTML generation steps

@app.post("/api/generate-html/title")
async def generate_html_title(request: HTMLGenerateRequest):
    """生成小红书笔记标题"""
    try:
        creator = HTMLCreator()
        title_generator = creator.get_title_generator()
        async with title_generator:
            title = await title_generator.generate_note_title(
                theme=request.theme, style=request.style, audience=request.audience
            )
        return {"title": title}
    except Exception as e:
        logger.error(f"生成标题失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"生成标题失败: {str(e)}")

@app.post("/api/generate-html/css")
async def generate_html_css(request: HTMLGenerateRequest): # Reuse HTMLGenerateRequest for style
    """生成HTML所需的CSS样式"""
    try:
        creator = HTMLCreator()
        css_generator = creator.get_css_generator()
        async with css_generator:
            css_style = await css_generator.generate_css_style(style=request.style)
        return {"css_style": css_style}
    except Exception as e:
        logger.error(f"生成CSS失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"生成CSS失败: {str(e)}")

@app.post("/api/generate-html/content")
async def generate_html_content(request: ContentRequest):
    """生成小红书笔记文案内容"""
    try:
        creator = HTMLCreator()
        content_generator = creator.get_content_generator()
        async with content_generator:
            content = await content_generator.generate_note_content(
                title=request.title,
                style=request.style,
                audience=request.audience,
                theme=request.theme
            )
        return {"content": content}
    except Exception as e:
        logger.error(f"生成内容失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"生成内容失败: {str(e)}")

@app.post("/api/generate-html/sections")
async def split_html_content(request: SectionsRequest):
    """将笔记内容分割成多个部分"""
    try:
        creator = HTMLCreator()
        content_splitter = creator.get_content_splitter()
        async with content_splitter:
            sections = await content_splitter.split_content_into_sections(
                content=request.content, num_sections=request.num_sections
            )
        return {"sections": sections}
    except ValueError as e: # Catch ValueError specifically
        error_msg = f"内容分割验证失败: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise HTTPException(status_code=500, detail=error_msg)
    except Exception as e:
        logger.error(f"分割内容失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"分割内容失败: {str(e)}")

@app.post("/api/generate-html/build")
async def build_final_html(request: BuildRequest):
    """根据标题、CSS和内容片段构建最终HTML并流式返回"""
    import time
    async def event_generator():
        try:
            creator = HTMLCreator()
            html_builder = creator.get_html_builder()
            async with html_builder:
                # Assuming sections are already the HTML snippets for each part
                async for chunk in html_builder.stream_final_html(
                    title=request.title,
                    css_style=request.css_style,
                    sections=request.sections # Pass pre-generated sections
                ):
                    # Decode chunk if it's bytes before JSON serialization
                    chunk_str = chunk.decode() if isinstance(chunk, bytes) else chunk
                    # 保存到/tests/test_outputs/
                    output_dir = os.path.join(os.path.dirname(__file__), '../../tests/test_outputs')
                    os.makedirs(output_dir, exist_ok=True)
                    file_path = os.path.join(output_dir, f'final_{int(time.time()*1000)}_{uuid.uuid4().hex}.html')
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(chunk_str)
                    # Use SSE format
                    yield f"data: {{\"type\": \"chunk\", \"content\": {json.dumps(chunk_str)} }}\n\n"
                    await asyncio.sleep(0.01) # Adjust stream rate if needed
                # Send completion signal
                yield f"data: {{\"type\": \"done\", \"content\": \"\"}}\n\n"
        except Exception as e:
            error_msg = f"构建HTML失败: {str(e)}"
            logger.error(error_msg, exc_info=True)
            yield f"data: {{\"type\": \"error\", \"content\": {json.dumps(error_msg)} }}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

# Add new endpoint for generating HTML for a single section
@app.post("/api/generate-html/section_html")
async def generate_html_section(request: SectionHTMLRequest):
    """生成单个内容区块的HTML"""
    try:
        creator = HTMLCreator()
        html_builder = creator.get_html_builder()
        async with html_builder:
            section_html = await html_builder.generate_image_html(
                title=request.title,
                description=request.description,
                css_style=request.css_style
            )
        # 保存到/tests/test_outputs/
        output_dir = os.path.join(os.path.dirname(__file__), '../../tests/test_outputs')
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, f'section_{uuid.uuid4().hex}.html')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(section_html)
        return {"html": section_html, "file_path": file_path}
    except Exception as e:
        logger.error(f"生成内容区块HTML失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"生成内容区块HTML失败: {str(e)}")

@app.post("/api/html-to-image")
async def html_to_image(request: HtmlToImageRequest, background_tasks: BackgroundTasks):
    """将HTML文件转为图片"""
    generator = ScreenshotGenerator()
    # 启动截图任务
    result = await generator.take_screenshot(
        html_file=request.html_path,
        output_path=request.output_path,
        width=request.width,
        height=request.height,
        headless=True,
        full_page=request.full_page,
        wait_time=request.wait_time
    )
    if result:
        return {"success": True, "output_path": request.output_path or request.html_path.replace('.html', '.png')}
    else:
        return {"success": False, "msg": "截图失败"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.app.main:app", host="0.0.0.0", port=port, reload=True)