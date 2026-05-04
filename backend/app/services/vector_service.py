import os
import time
from pathlib import Path
from typing import List, Dict, Optional, Sequence
import dashscope
from chromadb import EmbeddingFunction, Embeddings
from chromadb.api.types import Embeddable
import chromadb
from app.utils.config import get_settings
from app.utils.logger import get_logger

settings = get_settings()
logger = get_logger("vector_service")

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent


MODEL_DIMENSIONS = {
    "text-embedding-v1": 1536,
    "text-embedding-v2": 1536,
    "text-embedding-v3": 1024,
    "text-embedding-v4": 1024,
}


class CustomEmbeddingFunction(EmbeddingFunction):
    """
    自定义嵌入函数：基于 DashScope TextEmbedding API
    
    使用 .env 中 EMBEDDING_MODEL 配置的模型，默认 text-embedding-v4，
    通过 DASHSCOPE_API_KEY 鉴权调用
    """

    DEFAULT_MODEL = "text-embedding-v4"
    MAX_RETRIES = 3
    RETRY_DELAY_BASE = 1.0
    BATCH_SIZE = 25
    MAX_TOKENS = 8000

    def __init__(self):
        cfg = get_settings()
        self.model = cfg.EMBEDDING_MODEL or self.DEFAULT_MODEL
        self.api_key = cfg.DASHSCOPE_API_KEY

        if not self.api_key:
            raise RuntimeError("DashScope API Key (DASHSCOPE_API_KEY) 未配置")

        dashscope.api_key = self.api_key
        self.dimension = MODEL_DIMENSIONS.get(self.model)
        logger.info(f"EmbeddingFunction 初始化: model={self.model}, dimension={self.dimension}")

    def _truncate_texts(self, texts: Sequence[str]) -> List[str]:
        return [text[:self.MAX_TOKENS] if len(text) > self.MAX_TOKENS else text for text in texts]

    def _call_dashscope(self, texts: List[str]) -> List[List[float]]:
        last_error = None
        for attempt in range(self.MAX_RETRIES):
            try:
                resp = dashscope.TextEmbedding.call(
                    model=self.model,
                    input=texts,
                )

                if resp.status_code == 200:
                    embeddings = [
                        item["embedding"] for item in resp.output.get("embeddings", [])
                    ]
                    return embeddings

                if resp.status_code == 429:
                    wait_time = self.RETRY_DELAY_BASE * (2 ** attempt)
                    logger.warning(f"DashScope 限流 (429)，等待 {wait_time:.1f}s 后重试")
                    time.sleep(wait_time)
                    continue

                if resp.status_code >= 500:
                    wait_time = self.RETRY_DELAY_BASE * (2 ** attempt)
                    logger.warning(
                        f"DashScope 服务端错误 ({resp.status_code})，等待 {wait_time:.1f}s 后重试"
                    )
                    time.sleep(wait_time)
                    continue

                error_msg = (
                    f"DashScope 返回错误: status={resp.status_code}, "
                    f"code={resp.code}, message={resp.message}"
                )
                logger.error(error_msg)
                last_error = error_msg
                break

            except Exception as e:
                logger.error(f"DashScope 调用异常: {e}")
                last_error = str(e)

        raise RuntimeError(f"DashScope Embedding 调用失败，已重试 {self.MAX_RETRIES} 次: {last_error}")

    def _batch_generate(self, texts: Sequence[str]) -> Embeddings:
        text_list = self._truncate_texts(texts)

        for i in range(0, len(text_list), self.BATCH_SIZE):
            batch = text_list[i:i + self.BATCH_SIZE]
            logger.info(f"Embedding batch {i // self.BATCH_SIZE + 1}, 共 {len(batch)} 条")
            embeddings = self._call_dashscope(batch)
            if embeddings and len(embeddings) == len(batch):
                return embeddings

        raise RuntimeError("无法生成嵌入向量")

    def __call__(self, input: Embeddable) -> Embeddings:
        texts = input if isinstance(input, list) else [input]
        if not texts:
            return []

        try:
            return self._batch_generate(texts)
        except Exception as e:
            logger.error(f"生成嵌入向量失败: {e}")
            raise


class VectorService:
    """
    向量数据库服务

    基于 ChromaDB 提供内容向量化存储和语义检索功能
    使用 CustomEmbeddingFunction 通过 DashScope 生成嵌入向量
    """

    COLLECTION_NAME = "knowledge_embeddings"

    def __init__(self, persist_directory: Optional[str] = None):
        self.persist_dir = persist_directory or str(PROJECT_ROOT / "data" / "chroma_data")

        os.makedirs(self.persist_dir, exist_ok=True)

        self.embedding_function = CustomEmbeddingFunction()

        self.client = chromadb.PersistentClient(
            path=self.persist_dir,
            settings=chromadb.config.Settings(
                anonymized_telemetry=False
            )
        )

        self._init_or_migrate_collection()

        logger.info(f"向量服务初始化完成，持久化目录: {self.persist_dir}")
        logger.info(f"当前集合文档数量: {self.collection.count()}")

    def _init_or_migrate_collection(self):
        self.needs_rebuild = False
        try:
            self.collection = self.client.get_collection(
                name=self.COLLECTION_NAME,
                embedding_function=self.embedding_function,
            )
            collection_dim = self._get_collection_dimension()
            expected_dim = self.embedding_function.dimension

            if expected_dim and collection_dim and collection_dim != expected_dim:
                logger.warning(
                    f"集合维度不匹配: 集合={collection_dim}, 模型={expected_dim}，"
                    f"将重建向量集合"
                )
                self.client.delete_collection(name=self.COLLECTION_NAME)
                self.collection = self.client.create_collection(
                    name=self.COLLECTION_NAME,
                    embedding_function=self.embedding_function,
                    metadata={"hnsw:space": "cosine"}
                )
                self.needs_rebuild = True
                logger.info("向量集合已重建")
        except Exception:
            self.collection = self.client.get_or_create_collection(
                name=self.COLLECTION_NAME,
                embedding_function=self.embedding_function,
                metadata={"hnsw:space": "cosine"}
            )

    def _get_collection_dimension(self) -> Optional[int]:
        try:
            sample = self.collection.peek(limit=1)
            if sample and sample.get("embeddings") is not None:
                embeddings = sample["embeddings"]
                if len(embeddings) > 0 and len(embeddings[0]) > 0:
                    return len(embeddings[0])
        except Exception:
            pass

        try:
            metadata = self.collection.metadata
            if metadata and "dimension" in metadata:
                return metadata["dimension"]
        except Exception:
            pass

        return None

    def add_embedding(
        self,
        content_id: str,
        text: str,
        metadata: Optional[Dict] = None
    ) -> bool:
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
        try:
            self.collection.delete(ids=[content_id])
            logger.info(f"删除向量: {content_id}")
            return True
        except Exception as e:
            logger.error(f"删除向量失败 {content_id}: {str(e)}")
            return False

    def get_collection_size(self) -> int:
        return self.collection.count()

    def reset_collection(self) -> bool:
        try:
            self.client.delete_collection(name=self.COLLECTION_NAME)
            self.collection = self.client.create_collection(
                name=self.COLLECTION_NAME,
                embedding_function=self.embedding_function,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("向量集合已重置")
            return True
        except Exception as e:
            logger.error(f"重置集合失败: {str(e)}")
            return False
