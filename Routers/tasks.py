from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from Schemas.tasks import TaskRead, SubTaskRead, SubTaskCreate
from Crud import tasks as task_crud
from dependencies import get_db
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from Crud.auth import get_current_student
from Models import Student
from Crud.auth import get_current_student, admin_required, verify_password, get_current_student_or_redirect
from fastapi.responses import RedirectResponse
import logging
logger = logging.getLogger(__name__)
# Routers\tasks.py
''' Маршруты и Эндпоинты'''

'''Маршруты добавляются к основному адресу сайта localhost:9000/'''
task_router  = APIRouter(prefix="/tasks", tags=["tasks"])
subtask_router  = APIRouter(prefix="/subtasks", tags=["subtasks"])
task_js_router = APIRouter(prefix="/js", tags=["js"])
#task_ji_router = APIRouter(prefix="/html", tags=["html"])
templates = Jinja2Templates(directory="templates")

# /tasks/api/   (GET)
''' Эндпоинт: Получить список КАТЕГОРИЙ'''
# через @ указываем какому маршруту принадлежит Эндпоинт
@task_router.get(
    "/api/",                    # добавляем префикс к адресу
    response_model=list[TaskRead],   # указываем какой схеме должны соответсвовать данные
    summary="Получить список задач",
    description="Выводит список всех задач имеющихся в БД"
)
def read_all_tasks(db: Session = Depends(get_db)):
    return task_crud.get_all_tasks(db) # качестве результата запукаем функцию get_all_tasks из файла Crud\tasks.py



# /tasks/api/{task_id}  (GET)
''' Эндпоинт: Получить категорию по id'''
@task_router.get("/api/{task_id}", response_model=list[TaskRead],summary="Получить задачу по id")
def read_tasks_id(task_id: int, db: Session = Depends(get_db)):
    return task_crud.get_task_id(db, task_id)


# /tasks/(GET)
'''Вывод страницы html с категориями'''
@task_router.get("/", response_class=HTMLResponse)
def read_subtasks_TaskID(request: Request, current_student = Depends(get_current_student_or_redirect)):
    if isinstance(current_student, RedirectResponse):
        return current_student
    return templates.TemplateResponse("Tasks/tasks.html", {"request": request, "student": current_student})
# /tasks/(GET)

# /tasks/{task_id}  (GET)
'''Подключаем html с конкретной категорией'''
@task_router.get("/{task_id}", response_class=HTMLResponse)
def list_tasks(request: Request, current_student = Depends(get_current_student_or_redirect)):
    if isinstance(current_student, RedirectResponse):
        return current_student
    return templates.TemplateResponse("Tasks/subtask.html", {"request": request, "student": current_student})


'''Вывод страницы html с категориями'''
'''@task_router.get("/", response_class=HTMLResponse)
def read_subtasks_TaskID(request: Request, current_student: Student = Depends(get_current_student)):
    return templates.TemplateResponse("Tasks/tasks.html", {"request": request, "student": current_student})
'''

# /subtasks/api/columns (GET)
''' Эндпоинт: Получить список всех столбцов таблицы subtasks'''
@subtask_router.get("/api/columns", response_model=list[str],summary="Получить список всех столбцов таблицы 'subtasks'")
def get_task_columns(db: Session = Depends(get_db)):
    return task_crud.get_columns_of_table(db)

# /subtasks/api/    (GET)
''' Эндпоинт: Получить список всех подзадач'''
@subtask_router.get("/api/", response_model=list[SubTaskRead],summary="Получить список всех подзадач")
def read_all_subtasks(db: Session = Depends(get_db)):
    return task_crud.get_all_subtasks(db)

# /subtasks/
'''Вызываем html страницу с задачами'''
@subtask_router.get("/", response_class=HTMLResponse)
def list_tasks(request: Request, current_student = Depends(get_current_student_or_redirect)):
    if isinstance(current_student, RedirectResponse):
        return current_student
    return templates.TemplateResponse("Tasks/listTasks.html", {"request": request, "student": current_student})


# /subtasks/api/{subtask_id}    (GET)
''' Эндпоинт: Получить подзадачу по subtask_id'''
@subtask_router.get("/api/{subtask_id}", response_model=SubTaskRead,summary="Получить подзадачу по id")
def read_subtasks_subtask_id(subtask_id: int, db: Session = Depends(get_db)):
    return task_crud.get_subtasks_id(db, subtask_id)

# /subtasks/{subtask_id}   (GET)
'''Вывод страницы html с задачей'''
@subtask_router.get("/{subtask_id}", response_class=HTMLResponse)
def read_subtasks_subtask_id(request: Request, subtask_id: int):
    return templates.TemplateResponse("Tasks/task.html", {"request": request, "subtask_id": subtask_id})



# /subtasks/api/TaskID/{task_id}    (GET)
''' Эндпоинт: Получить подзадачу по TaskID'''
@subtask_router.get("/api/TaskID/{task_id}", response_model=list[SubTaskRead],summary="Получить подзадачу по TaskID")
def read_subtasks_TaskID(task_id: int, db: Session = Depends(get_db)):
    return task_crud.get_subtasks_TaskID(db, task_id)

# /subtasks/api/    (POST)
''' Эндпоинт: Добавление подзадачи'''
@subtask_router.post("/api/", status_code=201,summary="Добавление подзадачи")
def create_new_subtask(subtask: SubTaskCreate, db: Session = Depends(get_db)):
    new_id = task_crud.create_subtask(db, subtask)
    return {"message": "Подзадача успешно добавлена", "SubTaskID": new_id}


# /js   (GET)





# /html
'''Подключаем html файл с Jinja2'''
'''@task_ji_router.get("/", response_class=HTMLResponse)
def list_tasks_html(request: Request, db: Session = Depends(get_db)):
    tasks = db.query(Task).all() # передаю модель Task в запрос
    return templates.TemplateResponse("Tasks/tasks_jinja.html", {"request": request, "tasks": tasks})'''

