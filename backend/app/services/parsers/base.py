from abc import ABC, abstractmethod
from datetime import datetime, timezone, timedelta
from app.utils.config import get_settings
from app.utils.logger import get_logger
from app.models.schemas import ContentResponse
from app.services.llm_service import llm_service, LLMServiceError

settings = get_settings()
logger = get_logger("parser")


class BaseParser(ABC):
    def __init__(self):
        self.api_key = settings.TIKHUB_API_KEY
        self.api_url = settings.TIKHUB_API_URL
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        self.beijing_tz = timezone(timedelta(hours=8), name="Asia/Shanghai")

    @abstractmethod
    async def parse(self, url: str) -> ContentResponse:
        ...

    def _build_response(self, url: str, source: str, title: str, content: str,
                        author: str, create_time: datetime) -> ContentResponse:
        summary = self._generate_summary(content)
        tags = self._generate_tags(content)
        knowledge_points = self._extract_knowledge_points(content)

        return ContentResponse(
            title=title,
            content=content,
            author=author,
            update=create_time.strftime("%Y-%m-%d"),
            create_time=datetime.now(self.beijing_tz).strftime("%Y-%m-%d"),
            url=url,
            source=source,
            tags=tags,
            knowledge_points=knowledge_points,
            summary=summary
        )

    def _generate_summary(self, content: str) -> str:
        if not content:
            return ""
        try:
            logger.info("开始使用 LLM 生成摘要")
            content_truncated = content[:8000] if len(content) > 8000 else content
            summary = llm_service.generate_summary(content_truncated)
            logger.info(f"LLM 摘要生成成功，长度：{len(summary)}")
            return summary
        except LLMServiceError as e:
            logger.warning(f"LLM 摘要生成失败，使用备用方案：{str(e)}")
            return content[:200] + "..." if len(content) > 200 else content
        except Exception as e:
            logger.error(f"摘要生成异常：{str(e)}")
            return content[:200] + "..." if len(content) > 200 else content

    def _generate_tags(self, content: str) -> list:
        if not content:
            return []
        try:
            logger.info("开始使用 LLM 生成标签")
            content_truncated = content[:8000] if len(content) > 8000 else content
            tags = llm_service.generate_tags(content_truncated)
            logger.info(f"LLM 标签生成成功，数量：{len(tags)}")
            return tags
        except LLMServiceError as e:
            logger.warning(f"LLM 标签生成失败，使用备用方案：{str(e)}")
            return self._generate_tags_by_rules(content)
        except Exception as e:
            logger.error(f"标签生成异常：{str(e)}")
            return self._generate_tags_by_rules(content)

    def _generate_tags_by_rules(self, content: str) -> list:
        tags = []
        domain_tags = ["大模型", "Agent", "RAG", "多模态"]
        for tag in domain_tags:
            if tag in content:
                tags.append(tag)
        type_tags = ["教程", "综述", "实践", "论文", "面试", "解读"]
        for tag in type_tags:
            if tag in content:
                tags.append(tag)
        difficulty_tags = ["入门", "进阶", "高阶", "论文级"]
        for tag in difficulty_tags:
            if tag in content:
                tags.append(tag)
        return list(set(tags))

    def _extract_knowledge_points(self, content: str) -> list:
        if not content:
            return []
        try:
            logger.info("开始使用 LLM 提取知识点")
            content_truncated = content[:8000] if len(content) > 8000 else content
            knowledge_points = llm_service.extract_knowledge_points(content_truncated)
            logger.info(f"LLM 知识点提取成功，数量：{len(knowledge_points)}")
            return knowledge_points
        except LLMServiceError as e:
            logger.warning(f"LLM 知识点提取失败，使用备用方案：{str(e)}")
            return self._extract_knowledge_points_by_rules(content)
        except Exception as e:
            logger.error(f"知识点提取异常：{str(e)}")
            return self._extract_knowledge_points_by_rules(content)

    def _extract_knowledge_points_by_rules(self, content: str) -> list:
        knowledge_points = []
        common_knowledge = [
            "RAG", "向量库", "嵌入模型", "大语言模型", "Agent",
            "多模态", "检索增强", "微调", "Prompt Engineering",
            "记忆机制", "工具使用", "自主规划"
        ]
        for point in common_knowledge:
            if point in content:
                knowledge_points.append(point)
        return list(set(knowledge_points))
