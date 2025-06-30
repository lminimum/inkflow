# inkflow
一个基于 Vue 的 AI 内容创作与自动发布系统，支持文章生成、编辑与多平台投放自动化。

## 项目概述
inkflow 旨在通过 AI 技术提升内容创作效率，实现从文章生成到多平台发布的全流程自动化。系统集成了多种 AI 模型提供商，支持自定义模板与发布规则，满足不同场景下的内容创作需求。

## 核心功能
- **AI 内容生成**：集成 Ollama、DeepSeek、SiliconFlow、阿里云百炼等多平台 AI 模型
- **可视化编辑**：直观的富文本编辑器，支持内容格式化与多媒体插入
- **多平台发布**：一键发布至主流内容平台（需配置对应 API 密钥）
- **模板系统**：自定义文章模板，统一内容风格与格式
- **任务调度**：定时发布与批量操作，提升运营效率

## 技术栈
- **前端**：Vue 3、TypeScript、Vite、Pinia、Vue Router
- **后端**：Python、FastAPI、LangChain
- **AI 集成**：Ollama API、DeepSeek API、SiliconFlow API、阿里云百炼 API
- **数据库**：（待集成）
- **部署**：Docker（规划中）

## 快速开始
### 环境要求
- Node.js 16+ 
- Python 3.8+
- pip 21+
- npm 7+

### 安装步骤
#### 1. 克隆仓库
```bash
git clone https://github.com/yourusername/inkflow.git
cd inkflow
```

#### 2. 后端设置
```bash
cd ink-backend
pip install -r requirements.txt
# 配置环境变量
cp .env.example .env
# 编辑 .env 文件添加必要的 API 密钥
```

#### 3. 前端设置
```bash
cd ../ink-vue
npm install
# 配置环境变量
cp .env.example .env
# 编辑 .env 文件设置后端 API 地址
```

### 配置 AI 服务
修改 `ink-backend/ai_services.json` 配置文件，添加或调整 AI 服务提供商：
```json
{
  "services": [
    {
      "name": "ollama",
      "type": "ollama",
      "base_url": "https://ollama.campus.lk233.link/api",
      "models": ["deepseek-r1:14b", "huihui_ai/gemma3-abliterated:latest"],
      "api_key_required": false
    },
    // 其他 AI 服务配置...
  ]
}
```

### 启动服务
#### 后端服务
```bash
cd ink-backend
python main.py
# 或使用启动脚本
node ../start-backend.js
```

#### 前端服务
```bash
cd ink-vue
npm run dev
# 或使用启动脚本
node ../start-frontend.js
```

## 测试
运行后端单元测试：
```bash
cd ink-backend
pytest test_api.py
```

## 项目结构
```
inkflow/
├── ink-backend/        # Python 后端服务
│   ├── ai_providers.py # AI 服务提供商实现
│   ├── ai_services.json # AI 服务配置
│   ├── main.py         # FastAPI 应用入口
│   └── test_api.py     # API 测试用例
├── ink-vue/            # Vue 前端应用
│   ├── src/            # 源代码目录
│   └── public/         # 静态资源
└── start-*.js          # 启动脚本
```

## 许可证
[MIT](LICENSE)
