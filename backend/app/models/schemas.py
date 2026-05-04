from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

# 链接输入模型
class LinkInput(BaseModel):
    url: str = Field(..., description="平台链接")

# 内容响应模型
class ContentResponse(BaseModel):
    title: str = Field(..., description="标题")
    content: str = Field(..., description="内容")
    author: str = Field(..., description="作者")
    update: str = Field(..., description="文章更新时间")
    create_time: str = Field(..., description="笔记创建时间")
    url: str = Field(..., description="原文链接")
    source: str = Field(..., description="来源平台")
    tags: List[str] = Field(default_factory=list, description="标签")
    knowledge_points: List[str] = Field(default_factory=list, description="知识点")
    short_summary: str = Field(default="", description="短摘要（~200字，卡片展示）")
    long_summary: str = Field(default="", description="长摘要（~500-800字，详情展示）")

# 搜索查询模型
class SearchQuery(BaseModel):
    text: str = Field(..., description="搜索文本")
    domains: Optional[List[str]] = Field(default=None, description="领域筛选")
    sources: Optional[List[str]] = Field(default=None, description="来源筛选")
    difficulty: Optional[str] = Field(default=None, description="难度筛选")
    content_type: Optional[str] = Field(default=None, description="内容类型筛选")
    start_date: Optional[date] = Field(default=None, description="开始日期")
    end_date: Optional[date] = Field(default=None, description="结束日期")
    learning_status: Optional[str] = Field(default=None, description="学习状态筛选")
    use_semantic: Optional[bool] = Field(default=True, description="是否使用语义检索")
    page: Optional[int] = Field(default=1, ge=1, description="页码")
    page_size: Optional[int] = Field(default=20, ge=1, le=100, description="每页数量")

# 搜索结果模型
class SearchResult(BaseModel):
    content_id: str = Field(..., description="内容ID")
    title: str = Field(..., description="标题")
    short_summary: str = Field(default="", description="短摘要")
    long_summary: str = Field(default="", description="长摘要")
    author: str = Field(..., description="作者")
    source: str = Field(..., description="来源平台")
    url: str = Field(..., description="原文链接")
    update: str = Field(..., description="更新时间")
    create_time: str = Field(..., description="创建时间")
    tags: List[str] = Field(default_factory=list, description="标签")
    knowledge_points: List[str] = Field(default_factory=list, description="知识点")
    learning_status: str = Field(default="未读", description="学习状态")
    relevance_score: float = Field(..., description="相关度分数")

# 分页搜索响应模型
class PaginatedSearchResult(BaseModel):
    items: List[SearchResult] = Field(default_factory=list, description="搜索结果列表")
    total: int = Field(..., description="总条数")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页数量")
    total_pages: int = Field(..., description="总页数")

# 学习状态更新模型
class LearningStatusUpdate(BaseModel):
    content_id: str = Field(..., description="内容ID")
    status: str = Field(..., description="学习状态")

# 标签更新模型
class TagUpdate(BaseModel):
    content_id: str = Field(..., description="内容ID")
    tags: List[str] = Field(..., description="标签列表")

# 笔记更新模型
class NoteUpdate(BaseModel):
    content_id: str = Field(..., description="内容ID")
    note: str = Field(..., description="笔记内容")