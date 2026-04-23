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
│   ├── tests/
│   └── requirements.txt
│
├── python-parser/              # 独立解析服务
│   ├── main.py
│   ├── content_extractor.py
│   ├── summarizer.py
│   └── requirements.txt
│
└── tests/                      # 平台特定测试
```

## 快速开始

### 环境要求
- Python 3.8+
- TikHub API 密钥（平台接入）
- DashScope API 密钥（AI 能力）

### 安装步骤

```bash
# 克隆仓库
git clone <仓库地址>
cd collectly

# 设置后端
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 配置环境
cp .env.example .env
# 编辑 .env 填入你的 API 密钥

# 启动服务
python -m app.main
```

API 服务地址 `http://localhost:8000`

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
