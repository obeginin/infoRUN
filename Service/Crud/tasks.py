from Service.config import UPLOAD_IMAGE_DIR, UPLOAD_SOLUTION_DIR, UPLOAD_FILES_DIR
from Service.Schemas.tasks import SubTaskCreate, SubTaskUpdate
from Service.Models import SubTaskFiles

from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException, UploadFile, File
from typing import Optional, List
from pathlib import Path
import shutil
import logging


# Crud\tasks.py
''' 
CRUD - основная логика работы запроса
Основные функции для задач
'''


logger = logging.getLogger(__name__) # создание логгера для текущего модуля



# возможно не нужно! перенес логику в роут
''' функция-SQL запрос к БД для вывода всех задач'''
def get_all_tasks(db: Session):
    query = text("SELECT TaskID, TaskNumber, TaskTitle FROM Tasks ORDER BY TaskNumber")
    result = db.execute(query).fetchall()
    #print(result) # выводит результат запроса в консоль
    return [{"TaskID": row.TaskID, "TaskNumber": row.TaskNumber, "TaskTitle": row.TaskTitle} for row in result]

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


''' Добавление новой подзадачи (по API)'''
def create_subtask(db: Session, subtask_data: SubTaskCreate):
# Запрос на проверку наличия категории
    check_query = text("SELECT 1 FROM Tasks WHERE TaskID = :task_id")
    result = db.execute(check_query, {"task_id": subtask_data.TaskID}).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail=f"Категория с ID {subtask_data.TaskID} не найдена")

#Запрос на добавление задач
    query = text("""
        INSERT INTO SubTasks (TaskID, SubTaskNumber, ImagePath, Description, Answer, SolutionPath)
        OUTPUT INSERTED.SubTaskID
        VALUES (:TaskID, :SubTaskNumber, :ImagePath, :Description, :Answer, :SolutionPath)
    """)
    result = db.execute(query, {
        "TaskID": subtask_data.TaskID,
        "SubTaskNumber": subtask_data.SubTaskNumber,
        "ImagePath": subtask_data.ImagePath,
        "Description": subtask_data.Description,
        "Answer": subtask_data.Answer,
        "SolutionPath": subtask_data.SolutionPath,
    })

    new_id = result.scalar() # возвращаем id добавленной задачи
    return {"SubTaskID": new_id}


''' Проверка на наличие или добавление варианта'''
def get_or_create_variant(db: Session, VariantName: str) -> int:
    variant = db.execute(
        text("SELECT VariantID FROM Variants WHERE VariantName = :name"),
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
            filepath = UPLOAD_IMAGE_DIR / filename
            with filepath.open("wb") as buffer:
                shutil.copyfileobj(ImageFile.file, buffer)
            image_path = f"Uploads/images/{filename}"
            logger.debug(f"filepath: {filepath}")
            logger.debug(f"image_path: {image_path}")

        solution_path = None
        if SolutionFile and SolutionFile.filename:
            ext = SolutionFile.filename.split('.')[-1]
            filename = f"solution_task_{TaskID}_sub_{subtask_number}.{ext}"
            sol_filepath = UPLOAD_SOLUTION_DIR / filename
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



''' Редактирование подзадачи (через форму)'''
def update_subtask(
        SubTaskID: int,
        subtask_data: SubTaskUpdate,
        db: Session
):
    subtask = get_subtasks_id(db, SubTaskID)
    if subtask is None:
        logger.info("Нет такой задачи")
        return None  # Или выбросить исключение

    update_query = text("""
            UPDATE SubTasks SET
                TaskID = :task_id,
                VariantID = :VariantID,
                SubTaskNumber = :subtask_number,
                ImagePath = :image_path,
                Description = :description,
                Answer = :answer,
                SolutionPath = :solution_path
            WHERE SubTaskID = :subtask_id
        """)
    db.execute(update_query, {
        "task_id": subtask_data.TaskID,
        "VariantID": subtask_data.VariantID,
        "subtask_number": subtask_data.SubTaskNumber,
        "image_path": subtask_data.ImagePath,
        "description": subtask_data.Description,
        "answer": subtask_data.Answer,
        "solution_path": subtask_data.SolutionPath,
        "subtask_id": SubTaskID
    })
    db.commit()

    return get_subtasks_id(db, SubTaskID)
'''def get_all_tasks(db: Session):
    return db.query(Task).order_by(Task.TaskNumber).all()'''


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
            filepath = UPLOAD_FILES_DIR / filename
            file_path = f"{UPLOAD_FILES_DIR.as_posix()}/{filename}"
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


