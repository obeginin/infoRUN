from utils.config import settings
from utils import errors,general

from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException, UploadFile, File
from typing import Optional
import shutil
from pathlib import Path
import logging
from typing import List

# Crud\tasks.py
''' 
CRUD - основная логика работы запроса
Основные функции для задач
'''


logger = logging.getLogger(__name__) # создание логгера для текущего модуля




''' функция-SQL запрос к БД для вывода всех категорий'''
def get_all_tasks(db: Session, subjectID: int | None = None):
    if subjectID is None:
        query = """
                SELECT TaskID, TaskNumber, TaskTitle, SubjectID
                FROM Tasks
                ORDER BY TaskNumber
            """
        params = {}
    else:
        query = """
                SELECT TaskID, TaskNumber, TaskTitle, SubjectID
                FROM Tasks
                WHERE SubjectID = :subjectID
                ORDER BY TaskNumber
            """
        params = {"subjectID": subjectID}
    return general.run_query_select(
        db,
        query= query,
        mode="mappings_all",
        params= params,
        error_message=f"Ошибка при получения категорий из БД"
    )


''' функция-SQL запрос к БД для вывода задачи по id(категории)'''
def get_task_id(db: Session, task_id: int):
    query = f"SELECT * FROM Tasks where TaskID = :task_id"
    params = {"task_id": task_id}
    task = general.run_query_select(
        db,
        query=query,
        mode="mappings_first",
        params=params,
        error_message=f"Ошибка при получении категорий с TaskID:{task_id} из БД"
    )
    if not task:
        raise errors.not_found(message=f"Категория с ID {task_id} не найдена")
    return task









