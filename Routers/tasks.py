from fastapi import APIRouter, Depends, Request, Form, UploadFile, File, Query, HTTPException

from sqlalchemy.orm import Session
from Schemas.tasks import TaskRead, SubTaskRead, SubTaskCreate, SubTaskUpdate
from Crud import tasks as task_crud
from dependencies import get_db
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from Crud.auth import get_current_student
from Models import Student
from pathlib import Path
import shutil
from Crud.auth import get_current_student, admin_required, verify_password, get_current_student_or_redirect
from fastapi.responses import RedirectResponse
import os
import logging
logger = logging.getLogger(__name__)
# Routers\tasks.py
''' Маршруты и Эндпоинты'''

'''Маршруты добавляются к основному адресу сайта localhost:9000/'''
task_router  = APIRouter(prefix="/tasks", tags=["tasks"])
subtask_router  = APIRouter(prefix="/subtasks", tags=["subtasks"])
task_js_router = APIRouter(prefix="/js", tags=["js"])
#task_ji_router = APIRouter(prefix="/html", tags=["html"])
templates = Jinja2Templates(directory="templates")

# /tasks/api/   (GET)
''' Эндпоинт: Получить список КАТЕГОРИЙ'''
# через @ указываем какому маршруту принадлежит Эндпоинт
@task_router.get(
    "/api/",                    # добавляем префикс к адресу
    response_model=list[TaskRead],   # указываем какой схеме должны соответсвовать данные
    summary="Получить список задач",
    description="Выводит список всех задач имеющихся в БД"
)
def read_all_tasks(db: Session = Depends(get_db)):
    return task_crud.get_all_tasks(db) # качестве результата запукаем функцию get_all_tasks из файла Crud\tasks.py



# /tasks/api/{task_id}  (GET)
''' Эндпоинт: Получить категорию по id'''
@task_router.get("/api/{task_id}", response_model=list[TaskRead],summary="Получить задачу по id")
def read_tasks_id(task_id: int, db: Session = Depends(get_db)):
    return task_crud.get_task_id(db, task_id)


# /tasks/(GET)
'''Вывод страницы html с категориями'''
@task_router.get("/", response_class=HTMLResponse)
def read_subtasks_TaskID(request: Request, current_student = Depends(get_current_student_or_redirect)):
    if isinstance(current_student, RedirectResponse):
        return current_student
    return templates.TemplateResponse("Tasks/tasks.html", {"request": request, "student": current_student})
# /tasks/(GET)

# /tasks/{task_id}  (GET)
'''Подключаем html с конкретной категорией'''
@task_router.get("/{task_id}", response_class=HTMLResponse)
def list_tasks(request: Request, current_student = Depends(get_current_student_or_redirect)):
    if isinstance(current_student, RedirectResponse):
        return current_student
    return templates.TemplateResponse("Tasks/subtask.html", {"request": request, "student": current_student})


'''Вывод страницы html с категориями'''
'''@task_router.get("/", response_class=HTMLResponse)
def read_subtasks_TaskID(request: Request, current_student: Student = Depends(get_current_student)):
    return templates.TemplateResponse("Tasks/tasks.html", {"request": request, "student": current_student})
'''

# /subtasks/api/columns (GET)
''' Эндпоинт: Получить список всех столбцов таблицы subtasks'''
@subtask_router.get("/api/columns", response_model=list[str],summary="Получить список всех столбцов таблицы 'subtasks'")
def get_task_columns(db: Session = Depends(get_db)):
    return task_crud.get_columns_of_table(db)

# /subtasks/api/    (GET)
''' Эндпоинт: Получить список всех подзадач'''
@subtask_router.get("/api/", response_model=list[SubTaskRead],summary="Получить список всех подзадач")
def read_all_subtasks(db: Session = Depends(get_db)):
    return task_crud.get_all_subtasks(db)

# /subtasks/create/    (POST)
''' Эндпоинт: Добавление подзадачи (для API)'''
@subtask_router.post("/create/", status_code=201,summary="Добавление подзадачи")
def create_new_subtask(subtask: SubTaskCreate, db: Session = Depends(get_db)):
    new_id = task_crud.create_subtask(db, subtask)
    logger.info("Выполнили роут с добавлением задачи")
    return {"message": "Подзадача успешно добавлена", "SubTaskID": new_id}

#UPLOAD_DIR = Path("Uploads")
#UPLOAD_DIR.mkdir(exist_ok=True)
UPLOAD_IMAGE_DIR = Path("Uploads/images")
UPLOAD_SOLUTION_DIR = Path("Uploads/solutions")
UPLOAD_IMAGE_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_SOLUTION_DIR.mkdir(parents=True, exist_ok=True)


