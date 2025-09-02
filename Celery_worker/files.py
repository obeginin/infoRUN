from utils import errors,general
from utils.config import UPLOAD_SOLUTION_DIR, UPLOAD_FILES_DIR
from Celery_worker.worker import celery_app, SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, FROM_EMAIL, SessionLocal
import os
import shutil
import json
from pathlib import Path
from sqlalchemy import text
import os
import logging
import base64
import logging

logger = logging.getLogger(__name__)


@celery_app.task(name="save_subtask_files", max_retries=3)
def save_files_celery(subtask_id: int, files_data: list, folder: str, table: str, prefix: str = "subtask"):
    db = SessionLocal()
    """
    Сохраняет файлы на диск и записывает в таблицу базы данных.

    Args:
        db: SQLAlchemy Session
        subtask_id: ID задачи
        files_data: список словарей вида {'filename': str, 'content_type': str, 'data': base64 str}
        folder: папка для сохранения
        table: таблица для записи информации о файлах
        prefix: префикс для имени файла
    Returns:
        file_map: словарь {index: путь к файлу}
    """
    logging.info(f"[CELERY WORKER]: запуск функции save_files_celery")
    logging.info(f"[CELERY WORKER]: subtask_id:{subtask_id}, folder:{folder}, table:{table}, prefix:{prefix}")
    file_map = {}

    for idx, f in enumerate(files_data, start=1):
        ext = f['filename'].split('.')[-1]
        filename = f"{prefix}_{subtask_id}_{idx}.{ext}"
        full_path = os.path.join(folder, filename)

        try:
            # декодируем base64 обратно в байты
            content_bytes = base64.b64decode(f['data'])
            with open(full_path, "wb") as file_out:
                file_out.write(content_bytes)
            logging.info(f"[CELERY] Файл сохранен: {filename}, size={len(content_bytes)} bytes")
        except Exception:
            logging.exception(f"[CELERY] Ошибка при сохранении файла {f['filename']}")
            continue

        file_map[idx] = f"/{full_path}"

        # сохраняем запись в базу
        insert_query = f"""INSERT INTO {table} (SubTaskID, FileName, FilePath) VALUES (:SubTaskID, :FileName, :FilePath)"""
        general.run_query_insert(
            db,
            insert_query,
            {"SubTaskID": subtask_id, "FileName": filename, "FilePath": full_path}
        )

    return file_map
