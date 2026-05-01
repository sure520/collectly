---
type: config
title: 部署配置
updated: 2026-04-25
tags: [config, deployment, docker]
---

# 部署配置

## 概述

Collectly 支持多种部署方式，包括 Docker 部署、一键脚本部署和手动部署。

## Docker 部署

### docker-compose.yml

```yaml
version: '3.8'
services:
  backend:
    build: .
    ports:
      - "${BACKEND_PORT:-8000}:8000"
    env_file: .env
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
      - ./chroma_db:/app/chroma_db
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "3266:80"
    depends_on:
      - backend
```

### Dockerfile

后端 Dockerfile 使用 Python 3.11 基础镜像，安装依赖后启动 uvicorn 服务。

前端 Dockerfile.frontend 使用 Nginx 提供静态资源服务。

## 一键部署脚本

### Windows

```powershell
# 方案 A：本地部署 + 内网穿透
.\deploy.ps1 -Mode A

# 方案 B：云服务器公网部署
.\deploy.ps1 -Mode B
```

### Linux/macOS

```bash
# 方案 A
./deploy.sh --mode A

# 方案 B
./deploy.sh --mode B
```

部署脚本自动完成：
- 环境检查（uv、Node.js）
- 虚拟环境创建 & 依赖同步（通过 uv）
- 依赖安装（前后端）
- 环境变量配置
- 后端服务启动
- 前端静态资源构建
- 内网穿透配置（方案 A）/ Nginx 配置指导（方案 B）

## 手动部署

前置要求：安装 [uv](https://docs.astral.sh/uv/)（Python 包管理器）

```bash
# Windows 安装 uv
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux/macOS 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
# 后端
uv sync                                        # 同步虚拟环境和依赖

# 使用启动脚本
./start.sh          # Linux/macOS
# 或
.\start.ps1         # Windows PowerShell
# 或
.\start.bat         # Windows CMD
# 或手动启动
uv run uvicorn backend.app.main:app --host 0.0.0.0 --port 8000

# 前端
npm install
npm run build
```

## 访问地址

| 服务 | 地址 |
|------|------|
| 前端 | `http://localhost:3266` |
| 后端 API | `http://localhost:8000` |
| API 文档 | `http://localhost:8000/docs` |

## 相关文档

- [[configs/environment|环境变量配置]]
- [[overview|项目概览]]