# /subtasks/new/  (GET)
'''Вызов страницы с добавлением задачи'''
@subtask_router.get("/new", response_class=HTMLResponse)
def get_subtask_form(request: Request, current_student = Depends(admin_required), db: Session = Depends(get_db)):
    logger.info("Открываем страницу с созданием задачи")
    tasks = task_crud.get_all_tasks(db)
    if isinstance(current_student, RedirectResponse):
        return current_student
    return templates.TemplateResponse("Tasks/create.html", {"request": request, "student": current_student,"tasks": tasks})

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



# /subtasks/edit/  (GET)
'''Вызов страницы с редактированием задачи'''
@subtask_router.get("/edit/", response_class=HTMLResponse)
def get_edit_subtask_form(
        request: Request,
        SubTaskID: int = Query(...),
        current_student = Depends(admin_required),
        db: Session = Depends(get_db)):
    logger.info("Открываем страницу с редактированием задачи")
    if isinstance(current_student, RedirectResponse):
        logger.info("Пользователь не авторизован — перенаправляем")
        return current_student

    logger.info(f"Открываем страницу редактирования подзадачи ID={SubTaskID}")

    subtask = task_crud.get_subtasks_id(db, SubTaskID)
    tasks = task_crud.get_all_tasks(db)

    return templates.TemplateResponse("Tasks/edit.html", {"request": request, "student": current_student,"subtask": subtask, "tasks": tasks})

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
    if ImageFile and ImageFile.filename:
        # Сохраняем изображение
        ext = ImageFile.filename.split('.')[-1]
        filename = f"subtask_{SubTaskID}.{ext}"
        filepath = UPLOAD_IMAGE_DIR / filename

        # Сохраняем файл
        with filepath.open("wb") as buffer:
            shutil.copyfileobj(ImageFile.file, buffer)
        image_path = str(filepath)  # Обновляем переменную
        logger.info(f"Изображение сохранено как {filepath}")

        # Обработка файла решения
    solution_path = subtask.get('SolutionPath')  # сохраняем старый путь, если не загружено новое
    if SolutionFile and SolutionFile.filename:
        ext = SolutionFile.filename.split('.')[-1]
        filename = f"subtask_{SubTaskID}_solution.{ext}"
        filepath = UPLOAD_SOLUTION_DIR / filename

        with filepath.open("wb") as buffer:
            shutil.copyfileobj(SolutionFile.file, buffer)
        solution_path = str(filepath)
        logger.info(f"Решение сохранено как {filepath}")

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




# /subtasks/
'''Вызываем html страницу с задачами'''
@subtask_router.get("/", response_class=HTMLResponse)
def list_tasks(request: Request, current_student = Depends(get_current_student_or_redirect)):
    if isinstance(current_student, RedirectResponse):
        return current_student
    return templates.TemplateResponse("Tasks/listTasks.html", {"request": request, "student": current_student})


# /subtasks/api/{subtask_id}    (GET)
''' Эндпоинт: Получить подзадачу по subtask_id'''
@subtask_router.get("/api/{subtask_id}", response_model=SubTaskRead,summary="Получить подзадачу по id")
def read_subtasks_subtask_id(subtask_id: int, db: Session = Depends(get_db)):
    return task_crud.get_subtasks_id(db, subtask_id)



# /subtasks/{subtask_id}   (GET)
'''Вывод страницы html с задачей'''
@subtask_router.get("/{subtask_id}", response_class=HTMLResponse)
def read_subtasks_subtask_id(request: Request, subtask_id: int, current_student = Depends(get_current_student_or_redirect),):
    if isinstance(current_student, RedirectResponse):
        logger.info("Пользователь не авторизован — перенаправляем")
        return current_student

    return templates.TemplateResponse("Tasks/task.html", {"request": request, "student": current_student,"subtask_id": subtask_id})



# /subtasks/api/TaskID/{task_id}    (GET)
''' Эндпоинт: Получить подзадачу по TaskID'''
@subtask_router.get("/api/TaskID/{task_id}", response_model=list[SubTaskRead],summary="Получить подзадачу по TaskID")
def read_subtasks_TaskID(task_id: int, db: Session = Depends(get_db)):
    return task_crud.get_subtasks_TaskID(db, task_id)











# /html
'''Подключаем html файл с Jinja2'''
'''@task_ji_router.get("/", response_class=HTMLResponse)
def list_tasks_html(request: Request, db: Session = Depends(get_db)):
    tasks = db.query(Task).all() # передаю модель Task в запрос
    return templates.TemplateResponse("Tasks/tasks_jinja.html", {"request": request, "tasks": tasks})'''

