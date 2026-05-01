import aiohttp
from datetime import datetime
from app.models.schemas import ContentResponse
from app.services.parsers.base import BaseParser, logger


class ZhihuParser(BaseParser):
    async def parse(self, url: str) -> ContentResponse:
        article_id = url.split("/")[-1]
        endpoint = "/api/v1/zhihu/web/fetch_column_article_detail"
        params = f"article_id={article_id}"

        logger.debug(f"调用知乎 API: {endpoint}")

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}{endpoint}?{params}",
                headers=self.headers,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                data = await response.json()
                if data.get("code") != 200:
                    error_msg = data.get('message', '未知错误')
                    error_code = data.get('code', 'N/A')
                    logger.error(f"知乎 API 返回错误 [错误码：{error_code}]: {error_msg}")
                    raise ValueError(f"解析知乎链接失败 [错误码：{error_code}]: {error_msg}")

                article_detail = data["data"]
                title = article_detail.get("title", "知乎文章")
                content = article_detail.get("content", "")
                author = article_detail.get("author", {}).get("name", "")
                create_time = datetime.fromtimestamp(article_detail.get("updated", 0))

                return self._build_response(
                    url=url, source="知乎",
                    title=title, content=content,
                    author=author, create_time=create_time
                )
