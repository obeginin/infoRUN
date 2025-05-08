from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Models import Student
from Schemas.auth import StudentLogin, StudentOut
from Security.token import create_access_token
from Security.password import verify_password
from dependencies import get_db
from Crud.auth import get_current_student, admin_required

auth_router = APIRouter(prefix="/login", tags=["login"]) # страница для пользователей
admin_router = APIRouter(prefix="/admin", tags=["admin"]) # страница для админа

# /login/
'''Маршрут для аутентификации, запрос токена для пользователя'''
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

# /login/me
'''Доступ только для пользователей'''
@auth_router.get("/me", summary="Получить информацию о текущем студенте")
def read_students_me(current_student: Student = Depends(get_current_student)):
    return {
        "id": current_student.ID,
        "login": current_student.Login,
        "email": current_student.Email if hasattr(current_student, "Email") else None
    }

# /admin/dashboard
'''Роут, доступный только администраторам'''
@admin_router.get("/dashboard/")
def admin_dashboard(current_student=Depends(admin_required)):
    return {"message": f"Welcome, {current_student.Login}. You are an admin."}