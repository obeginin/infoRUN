# middlewares/logging_middleware.py
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import logging

logger = logging.getLogger("requests")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"Запрос: {request.method} {request.url.path}")
        response = await call_next(request)
        logger.info(f"Ответ: {request.method} {request.url.path} - статус {response.status_code}")
        return response