from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

async def app_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401:
        # Отдать стандартный ответ для BasicAuth
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers={"WWW-Authenticate": "Basic"}
        )
    logger.warning(f"{exc.detail} (Request: {request.url})")
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "detail": exc.detail}
    )

"""Handle request validation errors."""
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Логируем
    logger.warning(f"Validation error: {exc.errors()} (Request: {request.url})")

    # Преобразуем ошибки в безопасный формат
    safe_details = []
    for err in exc.errors():
        safe_err = {}
        for k, v in err.items():
            # Если значение — исключение, преобразуем в строку
            if isinstance(v, Exception):
                safe_err[k] = str(v)
            else:
                safe_err[k] = v
        safe_details.append(safe_err)

    return JSONResponse(
        status_code=422,
        content={"success": False, "message": "Validation error", "details": safe_details}
    )

"""Handle general exceptions."""
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)} (Request: {request.url})")
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "Internal server error"}
    )