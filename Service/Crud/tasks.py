from utils.config import settings
from utils import errors,general

from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException, UploadFile, File
from typing import Optional
import shutil
from pathlib import Path
import logging
from typing import List

# Crud\tasks.py
''' 
CRUD - основная логика работы запроса
Основные функции для задач
'''


logger = logging.getLogger(__name__) # создание логгера для текущего модуля




''' функция-SQL запрос к БД для вывода всех категорий'''
def get_all_tasks(db: Session, subjectID: int | None = None):
    if subjectID is None:
        query = """
                SELECT TaskID, TaskNumber, TaskTitle, SubjectID
                FROM Tasks
                ORDER BY TaskNumber
            """
        params = {}
    else:
        query = """
                SELECT TaskID, TaskNumber, TaskTitle, SubjectID
                FROM Tasks
                WHERE SubjectID = :subjectID
                ORDER BY TaskNumber
            """
        params = {"subjectID": subjectID}
    return general.run_query_select(
        db,
        query= query,
        mode="mappings_all",
        params= params,
        error_message=f"Ошибка при получения категорий из БД"
    )






# возможно не нужно! перенес логику в роут
''' функция-SQL запрос к БД для вывода задачи по id(категории)'''
def get_task_id(db: Session, task_id: int):
    query = text(f"SELECT TaskID, TaskNumber, TaskTitle FROM Tasks where TaskID={task_id}")
    result = db.execute(query).fetchall()
    if not result:
        raise HTTPException(status_code=404, detail=f"Категория с ID {task_id} не найдена")
    return result


