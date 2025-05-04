from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from Schemas.tasks import TaskRead, SubTaskRead, SubTaskCreate
from Crud import tasks as task_crud
from dependencies import get_db
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from Models import Task

task_router  = APIRouter(prefix="/tasks", tags=["tasks"])
subtask_router  = APIRouter(prefix="/subtasks", tags=["subtasks"])
task_js_router = APIRouter(prefix="/js", tags=["js"])
task_ji_router = APIRouter(prefix="/html", tags=["html"])
templates = Jinja2Templates(directory="templates")

# /tasks
''' Эндпоинт: Получить список задач (/tasks/api/)'''
@task_router.get("/api/", response_model=list[TaskRead],summary="Получить список задач")
def read_all_tasks(db: Session = Depends(get_db)):
    return task_crud.get_all_tasks(db)

''' Эндпоинт: Получить задачу по id (/tasks/api/{task_id})'''
@task_router.get("/api/{task_id}", response_model=list[TaskRead],summary="Получить задачу по id")
def read_tasks_id(task_id: int, db: Session = Depends(get_db)):
    return task_crud.get_task_id(db, task_id)

# /subtasks
''' Эндпоинт: Получить список всех столбцов таблицы (/subtasks/api/)'''
@subtask_router.get("/api/columns", response_model=list[str],summary="Получить список всех столбцов таблицы 'subtasks'")
def get_task_columns(db: Session = Depends(get_db)):
    return task_crud.get_columns_of_table(db)

''' Эндпоинт: Получить список всех подзадач (/subtasks/api/)'''
@subtask_router.get("/api/", response_model=list[SubTaskRead],summary="Получить список всех подзадач")
def read_all_subtasks(db: Session = Depends(get_db)):
    return task_crud.get_all_subtasks(db)

''' Эндпоинт: Получить подзадачу по subtask_id (/subtasks/api/{subtask_id})'''
@subtask_router.get("/api/{subtask_id}", response_model=list[SubTaskRead],summary="Получить подзадачу по id")
def read_subtasks_subtask_id(subtask_id: int, db: Session = Depends(get_db)):
    return task_crud.get_subtasks_id(db, subtask_id)

''' Эндпоинт: Получить подзадачу по TaskID (/subtasks/api/TaskID/{task_id})'''
@subtask_router.get("/api/TaskID/{task_id}", response_model=list[SubTaskRead],summary="Получить подзадачу по TaskID")
def read_subtasks_TaskID(task_id: int, db: Session = Depends(get_db)):
    return task_crud.get_subtasks_TaskID(db, task_id)

# /subtasks (POST)
''' Эндпоинт: Добавление подзадачи POST /tasks/api/'''
@subtask_router.post("/api/", status_code=201,summary="Добавление подзадачи")
def create_new_subtask(subtask: SubTaskCreate, db: Session = Depends(get_db)):
    new_id = task_crud.create_subtask(db, subtask)
    return {"message": "Подзадача успешно добавлена", "SubTaskID": new_id}


# /tasks
'''Подключаем html файл с JavaScript'''
@task_js_router.get("/", response_class=HTMLResponse)
def list_tasks_js(request: Request):
    return templates.TemplateResponse("tasks_js.html", {"request": request})

# /subtasks по task_id
@task_js_router.get("/{task_id}", response_class=HTMLResponse)
def read_subtasks_TaskID(request: Request, task_id: int):
    return templates.TemplateResponse("subtask.html", {"request": request, "task_id": task_id})

# /task по subtask_id
@task_js_router.get("/TaskID/{subtask_id}", response_class=HTMLResponse)
def read_subtasks_subtask_id(request: Request, subtask_id: int):
    return templates.TemplateResponse("task.html", {"request": request, "subtask_id": subtask_id})



# /html
'''Подключаем html файл с Jinja2'''
@task_ji_router.get("/", response_class=HTMLResponse)
def list_tasks_html(request: Request, db: Session = Depends(get_db)):
    tasks = db.query(Task).all() # передаю модель Task в запрос
    return templates.TemplateResponse("tasks_jinja.html", {"request": request, "tasks": tasks})

