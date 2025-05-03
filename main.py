from fastapi import FastAPI, Depends
from Routers import tasks,students  # Импортируем роутер задач
from fastapi.staticfiles import StaticFiles

app = FastAPI()
# Регистрируем роутер
app.include_router(tasks.task_router) # подключает маршруты из routers/tasks.py.
app.include_router(tasks.subtask_router)  # Регистрируем роутер для подзадач
app.include_router(tasks.task_js_router) # Регистрируем роутер для html файлов с js
app.include_router(tasks.task_ji_router) # Регистрируем роутер для html файлов с jinja2
app.include_router(students.students_router)  # Регистрируем роутер для студентов
app.include_router(students.students_subtasks_router) # Регистрируем роутер для задач студентов

app.mount("/static", StaticFiles(directory="Templates/Static"), name="static") # для файлов

'''Эндпоинт: Корень сайта (/)'''
@app.get("/")
def read_root():
    return {"message": "Connected to DB successfully!✅"}

