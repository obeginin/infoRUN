from Service.config_app import UPLOAD_IMAGE_DIR, UPLOAD_SOLUTION_DIR, UPLOAD_FILES_DIR, LOG_FILE
from Service.Schemas.tasks import SubTaskCreate, SubTaskUpdate
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

setup_logging(log_file=LOG_FILE)
async def save_subtask(db, subtask_obj, files: list):
        #blocks_json = json.dumps([b.dict() for b in subtask_obj.Blocks])
    logging.info("=== Запуск save_subtask ===")
    logging.info(f"Полученные данные подзадачи: {subtask_obj}")
    logging.info(f"Количество загруженных файлов: {len(files)}")
    for f in files:
        logging.info(f"Файл: {f.filename}")
    try:

        insert_subtask_query = """
            INSERT INTO SubTasks
                (TaskID, SubTaskNumber, VariantID, Answer, SolutionPath, Creator)
            OUTPUT INSERTED.SubTaskID
            VALUES (:TaskID, :SubTaskNumber, :VariantID,  :Answer, :SolutionPath, :Creator)
            """
        params_1 = {
            "TaskID": subtask_obj.TaskID,
            "SubTaskNumber": subtask_obj.SubTaskNumber,
            "VariantID": subtask_obj.VariantID,
            "Answer": subtask_obj.Answer,
            "SolutionPath": subtask_obj.SolutionPath,
            "Creator": subtask_obj.Creator
        }
        logging.info(f"Параметры для вставки подзадачи: {params_1}")
        subtask_id = general.run_query_insert(
            db,
            insert_subtask_query,
            params_1,
            return_id=True
        )

        logging.info(f"Подзадача вставлена с ID {subtask_id}")

        # Сохраняем файлы и создаем записи в SubTasksImages
        file_url_map = {}
        for idx, file in enumerate(files or [], start=0):  # start=0 для удобства
            ext = file.filename.split('.')[-1]
            filename = f"subtask_{subtask_id}_{idx + 1}.{ext}"
            full_path = os.path.join(UPLOAD_IMAGE_DIR, filename)

            try:
                with open(full_path, "wb") as f:
                    shutil.copyfileobj(file.file, f)
                logging.info(f"[SUBTASKS] Файл сохранен: {filename}")
            except Exception as fe:
                logging.exception(f"[SUBTASKS] Ошибка при сохранении файла {file.filename}")
                continue

            file_url_map[idx] = f"/{full_path}"


            # Вставка в SubTasksImages
            insert_file_query = """
               INSERT INTO SubTasksImages (SubTaskID, FileName, FilePath)
               VALUES (:SubTaskID, :FileName, :FilePath)
               """
            file_params = {
                "SubTaskID": subtask_id,
                "FileName": filename,
                "FilePath": full_path
            }
            logging.info(f"Вставка файла в БД: {file_params}")
            general.run_query_insert(db, insert_file_query, file_params)

        logging.info(f"Обновление блоков. Исходные блоки: {subtask_obj.Blocks}")
        # 3 Обновляем блоки (заменяем пути к картинкам)
        updated_blocks = []
        image_idx = 0

        for block in subtask_obj.Blocks:
            block_dict = block.dict()
            if block_dict["type"] == "image":
                if image_idx < len(files):
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

        #return subtask_id
        return {"SubTaskID": subtask_id, "Blocks": updated_blocks}

    except Exception as e:
        logging.exception("Ошибка при создании подзадачи")
        return {"error": str(e)}
