
import os
import logging
import uvicorn
import time
from sqlalchemy import text
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_400_BAD_REQUEST

from utils.config import settings
from utils.log import setup_logging
from utils.exceptions import app_exception_handler, validation_exception_handler, general_exception_handler
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from Service.api import tasks, subtasks,students,auth,subjects, variants  # Импортируем роутер задач
from Service.api.swagger import swagger_router
from Service.Crud.auth import get_swagger_user
from Service.Database import engine
from Service.producer import get_kafka_producer
from Service.middlewares import LoggingMiddleware

# main.py
'''главный файл проекта'''

# Настроим логирование при успешном запуске основного приложения FastAPI
setup_logging(log_file=settings.LOG_FILE)
logger = logging.getLogger(__name__)

# Инициализация FastAPI
app = FastAPI(debug=settings.LOG_LEVEL, docs_url=None, redoc_url=None)

# CORS (для запросов с фронта)
origins = [
    "http://localhost:5173",       # локальный фронт (Vite)
    "http://127.0.0.1:5173",       # иногда нужен этот
    "http://localhost:3000",       # локальный фронт (Vite)
    "http://127.0.0.1:3000",
    "http://10.8.0.9:3000",
    "https://info-run.ru",         # если фронт будет на проде
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,                   # ✅ разрешаешь запросы с фронта
    allow_credentials=True,                  # ✅ разрешаешь куки / авторизацию
    allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS"],                     # ✅ разрешаешь любые HTTP-методы (GET, POST, PUT и т.д.)
    allow_headers=["*"],                     # ✅ разрешаешь любые заголовки (например, Authorization)
)
app.add_middleware(LoggingMiddleware) # Middleware для логов всех запросов

# Путь до билд-фронта
#frontend_path = os.path.join(os.path.dirname(__file__), "..", "Client", "dist")
#dist_static_dir = os.path.join(os.path.dirname(__file__), "..", "Client", "dist", "_next")

# Исключения
app.add_exception_handler(HTTPException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)


# Kafka
producer = get_kafka_producer()
# корректное завершение соединения kafka
@app.on_event("shutdown")
def shutdown_event():
    if producer:
        producer.close()


# Подключение роутеров
app.include_router(auth.auth_router) # Регистрируем роутер Аутентификации
app.include_router(auth.admin_router)
app.include_router(auth.home_router)
app.include_router(subjects.subject_router)  # маршрут для предметов
app.include_router(tasks.task_router) # подключает маршруты из routers/tasks.py.
app.include_router(subtasks.subtask_router)  # Регистрируем роутер для подзадач
app.include_router(variants.variant_router)
app.include_router(students.students_router)  # Регистрируем роутер для студентов
app.include_router(students.students_subtasks_router) # Регистрируем роутер для задач студентов
app.include_router(swagger_router)


# Подключаем статику
app.mount("/Uploads", StaticFiles(directory=settings.UPLOADS_DIR), name="uploads") # для файлов
#app.mount("/static", StaticFiles(directory="Templates/Static"), name="static") # для CSS файлов
#templates = Jinja2Templates(directory=settings.TEMPLATES_DIR) # для Jinja




async def check_db_connection(engine, name: str, retries: int = 5, delay: int = 3):
    for attempt in range(1, retries + 1):
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            logger.info(f"✅ Подключение к базе данных '{name}' установлено.")
            return
        except Exception as e:
            logger.error(f"❌ Ошибка подключения к базе '{name}' (Попытка {attempt}/{retries}): {e}")
            if attempt < retries:
                await time.sleep(delay)
            else:
                logger.critical(f"Не удалось подключиться к базе '{name}' после {retries} попыток.")
                raise

@app.on_event("startup")
async def startup_event():
    logging.info("🚀 Проверка подключений к базам данных...")
    check_db_connection(engine, "infoDB")
    #check_db_connection(log_engine, "LogDB") # для использования второй базы логов



# Health check endpoint
@app.get("/api/health", tags=["Health"], summary="роут проверки конфигурации")
async def health_check():
    """Проверка состояния сервиса."""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": "1.0",
        "environment": settings.ENVIRONMENT
    }

"""Swagger"""

@app.get("/api/docs", dependencies=[Depends(get_swagger_user)])
async def get_documentation():
    return get_swagger_ui_html(
        openapi_url="/api/openapi.json",  # <- важно
        title="Документация API"
    )

@app.get("/api/redoc", dependencies=[Depends(get_swagger_user)])
async def get_redoc_documentation():
    return get_redoc_html(
        openapi_url="/api/openapi.json",
        title="Документация API"
    )

# openapi.json без защиты
@app.get("/api/openapi.json")
async def openapi():
    return app.openapi()



'''Функция для добавления токена авторизации в SWAGGER'''
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Документация API",
        version="1.0.0",
        description="Описание API с авторизацией",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # Добавим схему по умолчанию ко всем методам (можно кастомизировать при необходимости)
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth": []}])

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

"""запуск сервера"""
if __name__ == "__main__":
    uvicorn.run(
        "Service.main:app",  # путь к объекту app
        host="0.0.0.0",
        port=9000,
        reload=True  # только для dev
    )