from utils.config import settings
from utils import errors,general

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from fastapi import HTTPException, UploadFile, File
from typing import Optional
import shutil
from pathlib import Path
import logging
from typing import List
logger = logging.getLogger(__name__)
# Crud\tasks.py
''' 
CRUD - основная логика работы запроса
Основные функции для задач
'''


logger = logging.getLogger(__name__) # создание логгера для текущего модуля

# TODO переведен на асинхронный postgres

''' функция-SQL запрос к БД для вывода всех категорий'''
async def get_tasks(db: AsyncSession, subjectID: int | None = None, task_id: int | None = None):
    logger.debug(f"Запуск функции get_all_tasks")
    if task_id is not None:
        query = '''SELECT "TaskID", "TaskNumber", "TaskTitle", "SubjectID" FROM "Tasks" where "TaskID" = : task_id'''
        params = {"task_id": task_id}
    elif subjectID is not None:
        query = '''SELECT "TaskID", "TaskNumber", "TaskTitle", "SubjectID" FROM "Tasks" where "SubjectID" = :subjectID'''
        params = {"subjectID": subjectID}
    else:
        query = '''SELECT "TaskID", "TaskNumber", "TaskTitle", "SubjectID" FROM "Tasks"'''
        params = {}

    return await general.run_query_select(
        db,
        query= query,
        mode="mappings_all",
        params= params,
        error_message=f"Ошибка при получения категорий из БД"
    )

















