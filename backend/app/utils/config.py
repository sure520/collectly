import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv, set_key

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
ENV_PATH = PROJECT_ROOT / ".env"

load_dotenv(ENV_PATH)


class Settings(BaseSettings):
    TIKHUB_API_KEY: str = os.getenv("TIKHUB_API_KEY", "")
    TIKHUB_API_URL: str = "https://api.tikhub.dev"

    DASHSCOPE_API_KEY: str = os.getenv("DASHSCOPE_API_KEY", "")

    LLM_MODEL_NAME: str = os.getenv("LLM_MODEL_NAME", "qwen-plus")
    ASR_MODEL_NAME: str = os.getenv("ASR_MODEL_NAME", "qwen3-asr-flash")
    VISION_MODEL_NAME: str = os.getenv("VISION_MODEL_NAME", "qwen3-vl-flash")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-v4")
    EMBEDDING_API_KEY: str = os.getenv("EMBEDDING_API_KEY", "")
    EMBEDDING_API_ENDPOINT: str = os.getenv("EMBEDDING_API_ENDPOINT", "")

    DATABASE_URL: str = f"sqlite:///{PROJECT_ROOT / 'knowledge.db'}"

    APP_NAME: str = "AI 知识收藏与检索管家"
    DEBUG: bool = True

    class Config:
        case_sensitive = True


_settings: Optional[Settings] = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def update_settings(new_values: dict) -> Settings:
    global _settings
    current = get_settings()

    env_keys = [
        "TIKHUB_API_KEY",
        "DASHSCOPE_API_KEY",
        "LLM_MODEL_NAME",
        "ASR_MODEL_NAME",
        "VISION_MODEL_NAME",
        "EMBEDDING_MODEL",
        "EMBEDDING_API_KEY",
        "EMBEDDING_API_ENDPOINT",
    ]

    for key in env_keys:
        if key in new_values:
            value = str(new_values[key])
            if ENV_PATH.exists():
                set_key(str(ENV_PATH), key, value)
            else:
                with open(ENV_PATH, "a", encoding="utf-8") as f:
                    f.write(f"{key}={value}\n")
            os.environ[key] = value

    _settings = Settings()
    return _settings
