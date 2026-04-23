import sqlite3
import hashlib
import json
from app.models.schemas import ContentResponse
from typing import Optional

class ContentManager:
    def __init__(self):
        self.db_path = "knowledge.db"
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # 创建内容表
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
            # 创建学习状态表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS learning_status (
                    content_id TEXT PRIMARY KEY,
                    status TEXT DEFAULT '未读',
                    note TEXT DEFAULT '',
                    FOREIGN KEY (content_id) REFERENCES content(id)
                )
            ''')
            conn.commit()
    
    async def save(self, content: ContentResponse) -> str:
        """保存内容，实现去重"""
        # 生成内容哈希值
        content_hash = self._generate_hash(content)
        
        # 检查是否已存在
        existing_id = await self._check_duplicate(content_hash, content.url)
        if existing_id:
            return existing_id
        
        # 生成唯一ID
        content_id = hashlib.md5((content.url + str(content.create_time)).encode()).hexdigest()
        
        # 保存到数据库
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
                # 初始化学习状态
                cursor.execute('''
                    INSERT INTO learning_status (content_id, status, note)
                    VALUES (?, ?, ?)
                ''', (content_id, '未读', ''))
                conn.commit()
                return content_id
            except sqlite3.IntegrityError:
                # 处理唯一约束冲突
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
            # 检查哈希值
            cursor.execute('SELECT id FROM content WHERE hash = ?', (content_hash,))
            row = cursor.fetchone()
            if row:
                return row[0]
            # 检查URL
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
            return cursor.rowcount > 0
    
    async def delete(self, content_id: str) -> bool:
        """删除内容"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # 删除学习状态
            cursor.execute('DELETE FROM learning_status WHERE content_id = ?', (content_id,))
            # 删除内容
            cursor.execute('DELETE FROM content WHERE id = ?', (content_id,))
            conn.commit()
            return cursor.rowcount > 0
    
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