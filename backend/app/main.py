import sys
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# 将 backend 目录添加到模块搜索路径，支持从项目根目录启动
BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.api import routes
from app.services.platform_parser import PlatformParser
from app.utils.config import get_settings
from app.utils.logger import get_logger
from app.utils.exceptions import register_exception_handlers

settings = get_settings()
logger = get_logger("main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("AI 知识收藏与检索管家 API 启动")
    yield
    logger.info("AI 知识收藏与检索管家 API 关闭")

app = FastAPI(
    title="AI 知识收藏与检索管家 API",
    description="跨平台内容解析、存储、检索与学习管理服务",
    version="1.0.0",
    lifespan=lifespan
)

# 注册异常处理器
register_exception_handlers(app)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(routes.router, prefix="/api")

# 健康检查端点
@app.get("/health")
def health_check():
    logger.info("健康检查请求")
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)