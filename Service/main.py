from Service.Database import engine, log_engine
from Service.config import TEMPLATES_DIR
from Service.Routers import tasks,students,auth,files  # Импортируем роутер задач
from Service.Routers.auth import get_swagger_user
from Service.log import setup_logging
from Service.middlewares import LoggingMiddleware

from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy import text
import uvicorn
import logging

# main.py
'''главный файл проекта'''

# Настроим логирование при запуске приложения
setup_logging()



app = FastAPI(debug=True, docs_url=None, redoc_url=None)
# Регистрируем роутер
app.include_router(auth.home_router)
app.include_router(tasks.task_router) # подключает маршруты из routers/tasks.py.
app.include_router(tasks.subtask_router)  # Регистрируем роутер для подзадач
app.include_router(tasks.task_js_router) # Регистрируем роутер для html файлов с js
app.include_router(tasks.varinant_router) # Регистрируем роутер для html файлов с jinja2
app.include_router(students.students_router)  # Регистрируем роутер для студентов
app.include_router(students.students_subtasks_router) # Регистрируем роутер для задач студентов
app.include_router(auth.auth_router) # Регистрируем роутер Аутентификации
app.include_router(auth.admin_router)
app.add_middleware(LoggingMiddleware) # Middleware для логов всех запросов
#app.include_router(files.router)

#app.include_router(web_auth.router) # подключаем home
app.mount("/static", StaticFiles(directory="Templates/Static"), name="static") # для CSS файлов
app.mount("/Uploads", StaticFiles(directory="Uploads"), name="uploads") # для файлов
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# для запросов с фронта
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # ✅ разрешаешь запросы с фронта
    allow_credentials=True,                  # ✅ разрешаешь куки / авторизацию
    allow_methods=["*"],                     # ✅ разрешаешь любые HTTP-методы (GET, POST, PUT и т.д.)
    allow_headers=["*"],                     # ✅ разрешаешь любые заголовки (например, Authorization)
)


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

# Перенаправление на страницу логина при открытии корня (Основной адрес сайта)
@app.get("/")
def read():
    return RedirectResponse(url="/home/login_in/")

"""Swagger"""
@app.get("/docs", dependencies=[Depends(get_swagger_user)])
async def get_documentation():
    return get_swagger_ui_html(openapi_url=app.openapi_url, title="Документация API")

@app.get("/redoc", dependencies=[Depends(get_swagger_user)])
async def get_redoc_documentation():
    return get_redoc_html(openapi_url=app.openapi_url, title="Документация API")

"""запуск сервера"""
if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=9000)