import os
from pathlib import Path
import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Optional
import numpy as np
from app.utils.config import get_settings
from app.utils.logger import get_logger

settings = get_settings()
logger = get_logger("vector_service")

# 项目根目录
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent


class VectorService:
    """
    Chroma向量数据库服务
    
    提供内容向量化存储和语义检索功能
    使用本地持久化存储，支持增量更新
    """
    
    COLLECTION_NAME = "knowledge_embeddings"
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    
    def __init__(self, persist_directory: Optional[str] = None):
        """
        初始化向量服务
        
        Args:
            persist_directory: 向量数据库持久化目录，默认使用./chroma_data
        """
        self.persist_dir = persist_directory or str(PROJECT_ROOT / "chroma_data")
        
        os.makedirs(self.persist_dir, exist_ok=True)
        
        self.client = chromadb.PersistentClient(
            path=self.persist_dir,
            settings=chromadb.config.Settings(
                anonymized_telemetry=False
            )
        )
        
        self.collection = self.client.get_or_create_collection(
            name=self.COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        
        logger.info(f"向量服务初始化完成，持久化目录: {self.persist_dir}")
        logger.info(f"当前集合文档数量: {self.collection.count()}")
    
    def add_embedding(
        self,
        content_id: str,
        text: str,
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        添加内容向量
        
        Args:
            content_id: 内容ID
            text: 用于向量化的文本内容
            metadata: 附加元数据
            
        Returns:
            是否添加成功
        """
        try:
            if not text or not text.strip():
                logger.warning(f"内容为空，跳过向量化: {content_id}")
                return False
            
            embeddings_data = {
                "documents": [text],
                "ids": [content_id],
                "metadatas": [metadata or {}]
            }
            
            existing = self.collection.get(ids=[content_id])
            if existing and existing["ids"]:
                logger.info(f"更新已存在的向量: {content_id}")
                self.collection.update(**embeddings_data)
            else:
                logger.info(f"添加新向量: {content_id}")
                self.collection.add(**embeddings_data)
            
            return True
            
        except Exception as e:
            logger.error(f"添加向量失败 {content_id}: {str(e)}")
            return False
    
    def search(
        self,
        query: str,
        n_results: int = 10,
        where: Optional[Dict] = None
    ) -> List[Dict]:
        """
        语义搜索
        
        Args:
            query: 查询文本
            n_results: 返回结果数量
            where: 过滤条件
            
        Returns:
            搜索结果列表
        """
        try:
            if not query or not query.strip():
                return []
            
            query_params = {
                "query_texts": [query],
                "n_results": min(n_results, self.collection.count() or 100)
            }
            
            if where:
                query_params["where"] = where
            
            results = self.collection.query(**query_params)
            
            if not results or not results["ids"] or not results["ids"][0]:
                return []
            
            formatted_results = []
            for i, doc_id in enumerate(results["ids"][0]):
                result = {
                    "content_id": doc_id,
                    "distance": results["distances"][0][i] if results.get("distances") else 0,
                    "document": results["documents"][0][i] if results.get("documents") else "",
                    "metadata": results["metadatas"][0][i] if results.get("metadatas") else {}
                }
                formatted_results.append(result)
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"语义搜索失败: {str(e)}")
            return []
    
    def delete_embedding(self, content_id: str) -> bool:
        """
        删除内容向量
        
        Args:
            content_id: 内容ID
            
        Returns:
            是否删除成功
        """
        try:
            self.collection.delete(ids=[content_id])
            logger.info(f"删除向量: {content_id}")
            return True
        except Exception as e:
            logger.error(f"删除向量失败 {content_id}: {str(e)}")
            return False
    
    def get_collection_size(self) -> int:
        """获取集合中文档数量"""
        return self.collection.count()
    
    def reset_collection(self) -> bool:
        """重置整个集合（慎用）"""
        try:
            self.client.delete_collection(name=self.COLLECTION_NAME)
            self.collection = self.client.create_collection(
                name=self.COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("向量集合已重置")
            return True
        except Exception as e:
            logger.error(f"重置集合失败: {str(e)}")
            return False
