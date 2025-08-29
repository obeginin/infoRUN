from Service.Crud import general  # импорт твоей функции вставки
from utils.config import UPLOAD_SOLUTION_DIR, UPLOAD_FILES_DIR
from Celery_worker.email_worker import celery_app, SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, FROM_EMAIL, SessionLocal
import os
import shutil
import json
from pathlib import Path
from sqlalchemy import text

import logging
logger = logging.getLogger(__name__)

@celery_app.task(bind=True, name="save_subtask_files", max_retries=3)
def save_subtask_files_task(self, temp_record_id: int):
    logging.info(f"[CELERY WORKER]: запуск функции save_subtask_files_task c temp_record_id:{temp_record_id}")
    db = SessionLocal()
    try:
        # 1. Получаем запись с временными файлами
        temp_record = db.execute(text(
            "SELECT * FROM SubTaskTemp WHERE ID = :id"),
            {"id": temp_record_id}
        ).mappings().first()
        if not temp_record:
            return

        subtask_id = temp_record["SubTaskID"]
        logging.info(f"[CELERY WORKER]: subtask_id: {subtask_id}")
        # --- Сохраняем файлы с решением ---
        solution_files = json.loads(temp_record["SolutionTempPath"] or "[]")
        for idx, temp_path in enumerate(solution_files):
            ext = temp_path.split('.')[-1]
            filename = f"sol_subtask_{subtask_id}_{idx + 1}.{ext}"
            final_path = str(Path(UPLOAD_SOLUTION_DIR) / filename)
            shutil.move(temp_path, final_path)

            insert_query = """
                INSERT INTO SubTaskSolutions (SubTaskID, FileName, FilePath)
                VALUES (:SubTaskID, :FileName, :FilePath)
            """
            logging.info(f"[CELERY WORKER]: сохраняем файл с решеним: {final_path}")
            general.run_query_insert(db, insert_query, {"SubTaskID": subtask_id, "FileName": filename, "FilePath": final_path})

        # --- Сохраняем дополнительные файлы ---
        extra_files = json.loads(temp_record["FilesTempPaths"] or "[]")
        for idx, temp_path in enumerate(extra_files):
            ext = temp_path.split('.')[-1]
            filename = f"f_subtask_{subtask_id}_{idx + 1}.{ext}"
            final_path = str(Path(UPLOAD_FILES_DIR) / filename)
            shutil.move(temp_path, final_path)

            insert_query = """
                INSERT INTO SubTaskFiles (SubTaskID, FileName, FilePath)
                VALUES (:SubTaskID, :FileName, :FilePath)
            """
            logging.info(f"[CELERY WORKER]: сохраняем дополнительный файл: {final_path}")
            general.run_query_insert(db, insert_query, {"SubTaskID": subtask_id, "FileName": filename, "FilePath": final_path})

        db.commit()

    except Exception as exc:
        db.rollback()
        raise self.retry(exc=exc, countdown=5)
    finally:
        db.close()

