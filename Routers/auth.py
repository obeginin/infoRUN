from config import TEMPLATES_DIR
from fastapi import APIRouter, Depends,Form, Request, HTTPException
from sqlalchemy.orm import Session
from Models import Student
from Schemas.auth import StudentLogin, StudentOut, RoleRead
from Security.token import create_access_token
from dependencies import get_db
from Crud.auth import get_current_student, admin_required, verify_password, get_current_student_or_redirect
from fastapi.responses import JSONResponse
from sqlalchemy import text
from typing import List
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
import logging
logger = logging.getLogger(__name__)

# Routers\auth.py
home_router = APIRouter() # страница для пользователей
auth_router = APIRouter(prefix="/home", tags=["home"]) # страница для пользователей
admin_router = APIRouter(prefix="/admin", tags=["admin"]) # страница для админа
templates = Jinja2Templates(directory=TEMPLATES_DIR)
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# /
'''страница home без префикса'''
@home_router.get("/")
def home_page(request: Request, current_student = Depends(get_current_student_or_redirect)):
    client_ip = request.client.host
    path = request.url.path
    if isinstance(current_student, RedirectResponse):
        logger.info(f"[{client_ip}] Неавторизованный доступ к {path} — выполняется редирект на страницу входа")
        return current_student
    logger.info(f"[{client_ip}] Студент {current_student.Login} открыл корневую страницу")
    return templates.TemplateResponse("home.html", {"request": request, "student": current_student})

# /home/login_in (GET)
'''Страница входа (вывод страницы с ввдом логина)'''
@auth_router.get("/login_in/")
def login_form(request: Request):
    logger.info("Выводим страницу с логином")
    return templates.TemplateResponse("General/login.html", {"request": request})

# /home/
'''Домашняя страница (после авторизации)'''
@auth_router.get("/")
def home_page(request: Request, current_student = Depends(get_current_student_or_redirect)):
    # Проверим: если редирект, то возвращаем его
    client_ip = request.client.host
    path = request.url.path
    if isinstance(current_student, RedirectResponse):
        logger.info(f"[{client_ip}] Неавторизованный доступ к {path} — выполняется редирект на страницу входа")
        return current_student
    logger.info(f"[{client_ip}] Студент {current_student.Login} открыл главную страницу")
    return templates.TemplateResponse("home.html", {"request": request, "student": current_student})

# /home/login_in/ (POST)
'''Страница входа (отправка данных)'''
@auth_router.post("/login_in/")
async def login_in(
        request: Request,
        login: str = Form(...),
        password: str = Form(...),
        next: str = Form("/"),
        db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.Login == login).first()
    if not student or not pwd_context.verify(password, student.Password):
        return RedirectResponse("/home/login_in/?error=true", status_code=303)

    access_token = create_access_token(data={"sub": student.Login})
    response = RedirectResponse(url=next, status_code=303)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True, path="/")
    return response

# /home/logout/
'''Реализация выхода (удаления cookie с токеном)'''
@auth_router.get("/logout/")
async def logout():
    print("LOGOUT!!!")
    response = RedirectResponse(url="/home/login_in/", status_code=303)
    response.delete_cookie(key="access_token", path="/")
    return response

# /login/
'''Маршрут для аутентификации, запрос токена для пользователя'''
@auth_router.post("/login",  summary="Аутентификация",)
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

# /admin/ @
'''Роут, доступный только администраторам'''
@admin_router.get("/", response_class=HTMLResponse)
def admin_dashboard(
    request: Request,
    current_student=Depends(admin_required)
):
    return templates.TemplateResponse("Admin/dashboard.html", {
        "request": request,
        "student": current_student
    })


'''вывод списка студентов в формате JSON'''
# /admin/api/students @
@admin_router.get("/api/students")
def api_get_students(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM Students")).fetchall()
    students = [dict(row._mapping) for row in result]
    return JSONResponse(content=jsonable_encoder(students))

# /admin/api/students/{StudentID}/subtasks
'''Возвращем список задач выбранного студента в формате JSON'''
@admin_router.get("/api/students/{StudentID}/subtasks")
def api_get_student_subtasks(StudentID: int, db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM StudentTasks WHERE StudentID = :StudentID"), {"StudentID": StudentID}).fetchall()
    subtasks = [dict(row._mapping) for row in result]
    #print(subtasks)
    return JSONResponse(content=jsonable_encoder(subtasks))

# /admin/ListStudents @
'''Возвращем html страницу со списком всех студентов'''
@admin_router.get("/ListStudents",  response_class=HTMLResponse)
def admin_read_all_students(
        request: Request,
        current_student=Depends(get_current_student_or_redirect)):
    logger.debug("Получен запрос на список студентов")

    # Проверям что пользователь авторизован и отправляем на страницу с логином
    if isinstance(current_student, RedirectResponse):
        return current_student
    return templates.TemplateResponse("Admin/ListStudents.html", {"request": request, "student": current_student})


# /admin/roles (GET)
"""роут который возвращает список ролей"""
@admin_router.get("/roles", summary="Получить список ролей",)
def read_roles(db: Session = Depends(get_db)):
    roles = db.execute(text("SELECT * FROM Roles")).mappings().all()
    return roles

# /admin/students/{student_id}/assign-role (POST)
"""роут который назначает роль студенту"""
@admin_router.post("/students/{student_id}/assign-role", summary="Назначить роль студенту",)
def assign_role_to_student(student_id: int, role_id: int, db: Session = Depends(get_db)):
    role_exists = db.execute(text("SELECT * FROM Roles where RoleID = :role_id"), {"role_id": role_id}).mappings().fetchone()
    if not role_exists:
        raise HTTPException(status_code=404, detail="Роль не найдена")
    student_exists = db.execute(text("select * from students where id = :student_id"), {"student_id": student_id}).mappings().fetchone()
    if not student_exists:
        raise HTTPException(status_code=404, detail="Студент не найден")
    db.execute(text("update students set RoleID = :role_id where ID = :student_id"), {"role_id":role_id, "student_id": student_id})
    db.commit()
    return  {"message": f" Студенту {student_exists['Login']} успешно назначена роль {role_exists['Name']} "}


# /admin/
'''
роут которые назначает разрешения
@admin_router.post("/assign-permission/", summary="Назначить разрешение роли")

'''