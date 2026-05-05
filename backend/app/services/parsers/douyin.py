import aiohttp
from datetime import datetime
from urllib.parse import quote
from app.models.schemas import ContentResponse
from app.services.llm_service import llm_service
from app.services.parsers.base import BaseParser, logger


class DouyinParser(BaseParser):
    async def parse(self, url: str) -> ContentResponse:
        endpoint = "/api/v1/douyin/web/fetch_one_video_by_share_url"
        params = f"share_url={quote(url, safe='')}"

        logger.debug(f"调用抖音 API: {endpoint}")

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
                    logger.error(f"抖音 API 返回错误 [错误码：{error_code}]: {error_msg}")
                    raise ValueError(f"解析抖音链接失败 [错误码：{error_code}]: {error_msg}")

                aweme_detail = data["data"]["aweme_detail"]
                title = aweme_detail.get("caption") or "抖音图文"
                author = aweme_detail.get("author", {}).get("nickname", "")
                create_time = datetime.fromtimestamp(aweme_detail.get("create_time", 0))

                video_url_list = aweme_detail.get("music", {}).get("play_url", {}).get("url_list", [])
                content = ""
                for video_url in video_url_list:
                    content = llm_service.speech_to_text(video_url)
                    if content:
                        break
                if not content:
                    content = aweme_detail.get("desc", "")
                if not content:
                    content = title

                return self._build_response(
                    url=url, source="抖音",
                    title=title, content=content,
                    author=author, create_time=create_time
                )
