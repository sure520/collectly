# LLM 服务模块

基于 DashScope API 的内容处理服务，使用 qwen3.5-35b-a3b 模型提供智能内容分析功能。

## 功能特性

### 核心功能
- ✅ **智能摘要生成**: 自动提取文章核心内容，生成简洁摘要
- ✅ **关联标签创建**: 基于内容语义生成相关标签
- ✅ **知识点提取**: 识别并提取关键技术概念和知识点

### 技术特性
- ✅ **错误处理**: 完善的异常处理机制，包括超时、网络错误、无效响应等
- ✅ **重试机制**: 自动重试（最多 3 次），提高请求成功率
- ✅ **输入校验**: 严格的内容格式和长度验证
- ✅ **详细日志**: 记录请求参数、响应状态和处理耗时
- ✅ **模块化设计**: 独立的服务类，易于维护和测试
- ✅ **降级方案**: API 失败时自动切换到基于规则的备用方案

## 快速开始

### 1. 配置 API Key

在 `.env` 文件中配置 DashScope API Key:

```env
DASHSCOPE_API_KEY=your_api_key_here
```

### 2. 基本使用

```python
import asyncio
from app.services.llm_service import LLMService

async def main():
    llm = LLMService()
    content = "你的文章内容..."
    
    # 生成摘要
    summary = await llm.generate_summary(content)
    
    # 生成标签
    tags = await llm.generate_tags(content)
    
    # 提取知识点
    points = await llm.extract_knowledge_points(content)

asyncio.run(main())
```

### 3. 在 PlatformParser 中使用

```python
from app.services.platform_parser import PlatformParser

parser = PlatformParser()
result = await parser.parse("https://example.com/article")

# 自动使用 LLM 处理内容
print(result.summary)  # 智能摘要
print(result.tags)     # 关联标签
print(result.knowledge_points)  # 知识点
```

## API 参考

### LLMService 类

#### 初始化
```python
llm = LLMService(api_key=None)
```
- `api_key`: 可选，默认从环境变量读取

#### 方法

##### generate_summary(content, timeout=60)
生成内容摘要
- `content`: 原始内容（字符串）
- `timeout`: 超时时间（秒），默认 60
- 返回：摘要字符串

##### generate_tags(content, timeout=60)
生成关联标签
- `content`: 原始内容（字符串）
- `timeout`: 超时时间（秒），默认 60
- 返回：标签列表

##### extract_knowledge_points(content, timeout=60)
提取核心知识点
- `content`: 原始内容（字符串）
- `timeout`: 超时时间（秒），默认 60
- 返回：知识点列表

##### process_content(content, timeout=60, ...)
综合处理内容（并行调用）
- `content`: 原始内容
- `timeout`: 单个任务超时
- `include_summary/tags/knowledge_points`: 布尔值，控制处理项
- 返回：包含各项结果的字典

## 错误处理

### 异常类型

- `LLMServiceError`: 基础异常类
  - `message`: 错误消息
  - `error_code`: 错误码
  - `status_code`: HTTP 状态码（如有）

- `LLMServiceTimeout`: 请求超时
- `LLMServiceValidationError`: 输入校验失败

### 错误码说明

- `TIMEOUT`: 请求超时
- `NETWORK_ERROR`: 网络错误
- `HTTP_4XX/5XX`: HTTP 错误状态码
- `INVALID_RESPONSE`: API 响应格式无效
- `PARSE_ERROR`: 响应解析失败

### 示例

```python
from app.services.llm_service import LLMService, LLMServiceError

llm = LLMService()

try:
    result = await llm.generate_summary(content)
except LLMServiceTimeout as e:
    print(f"请求超时：{e.message}")
except LLMServiceValidationError as e:
    print(f"输入校验失败：{e.message}")
except LLMServiceError as e:
    print(f"API 错误 [{e.error_code}]: {e.message}")
```

## 日志记录

服务会记录详细的日志信息:

```
[请求 ID] 开始调用 DashScope API
[请求 ID] 请求参数：{...}
[请求 ID] API 调用成功，耗时：1.23 秒
[请求 ID] 响应数据：{...}
```

日志级别:
- `INFO`: 请求开始/结束、处理成功
- `DEBUG`: 详细的请求/响应数据
- `WARNING`: 重试、降级
- `ERROR`: 错误、异常

## 最佳实践

### 1. 并行处理
```python
# 同时执行多个任务
results = await asyncio.gather(
    llm.generate_summary(content),
    llm.generate_tags(content),
    llm.extract_knowledge_points(content)
)
```

### 2. 超时设置
- 短内容：30-60 秒
- 长内容：60-120 秒
- 批量处理：适当增加超时时间

### 3. 错误恢复
```python
async def robust_process(content):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return await llm.generate_summary(content)
        except LLMServiceError:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(1.0 * attempt)
```

## 测试

运行测试:
```bash
cd backend
python -m pytest tests/test_llm_service.py -v
```

或运行独立测试:
```bash
python tests/test_llm_service.py
```

## 示例代码

查看 `examples/llm_usage_examples.py` 获取更多使用示例。

## 依赖

- `aiohttp`: 异步 HTTP 客户端
- `python-dotenv`: 环境变量管理
- `pydantic-settings`: 配置管理

## 模型信息

- **模型名称**: qwen3.5-35b-a3b
- **提供商**: DashScope (阿里云)
- **默认超时**: 60 秒
- **最大重试**: 3 次
- **温度参数**: 0.7
- **最大 token**: 500

## 注意事项

1. **API Key 安全**: 不要将 API Key 提交到版本控制系统
2. **内容长度**: 建议控制在 10000 字符以内
3. **并发限制**: 注意 API 的并发请求限制
4. **成本控制**: 监控 API 调用次数和 token 消耗
5. **降级方案**: 生产环境建议保留备用方案

## 故障排查

### 常见问题

**Q: 收到 "API Key 未配置" 错误**
A: 检查 `.env` 文件中是否正确配置了 `DASHSCOPE_API_KEY`

**Q: 请求频繁超时**
A: 增加 `timeout` 参数值，或检查网络连接

**Q: 标签/知识点数量不符合预期**
A: 调整提示词或后处理逻辑

**Q: API 返回错误状态码**
A: 查看错误日志，确认 API Key 有效性和配额

## 更新日志

### v1.0.0
- ✅ 初始版本
- ✅ 集成 DashScope API
- ✅ 实现摘要、标签、知识点功能
- ✅ 完善错误处理和日志记录
- ✅ 添加输入校验和重试机制
- ✅ 提供降级方案
