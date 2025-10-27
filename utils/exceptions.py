from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

# TODO переведен на асинхронный postgres

async def app_exception_handler(request: Request, exc: HTTPException):
    '''обработчик исключений (приложение)'''
    if exc.status_code == 401 and request.url.path in ["/api/docs", "/api/redoc"]:
        # Отдать стандартный ответ для BasicAuth
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail}, headers={"WWW-Authenticate": "Basic"})
        # Для всех остальных 401 и других ошибок
    logger.warning(f"{exc.detail} (Request: {request.url})")
    return JSONResponse(status_code=exc.status_code, content={"success": False, "detail": exc.detail})

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    '''обработчик исключений request validation errors'''
    logger.warning(f"Validation error: {exc.errors()} (Request: {request.url})")
    return JSONResponse(status_code=422, content={"success": False, "message": "Validation error", "details": exc.errors()})

async def general_exception_handler(request: Request, exc: Exception):
    '''обработчик исключений общий (сюда попадают все остальные исключения, не попавшие под первые два)'''
    logger.error(f"Unhandled exception: {str(exc)} (Request: {request.url})")
    return JSONResponse(status_code=500, content={"success": False, "message": "Internal server error"})