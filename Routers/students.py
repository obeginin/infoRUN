from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from Schemas.students import StudentsRead, StudentTaskRead
from Crud import students
from dependencies import get_db  # Зависимость для подключения к базе данных
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

students_router = APIRouter(prefix="/students", tags=["students"])
students_subtasks_router = APIRouter(prefix="/students_subtasks", tags=["students_subtasks"])
templates = Jinja2Templates(directory="templates")

# /students//api/
''' Эндпоинт: Получить список пользователей (/students/)'''
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
'''Эндпоинт для получения подзадачи студента по его student_id и '''
@students_subtasks_router.get("/api/{student_id}/{SubTasksID}", response_model=list[StudentTaskRead])
def read_task_student(student_id: int, SubTasksID: int, db: Session = Depends(get_db)):
    return students.get_task_student(db, student_id, SubTasksID)


# /students/List/
'''Получаем всех пользователей'''
@students_router.get("/List/",  response_class=HTMLResponse)
def read_all_students(request: Request, db: Session = Depends(get_db)):
    students_list = students.get_all_students(db)
    print(students_list)
    return templates.TemplateResponse("Students/ListStudents.html", {"request": request, "students": students_list})

# /students_subtasks/StudentTask/{StudentID}
'''Получаем все задачи пользователя'''
@students_subtasks_router.get("/StudentTask/{StudentID}",  response_class=HTMLResponse)
def read_student_all_subtasks(request: Request, StudentID: int, db: Session = Depends(get_db)):
    student = students.get_student_all_tasks(db, StudentID)
    print(student)
    return templates.TemplateResponse("Students/StudentTask.html", {"request": request, "StudentID": StudentID, "tasks": student})

# /students_subtasks/StudentTask/{StudentID}/{SubTasksID}
'''Получаем задачу пользователя'''
@students_subtasks_router.get("/StudentTask/{StudentID}/{SubTasksID}",  response_class=HTMLResponse)
def read_student_all_subtasks(request: Request, StudentID: int, SubTasksID: int, db: Session = Depends(get_db)):
    Task = students.get_task_student(db, StudentID, SubTasksID)
    print(Task)
    return templates.TemplateResponse("Students/Task.html", {"request": request, "StudentID": StudentID, "Task": Task})