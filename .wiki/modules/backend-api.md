---
type: module
title: 后端 API 服务模块
module: backend-api
source_path: backend/app/
updated: 2026-04-25
tags: [backend, fastapi, python]
---

# 后端 API 服务模块

## 概述

后端 API 服务基于 FastAPI 框架构建，提供跨平台内容解析、存储、检索与学习管理功能。它是整个系统的核心，负责处理所有业务逻辑。

## 目录结构

```
backend/app/
├── api/
│   └── routes.py          # RESTful 接口定义
├── models/
│   └── schemas.py         # Pydantic 数据模型
├── services/
│   ├── platform_parser.py # 多平台内容解析器
│   ├── content_manager.py # 内容存储与去重管理
│   ├── search_engine.py   # 智能搜索引擎
│   ├── learning_manager.py# 学习状态管理
│   ├── llm_service.py     # DashScope AI 集成
│   └── vector_service.py  # ChromaDB 向量服务
├── utils/
│   ├── config.py          # 应用配置
│   ├── logger.py          # 日志系统
│   └── exceptions.py      # 异常处理
├── __init__.py
└── main.py                # 应用入口
```

## 核心服务

### [[modules/platform-parser|平台解析器 (PlatformParser)]]

负责从各平台 URL 中提取结构化内容，支持抖音、小红书、B站、知乎、微信公众号等平台。

### [[modules/content-manager|内容管理器 (ContentManager)]]

管理内容的存储、去重和向量化，使用 SQLite 作为主存储，ChromaDB 作为向量存储。

### [[modules/search-engine|搜索引擎 (SearchEngine)]]

提供混合搜索能力，结合关键词匹配和向量语义检索。

### [[modules/learning-manager|学习管理器 (LearningManager)]]

管理内容的学习状态流转（未读 → 已读 → 重点 → 待复习）和笔记功能。

### [[modules/llm-service|LLM 服务 (LLMService)]]

集成 DashScope 通义千问 API，提供内容摘要、标签生成、知识点提取等 AI 能力。

### [[modules/vector-service|向量服务 (VectorService)]]]

基于 ChromaDB 的向量存储与语义检索服务。

## 工具模块

### [[modules/config|配置模块 (Config)]]

使用 Pydantic Settings 管理应用配置，支持从 `.env` 文件加载环境变量。

### [[modules/logger|日志模块 (Logger)]]

提供文件和控制台双输出日志系统，按日期自动分割日志文件。

### [[modules/exceptions|异常处理模块 (Exceptions)]]

定义应用级异常类和全局异常处理器。

## 启动方式

```bash
# 开发模式
cd backend
uvicorn app.main:app --reload --port 8000

# 生产模式
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 依赖

- FastAPI — Web 框架
- SQLite — 关系数据库
- ChromaDB — 向量数据库
- DashScope SDK — AI 服务
- TikHub SDK — 平台数据 API
- httpx — HTTP 客户端
- Pydantic — 数据验证

## 相关文档

- [[apis/rest-api|RESTful API 文档]]
- [[overview|项目概览]]
