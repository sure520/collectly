# AI 驱动的大模型/Agent/RAG/多模态个人知识收藏与检索管家

## 项目概述

本项目是一个基于 AI 驱动的个人知识管理工具，实现跨平台收藏内容的统一解析、结构化存储、智能语义检索与高效学习管理。

### 核心功能

- **统一管理**：整合六大平台（抖音、小红书、公众号、B站、知乎、CSDN）收藏/点赞内容
- **智能解析**：自动抓取、解析不同平台内容，通过 AI 实现内容结构化处理
- **精准检索**：基于 RAG 架构实现语义检索，支持自然语言提问、多维度筛选
- **高效学习**：提供结构化摘要、知识点提炼、学习状态管理

## 技术架构

### 后端技术栈

- **框架**：FastAPI + Uvicorn
- **数据库**：SQLite（关系型数据）+ 内存存储（向量数据）
- **API 集成**：TikHub API（跨平台内容解析）
- **日志**：Python logging 模块

### 前端技术栈

- **框架**：React 18 + TypeScript
- **路由**：React Router 6
- **样式**：Tailwind CSS
- **图表**：Recharts
- **图标**：Lucide React

## 项目结构

```
collectly/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py          # API 路由定义
│   │   ├── models/
│   │   │   └── schemas.py         # 数据模型和验证
│   │   ├── services/
│   │   │   ├── platform_parser.py # 平台链接解析服务
│   │   │   ├── content_manager.py  # 内容存储和管理服务
│   │   │   ├── search_engine.py    # 搜索引擎服务
│   │   │   └── learning_manager.py # 学习管理服务
│   │   ├── utils/
│   │   │   ├── config.py          # 配置管理
│   │   │   ├── logger.py          # 日志工具
│   │   │   └── exceptions.py      # 异常处理
│   │   └── main.py                 # 应用入口
│   └── tests/                      # 后端测试脚本
├── src/                            # 前端源码
├── docs/                           # 文档
├── start.bat                       # Windows 启动脚本
├── start.ps1                       # PowerShell 启动脚本
├── Dockerfile                      # Docker 构建文件
├── docker-compose.yml              # Docker Compose 配置
├── deploy.ps1                      # 一键部署脚本 (Windows)
├── deploy.sh                       # 一键部署脚本 (Linux/macOS)
├── .env.example                    # 环境变量模板
├── requirements.txt                # Python 依赖
└── pyproject.toml                  # Python 项目配置
```

## 快速开始

### 环境要求

- Python 3.9+
- Node.js 16+
- npm 或 yarn

### 后端设置

1. 安装依赖（在项目根目录）：
   ```bash
   pip install -r requirements.txt
   ```

2. 配置环境变量：
   编辑项目根目录的 `.env` 文件（可从 `.env.example` 复制），添加必要的 API 密钥：
   ```
   TIKHUB_API_KEY=your_api_key
   DASHSCOPE_API_KEY=your_api_key
   ```

3. 启动后端服务：
   ```bash
   python -m uvicorn backend.app.main:app --reload --port 8000
   ```

### 前端设置

1. 进入项目根目录：
   ```bash
   cd collectly
   ```

2. 安装依赖：
   ```bash
   npm install
   ```

3. 启动开发服务器：
   ```bash
   npm run dev
   ```

4. 访问应用：
   打开浏览器访问 `http://localhost:3000`

## API 文档

### 基础信息

- **Base URL**: `http://localhost:8000/api`
- **Content-Type**: `application/json`

### 端点列表

#### 1. 解析链接

**POST** `/parse-link`

解析平台链接，提取内容。

Request Body:
```json
{
  "url": "https://zhihu.com/article/xxxx"
}
```

Response:
```json
{
  "title": "文章标题",
  "content": "文章内容",
  "author": "作者",
  "update": "2024-01-01",
  "create_time": "2024-01-01",
  "url": "原文链接",
  "source": "知乎",
  "tags": ["大模型", "教程"],
  "knowledge_points": ["RAG", "向量库"],
  "summary": "摘要内容"
}
```

#### 2. 批量解析链接

**POST** `/parse-links`

批量解析平台链接。

Request Body:
```json
[
  {"url": "https://zhihu.com/article/xxxx"},
  {"url": "https://bilibili.com/video/xxxx"}
]
```

#### 3. 保存内容

**POST** `/save-content`

保存解析后的内容。

Request Body: 同 `/parse-link` 的 Response

Response:
```json
{
  "content_id": "内容ID",
  "message": "保存成功"
}
```

#### 4. 搜索内容

**POST** `/search`

智能检索内容。

