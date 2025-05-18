from fastapi import FastAPI, Depends
from Routers import tasks,students,auth  # Импортируем роутер задач
from fastapi.staticfiles import StaticFiles
import uvicorn
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

app = FastAPI()
# Регистрируем роутер
app.include_router(tasks.task_router) # подключает маршруты из routers/tasks.py.
app.include_router(tasks.subtask_router)  # Регистрируем роутер для подзадач
app.include_router(tasks.task_js_router) # Регистрируем роутер для html файлов с js
#app.include_router(tasks.task_ji_router) # Регистрируем роутер для html файлов с jinja2
app.include_router(students.students_router)  # Регистрируем роутер для студентов
app.include_router(students.students_subtasks_router) # Регистрируем роутер для задач студентов
app.include_router(auth.auth_router) # Регистрируем роутер Аутентификации
app.include_router(auth.admin_router)
#app.include_router(web_auth.router) # подключаем home
app.mount("/static", StaticFiles(directory="Templates/Static"), name="static") # для CSS файлов
templates = Jinja2Templates(directory="templates") # для


# Перенаправление на страницу логина при открытии корня (Основной адрес сайта)
@app.get("/")
def read():
    return RedirectResponse(url="/home/login_in/")

"""запуск сервера"""
if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=9000, reload=True)