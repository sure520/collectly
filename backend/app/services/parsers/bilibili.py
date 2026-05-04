import aiohttp
from datetime import datetime
from app.models.schemas import ContentResponse
from app.services.parsers.base import BaseParser, logger


class BilibiliParser(BaseParser):
    async def parse(self, url: str) -> ContentResponse:
        endpoints = [
            "/api/v1/bilibili/web/fetch_one_video_v3",
            "/api/v1/bilibili/web/fetch_one_video"
        ]

        for endpoint in endpoints:
            params = f"url={url}"

            logger.debug(f"调用B站 API: {endpoint}")

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"{self.api_url}{endpoint}?{params}",
                        headers=self.headers,
                        timeout=aiohttp.ClientTimeout(total=30)
                    ) as response:
                        data = await response.json()
                        if data.get("code") == 200:
                            video_detail = data["data"]
                            title = video_detail.get("title", "B 站视频")
                            content = title
                            author = video_detail.get("owner", {}).get("name", "")
                            create_time = datetime.fromtimestamp(video_detail.get("pubdate", 0))

                            return self._build_response(
                                url=url, source="B站",
                                title=title, content=content,
                                author=author, create_time=create_time
                            )
            except Exception as e:
                logger.warning(f"尝试使用 {endpoint} 失败: {str(e)}")

        logger.warning("B站所有 API 端点都失败，使用备选方案")
        return ContentResponse(
            title="B站视频",
            content="B站视频内容（需登录查看完整内容）",
            author="",
            update=datetime.now(self.beijing_tz).strftime("%Y-%m-%d"),
            create_time=datetime.now(self.beijing_tz).strftime("%Y-%m-%d"),
            url=url,
            source="B站",
            tags=[],
            knowledge_points=[],
            short_summary="B站视频内容",
            long_summary="B站视频内容",
        )
