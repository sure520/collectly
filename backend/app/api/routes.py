from fastapi import APIRouter, HTTPException, Depends
from app.services.platform_parser import PlatformParser, process_url
from app.services.content_manager import ContentManager
from app.services.search_engine import SearchEngine
from app.services.learning_manager import LearningManager
from app.models.schemas import (
    LinkInput, ContentResponse, SearchQuery, SearchResult,
    PaginatedSearchResult, LearningStatusUpdate, TagUpdate, NoteUpdate
)
from typing import List
from pydantic import BaseModel

router = APIRouter()

# 初始化服务
platform_parser = PlatformParser()
content_manager = ContentManager()
search_engine = SearchEngine()
learning_manager = LearningManager()

class CleanUrlRequest(BaseModel):
    raw_texts: List[str]

class CleanUrlResponse(BaseModel):
    cleaned_url: str
    is_valid: bool

# URL 清理端点
@router.post("/clean-urls", response_model=List[CleanUrlResponse])
async def clean_urls(request: CleanUrlRequest):
    """清理应用分享的文本，提取并还原真实 URL"""
    results = []
    for raw_text in request.raw_texts:
        try:
            cleaned_url = process_url(raw_text)
            # 验证清理后的 URL 是否有效
            is_valid = bool(cleaned_url and cleaned_url.startswith(('http://', 'https://')))
            results.append(CleanUrlResponse(cleaned_url=cleaned_url, is_valid=is_valid))
        except Exception:
            results.append(CleanUrlResponse(cleaned_url=raw_text, is_valid=False))
    return results

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
@router.post("/search", response_model=PaginatedSearchResult)
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
            learning_status=query.learning_status,
            use_semantic=query.use_semantic,
            page=query.page,
            page_size=query.page_size
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

# 删除内容端点
@router.delete("/content/{content_id}", response_model=dict)
async def delete_content(content_id: str):
    """删除内容"""
    try:
        success = await content_manager.delete(content_id)
        if success:
            return {"message": "删除成功"}
        else:
            raise HTTPException(status_code=404, detail="内容不存在")
    except HTTPException:
        raise
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

# 获取向量库统计端点
@router.get("/vector-stats", response_model=dict)
async def get_vector_stats():
    """获取向量库统计信息"""
    try:
        stats = await content_manager.get_vector_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 重新嵌入内容向量端点
@router.post("/re-embed/{content_id}", response_model=dict)
async def re_embed_content(content_id: str):
    """重新生成指定内容的向量"""
    try:
        content = await content_manager.get(content_id)
        embedding_text = content_manager._build_embedding_text(content)
        metadata = {
            "source": content.source,
            "title": content.title,
            "tags": str(content.tags),
            "knowledge_points": str(content.knowledge_points)
        }
        success = content_manager.vector_service.add_embedding(
            content_id=content_id,
            text=embedding_text,
            metadata=metadata
        )
        if success:
            return {"message": "向量更新成功"}
        else:
            raise HTTPException(status_code=500, detail="向量更新失败")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# 全量重建向量索引端点
@router.post("/rebuild-vectors", response_model=dict)
async def rebuild_all_vectors():
    """全量重建向量索引"""
    try:
        content_manager.vector_service.reset_collection()
        
        all_content = await content_manager.get_all()
        success_count = 0
        for content in all_content:
            from app.models.schemas import ContentResponse
            content_obj = ContentResponse(
                title=content["title"],
                content=content["content"],
                author=content["author"],
                update=content["update"],
                create_time=content["create_time"],
                url=content["url"],
                source=content["source"],
                tags=content["tags"],
                knowledge_points=content["knowledge_points"],
                summary=content["summary"]
            )
            embedding_text = content_manager._build_embedding_text(content_obj)
            metadata = {
                "source": content["source"],
                "title": content["title"],
                "tags": str(content["tags"]),
                "knowledge_points": str(content["knowledge_points"])
            }
            if content_manager.vector_service.add_embedding(
                content_id=content["id"],
                text=embedding_text,
                metadata=metadata
            ):
                success_count += 1
        
        return {"message": f"向量索引重建完成", "success_count": success_count, "total": len(all_content)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))