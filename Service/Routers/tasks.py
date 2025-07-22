from Service.config import UPLOAD_IMAGE_DIR, UPLOAD_SOLUTION_DIR, UPLOAD_FILES_DIR, TEMPLATES_DIR
from Service.Schemas import tasks
from Service.Crud import tasks as task_crud
from Service.Crud import errors
from Service.dependencies import get_db
from Service.Models import Student, SubTaskFiles
from Service.Crud.auth import get_current_student, permission_required
from Service.producer import send_log

from fastapi import APIRouter, Depends, Request, Form, UploadFile, File, Query, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse
from typing import List
from pathlib import Path
from typing import Dict, Optional
import shutil
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import logging

# Routers\tasks.py
''' Маршруты и Эндпоинты'''

load_dotenv() # загружаем переменные из файла .env
logger = logging.getLogger(__name__) # создание логгера для текущего модуля


'''Маршруты добавляются к основному адресу сайта localhost:9000/'''
subject_router  = APIRouter(prefix="/api/subjects", tags=["subjects"])
task_router  = APIRouter(prefix="/api/tasks", tags=["tasks"])
subtask_router  = APIRouter(prefix="/api/subtasks", tags=["subtasks"])
task_js_router = APIRouter(prefix="/js", tags=["js"])
varinant_router = APIRouter(prefix="/api/variants", tags=["variants"])

#task_ji_router = APIRouter(prefix="/html", tags=["html"])

templates = Jinja2Templates(directory=TEMPLATES_DIR)


"""API"""

# /api/subjects   (GET) @
@subject_router.get(
    "",
    response_model=tasks.SubjectListResponse,   # указываем какой схеме должны соответствовать данные
    summary="Получить список всех предметов (Информатика, Математика)",
    description="""так же необходимо передавать в заголовке **токен** пользователя"""
)
def read_all_subject(
        db: Session = Depends(get_db),
        current_student = Depends(get_current_student)):     # получаем текущего студента по токену

    subjects = task_crud.get_all_subjects(db)  # функция без фильтрации
    logger.warning(f"subjects:{subjects}")

    if not subjects:
        logger.warning(f"Не найдено предметов, Возвращаем пустой список")
        return {
            "message": f"Предметов не найдено",
            "subjects": []
        }

    count = len(subjects)
    send_log(
        StudentID=None,  # Или 0
        StudentLogin=current_student.Login,
        action="GetSubjects",
        details={
            "DescriptionEvent": f"Получение всех предметов",
            "TasksCount": count
        }
    )
    logger.info(f"Пользователь {current_student.Login} запросил список всех предметов")
    return {
        "message": f"Найдено предметов: {count}",
        "count": count,
        "subjects": subjects
    }


# /api/subjects/{subjectID}   (GET) @
@subject_router.get(
    "/{subjectID}",
    response_model=tasks.SubjectRead,   # указываем какой схеме должны соответствовать данные
    summary="Получить предмет по его subjectID ",
    description="""так же необходимо передавать в заголовке **токен** пользователя"""
)
def read_all_subject(
        subjectID: int,
        db: Session = Depends(get_db),
        current_student = Depends(get_current_student)):     # получаем текущего студента по токену

    # ищем предмет по id
    subject = task_crud.get_subject_by_id(db, subjectID)
    logger.warning(f"subjects:{subject}")

    if not subject:
        logger.warning(f"Не найден предмет с id: {subjectID}")
        send_log(
            StudentID=None,  # Или 0
            StudentLogin=current_student.Login,
            action="SubjectNotFound",
            details={
                "DescriptionEvent": "Предмет не найден",
                "SubjectID": subjectID
            }
        )
        raise errors.not_found(error="SubjectNotFound", message=f"Предмет с id={subjectID} не найден")


    send_log(
        StudentID=None,  # Или 0
        StudentLogin=current_student.Login,
        action="GetSubjectForID",
        details={
            "DescriptionEvent": f"Получение предмета с id:{subjectID}",
            "SubjectID": subjectID
        }
    )
    logger.info(f"Пользователь {current_student.Login} запросил предмет с id:{subjectID}")
    return subject



'''@subject_router.get("/api", summary="Вывод списка предметов")
def read_subject (db: Session = Depends(get_db), response_model=List[tasks.SubjectOut]):
    subjects = db.execute(text("SELECT * FROM Subjects")).mappings().all()
    #subjects = [dict(row) for row in result]
    return subjects'''



