---
type: function
title: 关键函数文档
updated: 2026-04-25
tags: [functions, backend]
---

# 关键函数文档

## 后端核心函数

### URL 处理函数

**文件：** [platform_parser.py](file:///d:/python/code/myself/collectly/backend/app/services/platform_parser.py)

#### `extract_url(text: str) -> str`

从带文案的分享文本中提取 HTTP 链接。支持抖音、小红书、B站、知乎等平台的链接格式。

#### `resolve_short_url(url: str) -> str`

短链还原函数，追踪重定向获取真实长链接。支持 `b23.tv`、`v.douyin.com` 等短域名。

#### `resolve_xhs_short(url: str) -> str`

小红书专用短链还原，使用完整的浏览器 User-Agent 头进行重定向追踪。

#### `clean_pure_url(url: str) -> str`

清理 URL 中的追踪参数，生成永久纯净链接。各平台处理策略不同：
- **抖音** — 提取 `modal_id` 参数，生成标准视频链接
- **B站** — 保留 `p=` 分P参数，删除其他追踪参数
- **知乎** — 保留专栏路径

### 内容管理函数

**文件：** [content_manager.py](file:///d:/python/code/myself/collectly/backend/app/services/content_manager.py)

#### `_build_embedding_text(content: ContentResponse) -> str`

构建用于向量化的完整文本，组合标题、摘要、内容（前 3000 字）、知识点和标签。

#### `_generate_hash(content: ContentResponse) -> str`

基于标题和内容生成 MD5 哈希，用于内容去重。

#### `_check_duplicate(hash: str, url: str) -> Optional[str]`

检查内容是否已存在，支持哈希匹配和 URL 匹配两种方式。

### 时间戳工具函数

**文件：** [timestamp_utils.py](file:///d:/python/code/myself/collectly/python-parser/timestamp_utils.py)

| 函数 | 说明 |
|------|------|
| `timestamp_to_date()` | 时间戳 → `YYYY-MM-DD` 格式 |
| `timestamp_to_datetime()` | 时间戳 → datetime 对象 |
| `timestamp_to_chinese_date()` | 时间戳 → `YYYY年MM月DD日` 格式 |

## 前端关键函数

**文件：** [api.ts](file:///d:/python/code/myself/collectly/src/utils/api.ts)

| 函数 | 说明 |
|------|------|
| `parseLink(url)` | 解析单个链接 |
| `parseLinks(urls)` | 批量解析链接 |
| `saveContent(content)` | 保存内容 |
| `search(query)` | 智能搜索 |
| `updateLearningStatus(id, status)` | 更新学习状态 |
| `updateTags(id, tags)` | 更新标签 |
| `updateNote(id, note)` | 更新笔记 |
| `getContent(id)` | 获取内容详情 |
| `getLearningStats()` | 获取学习统计 |
| `getVectorStats()` | 获取向量统计 |
| `reEmbedContent(id)` | 重新生成向量 |
| `rebuildAllVectors()` | 全量重建向量索引 |

## 相关文档

- [[modules/backend-api|后端 API 服务模块]]
- [[modules/frontend|前端应用模块]]
