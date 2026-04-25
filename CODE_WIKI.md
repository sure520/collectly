
# Collectly - Code Wiki

## 1. 项目概述

### 1.1 项目简介

**Collectly** 是一个 AI 驱动的知识管家，专为收集、管理、检索和学习来自主流中文平台的内容而设计。它通过自动化的内容解析、AI 智能提炼和学习状态管理，将零散信息转化为系统化的知识体系。

**主要特点：**
- 多平台内容统一收集（抖音、小红书、微信公众号、B站、知乎、CSDN）
- AI 驱动的内容智能提炼（摘要生成、标签分类、知识点提取）
- 学习状态全流程管理
- 智能检索与个性化推荐
- 完整的个人知识体系构建

### 1.2 技术栈

| 层级 | 技术 | 版本/说明 |
|------|------|----------|
| **后端框架** | FastAPI | 0.104.1 |
| **AI 服务** | 阿里云 DashScope (通义千问) | qwen-plus 模型 |
| **数据库** | SQLite | 嵌入式关系型数据库 |
| **语音识别** | DashScope ASR | qwen3-asr-flash |
| **前端框架** | React | 18.2.0 |
| **前端 UI** | Tailwind CSS | 3.3.5 |
| **前端路由** | React Router | 6.8.0 |
| **内容解析** | TikHub API | 1.0.3+ |
| **构建工具** | Webpack | 5.106.2 |
| **开发语言** | Python 3.8+ / TypeScript 5.3.3 |

### 1.3 项目许可证

MIT License

---

## 2. 项目架构

### 2.1 系统架构图

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              用户界面 (Frontend)                             │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────┐  ┌─────────────┐        │
│  │  Dashboard  │  │  Link Input  │  │  Search   │  │   Stats     │        │
│  └─────────────┘  └──────────────┘  └───────────┘  └─────────────┘        │
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           RESTful API (FastAPI)                             │
│  ┌──────────────┐ ┌─────────────────┐ ┌───────────────┐ ┌──────────────┐  │
│  │ /parse-link  │ │ /parse-links    │ │ /save-content │ │ /search      │  │
│  │ /content/{id}│ │ /update-status  │ │ /update-tags  │ │ /update-note│  │
│  └──────────────┘ └─────────────────┘ └───────────────┘ └──────────────┘  │
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    │
            ┌───────────────────────┼───────────────────────┐
            ▼                       ▼                       ▼
┌───────────────────────┐  ┌───────────────────────┐  ┌───────────────────────┐
│  Platform Parser      │  │  Content Manager      │  │  LLM Service          │
│  - 抖音解析           │  │  - 存储管理          │  │  - 摘要生成          │
│  - 小红书解析         │  │  - 去重检测          │  │  - 标签生成          │
│  - 微信公众号解析     │  │  - CRUD 操作         │  │  - 知识点提取        │
│  - B站解析            │  └───────────────────────┘  │  - 语音转文字        │
│  - 知乎解析           │                             └───────────────────────┘
│  - CSDN解析           │
└───────────────────────┘                             ┌───────────────────────┐
            │                                          │  Search Engine        │
            ▼                                          │  - 全文检索          │
┌───────────────────────┐                             │  - 多条件筛选        │
│  Learning Manager     │                             │  - 相关度计算        │
│  - 状态管理           │                             └───────────────────────┘
│  - 笔记管理           │
│  - 统计分析           │
└───────────────────────┘
            │
            ▼
┌───────────────────────┐
│   SQLite Database     │
│  - content 表         │
│  - learning_status 表 │
└───────────────────────┘
```

### 2.2 核心流程

#### 内容收集流程

```
用户输入链接
       │
       ▼
平台检测与识别
       │
       ▼
调用 TikHub API 解析内容
       │
       ▼
提取原始内容（文本/视频语音转文字）
       │
       ▼
调用 LLM Service 处理
       │
       ├─→ 生成摘要
       ├─→ 生成标签
       └─→ 提取知识点
       │
       ▼
返回完整 ContentResponse
       │
       ▼
保存到数据库（检测去重）
       │
       ▼
初始化学习状态为 "未读"
```

#### 内容生命周期管理

```
[未读] → [阅读中] → [重点] → [待复习]
   ↑                                         ↓
   └─────────────── [归档] ←──────────────────┘