# /api/tasks/   (GET) @
''' Эндпоинт: Получить список КАТЕГОРИЙ'''
# через @ указываем какому маршруту принадлежит Эндпоинт
@task_router.get(
    "",                    # добавляем префикс к адресу
    response_model=tasks.TaskListResponse,   # указываем какой схеме должны соответствовать данные
    summary="Получить список категорий (ЕГЭ_1 ЕГЭ_2, и т.д)",
    description="""Если передан параметр **subjectID**, то возвращаются категории только для указанного предмета.  
        Если параметр не передан, возвращаются задачи по всем предметам.  
        **subjectID** передается как Query-параметр   
                "`/api/tasks` — все задачи"  
                "`/api/tasks?subjectID=10` — задачи для предмета с ID 10"  
                так же необходимо передавать в заголовке **токен** пользователя
        """
)
def read_all_tasks(
        db: Session = Depends(get_db),
        subjectID: int | None = Query(default=None),         # передаем id предмета (не обязательно, тогда выйдут категории всех предметов)
        current_student = Depends(get_current_student)):     # получаем текущего студента по токену

    if subjectID is None:
        tasks = task_crud.get_all_tasks(db)  # функция без фильтрации
    else:
        tasks = task_crud.get_all_tasks(db, subjectID)
    logger.warning(f"tasks:{tasks}")

    if not tasks:
        logger.warning(f"Не найдено задач с категорией id= {subjectID}, Возвращаем пустой список")
        return {
            "message": f"Для предмета с id={subjectID} категорий не найдено",
            "tasks": []
        }

    count = len(tasks)
    send_log(
        StudentID=None,  # Или 0
        StudentLogin=current_student.Login,
        action="GetTasks",
        details={
            "DescriptionEvent": f"Получение задач по предмету id:{subjectID}",
            "SubjectID": subjectID,
            "TasksCount": count
        }
    )
    logger.info(f"Пользователь {current_student.Login} запросил список категорий для предмета с id:{subjectID}")
    return {
        "message": f"Найдено задач: {count}",
        "count": count,
        "tasks": tasks
    }

# /api/tasks/TaskID/{task_id}    (GET) @
''' Эндпоинт: Получить список задач с категорией TaskID'''
@task_router.get("/TaskID/{task_id}", response_model=list[tasks.SubTaskRead],summary="Получить список задач с категорией TaskID")
def read_subtasks_TaskID(task_id: int, db: Session = Depends(get_db)):
    result = db.execute(text(f"""SELECT * FROM SubTasks s
                            LEFT JOIN Variants v on s.VariantID = v.VariantID
                            where TaskID={task_id} ORDER BY SubTaskNumber"""), {task_id: task_id}).fetchall()
    subtasks = [dict(row._mapping) for row in result]
    return subtasks

# /api/tasks/TaskID/subtasks{subtask_id}    (GET)
''' Эндпоинт: Получить подзадачу по subtask_id'''
@task_router.get("/api/{TaskID}/subtasks{subtask_id}", response_model=tasks.SubTaskRead,summary="Получить подзадачу по id")
def read_subtasks_subtask_id(subtask_id: int, db: Session = Depends(get_db)):
    return task_crud.get_subtasks_id(db, subtask_id)


# /api/tasks/variants  (GET) @
''' Получить список вариантов'''
@task_router.get("/variants")
def read_tasks_id(db: Session = Depends(get_db)):
    result = db.execute(text(f"select VariantID, VariantName from Variants order by VariantName")).fetchall()
    variants = [dict(row._mapping) for row in result]
    return variants

# /api/tasks/{task_id}  (GET) @
''' Эндпоинт: Получить категорию по id'''
@task_router.get("/{task_id}", response_model=list[tasks.TaskRead],summary="Получить задачу по id")
def read_tasks_id(task_id: int, db: Session = Depends(get_db)):
    print(type(task_id))
    result = db.execute(text(f"SELECT TaskID, TaskNumber, TaskTitle FROM Tasks where TaskID = :task_id"),{"task_id": task_id}).fetchall()
    subtasks = [dict(row._mapping) for row in result]
    return subtasks

# /api/tasks/exec/{VariantID}
'''вызов хранимки с вариантом'''
@task_router.get("/exec/{VariantID}/{StudentID}", summary="роут с вызовом хранимой процедуры")
def read_tasks_of_variant (VariantID: int, StudentID: int, db: Session = Depends(get_db)):
    query = text("EXEC dbo.GetStudentsTasks @VariantID =:VariantID, @StudentID =:StudentID")
    result = db.execute(query, {"VariantID": VariantID, "StudentID": StudentID}).fetchall()
    print(result)
    if not result:
            raise HTTPException(status_code=404, detail=f"нет задач с варианте с ID {VariantID}")
    subtasks = [dict(row._mapping) for row in result]
    return jsonable_encoder(subtasks)







# /api/variants/check_answers
@varinant_router.post("/check_answers", summary="роут который проверяет ответы пользователя для целого вараинта",
                      description="передаем словарь с ответами на все задангия пользователя в виде строк")
