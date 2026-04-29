---
type: module
title: LLM 服务模块
module: llm-service
source_path: backend/app/services/llm_service.py
updated: 2026-04-25
tags: [backend, ai, llm, dashscope]
---

# LLM 服务模块

## 概述

`LLMService` 封装了 DashScope（阿里云通义千问）API 的调用，提供内容摘要、标签生成、知识点提取等 AI 能力。使用 `qwen-plus` 模型进行文本生成，`qwen3-asr-flash` 模型进行语音识别。

## 核心能力

### 内容摘要

```python
def generate_summary(content: str) -> str
```

生成 200 字以内的精华摘要，提取核心观点和关键信息。

### 标签生成

```python
def generate_tags(content: str) -> List[str]
```

生成 5-10 个多维度标签，涵盖技术领域、应用场景、核心概念等。

### 知识点提取

```python
def extract_knowledge_points(content: str) -> List[str]
```

识别并提取内容中的关键概念和要点。

## 错误处理

| 异常类 | 说明 |
|--------|------|
| `LLMServiceError` | 服务异常基类 |
| `LLMServiceTimeout` | 请求超时异常 |
| `LLMServiceValidationError` | 输入校验异常 |

### 重试机制

- 最大重试次数：3 次
- 重试间隔：1 秒
- 超时时间：60 秒

### 输入校验

- 内容不能为空
- 内容必须是字符串
- 内容长度不超过 10000 字符
- 内容不能全为空白字符

## 提示词模板

每个任务类型有独立的提示词模板：
- `summary` — 摘要生成
- `tags` — 标签生成
- `knowledge_points` — 知识点提取

## 相关文档

- [[modules/platform-parser|平台解析器模块]]
- [[modules/backend-api|后端 API 服务模块]]
