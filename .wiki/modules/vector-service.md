---
type: module
title: 向量服务模块
module: vector-service
source_path: backend/app/services/vector_service.py
updated: 2026-04-25
tags: [backend, vector, chromadb, semantic]
---

# 向量服务模块

## 概述

`VectorService` 基于 ChromaDB 提供向量存储和语义检索功能。它使用本地持久化存储，支持增量更新，是语义搜索的基础设施。

## 核心功能

### 向量添加

```python
def add_embedding(content_id: str, text: str, metadata: dict) -> bool
```

- 自动检测已存在向量 → 更新
- 新向量 → 添加
- 空内容 → 跳过

### 语义搜索

```python
def search(query: str, n_results: int, where: dict) -> List[dict]
```

- 使用余弦相似度（cosine）进行向量匹配
- 支持元数据过滤（`where` 参数）
- 返回结果包含 `content_id` 和 `distance`（距离值）

### 集合管理

```python
def reset_collection()  # 重置集合（全量重建用）
def get_collection_stats() -> dict  # 获取统计信息
```

## 配置

| 参数 | 值 | 说明 |
|------|-----|------|
| 集合名称 | `knowledge_embeddings` | ChromaDB 集合名 |
| 嵌入模型 | `all-MiniLM-L6-v2` | 文本向量化模型 |
| 距离函数 | `cosine` | 余弦相似度 |
| 持久化目录 | `./chroma_data` | 向量数据存储路径 |

## 相关文档

- [[modules/content-manager|内容管理器模块]]
- [[modules/search-engine|搜索引擎模块]]
- [[modules/backend-api|后端 API 服务模块]]