def check_answers(user_answers: Dict[int, Optional[str]], db: Session = Depends(get_db)):
    results = []
    print(user_answers)
    for i, (subtask_id, user_answer) in enumerate(user_answers.items()):
        if user_answer is None:
            results.append({
                "SubTaskID": subtask_id,
                "IsCorrect": False,
                "CorrectAnswer": "...",  # можно не указывать
                "UserAnswer": None
            })
            continue
        correct = db.execute(
            text("SELECT Answer FROM SubTasks WHERE SubTaskID = :id"),
            {"id": subtask_id}
        ).scalar()

        is_correct = str(user_answer).strip().lower() == str(correct).strip().lower()
        #print(i, subtask_id, correct, is_correct)
        results.append({
            "SubTaskID": subtask_id,
            "UserAnswer": user_answer,
            "CorrectAnswer": correct,
            "IsCorrect": is_correct
        })
    print(results)
    return {
        "results": results,
        "correct_count": sum(r["IsCorrect"] for r in results),
        "total": len(results),
        "message": f"Верно: {sum(r['IsCorrect'] for r in results)} из {len(results)}"
    }



# /api/subtasks/create_form/    (POST)
'''Получаем с html страницы данные из формы и запускаем с этими параметрами функцию create_subtask_from_form
в ней добавляем новую задачу в базу и возвращаем номер новой задачи и редиректим на неё
'''
@subtask_router.post("/create_form", summary="роут с созданием задачи через форму")
def post_subtask_form(
    TaskID: int = Form(...),
    VariantName: str = Form(""),
    Description: str = Form(""),
    Answer: str = Form(""),
    ImageFile: UploadFile = File(None),
    SolutionFile: UploadFile = File(None),
    db: Session = Depends(get_db)
):

    logger.debug("Отправляем форму на добавление задачи")
    result = task_crud.create_subtask_from_form(
        TaskID=TaskID,
        VariantName=VariantName,
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

    return RedirectResponse(f"/tasks/{TaskID}/subtasks{result}", status_code=303)




# /api/subtasks/edit_form/    (POST)
'''Отправка данных с добавленной задачей из формы с html страницы'''
@subtask_router.post("/edit_form", summary="роут с редактированием задачи через форму")
def post_edit_subtask_form(
    SubTaskID: int = Form(...),
    TaskID: int = Form(...),
    VariantName: str = Form(...),
    SubTaskNumber: int = Form(...),
    Description: str = Form(""),
    Answer: str = Form(""),
    ImageFile: UploadFile = File(None),
    Files: List[UploadFile] = File(...),
    SolutionFile: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    logger.info(f"Редактируем подзадачу ID={SubTaskID}")

    current_variant_id = db.execute(text("SELECT VariantID FROM SubTasks WHERE SubTaskID = :id"),
                                    {"id": SubTaskID}).scalar()
    # Получаем имя текущего варианта
    current_variant_name = db.execute(text("SELECT VariantName FROM Variants WHERE VariantID = :id"),
                                      {"id": current_variant_id}).scalar()
    if VariantName != current_variant_name:
        variant_id = task_crud.get_or_create_variant(db, VariantName)
    else:
        variant_id = current_variant_id

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
    subtask_data = tasks.SubTaskUpdate(
        TaskID=TaskID,
        VariantID=variant_id,
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

    return RedirectResponse(f"/tasks/{TaskID}/subtasks{SubTaskID}", status_code=303)



# /api/subtasks/files/{file_id}/download   (GET)
'''Скачивание файла прикрепленного к задаче'''
@subtask_router.get("/files/{file_id}/download",  summary="скачивание файла с задачей")
def download_file(file_id: int, db: Session = Depends(get_db)):
    db_file = db.query(SubTaskFiles).filter(SubTaskFiles.ID == file_id).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="Файл не найден")

    return FileResponse(path=db_file.FilePath, filename=db_file.FileName)

'''получение всех файлов задачи'''
@subtask_router.get("/files/{subtask_id}", response_model=List[tasks.FileSchema], summary="роут с получением всех файлов задачи")
def get_files_for_subtask(subtask_id: int, db: Session = Depends(get_db)):
    files = db.execute(text("""
        SELECT ID, FileName, FilePath, UploadDate
        FROM SubTaskFiles
        WHERE SubTaskID = :subtask_id
    """), {"subtask_id": subtask_id}).mappings().all()
    return list(files)







"""HTML"""

# /tasks/   (GET) @
'''Вывод страницы html с категориями'''
''''@task_router.get("/", response_class=HTMLResponse)
def read_subtasks_TaskID(request: Request, current_student = Depends(get_current_student_or_redirect)):
    if isinstance(current_student, RedirectResponse):
        return current_student
    return templates.TemplateResponse("Tasks/tasks.html", {"request": request, "student": current_student})'''




# /tasks/{task_id}/subtasks{subtask_id}   (GET) @
'''Вывод страницы html с задачей
@task_router.get("/{task_id}/subtasks{subtask_id}", response_class=HTMLResponse)
def read_subtasks_subtask_id(request: Request, subtask_id: int, current_student = Depends(get_current_student_or_redirect),):
    if isinstance(current_student, RedirectResponse):
        logger.info("Пользователь не авторизован — перенаправляем")
        return current_student

    return templates.TemplateResponse("Tasks/task.html", {"request": request, "student": current_student,"subtask_id": subtask_id})
'''

# /tasks/create  (GET) @
'''Вызов страницы с добавлением задачи
@task_router.get("/create", response_class=HTMLResponse)
def get_subtask_form(request: Request, current_student = Depends(permission_required("create_tasks")), db: Session = Depends(get_db)):
    logger.info(f"Открываем страницу с созданием задачи {current_student}")
    tasks = task_crud.get_all_tasks(db)
    if isinstance(current_student, RedirectResponse):
        return current_student
    return templates.TemplateResponse("Tasks/create.html", {"request": request, "student": current_student,"tasks": tasks})
# /tasks/{task_id}/create  (GET) @
Два одинаковых роута, для ссылок с разных страниц, чтобы корректно отрабатывала кнопка назад
@task_router.get("/{task_id}/create", response_class=HTMLResponse)
def get_subtask_form_with_id(request: Request, current_student = Depends(permission_required("create_tasks")), db: Session = Depends(get_db)):
    logger.info("Открываем страницу с созданием задачи")
    tasks = task_crud.get_all_tasks(db)
    if isinstance(current_student, RedirectResponse):
        return current_student
    return templates.TemplateResponse("Tasks/create.html", {"request": request, "student": current_student,"tasks": tasks})
'''

# /tasks/{task_id}  (GET) @
'''Подключаем html с конкретной категорией
@task_router.get("/{task_id}", response_class=HTMLResponse)
def list_subtasks(request: Request, task_id: int, current_student = Depends(get_current_student_or_redirect)):
    if isinstance(current_student, RedirectResponse):
        return current_student
    return templates.TemplateResponse("Tasks/subtasks.html", {"request": request, "taskId": task_id, "student": current_student})
'''

# /tasks/{task_id}/subtasks{subtask_id}/edit  (GET) @
'''Вызов страницы с редактированием задачи
@task_router.get("/{task_id}/subtasks{subtask_id}/edit", response_class=HTMLResponse)
def get_edit_subtask_form(
        request: Request,
        subtask_id: int,
        current_student = Depends(permission_required("edit_tasks")),
        db: Session = Depends(get_db)):
    logger.info("Открываем страницу с редактированием задачи")
    if isinstance(current_student, RedirectResponse):
        logger.info("Пользователь не авторизован — перенаправляем")
        return current_student

    logger.info(f"Открываем страницу редактирования подзадачи ID={subtask_id}")

    subtask = task_crud.get_subtasks_id(db, subtask_id)
    tasks = task_crud.get_all_tasks(db)

    variants = db.execute(text("SELECT VariantName FROM Variants order by VariantName")).scalars().all()

    return templates.TemplateResponse("Tasks/edit.html", {"request": request, "student": current_student,"subtask": subtask, "tasks": tasks, "variants": variants})


'''



# /variants/   @
'''Вызываем html страницу с вариантами
@varinant_router.get("/", response_class=HTMLResponse)
def list_tasks_of_varinants(request: Request, current_student = Depends(get_current_student_or_redirect)):
    if isinstance(current_student, RedirectResponse):
        return current_student
    return templates.TemplateResponse("Tasks/variants.html", {"request": request, "student": current_student})
'''



# /variants/{VariantID}    @
'''Вызываем html страницу с конкретным вариантом
@varinant_router.get("/{VariantID}", response_class=HTMLResponse)
def list_tasks(request: Request, VariantID:int, current_student = Depends(get_current_student_or_redirect), db: Session = Depends(get_db)):
    print(current_student)
    if isinstance(current_student, RedirectResponse):
        return current_student
    print(current_student)
    StudentID = current_student.ID
    print(StudentID)
    tasks = read_tasks_of_variant(VariantID, db)
    return templates.TemplateResponse("Tasks/var.html", {"request": request, "tasks": tasks, "student":current_student})
'''












# /subtasks/api/columns (GET)
''' Эндпоинт: Получить список всех столбцов таблицы subtasks'''
'''@subtask_router.get("/api/columns", response_model=list[str],summary="Получить список всех столбцов таблицы 'subtasks'")
def get_task_columns(db: Session = Depends(get_db)):
    return task_crud.get_columns_of_table(db)'''

# /subtasks/api/    (GET)
''' Эндпоинт: Получить список всех подзадач'''
'''@subtask_router.get("/api/", response_model=list[tasks.SubTaskRead],summary="Получить список всех подзадач")
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

