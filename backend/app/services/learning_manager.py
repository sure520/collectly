import sqlite3
import json
from pathlib import Path
from typing import List, Optional

# 项目根目录
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent

class LearningManager:
    def __init__(self):
        self.db_path = str(PROJECT_ROOT / "knowledge.db")
    
    async def update_status(self, content_id: str, status: str) -> bool:
        """更新学习状态"""
        valid_statuses = ["未读", "已读", "重点", "待复习"]
        if status not in valid_statuses:
            raise ValueError(f"无效的学习状态: {status}")
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE learning_status
                SET status = ?
                WHERE content_id = ?
            ''', (status, content_id))
            conn.commit()
            return cursor.rowcount > 0
    
    async def update_tags(self, content_id: str, tags: List[str]) -> bool:
        """更新标签"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE content
                SET tags = ?
                WHERE id = ?
            ''', (json.dumps(tags), content_id))
            conn.commit()
            return cursor.rowcount > 0
    
    async def update_note(self, content_id: str, note: str) -> bool:
        """更新笔记"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE learning_status
                SET note = ?
                WHERE content_id = ?
            ''', (note, content_id))
            conn.commit()
            return cursor.rowcount > 0
    
    async def get_status(self, content_id: str) -> str:
        """获取学习状态"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT status
                FROM learning_status
                WHERE content_id = ?
            ''', (content_id,))
            row = cursor.fetchone()
            if row:
                return row[0]
            return "未读"
    
    async def get_note(self, content_id: str) -> str:
        """获取笔记"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT note
                FROM learning_status
                WHERE content_id = ?
            ''', (content_id,))
            row = cursor.fetchone()
            if row:
                return row[0]
            return ""
    
    async def get_stats(self) -> dict:
        """获取学习统计数据"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 总内容数
            cursor.execute('SELECT COUNT(*) FROM content')
            total_count = cursor.fetchone()[0]
            
            # 各状态内容数
            cursor.execute('''
                SELECT status, COUNT(*)
                FROM learning_status
                GROUP BY status
            ''')
            status_counts = {row[0]: row[1] for row in cursor.fetchall()}
            
            # 各平台内容数
            cursor.execute('''
                SELECT source, COUNT(*)
                FROM content
                GROUP BY source
            ''')
            source_counts = {row[0]: row[1] for row in cursor.fetchall()}
            
            # 各领域内容数
            cursor.execute('SELECT tags FROM content')
            domain_counts = {}
            for row in cursor.fetchall():
                if row[0]:
                    tags = json.loads(row[0])
                    for tag in tags:
                        if tag in ["大模型", "Agent", "RAG", "多模态"]:
                            domain_counts[tag] = domain_counts.get(tag, 0) + 1
            
            # 学习进度
            read_count = status_counts.get("已读", 0)
            progress = (read_count / total_count * 100) if total_count > 0 else 0
            
            return {
                "total_count": total_count,
                "status_counts": status_counts,
                "source_counts": source_counts,
                "domain_counts": domain_counts,
                "progress": round(progress, 2)
            }
    
    async def get_content_by_status(self, status: str) -> list:
        """根据学习状态获取内容"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.id, c.title, c.short_summary, c.long_summary, c.author, c.source, c.update_date, c.create_date
                FROM content c
                JOIN learning_status ls ON c.id = ls.content_id
                WHERE ls.status = ?
                ORDER BY c.create_date DESC
            ''', (status,))
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
                    "update": row[6],
                    "create_time": row[7]
                })
            return results
    
    async def get_content_by_tag(self, tag: str) -> list:
        """根据标签获取内容"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, title, short_summary, long_summary, author, source, update_date, create_date
                FROM content
                WHERE tags LIKE ?
                ORDER BY create_date DESC
            ''', (f"%{tag}%",))
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
                    "update": row[6],
                    "create_time": row[7]
                })
            return results