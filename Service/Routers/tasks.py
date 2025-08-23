from Service.config_app import UPLOAD_IMAGE_DIR, UPLOAD_SOLUTION_DIR, UPLOAD_FILES_DIR, TEMPLATES_DIR
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


























