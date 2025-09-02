from utils import errors,general
from Service.dependencies import get_db
from Service.Models import Student, SubTaskFiles
from Service.Crud.auth import get_current_student, permission_required
from Service.producer import send_log
from Service.Crud import subjects as subjects_crud
from Service.Schemas import subjects as subjects_schema

from fastapi import APIRouter, Depends, Request, Form, UploadFile, File, Query, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse
from typing import List
from pathlib import Path
from typing import Dict, Optional
import shutil
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import logging

# api\subjects.py


load_dotenv()
logger = logging.getLogger(__name__)

subject_router  = APIRouter(prefix="/api/subjects", tags=["subjects"])


# /api/subjects   (GET) @
@subject_router.get(
    "",
    response_model=subjects_schema.SubjectListResponse,   # указываем какой схеме должны соответствовать данные
    summary="Получить список всех предметов (Информатика, Математика)",
    description="""так же необходимо передавать в заголовке **токен** пользователя"""
)
def read_all_subject(
        db: Session = Depends(get_db),
        current_student = Depends(get_current_student)):     # получаем текущего студента по токену

    subjects = subjects_crud.get_all_subjects(db)  # функция без фильтрации
    logger.warning(f"subjects:{subjects}")

    if not subjects:
        logger.warning(f"Не найдено предметов, Возвращаем пустой список")
        return {
            "message": f"Предметов не найдено",
            "subjects": []
        }

    count = len(subjects)
    send_log(
        StudentID=None,  # Или 0
        StudentLogin=current_student.Login,
        action="GetSubjects",
        details={
            "DescriptionEvent": f"Получение всех предметов",
            "TasksCount": count
        }
    )
    logger.info(f"Пользователь {current_student.Login} запросил список всех предметов")
    return {
        "message": f"Найдено предметов: {count}",
        "count": count,
        "subjects": subjects
    }


# /api/subjects/{subjectID}   (GET) @
@subject_router.get(
    "/{subjectID}",
    response_model=subjects_schema.SubjectRead,   # указываем какой схеме должны соответствовать данные
    summary="Получить предмет по его subjectID ",
    description="""так же необходимо передавать в заголовке **токен** пользователя"""
)
def read_all_subject(
        subjectID: int,
        db: Session = Depends(get_db),
        current_student = Depends(get_current_student)):     # получаем текущего студента по токену

    # ищем предмет по id
    subject = subjects_crud.get_subject_by_id(db, subjectID)
    logger.warning(f"subjects:{subject}")

    if not subject:
        logger.warning(f"Не найден предмет с id: {subjectID}")
        send_log(
            StudentID=None,  # Или 0
            StudentLogin=current_student.Login,
            action="SubjectNotFound",
            details={
                "DescriptionEvent": "Предмет не найден",
                "SubjectID": subjectID
            }
        )
        raise errors.not_found(error="SubjectNotFound", message=f"Предмет с id={subjectID} не найден")


    send_log(
        StudentID=None,  # Или 0
        StudentLogin=current_student.Login,
        action="GetSubjectForID",
        details={
            "DescriptionEvent": f"Получение предмета с id:{subjectID}",
            "SubjectID": subjectID
        }
    )
    logger.info(f"Пользователь {current_student.Login} запросил предмет с id:{subjectID}")
    return subject
