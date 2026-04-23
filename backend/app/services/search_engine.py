import sqlite3
import json
from typing import List, Optional
from datetime import date
from app.models.schemas import SearchResult
import numpy as np

class SearchEngine:
    def __init__(self):
        self.db_path = "knowledge.db"
    
    async def search(
        self,
        text: str,
        domains: Optional[List[str]] = None,
        sources: Optional[List[str]] = None,
        difficulty: Optional[str] = None,
        content_type: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        learning_status: Optional[str] = None
    ) -> List[SearchResult]:
        """智能检索内容"""
        # 构建查询条件
        conditions = []
        params = []
        
        # 基本搜索条件
        if text:
            conditions.append("(title LIKE ? OR content LIKE ? OR summary LIKE ?)")
            params.extend([f"%{text}%", f"%{text}%", f"%{text}%"])
        
        # 领域筛选
        if domains:
            domain_conditions = []
            for domain in domains:
                domain_conditions.append("tags LIKE ?")
                params.append(f"%{domain}%")
            conditions.append(f"({' OR '.join(domain_conditions)})")
        
        # 来源筛选
        if sources:
            source_conditions = []
            for source in sources:
                source_conditions.append("source = ?")
                params.append(source)
            conditions.append(f"({' OR '.join(source_conditions)})")
        
        # 难度筛选
        if difficulty:
            conditions.append("tags LIKE ?")
            params.append(f"%{difficulty}%")
        
        # 内容类型筛选
        if content_type:
            conditions.append("tags LIKE ?")
            params.append(f"%{content_type}%")
        
        # 时间筛选
        if start_date:
            conditions.append("update_date >= ?")
            params.append(start_date.strftime("%Y-%m-%d"))
        if end_date:
            conditions.append("update_date <= ?")
            params.append(end_date.strftime("%Y-%m-%d"))
        
        # 构建SQL查询
        query = ""
        if conditions:
            query = "WHERE " + " AND ".join(conditions)
        
        # 执行查询
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            sql = f"""
                SELECT c.id, c.title, c.summary, c.author, c.source, c.update_date, c.create_date, 
                       c.tags, c.knowledge_points, ls.status
                FROM content c
                LEFT JOIN learning_status ls ON c.id = ls.content_id
                {query}
                ORDER BY c.create_date DESC
            """
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            
            # 构建搜索结果
            results = []
            for row in rows:
                # 计算相关度分数（简单实现，实际项目中可以使用向量相似度）
                relevance_score = self._calculate_relevance(text, row[1], row[2])
                
                results.append(SearchResult(
                    content_id=row[0],
                    title=row[1],
                    summary=row[2],
                    author=row[3],
                    source=row[4],
                    update=row[5],
                    create_time=row[6],
                    tags=json.loads(row[7]) if row[7] else [],
                    knowledge_points=json.loads(row[8]) if row[8] else [],
                    learning_status=row[9] or "未读",
                    relevance_score=relevance_score
                ))
            
            # 按相关度排序
            results.sort(key=lambda x: x.relevance_score, reverse=True)
            return results
    
    def _calculate_relevance(self, query: str, title: str, summary: str) -> float:
        """计算相关度分数"""
        if not query:
            return 1.0
        
        # 简单的相关度计算
        score = 0.0
        query_words = query.lower().split()
        
        # 标题匹配加分
        title_lower = title.lower()
        for word in query_words:
            if word in title_lower:
                score += 0.5
        
        # 摘要匹配加分
        summary_lower = summary.lower()
        for word in query_words:
            if word in summary_lower:
                score += 0.3
        
        # 归一化分数
        max_score = len(query_words) * 0.8
        if max_score > 0:
            score = min(1.0, score / max_score)
        
        return score
    
    async def get_similar_content(self, content_id: str, limit: int = 5) -> List[SearchResult]:
        """获取相似内容"""
        # 获取当前内容
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
            
            # 构建相似内容查询
            conditions = []
            params = []
            
            # 基于标签和知识点匹配
            all_keywords = tags + knowledge_points
            if all_keywords:
                keyword_conditions = []
                for keyword in all_keywords[:5]:  # 最多使用5个关键词
                    keyword_conditions.append("(tags LIKE ? OR knowledge_points LIKE ?)")
                    params.extend([f"%{keyword}%", f"%{keyword}%"])
                conditions.append(f"({' OR '.join(keyword_conditions)})")
            
            # 排除当前内容
            conditions.append("id != ?")
            params.append(content_id)
            
            # 构建SQL查询
            query = "WHERE " + " AND ".join(conditions)
            
            cursor.execute(f"""
                SELECT c.id, c.title, c.summary, c.author, c.source, c.update_date, c.create_date, 
                       c.tags, c.knowledge_points, ls.status
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
                    summary=row[2],
                    author=row[3],
                    source=row[4],
                    update=row[5],
                    create_time=row[6],
                    tags=json.loads(row[7]) if row[7] else [],
                    knowledge_points=json.loads(row[8]) if row[8] else [],
                    learning_status=row[9] or "未读",
                    relevance_score=0.0  # 相似内容不计算相关度
                ))
            
            return results
    
    async def get_recommendations(self, user_id: Optional[str] = None, limit: int = 5) -> List[SearchResult]:
        """获取个性化推荐"""
        # 简单的推荐实现，实际项目中可以基于用户历史行为
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.id, c.title, c.summary, c.author, c.source, c.update_date, c.create_date, 
                       c.tags, c.knowledge_points, ls.status
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
                    summary=row[2],
                    author=row[3],
                    source=row[4],
                    update=row[5],
                    create_time=row[6],
                    tags=json.loads(row[7]) if row[7] else [],
                    knowledge_points=json.loads(row[8]) if row[8] else [],
                    learning_status=row[9] or "未读",
                    relevance_score=0.0  # 推荐内容不计算相关度
                ))
            
            return results