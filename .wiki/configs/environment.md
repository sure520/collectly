---
type: config
title: 环境变量配置
module: config
source_path: .env.example
updated: 2026-04-25
tags: [config, environment]
---

# 环境变量配置

## 概述

Collectly 使用 `.env` 文件管理环境变量配置。参考模板文件为 `.env.example`。

## 配置项

### 部署模式

| 变量 | 说明 | 可选值 |
|------|------|--------|
| `DEPLOY_MODE` | 部署模式 | `local`（本地部署）/ `cloud`（云服务器） |

### 后端配置

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `BACKEND_HOST` | `0.0.0.0` | 后端监听地址 |
| `BACKEND_PORT` | `8000` | 后端监听端口 |

### 前端配置

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `API_BASE_URL` | `http://localhost:8000/api` | 后端 API 地址 |

### API 密钥

| 变量 | 说明 |
|------|------|
| `TIKHUB_API_KEY` | TikHub API 密钥（平台数据接入） |
| `DASHSCOPE_API_KEY` | DashScope API 密钥（AI 能力） |

### 访问控制（可选）

| 变量 | 说明 |
|------|------|
| `ACCESS_PASSWORD` | 访问密码 |
| `ACCESS_TOKEN` | 访问令牌 |
| `WHITE_LIST_IPS` | IP 白名单 |

## 部署模式说明

### 方案 A：本地部署 + 内网穿透

- 运行位置：本地 Windows/Mac 电脑
- 外网打通：Cloudflare Tunnel / ngrok / frp
- 优势：零服务器成本，数据完全本地私有化

### 方案 B：云服务器公网部署

- 运行位置：带独立公网 IP 的云轻量服务器
- 外网打通：固定公网 IP / 自定义域名 + HTTPS
- 优势：24 小时永久在线，不依赖个人电脑

## 相关文档

- [[modules/config|配置模块]]
- [[configs/deployment|部署配置]]
