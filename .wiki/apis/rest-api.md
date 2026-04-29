---
type: api
title: RESTful API 文档
module: backend-api
source_path: backend/app/api/routes.py
updated: 2026-04-25
tags: [api, rest, fastapi]
---

# RESTful API 文档

## 概述

Collectly 后端提供 RESTful API 接口，所有端点以 `/api` 为前缀。基础地址：`http://localhost:8000/api`。

## 端点列表

### 内容解析

#### POST `/api/parse-link`

解析单个平台链接。

**请求体：**
```json
{
  "url": "https://www.douyin.com/video/xxxxx"
}
```

**响应：** [[models/schemas|ContentResponse]]

#### POST `/api/parse-links`

批量解析平台链接。

**请求体：**
```json
[
  { "url": "https://..." },
  { "url": "https://..." }
]
```

**响应：** `ContentResponse[]`

### 内容存储

#### POST `/api/save-content`

保存解析后的内容。

**请求体：** [[models/schemas|ContentResponse]]

**响应：**
```json
{
  "content_id": "md5_hash_string",
  "message": "保存成功"
}
```

### 内容检索

#### POST `/api/search`

智能检索内容。

**请求体：**
```json
{
  "text": "搜索关键词",
  "domains": ["llm", "agent"],
  "sources": ["zhihu", "wechat"],
  "learning_status": "未读",
  "use_semantic": true
}
```

**响应：** `SearchResult[]`

### 学习管理

#### PUT `/api/update-learning-status`

更新学习状态。

**请求体：**
```json
{
  "content_id": "xxx",
  "status": "已读"
}
```

#### PUT `/api/update-tags`

更新标签。

**请求体：**
```json
{
  "content_id": "xxx",
  "tags": ["AI", "大模型"]
}
```

#### PUT `/api/update-note`

更新笔记。

**请求体：**
```json
{
  "content_id": "xxx",
  "note": "我的学习笔记..."
}
```

### 内容查询

#### GET `/api/content/{content_id}`

获取内容详情。

#### GET `/api/learning-stats`

获取学习统计数据。

#### GET `/api/vector-stats`

获取向量库统计信息。

### 向量管理

#### POST `/api/re-embed/{content_id}`

重新生成指定内容的向量。

#### POST `/api/rebuild-vectors`

全量重建向量索引。

### 健康检查

#### GET `/health`

```json
{
  "status": "healthy"
}
```

## 错误响应

所有错误统一返回：
```json
{
  "error": "错误描述信息"
}
```

## 相关文档

- [[modules/backend-api|后端 API 服务模块]]
- [[models/schemas|数据模型文档]]
