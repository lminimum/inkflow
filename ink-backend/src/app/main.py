import sys
from pathlib import Path
import asyncio

if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# 其余 import ...
import os
import logging
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from src.services.ai_providers import AIProviderFactory
import asyncio
import json
from dotenv import load_dotenv
from src.services.html_creator import HTMLCreator
from src.services.html_generation.title_generator import TitleGenerator
from src.services.html_generation.css_generator import CSSGenerator
from src.services.html_generation.content_generator import ContentGenerator
import uuid
from src.services.hotspot_service import HotspotService
import concurrent.futures
# 导入同步截图函数
from src.services.screenshot_sync import take_screenshot
from typing import Optional, List
from src.services.xhs_publisher import XHSPublisher
from src.services.cookie_service import CookieService

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

# 定义输出目录路径
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../static'))
HTML_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'html_outputs')
IMAGE_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'image_outputs')

# 确保输出目录存在
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(HTML_OUTPUT_DIR, exist_ok=True)
os.makedirs(IMAGE_OUTPUT_DIR, exist_ok=True)

# 实例化Cookie服务
cookie_service = CookieService()

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory=OUTPUT_DIR), name="static")

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
    model: Optional[str] = Field(None, description="AI模型名称，可选")
    service: Optional[str] = Field(None, description="AI服务提供商，可选")

# New request models for split and build steps
class ContentRequest(BaseModel):
    title: str = Field(..., min_length=1, description="标题不能为空")
    theme: str = Field(..., min_length=1, description="主题不能为空")
    style: str = Field(..., min_length=1, description="风格不能为空")
    audience: str = Field(..., min_length=1, description="受众不能为空")
    model: Optional[str] = Field(None, description="AI模型名称，可选")
    service: Optional[str] = Field(None, description="AI服务提供商，可选")

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
    style: str = Field(..., min_length=1, description="风格不能为空")
    css_style: Optional[str] = Field(None, description="CSS样式，可选")
    is_question: bool = Field(False, description="是否为问题模式")

from typing import Optional
class HtmlToImageRequest(BaseModel):
    html_path: str
    output_path: Optional[str] = None
    width: int = 375
    height: int = 667
    full_page: bool = False
    wait_time: float = 1.0

class HotspotAnalyzeRequest(BaseModel):
    ai_service: Optional[str] = None
    ai_model: Optional[str] = None

class HotspotContentRequest(BaseModel):
    url: str

class XHSPublishRequest(BaseModel):
    title: str
    content: str
    topics: Optional[List[str]] = None
    location: Optional[str] = None
    images: Optional[List[str]] = None
    videos: Optional[List[str]] = None

# Cookie管理请求模型
class CookieAccountRequest(BaseModel):
    account_name: str = Field(..., min_length=1, description="账号名称不能为空")

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
        # 如果指定了模型和服务，直接使用指定的参数创建生成器
        service_name = request.service or creator.service_name
        model = request.model or creator.model
        
        title_generator = TitleGenerator(
            config=creator.config,
            service_name=service_name,
            model=model,
            max_retries=creator.max_retries,
            retry_base_delay=creator.retry_base_delay
        )
            
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
        # 如果指定了模型和服务，直接使用指定的参数创建生成器
        service_name = request.service or creator.service_name
        model = request.model or creator.model
        
        css_generator = CSSGenerator(
            config=creator.config,
            service_name=service_name,
            model=model,
            max_retries=creator.max_retries,
            retry_base_delay=creator.retry_base_delay
        )
            
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
        # 如果指定了模型和服务，直接使用指定的参数创建生成器
        service_name = request.service or creator.service_name
        model = request.model or creator.model
        
        content_generator = ContentGenerator(
            config=creator.config,
            service_name=service_name,
            model=model,
            max_retries=creator.max_retries,
            retry_base_delay=creator.retry_base_delay
        )
            
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

