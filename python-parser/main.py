from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import Optional
import httpx
import asyncio
from datetime import datetime
import logging

from content_extractor import ContentExtractor
from summarizer import Summarizer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="链接内容解析服务",
    description="智能抓取网页内容并提取正文、生成摘要",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

extractor = ContentExtractor()
summarizer = Summarizer()


class ParseRequest(BaseModel):
    url: str
    include_summary: bool = True
    timeout: int = 30


class ParseResponse(BaseModel):
    success: bool
    url: str
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    author: Optional[str] = None
    publish_date: Optional[str] = None
    word_count: int = 0
    processing_time: float = 0.0
    error: Optional[str] = None


@app.post("/parse", response_model=ParseResponse)
async def parse_url(request: ParseRequest):
    start_time = datetime.now()
    
    try:
        logger.info(f"开始解析URL: {request.url}")
        
        # 验证URL格式
        if not request.url.startswith(('http://', 'https://')):
            return ParseResponse(
                success=False,
                url=request.url,
                error="无效的URL格式，必须以http://或https://开头",
                processing_time=(datetime.now() - start_time).total_seconds()
            )
        
        # 提取内容
        content_data = await extractor.extract(request.url, timeout=request.timeout)

        # 检查是否有错误
        if content_data.get('error'):
            return ParseResponse(
                success=False,
                url=request.url,
                error=content_data['error'],
                processing_time=(datetime.now() - start_time).total_seconds()
            )

        if not content_data.get('content'):
            return ParseResponse(
                success=False,
                url=request.url,
                error="无法提取有效内容，可能是动态加载页面或需要登录",
                processing_time=(datetime.now() - start_time).total_seconds()
            )
        
        # 生成摘要
        summary = None
        if request.include_summary and content_data.get('content'):
            try:
                summary = await summarizer.summarize(content_data['content'])
            except Exception as e:
                logger.warning(f"摘要生成失败: {e}")
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return ParseResponse(
            success=True,
            url=request.url,
            title=content_data.get('title'),
            content=content_data.get('content'),
            summary=summary,
            author=content_data.get('author'),
            publish_date=content_data.get('publish_date'),
            word_count=len(content_data.get('content', '')),
            processing_time=processing_time
        )
        
    except httpx.TimeoutException:
        return ParseResponse(
            success=False,
            url=request.url,
            error=f"请求超时，超过{request.timeout}秒未响应",
            processing_time=(datetime.now() - start_time).total_seconds()
        )
    except httpx.HTTPStatusError as e:
        return ParseResponse(
            success=False,
            url=request.url,
            error=f"HTTP错误: {e.response.status_code}",
            processing_time=(datetime.now() - start_time).total_seconds()
        )
    except Exception as e:
        error_msg = str(e)
        logger.error(f"解析失败: {error_msg}")
        if "Invalid URL" in error_msg or "invalid url" in error_msg.lower():
            return ParseResponse(
                success=False,
                url=request.url,
                error="无效的URL格式，请检查链接是否正确",
                processing_time=(datetime.now() - start_time).total_seconds()
            )
        return ParseResponse(
            success=False,
            url=request.url,
            error=f"解析失败: {error_msg}",
            processing_time=(datetime.now() - start_time).total_seconds()
        )


@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/")
async def root():
    return {
        "service": "链接内容解析服务",
        "version": "1.0.0",
        "endpoints": {
            "parse": "POST /parse - 解析URL内容",
            "health": "GET /health - 健康检查"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)