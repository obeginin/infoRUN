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

# Crud\variants.py


''' функция-SQL запрос к БД для вывода всех вариантов'''
def get_all_variants(db: Session, subjectID: int | None = None, variantID: int | None = None):
    logging.info(f"subjectID={subjectID}, variantID={variantID}")
    if subjectID is None and variantID is None:
        query = """SELECT * FROM Variants"""
        params = {}
        logging.debug(f"1")
    elif not (variantID is None):
        query = """select * from Variants where VariantID = :variantID"""
        params = {"variantID": variantID}
        logging.debug(f"2")
    else:
        query = """SELECT * FROM Variants WHERE SubjectID = :subjectID """
        params = {"subjectID": subjectID}
        logging.debug(f"3")
    return general.run_query_select(
        db,
        query= query,
        mode="mappings_all",
        params= params,
        error_message=f"Ошибка при получения вариантов из БД"
    )