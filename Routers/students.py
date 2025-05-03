from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Schemas.students import StudentsRead, StudentTaskRead
from Crud import students
from dependencies import get_db  # Зависимость для подключения к базе данных

students_router = APIRouter(prefix="/students", tags=["students"])
students_subtasks_router = APIRouter(prefix="/students_subtasks", tags=["students_subtasks"])

''' Эндпоинт: Получить список пользователей (/students/)'''
@students_router.get(
    "/",
    response_model=list[StudentsRead],
    summary="Получить список пользователей",
    description="."
)
def read_all_students(db: Session = Depends(get_db)):
    return students.get_all_students(db)

''' Эндпоинт: Получить пользователей по id (/students/{students_id})'''
@students_router.get("/{students_id}", response_model=list[StudentsRead],summary="Получить пользователя по ID")
def read_students_id(students_id: int, db: Session = Depends(get_db)):
    return students.get_student_id(db, students_id)

'''Эндпоинт для получения всех подзадач всех студентов'''
@students_subtasks_router.get("/", response_model=list[StudentTaskRead])
def read_all_students_subtasks(db: Session = Depends(get_db)):
    return students.get_all_students_tasks(db)

'''Эндпоинт для получения всех подзадач студента по его id'''
@students_subtasks_router.get("/{students_id}", response_model=list[StudentTaskRead])
def read_student_all_subtasks(students_id: int, db: Session = Depends(get_db)):
    return students.get_student_all_tasks(db, students_id)
