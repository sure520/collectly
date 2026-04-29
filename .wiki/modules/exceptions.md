---
type: module
title: 异常处理模块
module: exceptions
source_path: backend/app/utils/exceptions.py
updated: 2026-04-25
tags: [backend, error-handling]
---

# 异常处理模块

## 概述

定义应用级异常类和全局异常处理器，提供统一的错误响应格式。

## 异常类

| 异常类 | HTTP 状态码 | 说明 |
|--------|-------------|------|
| `AppException` | 500 | 应用异常基类 |
| `PlatformParseError` | 400 | 平台链接解析失败 |
| `ContentNotFoundError` | 404 | 内容不存在 |
| `DuplicateContentError` | 409 | 内容重复 |
| `InvalidStatusError` | 400 | 无效的学习状态 |

## 全局处理器

注册三个全局异常处理器：
1. `AppException` — 应用级异常
2. `HTTPException` — FastAPI HTTP 异常
3. `Exception` — 未捕获的通用异常

所有异常统一返回 JSON 格式：
```json
{
  "error": "错误描述信息"
}
```

## 相关文档

- [[modules/backend-api|后端 API 服务模块]]
