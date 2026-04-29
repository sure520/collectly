---
type: module
title: 配置模块
module: config
source_path: backend/app/utils/config.py
updated: 2026-04-25
tags: [backend, config]
---

# 配置模块

## 概述

使用 Pydantic Settings 管理应用配置，支持从 `.env` 文件加载环境变量。配置类 `Settings` 集中管理所有外部依赖的密钥和连接信息。

## 配置项

| 配置项 | 环境变量 | 默认值 | 说明 |
|--------|----------|--------|------|
| `TIKHUB_API_KEY` | `TIKHUB_API_KEY` | `""` | TikHub API 密钥 |
| `TIKHUB_API_URL` | — | `https://api.tikhub.dev` | TikHub API 地址 |
| `DASHSCOPE_API_KEY` | `DASHSCOPE_API_KEY` | `""` | DashScope API 密钥 |
| `QDRANT_API_KEY` | `QDRANT_API_KEY` | `""` | Qdrant 向量库密钥 |
| `QDRANT_CLUSTER_ENDPOINT` | `QDRANT_CLUSTER_ENDPOINT` | `""` | Qdrant 集群端点 |
| `DATABASE_URL` | — | `sqlite:///knowledge.db` | 数据库连接 |
| `APP_NAME` | — | `AI 知识收藏与检索管家` | 应用名称 |
| `DEBUG` | — | `True` | 调试模式 |

## 相关文档

- [[configs/environment|环境变量配置]]
- [[modules/backend-api|后端 API 服务模块]]
