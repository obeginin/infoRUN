from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from Schemas.students import StudentsRead, StudentTaskRead
from Crud import students
from dependencies import get_db  # Зависимость для подключения к базе данных
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

students_router = APIRouter(prefix="/students", tags=["students"])
students_subtasks_router = APIRouter(prefix="/students_subtasks", tags=["students_subtasks"])
templates = Jinja2Templates(directory="templates")  # Убедитесь, что у вас есть папка 'templates' с HTML файлами

''' Эндпоинт: Получить список пользователей (/students/)'''
@students_router.get(
    "/api/",
    response_model=list[StudentsRead],
    summary="Получить список пользователей",
    description="."
)
def read_all_students(db: Session = Depends(get_db)):
    return students.get_all_students(db)

''' Эндпоинт: Получить пользователей по id (/students/{student_id})'''
@students_router.get("/api/{student_id}", response_model=list[StudentsRead],summary="Получить пользователя по ID")
def read_student_id(student_id: int, db: Session = Depends(get_db)):
    return students.get_student_id(db, student_id)

'''Эндпоинт для получения всех подзадач всех студентов'''
@students_subtasks_router.get("/api", response_model=list[StudentTaskRead])
def read_all_students_subtasks(db: Session = Depends(get_db)):
    return students.get_all_students_tasks(db)

'''Эндпоинт для получения всех подзадач студента по его id'''
@students_subtasks_router.get("/api/{student_id}", response_model=list[StudentTaskRead])
def read_student_all_subtasks(student_id: int, db: Session = Depends(get_db)):
    return students.get_student_all_tasks(db, student_id)

@students_subtasks_router.get("/StudentTask/{StudentID}",  response_class=HTMLResponse)
def read_student_all_subtasks(request: Request, StudentID: int, db: Session = Depends(get_db)):
    # Получаем все задачи для пользователя
    tasks = students.get_student_all_tasks(db, StudentID)
    print(tasks)
    return templates.TemplateResponse("Students/StudentTask.html", {"request": request, "StudentID": StudentID, "tasks": tasks})
