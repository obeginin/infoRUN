from config import TEMPLATES_DIR
from fastapi import FastAPI
from Routers import tasks,students,auth,files  # Импортируем роутер задач
from fastapi.staticfiles import StaticFiles
import uvicorn
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from log import setup_logging
from middlewares import LoggingMiddleware
import logging
# main.py
'''главный файл проекта'''

# Настроим логирование при запуске приложения
setup_logging()



app = FastAPI()
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

# Перенаправление на страницу логина при открытии корня (Основной адрес сайта)
@app.get("/")
def read():
    return RedirectResponse(url="/home/login_in/")

"""запуск сервера"""
if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=9000)