Request Body:
```json
{
  "text": "RAG 优化方法",
  "domains": ["大模型", "RAG"],
  "sources": ["知乎", "B站"],
  "difficulty": "进阶",
  "content_type": "教程",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "learning_status": "未读"
}
```

#### 5. 更新学习状态

**PUT** `/update-learning-status`

更新内容的学习状态。

Request Body:
```json
{
  "content_id": "内容ID",
  "status": "已读"
}
```

#### 6. 更新标签

**PUT** `/update-tags`

更新内容的标签。

Request Body:
```json
{
  "content_id": "内容ID",
  "tags": ["大模型", "进阶", "教程"]
}
```

#### 7. 更新笔记

**PUT** `/update-note`

更新内容的笔记。

Request Body:
```json
{
  "content_id": "内容ID",
  "note": "这是我的学习笔记"
}
```

#### 8. 获取内容详情

**GET** `/content/{content_id}`

获取指定内容的详细信息。

#### 9. 获取学习统计

**GET** `/learning-stats`

获取学习统计数据。

Response:
```json
{
  "total_count": 100,
  "status_counts": {
    "未读": 50,
    "已读": 30,
    "重点": 15,
    "待复习": 5
  },
  "source_counts": {
    "知乎": 40,
    "B站": 30,
    "抖音": 20,
    "小红书": 10
  },
  "domain_counts": {
    "大模型": 35,
    "Agent": 25,
    "RAG": 30,
    "多模态": 10
  },
  "progress": 30.0
}
```

## 功能模块说明

### 1. 平台链接解析模块

支持解析以下六大平台的内容：

| 平台 | 解析内容 | 特殊处理 |
|------|---------|---------|
| 抖音 | 标题、作者、发布时间、简介、封面图、视频链接、AI字幕 | 短视频提取核心字幕，生成简短摘要 |
| 小红书 | 标题、作者、发布时间、正文、图片、OCR文字 | 对图片进行 OCR 识别 |
| 微信公众号 | 标题、作者、发布时间、正文、封面图 | 自动去除广告，保留核心正文 |
| B站 | 标题、UP主、发布时间、简介、封面图、视频链接、AI字幕 | 长视频生成章节总结 |
| 知乎 | 标题、作者、发布时间、回答正文、点赞数 | 优先解析高赞回答 |
| CSDN | 标题、作者、发布时间、正文、代码块、标签 | 保留代码块格式 |

### 2. 内容存储模块

- **关系型数据库**：存储结构化元数据
- **内容去重**：基于 URL 和内容哈希值自动识别重复内容
- **内容更新**：支持手动触发重新解析

### 3. 搜索模块

- **语义检索**：基于向量相似度实现语义匹配
- **关键词检索**：支持标题、摘要、知识点关键词匹配
- **多维度筛选**：领域、来源、难度、内容类型、时间、学习状态

### 4. 学习管理模块

- **学习状态**：未读、已读、重点、待复习
- **标签管理**：自动标签 + 自定义标签
- **笔记功能**：支持添加个人学习笔记
- **学习统计**：展示学习进度、各领域分布等

## 配置说明

### 环境变量

| 变量名 | 说明 | 必需 |
|--------|------|------|
| TIKHUB_API_KEY | TikHub API 密钥 | 是 |
| DASHSCOPE_API_KEY | 阿里云 DashScope API 密钥 | 是 |
| QDRANT_API_KEY | Qdrant 向量库 API 密钥 | 是 |
| QDRANT_CLUSTER_ENDPOINT | Qdrant 集群端点 | 是 |

### 日志配置

日志文件存储在项目根目录的 `logs/` 目录下，按日期命名。

日志级别：
- DEBUG：详细调试信息
- INFO：一般信息
- WARNING：警告信息
- ERROR：错误信息
- CRITICAL：严重错误

## 常见问题

### 1. 解析失败

- 检查网络连接
- 确认 API 密钥有效
- 检查链接是否有效且可访问

### 2. 搜索结果不准确

- 尝试使用更精确的搜索关键词
- 使用多维度筛选缩小范围
- 检查标签是否正确

### 3. 前端无法连接后端

- 确认后端服务已启动
- 检查 CORS 配置
- 确认端口配置正确

## 开发指南

### 添加新的平台支持

1. 在 `platform_parser.py` 中添加新的解析方法
2. 更新 `_detect_platform` 方法识别新平台
3. 在 `routes.py` 中添加对应的路由

### 添加新的功能

1. 在对应的服务模块中添加业务逻辑
2. 在 `routes.py` 中添加新的 API 端点
3. 在前端添加对应的 UI 组件和 API 调用

## 许可证

MIT License

## 联系方式

如有问题或建议，请提交 Issue 或 Pull Request。