# Collectly - 你的 AI 知识管家

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.104-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=white" alt="React">
  <img src="https://img.shields.io/badge/TypeScript-5.3-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/Tailwind_CSS-3.3-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white" alt="Tailwind CSS">
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/ChromaDB-FF6B6B?style=for-the-badge&logo=chromadb&logoColor=white" alt="ChromaDB">
  <img src="https://img.shields.io/badge/DashScope-FF6A00?style=for-the-badge&logo=alibabacloud&logoColor=white" alt="DashScope">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge&logo=opensource&logoColor=white" alt="License">
</p>

<p align="center">
  <a href="README.md">English</a> •
  <a href="#快速开始">快速开始</a> •
  <a href="#核心能力">核心能力</a> •
  <a href="#架构">架构</a> •
  <a href="#api-接口">API 接口</a>
</p>

> **"收藏"** 只是开始，**"管理"** 才是精髓。

Collectly 不只是一个内容收藏工具——它是你的**智能知识管家**，将零散的信息转化为系统化的智慧。通过 AI 驱动的管理，让你的知识资产井井有条、随时可用、持续增值。

***

## 为什么 Collectly 与众不同？

### "管理" 的哲学

与传统书签工具只**存储**不同，Collectly 通过以下方式**管理**你的知识：

- **生命周期管理** — 内容在阶段中流转：未读 → 阅读中 → 重点 → 待复习
- **智能分类** — AI 自动打标签、生成摘要、提取知识点
- **主动回忆系统** — 智能提醒需要复习的内容
- **学习分析** — 用详细洞察追踪你的知识获取旅程

## 核心能力

### 1. 全域内容捕获

无缝接入主流中文平台内容：

| 平台        | 能力        |
| --------- | --------- |
| **抖音**    | 视频语音转文字提取 |
| **小红书**   | 生活方式与产品洞察 |
| **微信公众号** | 专业博客与行业分析 |
| **B站**    | 教育视频与字幕提取 |
| **知乎**    | 专家问答与深度文章 |
| **CSDN**  | 技术教程与代码方案 |

### 2. AI 驱动的内容精炼

每篇内容自动处理：

- **智能摘要** — 200 字精华摘要，捕捉核心
- **自动标签** — 5-10 个多维度标签（技术领域、应用场景、核心概念）
- **知识点提取** — 识别关键概念与要点
- **内容去重** — 基于哈希的智能重复检测

### 3. 智能知识管理

#### 学习状态流水线

```
[未读] → [阅读中] → [重点] → [待复习]
   ↑                              ↓
   └────────── [归档] ←───────────┘
```

#### 多维度组织

- **按领域**: AI、大模型、Agent、RAG、多模态
- **按来源**: 平台级分类
- **按状态**: 学习进度追踪
- **按标签**: 自定义组织结构
- **按日期**: 时间线内容管理

### 4. 智能检索系统

精准找到所需：

- **全文搜索** — 覆盖标题、内容、摘要
- **多条件筛选** — 领域 + 来源 + 状态 + 日期范围组合
- **相关度评分** — AI 排序搜索结果
- **语义理解** — 基于向量嵌入的上下文感知内容发现

### 5. 个人知识库

- **自定义笔记** — 为任何内容添加洞察
- **标签管理** — 创建你自己的分类体系
- **学习统计** — 可视化进度追踪
- **内容集合** — 分组关联资料

## 架构

```
┌─────────────────────────────────────────────────────────────┐
│                      内容生命周期                            │
├─────────────────────────────────────────────────────────────┤
│   捕获  →  解析  →  精炼  →  存储  →  管理  →  检索        │
│    ↓        ↓        ↓        ↓        ↓          ↓        │
│  [URL]   [平台]    [LLM]   [SQLite]  [状态]    [搜索]      │
│          [API]     [AI]    [去重]    [标签]    [筛选]      │
│                    [标签]   [向量库]  [笔记]    [向量检索]  │
└─────────────────────────────────────────────────────────────┘
```

### 技术栈

