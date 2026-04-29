---
type: schema
title: Collectly Wiki Schema
project_type: web_app
language: python, typescript
framework: fastapi, react
last_sync_commit: 80762ac57f0ec92249651b50227f55438adbe507
updated: 2026-04-25
---

# Collectly Wiki 配置

## 项目概述

Collectly（AI 知识收藏与检索管家）是一个跨平台内容收藏与管理工具，支持从抖音、小红书、微信公众号、B站、知乎等主流中文平台抓取内容，通过 AI（DashScope LLM）进行智能摘要、标签生成和知识点提取，并提供全文搜索、语义检索和学习状态管理功能。

## 模块边界与命名约定

| 模块 | 路径 | 说明 |
|------|------|------|
| 后端 API 服务 | `backend/app/` | FastAPI 应用，提供 RESTful 接口 |
| 平台解析器 | `backend/app/services/platform_parser.py` | 多平台内容解析 |
| 内容管理器 | `backend/app/services/content_manager.py` | 存储与去重 |
| 搜索引擎 | `backend/app/services/search_engine.py` | 智能搜索 |
| 学习管理器 | `backend/app/services/learning_manager.py` | 状态与进度追踪 |
| LLM 服务 | `backend/app/services/llm_service.py` | DashScope AI 集成 |
| 向量服务 | `backend/app/services/vector_service.py` | ChromaDB 向量存储 |
| 数据模型 | `backend/app/models/schemas.py` | Pydantic 数据模型 |
| API 路由 | `backend/app/api/routes.py` | RESTful 接口定义 |
| 工具模块 | `backend/app/utils/` | 配置、日志、异常处理 |
| Python 解析器 | `python-parser/` | 独立的内容解析服务 |
| 前端应用 | `src/` | React + TypeScript 前端 |
| 前端组件 | `src/components/` | React 组件 |
| 前端工具 | `src/utils/` | API 调用、格式化等工具 |
| 云函数 | `functions/` | Supabase Edge Functions |

## 文档风格

- 使用中文编写
- 每个页面包含 YAML frontmatter
- 使用 `[[Wikilinks]]` 进行交叉引用
- 代码示例使用对应语言的语法高亮

## 关键目录

| 目录 | 角色 |
|------|------|
| `backend/app/` | FastAPI 后端服务 |
| `backend/app/services/` | 业务逻辑层 |
| `backend/app/api/` | API 路由层 |
| `backend/app/models/` | 数据模型层 |
| `backend/app/utils/` | 工具函数层 |
| `backend/tests/` | 后端测试 |
| `python-parser/` | 独立解析服务 |
| `src/` | React 前端 |
| `src/components/` | 前端 UI 组件 |
| `src/hooks/` | React Hooks |
| `src/utils/` | 前端工具函数 |
| `tests/` | 平台解析测试 |
| `docs/` | 项目文档 |
| `functions/` | Supabase Edge Functions |

## 领域术语

| 术语 | 说明 |
|------|------|
| 内容生命周期 | 未读 → 阅读中 → 重点 → 待复习 → 归档 |
| 平台解析 | 从各平台 URL 提取结构化内容 |
| 语义检索 | 基于向量相似度的内容搜索 |
| 混合搜索 | 关键词 + 向量语义的联合搜索 |
| 去重 | 基于内容哈希的重复检测 |
| DashScope | 阿里云通义千问 API 服务 |
| TikHub | 第三方平台数据 API |
| ChromaDB | 本地向量数据库 |
