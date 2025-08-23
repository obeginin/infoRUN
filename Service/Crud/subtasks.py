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

    try:
        logging.info(f"запуск run_query_insert")
        insert_subtask_query = """
            INSERT INTO SubTasks
                (TaskID, SubTaskNumber, VariantID, Answer, SolutionPath)
            OUTPUT INSERTED.SubTaskID
            VALUES (:TaskID, :SubTaskNumber, :VariantID,  :Answer, :SolutionPath)
            """
        params_1 = {
            "TaskID": subtask_obj.TaskID,
            "SubTaskNumber": subtask_obj.SubTaskNumber,
            "VariantID": subtask_obj.VariantID,


            "Answer": subtask_obj.Answer,
            "SolutionPath": subtask_obj.SolutionPath,

        }

        subtask_id = general.run_query_insert(
            db,
            insert_subtask_query,
            params_1,
            return_id=True
        )

        logging.info(f"Подзадача вставлена с ID {subtask_id}")

        # 2️⃣ Сохраняем файлы и создаем записи в SubTasksImages
        file_url_map = {}
        for idx, file in enumerate(files, start=1):
            original_name = file.filename  # исходное имя для поиска в блоках
            ext = file.filename.split('.')[-1]
            filename = f"subtask_{subtask_id}_{idx}.{ext}"
            full_path = os.path.join(UPLOAD_IMAGE_DIR, filename)

            # Сохраняем файл на диск
            with open(full_path, "wb") as f:
                shutil.copyfileobj(file.file, f)
            logging.info(f"Файл {filename} сохранен")

            file_url_map[original_name] = f"/{full_path}"


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
            general.run_query_insert(db, insert_file_query, file_params)


        # 3 Обновляем блоки (заменяем пути к картинкам)
        updated_blocks = []
        for block in subtask_obj.Blocks:
            block_dict = block.dict()
            if block_dict["type"] == "image":
                original_name = block_dict["content"]
                if original_name in file_url_map:
                    block_dict["content"] = file_url_map[original_name]
                else:
                    logging.warning(f"Файл {original_name} из блока не найден среди загруженных")
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
        general.run_query_update(db, update_subtask_query, params_2)

        #return subtask_id
        return {"SubTaskID": subtask_id, "Blocks": updated_blocks}

    except Exception as e:
        logging.exception("Ошибка при создании подзадачи")
        return {"error": str(e)}
