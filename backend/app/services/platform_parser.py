import asyncio
import aiohttp
import re
import requests
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timedelta, timezone
import os
from urllib.parse import quote
from app.utils.config import get_settings
from app.utils.logger import get_logger
from app.models.schemas import ContentResponse
import re
from app.services.llm_service import llm_service, LLMServiceError

settings = get_settings()
logger = get_logger("platform_parser")

# 1. 从文本中提取 http 链接（处理带文案的分享内容）
def extract_url(text: str) -> str:
    text = str(text).strip()
    # 精准匹配：抖音/小红书/B站/知乎 合法链接，遇到中文、符号自动截断
    pattern = re.compile(
        r"https?://(?:www\.|v\.|b23\.tv|xhslink\.com|zhuanlan\.zhihu\.com)"
        r"[a-zA-Z0-9_\-\/.?&=]+",
        re.I
    )
    match = pattern.search(text)
    return match.group(0) if match else text

# 2. 小红书短链还原：追踪重定向，得到真实长链接
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
        # 必须用 GET，不能只用 HEAD
        with requests.Session() as s:
            resp = s.get(url, headers=headers, allow_redirects=True, timeout=10)
            return resp.url
    except Exception as e:
        print(f"[xhs还原失败] {e}")
        return url

# 2. 短链还原：追踪重定向，得到真实长链接
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

# 3. 核心：清理成永久纯净链接（你所有平台都支持）
def clean_pure_url(url: str) -> str:
    parsed = urlparse(url)
    netloc = parsed.netloc
    path = parsed.path.rstrip("/")
    query = parse_qs(parsed.query)

    # --- 抖音：特殊处理 modal_id → 标准视频链接 ---
    if "douyin.com" in netloc:
        modal_id = query.get("modal_id", [None])[0]
        if modal_id:
            return f"https://www.douyin.com/video/{modal_id}"
        return f"https://{netloc}{path}"

    # --- B站：保留 p= 分P，删除所有追踪参数 ---
    elif "bilibili.com" in netloc:
        p = query.get("p", [None])[0]
        base = f"https://www.bilibili.com{path}"
        return f"{base}?p={p}" if p else base

    # --- 知乎专栏 ---
    elif "zhuanlan.zhihu.com" in netloc:
        return f"https://zhuanlan.zhihu.com{path}"

    # --- 小红书：必须保留 xsec_token 和 xsec_source，否则无法访问 ---
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

    # --- 其他 ---
    else:
        return f"{parsed.scheme}://{netloc}{path}"

# 4. 总调度函数：一键处理所有链接
def process_url(raw_text: str) -> str:
    # 微信公众号链接直接返回
    if "mp.weixin.qq.com" in raw_text:
        return raw_text
    url = extract_url(raw_text)
    url = resolve_short_url(url)
    url = clean_pure_url(url)
    return url


