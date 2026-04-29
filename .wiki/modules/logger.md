---
type: module
title: 日志模块
module: logger
source_path: backend/app/utils/logger.py
updated: 2026-04-25
tags: [backend, logging]
---

# 日志模块

## 概述

提供文件和控制台双输出日志系统，支持按日期自动分割日志文件。

## 特性

- **双输出** — 同时输出到控制台和文件
- **自动分割** — 按日期生成日志文件（`app_YYYYMMDD.log`）
- **级别控制** — 文件输出 DEBUG 级别，控制台输出 INFO 级别
- **统一格式** — `时间 - 模块名 - 级别 - 消息`

## 使用方式

```python
from app.utils.logger import get_logger

logger = get_logger("my_module")
logger.info("信息日志")
logger.error("错误日志", exc_info=True)
```

## 日志文件

日志文件存储在项目根目录的 `logs/` 文件夹中。

## 相关文档

- [[modules/backend-api|后端 API 服务模块]]
