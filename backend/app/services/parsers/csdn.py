import aiohttp
from datetime import datetime
from app.models.schemas import ContentResponse
from app.services.parsers.base import BaseParser, logger


class CsdnParser(BaseParser):
    async def parse(self, url: str) -> ContentResponse:
        endpoint = "/api/v1/csdn/web/fetch_article_by_url"
        params = f"url={url}"

        logger.debug(f"调用CSDN API: {endpoint}")

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
                    logger.error(f"CSDN API 返回错误 [错误码：{error_code}]: {error_msg}")
                    raise ValueError(f"解析 CSDN 链接失败 [错误码：{error_code}]: {error_msg}")

                article_detail = data["data"]["article_detail"]
                title = article_detail.get("title", "CSDN 文章")
                content = article_detail.get("content", "")
                author = article_detail.get("author", "")
                create_time = datetime.fromtimestamp(article_detail.get("create_time", 0))

                return self._build_response(
                    url=url, source="CSDN",
                    title=title, content=content,
                    author=author, create_time=create_time
                )