''' Вывод всех заголовков столбцов таблицы SubTasks'''
def get_columns_of_table(db: Session, table_name: str = 'SubTasks'):
    query = text(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = :table_name")
    result = db.execute(query, {"table_name": table_name}).fetchall()
    return [row.COLUMN_NAME for row in result]



''' функция-SQL запрос к БД для вывода всех подзадач с сортировкой по категориям'''
def get_all_subtasks(db: Session):
    query = text("SELECT SubTaskID, TaskID, SubTaskNumber, ImagePath, Description, Answer, SolutionPath FROM SubTasks ORDER BY TaskID")
    result = db.execute(query).fetchall()
    subtasks = [
        {"SubTaskID": row.SubTaskID,
        "TaskID": row.TaskID,
         "SubTaskNumber": row.SubTaskNumber,
         "ImagePath": row.ImagePath,
         "Description": row.Description,
         "Answer": row.Answer,
         "SolutionPath": row.SolutionPath}
        for row in result]
    return subtasks


''' функция-SQL для вывода подзадачи по её id (SubTaskID)'''
def get_subtasks_id(db: Session, subtasks_id: int):
    result = db.execute(text(f"""
                SELECT sb.*, v.VariantName, stf.ID AS FileID, stf.FileName, stf.FilePath, stf.UploadDate FROM SubTasks sb
                LEFT JOIN SubTaskFiles stf on stf.SubTaskID=sb.SubTaskID 
                LEFT JOIN Variants v on sb.VariantID = v.VariantID 
                WHERE sb.SubTaskID = :id"""),
                {"id": subtasks_id}).mappings().all()
    if not result:
        raise HTTPException(status_code=404, detail=f"Задача с ID {subtasks_id} не найдена")
    first = result[0]
    subtask = {
        "SubTaskID": first["SubTaskID"],
        "TaskID": first["TaskID"],

        "SubTaskNumber": first["SubTaskNumber"],
        "ImagePath": first["ImagePath"],
        "Description": first["Description"],
        "Answer": first["Answer"],
        "files": [],
    }
    # Добавляем файлы, если есть
    for row in result:
        if row["FileID"] is not None:
            subtask["files"].append({
                "ID": row["FileID"],
                "FileName": row["FileName"],
                "FilePath": row["FilePath"],
                "UploadDate": row["UploadDate"]
            })
    if not first:
        raise HTTPException(status_code=404, detail=f"Задача с ID {subtasks_id} не найдена")
    return subtask


# возможно не нужно! перенес логику в роут
''' функция-SQL для вывода подзадач по типу номеру ЕГЭ'''
def get_subtasks_TaskID(db: Session, task_id: int):
    query = text(f"SELECT * FROM SubTasks where TaskID={task_id} ORDER BY SubTaskNumber")
    result = db.execute(query).fetchall()
    subtasks = [
        {"SubTaskID": row.SubTaskID,
        "TaskID": row.TaskID,
         "SubTaskNumber": row.SubTaskNumber,
         "ImagePath": row.ImagePath,
         "Description": row.Description,
         "Answer": row.Answer,
         "SolutionPath": row.SolutionPath}
        for row in result]
    if not result:
        raise HTTPException(status_code=404, detail=f"Задача с Категорией {task_id} не найдена")
    return subtasks





''' Проверка на наличие или добавление варианта'''
def get_or_create_variant(db: Session, VariantName: str) -> int:
    variant = db.execute(
        text("SELECT VariantID FROM Variants WHERE Name = :name"),
        {"name": VariantName}
    ).scalar()

    if variant:
        return variant
    else:
        # OUTPUT INSERTED.VariantID сразу возвращает новое значнеи VariantID
        result = db.execute(
            text("INSERT INTO Variants (Name) OUTPUT INSERTED.VariantID VALUES (:name)"),
            {"name": VariantName}
        )
        db.commit()
        new_id = result.fetchone()[0]
        return new_id


''' Добавление новой подзадачи (через форму)'''
def create_subtask_from_form(
        TaskID: int,
        VariantName: str,
        Description: str,
        Answer: str,
        ImageFile: Optional[UploadFile],
        SolutionFile: Optional[UploadFile],
        db: Session
):
    logger.debug("Запуск функции create_subtask_from_form")
    logger.debug(f"Передали параметры: TaskID:{TaskID} VariantName:{VariantName} Description: {Description} Answer:{Answer} ImageFile{ImageFile} SolutionFile: {SolutionFile} db:{db}")
    try:
        variant_id = get_or_create_variant(db, VariantName)
        # Генерация SubTaskNumber — последний + 1
        result = db.execute(
            text("SELECT MAX(SubTaskNumber) FROM SubTasks WHERE TaskID = :task_id"),
            {"task_id": TaskID}
        ).scalar()
        subtask_number = (int(result) if result else 0) + 1

        logger.debug(f"Новый номер подзадачи: {subtask_number}")

        # Сохраняем файл, если есть
        image_path = None
        if ImageFile and ImageFile.filename:
            ext = ImageFile.filename.split('.')[-1]
            filename = f"task_{TaskID}_sub_{subtask_number}.{ext}"
            filepath = settings.UPLOAD_IMAGE_DIR / filename
            with filepath.open("wb") as buffer:
                shutil.copyfileobj(ImageFile.file, buffer)
            image_path = f"Uploads/images/{filename}"
            logger.debug(f"filepath: {filepath}")
            logger.debug(f"image_path: {image_path}")

        solution_path = None
        if SolutionFile and SolutionFile.filename:
            ext = SolutionFile.filename.split('.')[-1]
            filename = f"solution_task_{TaskID}_sub_{subtask_number}.{ext}"
            sol_filepath = settings.PLOAD_SOLUTION_DIR / filename
            with sol_filepath.open("wb") as buffer:
                shutil.copyfileobj(SolutionFile.file, buffer)
            solution_path = f"Uploads/solutions/{filename}"
            logger.debug(f"sol_filepath: {sol_filepath}")
            logger.debug(f"solution_path: {solution_path}")
        # Вставка подзадачи в БД
        insert_query = (
            text("""
                INSERT INTO SubTasks (TaskID, SubTaskNumber, ImagePath, SolutionPath, Description, Answer, VariantID)
                OUTPUT INSERTED.SubTaskID
                VALUES (:task_id, :subtask_number, :image_path, :solution_path, :description, :answer, :variant_id)
            """))
        result = db.execute(insert_query, {
            "task_id": TaskID,
            "subtask_number": subtask_number,
            "image_path": image_path,
            "solution_path": solution_path or "",
            "description": Description,
            "answer": Answer,
            "variant_id":variant_id
        }
                   )
        new_SubTaskID = result.scalar_one() # Получаем единственное значение - новый SubTaskID
        db.execute(text("EXEC dbo.AssignSubTasksToStudent"))
        db.commit()
        return new_SubTaskID

    except Exception as e:
        logger.error(f"Ошибка создания подзадачи: {e}")
        db.rollback()
        return None




'''Прикрепление дополнительных файлов к задаче'''
def upload_file(
        subtask_id: int,
        task_id: int,
        subtask_number: int,
        files: List[UploadFile],
        db: Session
):
    #logger.info("Запускаем роут сохранения дополнительного файла")
    '''# берем TaskID и SubTaskNumber
    result_SubTasks = db.execute(
        text("SELECT TaskID, SubTaskNumber FROM SubTasks WHERE SubTaskID = :SubTaskID"),
        {"SubTaskID": subtask_id}
    ).mappings().fetchone()

    if not result_SubTasks:
        raise HTTPException(status_code=404, detail="SubTask not found")'''

    '''task_id = result_SubTasks["TaskID"]
    subtask_number = result_SubTasks["SubTaskNumber"]'''
    try:
        logger.info(
            f"Start uploading files for subtask_id={subtask_id}, task_id={task_id}, subtask_number={subtask_number}")
        start_index = db.execute(
            text("SELECT count(*) FROM SubTaskFiles WHERE SubTaskID = :subtask_id"),
            {"subtask_id": subtask_id}
        ).scalar()
        logger.info(f"Initial file count: {start_index}")

        uploaded_files = []
        for idx, file in enumerate(files, start=1):
            pos = file.file.tell()
            file_content = file.file.read()
            if not file_content:
                logger.warning(f"Пропущен пустой файл: {file.filename}")
                continue
            file.file.seek(pos)  # вернуться обратно
            ext = Path(file.filename).suffix  # с точкой или пустая строка
            filename = f"task_{task_id}_sub_{subtask_number}_file{start_index + idx}{ext}"
            filepath = settings.UPLOAD_FILES_DIR / filename
            file_path = f"{settings.UPLOAD_FILES_DIR.as_posix()}/{filename}"
            filename_db = f"№{task_id}_{start_index + idx}{ext}"
            with filepath.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            logger.info(f"Saved file {filename}")

            db_file = SubTaskFiles(
                SubTaskID=subtask_id,
                FileName=filename_db,
                FilePath=file_path
            )
            db.add(db_file)
            uploaded_files.append(file.filename)

        db.commit()
        logger.info(f"Uploaded files: {uploaded_files}")

        return {"message": "Файлы загружены", "files": uploaded_files}
    except Exception as e:
        logger.error(f"Error during file upload: {e}", exc_info=True)
        raise


