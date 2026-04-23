import asyncio
import time
import os
from typing import Optional, List, Dict, Any
from http import HTTPStatus
import dashscope
from dashscope import Generation, MultiModalConversation
from dashscope.api_entities.dashscope_response import Role
from app.utils.config import get_settings
from app.utils.logger import get_logger

settings = get_settings()
logger = get_logger("llm_service")


class LLMServiceError(Exception):
    """LLM 服务异常基类"""
    def __init__(self, message: str, error_code: Optional[str] = None, status_code: Optional[int] = None):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(self.message)


class LLMServiceTimeout(LLMServiceError):
    """LLM 服务超时异常"""
    pass


class LLMServiceValidationError(LLMServiceError):
    """LLM 服务输入校验异常"""
    pass


class LLMService:
    """
    DashScope LLM 服务客户端
    
    提供与大语言模型的交互功能，支持内容摘要、标签生成、知识点提取等功能
    使用 qwen-plus 模型
    """
    
    LLM_MODEL_NAME = "qwen-plus"
    ASR_MODEL_NAME = "qwen3-asr-flash"
    DEFAULT_TIMEOUT = 60
    MAX_RETRIES = 3
    RETRY_DELAY = 1.0
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化 LLM 服务
        
        Args:
            api_key: DashScope API Key，如果不传则从环境变量获取
        """
        self.api_key = api_key or settings.DASHSCOPE_API_KEY
        if not self.api_key:
            raise LLMServiceError("DashScope API Key 未配置")
        
        dashscope.api_key = self.api_key
    
    def _validate_input(self, content: str, max_length: int = 10000) -> None:
        """
        输入内容校验
        
        Args:
            content: 待校验的内容
            max_length: 最大长度限制
            
        Raises:
            LLMServiceValidationError: 校验失败时抛出
        """
        if not content:
            raise LLMServiceValidationError("输入内容不能为空")
        
        if not isinstance(content, str):
            raise LLMServiceValidationError("输入内容必须是字符串类型")
        
        if len(content) > max_length:
            raise LLMServiceValidationError(f"输入内容过长，最大支持{max_length}字符，当前{len(content)}字符")
        
        content_trimmed = content.strip()
        if not content_trimmed:
            raise LLMServiceValidationError("输入内容不能全为空白字符")
    
    def _build_prompt(self, task_type: str, content: str) -> str:
        """
        构建不同任务的提示词
        
        Args:
            task_type: 任务类型 (summary/tags/knowledge_points)
            content: 原始内容
            
        Returns:
            构建好的提示词
        """
        prompts = {
            "summary": f"""请为以下内容生成一个简洁的摘要（200 字以内）：

{content}

要求：
1. 准确概括核心内容
2. 语言简洁明了
3. 突出关键信息
4. 保持逻辑连贯

请直接输出摘要内容，不要添加其他说明。""",
            
            "tags": f"""请为以下内容提取 5-10 个关键标签：

{content}

要求：
1. 标签应准确反映内容主题
2. 涵盖技术领域、应用场景、核心概念等维度
3. 每个标签 2-8 个字
4. 标签之间用逗号分隔

请只输出标签列表，格式如：标签 1，标签 2，标签 3""",
            
            "knowledge_points": f"""请从以下内容中提取核心知识点：

{content}

要求：
1. 提取重要的技术概念、原理、方法
2. 每个知识点简洁明了（不超过 30 字）
3. 按重要性排序
4. 避免重复

