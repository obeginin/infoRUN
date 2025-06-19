from config import UPLOAD_IMAGE_DIR, UPLOAD_SOLUTION_DIR, UPLOAD_FILES_DIR, TEMPLATES_DIR
from fastapi import APIRouter, Depends, Request, Form, UploadFile, File, Query, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from Schemas.tasks import TaskRead, SubTaskRead, SubTaskCreate, SubTaskUpdate, FileSchema
from Crud import tasks as task_crud
from dependencies import get_db
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse
from Crud.auth import get_current_student
from Models import Student, SubTaskFiles
from typing import List
from pathlib import Path
import shutil
from Crud.auth import get_current_student, admin_required, verify_password, get_current_student_or_redirect
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from sqlalchemy import text
from fastapi.encoders import jsonable_encoder
import logging

# Routers\tasks.py
''' Маршруты и Эндпоинты'''

load_dotenv() # загружаем переменные из файла .env
logger = logging.getLogger(__name__) # создание логгера для текущего модуля


'''Маршруты добавляются к основному адресу сайта localhost:9000/'''
task_router  = APIRouter(prefix="/tasks", tags=["tasks"])
subtask_router  = APIRouter(prefix="/subtasks", tags=["subtasks"])
task_js_router = APIRouter(prefix="/js", tags=["js"])
varinant_router = APIRouter(prefix="/variants", tags=["variants"])
#task_ji_router = APIRouter(prefix="/html", tags=["html"])

templates = Jinja2Templates(directory=TEMPLATES_DIR)


"""API"""

