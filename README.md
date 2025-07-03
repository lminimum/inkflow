# inkflow
一个基于 Electron + Vue3 的 AI 内容创作与自动发布系统，支持文章生成、编辑与多平台投放自动化，拥有美观的吸血鬼暗色主题桌面端体验。

## 项目概述
inkflow 致力于通过 AI 技术提升内容创作效率，实现从文章生成到多平台发布的全流程自动化。系统集成多种 AI 模型，支持自定义模板与发布规则，适用于多场景内容创作。

## 核心功能
- **AI 内容生成**：集成 Ollama、DeepSeek、SiliconFlow、阿里云百炼等多平台 AI 模型
- **桌面端体验**：Electron 打包，支持 Windows/macOS/Linux，原生窗口自定义、吸血鬼暗色主题
- **可视化编辑**：富文本编辑器，支持内容格式化与多媒体插入
- **多平台发布**：一键发布至主流内容平台（需配置 API 密钥）
- **模板系统**：自定义文章模板，统一内容风格与格式
- **任务调度**：定时发布与批量操作，提升运营效率

## 技术栈
- **桌面端**：Electron、Vue 3、TypeScript、Vite、Pinia、Vue Router、Ant Design Vue
- **后端**：Python、FastAPI、LangChain
- **AI 集成**：Ollama API、DeepSeek API、SiliconFlow API、阿里云百炼 API
- **数据库**：（规划中）
- **部署**：Docker（规划中）

## 目录结构
```
inkflow/
├── ink-backend/            # Python 后端服务
│   ├── src/                # FastAPI 应用与服务实现
│   ├── requirements.txt    # 后端依赖
│   └── ...
├── ink-electron-vue/       # Electron+Vue3 桌面端
│   ├── src/                # 前端源码（renderer、主进程、预加载等）
│   ├── package.json        # 前端依赖
│   └── ...
├── start-backend.js        # 后端启动脚本
├── start-frontend.js       # 前端启动脚本（如需）
└── README.md
```

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

#### 3. 桌面端（Electron+Vue）设置
```bash
cd ../ink-electron-vue
npm install
# 配置环境变量（如需）
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
    }
    // 其他 AI 服务配置...
  ]
}
```

### 启动服务
#### 后端服务
```bash
cd ink-backend
python src/app/main.py
# 或使用启动脚本
node ../start-backend.js
```

#### 桌面端（Electron+Vue）
```bash
cd ink-electron-vue
npm run dev # 开发模式
# 或
npm run build && npm run start # 生产模式
```

## 测试
运行后端单元测试：
```bash
cd ink-backend
pytest tests/test_api.py
```

## 特色亮点
- **吸血鬼暗色主题**，更具美感与层次感
- **自定义窗口栏与原生按钮**，桌面端体验极佳
- **AI 内容生成与多平台自动发布**
- **支持浏览器和桌面端双模式访问**（桌面端有更多原生特性）

## 许可证
[MIT](LICENSE)
