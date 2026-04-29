import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# 项目根目录（collectly/）
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent

# 加载项目根目录下的 .env 文件
load_dotenv(PROJECT_ROOT / ".env")

class Settings(BaseSettings):
    # TikHub API 配置
    TIKHUB_API_KEY: str = os.getenv("TIKHUB_API_KEY", "")
    TIKHUB_API_URL: str = "https://api.tikhub.dev"
    
    # DashScope API 配置
    DASHSCOPE_API_KEY: str = os.getenv("DASHSCOPE_API_KEY", "")
    
    # Qdrant 向量库配置
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")
    QDRANT_CLUSTER_ENDPOINT: str = os.getenv("QDRANT_CLUSTER_ENDPOINT", "")
    
    # Embedding 模型配置
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-v4")
    EMBEDDING_API_KEY: str = os.getenv("EMBEDDING_API_KEY", "")
    EMBEDDING_API_ENDPOINT: str = os.getenv("EMBEDDING_API_ENDPOINT", "")
    
    # 数据库配置
    DATABASE_URL: str = f"sqlite:///{PROJECT_ROOT / 'knowledge.db'}"
    
    # 应用配置
    APP_NAME: str = "AI 知识收藏与检索管家"
    DEBUG: bool = True
    
    class Config:
        case_sensitive = True

def get_settings() -> Settings:
    return Settings()
