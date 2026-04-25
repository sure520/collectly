# Collectly - 你的 AI 知识管家

> **"收藏"** 只是开始，**"管理"** 才是精髓。

Collectly 不只是一个内容收藏工具——它是你的**智能知识管家**，将零散的信息转化为系统化的智慧。通过 AI 驱动的管理，让你的知识资产井井有条、随时可用、持续增值。

## 为什么 Collectly 与众不同？

### "管理" 的哲学

与传统书签工具只**存储**不同，Collectly 通过以下方式**管理**你的知识：

- **生命周期管理** - 内容在阶段中流转：未读 → 阅读中 → 重点 → 待复习
- **智能分类** - AI 自动打标签、生成摘要、提取知识点
- **主动回忆系统** - 智能提醒需要复习的内容
- **学习分析** - 用详细洞察追踪你的知识获取旅程

## 核心能力

### 1. 全域内容捕获
无缝接入主流中文平台内容：
- **抖音** - 视频语音转文字提取
- **小红书** - 生活方式与产品洞察
- **微信公众号** - 专业博客与行业分析
- **B站** - 教育视频与字幕提取
- **知乎** - 专家问答与深度文章
- **CSDN** - 技术教程与代码方案

### 2. AI 驱动的内容精炼
每篇内容自动处理：
- **智能摘要** - 200 字精华摘要，捕捉核心
- **自动标签** - 5-10 个多维度标签（技术领域、应用场景、核心概念）
- **知识点提取** - 识别关键概念与要点
- **内容去重** - 基于哈希的智能重复检测

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
- **全文搜索** - 覆盖标题、内容、摘要
- **多条件筛选** - 领域 + 来源 + 状态 + 日期范围组合
- **相关度评分** - AI 排序搜索结果
- **语义理解** - 上下文感知的内容发现

### 5. 个人知识库
- **自定义笔记** - 为任何内容添加洞察
- **标签管理** - 创建你自己的分类体系
- **学习统计** - 可视化进度追踪
- **内容集合** - 分组关联资料

## 架构亮点

```
┌─────────────────────────────────────────────────────────────┐
│                      内容生命周期                            │
├─────────────────────────────────────────────────────────────┤
│   捕获  →  解析  →  精炼  →  存储  →  管理  →  检索        │
│    ↓        ↓        ↓        ↓        ↓          ↓        │
│  [URL]   [平台]    [LLM]   [SQLite]  [状态]    [搜索]      │
│          [API]     [AI]    [去重]    [标签]    [筛选]      │
│                    [标签]            [笔记]                │
└─────────────────────────────────────────────────────────────┘
```

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
│   │   │   └── llm_service.py         # DashScope AI 集成
│   │   └── utils/
│   └── tests/
│
├── python-parser/              # 独立解析服务
│   ├── main.py
│   ├── content_extractor.py
│   ├── summarizer.py
│   └── requirements.txt
│
├── tests/                      # 平台特定测试
│
├── start.bat                   # Windows 启动脚本
├── start.ps1                   # PowerShell 启动脚本
├── Dockerfile                  # Docker 构建文件
├── docker-compose.yml          # Docker Compose 配置
├── deploy.ps1                  # 一键部署脚本 (Windows)
├── deploy.sh                   # 一键部署脚本 (Linux/macOS)
├── .env.example                # 环境变量模板
├── requirements.txt            # Python 依赖
└── pyproject.toml              # Python 项目配置
```

## 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+（前端构建）
- TikHub API 密钥（平台接入）
- DashScope API 密钥（AI 能力）

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
- ✅ 环境检查（Python、Node.js）
- ✅ 虚拟环境创建
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
- 前端：http://localhost:3266
- 后端 API：http://localhost:8000
- API 文档：http://localhost:8000/docs

### 方式三：手动安装（开发模式）

```bash
# 克隆仓库
git clone <仓库地址>
cd collectly

# 设置后端
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt

# 配置环境
cp .env.example .env
# 编辑 .env 填入你的 API 密钥

# 启动后端（终端 1）
.\start.bat  # Windows
# 或
.\start.ps1  # PowerShell
# 或
python -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

# 构建并启动前端（终端 2）
cd ..
npm install
npm run dev
```

访问地址：
- 前端：http://localhost:3266
- 后端 API：http://localhost:8000
- API 文档：http://localhost:8000/docs

## API 接口

### 内容管理
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/parse-link` | POST | 解析单个链接 |
| `/api/parse-links` | POST | 批量解析链接 |
| `/api/save-content` | POST | 保存到知识库 |
| `/api/content/{id}` | GET | 获取内容详情 |

### 知识管理
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/update-learning-status` | PUT | 更新内容状态 |
| `/api/update-tags` | PUT | 修改标签 |
| `/api/update-note` | PUT | 添加个人笔记 |
| `/api/learning-stats` | GET | 查看进度分析 |

### 搜索
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/search` | POST | 多条件搜索 |

## 配置说明

```env
# TikHub API
TIKHUB_API_KEY=your_key
TIKHUB_API_URL=https://api.tikhub.io

# DashScope（阿里云）大模型
DASHSCOPE_API_KEY=your_key

# 应用设置
APP_NAME="Collectly - AI 知识管家"
DEBUG=false
```

## "管理" 的差异

| 特性 | 传统书签 | Collectly |
|------|---------|-----------|
| 存储 | 保存 URL | 全文内容提取 |
| 组织 | 手动文件夹 | AI 自动分类 |
| 发现 | 手动浏览 | 智能搜索 + 筛选 |
| 留存 | 静态 | 学习状态追踪 |
| 洞察 | 无 | 学习分析 |
| 复习 | 手动 | 定时回忆系统 |

## 开发指南

```bash
# 运行测试
cd backend
pytest tests/

# 测试特定平台
python tests/test_douyin.py
python tests/test_zhihu.py
```

## 技术栈

- **框架**: FastAPI
- **数据库**: SQLite 自定义 schema
- **AI/大模型**: DashScope (Qwen-plus)
- **解析**: TikHub API + BeautifulSoup
- **语音转文字**: Qwen3-ASR
- **模型**: Pydantic

## 开源协议

MIT License

## 致谢

- [TikHub](https://api.tikhub.io) - 多平台内容接入
- [DashScope](https://dashscope.aliyun.com) - 大模型能力
- [FastAPI](https://fastapi.tiangolo.com) - Web 框架

---

> **Collectly** - 将信息过载转化为有序智慧。
