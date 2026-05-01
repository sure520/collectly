import re
import requests
from urllib.parse import urlparse, parse_qs
from app.utils.config import get_settings
from app.utils.logger import get_logger
from app.models.schemas import ContentResponse
from app.services.parsers import (
    DouyinParser,
    XiaohongshuParser,
    WeixinParser,
    BilibiliParser,
    ZhihuParser,
    CsdnParser,
)

settings = get_settings()
logger = get_logger("platform_parser")


def extract_url(text: str) -> str:
    text = str(text).strip()
    pattern = re.compile(
        r"https?://(?:www\.|v\.|b23\.tv|xhslink\.com|zhuanlan\.zhihu\.com)"
        r"[a-zA-Z0-9_\-\/.?&=]+",
        re.I
    )
    match = pattern.search(text)
    return match.group(0) if match else text


def resolve_xhs_short(url: str) -> str:
    if "xhslink.com" not in url:
        return url

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Referer": "https://www.xiaohongshu.com/",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "sec-ch-ua": '"Chromium";v="130", "Not=A?Brand";v="99", "Google Chrome";v="130"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1"
    }

    try:
        with requests.Session() as s:
            resp = s.get(url, headers=headers, allow_redirects=True, timeout=10)
            return resp.url
    except Exception as e:
        print(f"[xhs还原失败] {e}")
        return url


def resolve_short_url(url: str) -> str:
    if "xhslink.com" in url:
        return resolve_xhs_short(url)

    short_domains = ["b23.tv", "v.douyin.com"]
    if not any(d in url for d in short_domains):
        return url

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/130.0.0.0 Safari/537.36"
    }
    try:
        with requests.Session() as s:
            resp = s.head(url, headers=headers, allow_redirects=True, timeout=10)
            return resp.url
    except Exception:
        return url


def clean_pure_url(url: str) -> str:
    parsed = urlparse(url)
    netloc = parsed.netloc
    path = parsed.path.rstrip("/")
    query = parse_qs(parsed.query)

    if "douyin.com" in netloc:
        modal_id = query.get("modal_id", [None])[0]
        if modal_id:
            return f"https://www.douyin.com/video/{modal_id}"
        return f"https://{netloc}{path}"

    elif "bilibili.com" in netloc:
        p = query.get("p", [None])[0]
        base = f"https://www.bilibili.com{path}"
        return f"{base}?p={p}" if p else base

    elif "zhuanlan.zhihu.com" in netloc:
        return f"https://zhuanlan.zhihu.com{path}"

    elif "xiaohongshu.com" in netloc:
        xsec_token = query.get("xsec_token", [None])[0]
        xsec_source = query.get("xsec_source", [None])[0]

        params = []
        if xsec_token:
            params.append(f"xsec_token={xsec_token}")
        if xsec_source:
            params.append(f"xsec_source={xsec_source}")

        base = f"https://www.xiaohongshu.com{path}"
        return f"{base}?{'&'.join(params)}" if params else base

    else:
        return f"{parsed.scheme}://{netloc}{path}"


def process_url(raw_text: str) -> str:
    if "mp.weixin.qq.com" in raw_text:
        return raw_text
    url = extract_url(raw_text)
    url = resolve_short_url(url)
    url = clean_pure_url(url)
    return url


class PlatformParser:
    def __init__(self):
        self._parsers = {
            "抖音": DouyinParser(),
            "小红书": XiaohongshuParser(),
            "微信公众号": WeixinParser(),
            "B站": BilibiliParser(),
            "知乎": ZhihuParser(),
            "CSDN": CsdnParser(),
        }

    def _detect_platform(self, url: str) -> str:
        if "douyin.com" in url:
            return "抖音"
        elif "xiaohongshu.com" in url:
            return "小红书"
        elif "mp.weixin.qq.com" in url:
            return "微信公众号"
        elif "bilibili.com" in url:
            return "B站"
        elif "zhihu.com" in url:
            return "知乎"
        elif "csdn.net" in url:
            return "CSDN"
        else:
            return ""

    async def parse(self, url: str) -> ContentResponse:
        logger.info(f"开始解析链接: {url}")
        url = process_url(url)
        platform = self._detect_platform(url)
        if not platform:
            logger.warning(f"不支持的平台链接: {url}")
            raise ValueError("不支持的平台链接")

        parser = self._parsers.get(platform)
        if not parser:
            raise ValueError("不支持的平台")

        try:
            result = await parser.parse(url)
            logger.info(f"成功解析 {platform} 链接: {result.title}")
            return result
        except Exception as e:
            logger.error(f"解析 {platform} 链接失败: {str(e)}")
            raise