```

---

## 3. 目录结构

### 3.1 根目录结构

```
/workspace/
├── backend/                # 后端代码
├── src/                    # 前端源代码
├── docs/                   # 文档
│   ├── api_response_format/  # API 响应格式示例
│   └── IMPLEMENTATION.md    # 实现说明
├── assets/                 # 静态资源
├── .venv/                  # Python 虚拟环境
├── pyproject.toml          # Python 项目配置
├── package.json            # Node.js 项目配置
├── tsconfig.json           # TypeScript 配置
├── webpack.config.js       # Webpack 配置
├── tailwind.config.js      # Tailwind CSS 配置
├── postcss.config.js       # PostCSS 配置
├── README.md               # 英文说明文档
└── READMEzh.md             # 中文说明文档
```

### 3.2 后端目录详解

```
/workspace/backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 应用入口
│   ├── api/
│   │   └── routes.py           # 路由定义
│   ├── models/
│   │   └── schemas.py          # Pydantic 数据模型
│   ├── services/
│   │   ├── platform_parser.py  # 多平台解析器
│   │   ├── content_manager.py  # 内容管理器
│   │   ├── search_engine.py    # 搜索引擎
│   │   ├── learning_manager.py # 学习管理器
│   │   ├── llm_service.py      # LLM 服务
│   │   └── README_LLM.md       # LLM 服务说明
│   └── utils/
│       ├── config.py           # 配置管理
│       ├── logger.py           # 日志工具
│       └── exceptions.py       # 异常处理
├── tests/                      # 测试文件
│   ├── test_parser.py
│   ├── test_content_manager.py
│   ├── test_learning_manager.py
│   └── ...
├── examples/                   # 示例代码
├── requirements.txt            # Python 依赖
├── start.bat                   # Windows 启动脚本
└── start.ps1                   # PowerShell 启动脚本
```

### 3.3 前端目录详解

```
/workspace/src/
├── index.tsx                   # React 入口
├── App.tsx                     # 主应用组件
├── styles/
│   └── index.css               # 全局样式
├── components/                 # React 组件
│   ├── Layout.tsx              # 布局组件
│   ├── Dashboard.tsx           # 仪表板
│   ├── LinkInput.tsx           # 链接输入组件
│   ├── KnowledgeList.tsx       # 知识列表
│   ├── KnowledgeCard.tsx       # 知识卡片
│   ├── DetailModal.tsx         # 详情弹窗
│   ├── Search.tsx              # 搜索组件
│   ├── FilterPanel.tsx         # 筛选面板
│   ├── Stats.tsx               # 统计组件
│   ├── Settings.tsx            # 设置组件
│   └── Auth.tsx                # 认证组件（未使用）
├── hooks/                      # React Hooks
│   ├── useAuth.ts              # 认证 Hook（未使用）
│   ├── useKnowledge.ts         # 知识管理 Hook
│   └── useTheme.ts             # 主题 Hook
├── utils/                      # 工具函数
│   ├── api.ts                  # API 调用封装
│   ├── types.ts                # 类型定义
│   ├── format.ts               # 格式化工具
│   └── platform.ts             # 平台工具
├── types/                      # 类型定义
│   └── index.ts                # 类型声明
└── supabase/                   # Supabase 相关（未使用）
    ├── client.ts
    └── types.ts
