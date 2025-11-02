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
from sqlalchemy.ext.asyncio import AsyncSession
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


# TODO переведен на асинхронный postgres

@subtask_router.post("/create",operation_id = 'SubtasksCreate', summary="Создание задачи с файлами и блоками",
                     description="""Создает задачу с текстовыми, графическими и другими блоками.  
Поддерживает прикрепление файлов через multipart/form-data.  
возвращает `files_blocks` - количество вставленных файлов с изображением задачи  
`files_solution` - количество вставленных файлов с решением задачи  
`files` - количество вставленных дополнительных файлов к задачи""")
async def create_subtask(
        task_id: int = Form(None, description="Task_id категории"),
        subtask_number: str = Form(None, description="Номер задачи в категории"),
        variant_id: int = Form(None, description="ID варианта (если есть)"),
        blocks: str = Form(...,description='JSON список блоков: [{"type":"text","content":"Текст"},{"type":"image","content":"image.png"}]'),
        files_blocks: List[UploadFile] = File([], description="Список файлов для блоков"),
        answer: str = Form(None, description="Ответ на задачу"),
        files_solution: List[UploadFile] = File([], description="Список файлов для решения"),
        files_extra: List[UploadFile] = File([], description="Список дополнительных файлов к задаче"),
        db: AsyncSession = Depends(get_db),
        current_student=Depends(auth.permission_required("create_tasks"))
):
    logger.debug(f"Пользователь {current_student.Login} отправил запрос на создание новой задачи")
    logging.debug(f"Параметры: TaskID={task_id}, SubTaskNumber={subtask_number}, VariantID={variant_id}, Answer={answer}")
    logging.debug(f"[SUBTASKS] Blocks (raw)={blocks}")

    # парсим строку JSON
    try:
        blocks_json = json.loads(blocks)  # преобразует строку JSON в Python-объект:
        if not isinstance(blocks_json, list):
            raise ValueError("blocks должен быть списком")
        blocks_list = [Block(**b) for b in blocks_json]
        if not blocks_list:
            raise ValueError("Список блоков не может быть пустым")
    except (json.JSONDecodeError, ValueError) as e:
        logging.exception(f"Ошибка с блоками: {str(e)}")
        raise errors.bad_request(message="Ошибка с блоками")

    # дополнительная проверка файлов

    logger.info(f"FILES BLOCKS: {[file.filename for file in files_blocks]}")
    await subtasks_crud.log_and_validate_files(files_blocks, 'с изображением')
    logger.info(f"FILES SOLUTION: {[file.filename for file in files_solution]}")
    await subtasks_crud.log_and_validate_files(files_extra, 'с решением')
    logger.info(f"FILES EXTRA: {[file.filename for file in files_extra]}")
    await subtasks_crud.log_and_validate_files(files_extra, 'дополнительные')


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
        logging.exception(f"Ошибка при создании задачи: {str(e)}")
        raise errors.bad_request(message=f"Ошибка при создании задачи")


    # 4 Создаем новую задачу
    try:
        result = await subtasks_crud.create_subtask(db, subtask_obj, files_blocks)
        subtask_id = result["SubTaskID"]
        logging.info(f"[SUBTASKS] Пользователь {current_student.Login} успешно создал задачу id={subtask_id}")

        # логируем в Kafka

        send_log(
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
        logger.info(f"Пользователь {current_student.Login} создал новую задачу с subtask_id={subtask_id}")
        return {"status": "success", "data": result}

    except Exception as e:
        logging.exception(f"Не удалось создать задачу: {str(e)}")
        raise errors.internal_server(message="Не удалось создать задачу")




@subtask_router.put(
    "/update/{subtask_id}",
    operation_id = 'SubtasksUpdateSubtaskID',
    summary="Полное обновление задачи с блоками и файлами",
    description="Заменяет старые значения на новые!(старые файлы удаляются и записываются новые)."
)
async def full_update_subtask(
    subtask_id: int,
    task_id: int = Form(None, description="Task_id категории"),
    subtask_number: str = Form(None, description="Номер задачи в категории"),
    variant_id: int = Form(None, description="ID варианта (если есть)"),
    blocks: str = Form(...,description='JSON список блоков: [{"type":"image","content":"image.png"},{"type":"text","content":"Текст"}]'),
    files_blocks: Optional[List[UploadFile]] = File(None, description="Файлы для блоков"),
    answer: str = Form(None, description="Ответ на задачу"),
    files_solution: Optional[List[UploadFile]] = File(None, description="Файлы решения"),
    files_extra: Optional[List[UploadFile]] = File(None, description="Дополнительные файлы"),
    db: AsyncSession = Depends(get_db),
    current_student=Depends(auth.permission_required("edit_tasks"))
):
    logger.debug(f"Пользователь {current_student.Login} отправил запрос на изменение задачи с subtask_id={subtask_id}")
    logger.debug(f"Параметры запроса (пришло с фронта): "
        f"task_id={task_id}, "
        f"subtask_number={subtask_number}, "
        f"variant_id={variant_id}, "
        f"answer={answer}")

    subtask = await subtasks_crud.view_all_subtasks(db, params={"subtask_id": subtask_id}, mode='mappings_first')
    logger.debug(f"subtask:{subtask} ===")
    if not subtask:
        logger.warning(f"Подзадача ID={subtask_id} не найдена в базе")
        return {"success": False, "message": "Подзадача не найдена"}
    # TODO избавиться от try except  нормально обрабатывать ошибки
    try:
        # Парсим блоки
        try:
            blocks_json = json.loads(blocks)
            blocks_list = [Block(**b) for b in blocks_json]
        except Exception as e:
            logging.exception(f"Ошибка с блоками: {str(e)}")
            raise errors.bad_request(message="Ошибка с блоками")



        # Создаем объект для передачи в crud
        subtask_data = SubTaskCreate(
            TaskID=task_id,
            SubTaskNumber=subtask_number,
            VariantID=variant_id,
            Answer=answer,
            Blocks=blocks_list,
            Creator=current_student.Login
        )
        logger.debug(f"[SUBTASKS] === 0")
        # Обновляем подзадачу и файлы
        result = await subtasks_crud.update_subtask(db, subtask_data, files_blocks, files_solution, files_extra, subtask_id)
        logger.debug(f"[SUBTASKS] === 1")
        # Загружаем новые файлы решения через Celery
        if files_solution:
            solution_files_data = await subtasks_crud.prepare_files_data(files_solution, "решение")
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
        logger.debug(f"[SUBTASKS] === 2")
        # Загружаем новые дополнительные файлы через Celery
        if files_extra:
            extra_files_data = await subtasks_crud.prepare_files_data(files_extra, "дополнительный")
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
        logger.debug(f"[SUBTASKS] === 3")
        # Логирование в Kafka

        send_log(
        StudentID=current_student.ID,
        StudentLogin=current_student.Login,
        action="UPDATE_SUBTASK",
        details={
            "SubTaskID": subtask_id,
            "DescriptionEvent": f"Пользователь {current_student.Login} полностью обновил задачу ID={subtask_id}"
        }
        )
        logger.info(f"Пользователь {current_student.Login} обновил задачу с subtask_id={subtask_id}")
        return {"status": "success", "data": result}

    except Exception as e:
        logging.exception(f"Ошибка при обновлении задачи ID={subtask_id} {str(e)}")
        raise errors.internal_server(message=f"Ошибка при обновлении задачи ID={subtask_id}")



@subtask_router.delete(
    "/delete/{subtask_id}",
    operation_id = 'SubtasksDeleteSubtaskID',
    summary="Удаление подзадачи",
    description="Удаляет подзадачу, все её файлы и записи из таблиц"
)
async def delete_subtask(
    subtask_id: int,
    db: AsyncSession = Depends(get_db),
    current_student = Depends(auth.permission_required("delete_tasks"))
):
    logger.debug(f"Пользователь {current_student.Login} отправил запрос на удаление задачи с subtask_id={subtask_id}")

    try:

        subtask = await subtasks_crud.view_all_subtasks(db, params={"subtask_id": subtask_id}, mode='mappings_first')
        if not subtask:
            logger.warning(f"[SUBTASKS_CRUD] Подзадача ID={subtask_id} не найдена в базе")
            return {"success": False, "message": "Подзадача не найдена"}

# TODO надо переделать! чтобы сначала удалялась задача из БД, а потом только файлы!
        # 1. Удаляем все файлы и записи из вспомогательных таблиц
        await subtasks_crud.delete_subtask_files(db,subtask_id)

        # 2. Удаляем саму подзадачу
        await subtasks_crud.delete_subtask_record(db, subtask_id)

        logger.debug(f"Пользователь {current_student.Login} удалил задачу с subtask_id={subtask_id}")
        return {"success": True, "message": f"Подзадача {subtask_id} удалена"}

    except Exception as e:
        logging.exception(f"Ошибка при удалении подзадачи ID={subtask_id} {str(e)}")
        raise errors.internal_server(message=f"Ошибка при удалении подзадачи ID={subtask_id}")





@subtask_router.get(
    "",
    operation_id = 'Subtasks',
    summary="Получение всех задач с блоками и дополнительными файлами",
    description="""Возвращает список всех подзадач с их блоками и прикрепленными файлами.  
        Подзадачи могут фильтроваться по параметрам: SubTaskID, TaskID, SubjectID, VariantID,   
        Search, UploadDate, Creator, сортироваться по любым колонкам и ограничиваться диапазоном   
        через Offset и Limit."""
)
async def get_all_subtasks(
    filters: subtasks_schema.SubTaskQueryParams = Depends(),
    db: AsyncSession = Depends(get_db),
    current_student=Depends(auth.permission_required("view_tasks"))
):
    logger.debug(f"Пользователь {current_student.Login} отправил запрос на получение всех задачи")
    try:
        # 1. Получаем задачу из базы
        subtasks = await subtasks_crud.view_all_subtasks(db, params=filters.dict())
        logger.debug(f"subtasks {subtasks}")
        if not subtasks:
            logger.warning("Задачи не найдены")
            return {"status": "success", "data": []}

        all_data = []
        for subtask in subtasks:
            # 2. Парсим блоки
            try:
                blocks_list = json.loads(subtask["Blocks"]) if subtask.get("Blocks") else []
            except json.JSONDecodeError as e:
                logger.error(f"Ошибка парсинга блоков у задачи ID={subtask.SubTaskID}: {e}")
                blocks_list = []

            # 3. Получаем прикрепленные файлы
            files = await subtasks_crud.view_files(db, subtask.SubTaskID)
            file_list = [
                {"FileID": f["ID"], "FileName": f["FileName"], "FilePath": f["FilePath"]}
                for f in files
            ]
            logger.debug(f"subtasks {subtasks}")

        # 4.Формируем ответ, копируя все поля и заменяя Blocks и Files
            result = dict(subtask)  # копируем весь словарь
            result["Blocks"] = blocks_list
            result["Files"] = file_list

            all_data.append(result)

        send_log(
            StudentID=current_student.ID,
            StudentLogin=current_student.Login,
            action="VIEW_ALL_SUBTASKS",
            details={ "DescriptionEvent": f"Пользователь {current_student.Login} просмотрел все задачи"}
        )
        logger.info(f"Пользователь {current_student.Login} получил {len(all_data)} задач")
        return {"status": "success", "data": all_data}

    except Exception as e:
        logging.exception(f"Ошибка при получении всех задач {str(e)}")
        raise errors.internal_server(message=f"Ошибка при получении всех задач")




@subtask_router.get(
    "/{subtask_id}",
    operation_id = 'SubtasksSubtaskID',
    summary="Получение задачи с блоками и с дополнительными файлами",
    description="Возвращает задачу с текстовыми, графическими и другими блоками, а также прикрепленные файлы."
)
async def get_subtask(
    subtask_id: int,
    db: AsyncSession = Depends(get_db),
    current_student=Depends(auth.permission_required("view_tasks"))
):
    logger.debug(f"Пользователь {current_student.Login} отправил запрос на получение задачи c subtask_id={subtask_id}")

    try:
        # 1. Получаем задачу из базы
        subtask = await subtasks_crud.view_all_subtasks(db, params={"subtask_id": subtask_id}, mode='mappings_first')

        if not subtask:
            logger.warning(f"Задача с ID={subtask_id} не найдена")
            return {"status": "error", "message": "задача не найдена"}

        # 2. Преобразуем блоки из строки JSON, если они в базе хранятся в JSON-формате
        try:
            blocks_list = json.loads(subtask["Blocks"]) if subtask.get("Blocks") else []
        except json.JSONDecodeError as e:
            logger.exception(f"Ошибка парсинга блоков у задачи ID={subtask_id}: {e}")
            blocks_list = []

        # 3. Получаем прикрепленные файлы (если они хранятся в отдельной таблице)
        files = await subtasks_crud.view_files(db,subtask_id)

        file_list = [
            {"FileID": f["ID"], "FileName": f["FileName"], "FilePath": f["FilePath"]}
            for f in files
        ]

        # 4.Формируем ответ, копируя все поля и заменяя Blocks и Files
        result = dict(subtask)  # копируем весь словарь
        result["Blocks"] = blocks_list
        result["Files"] = file_list


        send_log(
            StudentID=current_student.ID,
            StudentLogin=current_student.Login,
            action="VIEW_SUBTASK",
            details={
                "SubTaskID": subtask_id,
                "DescriptionEvent": f"Пользователь {current_student.Login} просмотрел задачу ID={subtask_id}"
            }
        )
        logger.info(f"Пользователь {current_student.Login} получил задачу с subtask_id={subtask_id}")
        logger.debug(f"Данные задачи: {result}")
        return {"status": "success", "data": result}

    except Exception as e:
        logger.exception(f"Ошибка при получении задачи subtask_id={subtask_id} {str(e)}")
        raise errors.internal_server(message=f"Ошибка при получении задачи c subtask_id={subtask_id}")




#@subtask_router.get("/{subtask_id}/solution", summary="Получение файлов с решением")
async def get_solution_files(
    subtask_id: int,
    db: AsyncSession = Depends(get_db),
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

#@subtask_router.get("/{subtask_id}/extra_files", summary="Получение дополнительных файлов для задачи")
async def get_solution_files(
    subtask_id: int,
    db: AsyncSession = Depends(get_db),
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


