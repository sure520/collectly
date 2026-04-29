---
type: module
title: 前端应用模块
module: frontend
source_path: src/
updated: 2026-04-25
tags: [frontend, react, typescript]
---

# 前端应用模块

## 概述

前端应用基于 React 18 + TypeScript 构建，使用 Webpack 5 打包，Tailwind CSS 进行样式设计。提供直观的 UI 界面，支持内容收藏、搜索、管理和学习追踪。

## 目录结构

```
src/
├── components/           # UI 组件
│   ├── Dashboard.tsx     # 仪表盘
│   ├── DetailModal.tsx   # 内容详情弹窗
│   ├── FilterPanel.tsx   # 筛选面板
│   ├── KnowledgeCard.tsx # 知识卡片
│   ├── KnowledgeList.tsx # 知识列表
│   ├── Layout.tsx        # 布局组件
│   ├── LinkInput.tsx     # 链接输入
│   ├── Search.tsx        # 搜索组件
│   ├── Settings.tsx      # 设置页面
│   └── Stats.tsx         # 统计页面
├── hooks/
│   ├── useKnowledge.ts   # 知识管理 Hook
│   └── useTheme.ts       # 主题 Hook
├── styles/
│   └── index.css         # 全局样式
├── types/
│   └── index.ts          # TypeScript 类型定义
├── utils/
│   ├── api.ts            # API 调用封装
│   ├── format.ts         # 格式化工具
│   ├── platform.ts       # 平台检测工具
│   └── types.ts          # 类型工具
├── App.tsx               # 应用入口组件
└── index.tsx             # 渲染入口
```

## 核心组件

### Layout

应用布局组件，提供导航栏和页面容器。

### Dashboard

仪表盘页面，展示学习统计概览和最近内容。

### LinkInput

链接输入组件，支持批量输入 URL 进行内容收藏。

### KnowledgeList / KnowledgeCard

知识列表和卡片组件，支持网格/列表两种视图模式。

### Search

搜索组件，支持关键词搜索和语义搜索。

### FilterPanel

筛选面板，支持按领域、平台、难度、状态等多维度筛选。

### DetailModal

内容详情弹窗，展示完整内容、AI 摘要、标签、知识点，支持笔记编辑和状态更新。

### Stats

学习统计页面，使用 Recharts 图表展示学习进度。

### Settings

设置页面，管理 API 密钥和应用配置。

## 类型系统

```typescript
// 核心类型
type Platform = 'wechat' | 'zhihu' | 'csdn' | 'bilibili' | 'douyin' | 'xiaohongshu'
type Domain = 'llm' | 'agent' | 'rag' | 'multimodal'
type LearningStatus = 'unread' | 'read' | 'important' | 'review'

// 知识条目
interface KnowledgeItem {
  id: string
  title: string
  content: string
  platform: Platform
  domains: Domain[]
  status: LearningStatus
  // ...
}
```

## 相关文档

- [[apis/rest-api|RESTful API 文档]]
- [[overview|项目概览]]
