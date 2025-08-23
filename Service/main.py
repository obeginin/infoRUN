from Service.config_app import TEMPLATES_DIR, LOG_LEVEL, LOG_FILE
from fastapi import FastAPI, Depends, Request, HTTPException
from Service.Routers import tasks, subtasks,students,auth,files  # Импортируем роутер задач
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.staticfiles import StaticFiles
from Service.Crud.auth import get_swagger_user
import uvicorn
from sqlalchemy import text
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from utils.log import setup_logging
from Service.middlewares import LoggingMiddleware
from fastapi.middleware.cors import CORSMiddleware
import logging
from Service.Database import engine, log_engine
from Service.producer import get_kafka_producer
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from fastapi.openapi.utils import get_openapi
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request
from starlette.status import HTTP_400_BAD_REQUEST
# main.py
'''главный файл проекта'''

# Настроим логирование при успешном запуске основного приложения FastAPI
setup_logging(log_file=LOG_FILE)
logging.info(f"Запускаем логирование с файлом: {LOG_FILE}")

app = FastAPI(debug=LOG_LEVEL, docs_url=None, redoc_url=None)

origins = [
    "http://localhost:5173",       # локальный фронт (Vite)
    "http://127.0.0.1:5173",       # иногда нужен этот
    "http://localhost:3000",       # локальный фронт (Vite)
    "http://127.0.0.1:3000",
    "http://10.8.0.9:3000",
    "https://info-run.ru",         # если фронт будет на проде
]
# для запросов с фронта
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


producer = get_kafka_producer()
# Регистрируем роутер
app.include_router(auth.auth_router) # Регистрируем роутер Аутентификации
app.include_router(auth.admin_router)
app.include_router(auth.home_router)
app.include_router(tasks.subject_router)  # маршрут для предметов
app.include_router(tasks.task_router) # подключает маршруты из routers/tasks.py.
app.include_router(subtasks.subtask_router)  # Регистрируем роутер для подзадач
app.include_router(tasks.task_js_router) # Регистрируем роутер для html файлов с js
app.include_router(tasks.varinant_router) # Регистрируем роутер для html файлов с jinja2

app.include_router(students.students_router)  # Регистрируем роутер для студентов
app.include_router(students.students_subtasks_router) # Регистрируем роутер для задач студентов



#app.include_router(files.router)

#app.include_router(web_auth.router) # подключаем home
#app.mount("/static", StaticFiles(directory="Templates/Static"), name="static") # для CSS файлов
app.mount("/Uploads", StaticFiles(directory="Uploads"), name="uploads") # для файлов
templates = Jinja2Templates(directory=TEMPLATES_DIR)



# Подключаем статику
#app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
#app.mount("/_next", StaticFiles(directory=dist_static_dir), name="next")



def check_db_connection(engine, name):
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logging.info(f"✅ Подключение к базе данных '{name}' установлено.")
    except Exception as e:
        logging.error(f"❌ Ошибка подключения к базе '{name}': {e}")

@app.on_event("startup")
def startup_event():
    logging.info("🚀 Проверка подключений к базам данных...")
    check_db_connection(engine, "infoDB")
    check_db_connection(log_engine, "LogDB")

# корректное завершение соединения kafka
@app.on_event("shutdown")
def shutdown_event():
    producer = get_kafka_producer()
    if producer:
        producer.close()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()

    # Удаляем поле ctx, чтобы убрать дублирование
    for error in errors:
        if "ctx" in error:
            del error["ctx"]

    logging.warning(f"[400 VALIDATION ERROR] {request.method} {request.url} - ошибки: {errors}")

    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"detail": errors},
    )

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

# Обработка остальных маршрутов (если SPA)
'''@app.get("/{full_path:path}")
def read_spa(full_path: str):
    excluded_paths = ("api", "docs", "openapi.json", "redoc")
    if any(full_path == p or full_path.startswith(p + "/") for p in excluded_paths):
        raise HTTPException(status_code=404)
    return FileResponse(os.path.join(frontend_path, "index.html"))'''

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
    uvicorn.run("main:app", host="localhost", port=9000)