# Add new endpoint for generating HTML for a single section
@app.post("/api/generate-html/section_html")
async def generate_html_section(request: SectionHTMLRequest):
    """生成单个内容区块的HTML"""
    try:
        creator = HTMLCreator()
        html_builder = creator.get_html_builder()
        async with html_builder:
            # 根据是否为问题模式选择不同的生成方法
            if request.is_question:
                section_html = await html_builder.generate_question_html(
                    title=request.title,
                    question=request.description,
                    style=request.style,
                    css_style=request.css_style or ""
                )
            else:
                section_html = await html_builder.generate_image_html(
                title=request.title,
                description=request.description,
                    style=request.style,
                    css_style=request.css_style or ""
            )
        # 保存到输出目录
        section_id = uuid.uuid4().hex
        html_filename = f'section_{section_id}.html'
        html_path = os.path.join(HTML_OUTPUT_DIR, html_filename)
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(html_path), exist_ok=True)
        
        # 保存 HTML 文件
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(section_html)
        
        # 生成 HTML 文件的 URL
        html_url = f"/static/html_outputs/{html_filename}"
        
        return {
            "html": section_html, 
            "file_path": html_path,
            "html_url": html_url,
            "section_id": section_id
        }
    except Exception as e:
        logger.error(f"生成内容区块HTML失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"生成内容区块HTML失败: {str(e)}")

@app.post("/api/html-to-image")
async def html_to_image(request: HtmlToImageRequest, background_tasks: BackgroundTasks):
    """将HTML文件转为图片"""
    try:
        # 检查文件路径
        html_path = request.html_path
        
        # 如果是相对路径，转换为绝对路径
        if not os.path.isabs(html_path):
            html_path = os.path.abspath(html_path)
            logger.debug(f"HTML路径转换为绝对路径: {html_path}")
        
        # 检查文件是否存在
        if not os.path.exists(html_path):
            error_msg = f"HTML文件不存在: {html_path}"
            logger.error(error_msg)
            return {"success": False, "msg": error_msg}
        
        # 处理输出路径
        output_path = request.output_path
        if output_path:
            if not os.path.isabs(output_path):
                output_path = os.path.abspath(output_path)
                logger.debug(f"输出路径转换为绝对路径: {output_path}")
        else:
            # 使用 HTML 文件名作为图片名，保存到 IMAGE_OUTPUT_DIR 目录
            html_filename = os.path.basename(html_path)
            image_filename = html_filename.replace('.html', '.png')
            output_path = os.path.join(IMAGE_OUTPUT_DIR, image_filename)
            logger.debug(f"自动生成输出路径: {output_path}")
        
        # 确保输出目录存在
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)
        
        # 使用线程池运行同步截图代码
        logger.info(f"使用线程池生成截图: {html_path} -> {output_path}")
        
        # 创建线程池执行同步截图函数
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # 将同步函数包装在线程池中执行
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                executor, 
                take_screenshot,
                html_path,
                output_path,
                request.width,
                request.height,
                True,  # headless
                request.full_page,
                request.wait_time
            )
        
        # 检查结果
        if result:
            logger.info(f"截图生成成功: {output_path}")
            
            if os.path.exists(output_path):
                # 获取文件大小
                file_size = os.path.getsize(output_path)
                logger.info(f"文件大小: {file_size} 字节")
                
                # 生成图片 URL
                image_filename = os.path.basename(output_path)
                image_url = f"/api/images/{image_filename}"
                
                return {
                    "success": True, 
                    "output_path": output_path, 
                    "file_size": file_size,
                    "image_url": image_url
                }
            else:
                error_msg = f"截图生成成功但文件不存在: {output_path}"
                logger.error(error_msg)
                return {"success": False, "msg": error_msg}
        else:
            error_msg = "截图生成失败"
            logger.error(error_msg)
            return {"success": False, "msg": error_msg}
    except Exception as e:
        error_msg = f"截图生成过程中发生错误: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {"success": False, "msg": error_msg}

