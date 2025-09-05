from Service.Schemas.subtasks import SubTaskCreate, Block #, SubTaskResponse
from utils.config import settings

from Service.Crud import subtasks as subtasks_crud
from Service.Crud import auth
from Service.Crud import tasks as task_crud
from utils import errors,general
from Service.Database import get_db
from Service.Models import Student
from Service.Schemas import subtasks as subtasks_schema
from Service.producer import send_log
from Service.celery_tasks.celery_app import celery_app

from uuid import uuid4
import base64

from fastapi.concurrency import run_in_threadpool
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
import shutil, os, json
import logging
from pydantic import parse_obj_as
# api\tasks.py
''' Маршруты и Эндпоинты'''

load_dotenv() # загружаем переменные из файла .env
logger = logging.getLogger(__name__) # создание логгера для текущего модуля

subtask_router  = APIRouter(prefix="/api/subtasks", tags=["subtasks"])


@subtask_router.post("/create/", summary="Создание задачи с файлами и блоками",
                     description="""Создает задачу с текстовыми, графическими и другими блоками.  
Поддерживает прикрепление файлов через multipart/form-data.  
возвращает `files_blocks` - количество вставленных файлов с изображением задачи  
`files_solution` - количество вставленных файлов с решением задачи  
`files` - количество вставленных дополнительных файлов к задачи""")
async def create_subtask(
        task_id: int = Form(..., description="ID категории"),
        subtask_number: int = Form(None, description="Номер задачи в категории"),
        variant_id: int = Form(None, description="ID варианта (если есть)"),
        blocks: str = Form(...,description='JSON список блоков: [{"type":"text","content":"Текст"},{"type":"image","content":"image.png"}]'),
        files_blocks: List[UploadFile] = File([], description="Список файлов для блоков"),
        answer: str = Form("", description="Ответ на задачу"),
        files_solution: List[UploadFile] = File([], description="Список файлов для решения"),
        files_extra: List[UploadFile] = File([], description="Список дополнительных файлов к задаче"),
        db: Session = Depends(get_db),
        current_student=Depends(auth.permission_required("create_tasks"))
):
    logging.info(f"[SUBTASKS] === Поступил запрос на создание задачи ===")
    logging.info(
        f"[SUBTASKS] TaskID={task_id}, SubTaskNumber={subtask_number}, VariantID={variant_id}, Answer={answer}")
    logging.info(f"[SUBTASKS] Blocks (raw)={blocks}")

    # парсим строку JSON
    try:
        blocks_json = json.loads(blocks)  # преобразует строку JSON в Python-объект:
        if not isinstance(blocks_json, list):
            raise ValueError("blocks должен быть списком")
        blocks_list = [Block(**b) for b in blocks_json]
        if not blocks_list:
            raise ValueError("Список блоков не может быть пустым")
    except (json.JSONDecodeError, ValueError) as e:
        logging.error(f"Ошибка с блоками: {e}")
        return {"status": "error", "message": str(e)}

    # дополнительная проверка файлов

    logger.info(f"FILES BLOCKS: {[file.filename for file in files_blocks]}")
    subtasks_crud.log_and_validate_files(files_blocks, 'с изображением')
    logger.info(f"FILES SOLUTION: {[file.filename for file in files_solution]}")
    subtasks_crud.log_and_validate_files(files_extra, 'с решением')
    logger.info(f"FILES EXTRA: {[file.filename for file in files_extra]}")
    subtasks_crud.log_and_validate_files(files_extra, 'дополнительные')


    subtask_data = {
        "TaskID": task_id,
        "SubTaskNumber": subtask_number,
        "VariantID": variant_id,
        "Blocks": blocks_list,
        "Answer": answer,
        "Creator": current_student.Login
    }

    try:
        subtask_obj = SubTaskCreate(**subtask_data)  # **kwargs распаковка словаря
    except Exception as e:
        logging.error(f"[SUBTASKS] Ошибка при создании SubTaskCreate: {e}")
        return {"status": "error", "message": f"Ошибка создания задачи: {e}"}

    # 4 Создаем новую задачу
    try:
        result = await subtasks_crud.save_subtask(db, subtask_obj, files_blocks)
        subtask_id = result["SubTaskID"]
        logging.info(f"[SUBTASKS] Пользователь {current_student.Login} успешно создал задачу id={subtask_id}")

        # логируем в Kafka
        await run_in_threadpool(
            send_log,
            StudentID=current_student.ID,
            StudentLogin=current_student.Login,
            action="CREATE_SUBTASK",
            details={
                "SubTaskID": subtask_id,
                "DescriptionEvent": f"Пользователь {current_student.Login} успешно создал задачу id={subtask_id})"
            }
        )
        # 3. Читаем файлы в байты и формируем список для Celery
        solution_files_data = await subtasks_crud.prepare_files_data(files_solution, "решение")
        extra_files_data = await subtasks_crud.prepare_files_data(files_extra, "дополнительный")

        logging.info(f"[SUBTASKS] Отправляем задачу сохранения файлов в Celery")
        # 4. Отправляем в Celery
        # Файлы с решением
        celery_app.send_task(
            "save_subtask_files",
            kwargs={
                "subtask_id": subtask_id,
                "files_data": solution_files_data,
                "folder": str(settings.UPLOAD_SOLUTION_DIR),
                "table": "SubTaskSolutions",
                "prefix": "sol_subtask"
            }
        )

        # Дополнительные файлы
        celery_app.send_task(
            "save_subtask_files",
            kwargs={
                "subtask_id": subtask_id,
                "files_data": extra_files_data,
                "folder": str(settings.UPLOAD_FILES_DIR),
                "table": "SubTaskFiles",
                "prefix": "f_subtask"
            }
        )

        return {"status": "success", "data": result}
    except Exception as e:
        logging.exception("Не удалось создать задачу")
        return {"status": "error", "message": str(e)}

