from sqlalchemy.orm import Session
from sqlalchemy import text
from Schemas.tasks import SubTaskCreate, SubTaskUpdate
from fastapi import HTTPException, UploadFile, File
from typing import Optional
from Models import SubTaskFiles
import shutil
from pathlib import Path
import logging
from typing import List
logger = logging.getLogger(__name__)
# Crud\tasks.py


UPLOAD_IMAGE_DIR = Path("Uploads/images")
UPLOAD_SOLUTION_DIR = Path("Uploads/solutions")
UPLOAD_IMAGE_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_SOLUTION_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_FILES_DIR = Path("Uploads/files")
UPLOAD_FILES_DIR.mkdir(parents=True, exist_ok=True)
''' 
CRUD - основная логика работы запроса
описываем функции, которые выполняют SQL запросы к БД, результат возвращается в виде кортежа
'''

''' функция-SQL запрос к БД для вывода всех задач'''
def get_all_tasks(db: Session):
    query = text("SELECT TaskID, TaskNumber, TaskTitle FROM Tasks ORDER BY TaskNumber")
    result = db.execute(query).fetchall()
    #print(result) # выводит результат запроса в консоль
    return [{"TaskID": row.TaskID, "TaskNumber": row.TaskNumber, "TaskTitle": row.TaskTitle} for row in result]


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
    query = text("SELECT * FROM SubTasks WHERE SubTaskID = :id")
    result = db.execute(query, {"id": subtasks_id}).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail=f"Задача с ID {subtasks_id} не найдена")
    subtask = {
        "SubTaskID": result.SubTaskID,
        "TaskID": result.TaskID,
         "SubTaskNumber": result.SubTaskNumber,
         "ImagePath": result.ImagePath,
         "Description": result.Description,
         "Answer": result.Answer,
         "SolutionPath": result.SolutionPath
    }

    if not result:
        raise HTTPException(status_code=404, detail=f"Задача с ID {subtasks_id} не найдена")
    return subtask

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






''' Добавление новой подзадачи (через форму)'''
def create_subtask_from_form(
        TaskID: int,
        Description: str,
        Answer: str,
        ImageFile: Optional[UploadFile],
        SolutionFile: Optional[UploadFile],
        db: Session
):
    try:
        # Генерация SubTaskNumber — последний + 1
        result = db.execute(
            text("SELECT MAX(SubTaskNumber) FROM SubTasks WHERE TaskID = :task_id"),
            {"task_id": TaskID}
        ).scalar()
        subtask_number = (int(result) if result else 0) + 1

        # Сохраняем файл, если есть
        image_path = None
        if ImageFile and ImageFile.filename:
            ext = ImageFile.filename.split('.')[-1]
            filename = f"task_{TaskID}_sub_{subtask_number}.{ext}"
            filepath = UPLOAD_IMAGE_DIR / filename
            with filepath.open("wb") as buffer:
                shutil.copyfileobj(ImageFile.file, buffer)
            image_path = f"Uploads/images/{filename}"

        solution_path = None
        if SolutionFile and SolutionFile.filename:
            ext = SolutionFile.filename.split('.')[-1]
            filename = f"solution_task_{TaskID}_sub_{subtask_number}.{ext}"
            filepath = UPLOAD_SOLUTION_DIR / filename
            with filepath.open("wb") as buffer:
                shutil.copyfileobj(SolutionFile.file, buffer)
            solution_path = f"Uploads/solutions/{filename}"

        # Вставка подзадачи в БД
        insert_query = (
            text("""
                INSERT INTO SubTasks (TaskID, SubTaskNumber, ImagePath, SolutionPath, Description, Answer)
                OUTPUT INSERTED.SubTaskID
                VALUES (:task_id, :subtask_number, :image_path, :solution_path, :description, :answer)
            """))
        result = db.execute(insert_query, {
            "task_id": TaskID,
            "subtask_number": subtask_number,
            "image_path": image_path,
            "solution_path": solution_path or "",
            "description": Description,
            "answer": Answer,
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
                SubTaskNumber = :subtask_number,
                ImagePath = :image_path,
                Description = :description,
                Answer = :answer,
                SolutionPath = :solution_path
            WHERE SubTaskID = :subtask_id
        """)
    db.execute(update_query, {
        "task_id": subtask_data.TaskID,
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
            ext = Path(file.filename).suffix  # с точкой или пустая строка
            filename = f"task_{task_id}_sub_{subtask_number}_file{start_index + idx}{ext}"
            filepath = UPLOAD_FILES_DIR / filename
            file_path = f"{UPLOAD_FILES_DIR.as_posix()}/{filename}"

            with filepath.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            logger.info(f"Saved file {filename}")

            db_file = SubTaskFiles(
                SubTaskID=subtask_id,
                FileName=file.filename,
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


# /subtasks/files/{file_id}/download   (GET)
'''Скачивание файла прикрепленного к задаче'''
'''@subtask_router.get("/files/{file_id}/download")
def download_file(file_id: int, db: Session = Depends(get_db)):
    db_file = db.query(TaskFile).filter(TaskFile.ID == file_id).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="Файл не найден")

    return FileResponse(path=db_file.FilePath, filename=db_file.FileName)'''