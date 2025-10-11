from utils.config import settings
from Service.Schemas import tasks
from Service.Crud import tasks as task_crud
from utils import errors,general
from Service.Database import get_db
from Service.Models import Student
from Service.Crud.auth import get_current_student, permission_required
from Service.producer import send_log

from fastapi import APIRouter, Depends, Request, Form, UploadFile, File, Query, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.responses import HTMLResponse
from starlette.responses import FileResponse
from typing import List
from pathlib import Path
from typing import Dict, Optional
import shutil

from dotenv import load_dotenv

import logging

# api\tasks.py
''' Маршруты и Эндпоинты'''

load_dotenv() # загружаем переменные из файла .env
logger = logging.getLogger(__name__) # создание логгера для текущего модуля


'''Маршруты добавляются к основному адресу сайта localhost:9000/'''
task_router  = APIRouter(prefix="/api/tasks", tags=["tasks"])


# TODO переведен на асинхронный postgres

# /api/tasks/   (GET) @
''' Эндпоинт: Получить список КАТЕГОРИЙ'''
# через @ указываем какому маршруту принадлежит Эндпоинт
@task_router.get(
    "",                    # добавляем префикс к адресу
    response_model=tasks.TaskListResponse,   # указываем какой схеме должны соответствовать данные
    summary="Получить список категорий (ЕГЭ_1 ЕГЭ_2, и т.д)",
    description="""Если передан параметр **subjectID**, то возвращаются категории только для указанного предмета.  
        Если параметр не передан, возвращаются категории по всем предметам.  
        **subjectID** передается как Query-параметр   
                "`/api/tasks` — все категории"  
                "`/api/tasks?subjectID=10` — категории для предмета с subject ID 10"  
                так же необходимо передавать в заголовке **токен** пользователя
        """
)
async def read_all_tasks(
        subjectID: int | None = Query(None, description="ID предмета для фильтрации"),
        db: AsyncSession = Depends(get_db),
        current_student=Depends(permission_required("view_category"))):     # получаем текущего студента по токену
    tasks = await task_crud.get_tasks(db, subjectID=subjectID)
    if not tasks:
        logger.warning(f"Не найдено категорий")
        raise errors.not_found(message=f"Не найдено категорий")

    count = len(tasks)
    send_log(
        StudentID=None,  # Или 0
        StudentLogin=current_student.Login,
        action="GetTasks",
        details={
            "DescriptionEvent": f"Получение задач по предмету id:{subjectID}",
            "SubjectID": subjectID,
            "TasksCount": count
        }
    )
    logger.info(f"Пользователь {current_student.Login} запросил список категорий для предмета с id:{subjectID}")
    return {
        "message": f"Найдено Категорий: {count}",
        "count": count,
        "tasks": tasks
    }

@task_router.get("/{task_id}", summary="Получить категорию по его task_id")
async def read_task_by_id(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_student=Depends(permission_required("view_category"))
):
    logger.info(f"Пользователь {current_student.Login} запросил категорию с task_id={task_id}")
    task = await task_crud.get_tasks(db, task_id=task_id)
    if not task:
        logger.warning(f"Категория с task_id={task_id} не найдена")
        raise errors.not_found(message=f"Категория с task_id={task_id} не найдено")
    return task[0]


# TODO удалить после полного перехода
# /api/tasks/{id}?subject_id=    (GET) @
#@task_router.get("/{id}", response_model=list[tasks.SubTaskRead],summary="Получить список категорией по выбранному предмету")
async def read_subtasks_TaskID(id: int, subject_id: int = None, db: AsyncSession = Depends(get_db),
                         current_student=Depends(permission_required("view__category"))):
    result = db.execute(text(f"""SELECT * FROM Tasks where SubjectID={subject_id}"""),
                        {subject_id: subject_id}).fetchall()
    subtasks = [dict(row._mapping) for row in result]
    return subtasks


# TODO удалить после полного перехода
# /api/tasks/{task_id}  (GET) @
''' Эндпоинт: Получить категорию по id'''
#@task_router.get("/{task_id}", response_model=list[tasks.TaskRead],summary="Получить задачу по id")
async def read_tasks_id(task_id: int, db: AsyncSession = Depends(get_db),current_student=Depends(permission_required("view__category"))):
    print(type(task_id))
    result = db.execute(text(f"SELECT TaskID, TaskNumber, TaskTitle FROM Tasks where TaskID = :task_id"),{"task_id": task_id}).fetchall()
    subtasks = [dict(row._mapping) for row in result]
    return subtasks



































