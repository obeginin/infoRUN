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
from Service.config_app import UPLOAD_IMAGE_DIR

# Crud\subtasks.py

logger = logging.getLogger(__name__)

async def view_subtask(db: Session, subtask_id):
    query = """EXEC GetSubtask @SubTaskID = :subtask_id"""
    params = { "subtask_id": subtask_id}
    logging.info("=== Запуск view_subtask ===")
    logging.info(f"Получение задачи с id: {subtask_id}")
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


async def save_subtask(db, subtask_obj, files_blocks: list, files_solution: list, files: list):
        #blocks_json = json.dumps([b.dict() for b in subtask_obj.Blocks])
    logging.info("=== Запуск save_subtask ===")
    logging.info(f"Полученные данные подзадачи: {subtask_obj}")
    logging.info(f"Количество загруженных файлов с изображением задачи: {len(files_blocks)}")
    logging.info(f"Количество загруженных файлов с решением задачи: {len(files_solution)}")
    logging.info(f"Количество загруженных дополнительных файлов к задаче: {len(files)}")
    for f in files_blocks:
        logging.info(f"Файл: {f.filename}")
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
        logging.info(f"Добавляем строку в таблицу SubTasks с параметрами: {params_1}")
        subtask_id = general.run_query_insert(
            db,
            insert_subtask_query,
            params_1,
            return_id=True
        )
        logging.info(f"Подзадача вставлена с ID {subtask_id}")

        # Сохраняем файлы и создаем записи в таблицах
        file_url_map = save_files(db, files_blocks, subtask_id, UPLOAD_IMAGE_DIR, "subtask", "SubTasksImages")
        #file_url_map_2 = save_files(files_solution, UPLOAD_SOLUTION_DIR, "sol_subtask", "SubTaskSolutions")
        #ile_url_map_3 = save_files(files, UPLOAD_FILES_DIR, "f_subtask", "SubTaskFiles")


        logging.info(f"Обновление блоков. Исходные блоки: {subtask_obj.Blocks}")
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
                    logging.warning(f"[SUBTASKS] Файл для блока не найден: {block_dict}")
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
        logging.info(f"Обновление подзадачи {subtask_id} с блоками: {params_2}")
        general.run_query_update(db, update_subtask_query, params_2)

        # Возвращаем результат с количеством вставленных файлов
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
        filename = f"{prefix}_{subtask_id}_{idx + 1}.{ext}"
        full_path = os.path.join(folder, filename)
        try:
            with open(full_path, "wb") as f:
                shutil.copyfileobj(file.file, f)
            logging.info(f"Файл сохранен: {filename}")
        except Exception:
            logging.exception(f"Ошибка при сохранении файла {file.filename}")
            continue

        file_map[idx] = f"/{full_path}"
        insert_query = f"INSERT INTO {table} (SubTaskID, FileName, FilePath) VALUES (:SubTaskID, :FileName, :FilePath)"
        general.run_query_insert(db, insert_query, {"SubTaskID": subtask_id, "FileName": filename, "FilePath": full_path})

    return file_map