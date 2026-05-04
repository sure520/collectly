import sqlite3
import json
from pathlib import Path
from typing import List, Optional
from datetime import date
from app.models.schemas import SearchResult, PaginatedSearchResult
from app.services.vector_service import VectorService

# 项目根目录
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent

class SearchEngine:
    def __init__(self):
        self.db_path = str(PROJECT_ROOT / "knowledge.db")
        self.vector_service = VectorService()
    
    async def search(
        self,
        text: str,
        domains: Optional[List[str]] = None,
        sources: Optional[List[str]] = None,
        difficulty: Optional[str] = None,
        content_type: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        learning_status: Optional[str] = None,
        use_semantic: bool = True,
        page: int = 1,
        page_size: int = 20
    ) -> PaginatedSearchResult:
        if text and use_semantic:
            all_results = await self._hybrid_search(
                text, domains, sources, difficulty, content_type,
                start_date, end_date, learning_status
            )
        else:
            all_results = await self._keyword_search(
                text, domains, sources, difficulty, content_type,
                start_date, end_date, learning_status
            )

        total = len(all_results)
        total_pages = max(1, (total + page_size - 1) // page_size)
        start = (page - 1) * page_size
        end = start + page_size
        items = all_results[start:end]

        return PaginatedSearchResult(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
    
    async def _hybrid_search(
        self,
        text: str,
        domains: Optional[List[str]],
        sources: Optional[List[str]],
        difficulty: Optional[str],
        content_type: Optional[str],
        start_date: Optional[date],
        end_date: Optional[date],
        learning_status: Optional[str]
    ) -> List[SearchResult]:
        """混合搜索：结合语义和关键词"""
        vector_results = self.vector_service.search(query=text, n_results=50)
        
        if not vector_results:
            return await self._keyword_search(
                text, domains, sources, difficulty, content_type,
                start_date, end_date, learning_status
            )
        
        vector_ids = [r["content_id"] for r in vector_results]
        
        all_content = self._get_content_by_ids(vector_ids)
        if not all_content:
            return await self._keyword_search(
                text, domains, sources, difficulty, content_type,
                start_date, end_date, learning_status
            )
        
        filtered_content = self._apply_filters(
            all_content, domains, sources, difficulty, content_type,
            start_date, end_date, learning_status
        )
        
        results = []
        for content in filtered_content:
            content_id = content["id"]
            
            vector_distance = None
            for vr in vector_results:
                if vr["content_id"] == content_id:
                    vector_distance = vr["distance"]
                    break
            
            keyword_score = self._calculate_keyword_score(
                text, content.get("title", ""), content.get("short_summary", "")
            )
            
            semantic_score = 1.0 - vector_distance if vector_distance is not None else 0.0
            
            final_score = 0.6 * semantic_score + 0.4 * keyword_score
            
            results.append(SearchResult(
                content_id=content_id,
                title=content.get("title", ""),
                short_summary=content.get("short_summary", "") or content.get("summary", ""),
                long_summary=content.get("long_summary", "") or content.get("summary", ""),
                author=content.get("author", ""),
                source=content.get("source", ""),
                url=content.get("url", ""),
                update=content.get("update_date", ""),
                create_time=content.get("create_date", ""),
                tags=json.loads(content["tags"]) if content.get("tags") else [],
                knowledge_points=json.loads(content["knowledge_points"]) if content.get("knowledge_points") else [],
                learning_status=content.get("status", "未读"),
                relevance_score=round(final_score, 4)
            ))
        
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        return results
    
    async def _keyword_search(
        self,
        text: str,
        domains: Optional[List[str]],
        sources: Optional[List[str]],
        difficulty: Optional[str],
        content_type: Optional[str],
        start_date: Optional[date],
        end_date: Optional[date],
        learning_status: Optional[str]
    ) -> List[SearchResult]:
        """关键词搜索"""
        conditions = []
        params = []
        
        if text:
            conditions.append("(title LIKE ? OR content LIKE ? OR short_summary LIKE ?)")
            params.extend([f"%{text}%", f"%{text}%", f"%{text}%"])
        
        if domains:
            domain_conditions = []
            for domain in domains:
                domain_conditions.append("tags LIKE ?")
                params.append(f"%{domain}%")
            conditions.append(f"({' OR '.join(domain_conditions)})")
        
        if sources:
            source_conditions = []
            for source in sources:
                source_conditions.append("source = ?")
                params.append(source)
            conditions.append(f"({' OR '.join(source_conditions)})")
        
        if difficulty:
            conditions.append("tags LIKE ?")
            params.append(f"%{difficulty}%")
        
        if content_type:
            conditions.append("tags LIKE ?")
            params.append(f"%{content_type}%")
        
        if start_date:
            conditions.append("update_date >= ?")
            params.append(start_date.strftime("%Y-%m-%d"))
        if end_date:
            conditions.append("update_date <= ?")
            params.append(end_date.strftime("%Y-%m-%d"))
        
        if learning_status:
            conditions.append("ls.status = ?")
            params.append(learning_status)
        
        query = ""
        if conditions:
            query = "WHERE " + " AND ".join(conditions)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            sql = f"""
                SELECT c.id, c.title, c.short_summary, c.long_summary, c.author, c.source, c.update_date, c.create_date, 
                       c.tags, c.knowledge_points, c.url, ls.status
                FROM content c
                LEFT JOIN learning_status ls ON c.id = ls.content_id
                {query}
                ORDER BY c.create_date DESC
            """
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            
            results = []
            for row in rows:
                relevance_score = self._calculate_keyword_score(text, row[1], row[2])
                
                results.append(SearchResult(
                    content_id=row[0],
                    title=row[1],
                    short_summary=row[2] or "",
                    long_summary=row[3] or "",
                    author=row[4],
                    source=row[5],
                    url=row[10],
                    update=row[6],
                    create_time=row[7],
                    tags=json.loads(row[8]) if row[8] else [],
                    knowledge_points=json.loads(row[9]) if row[9] else [],
                    learning_status=row[11] or "未读",
                    relevance_score=round(relevance_score, 4)
                ))
            
            return results
    
    def _apply_filters(
        self,
        contents: List[dict],
        domains: Optional[List[str]],
        sources: Optional[List[str]],
        difficulty: Optional[str],
        content_type: Optional[str],
        start_date: Optional[date],
        end_date: Optional[date],
        learning_status: Optional[str]
    ) -> List[dict]:
        """应用筛选条件到内容列表"""
        filtered = []
        
        for content in contents:
            if domains:
                tags = json.loads(content["tags"]) if content.get("tags") else []
                if not any(d in tags for d in domains):
                    continue
            
            if sources and content.get("source") not in sources:
                continue
            
            if difficulty:
                tags = json.loads(content["tags"]) if content.get("tags") else []
                if difficulty not in tags:
                    continue
            
            if content_type:
                tags = json.loads(content["tags"]) if content.get("tags") else []
                if content_type not in tags:
                    continue
            
            if start_date and content.get("update_date"):
                if content["update_date"] < start_date.strftime("%Y-%m-%d"):
                    continue
            
            if end_date and content.get("update_date"):
                if content["update_date"] > end_date.strftime("%Y-%m-%d"):
                    continue
            
            if learning_status and content.get("status") != learning_status:
                continue
            
            filtered.append(content)
        
        return filtered
    
    def _get_content_by_ids(self, ids: List[str]) -> List[dict]:
        """根据ID列表获取内容"""
        if not ids:
            return []
        
        placeholders = ",".join(["?"] * len(ids))
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                SELECT c.id, c.title, c.short_summary, c.long_summary, c.author, c.source, c.update_date, c.create_date, 
                       c.tags, c.knowledge_points, c.content, c.url, ls.status
                FROM content c
                LEFT JOIN learning_status ls ON c.id = ls.content_id
                WHERE c.id IN ({placeholders})
            ''', ids)
            
            rows = cursor.fetchall()
            results = []
            for row in rows:
                results.append({
                    "id": row[0],
                    "title": row[1],
                    "short_summary": row[2] or "",
                    "long_summary": row[3] or "",
                    "author": row[4],
                    "source": row[5],
                    "update_date": row[6],
                    "create_date": row[7],
                    "tags": row[8],
                    "knowledge_points": row[9],
                    "content": row[10],
                    "url": row[11],
                    "status": row[12]
                })
            
            return results
    
    def _calculate_keyword_score(self, query: str, title: str, short_summary: str) -> float:
        """关键词相关度分数"""
        if not query:
            return 0.5
        
        score = 0.0
        query_lower = query.lower()
        
        if query_lower in title.lower():
            score += 0.6
        
        query_words = query_lower.split()
        for word in query_words:
            if word in title.lower():
                score += 0.3
            if word in short_summary.lower():
                score += 0.1
        
        return min(1.0, score)
    
    async def get_similar_content(self, content_id: str, limit: int = 5) -> List[SearchResult]:
        """基于向量相似度获取相似内容"""
        similar_ids = self.vector_service.search(
            query=f"similar_to:{content_id}",
            n_results=limit + 1
        )
        
        similar_ids = [r["content_id"] for r in similar_ids if r["content_id"] != content_id][:limit]
        
        if not similar_ids:
            return await self._get_similar_by_keywords(content_id, limit)
        
        all_content = self._get_content_by_ids(similar_ids)
        
        results = []
        for content in all_content:
            distance = None
            for sr in similar_ids:
                if sr == content["id"]:
                    distance = next((r["distance"] for r in similar_ids if r["content_id"] == content["id"]), None)
                    break
            
            results.append(SearchResult(
                content_id=content["id"],
                title=content.get("title", ""),
                short_summary=content.get("short_summary", "") or content.get("summary", ""),
                long_summary=content.get("long_summary", "") or content.get("summary", ""),
                author=content.get("author", ""),
                source=content.get("source", ""),
                url=content.get("url", ""),
                update=content.get("update_date", ""),
                create_time=content.get("create_date", ""),
                tags=json.loads(content["tags"]) if content.get("tags") else [],
                knowledge_points=json.loads(content["knowledge_points"]) if content.get("knowledge_points") else [],
                learning_status=content.get("status", "未读"),
                relevance_score=round(1.0 - distance, 4) if distance else 0.0
            ))
        
        return results
    
    async def _get_similar_by_keywords(self, content_id: str, limit: int) -> List[SearchResult]:
        """基于关键词获取相似内容（降级方案）"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT title, tags, knowledge_points
                FROM content
                WHERE id = ?
            ''', (content_id,))
            row = cursor.fetchone()
            if not row:
                return []
            
            title, tags_str, knowledge_points_str = row
            tags = json.loads(tags_str) if tags_str else []
            knowledge_points = json.loads(knowledge_points_str) if knowledge_points_str else []
            
            conditions = []
            params = []
            
            all_keywords = tags + knowledge_points
            if all_keywords:
                keyword_conditions = []
                for keyword in all_keywords[:5]:
                    keyword_conditions.append("(tags LIKE ? OR knowledge_points LIKE ?)")
                    params.extend([f"%{keyword}%", f"%{keyword}%"])
                conditions.append(f"({' OR '.join(keyword_conditions)})")
            
            conditions.append("id != ?")
            params.append(content_id)
            
            query = "WHERE " + " AND ".join(conditions)
            
            cursor.execute(f"""
                SELECT c.id, c.title, c.short_summary, c.long_summary, c.author, c.source, c.update_date, c.create_date, 
                       c.tags, c.knowledge_points, c.url, ls.status
                FROM content c
                LEFT JOIN learning_status ls ON c.id = ls.content_id
                {query}
                ORDER BY c.create_date DESC
                LIMIT ?
            """, params + [limit])
            
            rows = cursor.fetchall()
            results = []
            for row in rows:
                results.append(SearchResult(
                    content_id=row[0],
                    title=row[1],
                    short_summary=row[2] or "",
                    long_summary=row[3] or "",
                    author=row[4],
                    source=row[5],
                    url=row[10],
                    update=row[6],
                    create_time=row[7],
                    tags=json.loads(row[8]) if row[8] else [],
                    knowledge_points=json.loads(row[9]) if row[9] else [],
                    learning_status=row[11] or "未读",
                    relevance_score=0.0
                ))
            
            return results
    
    async def get_recommendations(self, user_id: Optional[str] = None, limit: int = 5) -> List[SearchResult]:
        """获取个性化推荐"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.id, c.title, c.short_summary, c.long_summary, c.author, c.source, c.update_date, c.create_date, 
                       c.tags, c.knowledge_points, c.url, ls.status
                FROM content c
                LEFT JOIN learning_status ls ON c.id = ls.content_id
                WHERE ls.status != '已读'
                ORDER BY c.create_date DESC
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            results = []
            for row in rows:
                results.append(SearchResult(
                    content_id=row[0],
                    title=row[1],
                    short_summary=row[2] or "",
                    long_summary=row[3] or "",
                    author=row[4],
                    source=row[5],
                    url=row[10],
                    update=row[6],
                    create_time=row[7],
                    tags=json.loads(row[8]) if row[8] else [],
                    knowledge_points=json.loads(row[9]) if row[9] else [],
                    learning_status=row[11] or "未读",
                    relevance_score=0.0
                ))
            
            return results