```

---

## 4. 核心模块说明

### 4.1 后端核心模块

#### 4.1.1 应用入口 ([`backend/app/main.py`](file:///workspace/backend/app/main.py))

**功能：** FastAPI 应用的主入口点，配置路由、中间件和生命周期

**核心组件：**
- `app = FastAPI()` - 初始化 FastAPI 应用
- 配置 CORS 中间件（允许所有来源）
- 注册异常处理器
- 挂载 `/api` 路由
- 提供 `/health` 健康检查端点

**启动命令：**
```bash
cd backend
python -m app.main
# 或
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 4.1.2 路由模块 ([`backend/app/api/routes.py`](file:///workspace/backend/app/api/routes.py))

**功能：** 定义所有 RESTful API 端点

**API 端点列表：**

| 方法 | 路径 | 描述 | 请求体 | 响应 |
|------|------|------|--------|------|
| POST | `/parse-link` | 解析单个链接 | `{ url: string }` | `ContentResponse` |
| POST | `/parse-links` | 批量解析链接 | `[{ url: string }, ...]` | `ContentResponse[]` |
| POST | `/save-content` | 保存内容 | `ContentResponse` | `{ content_id: string, message: string }` |
| POST | `/search` | 搜索内容 | `SearchQuery` | `SearchResult[]` |
| PUT | `/update-learning-status` | 更新学习状态 | `LearningStatusUpdate` | `{ message: string }` |
| PUT | `/update-tags` | 更新标签 | `TagUpdate` | `{ message: string }` |
| PUT | `/update-note` | 更新笔记 | `NoteUpdate` | `{ message: string }` |
| GET | `/content/{content_id}` | 获取内容详情 | - | `ContentResponse` |
| GET | `/learning-stats` | 获取学习统计 | - | `{ total_count, status_counts, ... }` |

#### 4.1.3 数据模型 ([`backend/app/models/schemas.py`](file:///workspace/backend/app/models/schemas.py))

**核心数据模型：**

```python
class LinkInput(BaseModel):
    url: str  # 平台链接

class ContentResponse(BaseModel):
    title: str              # 标题
    content: str            # 内容正文
    author: str             # 作者
    update: str             # 文章更新时间
    create_time: str        # 笔记创建时间
    url: str                # 原文链接
    source: str             # 来源平台
    tags: List[str] = []    # 标签列表
    knowledge_points: List[str] = []  # 知识点列表
    summary: str = ""       # AI 生成的摘要

class SearchQuery(BaseModel):
    text: str                       # 搜索文本
    domains: Optional[List[str]]    # 领域筛选
    sources: Optional[List[str]]    # 来源筛选
    difficulty: Optional[str]       # 难度筛选
    content_type: Optional[str]     # 内容类型筛选
    start_date: Optional[date]      # 开始日期
    end_date: Optional[date]        # 结束日期
    learning_status: Optional[str]  # 学习状态筛选

class SearchResult(BaseModel):
    content_id: str          # 内容ID
    title: str               # 标题
    summary: str             # 摘要
    author: str              # 作者
    source: str              # 来源
    update: str              # 更新时间
    create_time: str         # 创建时间
    tags: List[str]          # 标签
    knowledge_points: List[str]  # 知识点
    learning_status: str     # 学习状态
    relevance_score: float   # 相关度评分
```

#### 4.1.4 平台解析器 ([`backend/app/services/platform_parser.py`](file:///workspace/backend/app/services/platform_parser.py))

**类名：** `PlatformParser`

**功能：** 检测平台并解析各平台内容

**支持的平台：**
| 平台 | URL 模式 |
|------|---------|
| 抖音 | `douyin.com` |
| 小红书 | `xiaohongshu.com` |
| 微信公众号 | `mp.weixin.qq.com` |
| B站 | `bilibili.com` / `b23.tv` |
| 知乎 | `zhihu.com` |
| CSDN | `csdn.net` |

**主要方法：**

```python
# 主方法
async def parse(self, url: str) -> ContentResponse

# 平台检测
def _detect_platform(self, url: str) -> str

# 各平台解析方法
async def _parse_douyin(self, url: str) -> ContentResponse
async def _parse_xiaohongshu(self, url: str) -> ContentResponse
async def _parse_weixin(self, url: str) -> ContentResponse
async def _parse_bilibili(self, url: str) -> ContentResponse
async def _parse_zhihu(self, url: str) -> ContentResponse
async def _parse_csdn(self, url: str) -> ContentResponse

# LLM 处理（失败时有备用方案）
def _generate_summary(self, content: str) -> str
def _generate_tags(self, content: str) -> List[str]
def _extract_knowledge_points(self, content: str) -> List[str]
```

**解析流程：**
1. 检测平台类型
2. 调用 TikHub API 获取原始数据
3. 提取关键信息（标题、作者、时间、内容）
4. 视频内容调用 ASR 转文字
5. 调用 LLM 服务生成摘要、标签、知识点
6. 返回完整的 ContentResponse

#### 4.1.5 LLM 服务 ([`backend/app/services/llm_service.py`](file:///workspace/backend/app/services/llm_service.py))

**类名：** `LLMService`（单例模式 `llm_service`）

**功能：** 封装 DashScope API，提供 AI 能力

**配置：**
- 模型：`qwen-plus`
- ASR 模型：`qwen3-asr-flash`
- 默认超时：60 秒
- 最大重试：3 次

**主要方法：**

```python
# 生成内容摘要
def generate_summary(self, content: str, timeout: int) -> str

# 生成标签
def generate_tags(self, content: str, timeout: int) -> List[str]

# 提取知识点
def extract_knowledge_points(self, content: str, timeout: int) -> List[str]

# 语音转文字
def speech_to_text(self, audio_url: str, language: str, timeout: int) -> str

# 综合处理（串行调用多个任务）
def process_content(
    self,
    content: str,
    include_summary: bool = True,
    include_tags: bool = True,
    include_knowledge_points: bool = True
) -> Dict[str, Any]
```

**异常类：**
- `LLMServiceError` - 基础异常
- `LLMServiceTimeout` - 超时异常
- `LLMServiceValidationError` - 输入验证异常

**提示词模板：**
- **摘要生成**：简洁概括（200字以内）
- **标签生成**：5-10个标签，覆盖技术领域、应用场景、核心概念
- **知识点提取**：提取重要技术概念、原理、方法

#### 4.1.6 内容管理器 ([`backend/app/services/content_manager.py`](file:///workspace/backend/app/services/content_manager.py))

**类名：** `ContentManager`

**功能：** 内容的 CRUD 操作、去重检测、数据库操作

**数据库 Schema：**

```sql
-- 内容表
CREATE TABLE content (
    id TEXT PRIMARY KEY,          -- 内容ID（MD5(url+create_time)）
    title TEXT,                   -- 标题
    content TEXT,                 -- 内容
    author TEXT,                  -- 作者
    update_date TEXT,             -- 文章更新时间
    create_date TEXT,             -- 笔记创建时间
    url TEXT UNIQUE,              -- 原文链接（唯一）
    source TEXT,                  -- 来源平台
    tags TEXT,                    -- JSON 格式的标签
    knowledge_points TEXT,        -- JSON 格式的知识点
    summary TEXT,                 -- 摘要
    hash TEXT UNIQUE              -- 内容哈希（用于去重）
);

-- 学习状态表
CREATE TABLE learning_status (
    content_id TEXT PRIMARY KEY,  -- 内容ID（外键）
    status TEXT DEFAULT '未读',   -- 学习状态
    note TEXT DEFAULT '',         -- 笔记
    FOREIGN KEY (content_id) REFERENCES content(id)
);
```

**主要方法：**

```python
# 保存内容（自动去重）
async def save(self, content: ContentResponse) -> str

# 获取内容
async def get(self, content_id: str) -> ContentResponse

# 获取所有内容
async def get_all(self) -> List[Dict]

# 更新内容
async def update(self, content_id: str, content: ContentResponse) -> bool

# 删除内容
async def delete(self, content_id: str) -> bool

# 内部方法
async def _check_duplicate(self, content_hash: str, url: str) -> Optional[str]
def _generate_hash(self, content: ContentResponse) -> str  # 生成内容哈希
```

**去重策略：**
- 基于内容哈希（`title + content + author` 的 MD5）
- 基于 URL 唯一性
- 两者任一匹配即认为是重复内容

#### 4.1.7 搜索引擎 ([`backend/app/services/search_engine.py`](file:///workspace/backend/app/services/search_engine.py))

**类名：** `SearchEngine`

**功能：** 全文检索、多条件筛选、相关度计算

**主要方法：**

```python
# 主搜索方法
async def search(
    self,
    text: str,
    domains: Optional[List[str]] = None,
    sources: Optional[List[str]] = None,
    difficulty: Optional[str] = None,
    content_type: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    learning_status: Optional[str] = None
) -> List[SearchResult]

# 相关度计算
def _calculate_relevance(self, query: str, title: str, summary: str) -> float

# 获取相似内容
async def get_similar_content(self, content_id: str, limit: int = 5) -> List[SearchResult]

# 获取推荐内容
async def get_recommendations(self, user_id: Optional[str] = None, limit: int = 5) -> List[SearchResult]
```

**相关度评分算法：**
- 标题匹配：每个匹配词 +0.5 分
- 摘要匹配：每个匹配词 +0.3 分
- 归一化到 [0, 1] 范围
- 按相关度降序排序结果

#### 4.1.8 学习管理器 ([`backend/app/services/learning_manager.py`](file:///workspace/backend/app/services/learning_manager.py))

**类名：** `LearningManager`

**功能：** 学习状态管理、笔记管理、统计分析

**学习状态：**
- `未读` - 初始状态
- `阅读中` - 正在阅读
- `重点` - 标记为重要
- `待复习` - 安排复习

**主要方法：**

```python
# 更新学习状态
async def update_status(self, content_id: str, status: str) -> bool

# 更新标签
async def update_tags(self, content_id: str, tags: List[str]) -> bool

# 更新笔记
async def update_note(self, content_id: str, note: str) -> bool

# 获取状态
async def get_status(self, content_id: str) -> str

# 获取笔记
async def get_note(self, content_id: str) -> str

# 获取统计数据
async def get_stats(self) -> Dict[str, Any]

# 按状态获取内容
async def get_content_by_status(self, status: str) -> List[Dict]

# 按标签获取内容
async def get_content_by_tag(self, tag: str) -> List[Dict]
```

**统计数据结构：**
```python
{
    "total_count": 100,              # 总内容数
    "status_counts": {               # 各状态计数
        "未读": 50,
        "已读": 30,
        "重点": 15,
        "待复习": 5
    },
    "source_counts": {               # 各平台计数
        "知乎": 40,
        "微信公众号": 30,
        ...
    },
    "domain_counts": {               # 各领域计数
        "llm": 50,
        "agent": 30,
        ...
    },
    "progress": 30.0                 # 学习进度百分比
}
```

#### 4.1.9 配置管理 ([`backend/app/utils/config.py`](file:///workspace/backend/app/utils/config.py))

**功能：** 管理环境变量和应用配置

**配置项：**
```python
# TikHub API
TIKHUB_API_KEY = os.getenv("TIKHUB_API_KEY", "")
TIKHUB_API_URL = "https://api.tikhub.dev"

# DashScope API
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "")

# Qdrant（预留）
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")
QDRANT_CLUSTER_ENDPOINT = os.getenv("QDRANT_CLUSTER_ENDPOINT", "")

# 数据库
DATABASE_URL = "sqlite:///./knowledge.db"

# 应用
APP_NAME = "AI 知识收藏与检索管家"
DEBUG = True
```

**使用方式：**
```python
from app.utils.config import get_settings

settings = get_settings()
api_key = settings.DASHSCOPE_API_KEY
```

### 4.2 前端核心模块

#### 4.2.1 应用入口 ([`src/index.tsx`](file:///workspace/src/index.tsx))

**功能：** React 应用启动入口

```tsx
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

#### 4.2.2 主应用组件 ([`src/App.tsx`](file:///workspace/src/App.tsx))

**功能：** 路由管理、状态管理、主要业务逻辑

**路由结构：**

| 路径 | 组件 | 功能 |
|------|------|------|
| `/` | Dashboard | 仪表板、统计概览、最近内容 |
| `/collect` | LinkInput + KnowledgeCard | 收集链接、展示内容列表 |
| `/search` | Search + FilterPanel + KnowledgeList | 搜索和筛选 |
| `/learn` | Stats | 学习统计分析 |
| `/settings` | Settings | 设置页面 |

**主要状态：**
```tsx
const [selectedItem, setSelectedItem] = useState<KnowledgeItem | null>(null);
const [isDetailOpen, setIsDetailOpen] = useState(false);
const [isParsing, setIsParsing] = useState(false);
const [parseProgress, setParseProgress] = useState(0);
const [filters, setFilters] = useState<SearchFilters>({});
const [searchQuery, setSearchQuery] = useState('');
const [searchResults, setSearchResults] = useState<KnowledgeItem[]>([]);
const [isSemanticSearch, setIsSemanticSearch] = useState(false);
```

**平台检测函数：**
```tsx
function detectPlatform(url: string): string | null {
  const patterns: Record<string, RegExp> = {
    wechat: /mp\.weixin\.qq\.com/,
    zhihu: /zhihu\.com/,
    csdn: /csdn\.net/,
    bilibili: /bilibili\.com|b23\.tv/,
    douyin: /douyin\.com|iesdouyin\.com/,
    xiaohongshu: /xiaohongshu\.com|xhslink\.com/,
  };
  // ...
}
```

#### 4.2.3 API 工具 ([`src/utils/api.ts`](file:///workspace/src/utils/api.ts))

**功能：** 封装所有后端 API 调用

**API 基础地址：** `http://localhost:8000/api`

**导出函数：**
```typescript
// 解析链接
export async function parseLink(url: string): Promise<ContentResponse>

// 批量解析链接
export async function parseLinks(urls: string[]): Promise<ContentResponse[]>

// 保存内容
export async function saveContent(content: ContentResponse): Promise<{ content_id: string; message: string }>

// 搜索内容
export async function search(query: SearchQuery): Promise<SearchResult[]>

// 更新学习状态
export async function updateLearningStatus(contentId: string, status: string): Promise<{ message: string }>

// 更新标签
export async function updateTags(contentId: string, tags: string[]): Promise<{ message: string }>

// 更新笔记
export async function updateNote(contentId: string, note: string): Promise<{ message: string }>

// 获取内容详情
export async function getContent(contentId: string): Promise<ContentResponse>

// 获取学习统计
export async function getLearningStats(): Promise<Record<string, any>>
```

#### 4.2.4 类型定义 ([`src/types/index.ts`](file:///workspace/src/types/index.ts))

**主要类型：**

```typescript
// 平台类型
type Platform = 'wechat' | 'zhihu' | 'csdn' | 'bilibili' | 'douyin' | 'xiaohongshu';

// 领域类型
type Domain = 'llm' | 'agent' | 'rag' | 'multimodal';

// 内容类型
type ContentType = 'tutorial' | 'review' | 'practice' | 'paper' | 'interview' | 'analysis';

// 难度
type Difficulty = 'beginner' | 'intermediate' | 'advanced' | 'paper';

// 学习状态
type LearningStatus = 'unread' | 'read' | 'important' | 'review';

// 知识项
interface KnowledgeItem {
  id: string;
  user_id: string;
  platform: Platform;
  url: string;
  title: string;
  author: string;
  publish_time: string;
  content: string;
  short_summary: string;
  long_summary: string;
  domains: Domain[];
  content_type: ContentType;
  difficulty: Difficulty;
  key_points: string[];
  tags: string[];
  status: LearningStatus;
  is_deleted: boolean;
  note?: string;
  created_at: string;
  updated_at: string;
}

// 搜索筛选
interface SearchFilters {
  domains?: Domain[];
  platforms?: Platform[];
  difficulty?: Difficulty[];
  contentTypes?: ContentType[];
  status?: LearningStatus[];
  startDate?: string;
  endDate?: string;
}
```

---

## 5. 关键类与函数

### 5.1 后端关键类

#### `PlatformParser` ([`backend/app/services/platform_parser.py`](file:///workspace/backend/app/services/platform_parser.py))

| 方法 | 参数 | 返回 | 说明 |
|------|------|------|------|
| `parse()` | `url: str` | `ContentResponse` | 主解析方法 |
| `_detect_platform()` | `url: str` | `str` | 检测平台类型 |
| `_parse_douyin()` | `url: str` | `ContentResponse` | 解析抖音 |
| `_parse_xiaohongshu()` | `url: str` | `ContentResponse` | 解析小红书 |
| `_parse_weixin()` | `url: str` | `ContentResponse` | 解析微信公众号 |
| `_parse_bilibili()` | `url: str` | `ContentResponse` | 解析B站 |
| `_parse_zhihu()` | `url: str` | `ContentResponse` | 解析知乎 |
| `_parse_csdn()` | `url: str` | `ContentResponse` | 解析CSDN |
| `_generate_summary()` | `content: str` | `str` | 生成摘要 |
| `_generate_tags()` | `content: str` | `List[str]` | 生成标签 |
| `_extract_knowledge_points()` | `content: str` | `List[str]` | 提取知识点 |

#### `LLMService` ([`backend/app/services/llm_service.py`](file:///workspace/backend/app/services/llm_service.py))

| 方法 | 参数 | 返回 | 说明 |
|------|------|------|------|
| `generate_summary()` | `content, timeout` | `str` | 生成内容摘要 |
| `generate_tags()` | `content, timeout` | `List[str]` | 生成标签列表 |
| `extract_knowledge_points()` | `content, timeout` | `List[str]` | 提取知识点 |
| `speech_to_text()` | `audio_url, language, timeout` | `str` | 语音转文字 |
| `process_content()` | `content, ...` | `Dict` | 综合处理内容 |
| `_validate_input()` | `content, max_length` | `None` | 验证输入 |
| `_build_prompt()` | `task_type, content` | `str` | 构建提示词 |
| `_parse_response()` | `response, task_type` | `Any` | 解析响应 |
| `_request_with_retry()` | `prompt, ...` | `Any` | 带重试的请求 |

#### `ContentManager` ([`backend/app/services/content_manager.py`](file:///workspace/backend/app/services/content_manager.py))

| 方法 | 参数 | 返回 | 说明 |
|------|------|------|------|
| `save()` | `content: ContentResponse` | `str` | 保存内容（返回ID） |
| `get()` | `content_id: str` | `ContentResponse` | 获取内容 |
| `get_all()` | - | `List[Dict]` | 获取所有内容 |
| `update()` | `content_id, content` | `bool` | 更新内容 |
| `delete()` | `content_id: str` | `bool` | 删除内容 |
| `_check_duplicate()` | `content_hash, url` | `Optional[str]` | 检测重复 |
| `_generate_hash()` | `content: ContentResponse` | `str` | 生成内容哈希 |

#### `SearchEngine` ([`backend/app/services/search_engine.py`](file:///workspace/backend/app/services/search_engine.py))

| 方法 | 参数 | 返回 | 说明 |
|------|------|------|------|
| `search()` | `text, domains, sources, ...` | `List[SearchResult]` | 搜索内容 |
| `_calculate_relevance()` | `query, title, summary` | `float` | 计算相关度 |
| `get_similar_content()` | `content_id, limit` | `List[SearchResult]` | 获取相似内容 |
| `get_recommendations()` | `user_id, limit` | `List[SearchResult]` | 获取推荐内容 |

#### `LearningManager` ([`backend/app/services/learning_manager.py`](file:///workspace/backend/app/services/learning_manager.py))

| 方法 | 参数 | 返回 | 说明 |
|------|------|------|------|
| `update_status()` | `content_id, status` | `bool` | 更新学习状态 |
| `update_tags()` | `content_id, tags` | `bool` | 更新标签 |
| `update_note()` | `content_id, note` | `bool` | 更新笔记 |
| `get_status()` | `content_id: str` | `str` | 获取学习状态 |
| `get_note()` | `content_id: str` | `str` | 获取笔记 |
| `get_stats()` | - | `Dict[str, Any]` | 获取统计数据 |
| `get_content_by_status()` | `status: str` | `List[Dict]` | 按状态获取内容 |
| `get_content_by_tag()` | `tag: str` | `List[Dict]` | 按标签获取内容 |

### 5.2 前端关键组件

| 组件 | 路径 | 功能 |
|------|------|------|
| `App` | [`src/App.tsx`](file:///workspace/src/App.tsx) | 主应用，路由管理 |
| `Layout` | [`src/components/Layout.tsx`](file:///workspace/src/components/Layout.tsx) | 页面布局框架 |
| `Dashboard` | [`src/components/Dashboard.tsx`](file:///workspace/src/components/Dashboard.tsx) | 仪表板首页 |
| `LinkInput` | [`src/components/LinkInput.tsx`](file:///workspace/src/components/LinkInput.tsx) | 链接输入组件 |
| `KnowledgeCard` | [`src/components/KnowledgeCard.tsx`](file:///workspace/src/components/KnowledgeCard.tsx) | 知识卡片 |
| `KnowledgeList` | [`src/components/KnowledgeList.tsx`](file:///workspace/src/components/KnowledgeList.tsx) | 知识列表 |
| `DetailModal` | [`src/components/DetailModal.tsx`](file:///workspace/src/components/DetailModal.tsx) | 内容详情弹窗 |
| `Search` | [`src/components/Search.tsx`](file:///workspace/src/components/Search.tsx) | 搜索组件 |
| `FilterPanel` | [`src/components/FilterPanel.tsx`](file:///workspace/src/components/FilterPanel.tsx) | 筛选面板 |
| `Stats` | [`src/components/Stats.tsx`](file:///workspace/src/components/Stats.tsx) | 统计组件 |

---

## 6. 依赖关系

### 6.1 后端依赖 ([`pyproject.toml`](file:///workspace/pyproject.toml))

| 依赖 | 版本 | 用途 |
|------|------|------|
| `fastapi` | 0.104.1 | Web 框架 |
| `uvicorn[standard]` | 0.24.0 | ASGI 服务器 |
| `httpx` | 0.25.2 | HTTP 客户端 |
| `beautifulsoup4` | 4.12.2 | HTML 解析 |
| `lxml` | 4.9.3 | XML/HTML 处理 |
| `pydantic` | 2.5.0 | 数据验证 |
| `python-multipart` | 0.0.6 | 表单数据处理 |
| `openai` | 1.3.0 | OpenAI API |
| `trafilatura` | 1.6.2 | 网页内容提取 |
| `readability-lxml` | 0.8.1 | 网页可读性处理 |
| `tikhub` | 1.0.3+ | 多平台内容 API |
| `dashscope` | 1.25.17+ | 阿里云 AI 服务 |
| `aiohttp` | - | 异步 HTTP 客户端（requirements.txt） |
| `requests` | - | HTTP 客户端（requirements.txt） |
| `numpy` | - | 数值计算（requirements.txt） |
| `pydantic-settings` | - | 配置管理（requirements.txt） |
| `python-dotenv` | - | 环境变量加载（requirements.txt） |

### 6.2 前端依赖 ([`package.json`](file:///workspace/package.json))

#### 生产依赖

| 依赖 | 版本 | 用途 |
|------|------|------|
| `react` | 18.2.0 | 前端框架 |
| `react-dom` | 18.2.0 | DOM 渲染 |
| `react-router-dom` | 6.8.0 | 路由管理 |
| `framer-motion` | 11.16.1 | 动画效果 |
| `lucide-react` | 0.294.0 | 图标库 |
| `date-fns` | 2.30.0 | 日期处理 |
| `recharts` | 2.10.0 | 图表库 |
| `@supabase/supabase-js` | 2.98.0 | Supabase 客户端（未使用） |

#### 开发依赖

| 依赖 | 版本 | 用途 |
|------|------|------|
| `typescript` | 5.3.3 | TypeScript 编译器 |
| `webpack` | 5.106.2 | 模块打包器 |
| `webpack-cli` | 5.1.4 | Webpack CLI |
| `webpack-dev-server` | 4.15.2 | 开发服务器 |
| `html-webpack-plugin` | 5.5.3 | HTML 模板插件 |
| `babel-loader` | 9.1.3 | Babel 加载器 |
| `@babel/core` | 7.23.5 | Babel 核心 |
| `@babel/preset-env` | 7.23.5 | ES 转换 |
| `@babel/preset-react` | 7.23.5 | React JSX 转换 |
| `@babel/preset-typescript` | 7.23.5 | TypeScript 转换 |
| `@types/react` | 18.2.0 | React 类型定义 |
| `@types/react-dom` | 18.2.0 | React DOM 类型定义 |
| `css-loader` | 6.8.1 | CSS 加载器 |
| `style-loader` | 3.3.3 | Style 加载器 |
| `postcss` | 8.4.31 | PostCSS |
| `postcss-loader` | 7.3.3 | PostCSS 加载器 |
| `autoprefixer` | 10.4.16 | 自动前缀 |
| `tailwindcss` | 3.3.5 | Tailwind CSS |

### 6.3 第三方服务

| 服务 | 用途 | 配置项 |
|------|------|--------|
| **TikHub** | 多平台内容解析 API | `TIKHUB_API_KEY`, `TIKHUB_API_URL` |
| **DashScope** | AI 服务（LLM、ASR） | `DASHSCOPE_API_KEY` |

---

## 7. 配置与部署

### 7.1 环境变量配置

创建 `.env` 文件（在 `backend/` 目录下）：

```env
# TikHub API
TIKHUB_API_KEY=your_tikhub_api_key_here
TIKHUB_API_URL=https://api.tikhub.dev

# DashScope (阿里云) API
DASHSCOPE_API_KEY=your_dashscope_api_key_here

# Qdrant (可选，用于向量检索)
QDRANT_API_KEY=
QDRANT_CLUSTER_ENDPOINT=
```

### 7.2 后端启动

#### 方式一：直接运行 Python

```bash
cd backend

# 创建虚拟环境（首次）
python -m venv .venv

# 激活虚拟环境
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 启动服务
python -m app.main
```

#### 方式二：使用 Uvicorn

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 方式三：使用启动脚本

**Windows (PowerShell):**
```powershell
cd backend
.\start.ps1
```

**Windows (CMD):**
```cmd
cd backend
start.bat
```

### 7.3 前端启动

```bash
# 安装依赖
npm install

# 开发模式
npm run dev

# 类型检查
npm run typecheck

# 生产构建
npm run build
```

开发服务器默认运行在 `http://localhost:8080`

### 7.4 访问应用

- **API 文档（Swagger UI）**: `http://localhost:8000/docs`
- **API 文档（ReDoc）**: `http://localhost:8000/redoc`
- **健康检查**: `http://localhost:8000/health`
- **前端应用**: `http://localhost:8080`

---

## 8. 数据库说明

### 8.1 数据库位置

默认 SQLite 数据库文件位置：`/workspace/backend/knowledge.db`

### 8.2 表结构详解

#### `content` 表

| 列 | 类型 | 约束 | 说明 |
|----|------|------|------|
| `id` | TEXT | PRIMARY KEY | 内容唯一标识 |
| `title` | TEXT | | 标题 |
| `content` | TEXT | | 正文内容 |
| `author` | TEXT | | 作者 |
| `update_date` | TEXT | | 文章更新时间 |
| `create_date` | TEXT | | 笔记创建时间 |
| `url` | TEXT | UNIQUE | 原文链接 |
| `source` | TEXT | | 来源平台 |
| `tags` | TEXT | | JSON 格式标签数组 |
| `knowledge_points` | TEXT | | JSON 格式知识点数组 |
| `summary` | TEXT | | 摘要 |
| `hash` | TEXT | UNIQUE | 内容哈希 |

#### `learning_status` 表

| 列 | 类型 | 约束 | 说明 |
|----|------|------|------|
| `content_id` | TEXT | PRIMARY KEY, FOREIGN KEY | 内容 ID |
| `status` | TEXT | DEFAULT '未读' | 学习状态 |
| `note` | TEXT | DEFAULT '' | 笔记 |

### 8.3 数据库操作示例

**查询所有内容：**
```sql
SELECT * FROM content ORDER BY create_date DESC;
```

**查询某状态的内容：**
```sql
SELECT c.*, ls.status, ls.note
FROM content c
JOIN learning_status ls ON c.id = ls.content_id
WHERE ls.status = '重点';
```

**统计各平台内容数量：**
```sql
SELECT source, COUNT(*) as count
FROM content
GROUP BY source
ORDER BY count DESC;
```

---

## 9. API 参考

### 9.1 内容解析 API

#### 解析单个链接

**请求：**
```http
POST /api/parse-link
Content-Type: application/json

{
  "url": "https://zhuanlan.zhihu.com/p/123456"
}
```

**响应：**
```json
{
  "title": "文章标题",
  "content": "文章内容...",
  "author": "作者名",
  "update": "2024-01-15",
  "create_time": "2024-01-20",
  "url": "https://zhuanlan.zhihu.com/p/123456",
  "source": "知乎",
  "tags": ["llm", "agent", "教程"],
  "knowledge_points": ["提示词工程", "RAG 检索"],
  "summary": "这是摘要..."
}
```

#### 批量解析链接

**请求：**
```http
POST /api/parse-links
Content-Type: application/json

[
  { "url": "https://..." },
  { "url": "https://..." }
]
```

### 9.2 内容管理 API

#### 保存内容

**请求：**
```http
POST /api/save-content
Content-Type: application/json

{
  "title": "...",
  "content": "...",
  "author": "...",
  "update": "2024-01-15",
  "create_time": "2024-01-20",
  "url": "https://...",
  "source": "知乎",
  "tags": ["llm", "agent"],
  "knowledge_points": ["...", "..."],
  "summary": "..."
}
```

**响应：**
```json
{
  "content_id": "abc123...",
  "message": "保存成功"
}
```

#### 获取内容详情

**请求：**
```http
GET /api/content/{content_id}
```

### 9.3 搜索 API

**请求：**
```http
POST /api/search
Content-Type: application/json

{
  "text": "RAG",
  "domains": ["llm", "rag"],
  "sources": ["知乎", "微信公众号"],
  "difficulty": "intermediate",
  "content_type": "tutorial",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "learning_status": "未读"
}
```

**响应：**
```json
[
  {
    "content_id": "...",
    "title": "...",
    "summary": "...",
    "author": "...",
    "source": "知乎",
    "update": "2024-01-15",
    "create_time": "2024-01-20",
    "tags": ["llm", "rag"],
    "knowledge_points": ["...", "..."],
    "learning_status": "未读",
    "relevance_score": 0.85
  }
]
```

### 9.4 学习管理 API

#### 更新学习状态

**请求：**
```http
PUT /api/update-learning-status
Content-Type: application/json

{
  "content_id": "abc123",
  "status": "重点"
}
```

#### 更新标签

**请求：**
```http
PUT /api/update-tags
Content-Type: application/json

{
  "content_id": "abc123",
  "tags": ["llm", "agent", "new-tag"]
}
```

#### 更新笔记

**请求：**
```http
PUT /api/update-note
Content-Type: application/json

{
  "content_id": "abc123",
  "note": "这是我的学习笔记..."
}
```

#### 获取学习统计

**请求：**
```http
GET /api/learning-stats
```

**响应：**
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
    "微信公众号": 30
  },
  "domain_counts": {
    "llm": 50,
    "agent": 30
  },
  "progress": 30.0
}
```

---

## 10. 开发指南

### 10.1 项目设置步骤

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd collectly
   ```

2. **设置后端**
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   # 编辑 .env 填入 API keys
   ```

3. **设置前端**
   ```bash
   cd ..  # 返回项目根目录
   npm install
   ```

4. **启动开发服务器**
   - 终端 1（后端）：`cd backend && python -m app.main`
   - 终端 2（前端）：`npm run dev`

### 10.2 代码规范

**后端（Python）：**
- 遵循 PEP 8 规范
- 使用类型提示（Type Hints）
- 使用 Pydantic 进行数据验证
- 使用异步（async/await）进行 I/O 操作

**前端（TypeScript）：**
- 使用 TypeScript 严格模式
- 函数式组件 + Hooks
- 使用 Tailwind CSS 进行样式
- 组件命名采用 PascalCase

### 10.3 测试

**后端测试：**
```bash
cd backend
python -m pytest tests/ -v
```

**测试文件：**
- [`backend/tests/test_parser.py`](file:///workspace/backend/tests/test_parser.py) - 解析器测试
- [`backend/tests/test_content_manager.py`](file:///workspace/backend/tests/test_content_manager.py) - 内容管理器测试
- [`backend/tests/test_learning_manager.py`](file:///workspace/backend/tests/test_learning_manager.py) - 学习管理器测试
- [`backend/tests/test_llm_service.py`](file:///workspace/backend/tests/test_llm_service.py) - LLM 服务测试

### 10.4 常见问题排查

**Q: 后端启动失败，提示缺少 API Key？**
A: 检查 `backend/.env` 文件是否存在且配置了 `TIKHUB_API_KEY` 和 `DASHSCOPE_API_KEY`

**Q: 前端无法连接后端？**
A: 确认后端运行在 `http://localhost:8000`，检查 [`src/utils/api.ts`](file:///workspace/src/utils/api.ts) 中的 `API_BASE_URL` 是否正确

**Q: 数据库文件在哪里？**
A: 默认在 `backend/knowledge.db`，这是 SQLite 文件，可以使用任何 SQLite 客户端查看

**Q: 如何重置数据库？**
A: 删除 `backend/knowledge.db` 文件，重启后端会自动创建新数据库

---

## 11. 扩展开发

### 11.1 添加新平台支持

要添加新的内容平台支持，需要：

1. 在 [`PlatformParser._detect_platform()`](file:///workspace/backend/app/services/platform_parser.py) 中添加 URL 检测逻辑
2. 实现 `_parse_<platform>()` 方法
3. 在 [`parse()`](file:///workspace/backend/app/services/platform_parser.py) 主方法中添加条件分支
4. 在前端 [`detectPlatform()`](file:///workspace/src/App.tsx) 中添加对应检测

### 11.2 添加新的筛选条件

1. 在 [`SearchQuery`](file:///workspace/backend/app/models/schemas.py) 中添加新字段
2. 在 [`SearchEngine.search()`](file:///workspace/backend/app/services/search_engine.py) 中添加筛选逻辑
3. 在前端 [`SearchFilters`](file:///workspace/src/types/index.ts) 类型中添加
4. 在 [`FilterPanel`](file:///workspace/src/components/FilterPanel.tsx) 组件中添加 UI

### 11.3 集成向量数据库

项目预留了 Qdrant 配置，可用于：
- 语义搜索
- 内容相似度计算
- 推荐算法

需要修改 [`SearchEngine`](file:///workspace/backend/app/services/search_engine.py) 来集成向量检索功能。

---

## 12. 附录

### 12.1 相关文档

- [`README.md`](file:///workspace/README.md) - 英文项目说明
- [`READMEzh.md`](file:///workspace/READMEzh.md) - 中文项目说明
- [`docs/IMPLEMENTATION.md`](file:///workspace/docs/IMPLEMENTATION.md) - 实现说明
- [`backend/app/services/README_LLM.md`](file:///workspace/backend/app/services/README_LLM.md) - LLM 服务说明
- [`assets/AI_驱动的大模型_Agent_RAG_多模态个人知识收藏与检索管家——完整可落地需求文档.md`](file:///workspace/assets/AI_驱动的大模型_Agent_RAG_多模态个人知识收藏与检索管家——完整可落地需求文档.md) - 原始需求文档

### 12.2 链接与资源

- **FastAPI 文档**: https://fastapi.tiangolo.com
- **DashScope (阿里云)**: https://dashscope.aliyun.com
- **TikHub**: https://api.tikhub.io
- **React**: https://react.dev
- **Tailwind CSS**: https://tailwindcss.com

### 12.3 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0.0 | 2024-01 | 初始版本 |

---

## 联系方式

如有问题或建议，请参考项目仓库的 Issue 页面。

---

**文档最后更新：** 2024-04-23