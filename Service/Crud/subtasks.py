from Service.config_app import UPLOAD_IMAGE_DIR, UPLOAD_SOLUTION_DIR, UPLOAD_FILES_DIR, LOG_FILE
from Service.Models import SubTaskFiles
from Service.Crud import errors,general
from utils.log import setup_logging
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException, UploadFile, File
from typing import Optional
import shutil
import json
import os
from pathlib import Path
import logging
from typing import List
from uuid import uuid4
import base64
from Service.config_app import UPLOAD_IMAGE_DIR

# Crud\subtasks.py

logger = logging.getLogger(__name__)

async def view_subtask(db: Session, subtask_id):
    query = """[SUBTASKS_CRUD] EXEC GetSubtask @SubTaskID = :subtask_id"""
    params = { "[SUBTASKS_CRUD] subtask_id": subtask_id}
    logging.info("[SUBTASKS_CRUD] === Запуск view_subtask ===")
    logging.info(f"[SUBTASKS_CRUD] Получение задачи с id: {subtask_id}")
    return general.run_query_select(
        db=db,
        query=query,
        params=params,
        mode="mappings_first",  # Возвращаем список словарей
        required=False,
        error_message=f"[EXEC] Не удалось получить задачу с id:{subtask_id}"
    )

async def view_files(db: Session, subtask_id):
    query = """select * from SubTaskFiles where SubTaskID = :subtask_id"""
    params = {"subtask_id": subtask_id}
    logging.info("=== Запуск view_files ===")
    logging.info(f"Полученные файлов задачи с id: {subtask_id}")
    return general.run_query_select(
        db=db,
        query=query,
        params=params,
        mode="mappings_all",  # Возвращаем список словарей
        required=False,
        error_message=f"Не удалось получить файлы для задачи с id:{subtask_id}"
    )


async def save_subtask(db, subtask_obj, files_blocks: list):
        #blocks_json = json.dumps([b.dict() for b in subtask_obj.Blocks])
    logging.info("[SUBTASKS_CRUD] === Запуск save_subtask ===")
    logging.info(f"[SUBTASKS_CRUD] Полученные данные подзадачи: {subtask_obj}")
    logging.info(f"[SUBTASKS_CRUD] Количество загруженных файлов с изображением задачи: {len(files_blocks)}")
    #logging.info(f"Количество загруженных файлов с решением задачи: {len(files_solution)}")
    #logging.info(f"Количество загруженных дополнительных файлов к задаче: {len(files)}")
    for f in files_blocks:
        logging.info(f"[SUBTASKS_CRUD] Файл: {f.filename}")
    try:
        # 1 Вставка основной подзадачи
        insert_subtask_query = """
            INSERT INTO SubTasks
                (TaskID, SubTaskNumber, VariantID, Answer, Creator)
            OUTPUT INSERTED.SubTaskID
            VALUES (:TaskID, :SubTaskNumber, :VariantID,  :Answer, :Creator)
            """
        params_1 = {
            "TaskID": subtask_obj.TaskID,
            "SubTaskNumber": subtask_obj.SubTaskNumber,
            "VariantID": subtask_obj.VariantID,
            "Answer": subtask_obj.Answer,
            "Creator": subtask_obj.Creator
        }
        logging.info(f"[SUBTASKS_CRUD] Добавляем строку в таблицу SubTasks с параметрами: {params_1}")
        subtask_id = general.run_query_insert(
            db,
            insert_subtask_query,
            params_1,
            return_id=True
        )
        logging.info(f"[SUBTASKS_CRUD] Подзадача вставлена с ID {subtask_id}")

        # Сохраняем файлы и создаем записи в таблицах
        file_url_map = save_files(db, files_blocks, subtask_id, UPLOAD_IMAGE_DIR, "subtask", "SubTasksImages")
        #file_url_map_2 = save_files(files_solution, UPLOAD_SOLUTION_DIR, "sol_subtask", "SubTaskSolutions")
        #ile_url_map_3 = save_files(files, UPLOAD_FILES_DIR, "f_subtask", "SubTaskFiles")


        logging.info(f"[SUBTASKS_CRUD] Обновление блоков. Исходные блоки: {subtask_obj.Blocks}")
        # 3 Обновляем блоки (заменяем пути к картинкам)
        updated_blocks = []
        image_idx = 0
        for block in subtask_obj.Blocks:
            block_dict = block.dict()
            if block_dict["type"] == "image":
                if image_idx < len(files_blocks):
                    block_dict["content"] = file_url_map[image_idx]
                    image_idx += 1
                else:
                    logging.warning(f"[SUBTASKS_CRUD] Файл для блока не найден: {block_dict}")
            updated_blocks.append(block_dict)

        update_subtask_query = """
                UPDATE SubTasks
                SET Blocks = :Blocks
                WHERE SubTaskID = :SubTaskID
                """
        params_2 = {
            "Blocks": json.dumps(updated_blocks, ensure_ascii=False),
            "SubTaskID": subtask_id
        }
        logging.info(f"[SUBTASKS_CRUD] Обновление подзадачи {subtask_id} с блоками: {params_2}")
        general.run_query_update(db, update_subtask_query, params_2)


        #return subtask_id
        return {
            "SubTaskID": subtask_id,
            "Blocks": updated_blocks,
        }

    except Exception as e:
        logging.exception("Ошибка при создании подзадачи")
        return {"error": str(e)}


