import aiohttp
from datetime import datetime
from typing import Optional
from app.models.schemas import ContentResponse
from app.services.parsers.base import BaseParser, logger


class XiaohongshuParser(BaseParser):
    def _extract_from_app_api(self, data: dict, url: str) -> Optional[ContentResponse]:
        if data.get("code") != 200:
            return None
        try:
            note = data["data"]["data"][0]
            note_detail = note["note_list"][0]
            title = note_detail.get("title", "小红书笔记")
            content = note_detail.get("desc", "")
            author = note.get("user", {}).get("nickname", "")
            create_time = datetime.fromtimestamp(note_detail.get("time", datetime.now().timestamp()))

            return self._build_response(
                url=url, source="小红书",
                title=title, content=content,
                author=author, create_time=create_time
            )
        except (KeyError, IndexError):
            return None

    def _extract_from_web_v2_api(self, data: dict, url: str) -> Optional[ContentResponse]:
        if data.get("code") != 200:
            return None
        try:
            note_detail = data["data"]["note_list"][0]
            user = data["data"].get("user", {})
            title = note_detail.get("title", "小红书笔记")
            content = note_detail.get("desc", "")
            author = user.get("nickname", "")
            create_time = datetime.fromtimestamp(note_detail.get("time", datetime.now().timestamp()))

            return self._build_response(
                url=url, source="小红书",
                title=title, content=content,
                author=author, create_time=create_time
            )
        except (KeyError, IndexError):
            return None

    def _extract_from_web_v3_api(self, data: dict, url: str) -> Optional[ContentResponse]:
        if data.get("code") != 200:
            return None
        try:
            note_card = data["data"]["data"]["items"][0]["noteCard"]
            user = note_card.get("user", {})
            title = note_card.get("title", "小红书笔记")
            content = note_card.get("desc", "")
            author = user.get("nickname", "")
            timestamp = note_card.get("time", 0) / 1000
            create_time = datetime.fromtimestamp(timestamp) if timestamp else datetime.now()

            return self._build_response(
                url=url, source="小红书",
                title=title, content=content,
                author=author, create_time=create_time
            )
        except (KeyError, IndexError):
            return None

    async def parse(self, url: str) -> ContentResponse:
        endpoints = [
            ("/api/v1/xiaohongshu/app_v2/get_image_note_detail", self._extract_from_app_api),
            ("/api/v1/xiaohongshu/app/get_note_info", self._extract_from_app_api),
            ("/api/v1/xiaohongshu/app/get_note_info_v2", self._extract_from_app_api),
            ("/api/v1/xiaohongshu/web_v3/fetch_note_detail", self._extract_from_web_v3_api),
            ("/api/v1/xiaohongshu/web_v2/fetch_feed_notes_v2", self._extract_from_web_v2_api),
        ]
        note_id = url.split('?')[0].strip('/').split('/')[-1]
        params = f"note_id={note_id}"

        last_error = None
        for endpoint, extractor in endpoints:
            logger.debug(f"调用小红书 API: {endpoint}")
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"{self.api_url}{endpoint}?{params}",
                        headers=self.headers,
                        timeout=aiohttp.ClientTimeout(total=30)
                    ) as response:
                        data = await response.json()
                        result = extractor(data, url)
                        if result is not None:
                            return result
                        last_error = data
            except Exception as e:
                logger.warning(f"API {endpoint} 请求失败: {e}")
                last_error = {"message": str(e)}
                continue

        error_msg = last_error.get('message', '未知错误') if last_error else '所有 API 均失败'
        error_code = last_error.get('code', 'N/A') if last_error else 'N/A'
        logger.error(f"小红书 API 返回错误 [错误码：{error_code}]: {error_msg}")
        raise ValueError(f"解析小红书链接失败 [错误码：{error_code}]: {error_msg}")
