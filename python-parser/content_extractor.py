import httpx
from bs4 import BeautifulSoup
from typing import Dict, Optional
import re
import json


class ContentExtractor:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        }
    
    async def extract(self, url: str, timeout: int = 30) -> Dict:
        domain = self._get_domain(url)
        
        async with httpx.AsyncClient(headers=self.headers, follow_redirects=True, timeout=timeout) as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
                
                # 尝试自动检测编码
                html_content = self._decode_response(response)
                
                # 针对不同域名使用不同策略
                if 'douyin.com' in domain:
                    return self._extract_douyin(html_content, url)
                elif 'zhihu.com' in domain:
                    return self._extract_zhihu(html_content, url)
                elif 'weixin.qq.com' in domain or 'mp.weixin.qq.com' in domain:
                    return self._extract_weixin(html_content, url)
                else:
                    return self._extract_generic(html_content, url)
                    
            except Exception as e:
                error_msg = str(e)
                if "Name or service not known" in error_msg:
                    return {
                        'title': None,
                        'content': None,
                        'author': None,
                        'publish_date': None,
                        'source': 'error',
                        'error': f"域名解析失败: 无法找到该网站"
                    }
                return {
                    'title': None,
                    'content': None,
                    'author': None,
                    'publish_date': None,
                    'source': 'error',
                    'error': f"抓取失败: {error_msg}"
                }
    
    def _decode_response(self, response) -> str:
        content = response.content
        
        # 尝试从响应头获取编码
        encoding = response.encoding
        if encoding and encoding.lower() != 'utf-8':
            try:
                return content.decode(encoding, errors='replace')
            except:
                pass
        
        # 尝试UTF-8
        try:
            return content.decode('utf-8')
        except:
            pass
        
        # 尝试GBK/GB2312
        try:
            return content.decode('gbk', errors='replace')
        except:
            pass
        
        # 最后尝试latin-1
        return content.decode('latin-1', errors='replace')
    
    def _get_domain(self, url: str) -> str:
        match = re.search(r'https?://([^/]+)', url)
        return match.group(1) if match else ''
    
    def _extract_douyin(self, html: str, url: str) -> Dict:
        soup = BeautifulSoup(html, 'html.parser')
        
        title = None
        content = None
        author = None
        
        # 尝试从SSR数据中提取
        scripts = soup.find_all('script')
        for script in scripts:
            text = script.string if script.string else ''
            
            # 查找RENDER_DATA
            if 'RENDER_DATA' in text:
                try:
                    match = re.search(r'<script[^>]*>window\._SSR_HYDRATED_DATA\s*=\s*({.*?})</script>', html, re.DOTALL)
                    if match:
                        data = json.loads(match.group(1))
                        if 'app' in data and 'videoDetail' in data['app']:
                            video = data['app']['videoDetail']
                            title = video.get('desc', '')
                            author = video.get('author', {}).get('nickname', '')
                            content = title
                except:
                    pass
            
            # 查找INITIAL_STATE
            if 'INITIAL_STATE' in text or 'SSR_HYDRATED_DATA' in text:
                try:
                    json_match = re.search(r'window\._SSR_HYDRATED_DATA\s*=\s*({.*?})<', text, re.DOTALL)
                    if json_match:
                        data = json.loads(json_match.group(1))
                        if 'app' in data and 'videoDetail' in data['app']:
                            video = data['app']['videoDetail']
                            title = video.get('desc', '')
                            author_info = video.get('author', {})
                            author = author_info.get('nickname', '')
                            content = title
                except:
                    pass
        
        # 从meta标签提取
        if not title:
            meta_title = soup.find('meta', property='og:title')
            if meta_title:
                title = meta_title.get('content', '')
        
        if not content:
            meta_desc = soup.find('meta', property='og:description')
            if meta_desc:
                content = meta_desc.get('content', '')
        
        # 从页面标题提取
        if not title:
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.get_text(strip=True)
                title = title.replace(' - 抖音', '').replace(' - Douyin', '')
        
        return {
            'title': title or '抖音视频',
            'content': content or title or '抖音视频内容（需登录查看完整内容）',
            'author': author,
            'publish_date': None,
            'source': 'douyin'
        }
    
    def _extract_zhihu(self, html: str, url: str) -> Dict:
        soup = BeautifulSoup(html, 'html.parser')
        
        title = None
        content = None
        author = None
        
        # 提取标题
        title_tag = soup.find('h1', class_='Post-Title') or soup.find('h1', class_='QuestionHeader-title')
        if title_tag:
            title = title_tag.get_text(strip=True)
        
        # 提取内容
        content_div = soup.find('div', class_='Post-RichTextContainer') or soup.find('div', class_='RichContent-inner')
        if content_div:
            content = content_div.get_text(separator='\n', strip=True)
        
        # 提取作者
        author_elem = soup.find('a', class_='UserLink-link') or soup.find('span', class_='AuthorInfo-name')
        if author_elem:
            author = author_elem.get_text(strip=True)
        
        return {
            'title': title,
            'content': content or '知乎内容（需登录查看完整内容）',
            'author': author,
            'publish_date': None,
            'source': 'zhihu'
        }
    
    def _extract_weixin(self, html: str, url: str) -> Dict:
        soup = BeautifulSoup(html, 'html.parser')
        
        title = None
        content = None
        author = None
        
        # 提取标题
        title_tag = soup.find('h2', class_='rich_media_title') or soup.find('h1', id='activity-name')
        if title_tag:
            title = title_tag.get_text(strip=True)
        
        # 提取内容
        content_div = soup.find('div', id='js_content') or soup.find('div', class_='rich_media_content')
        if content_div:
            content = content_div.get_text(separator='\n', strip=True)
        
        # 提取作者
        author_elem = soup.find('a', id='js_name') or soup.find('span', class_='profile_nickname')
        if author_elem:
            author = author_elem.get_text(strip=True)
        
        return {
            'title': title,
            'content': content or '微信公众号文章',
            'author': author,
            'publish_date': None,
            'source': 'weixin'
        }
    
    def _extract_generic(self, html: str, url: str) -> Dict:
        soup = BeautifulSoup(html, 'html.parser')

        title = None
        content = None
        author = None
        publish_date = None

        # 提取标题 - 多种策略
        # 1. Open Graph
        og_title = soup.find('meta', property='og:title')
        if og_title:
            title = og_title.get('content', '')

        # 2. Twitter Card
        if not title:
            twitter_title = soup.find('meta', attrs={'name': 'twitter:title'})
            if twitter_title:
                title = twitter_title.get('content', '')

        # 3. 页面标题
        if not title:
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.get_text(strip=True)

        # 4. h1标签
        if not title:
            h1 = soup.find('h1')
            if h1:
                title = h1.get_text(strip=True)

        # 提取描述/摘要
        og_desc = soup.find('meta', property='og:description')
        if og_desc:
            content = og_desc.get('content', '')

        if not content:
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                content = meta_desc.get('content', '')

        # 提取正文内容
        if not content or len(content) < 100:
            # 尝试找到主要内容区域
            selectors = [
                'article',
                '[role="main"]',
                'main',
                '.post-content',
                '.entry-content',
                '.article-content',
                '.content',
                '#content',
                '.post',
                '.article',
                '.blog-post',
                '#mw-content-text',  # Wikipedia
                '.mw-parser-output',  # Wikipedia
            ]

            for selector in selectors:
                element = soup.select_one(selector)
                if element:
                    text = element.get_text(separator='\n', strip=True)
                    if len(text) > 200:
                        content = text
                        break

            # 如果没找到，提取所有段落
            if not content or len(content) < 100:
                paragraphs = soup.find_all('p')
                texts = []
                for p in paragraphs:
                    text = p.get_text(strip=True)
                    if len(text) > 30:
                        texts.append(text)
                if texts:
                    content = '\n\n'.join(texts)

        # 提取作者
        author_selectors = [
            'meta[name="author"]',
            '.author',
            '.byline',
            '[rel="author"]'
        ]
        for selector in author_selectors:
            elem = soup.select_one(selector)
            if elem:
                if elem.name == 'meta':
                    author = elem.get('content', '')
                else:
                    author = elem.get_text(strip=True)
                if author:
                    break

        # 提取发布日期
        date_selectors = [
            'meta[property="article:published_time"]',
            'meta[name="publishedDate"]',
            'time[datetime]',
            '.published',
            '.date'
        ]
        for selector in date_selectors:
            elem = soup.select_one(selector)
            if elem:
                if elem.name == 'meta':
                    publish_date = elem.get('content', '')
                elif elem.name == 'time':
                    publish_date = elem.get('datetime', '')
                else:
                    publish_date = elem.get_text(strip=True)
                if publish_date:
                    break

        # 确保至少有内容返回
        if not content:
            # 提取body中的所有文本
            body = soup.find('body')
            if body:
                # 先移除script和style标签
                for script in body.find_all(['script', 'style']):
                    script.decompose()
                content = body.get_text(separator='\n', strip=True)

        # 如果内容太短，尝试提取所有可见文本
        if not content or len(content) < 50:
            all_text = soup.get_text(separator='\n', strip=True)
            if len(all_text) > len(content or ''):
                content = all_text

        return {
            'title': title,
            'content': self._clean_content(content) if content else None,
            'author': author,
            'publish_date': publish_date,
            'source': 'generic'
        }
    
    def _clean_content(self, text: str) -> str:
        if not text:
            return ""

        # 检测是否为乱码（包含大量替换字符或非打印字符）
        replacement_count = text.count('\ufffd')
        non_printable = sum(1 for c in text if ord(c) < 32 and c not in '\n\r\t')

        if replacement_count > len(text) * 0.05 or non_printable > len(text) * 0.1:
            return "[内容编码异常，无法正确解析]"

        # 移除多余空白
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r'[ \t]+', ' ', text)

        # 移除特殊控制字符
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)

        # 移除广告相关文本
        ad_patterns = [
            r'广告\s*\d+',
            r' Sponsored ',
            r'Advertisement',
            r'推广',
            r'相关推荐',
            r'猜你喜欢',
            r'热门文章',
            r'阅读更多',
            r'点击查看',
            r'加载中',
            r'分享至',
            r'收藏',
            r'点赞',
        ]

        for pattern in ad_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)

        return text.strip()