'''функция сохранения файлов'''
def save_files(db, files: list, subtask_id: int, folder: str, prefix: str, table: str):
    file_map = {}
    for idx, file in enumerate(files or []):
        ext = file.filename.split('.')[-1]
        filename = f"{prefix}_{subtask_id}_{idx+1}.{ext}"
        full_path = os.path.join(folder, filename)
        try:
            with open(full_path, "wb") as f:
                shutil.copyfileobj(file.file, f)
            logging.info(f"[SUBTASKS_CRUD] Файл сохранен: {filename}")
        except Exception:
            logging.exception(f"[SUBTASKS_CRUD] Ошибка при сохранении файла {file.filename}")
            continue

        file_map[idx] = f"/{full_path}"
        insert_query = f"INSERT INTO {table} (SubTaskID, FileName, FilePath) VALUES (:SubTaskID, :FileName, :FilePath)"
        general.run_query_insert(db, insert_query, {"SubTaskID": subtask_id, "FileName": filename, "FilePath": full_path})

    return file_map

async def prepare_files_data(files: List[UploadFile], file_type: str = "file") -> list:
    """
    Преобразует список UploadFile в сериализуемый список с base64 и логирует каждый файл.

    Args:
        files: список UploadFile
        file_type: строка для логов, например "решение" или "дополнительный"

    Returns:
        list: список словарей с filename, content_type и base64-данными
    """
    logging.info(
        f"[SUBTASKS_CRUD] Запуск функции prepare_files_data")

    files_data = []
    for idx, f in enumerate(files, start=1):
        content = await f.read()
        files_data.append({
            "filename": f.filename,
            "content_type": f.content_type,
            "data": base64.b64encode(content).decode('utf-8')
        })
        logging.info(f"[SUBTASKS_CRUD] {file_type.capitalize()} файл {idx}: {f.filename}, content_type={f.content_type}, size={len(content)} bytes")
    return files_data

# TODO: пока не нужна, но может пригодтся (перенес логику записи в Celery)
'''Логирование и проверка списка файлов'''
def log_and_validate_files(files: Optional[List], label: str):
    count = len(files) if files else 0
    logging.info(f"[SUBTASKS_CRUD] Получено файлов ({label}): {count}")

    for idx, file in enumerate(files or [], start=1):
        filename = getattr(file, "filename", None)
        logging.info(f"[SUBTASKS_CRUD] Файл {idx} ({label}): {filename if filename else 'None'}")
        if not filename:
            logging.warning(f"[SUBTASKS_CRUD] Файл без имени пропущен ({label})")



# TODO: пока не нужна, но может пригодтся (перенес логику записи в Celery)
'''Сохраняет список файлов во временную директорию с уникальными именами'''
async def save_temp_files(files: List[UploadFile], target_dir: Path) -> List[str]:
    """
    files: Список файлов .
    target_dir: Директория, куда будут сохранены файлы.
    return: Список путей к сохранённым файлам.
    """
    saved_paths = []
    target_dir.mkdir(parents=True, exist_ok=True)  # гарантируем, что папка существует
    logging.info(f"[SUBTASKS] Сохраняем файлы в папку: {target_dir.resolve()}")
    for idx, file in enumerate(files or [], start=1):                        # перебираем файлы
        unique_name = f"{uuid4()}_{file.filename}"  # создаем уникальное имя для файла с оригинальным окончанием
        temp_path = target_dir / unique_name        # формируем путь (директория + имя)

        # Сохраняем файл
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        saved_paths.append(str(temp_path))          # путь добавляем в список как строку
        logging.info(f"[SUBTASKS] Файл {idx}: {file.filename} сохранён как {unique_name}")
    logging.info(f"[SUBTASKS] Всего файлов сохранено: {len(saved_paths)}")
    return saved_paths

# TODO: пока не нужна, но может пригодтся (перенес логику записи в Celery)
"""Сохраняет временные пути файлов подзадачи в таблицу SubTaskTemp и возвращает ID записи"""
def save_subtask_temp_record(db: Session, subtask_id: int, student_id: int, temp_solution_paths: list, temp_files_paths: list) -> int:

    logging.info(f"[SUBTASKS_CRUD] Добавляем запись о временных файлах в таблицу SubTaskTemp")
    insert_query = """
        INSERT INTO SubTaskTemp (SubTaskID, StudentID, SolutionTempPath, FilesTempPaths)
        OUTPUT INSERTED.ID
        VALUES (:SubTaskID, :StudentID, :SolutionTempPath, :FilesTempPaths)
    """

    inserted_id = general.run_query_insert(
        db=db,
        query=insert_query,
        params={
            "SubTaskID": subtask_id,
            "StudentID": student_id,
            "SolutionTempPath": json.dumps(temp_solution_paths),
            "FilesTempPaths": json.dumps(temp_files_paths)
        },
        return_id=True
    )

    return inserted_id