@app.get("/api/hotspots")
async def get_hotspots():
    """获取当前热点榜单"""
    try:
        service = HotspotService()
        hotspots = service.fetch_all_hotspots()
        return {"hotspots": hotspots}
    except Exception as e:
        logger.error(f"获取热点失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"获取热点失败: {str(e)}")

@app.post("/api/hotspots/analyze")
async def analyze_hotspots(request: HotspotAnalyzeRequest):
    """AI分析当前热点榜单"""
    try:
        service = HotspotService()
        hotspots = service.fetch_all_hotspots()
        report = service.analyze_hotspots(hotspots, ai_service=request.ai_service or None, ai_model=request.ai_model or None)
        return {"report": report}
    except Exception as e:
        logger.error(f"热点分析失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"热点分析失败: {str(e)}")

@app.post("/api/hotspots/content")
async def get_hotspot_content(request: HotspotContentRequest):
    """获取指定URL的热点内容"""
    try:
        service = HotspotService()
        content = service.get_hotspot_content(request.url)
        return {"content": content}
    except Exception as e:
        logger.error(f"获取热点内容失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"获取热点内容失败: {str(e)}")

@app.get("/api/cookies/accounts")
async def list_cookie_accounts():
    """获取所有已保存的Cookie账号列表"""
    try:
        accounts = cookie_service.list_accounts()
        return {"success": True, "accounts": accounts}
    except Exception as e:
        logger.error(f"列出Cookie账号时出错: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"无法获取账号列表: {e}")

@app.post("/api/cookies/add")
async def add_cookie_account(request: CookieAccountRequest, background_tasks: BackgroundTasks):
    """添加一个新的Cookie账号（启动浏览器进行登录）"""
    # 使用后台任务来运行阻塞的浏览器操作，避免API超时
    background_tasks.add_task(cookie_service.add_account, request.account_name)
    return {
        "success": True, 
        "message": f"已启动为账号 '{request.account_name}' 添加Cookie的后台任务。请在弹出的浏览器窗口中完成登录。"
    }

@app.post("/api/cookies/delete")
async def delete_cookie_account(request: CookieAccountRequest):
    """删除一个指定的Cookie账号"""
    try:
        result = cookie_service.delete_account(request.account_name)
        return result
    except Exception as e:
        logger.error(f"删除Cookie账号 '{request.account_name}' 时出错: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"删除账号时出错: {e}")

@app.post("/api/cookies/validate")
async def validate_cookie_account(request: CookieAccountRequest):
    """验证指定Cookie账号的有效性"""
    try:
        result = cookie_service.validate_account(request.account_name)
        return result
    except Exception as e:
        logger.error(f"验证Cookie账号 '{request.account_name}' 时出错: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"验证账号时出错: {e}")

@app.post("/api/cookies/set_active")
async def set_active_cookie_account(request: CookieAccountRequest):
    """设置当前活动的Cookie账号"""
    try:
        result = cookie_service.set_active_account(request.account_name)
        if not result.get("success"):
            raise HTTPException(status_code=404, detail=result.get("message"))
        return result
    except Exception as e:
        logger.error(f"设置活动Cookie账号 '{request.account_name}' 时出错: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"设置活动账号时出错: {e}")

@app.get("/api/cookies/get_active")
async def get_active_cookie_account():
    """获取当前活动的Cookie账号"""
    try:
        active_account = cookie_service.get_active_account()
        return {"success": True, "active_account": active_account}
    except Exception as e:
        logger.error(f"获取活动Cookie账号时出错: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"获取活动账号时出错: {e}")

@app.post("/api/publish/xhs")
async def publish_to_xiaohongshu(request: XHSPublishRequest):
    """发布内容到小红书"""
    try:
        publisher = XHSPublisher()
        result = publisher.publish_note(
            title=request.title,
            content=request.content,
            topics=request.topics,
            location=request.location,
            images=request.images,
            videos=request.videos
        )
        
        if not result["success"]:
            logger.error(f"发布到小红书失败: {result['message']}")
            raise HTTPException(
                status_code=500, 
                detail=f"发布失败: {result['message']}"
            )
        
        return result
    except Exception as e:
        logger.error(f"发布到小红书时出错: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail=f"发布过程出错: {str(e)}"
        )

@app.get("/api/images/{image_name}")
async def get_image(image_name: str):
    """获取图片文件"""
    # 构建图片路径
    image_path = os.path.join(IMAGE_OUTPUT_DIR, image_name)
    
    # 检查文件是否存在
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail=f"图片不存在: {image_name}")
    
    # 返回图片文件
    return FileResponse(image_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.app.main:app", host="0.0.0.0", port=port, reload=True)