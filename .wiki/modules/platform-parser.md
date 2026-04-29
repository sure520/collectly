---
type: module
title: 平台解析器模块
module: platform-parser
source_path: backend/app/services/platform_parser.py
updated: 2026-04-25
tags: [backend, parser, platform]
---

# 平台解析器模块

## 概述

`PlatformParser` 是 Collectly 的内容捕获核心，负责从各主流中文平台的 URL 中提取结构化内容。它通过 TikHub API 获取平台数据，并利用 LLM 进行内容精炼。

## 核心功能

### URL 处理

```python
# URL 提取 — 从带文案的分享文本中提取链接
extract_url(text: str) -> str

# 短链还原 — 追踪重定向获取真实长链接
resolve_short_url(url: str) -> str
resolve_xhs_short(url: str) -> str  # 小红书专用

# 链接净化 — 清理追踪参数，生成永久纯净链接
clean_pure_url(url: str) -> str
```

### 平台解析

每个平台有独立的解析方法：

| 方法 | 平台 | 说明 |
|------|------|------|
| `_parse_douyin()` | 抖音 | 视频内容 + 语音转文字 |
| `_parse_xiaohongshu()` | 小红书 | 图文笔记 |
| `_parse_bilibili()` | B站 | 视频 + 字幕提取 |
| `_parse_zhihu()` | 知乎 | 文章/问答 |
| `_parse_weixin()` | 微信公众号 | 文章内容 |

### AI 精炼

解析完成后，调用 LLM 服务进行：
- **智能摘要** — 200 字精华摘要
- **自动标签** — 5-10 个多维度标签
- **知识点提取** — 识别关键概念

## 数据流

```
URL 输入 → URL 提取/净化 → 短链还原 → TikHub API 调用
    → 平台特定解析 → LLM 精炼 → ContentResponse 输出
```

## 错误处理

- 无效 URL 格式 → 返回错误信息
- 平台解析失败 → 返回 `PlatformParseError`
- LLM 调用失败 → 返回原始内容，跳过精炼步骤

## 相关文档

- [[modules/backend-api|后端 API 服务模块]]
- [[modules/llm-service|LLM 服务模块]]
- [[apis/rest-api|RESTful API 文档]]
