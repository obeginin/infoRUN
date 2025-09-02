from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import shutil
import os
from sqlalchemy.orm import Session
from uuid import uuid4
from pathlib import Path

from Service.Crud.tasks import get_subtasks_id
import logging
logger = logging.getLogger(__name__)
# /api/files.py
'''Загрузка файла'''

'''Не используется!!!!!!!'''
'''router = APIRouter(prefix="/files", tags=["Files"])
UPLOAD_DIR = Path("Uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)  # Создаём папку, если нет

@router.post("/upload/{subtask_id}")
async def upload_file(
        subtask_id: int, # указываем id задачи
        file: UploadFile = File(...),
        db: Session = Depends(get_db)):
    logger.debug("Функция загрузки файла. ищем subtask_id")
    # Получаем подзадачу
    subtask = get_subtasks_id(subtask_id)
    if not subtask:
        raise HTTPException(status_code=404, detail="SubTask not found")

    ext = file.filename.split(".")[-1]  # Получаем расширение файла
    unique_name = f"subtask_{subtask.ID}.{ext}"  # Генерируем уникальное имя
    file_path = UPLOAD_DIR / unique_name

    # Проверка на дублирование
    if file_path.exists():
        filename = f"subtask_{subtask.SubTaskID}_{uuid4().hex[:6]}.{ext}"
        file_path = UPLOAD_DIR / filename

# Сохраняем файл по этому пути.
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

# Пример: сохраняем путь к файлу в подзадаче
    subtask.FilePath = str(file_path)
    db.commit()
    logger.debug(f"Имя файла: subtask_subtask_{subtask.ID}.{ext}")
# Возвращаем клиенту имя и путь.
    return {
        "filename": unique_name,
        "path": str(file_path)
    }'''
