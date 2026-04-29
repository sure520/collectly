---
type: module
title: 学习管理器模块
module: learning-manager
source_path: backend/app/services/learning_manager.py
updated: 2026-04-25
tags: [backend, learning, status]
---

# 学习管理器模块

## 概述

`LearningManager` 管理内容的学习生命周期，支持状态流转、标签管理和笔记功能，帮助用户系统化地消化知识。

## 学习状态流水线

```
[未读] → [已读] → [重点] → [待复习]
   ↑                        ↓
   └────── [归档] ←─────────┘
```

| 状态 | 说明 |
|------|------|
| 未读 | 刚收藏，尚未阅读 |
| 已读 | 已阅读完成 |
| 重点 | 标记为重要内容 |
| 待复习 | 需要定期复习 |

## 核心功能

### 状态管理

```python
async def update_status(content_id: str, status: str) -> bool
async def get_status(content_id: str) -> str
```

### 标签管理

```python
async def update_tags(content_id: str, tags: List[str]) -> bool
```

### 笔记管理

```python
async def update_note(content_id: str, note: str) -> bool
async def get_note(content_id: str) -> str
```

### 统计分析

```python
async def get_stats() -> dict
```

返回统计数据包括：
- 总内容数
- 各状态内容数
- 各平台内容数
- 各领域内容数

## 相关文档

- [[modules/backend-api|后端 API 服务模块]]
- [[apis/rest-api|RESTful API 文档]]
