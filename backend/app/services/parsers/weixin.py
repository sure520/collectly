import aiohttp
from datetime import datetime
from app.models.schemas import ContentResponse
from app.services.parsers.base import BaseParser, logger


class WeixinParser(BaseParser):
    async def parse(self, url: str) -> ContentResponse:
        endpoint = "/api/v1/wechat_mp/web/fetch_mp_article_detail_json"
        params = f"url={url}"

        logger.debug(f"调用微信公众号 API: {endpoint}")

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
                    logger.error(f"微信公众号 API 返回错误 [错误码：{error_code}]: {error_msg}")
                    raise ValueError(f"解析微信公众号链接失败 [错误码：{error_code}]: {error_msg}")

                article_detail = data["data"]
                title = article_detail.get("title", "微信公众号文章")
                content = article_detail.get("content", {}).get("raw_content", [""])[0].get("text", "")
                author = article_detail.get("author", "")
                create_time = datetime.fromtimestamp(article_detail.get("create_time", datetime.now().timestamp()))

                return self._build_response(
                    url=url, source="微信公众号",
                    title=title, content=content,
                    author=author, create_time=create_time
                )