| 层级           | 技术                                         |
| ------------ | ------------------------------------------ |
| **后端框架**     | FastAPI (Python)                           |
| **AI / 大模型** | DashScope (Qwen-plus, Qwen3-ASR, Qwen3-VL) |
| **向量数据库**    | ChromaDB（本地持久化）                            |
| **关系数据库**    | SQLite                                     |
| **内容解析**     | TikHub API + BeautifulSoup + Trafilatura   |
| **前端**       | React 18 + TypeScript + Tailwind CSS       |
| **UI 组件**    | Framer Motion, Lucide React, Recharts      |
| **构建工具**     | Webpack 5                                  |
| **容器化**      | Docker / Docker Compose                    |
| **部署模式**     | 本地部署 + 内网穿透 / 云服务器公网部署                     |

## 项目结构

```
collectly/
├── backend/                    # 核心 API 服务
│   ├── app/
│   │   ├── api/routes.py       # RESTful 接口
│   │   ├── models/schemas.py   # 数据模型
│   │   ├── services/
│   │   │   ├── platform_parser.py     # 多平台解析器
│   │   │   ├── content_manager.py     # 存储与去重
│   │   │   ├── search_engine.py       # 智能搜索
│   │   │   ├── learning_manager.py    # 状态与进度追踪
│   │   │   ├── llm_service.py         # DashScope AI 集成
│   │   │   └── vector_service.py      # 向量嵌入与语义搜索
│   │   └── utils/
│   └── tests/
│
├── python-parser/              # 独立解析服务
│   ├── main.py
│   ├── content_extractor.py
│   ├── summarizer.py
│   └── requirements.txt
│
├── src/                        # React 前端
│   ├── components/             # UI 组件
│   ├── hooks/                  # React Hooks
│   ├── utils/                  # 前端工具
│   └── types/                  # TypeScript 类型
│
├── functions/                  # Supabase Edge Functions
│
├── tests/                      # 平台特定测试
│
├── .wiki/                      # 项目文档 Wiki
│
├── start.bat                   # Windows CMD 启动脚本
├── start.ps1                   # PowerShell 启动脚本
├── start.sh                    # Linux/macOS 启动脚本
├── Dockerfile                  # Docker 构建文件
├── docker-compose.yml          # Docker Compose 配置
├── deploy.ps1                  # 一键部署脚本 (Windows PowerShell)
├── deploy.sh                   # 一键部署脚本 (Linux/macOS)
├── deploy-local.ps1            # 本地交互式部署 (Windows)
├── deploy-local.sh             # 本地交互式部署 (Linux/macOS)
├── .env.example                # 环境变量模板
├── requirements.txt            # Python 依赖
└── pyproject.toml              # Python 项目配置
```

## 快速开始

### 环境要求

