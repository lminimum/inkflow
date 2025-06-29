import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_ollama import OllamaLLM
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

# Ollama配置
OLLAMA_BASE_URL = "https://ollama.campus.lk233.link/"

# 请求模型定义
class GenerateRequest(BaseModel):
    prompt: str
    model: str

@app.get("/")
async def read_root():
    return {"message": "AI Content Creation Backend is running!"}

@app.get("/api/models")
async def get_models():
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}v1/models")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch models list: {str(e)}")

@app.post("/api/generate")
async def generate_content(request: GenerateRequest):
    if not request.prompt or not request.model:
        raise HTTPException(status_code=400, detail="Prompt and model are required")

    try:
        # 初始化Ollama模型
        llm = OllamaLLM(
            base_url=OLLAMA_BASE_URL,
            model=request.model,
            timeout=30
        )

        # 调用模型生成内容
        result = llm.invoke(request.prompt)
        return {"content": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate content: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)