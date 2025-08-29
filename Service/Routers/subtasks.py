from Service.Schemas.subtasks import SubTaskCreate, Block #, SubTaskResponse
from Service.config_app import UPLOAD_IMAGE_DIR, UPLOAD_SOLUTION_DIR, UPLOAD_FILES_DIR, TEMPLATES_DIR
from Service.Crud import subtasks
from Service.Crud import auth
from Service.Crud import tasks as task_crud
from Service.Crud import errors
from Service.dependencies import get_db
from Service.Models import Student, SubTaskFiles
from Service.Schemas import tasks
from Service.producer import send_log

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
from Service.config_app import UPLOAD_IMAGE_DIR
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import shutil, os, json
import logging
from pydantic import parse_obj_as
# Routers\tasks.py
''' Маршруты и Эндпоинты'''

load_dotenv() # загружаем переменные из файла .env
logger = logging.getLogger(__name__) # создание логгера для текущего модуля

subtask_router  = APIRouter(prefix="/api/subtasks", tags=["subtasks"])


@subtask_router.get(
    "/{subtask_id}",
    summary="Получение задачи с блоками и файлами",
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
        subtask = await subtasks.view_subtask(db,subtask_id)

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
        files = await subtasks.view_files(db,subtask_id)

        file_list = [
            {"FileID": f["ID"], "FileName": f["FileName"], "FilePath": f["FilePath"]}
            for f in files
        ]


        # 4. Формируем ответ
        response_data = {
            "SubTaskID": subtask.SubTaskID,
            "TaskID": subtask.TaskID,
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


@subtask_router.post("/create", summary="Создание задачи с файлами и блоками", description="""Создает задачу с текстовыми, графическими и другими блоками.  
Поддерживает прикрепление файлов через multipart/form-data.""")
async def create_subtask(
        subject_id: int = Form(..., description="ID предмета"),
        task_id: int = Form(..., description="ID категории"),
        subtask_number: int = Form(None, description="Номер задачи"),
        variant_id: int = Form(None, description="ID варианта (если есть)"),
        variant_name: str = Form("", description="Название варианта"),
        type_variant: str = Form("", description="тип варианта"),
        year_variant: int = Form("", description="год варианта"),
        number_variant: str = Form("", description="специальный номер варианта"),
        difficulty_level: str = Form("", description="Сложность варианта"),
        comment: str = Form("", description="Комменатрий"),
        blocks: str = Form(..., description='JSON список блоков: [{"type":"text","content":"Текст"},{"type":"image","content":"image.png"}]'),
        files: List[UploadFile] = File([], description="Список файлов"),
        answer: str = Form("", description="Ответ на задачу"),
        solution_path: str = Form("", description="Ссылка на решение"),
    db: Session = Depends(get_db),
    current_student=Depends(auth.permission_required("create_tasks"))
):
    logging.info(f"[SUBTASKS] === Поступил запрос на создание задачи ===")
    logging.info(f"[SUBTASKS] TaskID={task_id}, SubTaskNumber={subtask_number}, VariantID={variant_id}")
    logging.info(f"[SUBTASKS] Answer={answer}, SolutionPath={solution_path}")
    logging.info(f"[SUBTASKS] Blocks (raw)={blocks}")
    logging.info(f"[SUBTASKS] Получено файлов: {len(files) if files else 0}")
    for idx, f in enumerate(files or [], start=1):
        logging.info(f"[SUBTASKS] Файл {idx}: {f.filename if f else 'None'}")
    try:
        blocks_json = json.loads(blocks)
        if not isinstance(blocks_json, list):
            raise ValueError("blocks должен быть списком")
        blocks_list = [Block(**b) for b in blocks_json]
        if not blocks_list:
            raise ValueError("Список блоков не может быть пустым")
    except (json.JSONDecodeError, ValueError) as e:
        logging.error(f"Ошибка с блоками: {e}")
        return {"status": "error", "message": str(e)}

    # Проверки файлов
    if files:
        for file in files:
            if not getattr(file, "filename", None):
                logging.warning("Файл без имени пропущен")

    subtask_data = {
        "TaskID": task_id,
        "SubTaskNumber": subtask_number,
        "VariantID": variant_id,
        "Description": description,
        "Answer": answer,
        "SolutionPath": solution_path,
        "Blocks": blocks_list,
        "Creator": current_student.Login
    }

    try:
        subtask_obj = SubTaskCreate(**subtask_data)  # **kwargs распаковка словаря
    except Exception as e:
        logging.error(f"Ошибка при создании SubTaskCreate: {e}")
        return {"status": "error", "message": f"Ошибка создания задачи: {e}"}

    # 4 Вызываем функцию сохранения
    try:
        result = await subtasks.save_subtask(db, subtask_obj, files)
        logging.info(result)
        logging.info(f"Пользователь {current_student.Login} успешно создал задачу id={result["SubTaskID"]}")

        await run_in_threadpool(
            send_log,
            StudentID=current_student.ID,
            StudentLogin=current_student.Login,
            action="CREATE_SUBTASK",
            details={
                "SubTaskID": result["SubTaskID"],
                "DescriptionEvent": f"Пользователь {current_student.Login} успешно создал задачу id={result["SubTaskID"]})"
            }
        )

        return {"status": "success", "data": result}

    except Exception as e:
        logging.exception("Не удалось создать задачу")
        return {"status": "error", "message": str(e)}




# /api/subtasks/files/{file_id}/download   (GET)
'''Скачивание файла прикрепленного к задаче'''
@subtask_router.get("/files/{file_id}/download",  summary="скачивание файла с задачей")
def download_file(file_id: int, db: Session = Depends(get_db)):
    db_file = db.query(SubTaskFiles).filter(SubTaskFiles.ID == file_id).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="Файл не найден")

    return FileResponse(path=db_file.FilePath, filename=db_file.FileName)

'''получение всех файлов задачи'''
@subtask_router.get("/files/{subtask_id}", response_model=List[tasks.FileSchema], summary="роут с получением всех файлов задачи")
def get_files_for_subtask(subtask_id: int, db: Session = Depends(get_db)):
    files = db.execute(text("""
        SELECT ID, FileName, FilePath, UploadDate
        FROM SubTaskFiles
        WHERE SubTaskID = :subtask_id
    """), {"subtask_id": subtask_id}).mappings().all()
    return list(files)



# OLD
# /api/subtasks/create_form/    (POST)
'''Получаем с html страницы данные из формы и запускаем с этими параметрами функцию create_subtask_from_form
в ней добавляем новую задачу в базу и возвращаем номер новой задачи и редиректим на неё
'''
#@subtask_router.post("/create_form", summary="роут с созданием задачи через форму")
def post_subtask_form(
    TaskID: int = Form(...),
    VariantName: str = Form(""),
    Description: str = Form(""),
    Answer: str = Form(""),
    ImageFile: UploadFile = File(None),
    SolutionFile: UploadFile = File(None),
    db: Session = Depends(get_db)
):

    logger.debug("Отправляем форму на добавление задачи")
    result = task_crud.create_subtask_from_form(
        TaskID=TaskID,
        VariantName=VariantName,
        Description=Description,
        Answer=Answer,
        ImageFile=ImageFile,
        SolutionFile=SolutionFile,
        db=db
    )

    if result is None:
        # Если не создалось, выбрасываем ошибку 400 с сообщением
        logger.error("Не удалось создать подзадачу")
        raise HTTPException(status_code=400, detail="Не удалось создать подзадачу")

    return RedirectResponse(f"/tasks/{TaskID}/subtasks{result}", status_code=303)



# /api/subtasks/edit_form/    (POST)
'''Отправка данных с добавленной задачей из формы с html страницы'''
#@subtask_router.post("/edit_form", summary="роут с редактированием задачи через форму")
def post_edit_subtask_form(
    SubTaskID: int = Form(...),
    TaskID: int = Form(...),
    VariantName: str = Form(...),
    SubTaskNumber: int = Form(...),
    Description: str = Form(""),
    Answer: str = Form(""),
    ImageFile: UploadFile = File(None),
    Files: List[UploadFile] = File(...),
    SolutionFile: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    logger.info(f"Редактируем подзадачу ID={SubTaskID}")

    current_variant_id = db.execute(text("SELECT VariantID FROM SubTasks WHERE SubTaskID = :id"),
                                    {"id": SubTaskID}).scalar()
    # Получаем имя текущего варианта
    current_variant_name = db.execute(text("SELECT VariantName FROM Variants WHERE VariantID = :id"),
                                      {"id": current_variant_id}).scalar()
    if VariantName != current_variant_name:
        variant_id = task_crud.get_or_create_variant(db, VariantName)
    else:
        variant_id = current_variant_id

    # Получаем текущую подзадачу из базы
    subtask = task_crud.get_subtasks_id(db,SubTaskID)
    if not subtask:
        logger.warning("Подзадача не найдена")
        return RedirectResponse("/error", status_code=303)

    # Обработка изображения
    image_path = subtask.get('ImagePath')  # по умолчанию оставляем старое изображение
    if ImageFile and ImageFile.filename: # Если был загружен новый файл изображения
        # Сохраняем изображение
        ext = ImageFile.filename.split('.')[-1]
        if image_path:
            # Было изображение — сохраняем под тем же именем
            filename = Path(image_path).name
        else:
            # Не было изображения — создаем имя по логике новой подзадачи
            result = db.execute(
                text("SELECT MAX(SubTaskNumber) FROM SubTasks WHERE TaskID = :task_id"),
                {"task_id": TaskID}
            ).scalar()
            SubTaskNumber = (int(result) if result else 0) + 1
            filename = f"task_{TaskID}_sub_{SubTaskNumber}.{ext}"
            image_path = f"Uploads/images/{filename}"

        filepath = UPLOAD_IMAGE_DIR / filename

        # Сохраняем файл
        with filepath.open("wb") as buffer:
            shutil.copyfileobj(ImageFile.file, buffer)

        logger.info(f"Изображение сохранено как {filepath}")
    else:
        # Файл не загружен
        if not image_path:
            # И раньше не было изображения — путь остаётся пустым
            image_path = None

    # Обработка файла решения
    solution_path = subtask.get('SolutionPath')  # по умолчанию оставляем старое решение

    if SolutionFile and SolutionFile.filename:  # Если был загружен новый файл решения
        # Сохраняем решение
        ext = SolutionFile.filename.split('.')[-1]
        if solution_path:
            # Был файл — сохраняем под тем же именем
            filename = Path(solution_path).name
        else:
            # Не было файла — создаем имя по логике новой подзадачи
            result = db.execute(
                text("SELECT MAX(SubTaskNumber) FROM SubTasks WHERE TaskID = :task_id"),
                {"task_id": TaskID}
            ).scalar()
            SubTaskNumber = (int(result) if result else 0) + 1
            filename = f"solution_task_{TaskID}_sub_{SubTaskNumber}.{ext}"
            solution_path = f"Uploads/solutions/{filename}"

        filepath = UPLOAD_SOLUTION_DIR / filename

        # Сохраняем файл
        with filepath.open("wb") as buffer:
            shutil.copyfileobj(SolutionFile.file, buffer)

        logger.info(f"Решение сохранено как {filepath}")
    else:
        # Файл не загружен
        if not solution_path:
            # И раньше не было файла — путь остаётся пустым
            solution_path = None

    print(f"SubTaskID:{type(SubTaskID)} TaskID:{type(TaskID)} SubTaskNumber:{type(SubTaskNumber)}")
    print(f"Files: {Files}, type: {type(Files)}")
    for f in Files:
        print(f"File: filename={f.filename}, content_type={f.content_type}, type={type(f)}")
    uploaded_files = task_crud.upload_file(SubTaskID, TaskID, SubTaskNumber, Files, db)
    print(uploaded_files)
    subtask_data = tasks.SubTaskUpdate(
        TaskID=TaskID,
        VariantID=variant_id,
        SubTaskNumber=SubTaskNumber,
        Description=Description,
        Answer=Answer,
        ImagePath=image_path,
        SolutionPath=solution_path  # если есть
    )

    updated_subtask = task_crud.update_subtask(SubTaskID, subtask_data, db)
    if updated_subtask is None:
        logger.info("Ошибка при обновлении подзадачи")
        return RedirectResponse("/error", status_code=303)

    return RedirectResponse(f"/tasks/{TaskID}/subtasks{SubTaskID}", status_code=303)
