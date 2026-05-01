import sqlite3
import hashlib
import json
import logging
from pathlib import Path
from app.models.schemas import ContentResponse
from app.services.vector_service import VectorService
from typing import Optional

logger = logging.getLogger("vector_service")

# 项目根目录
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent

class ContentManager:
    def __init__(self):
        self.db_path = str(PROJECT_ROOT / "knowledge.db")
        self._init_db()
        self.vector_service = VectorService()
        if self.vector_service.needs_rebuild:
            self._auto_rebuild_vectors()
    
    def _auto_rebuild_vectors(self):
        """当向量集合因维度变化被重建时，自动重新嵌入所有已有内容"""
        logger.info("检测到向量集合维度变更，开始自动重建向量索引...")
        try:
            all_content = self.get_all_sync()
            if not all_content:
                logger.info("没有已有内容需要重新嵌入")
                return

            success_count = 0
            for content in all_content:
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
                embedding_text = self._build_embedding_text(content_obj)
                metadata = {
                    "source": content["source"],
                    "title": content["title"],
                    "tags": json.dumps(content["tags"]),
                    "knowledge_points": json.dumps(content["knowledge_points"])
                }
                if self.vector_service.add_embedding(
                    content_id=content["id"],
                    text=embedding_text,
                    metadata=metadata
                ):
                    success_count += 1

            logger.info(
                f"向量索引自动重建完成: {success_count}/{len(all_content)} 条成功"
            )
        except Exception as e:
            logger.error(f"自动重建向量索引失败: {e}")
    
    def get_all_sync(self) -> list:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, title, content, author, update_date, create_date, url, source, 
                       tags, knowledge_points, summary
                FROM content
            ''')
            rows = cursor.fetchall()
            results = []
            for row in rows:
                results.append({
                    "id": row[0],
                    "title": row[1],
                    "content": row[2],
                    "author": row[3],
                    "update": row[4],
                    "create_time": row[5],
                    "url": row[6],
                    "source": row[7],
                    "tags": json.loads(row[8]) if row[8] else [],
                    "knowledge_points": json.loads(row[9]) if row[9] else [],
                    "summary": row[10]
                })
            return results
    
    def _init_db(self):
        """初始化数据库"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS content (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    content TEXT,
                    author TEXT,
                    update_date TEXT,
                    create_date TEXT,
                    url TEXT UNIQUE,
                    source TEXT,
                    tags TEXT,
                    knowledge_points TEXT,
                    summary TEXT,
                    hash TEXT UNIQUE
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS learning_status (
                    content_id TEXT PRIMARY KEY,
                    status TEXT DEFAULT '未读',
                    note TEXT DEFAULT '',
                    FOREIGN KEY (content_id) REFERENCES content(id)
                )
            ''')
            conn.commit()
    
    def _build_embedding_text(self, content: ContentResponse) -> str:
        """构建用于向量化的完整文本"""
        parts = []
        if content.title:
            parts.append(f"标题: {content.title}")
        if content.summary:
            parts.append(f"摘要: {content.summary}")
        if content.content:
            content_text = content.content[:3000]
            parts.append(f"内容: {content_text}")
        if content.knowledge_points:
            parts.append(f"知识点: {', '.join(content.knowledge_points)}")
        if content.tags:
            parts.append(f"标签: {', '.join(content.tags)}")
        return "\n".join(parts)
    
    async def save(self, content: ContentResponse) -> str:
        """保存内容，实现去重"""
        content_hash = self._generate_hash(content)
        
        existing_id = await self._check_duplicate(content_hash, content.url)
        if existing_id:
            return existing_id
        
        content_id = hashlib.md5((content.url + str(content.create_time)).encode()).hexdigest()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO content (
                        id, title, content, author, update_date, create_date, url, source, 
                        tags, knowledge_points, summary, hash
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    content_id,
                    content.title,
                    content.content,
                    content.author,
                    content.update,
                    content.create_time,
                    content.url,
                    content.source,
                    json.dumps(content.tags),
                    json.dumps(content.knowledge_points),
                    content.summary,
                    content_hash
                ))
                cursor.execute('''
                    INSERT INTO learning_status (content_id, status, note)
                    VALUES (?, ?, ?)
                ''', (content_id, '未读', ''))
                conn.commit()
                
                embedding_text = self._build_embedding_text(content)
                metadata = {
                    "source": content.source,
                    "title": content.title,
                    "tags": json.dumps(content.tags),
                    "knowledge_points": json.dumps(content.knowledge_points)
                }
                self.vector_service.add_embedding(
                    content_id=content_id,
                    text=embedding_text,
                    metadata=metadata
                )
                
                return content_id
            except sqlite3.IntegrityError:
                return await self._get_existing_id(content.url)
    
    async def get(self, content_id: str) -> ContentResponse:
        """获取内容详情"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT title, content, author, update_date, create_date, url, source, 
                       tags, knowledge_points, summary
                FROM content
                WHERE id = ?
            ''', (content_id,))
            row = cursor.fetchone()
            if not row:
                raise ValueError("内容不存在")
            
            return ContentResponse(
                title=row[0],
                content=row[1],
                author=row[2],
                update=row[3],
                create_time=row[4],
                url=row[5],
                source=row[6],
                tags=json.loads(row[7]) if row[7] else [],
                knowledge_points=json.loads(row[8]) if row[8] else [],
                summary=row[9]
            )
    
    async def _check_duplicate(self, content_hash: str, url: str) -> Optional[str]:
        """检查是否存在重复内容"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM content WHERE hash = ?', (content_hash,))
            row = cursor.fetchone()
            if row:
                return row[0]
            cursor.execute('SELECT id FROM content WHERE url = ?', (url,))
            row = cursor.fetchone()
            if row:
                return row[0]
            return None
    
    async def _get_existing_id(self, url: str) -> str:
        """获取已存在内容的ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM content WHERE url = ?', (url,))
            row = cursor.fetchone()
            if row:
                return row[0]
            raise ValueError("内容不存在")
    
    def _generate_hash(self, content: ContentResponse) -> str:
        """生成内容哈希值"""
        hash_input = f"{content.title}{content.content}{content.author}"
        return hashlib.md5(hash_input.encode()).hexdigest()
    
    async def update(self, content_id: str, content: ContentResponse) -> bool:
        """更新内容"""
        content_hash = self._generate_hash(content)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE content
                SET title = ?, content = ?, author = ?, update_date = ?, 
                    tags = ?, knowledge_points = ?, summary = ?, hash = ?
                WHERE id = ?
            ''', (
                content.title,
                content.content,
                content.author,
                content.update,
                json.dumps(content.tags),
                json.dumps(content.knowledge_points),
                content.summary,
                content_hash,
                content_id
            ))
            conn.commit()
            success = cursor.rowcount > 0
            
            if success:
                embedding_text = self._build_embedding_text(content)
                metadata = {
                    "source": content.source,
                    "title": content.title,
                    "tags": json.dumps(content.tags),
                    "knowledge_points": json.dumps(content.knowledge_points)
                }
                self.vector_service.add_embedding(
                    content_id=content_id,
                    text=embedding_text,
                    metadata=metadata
                )
            
            return success
    
    async def delete(self, content_id: str) -> bool:
        """删除内容"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM learning_status WHERE content_id = ?', (content_id,))
            cursor.execute('DELETE FROM content WHERE id = ?', (content_id,))
            conn.commit()
            deleted = cursor.rowcount > 0
            
            if deleted:
                self.vector_service.delete_embedding(content_id)
            
            return deleted
    
    async def get_all(self) -> list:
        """获取所有内容"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, title, content, author, update_date, create_date, url, source, 
                       tags, knowledge_points, summary
                FROM content
            ''')
            rows = cursor.fetchall()
            results = []
            for row in rows:
                results.append({
                    "id": row[0],
                    "title": row[1],
                    "content": row[2],
                    "author": row[3],
                    "update": row[4],
                    "create_time": row[5],
                    "url": row[6],
                    "source": row[7],
                    "tags": json.loads(row[8]) if row[8] else [],
                    "knowledge_points": json.loads(row[9]) if row[9] else [],
                    "summary": row[10]
                })
            return results
    
    async def get_vector_stats(self) -> dict:
        """获取向量库统计信息"""
        return {
            "collection_size": self.vector_service.get_collection_size()
        }
