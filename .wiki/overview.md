---
type: overview
title: Collectly 项目概览
updated: 2026-04-25
---

# Collectly 项目概览

Collectly（AI 知识收藏与检索管家）是一个智能知识管理工具，旨在将零散的网络内容转化为系统化的知识资产。它支持从多个主流中文平台抓取内容，通过 AI 进行智能处理，并提供强大的检索和学习管理功能。

## 核心理念

> **"收藏"** 只是开始，**"管理"** 才是精髓。

与传统书签工具只存储不同，Collectly 通过以下方式管理你的知识：

- **生命周期管理** — 内容在阶段中流转：未读 → 阅读中 → 重点 → 待复习
- **智能分类** — AI 自动打标签、生成摘要、提取知识点
- **主动回忆系统** — 智能提醒需要复习的内容
- **学习分析** — 用详细洞察追踪你的知识获取旅程

## 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                      内容生命周期                            │
├─────────────────────────────────────────────────────────────┤
│   捕获  →  解析  →  精炼  →  存储  →  管理  →  检索        │
│    ↓        ↓        ↓        ↓        ↓          ↓        │
│  [URL]   [平台]    [LLM]   [SQLite]  [状态]    [搜索]      │
│          [API]     [AI]    [去重]    [标签]    [筛选]      │
│                    [标签]            [笔记]                │
└─────────────────────────────────────────────────────────────┘
```

## 技术栈

### 后端
- **框架**: FastAPI (Python)
- **AI 服务**: DashScope (通义千问 qwen-plus)
- **向量数据库**: ChromaDB (本地持久化)
- **关系数据库**: SQLite
- **平台数据**: TikHub API

### 前端
- **框架**: React 18 + TypeScript
- **构建工具**: Webpack 5
- **样式**: Tailwind CSS
- **UI 组件**: Framer Motion, Lucide React, Recharts
- **路由**: React Router v6

### 部署
- **容器化**: Docker / Docker Compose
- **部署模式**: 本地部署 + 内网穿透 / 云服务器公网部署
- **Web 服务器**: Nginx (前端静态资源)

## 支持平台

| 平台 | 说明 |
|------|------|
| 抖音 | 视频语音转文字提取 |
| 小红书 | 生活方式与产品洞察 |
| 微信公众号 | 专业博客与行业分析 |
| B站 | 教育视频与字幕提取 |
| 知乎 | 专家问答与深度文章 |
| CSDN | 技术教程与代码方案 |

## 项目结构

```
collectly/
├── backend/                    # 核心 API 服务
│   ├── app/
│   │   ├── api/               # RESTful 接口
│   │   ├── models/            # 数据模型
│   │   ├── services/          # 业务逻辑
│   │   └── utils/             # 工具函数
│   └── tests/                 # 后端测试
├── python-parser/              # 独立解析服务
├── src/                        # React 前端
│   ├── components/             # UI 组件
│   ├── hooks/                  # React Hooks
│   ├── utils/                  # 前端工具
│   └── types/                  # TypeScript 类型
├── functions/                  # Supabase Edge Functions
├── tests/                      # 平台解析测试
├── docs/                       # 项目文档
└── 配置文件                     # Docker, Nginx, Webpack 等
```

## 快速部署

项目支持两种部署模式：

1. **本地部署 + 内网穿透** — 适合个人电脑使用，零服务器成本
2. **云服务器公网部署** — 24 小时在线，适合团队使用

详见 [[configs/deployment|部署配置]]。

## 相关文档

- [[modules/backend-api|后端 API 服务模块]]
- [[modules/python-parser|Python 解析服务模块]]
- [[modules/frontend|前端应用模块]]
- [[apis/rest-api|RESTful API 文档]]
- [[configs/environment|环境变量配置]]
