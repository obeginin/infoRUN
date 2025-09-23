from utils.config import settings
from Service.Schemas import tasks
from Service.Crud import tasks as task_crud
from utils import errors,general
from Service.dependencies import get_db
from Service.Models import Student
from Service.Crud.auth import get_current_student, permission_required
from Service.producer import send_log

from fastapi import APIRouter, Depends, Request, Form, UploadFile, File, Query, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
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
def read_all_tasks(
        db: Session = Depends(get_db),
        subjectID: int | None = Query(default=None),         # передаем id предмета (не обязательно, тогда выйдут категории всех предметов)
        current_student = Depends(get_current_student)):     # получаем текущего студента по токену

    if subjectID is None:
        tasks = task_crud.get_all_tasks(db)  # функция без фильтрации
    else:
        tasks = task_crud.get_all_tasks(db, subjectID)
    logger.warning(f"tasks:{tasks}")

    if not tasks:
        logger.warning(f"Для предмета с id={subjectID} категорий не найдено")
        return {
            "message": f"Для предмета с id={subjectID} категорий не найдено",
            "tasks": []
        }

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


# /api/tasks/{task_id}  (GET) @
''' Эндпоинт: Получить категорию по id'''
@task_router.get("/{task_id}", response_model=tasks.TaskRead,summary="Получить категорию по Task id")
def read_tasks_id(task_id: int, db: Session = Depends(get_db), current_student = Depends(get_current_student)):
    task = task_crud.get_task_id(db, task_id)
    return task



































