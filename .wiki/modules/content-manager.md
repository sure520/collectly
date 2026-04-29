---
type: module
title: 内容管理器模块
module: content-manager
source_path: backend/app/services/content_manager.py
updated: 2026-04-25
tags: [backend, storage, dedup]
---

# 内容管理器模块

## 概述

`ContentManager` 负责内容的持久化存储、去重和向量化。它使用 SQLite 作为主存储数据库，ChromaDB 作为向量存储，实现内容的可靠存储和高效检索。

## 核心功能

### 数据库初始化

自动创建两张核心表：
- `content` — 存储内容元数据（标题、内容、作者、标签等）
- `learning_status` — 存储学习状态和笔记

### 内容保存

```python
async def save(content: ContentResponse) -> str
```

保存流程：
1. 生成内容哈希（基于标题 + 内容）
2. 检查重复（哈希匹配或 URL 匹配）
3. 如重复 → 返回已有 content_id
4. 如不重复 → 写入 SQLite + 创建学习状态记录 + 生成向量嵌入

### 去重策略

- **哈希去重** — 基于 `hashlib.md5(title + content)` 生成唯一哈希
- **URL 去重** — URL 字段设为 UNIQUE 约束
- 双重保障，避免重复内容入库

### 向量化

```python
def _build_embedding_text(content: ContentResponse) -> str
```

构建用于向量化的完整文本，包含：标题、摘要、内容（前 3000 字）、知识点、标签。

## 数据模型

详见 [[models/schemas|数据模型文档]]。

## 相关文档

- [[modules/vector-service|向量服务模块]]
- [[modules/backend-api|后端 API 服务模块]]
- [[apis/rest-api|RESTful API 文档]]