class PlatformParser:
    def __init__(self):
        self.api_key = settings.TIKHUB_API_KEY
        self.api_url = settings.TIKHUB_API_URL
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        # 定义北京时间 UTC+8
        self.beijing_tz = timezone(timedelta(hours=8), name="Asia/Shanghai")
    
    async def parse(self, url: str) -> ContentResponse:
        """解析平台链接，提取内容"""
        logger.info(f"开始解析链接: {url}")
        url = process_url(url)
        platform = self._detect_platform(url)
        if not platform:
            logger.warning(f"不支持的平台链接: {url}")
            raise ValueError("不支持的平台链接")
        
        try:
            if platform == "抖音":
                result = await self._parse_douyin(url)
            elif platform == "小红书":
                result = await self._parse_xiaohongshu(url)
            elif platform == "微信公众号":
                result = await self._parse_weixin(url)
            elif platform == "B站":
                result = await self._parse_bilibili(url)
            elif platform == "知乎":
                result = await self._parse_zhihu(url)
            elif platform == "CSDN":
                result = await self._parse_csdn(url)
            else:
                raise ValueError("不支持的平台")
            
            logger.info(f"成功解析 {platform} 链接: {result.title}")
            return result
        except Exception as e:
            logger.error(f"解析 {platform} 链接失败: {str(e)}")
            raise
    
    def _detect_platform(self, url: str) -> str:
        """检测链接所属平台"""
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
    
    async def _parse_douyin(self, url: str) -> ContentResponse:
        """解析抖音链接"""
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
                if data.get("code") == 200:
                    aweme_detail = data["data"]["aweme_detail"]
                    title = aweme_detail.get("caption", "抖音视频")
                    author = aweme_detail.get("author", {}).get("nickname", "")
                    create_time = datetime.fromtimestamp(aweme_detail.get("create_time", 0))
                    
                    video_url_list = aweme_detail.get("music", {}).get("play_url", {}).get("url_list", [])
                    content = ""
                    for video_url in video_url_list:
                        content = llm_service.speech_to_text(video_url)
                        if content:
                            break
                    if not content:
                        content = title
                    
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
                        source="抖音",
                        tags=tags,
                        knowledge_points=knowledge_points,
                        summary=summary
                    )
                else:
                    error_msg = data.get('message', '未知错误')
                    error_code = data.get('code', 'N/A')
                    logger.error(f"抖音 API 返回错误 [错误码：{error_code}]: {error_msg}")
                    raise ValueError(f"解析抖音链接失败 [错误码：{error_code}]: {error_msg}")
    
    async def _parse_xiaohongshu(self, url: str) -> ContentResponse:
        """解析小红书链接"""
        endpoint = "/api/v1/xiaohongshu/app/get_note_info"
        params = f"note_id={url.split('?')[0].strip('/').split('/')[-1]}"
        
        logger.debug(f"调用小红书 API: {endpoint}")
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}{endpoint}?{params}",
                headers=self.headers,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                data = await response.json()
                if data.get("code") == 200:
                    note = data["data"]["data"][0]
                    note_detail = note["note_list"][0]
                    title = note_detail.get("title", "小红书笔记")
                    content = note_detail.get("desc", "")
                    author = note.get("user", {}).get("nickname", "")
                    create_time = datetime.fromtimestamp(note_detail.get("time", datetime.now().timestamp()))
                    
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
                        source="小红书",
                        tags=tags,
                        knowledge_points=knowledge_points,
                        summary=summary
                    )
                else:
                    error_msg = data.get('message', '未知错误')
                    error_code = data.get('code', 'N/A')
                    logger.error(f"小红书 API 返回错误 [错误码：{error_code}]: {error_msg}")
                    raise ValueError(f"解析小红书链接失败 [错误码：{error_code}]: {error_msg}")
    
    async def _parse_weixin(self, url: str) -> ContentResponse:
        """解析微信公众号链接"""
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
                if data.get("code") == 200:
                    article_detail = data["data"]
                    title = article_detail.get("title", "微信公众号文章")
                    content = article_detail.get("content", "").get("raw_content", [""])[0].get("text", "")
                    author = article_detail.get("author", "")
                    create_time = datetime.fromtimestamp(article_detail.get("create_time", datetime.now().timestamp()))
                    
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
                        source="微信公众号",
                        tags=tags,
                        knowledge_points=knowledge_points,
                        summary=summary
                    )
                else:
                    error_msg = data.get('message', '未知错误')
                    error_code = data.get('code', 'N/A')
                    logger.error(f"微信公众号 API 返回错误 [错误码：{error_code}]: {error_msg}")
                    raise ValueError(f"解析微信公众号链接失败 [错误码：{error_code}]: {error_msg}")
    
    async def _parse_bilibili(self, url: str) -> ContentResponse:
        """解析B站链接"""
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
                                source="B站",
                                tags=tags,
                                knowledge_points=knowledge_points,
                                summary=summary
                            )
            except Exception as e:
                logger.warning(f"尝试使用 {endpoint} 失败: {str(e)}")
        
        logger.warning(f"B站所有 API 端点都失败，使用备选方案")
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
            summary="B站视频内容"
        )
    
    async def _parse_zhihu(self, url: str) -> ContentResponse:
        """解析知乎链接"""
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
                if data.get("code") == 200:
                    article_detail = data["data"]
                    title = article_detail.get("title", "知乎文章")
                    content = article_detail.get("content", "")
                    author = article_detail.get("author", {}).get("name", "")
                    create_time = datetime.fromtimestamp(article_detail.get("updated", 0))
                    
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
                        source="知乎",
                        tags=tags,
                        knowledge_points=knowledge_points,
                        summary=summary
                    )
                else:
                    error_msg = data.get('message', '未知错误')
                    error_code = data.get('code', 'N/A')
                    logger.error(f"知乎 API 返回错误 [错误码：{error_code}]: {error_msg}")
                    raise ValueError(f"解析知乎链接失败 [错误码：{error_code}]: {error_msg}")
    
    async def _parse_csdn(self, url: str) -> ContentResponse:
        """解析CSDN链接"""
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
                if data.get("code") == 200:
                    article_detail = data["data"]["article_detail"]
                    title = article_detail.get("title", "CSDN 文章")
                    content = article_detail.get("content", "")
                    author = article_detail.get("author", "")
                    create_time = datetime.fromtimestamp(article_detail.get("create_time", 0))
                    
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
                        source="CSDN",
                        tags=tags,
                        knowledge_points=knowledge_points,
                        summary=summary
                    )
                else:
                    error_msg = data.get('message', '未知错误')
                    error_code = data.get('code', 'N/A')
                    logger.error(f"CSDN API 返回错误 [错误码：{error_code}]: {error_msg}")
                    raise ValueError(f"解析 CSDN 链接失败 [错误码：{error_code}]: {error_msg}")
    
    def _generate_summary(self, content: str) -> str:
        """
        使用 LLM 生成内容摘要
        
        Args:
            content: 原始内容
            
        Returns:
            生成的摘要，如果失败则返回简单截断
        """
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
            summary = content[:200] + "..." if len(content) > 200 else content
            return summary
        except Exception as e:
            logger.error(f"摘要生成异常：{str(e)}")
            summary = content[:200] + "..." if len(content) > 200 else content
            return summary
    
    def _generate_tags(self, content: str) -> list:
        """
        使用 LLM 创建关联标签
        
        Args:
            content: 原始内容
            
        Returns:
            标签列表，如果失败则返回基于规则的标签
        """
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
        """
        基于规则生成标签（备用方案）
        
        Args:
            content: 原始内容
            
        Returns:
            标签列表
        """
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
        """
        使用 LLM 提取核心知识点
        
        Args:
            content: 原始内容
            
        Returns:
            知识点列表，如果失败则返回基于规则的知识点
        """
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
        """
        基于规则提取知识点（备用方案）
        
        Args:
            content: 原始内容
            
        Returns:
            知识点列表
        """
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