| 依赖                               | 版本  | 用途                   |
| -------------------------------- | --- | -------------------- |
| [uv](https://docs.astral.sh/uv/) | 最新  | Python 包管理器 & 虚拟环境管理 |
| Node.js                          | 16+ | 前端构建                 |
| TikHub API 密钥                    | —   | 平台内容接入               |
| DashScope API 密钥                 | —   | AI 能力（LLM、ASR、视觉、嵌入） |

**安装 uv：**

```powershell
# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 方式一：一键部署脚本（推荐）

#### Windows 用户

```powershell
# 克隆仓库
git clone <仓库地址>
cd collectly

# 方案 A：本地部署 + 内网穿透（个人电脑使用）
.\deploy.ps1 -Mode A

# 方案 B：云服务器公网部署（24 小时在线）
.\deploy.ps1 -Mode B
```

#### Linux/macOS 用户

```bash
# 克隆仓库
git clone <仓库地址>
cd collectly

# 方案 A：本地部署 + 内网穿透
./deploy.sh --mode A

# 方案 B：云服务器公网部署
./deploy.sh --mode B
```

**部署脚本自动完成：**

- ✅ 环境检查（uv、Node.js）
- ✅ 虚拟环境创建 & 依赖同步（通过 uv）
- ✅ 依赖安装（前后端）
- ✅ 环境变量配置
- ✅ 后端服务启动
- ✅ 前端静态资源构建
- ✅ 内网穿透配置（方案 A）/ Nginx 配置指导（方案 B）

### 方式二：Docker 部署

```bash
# 克隆仓库
git clone <仓库地址>
cd collectly

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入 API 密钥

# 一键启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

访问地址：

- 前端：<http://localhost:3266>
- 后端 API：<http://localhost:8000>
- API 文档：<http://localhost:8000/docs>

### 方式三：手动安装（开发模式）

```bash
# 克隆仓库
git clone <仓库地址>
cd collectly

# 安装 uv（如未安装）
# Windows: powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
# Linux/macOS: curl -LsSf https://astral.sh/uv/install.sh | sh

# 同步虚拟环境和依赖
uv sync

# 配置环境
cp .env.example .env
# 编辑 .env 填入你的 API 密钥

# 启动后端（终端 1）
.\start.bat   # Windows CMD
# 或
.\start.ps1   # Windows PowerShell
# 或
./start.sh    # Linux/macOS
# 或
uv run uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

# 构建并启动前端（终端 2）
npm install
npm run dev
```

访问地址：

- 前端：<http://localhost:3266>
- 后端 API：<http://localhost:8000>
- API 文档：<http://localhost:8000/docs>

## API 接口

### 认证

| 接口                 | 方法   | 说明             |
| ------------------ | ---- | -------------- |
| `/api/auth/status` | GET  | 检查是否需要认证       |
| `/api/auth/login`  | POST | 使用访问密码登录       |
| `/api/auth/verify` | GET  | 验证当前 Token 有效性 |

### 内容管理

| 接口                  | 方法   | 说明              |
| ------------------- | ---- | --------------- |
| `/api/parse-link`   | POST | 解析单个链接          |
| `/api/parse-links`  | POST | 批量解析链接          |
| `/api/save-content` | POST | 保存到知识库          |
| `/api/content/{id}` | GET  | 获取内容详情          |
| `/api/clean-urls`   | POST | 清理并提取原始文本中的 URL |

### 知识管理

| 接口                            | 方法  | 说明     |
| ----------------------------- | --- | ------ |
| `/api/update-learning-status` | PUT | 更新内容状态 |
| `/api/update-tags`            | PUT | 修改标签   |
| `/api/update-note`            | PUT | 添加个人笔记 |
| `/api/learning-stats`         | GET | 查看进度分析 |

### 搜索

| 接口            | 方法   | 说明    |
| ------------- | ---- | ----- |
| `/api/search` | POST | 多条件搜索 |

## 配置说明

```env
# TikHub API
TIKHUB_API_KEY=your_key
TIKHUB_API_URL=https://api.tikhub.io

# DashScope（阿里云）大模型
DASHSCOPE_API_KEY=your_key

# 模型配置
LLM_MODEL_NAME=qwen-plus
ASR_MODEL_NAME=qwen3-asr-flash
VISION_MODEL_NAME=qwen3-vl-flash
EMBEDDING_MODEL=text-embedding-v4

# 应用设置
APP_NAME="Collectly - AI 知识管家"
DEBUG=false
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# 访问控制
ACCESS_PASSWORD=your_password
TOKEN_EXPIRE_HOURS=24
```

## "管理" 的差异

| 特性 | 传统书签   | Collectly     |
| -- | ------ | ------------- |
| 存储 | 保存 URL | 全文内容提取        |
| 组织 | 手动文件夹  | AI 自动分类       |
| 发现 | 手动浏览   | 智能搜索 + 筛选     |
| 留存 | 静态     | 学习状态追踪        |
| 洞察 | 无      | 学习分析          |
| 复习 | 手动     | 定时回忆系统        |
| 搜索 | 仅标题    | 全文搜索 + 语义向量检索 |

## 开发指南

```bash
# 运行测试
cd backend
pytest tests/

# 测试特定平台
python tests/test_douyin.py
python tests/test_zhihu.py
```

## 开源协议

MIT License

## 致谢

- [TikHub](https://api.tikhub.io) — 多平台内容接入
- [DashScope](https://dashscope.aliyun.com) — 大模型、语音、视觉与嵌入能力
- [FastAPI](https://fastapi.tiangolo.com) — Web 框架
- [ChromaDB](https://www.trychroma.com) — 向量数据库
- [React](https://react.dev) — 前端框架

***

> **Collectly** — 将信息过载转化为有序智慧。

