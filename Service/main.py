from config import TEMPLATES_DIR
from fastapi import FastAPI, Depends
from Routers import tasks,students,auth,files  # Импортируем роутер задач
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.staticfiles import StaticFiles
from Crud.auth import get_swagger_user
import uvicorn
from sqlalchemy import text
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from log import setup_logging
from middlewares import LoggingMiddleware
from fastapi.middleware.cors import CORSMiddleware
import logging
from Database import engine, log_engine
from producer import get_kafka_producer
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# main.py
'''главный файл проекта'''

# Настроим логирование при запуске приложения
setup_logging()





app = FastAPI(debug=True, redoc_url=None)
producer = get_kafka_producer()
# Регистрируем роутер
app.include_router(auth.home_router)
app.include_router(tasks.task_router) # подключает маршруты из routers/tasks.py.
app.include_router(tasks.subtask_router)  # Регистрируем роутер для подзадач
app.include_router(tasks.task_js_router) # Регистрируем роутер для html файлов с js
app.include_router(tasks.varinant_router) # Регистрируем роутер для html файлов с jinja2
app.include_router(tasks.subject_router)  # маршрут для предметов
app.include_router(students.students_router)  # Регистрируем роутер для студентов
app.include_router(students.students_subtasks_router) # Регистрируем роутер для задач студентов
app.include_router(auth.auth_router) # Регистрируем роутер Аутентификации
app.include_router(auth.admin_router)
app.add_middleware(LoggingMiddleware) # Middleware для логов всех запросов
#app.include_router(files.router)

#app.include_router(web_auth.router) # подключаем home
#app.mount("/static", StaticFiles(directory="Templates/Static"), name="static") # для CSS файлов
app.mount("/Uploads", StaticFiles(directory="Uploads"), name="uploads") # для файлов
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Путь до билд-фронта
frontend_path = os.path.join(os.path.dirname(__file__), "..", "Client", "dist")
# Подключаем статику
app.mount("/assets", StaticFiles(directory=os.path.join(frontend_path, "assets")), name="assets")

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

# корректное завершение соединения kafka
@app.on_event("shutdown")
def shutdown_event():
    producer.close()

# Главная страница
@app.get("/")
def read_index():
    return FileResponse(os.path.join(frontend_path, "index.html"))

# Обработка остальных маршрутов (если SPA)
@app.get("/{full_path:path}")
def read_spa(full_path: str):
    return FileResponse(os.path.join(frontend_path, "index.html"))


# Перенаправление на страницу логина при открытии корня (Основной адрес сайта)
'''@app.get("/")
def read():
    return RedirectResponse(url="/home/login_in/")'''

"""Swagger
@app.get("/docs", dependencies=[Depends(get_swagger_user)])
async def get_documentation():
    return get_swagger_ui_html(openapi_url=app.openapi_url, title="Документация API")

@app.get("/redoc", dependencies=[Depends(get_swagger_user)])
async def get_redoc_documentation():
    return get_redoc_html(openapi_url=app.openapi_url, title="Документация API")
"""
"""запуск сервера"""
if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=9000)