请直接输出知识点列表，每行一个知识点。"""
        }
        
        return prompts.get(task_type, content)
    
    def _parse_response(self, response: Any, task_type: str) -> Any:
        """
        解析 DashScope SDK 响应数据
        
        Args:
            response: SDK 返回的响应对象
            task_type: 任务类型
            
        Returns:
            解析后的结果
            
        Raises:
            LLMServiceError: 响应解析失败时抛出
        """
        try:
            if response.status_code != HTTPStatus.OK:
                raise LLMServiceError(
                    f"DashScope API 返回错误：{response.message}",
                    error_code=response.code,
                    status_code=response.status_code
                )
            
            output = response.output
            if not output:
                raise LLMServiceError("API 响应缺少 output 字段", error_code="INVALID_RESPONSE")
            
            text = None
            if output.get("text"):
                text = output.get("text", "").strip()
            elif output.get("choices"):
                choices = output.get("choices", [])
                if choices and len(choices) > 0:
                    message = choices[0].get("message", {})
                    if message:
                        text = message.get("content", "")
                    if text:
                        text = text.strip()
            
            if not text:
                logger.error(f"响应解析失败，output 结构: {dict(output)}")
                raise LLMServiceError("API 响应缺少文本内容", error_code="INVALID_RESPONSE")
            
            if task_type == "tags":
                tags = [tag.strip() for tag in text.replace("，", ",").split(",") if tag.strip()]
                return tags[:10]
            
            elif task_type == "knowledge_points":
                points = [line.strip() for line in text.split("\n") if line.strip()]
                return points[:10]
            
            else:
                return text[:200]
                
        except LLMServiceError:
            raise
        except Exception as e:
            raise LLMServiceError(f"解析响应失败：{str(e)}", error_code="PARSE_ERROR")
    
    def _make_request(
        self,
        prompt: str,
        timeout: int = DEFAULT_TIMEOUT
    ) -> Any:
        """
        使用 DashScope SDK 发送请求
        
        Args:
            prompt: 提示词
            timeout: 超时时间（秒）
            
        Returns:
            SDK 响应对象
            
        Raises:
            LLMServiceTimeout: 请求超时
            LLMServiceError: 其他错误
        """
        messages = [
            {"role": Role.USER, "content": prompt}
        ]
        
        request_id = f"{int(time.time())}-{id(self)}"
        start_time = time.time()
        
        logger.info(f"[请求 {request_id}] 开始调用 DashScope API，模型：{self.LLM_MODEL_NAME}")
        logger.debug(f"[请求 {request_id}] 提示词长度：{len(prompt)} 字符")
        
        try:
            response = Generation.call(
                model=self.LLM_MODEL_NAME,
                messages=messages,
                result_format='message',
                temperature=0.7,
                max_tokens=500
            )
            
            elapsed_time = time.time() - start_time
            
            if response.status_code == HTTPStatus.OK:
                logger.info(f"[请求 {request_id}] API 调用成功，耗时：{elapsed_time:.2f}秒")
                output_text = response.output.get('text') or ''
                if not output_text and response.output.get('choices'):
                    output_text = response.output['choices'][0]['message']['content'] or ''
                logger.debug(f"[请求 {request_id}] 响应内容：{output_text[:200]}")
                return response
            else:
                logger.error(f"[请求 {request_id}] API 返回错误状态码：{response.status_code}")
                logger.error(f"[请求 {request_id}] 错误码：{response.code}，错误信息：{response.message}")
                raise LLMServiceError(
                    f"DashScope API 返回错误：{response.message}",
                    error_code=response.code,
                    status_code=response.status_code
                )
                
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(f"[请求 {request_id}] 请求异常，耗时：{elapsed_time:.2f}秒，错误：{str(e)}")
            raise LLMServiceError(f"请求异常：{str(e)}", error_code="REQUEST_ERROR")
    
    def _request_with_retry(
        self,
        prompt: str,
        timeout: int = DEFAULT_TIMEOUT,
        max_retries: int = MAX_RETRIES
    ) -> Any:
        """
        带重试机制的 API 请求
        
        Args:
            prompt: 提示词
            timeout: 超时时间
            max_retries: 最大重试次数
            
        Returns:
            SDK 响应对象
        """
        last_exception = None
        
        for attempt in range(1, max_retries + 1):
            try:
                return self._make_request(prompt, timeout)
            except (LLMServiceTimeout, LLMServiceError) as e:
                last_exception = e
                if attempt < max_retries:
                    wait_time = self.RETRY_DELAY * attempt
                    logger.warning(f"API 请求失败，{wait_time}秒后重试（第{attempt}/{max_retries}次）: {str(e)}")
                    time.sleep(wait_time)
                else:
                    logger.error(f"API 请求失败，已达到最大重试次数{max_retries}")
                    raise
        
        if last_exception:
            raise last_exception
        raise LLMServiceError("未知错误", error_code="UNKNOWN_ERROR")
    
    def generate_summary(self, content: str, timeout: int = DEFAULT_TIMEOUT) -> str:
        """
        使用 LLM 生成内容摘要
        
        Args:
            content: 原始内容
            timeout: 超时时间（秒）
            
        Returns:
            生成的摘要
            
        Raises:
            LLMServiceValidationError: 输入校验失败
            LLMServiceTimeout: API 超时
            LLMServiceError: 其他错误
        """
        self._validate_input(content)
        prompt = self._build_prompt("summary", content)
        
        try:
            response = self._request_with_retry(prompt, timeout)
            summary = self._parse_response(response, "summary")
            return summary
        except (LLMServiceTimeout, LLMServiceError):
            raise
        except Exception as e:
            logger.error(f"生成摘要失败：{str(e)}")
            raise LLMServiceError(f"生成摘要失败：{str(e)}", error_code="GENERATE_SUMMARY_ERROR")
    
    def generate_tags(self, content: str, timeout: int = DEFAULT_TIMEOUT) -> List[str]:
        """
        使用 LLM 生成关联标签
        
        Args:
            content: 原始内容
            timeout: 超时时间（秒）
            
        Returns:
            标签列表
            
        Raises:
            LLMServiceValidationError: 输入校验失败
            LLMServiceTimeout: API 超时
            LLMServiceError: 其他错误
        """
        self._validate_input(content)
        prompt = self._build_prompt("tags", content)
        
        try:
            response = self._request_with_retry(prompt, timeout)
            tags = self._parse_response(response, "tags")
            return tags
        except (LLMServiceTimeout, LLMServiceError):
            raise
        except Exception as e:
            logger.error(f"生成标签失败：{str(e)}")
            raise LLMServiceError(f"生成标签失败：{str(e)}", error_code="GENERATE_TAGS_ERROR")
    
    def extract_knowledge_points(self, content: str, timeout: int = DEFAULT_TIMEOUT) -> List[str]:
        """
        使用 LLM 提取核心知识点
        
        Args:
            content: 原始内容
            timeout: 超时时间（秒）
            
        Returns:
            知识点列表
            
        Raises:
            LLMServiceValidationError: 输入校验失败
            LLMServiceTimeout: API 超时
            LLMServiceError: 其他错误
        """
        self._validate_input(content)
        prompt = self._build_prompt("knowledge_points", content)
        
        try:
            response = self._request_with_retry(prompt, timeout)
            points = self._parse_response(response, "knowledge_points")
            return points
        except (LLMServiceTimeout, LLMServiceError):
            raise
        except Exception as e:
            logger.error(f"提取知识点失败：{str(e)}")
            raise LLMServiceError(f"提取知识点失败：{str(e)}", error_code="EXTRACT_KNOWLEDGE_POINTS_ERROR")
    
    def speech_to_text(self, audio_url: str, language: str = "zh", timeout: int = DEFAULT_TIMEOUT) -> str:
        """
        使用语音识别模型将音频转换为文字
        
        Args:
            audio_url: 音频文件的 URL 或本地路径
            language: 音频语种，默认中文（zh）
            timeout: 超时时间（秒）
            
        Returns:
            识别出的文字
            
        Raises:
            LLMServiceValidationError: 输入校验失败
            LLMServiceError: 其他错误
        """
        if not audio_url:
            raise LLMServiceValidationError("音频 URL 不能为空")
        
        if not isinstance(audio_url, str):
            raise LLMServiceValidationError("音频 URL 必须是字符串类型")
        
        request_id = f"{int(time.time())}-{id(self)}"
        start_time = time.time()
        
        logger.info(f"[请求 {request_id}] 开始调用语音识别 API，模型：{self.ASR_MODEL_NAME}")
        logger.debug(f"[请求 {request_id}] 音频 URL：{audio_url}")
        
        messages = [
            {
                "role": Role.SYSTEM,
                "content": [
                    {"text": ""},
                ]
            },
            {
                "role": Role.USER,
                "content": [
                    {"audio": audio_url},
                ]
            }
        ]
        
        try:
            response = MultiModalConversation.call(
                api_key=self.api_key,
                model=self.ASR_MODEL_NAME,
                messages=messages,
                result_format="message",
                asr_options={
                    "language": language,
                    "enable_lid": True,
                    "enable_itn": False
                }
            )
            
            elapsed_time = time.time() - start_time
            
            if response.status_code == HTTPStatus.OK:
                text = response.output["choices"][0]["message"]["content"][0]["text"]
                logger.info(f"[请求 {request_id}] 语音识别成功，耗时：{elapsed_time:.2f}秒，文本长度：{len(text)}")
                return text
            else:
                logger.error(f"[请求 {request_id}] 语音识别失败，状态码：{response.status_code}")
                logger.error(f"[请求 {request_id}] 错误码：{response.code}，错误信息：{response.message}")
                raise LLMServiceError(
                    f"语音识别失败：{response.message}",
                    error_code=response.code,
                    status_code=response.status_code
                )
                
        except LLMServiceError:
            raise
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(f"[请求 {request_id}] 语音识别异常，耗时：{elapsed_time:.2f}秒，错误：{str(e)}")
            raise LLMServiceError(f"语音识别异常：{str(e)}", error_code="ASR_ERROR")
    
    def process_content(
        self,
        content: str,
        timeout: int = DEFAULT_TIMEOUT,
        include_summary: bool = True,
        include_tags: bool = True,
        include_knowledge_points: bool = True
    ) -> Dict[str, Any]:
        """
        综合处理内容（串行调用多个 LLM 任务）
        
        Args:
            content: 原始内容
            timeout: 单个任务的超时时间
            include_summary: 是否生成摘要
            include_tags: 是否生成标签
            include_knowledge_points: 是否提取知识点
            
        Returns:
            包含各项结果的字典
        """
        self._validate_input(content)
        
        results = {}
        
        if include_summary:
            try:
                results["summary"] = self.generate_summary(content, timeout)
            except LLMServiceError as e:
                logger.error(f"摘要生成失败：{str(e)}")
                results["summary"] = None
                results["summary_error"] = str(e)
        
        if include_tags:
            try:
                results["tags"] = self.generate_tags(content, timeout)
            except LLMServiceError as e:
                logger.error(f"标签生成失败：{str(e)}")
                results["tags"] = None
                results["tags_error"] = str(e)
        
        if include_knowledge_points:
            try:
                results["knowledge_points"] = self.extract_knowledge_points(content, timeout)
            except LLMServiceError as e:
                logger.error(f"知识点提取失败：{str(e)}")
                results["knowledge_points"] = None
                results["knowledge_points_error"] = str(e)
        
        return results


llm_service = LLMService()
