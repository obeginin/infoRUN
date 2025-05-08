from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Models import Student
from Schemas.auth import StudentLogin
from Security.token import create_access_token
from Security.password import verify_password
from dependencies import get_db

auth_router = APIRouter(prefix="/login", tags=["login"])


# Маршрут для аутентификации
@auth_router.post("/",  summary="Аутентификация",)
def login(student_login: StudentLogin, db: Session = Depends(get_db)):
    # Поиск студента по логину
    student = db.query(Student).filter(Student.Login == student_login.Login).first()

    if not student:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Проверяем пароль
    if not verify_password(student_login.Password, student.Password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Создаём токен
    access_token = create_access_token(data={"sub": student.Login})
    return {"access_token": access_token, "token_type": "bearer"}