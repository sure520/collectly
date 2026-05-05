# Collectly - Your AI Knowledge Butler

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
  <a href="READMEzh.md">中文</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#core-capabilities">Core Capabilities</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#api-reference">API Reference</a>
</p>

> **"Collect"** is just the beginning, **"Manage"** is the essence.

Collectly is not just a content collector—it's your **intelligent knowledge butler** that transforms scattered information into systematic wisdom. With AI-powered management, your knowledge assets are organized, activated, and always at your fingertips.

---

## What Makes Collectly Different?

### The "Management" Philosophy

Unlike traditional bookmarking tools that only **store**, Collectly **manages** your knowledge through:

- **Lifecycle Management** — Content flows through stages: Unread → Reading → Key Points → Review Scheduled
- **Intelligent Categorization** — AI automatically tags, summarizes, and extracts knowledge points
- **Active Recall System** — Smart reminders for content that needs review
- **Learning Analytics** — Track your knowledge acquisition journey with detailed insights

## Core Capabilities

### 1. Universal Content Capture
Seamlessly ingest content from major Chinese platforms:

| Platform | Capability |
|----------|-----------|
| **Douyin (TikTok)** | Video-to-text extraction with speech recognition |
| **Xiaohongshu** | Lifestyle and product insights |
| **WeChat Articles** | Professional blogs and industry analysis |
| **Bilibili** | Educational videos with subtitle extraction |
| **Zhihu** | Expert Q&A and in-depth articles |
| **CSDN** | Technical tutorials and code solutions |

### 2. AI-Powered Content Refinement
Every piece of content is automatically processed:

- **Smart Summarization** — Condensed 200-word summaries capturing essence
- **Auto-Tagging** — 5-10 relevant tags across multiple dimensions (tech domain, application, concept)
- **Knowledge Point Extraction** — Key concepts and takeaways identified
- **Content Deduplication** — Intelligent hash-based duplicate detection

### 3. Intelligent Knowledge Management

#### Learning Status Pipeline
```
[Unread] → [Reading] → [Key Points] → [Review Scheduled]
   ↑                                            ↓
   └──────────── [Archive] ←────────────────────┘
```

#### Multi-Dimensional Organization
- **By Domain**: AI, LLM, Agent, RAG, Multi-modal
- **By Source**: Platform-based categorization
- **By Status**: Learning progress tracking
- **By Tags**: Custom organizational structure
- **By Date**: Temporal content management

### 4. Smart Retrieval System
Find exactly what you need:

- **Full-Text Search** — Across titles, content, and summaries
- **Multi-Filter Search** — Combine domain + source + status + date range
- **Relevance Scoring** — AI-ranked search results
- **Semantic Understanding** — Context-aware content discovery via vector embeddings

### 5. Personal Knowledge Base
- **Custom Notes** — Add insights to any content
- **Tag Management** — Create your own taxonomy
- **Learning Statistics** — Visual progress tracking
- **Content Collections** — Group related materials

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CONTENT LIFECYCLE                         │
├─────────────────────────────────────────────────────────────┤
│  CAPTURE → PARSE → REFINE → STORE → MANAGE → RETRIEVE      │
│     ↓        ↓        ↓        ↓        ↓          ↓       │
│  [URL]   [Platform]  [LLM]   [SQLite] [Status]   [Search]  │
│          [API]       [AI]    [Dedup]  [Tags]     [Filter]  │
│                      [Tags]   [VecDB]  [Notes]    [Vector] │
└─────────────────────────────────────────────────────────────┘
```

### Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend Framework** | FastAPI (Python) |
| **AI / LLM** | DashScope (Qwen-plus, Qwen3-ASR, Qwen3-VL) |
| **Vector Database** | ChromaDB (local persistence) |
| **Relational Database** | SQLite |
| **Content Parsing** | TikHub API + BeautifulSoup + Trafilatura |
| **Frontend** | React 18 + TypeScript + Tailwind CSS |
| **UI Components** | Framer Motion, Lucide React, Recharts |
| **Build Tool** | Webpack 5 |
| **Containerization** | Docker / Docker Compose |
| **Deployment** | Local + Tunnel / Cloud Server |

## Project Structure

```
collectly/
├── backend/                    # Core API Service
│   ├── app/
│   │   ├── api/routes.py       # RESTful endpoints
│   │   ├── models/schemas.py   # Data models
│   │   ├── services/
│   │   │   ├── platform_parser.py     # Multi-platform parser
│   │   │   ├── content_manager.py     # Storage & deduplication
│   │   │   ├── search_engine.py       # Intelligent search
│   │   │   ├── learning_manager.py    # Status & progress tracking
│   │   │   ├── llm_service.py         # DashScope AI integration
│   │   │   └── vector_service.py      # Vector embeddings & search
│   │   └── utils/
│   └── tests/
│
├── python-parser/              # Standalone parsing service
│   ├── main.py
│   ├── content_extractor.py
│   ├── summarizer.py
│   └── requirements.txt
│
├── src/                        # React frontend
│   ├── components/             # UI components
│   ├── hooks/                  # React hooks
│   ├── utils/                  # Frontend utilities
│   └── types/                  # TypeScript types
│
├── functions/                  # Supabase Edge Functions
│
├── tests/                      # Platform-specific tests
│
├── .wiki/                      # Project documentation wiki
│
├── start.bat                   # Windows CMD startup script
├── start.ps1                   # PowerShell startup script
├── start.sh                    # Linux/macOS startup script
├── Dockerfile                  # Docker build file
├── docker-compose.yml          # Docker Compose configuration
├── deploy.ps1                  # One-click deployment (Windows PowerShell)
├── deploy.sh                   # One-click deployment (Linux/macOS)
├── deploy-local.ps1            # Local interactive deployment (Windows)
├── deploy-local.sh             # Local interactive deployment (Linux/macOS)
├── .env.example                # Environment variables template
├── requirements.txt            # Python dependencies
└── pyproject.toml              # Python project configuration
```

## Quick Start

### Prerequisites

| Dependency | Version | Purpose |
|-----------|---------|---------|
| [uv](https://docs.astral.sh/uv/) | Latest | Python package & virtual environment manager |
| Node.js | 16+ | Frontend build |
| TikHub API Key | — | Platform content access |
| DashScope API Key | — | AI capabilities (LLM, ASR, Vision, Embedding) |

**Install uv:**
```powershell
# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Option 1: One-Click Deployment Script (Recommended)

