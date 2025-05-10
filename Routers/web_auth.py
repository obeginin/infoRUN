from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, Form, Depends, status
from sqlalchemy.orm import Session
from Security.password import verify_password
from Security.token import create_access_token # или откуда у тебя функции
from dependencies import get_db
from Models import Student  # или откуда у тебя модель

router = APIRouter(prefix="/login_in", tags=["login_in"])
templates = Jinja2Templates(directory="templates")

@router.post("/")
def login_from_form(
    request: Request,
    student: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    student_obj = db.query(Student).filter(Student.Login == student).first()

    if not student_obj or not verify_password(password, student_obj.Password):
        return templates.TemplateResponse(
            "General/login.html",
            {"request": request, "error": "Неверный логин или пароль"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    # Успешная авторизация: создаём токен
    access_token = create_access_token(data={"sub": student_obj.Login})

    # Сохраняем токен в cookie и редиректим
    response = RedirectResponse(url="/home", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response