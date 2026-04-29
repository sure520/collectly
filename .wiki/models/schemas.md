---
type: class
title: 数据模型文档
module: backend-api
source_path: backend/app/models/schemas.py
updated: 2026-04-25
tags: [models, pydantic, schemas]
---

# 数据模型文档

## 概述

使用 Pydantic 定义的数据模型，用于 API 请求和响应的数据验证与序列化。

## 模型列表

### LinkInput

链接输入模型。

| 字段 | 类型 | 说明 |
|------|------|------|
| `url` | str | 平台链接 |

### ContentResponse

内容响应模型，是系统的核心数据模型。

| 字段 | 类型 | 说明 |
|------|------|------|
| `title` | str | 标题 |
| `content` | str | 正文内容 |
| `author` | str | 作者 |
| `update` | str | 文章更新时间 |
| `create_time` | str | 笔记创建时间 |
| `url` | str | 原文链接 |
| `source` | str | 来源平台 |
| `tags` | List[str] | 标签列表 |
| `knowledge_points` | List[str] | 知识点列表 |
| `summary` | str | AI 生成的摘要 |

### SearchQuery

搜索查询模型。

| 字段 | 类型 | 说明 |
|------|------|------|
| `text` | str | 搜索文本 |
| `domains` | Optional[List[str]] | 领域筛选 |
| `sources` | Optional[List[str]] | 来源筛选 |
| `difficulty` | Optional[str] | 难度筛选 |
| `content_type` | Optional[str] | 内容类型筛选 |
| `start_date` | Optional[date] | 开始日期 |
| `end_date` | Optional[date] | 结束日期 |
| `learning_status` | Optional[str] | 学习状态筛选 |
| `use_semantic` | Optional[bool] | 是否使用语义检索 |

### SearchResult

搜索结果模型。

| 字段 | 类型 | 说明 |
|------|------|------|
| `content_id` | str | 内容 ID |
| `title` | str | 标题 |
| `summary` | str | 摘要 |
| `author` | str | 作者 |
| `source` | str | 来源平台 |
| `update` | str | 更新时间 |
| `create_time` | str | 创建时间 |
| `tags` | List[str] | 标签 |
| `knowledge_points` | List[str] | 知识点 |
| `learning_status` | str | 学习状态 |
| `relevance_score` | float | 相关度分数 |

### LearningStatusUpdate

学习状态更新模型。

| 字段 | 类型 | 说明 |
|------|------|------|
| `content_id` | str | 内容 ID |
| `status` | str | 学习状态 |

### TagUpdate

标签更新模型。

| 字段 | 类型 | 说明 |
|------|------|------|
| `content_id` | str | 内容 ID |
| `tags` | List[str] | 标签列表 |

### NoteUpdate

笔记更新模型。

| 字段 | 类型 | 说明 |
|------|------|------|
| `content_id` | str | 内容 ID |
| `note` | str | 笔记内容 |

## 相关文档

- [[apis/rest-api|RESTful API 文档]]
- [[modules/backend-api|后端 API 服务模块]]