# /tasks/api   (GET) @
''' Эндпоинт: Получить список КАТЕГОРИЙ'''
# через @ указываем какому маршруту принадлежит Эндпоинт
@task_router.get(
    "/api",                    # добавляем префикс к адресу
    response_model=list[TaskRead],   # указываем какой схеме должны соответствовать данные
    summary="Получить список задач",
    description="Выводит список всех задач имеющихся в БД"
)
def read_all_tasks(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT TaskID, TaskNumber, TaskTitle FROM Tasks ORDER BY TaskNumber")).fetchall()
    tasks = [dict(row._mapping) for row in result]
    logger.debug(tasks)
    return JSONResponse(content=jsonable_encoder(tasks))

# /tasks/api/TaskID/{task_id}    (GET) @
''' Эндпоинт: Получить список задач с категорией TaskID'''
@task_router.get("/api/TaskID/{task_id}", response_model=list[SubTaskRead],summary="Получить подзадачу по TaskID")
def read_subtasks_TaskID(task_id: int, db: Session = Depends(get_db)):
    result = db.execute(text(f"SELECT * FROM SubTasks where TaskID={task_id} ORDER BY SubTaskNumber"), {task_id: task_id}).fetchall()
    subtasks = [dict(row._mapping) for row in result]
    return subtasks

# /tasks/api/TaskID/subtasks{subtask_id}    (GET)
''' Эндпоинт: Получить подзадачу по subtask_id'''
@task_router.get("/api/{TaskID}/subtasks{subtask_id}", response_model=SubTaskRead,summary="Получить подзадачу по id")
def read_subtasks_subtask_id(subtask_id: int, db: Session = Depends(get_db)):
    return task_crud.get_subtasks_id(db, subtask_id)


# /tasks/api/variants  (GET) @
''' Получить список вариантов'''
@task_router.get("/api/variants")
def read_tasks_id(db: Session = Depends(get_db)):
    result = db.execute(text(f"select VariantID, Name from Variants")).fetchall()
    variants = [dict(row._mapping) for row in result]
    return variants

# /tasks/api/{task_id}  (GET) @
''' Эндпоинт: Получить категорию по id'''
@task_router.get("/api/{task_id}", response_model=list[TaskRead],summary="Получить задачу по id")
def read_tasks_id(task_id: int, db: Session = Depends(get_db)):
    print(type(task_id))
    result = db.execute(text(f"SELECT TaskID, TaskNumber, TaskTitle FROM Tasks where TaskID = :task_id"),{"task_id": task_id}).fetchall()
    subtasks = [dict(row._mapping) for row in result]
    return subtasks

# /tasks/exec/{VariantID}
'''вызов хранимки с вариантом'''
@task_router.get("/exec/{VariantID}/{StudentID}")
def read_tasks_of_variant (VariantID: int, db: Session = Depends(get_db), current_student = Depends(get_current_student_or_redirect)):
    query = text("EXEC dbo.GetStudentsTasks @VariantID =:VariantID, @StudentID =:StudentID")
    result = db.execute(query, {"VariantID": VariantID, "StudentID": 2}).fetchall()
    print(result)
    if not result:
            raise HTTPException(status_code=404, detail=f"нет задач с варианте с ID {VariantID}")
    subtasks = [dict(row._mapping) for row in result]
    return subtasks



"""HTML"""

# /tasks/   (GET) @
'''Вывод страницы html с категориями'''
@task_router.get("/", response_class=HTMLResponse)
def read_subtasks_TaskID(request: Request, current_student = Depends(get_current_student_or_redirect)):
    if isinstance(current_student, RedirectResponse):
        return current_student
    return templates.TemplateResponse("Tasks/tasks.html", {"request": request, "student": current_student})




# /tasks/{task_id}/subtasks{subtask_id}   (GET) @
'''Вывод страницы html с задачей'''
@task_router.get("/{task_id}/subtasks{subtask_id}", response_class=HTMLResponse)
def read_subtasks_subtask_id(request: Request, subtask_id: int, current_student = Depends(get_current_student_or_redirect),):
    if isinstance(current_student, RedirectResponse):
        logger.info("Пользователь не авторизован — перенаправляем")
        return current_student

    return templates.TemplateResponse("Tasks/task.html", {"request": request, "student": current_student,"subtask_id": subtask_id})


# /tasks/create  (GET) @
'''Вызов страницы с добавлением задачи'''
@task_router.get("/create", response_class=HTMLResponse)
def get_subtask_form(request: Request, current_student = Depends(admin_required), db: Session = Depends(get_db)):
    logger.info("Открываем страницу с созданием задачи")
    tasks = task_crud.get_all_tasks(db)
    if isinstance(current_student, RedirectResponse):
        return current_student
    return templates.TemplateResponse("Tasks/create.html", {"request": request, "student": current_student,"tasks": tasks})
# /tasks/{task_id}/create  (GET) @
'''Два одинаковых роута, для ссылок с разных страниц, чтобы корректно отрабатывала кнопка назад'''
@task_router.get("/{task_id}/create", response_class=HTMLResponse)
def get_subtask_form_with_id(request: Request, current_student = Depends(admin_required), db: Session = Depends(get_db)):
    logger.info("Открываем страницу с созданием задачи")
    tasks = task_crud.get_all_tasks(db)
    if isinstance(current_student, RedirectResponse):
        return current_student
    return templates.TemplateResponse("Tasks/create.html", {"request": request, "student": current_student,"tasks": tasks})


# /tasks/{task_id}  (GET) @
'''Подключаем html с конкретной категорией'''
@task_router.get("/{task_id}", response_class=HTMLResponse)
def list_subtasks(request: Request, task_id: int, current_student = Depends(get_current_student_or_redirect)):
    if isinstance(current_student, RedirectResponse):
        return current_student
    return templates.TemplateResponse("Tasks/subtasks.html", {"request": request, "taskId": task_id, "student": current_student})


# /tasks/{task_id}/subtasks{subtask_id}/edit  (GET)
'''Вызов страницы с редактированием задачи'''
@task_router.get("/{task_id}/subtasks{subtask_id}/edit", response_class=HTMLResponse)
def get_edit_subtask_form(
        request: Request,
        subtask_id: int,
        current_student = Depends(admin_required),
        db: Session = Depends(get_db)):
    logger.info("Открываем страницу с редактированием задачи")
    if isinstance(current_student, RedirectResponse):
        logger.info("Пользователь не авторизован — перенаправляем")
        return current_student

    logger.info(f"Открываем страницу редактирования подзадачи ID={subtask_id}")

    subtask = task_crud.get_subtasks_id(db, subtask_id)
    tasks = task_crud.get_all_tasks(db)

    return templates.TemplateResponse("Tasks/edit.html", {"request": request, "student": current_student,"subtask": subtask, "tasks": tasks})




# /varinants/
'''Вызываем html страницу с вариантами'''
@varinant_router.get("/", response_class=HTMLResponse)
def list_tasks_of_varinants(request: Request, current_student = Depends(get_current_student_or_redirect)):
    if isinstance(current_student, RedirectResponse):
        return current_student
    return templates.TemplateResponse("Tasks/variants.html", {"request": request, "student": current_student})

# /varinants/{VariantID}
'''Вызываем html страницу с конкретным вариантом'''
@varinant_router.get("/{VariantID}", response_class=HTMLResponse)
def list_tasks(request: Request, VariantID:int, current_student = Depends(get_current_student_or_redirect)):
    print(current_student)
    if isinstance(current_student, RedirectResponse):
        return current_student
    print(current_student)
    StudentID = current_student.ID
    print(StudentID)
    return templates.TemplateResponse("Tasks/var.html", {"request": request, "VariantID": VariantID, "student":current_student})








# /subtasks/create_form/    (POST)
'''Отправка данных с добавленной задачей из формы с html страницы'''
@subtask_router.post("/create_form")
def post_subtask_form(
    TaskID: int = Form(...),
    Description: str = Form(""),
    Answer: str = Form(""),
    ImageFile: UploadFile = File(None),
    SolutionFile: UploadFile = File(None),
    db: Session = Depends(get_db)
):

    logger.info("Отправляем форму на добавление задачи")
    result = task_crud.create_subtask_from_form(
        TaskID=TaskID,
        Description=Description,
        Answer=Answer,
        ImageFile=ImageFile,
        SolutionFile=SolutionFile,
        db=db
    )

    if result is None:
        # Если не создалось, выбрасываем ошибку 400 с сообщением
        logger.error("Не удалось создать подзадачу")
        raise HTTPException(status_code=400, detail="Не удалось создать подзадачу")

    return RedirectResponse(f"/subtasks/{result}", status_code=303)




# /subtasks/edit_form/    (POST)
'''Отправка данных с добавленной задачей из формы с html страницы'''
@subtask_router.post("/edit_form")
def post_edit_subtask_form(
    SubTaskID: int = Form(...),
    TaskID: int = Form(...),
    SubTaskNumber: int = Form(...),
    Description: str = Form(""),
    Answer: str = Form(""),
    ImageFile: UploadFile = File(None),
    Files: List[UploadFile] = File(...),
    SolutionFile: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    logger.info(f"Редактируем подзадачу ID={SubTaskID}")

    # Получаем текущую подзадачу из базы
    subtask = task_crud.get_subtasks_id(db,SubTaskID)
    if not subtask:
        logger.warning("Подзадача не найдена")
        return RedirectResponse("/error", status_code=303)

    # Обработка изображения
    image_path = subtask.get('ImagePath')  # по умолчанию оставляем старое изображение
    if ImageFile and ImageFile.filename: # Если был загружен новый файл изображения
        # Сохраняем изображение
        ext = ImageFile.filename.split('.')[-1]
        if image_path:
            # Было изображение — сохраняем под тем же именем
            filename = Path(image_path).name
        else:
            # Не было изображения — создаем имя по логике новой подзадачи
            result = db.execute(
                text("SELECT MAX(SubTaskNumber) FROM SubTasks WHERE TaskID = :task_id"),
                {"task_id": TaskID}
            ).scalar()
            SubTaskNumber = (int(result) if result else 0) + 1
            filename = f"task_{TaskID}_sub_{SubTaskNumber}.{ext}"
            image_path = f"Uploads/images/{filename}"

        filepath = UPLOAD_IMAGE_DIR / filename

        # Сохраняем файл
        with filepath.open("wb") as buffer:
            shutil.copyfileobj(ImageFile.file, buffer)

        logger.info(f"Изображение сохранено как {filepath}")
    else:
        # Файл не загружен
        if not image_path:
            # И раньше не было изображения — путь остаётся пустым
            image_path = None

    # Обработка файла решения
    solution_path = subtask.get('SolutionPath')  # по умолчанию оставляем старое решение

    if SolutionFile and SolutionFile.filename:  # Если был загружен новый файл решения
        # Сохраняем решение
        ext = SolutionFile.filename.split('.')[-1]
        if solution_path:
            # Был файл — сохраняем под тем же именем
            filename = Path(solution_path).name
        else:
            # Не было файла — создаем имя по логике новой подзадачи
            result = db.execute(
                text("SELECT MAX(SubTaskNumber) FROM SubTasks WHERE TaskID = :task_id"),
                {"task_id": TaskID}
            ).scalar()
            SubTaskNumber = (int(result) if result else 0) + 1
            filename = f"solution_task_{TaskID}_sub_{SubTaskNumber}.{ext}"
            solution_path = f"Uploads/solutions/{filename}"

        filepath = UPLOAD_SOLUTION_DIR / filename

        # Сохраняем файл
        with filepath.open("wb") as buffer:
            shutil.copyfileobj(SolutionFile.file, buffer)

        logger.info(f"Решение сохранено как {filepath}")
    else:
        # Файл не загружен
        if not solution_path:
            # И раньше не было файла — путь остаётся пустым
            solution_path = None

    print(f"SubTaskID:{type(SubTaskID)} TaskID:{type(TaskID)} SubTaskNumber:{type(SubTaskNumber)}")
    print(f"Files: {Files}, type: {type(Files)}")
    for f in Files:
        print(f"File: filename={f.filename}, content_type={f.content_type}, type={type(f)}")
    uploaded_files = task_crud.upload_file(SubTaskID, TaskID, SubTaskNumber, Files, db)
    print(uploaded_files)
    subtask_data = SubTaskUpdate(
        TaskID=TaskID,
        SubTaskNumber=SubTaskNumber,
        Description=Description,
        Answer=Answer,
        ImagePath=image_path,
        SolutionPath=solution_path  # если есть
    )

    updated_subtask = task_crud.update_subtask(SubTaskID, subtask_data, db)
    if updated_subtask is None:
        logger.info("Ошибка при обновлении подзадачи")
        return RedirectResponse("/error", status_code=303)

    return RedirectResponse(f"/tasks/{TaskID}", status_code=303)











# /subtasks/files/{file_id}/download   (GET)
'''Скачивание файла прикрепленного к задаче'''
@subtask_router.get("/files/{file_id}/download")
def download_file(file_id: int, db: Session = Depends(get_db)):
    db_file = db.query(SubTaskFiles).filter(SubTaskFiles.ID == file_id).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="Файл не найден")

    return FileResponse(path=db_file.FilePath, filename=db_file.FileName)

'''получение всех файлов задачи'''
@subtask_router.get("/api/files/{subtask_id}", response_model=List[FileSchema])
def get_files_for_subtask(subtask_id: int, db: Session = Depends(get_db)):
    files = db.execute(text("""
        SELECT ID, FileName, FilePath, UploadDate
        FROM SubTaskFiles
        WHERE SubTaskID = :subtask_id
    """), {"subtask_id": subtask_id}).mappings().all()
    return list(files)








# /subtasks/api/columns (GET)
''' Эндпоинт: Получить список всех столбцов таблицы subtasks'''
'''@subtask_router.get("/api/columns", response_model=list[str],summary="Получить список всех столбцов таблицы 'subtasks'")
def get_task_columns(db: Session = Depends(get_db)):
    return task_crud.get_columns_of_table(db)'''

# /subtasks/api/    (GET)
''' Эндпоинт: Получить список всех подзадач'''
'''@subtask_router.get("/api/", response_model=list[SubTaskRead],summary="Получить список всех подзадач")
def read_all_subtasks(db: Session = Depends(get_db)):
    return task_crud.get_all_subtasks(db)'''

# /subtasks/create/    (POST)
''' Эндпоинт: Добавление подзадачи (для API)'''
'''@subtask_router.post("/create/", status_code=201,summary="Добавление подзадачи")
def create_new_subtask(subtask: SubTaskCreate, db: Session = Depends(get_db)):
    new_id = task_crud.create_subtask(db, subtask)
    logger.info("Выполнили роут с добавлением задачи")
    return {"message": "Подзадача успешно добавлена", "SubTaskID": new_id}'''










# /html
'''Подключаем html файл с Jinja2'''
'''@task_ji_router.get("/", response_class=HTMLResponse)
def list_tasks_html(request: Request, db: Session = Depends(get_db)):
    tasks = db.query(Task).all() # передаю модель Task в запрос
    return templates.TemplateResponse("Tasks/tasks_jinja.html", {"request": request, "tasks": tasks})'''