#### Windows Users
```powershell
# Clone repository
git clone <repository-url>
cd collectly

# Mode A: Local deployment + Tunnel (for personal computer)
.\deploy.ps1 -Mode A

# Mode B: Cloud server public deployment (24/7 online)
.\deploy.ps1 -Mode B
```

#### Linux/macOS Users
```bash
# Clone repository
git clone <repository-url>
cd collectly

# Mode A: Local deployment + Tunnel
./deploy.sh --mode A

# Mode B: Cloud server public deployment
./deploy.sh --mode B
```

**The deployment script automatically:**
- ✅ Environment check (uv, Node.js)
- ✅ Virtual environment creation & dependency sync (via uv)
- ✅ Dependency installation (frontend & backend)
- ✅ Environment variable configuration
- ✅ Backend service startup
- ✅ Frontend static resource build
- ✅ Tunnel configuration (Mode A) / Nginx setup guide (Mode B)

### Option 2: Docker Deployment

```bash
# Clone repository
git clone <repository-url>
cd collectly

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys

# Start with one command
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Access URLs:
- Frontend: http://localhost:3266
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 3: Manual Installation (Development Mode)

```bash
# Clone repository
git clone <repository-url>
cd collectly

# Install uv (if not installed)
# Windows: powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
# Linux/macOS: curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync virtual environment and dependencies
uv sync

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Start backend (Terminal 1)
.\start.bat   # Windows CMD
# or
.\start.ps1   # Windows PowerShell
# or
./start.sh    # Linux/macOS
# or
uv run uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

# Build and start frontend (Terminal 2)
npm install
npm run dev
```

Access URLs:
- Frontend: http://localhost:3266
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## API Reference

### Authentication
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/status` | GET | Check if authentication is required |
| `/api/auth/login` | POST | Login with access password |
| `/api/auth/verify` | GET | Verify current token validity |

### Content Management
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/parse-link` | POST | Parse single URL |
| `/api/parse-links` | POST | Batch parse URLs |
| `/api/save-content` | POST | Save to knowledge base |
| `/api/content/{id}` | GET | Retrieve content |
| `/api/clean-urls` | POST | Clean and extract URLs from raw text |

### Knowledge Management
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/update-learning-status` | PUT | Update content status |
| `/api/update-tags` | PUT | Modify tags |
| `/api/update-note` | PUT | Add personal notes |
| `/api/learning-stats` | GET | View progress analytics |

### Search
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/search` | POST | Multi-filter search |

## Configuration

```env
# TikHub API
TIKHUB_API_KEY=your_key
TIKHUB_API_URL=https://api.tikhub.io

# DashScope (Aliyun) LLM
DASHSCOPE_API_KEY=your_key

# Model Configuration
LLM_MODEL_NAME=qwen-plus
ASR_MODEL_NAME=qwen3-asr-flash
VISION_MODEL_NAME=qwen3-vl-flash
EMBEDDING_MODEL=text-embedding-v4

# App Settings
APP_NAME="Collectly - AI Knowledge Butler"
DEBUG=false
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# Access Control
ACCESS_PASSWORD=your_password
TOKEN_EXPIRE_HOURS=24
```

## The "Manage" Difference

| Feature | Traditional Bookmark | Collectly |
|---------|---------------------|-----------|
| Storage | Save URL | Full content extraction |
| Organization | Manual folders | AI auto-categorization |
| Discovery | Manual browsing | Smart search + filters |
| Retention | Static | Learning status tracking |
| Insights | None | Learning analytics |
| Review | Manual | Scheduled recall system |
| Search | Title only | Full-text + semantic vector search |

## Development

```bash
# Run tests
cd backend
pytest tests/

# Test specific platform
python tests/test_douyin.py
python tests/test_zhihu.py
```

## License

MIT License

## Acknowledgments

- [TikHub](https://api.tikhub.io) — Multi-platform content access
- [DashScope](https://dashscope.aliyun.com) — LLM, ASR, Vision & Embedding capabilities
- [FastAPI](https://fastapi.tiangolo.com) — Web framework
- [ChromaDB](https://www.trychroma.com) — Vector database
- [React](https://react.dev) — Frontend library

---

> **Collectly** — Transform information overload into organized wisdom.
