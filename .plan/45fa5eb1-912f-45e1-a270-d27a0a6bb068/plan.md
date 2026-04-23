# 问题修复计划

## 问题描述
用户点击"开始解析"按钮后，显示解析完成，但没有返回解析内容。

## 问题分析
1. 前端调用 Edge Function `parse-content`
2. Edge Function 尝试调用本地 Python 服务 `http://localhost:8000/parse`
3. 但 Edge Function 运行在云端，无法访问本地 localhost
4. 导致解析失败，但错误处理不完善，前端显示完成但没有内容

## 修复方案
1. 修改前端代码，直接调用 Python 解析服务（绕过 Edge Function）
2. 或者修改 Edge Function 使用纯 LLM 方式解析（不依赖本地服务）

## 实施步骤
1. 修改 `src/hooks/useKnowledge.ts` 中的 `parseAndAddItem` 函数
2. 直接调用 Python 服务的 `/parse` 接口
3. 获取结果后存入 Supabase
