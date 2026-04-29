---
type: module
title: 搜索引擎模块
module: search-engine
source_path: backend/app/services/search_engine.py
updated: 2026-04-25
tags: [backend, search, semantic]
---

# 搜索引擎模块

## 概述

`SearchEngine` 提供混合检索能力，结合传统关键词搜索和向量语义搜索，实现精准的内容发现。

## 搜索模式

### 混合搜索（默认）

```
关键词搜索 + 向量语义搜索 → 结果融合 → 排序输出
```

1. 先执行向量语义搜索，获取 Top 50 结果
2. 再执行关键词 SQL 搜索
3. 融合两种结果，去重后按相关度排序
4. 应用筛选条件（领域、来源、日期、学习状态等）

### 纯关键词搜索

当 `use_semantic=False` 或向量搜索无结果时，回退到纯关键词搜索。

## 筛选条件

| 参数 | 类型 | 说明 |
|------|------|------|
| `domains` | List[str] | 领域筛选 |
| `sources` | List[str] | 来源平台筛选 |
| `difficulty` | str | 难度筛选 |
| `content_type` | str | 内容类型筛选 |
| `start_date` | date | 开始日期 |
| `end_date` | date | 结束日期 |
| `learning_status` | str | 学习状态筛选 |

## 相关度评分

搜索结果包含 `relevance_score` 字段，综合考量：
- 向量距离（余弦相似度）
- 关键词匹配度
- 综合排序

## 相关文档

- [[modules/vector-service|向量服务模块]]
- [[modules/backend-api|后端 API 服务模块]]
- [[apis/rest-api|RESTful API 文档]]
