from utils.config import settings

from Service.Models import SubTaskFiles
from utils import errors,general

from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException, UploadFile, File
from typing import Optional
import shutil
from pathlib import Path
import logging
from typing import List


logger = logging.getLogger(__name__) # создание логгера для текущего модуля



''' функция-SQL запрос к БД для вывода всех предметов'''
def get_all_subjects(db: Session):
    return general.run_query_select(
        db,
        query= """SELECT * FROM Subjects""",
        mode="mappings_all",
        params= None,
        error_message=f"Ошибка при получения предметов из БД"
    )

''' функция-SQL запрос к БД для вывода определенного предмета'''
def get_subject_by_id(db: Session, subjectID: int):
    return general.run_query_select(
        db,
        query= """SELECT * FROM Subjects WHERE ID = :subjectID""",
        mode="mappings_first",
        params= {"subjectID": subjectID},
        error_message=f"Ошибка при получения предмета из БД"
    )