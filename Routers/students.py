from http.client import HTTPException

from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session
from Schemas.students import StudentsRead, StudentTaskRead
from Crud import students
from dependencies import get_db  # Зависимость для подключения к базе данных
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Literal
import logging
from Crud.auth import get_current_student, admin_required, verify_password, get_current_student_or_redirect
from fastapi.responses import RedirectResponse

logger = logging.getLogger(__name__)
# Routers\Students.py
''' Маршруты и Эндпоинты'''

students_router = APIRouter(prefix="/students", tags=["students"])
students_subtasks_router = APIRouter(prefix="/students_subtasks", tags=["students_subtasks"])
templates = Jinja2Templates(directory="templates")

# /students/api/
''' Эндпоинт: Получить список пользователей'''
@students_router.get(
    "/api/",
    response_model=list[StudentsRead],
    summary="Получить список пользователей",
    description="."
)
def read_all_students(db: Session = Depends(get_db)):
    return students.get_all_students(db)

# /students/api{student_id}
''' Эндпоинт: Получить пользователей по id (/students/{student_id})'''
@students_router.get("/api/{student_id}", response_model=list[StudentsRead],summary="Получить пользователя по ID")
def read_student_id(student_id: int, db: Session = Depends(get_db)):
    return students.get_student_id(db, student_id)

# /students/{value}
''' Эндпоинт: Получить пользователей по параметру '''
@students_router.get("/{value}", response_model=list[StudentsRead],summary="Получить пользователя по выбранному полю")
def read_student_by_field(
        value: str,
        #by: str = 'id', # значение по умолчанию
        by: Literal["id", "login"] = Query("id", description="Поле для поиска: 'id' или 'login'"),
        db: Session = Depends(get_db)):
    return students.get_student_by_field(db, value, by)



# /students_subtasks/api
'''Эндпоинт для получения всех подзадач всех студентов'''
@students_subtasks_router.get("/api", response_model=list[StudentTaskRead])
def read_all_students_subtasks(db: Session = Depends(get_db)):
    return students.get_all_students_tasks(db)

# /students_subtasks/api/{student_id}
'''Эндпоинт для получения всех подзадач студента по его student_id'''
@students_subtasks_router.get("/api/{student_id}", response_model=list[StudentTaskRead])
def read_student_all_subtasks(student_id: int, db: Session = Depends(get_db)):
    return students.get_student_all_tasks(db, student_id)

#/students_subtasks/api/{StudentID}/{SubTasksID}
'''Эндпоинт для получения задачи студента по его student_id и номеру SubTasksID'''
@students_subtasks_router.get("/api/{student_id}/{SubTasksID}", response_model=list[StudentTaskRead])
def read_task_student(student_id: int, SubTasksID: int, db: Session = Depends(get_db)):
    return students.get_task_student(db, student_id, SubTasksID)


# /students/List/
'''Возвращем html страницу со списком всех пользователей'''
@students_router.get("/List/",  response_class=HTMLResponse)
def read_all_students(request: Request, db: Session = Depends(get_db)):
    students_list = students.get_all_students(db)
    logger.info("Получен запрос на список студентов")
    return templates.TemplateResponse("Students/ListStudents.html", {"request": request, "students": students_list})

# /students_subtasks/StudentTask/{StudentID}
'''Возвращем страницу со всеми задачами пользователя'''
@students_subtasks_router.get("/StudentTask/{StudentID}",  response_class=HTMLResponse)
def read_student_all_subtasks(
        request: Request,
        StudentID: int,
        current_student=Depends(get_current_student_or_redirect),
        db: Session = Depends(get_db)):
    logger.info(f"Вызван роут read_student_all_subtasks с StudentID={StudentID}")
    student_tasks = students.get_student_all_tasks(db, StudentID)
    print(student_tasks)
    return templates.TemplateResponse("Students/StudentTask.html", {"request": request, "StudentID": StudentID, "tasks": student_tasks, "student": current_student})

# /students_subtasks/StudentTasksByLogin
'''возвращаем страницу со всеми задачами пользователя в личном кабинете по логину из авторизации'''
@students_subtasks_router.get("/StudentTasksByLogin/", response_class=HTMLResponse)
def read_student_all_subtasks_by_login(
    request: Request,
    current_student=Depends(get_current_student_or_redirect),
    db: Session = Depends(get_db)
):
    if isinstance(current_student, RedirectResponse):
        return current_student
    StudentID = current_student.ID
    tasks = students.get_student_all_tasks(db, StudentID)

    logging.warning(f"ПАРАМЕТРЫ: StudentID={StudentID}") # логирование

    if not current_student:
        return templates.TemplateResponse("Students/StudentTask.html", {
            "request": request,
            "error": "Студент не найден"
        })
    StudentID = current_student.ID

    return templates.TemplateResponse("Students/StudentTask.html", {
        "request": request,
        "StudentID": StudentID,
        "tasks": tasks,
        "student": current_student,
    })

# /students_subtasks/StudentTask/{StudentID}/{SubTasksID}
'''Возращаем страницу с задачей пользователя по его id и номеру задачи'''
@students_subtasks_router.get("/StudentTask/{StudentID}/{SubTasksID}",  response_class=HTMLResponse)
def read_student_all_subtasks(
        request: Request,
        StudentID: int,
        SubTasksID: int,
        current_student=Depends(get_current_student_or_redirect),
        db: Session = Depends(get_db)):
    logging.warning(f"Вызываем роут read_student_all_subtasks с параметрами: student_id={StudentID} SubTasksID={SubTasksID}")  # логирование
    Task = students.get_task_student(db, StudentID, SubTasksID)
    print(Task)

    return templates.TemplateResponse("Students/Task.html", {"request": request, "StudentID": StudentID, "SubTasksID": SubTasksID, "Task": Task, "student": current_student})

