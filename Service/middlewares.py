# middlewares.py
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import logging
import asyncio
import time
logger = logging.getLogger("requests")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = asyncio.get_event_loop().time()
        client_ip = request.client.host if request.client else "unknown"
        logger.info(f"[НАЧАЛО] {request.method} {request.url.path} от {client_ip}")

        try:
            response = await call_next(request)
        except Exception as e:
            duration = time.time() - start
            logger.exception(
                f"[ОШИБКА] {request.method} {request.url.path} от {client_ip} - исключение: {e} - время: {duration:.3f} сек")
            raise  # обязательно пробрасываем ошибку дальше, чтобы FastAPI мог её корректно обработать
        else:
            duration = time.time() - start
            logger.info(
                f"[ЗАВЕРШЕНО] {request.method} {request.url.path} - статус {response.status_code} - время: {duration:.3f} сек")
            return response