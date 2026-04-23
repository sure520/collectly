from fastapi import APIRouter, HTTPException, Depends
from app.services.platform_parser import PlatformParser
from app.services.content_manager import ContentManager
from app.services.search_engine import SearchEngine
from app.services.learning_manager import LearningManager
from app.models.schemas import (
    LinkInput, ContentResponse, SearchQuery, SearchResult,
    LearningStatusUpdate, TagUpdate, NoteUpdate
)
from typing import List

router = APIRouter()

# 初始化服务
platform_parser = PlatformParser()
content_manager = ContentManager()
search_engine = SearchEngine()
learning_manager = LearningManager()

# 链接解析端点
@router.post("/parse-link", response_model=ContentResponse)
async def parse_link(link_input: LinkInput):
    """解析平台链接，提取内容"""
    try:
        result = await platform_parser.parse(link_input.url)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 批量解析端点
@router.post("/parse-links", response_model=List[ContentResponse])
async def parse_links(links: List[LinkInput]):
    """批量解析平台链接"""
    results = []
    for link in links:
        try:
            result = await platform_parser.parse(link.url)
            results.append(result)
        except Exception as e:
            results.append({
                "title": "解析失败",
                "content": str(e),
                "author": "",
                "update": "",
                "create_time": "",
                "url": link.url,
                "source": "",
                "tags": [],
                "knowledge_points": [],
                "summary": ""
            })
    return results

# 内容存储端点
@router.post("/save-content", response_model=dict)
async def save_content(content: ContentResponse):
    """保存解析后的内容"""
    try:
        content_id = await content_manager.save(content)
        return {"content_id": content_id, "message": "保存成功"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 内容检索端点
@router.post("/search", response_model=List[SearchResult])
async def search(query: SearchQuery):
    """智能检索内容"""
    try:
        results = await search_engine.search(
            query.text,
            domains=query.domains,
            sources=query.sources,
            difficulty=query.difficulty,
            content_type=query.content_type,
            start_date=query.start_date,
            end_date=query.end_date,
            learning_status=query.learning_status
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 学习状态更新端点
@router.put("/update-learning-status", response_model=dict)
async def update_learning_status(update: LearningStatusUpdate):
    """更新学习状态"""
    try:
        await learning_manager.update_status(update.content_id, update.status)
        return {"message": "更新成功"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 标签更新端点
@router.put("/update-tags", response_model=dict)
async def update_tags(update: TagUpdate):
    """更新标签"""
    try:
        await learning_manager.update_tags(update.content_id, update.tags)
        return {"message": "更新成功"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 笔记更新端点
@router.put("/update-note", response_model=dict)
async def update_note(update: NoteUpdate):
    """更新笔记"""
    try:
        await learning_manager.update_note(update.content_id, update.note)
        return {"message": "更新成功"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 获取内容详情端点
@router.get("/content/{content_id}", response_model=ContentResponse)
async def get_content(content_id: str):
    """获取内容详情"""
    try:
        content = await content_manager.get(content_id)
        return content
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# 获取学习统计端点
@router.get("/learning-stats", response_model=dict)
async def get_learning_stats():
    """获取学习统计数据"""
    try:
        stats = await learning_manager.get_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))