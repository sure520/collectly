---
type: module
title: Python 解析服务模块
module: python-parser
source_path: python-parser/
updated: 2026-04-25
tags: [backend, parser, fastapi]
---

# Python 解析服务模块

## 概述

`python-parser` 是一个独立的网页内容解析服务，基于 FastAPI 构建。它可以从任意 URL 中提取正文内容、标题、作者等信息，并支持 AI 摘要生成。

## 目录结构

```
python-parser/
├── main.py                # FastAPI 应用入口
├── content_extractor.py   # 网页内容提取器
├── summarizer.py          # AI 摘要生成器
├── timestamp_utils.py     # 时间戳工具函数
├── test_api.py            # API 测试
└── requirements.txt       # 依赖清单
```

## 核心组件

### ContentExtractor

通用的网页内容提取器，支持多种提取策略：
- **通用提取** — 使用 Trafilatura + Readability 提取正文
- **平台特定** — 针对抖音、知乎、微信公众号的定制提取
- **编码自动检测** — 支持 UTF-8、GBK、Latin-1 等多种编码

### Summarizer

基于 DashScope API 的 AI 摘要生成器：
- 使用 `qwen-turbo` 模型
- 200 字以内中文摘要
- 失败时回退到文本截断

### TimestampUtils

时间戳转换工具函数：
- `timestamp_to_date()` — 转为 `YYYY-MM-DD` 格式
- `timestamp_to_datetime()` — 转为 datetime 对象
- `timestamp_to_chinese_date()` — 转为中文日期格式

## API 接口

| 端点 | 方法 | 说明 |
|------|------|------|
| `/parse` | POST | 解析 URL 内容 |

请求参数：
- `url` — 目标 URL
- `include_summary` — 是否生成摘要（默认 true）
- `timeout` — 超时时间（默认 30 秒）

## 相关文档

- [[modules/backend-api|后端 API 服务模块]]
- [[modules/platform-parser|平台解析器模块]]
