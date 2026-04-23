from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from app.utils.logger import get_logger

logger = get_logger("error_handler")

class AppException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class PlatformParseError(AppException):
    def __init__(self, platform: str, message: str):
        super().__init__(f"解析{platform}链接失败: {message}", 400)

class ContentNotFoundError(AppException):
    def __init__(self, content_id: str):
        super().__init__(f"内容不存在: {content_id}", 404)

class DuplicateContentError(AppException):
    def __init__(self, content_id: str):
        super().__init__(f"内容已存在: {content_id}", 409)

class InvalidStatusError(AppException):
    def __init__(self, status: str):
        super().__init__(f"无效的学习状态: {status}", 400)

async def app_exception_handler(request: Request, exc: AppException):
    logger.error(f"Application error: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message}
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "服务器内部错误，请稍后重试"}
    )

def register_exception_handlers(app):
    from fastapi import FastAPI
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)