@subtask_router.get(
    "/{subtask_id}",
    summary="Получение задачи с блоками и с дополнительными файлами",
    description="Возвращает задачу с текстовыми, графическими и другими блоками, а также прикрепленные файлы."
)
async def get_subtask(
    subtask_id: int,
    db: Session = Depends(get_db),
    current_student=Depends(auth.permission_required("view_tasks"))
):
    logging.info(f"[SUBTASKS] === Поступил запрос на получение задачи ID={subtask_id} ===")
    try:
        # 1. Получаем задачу из базы
        subtask = await subtasks_crud.view_subtask(db,subtask_id)

        if not subtask:
            logging.warning(f"Задача с ID={subtask_id} не найдена")
            return {"status": "error", "message": "задача не найдена"}

        # 2. Преобразуем блоки из строки JSON, если они в базе хранятся в JSON-формате
        try:
            blocks_list = json.loads(subtask["Blocks"]) if subtask.get("Blocks") else []
        except json.JSONDecodeError as e:
            logging.error(f"Ошибка парсинга блоков у задачи ID={subtask_id}: {e}")
            blocks_list = []

        # 3. Получаем прикрепленные файлы (если они хранятся в отдельной таблице)
        files = await subtasks_crud.view_files(db,subtask_id)

        file_list = [
            {"FileID": f["ID"], "FileName": f["FileName"], "FilePath": f["FilePath"]}
            for f in files
        ]


        # 4. Формируем ответ
        response_data = {
            "SubTaskID": subtask.SubTaskID,
            "SubjectID": subtask.SubjectID,
            "SubjectName": subtask.SubjectName,
            "Description": subtask.Description,
            "TaskID": subtask.TaskID,
            "TaskTitle": subtask.TaskTitle,
            "SubTaskNumber": subtask.SubTaskNumber,
            "VariantID": subtask.VariantID,
            "VariantName": subtask.VariantName,
            "TypeVariant": subtask.TypeVariant,
            "YearVariant": subtask.YearVariant,
            "NumberVarinat": subtask.NumberVarinat,
            "DifficultyLevel": subtask.DifficultyLevel,
            "Comment": subtask.Comment,
            "Creator": subtask.Creator,
            "UploadDate": subtask.UploadDate,
            "Blocks": blocks_list,
            "Files": file_list,
            #"SolutionPath": subtask.SolutionPath,
        }

        logging.info(f"[SUBTASKS] Задача ID={subtask_id} успешно получена")

        await run_in_threadpool(
            send_log,
            StudentID=current_student.ID,
            StudentLogin=current_student.Login,
            action="VIEW_SUBTASK",
            details={
                "SubTaskID": subtask_id,
                "DescriptionEvent": f"Пользователь {current_student.Login} просмотрел задачу ID={subtask_id}"
            }
        )
        return {"status": "success", "data": response_data}

    except Exception as e:
        logging.exception("Ошибка при получении задачи")
        return {"status": "error", "message": str(e)}



@subtask_router.get("/{subtask_id}/solution", summary="Получение файлов с решением")
async def get_solution_files(
    subtask_id: int,
    db: Session = Depends(get_db),
    current_student=Depends(auth.permission_required("view_solutions"))
):

    files = await subtasks_crud.view_solutions_files(db, subtask_id)

    file_list = [
        {"FileID": f["ID"], "FileName": f["FileName"], "FilePath": f["FilePath"]}
        for f in files
    ]
    return {
        "status": "success",
        "files": [
            {
                "id": f.ID,
                "filename": f.FileName,
                "url": f"{f.FilePath}",
                "date": f.UploadDate
            } for f in files
        ]
    }

@subtask_router.get("/{subtask_id}/extra_files", summary="Получение дополнительных файлов для задачи")
async def get_solution_files(
    subtask_id: int,
    db: Session = Depends(get_db),
    current_student=Depends(auth.permission_required("view_tasks"))
):

    files = await subtasks_crud.view_files(db, subtask_id)

    file_list = [
        {"FileID": f["ID"], "FileName": f["FileName"], "FilePath": f["FilePath"]}
        for f in files
    ]
    return {
        "status": "success",
        "files": [
            {
                "id": f.ID,
                "filename": f.FileName,
                "url": f"{f.FilePath}",
                "date": f.UploadDate
            } for f in files
        ]
    }


