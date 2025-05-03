from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Schemas.tasks import TaskRead, SubTaskRead, SubTaskCreate
from Crud import tasks as task_crud
from dependencies import get_db


task_router  = APIRouter(prefix="/tasks", tags=["tasks"])
subtask_router  = APIRouter(prefix="/subtasks", tags=["subtasks"])


''' Эндпоинт: Получить список задач (/tasks/)'''
@task_router.get("/", response_model=list[TaskRead],summary="Получить список задач")
def read_all_tasks(db: Session = Depends(get_db)):
    return task_crud.get_all_tasks(db)

''' Эндпоинт: Получить задачу по id (/tasks/{task_id})'''
@task_router.get("/{task_id}", response_model=list[TaskRead],summary="Получить задачу по id")
def read_tasks_id(task_id: int, db: Session = Depends(get_db)):
    return task_crud.get_task_id(db, task_id)

''' Эндпоинт: Получить список всех столбцов таблицы (/subtasks/)'''
@subtask_router.get("/columns", response_model=list[str],summary="Получить список всех столбцов таблицы 'subtasks'")
def get_task_columns(db: Session = Depends(get_db)):
    return task_crud.get_columns_of_table(db)

''' Эндпоинт: Получить список всех подзадач (/subtasks/)'''
@subtask_router.get("/", response_model=list[SubTaskRead],summary="Получить список всех подзадач")
def read_all_subtasks(db: Session = Depends(get_db)):
    return task_crud.get_all_subtasks(db)

''' Эндпоинт: Получить подзадачу по id (/subtasks/{task_id})'''
@subtask_router.get("/id/{subtask_id}", response_model=list[SubTaskRead],summary="Получить подзадачу по id")
def read_subtasks_id(subtask_id: int, db: Session = Depends(get_db)):
    return task_crud.get_subtasks_id(db, subtask_id)

''' Эндпоинт: Получить подзадачу по TaskID (/subtasks/{task_id})'''
@subtask_router.get("/task/{task_id}", response_model=list[SubTaskRead],summary="Получить подзадачу по TaskID")
def read_subtasks_TaskID(task_id: int, db: Session = Depends(get_db)):
    return task_crud.get_subtasks_TaskID(db, task_id)



''' Эндпоинт: Добавление подзадачи POST /tasks/'''
@subtask_router.post("/", status_code=201,summary="Добавление подзадачи")
def create_new_subtask(subtask: SubTaskCreate, db: Session = Depends(get_db)):
    new_id = task_crud.create_subtask(db, subtask)
    return {"message": "Подзадача успешно добавлена", "SubTaskID": new_id}