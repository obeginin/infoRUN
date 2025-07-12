from Service.config import TEMPLATES_DIR
from Service.Models import Student
from Service.Schemas.auth import StudentLogin, StudentAuth, AssignPermissionsRequest, ChangePasswordRequest, AdminChangePasswordRequest, TokenWithStudent
from Service.Crud.auth import get_current_student, permission_required, verify_password, hash_password, get_current_student_or_redirect, get_student_by_login
from Service.Security.token import create_access_token
from Service.dependencies import get_db,get_log_db, get_producer_dep
from Service.producer import send_log
from Service.Crud import errors

from fastapi import APIRouter, Depends,Form, Request, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from sqlalchemy import text
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
import logging
logger = logging.getLogger(__name__)

# Routers\auth.py
home_router = APIRouter() # страница для пользователей
auth_router = APIRouter(prefix="/auth", tags=["auth"]) # страница для пользователей
admin_router = APIRouter(prefix="/admin", tags=["admin"]) # страница для админа
templates = Jinja2Templates(directory=TEMPLATES_DIR)
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")



"""Роут с аутентификацией (логирование в kafka)"""
# /auth/login
@auth_router.post("/login", response_model=TokenWithStudent,
                  summary="Аутентификация (запрос токена для пользователя)",
                  description="Возвращает токен, если логин и пароль пользователя корректны, а так же пользователь активен")
def login(
    request: Request,
    student_login: StudentLogin,
    db: Session = Depends(get_db),
    kafka_producer = Depends(get_producer_dep)
):
    ip = request.headers.get("X-Forwarded-For") or request.client.host
    user_agent = request.headers.get("User-Agent")

    # Ищем студента в базе по логину
    student = get_student_by_login(student_login.Login, db)
    if not student:
        logger.warning(f"Попытка входа с несуществующим логином: {student_login.Login}")
        send_log(
            StudentID=None,  # Или 0
            StudentLogin=student_login.Login,
            action="login_failed",
            details={
                "DescriptionEvent": "Неуспешный вход",
                "Reason": "InvalidCredentials",
                "IPAddress": ip,
                "UserAgent": user_agent
            }
        )
        raise errors.bad_request(error="InvalidCredentials", message ="Пользователь с таким логином не найден")
    logger.info(f"Аутентифицирован студент: ({student['ID']}) {student['Login']} ")

    # Проверяем пароль
    if not verify_password(student_login.Password, student["Password"]):
        logger.warning(f"Попытка входа {student_login.Login} с неправильным паролем!")
        send_log(
            StudentID=student["ID"],
            StudentLogin=student_login.Login,
            action="password_failed",
            details={
                "DescriptionEvent": "Неуспешный вход",
                "Reason": "InvalidCredentials",
                "IPAddress": ip,
                "UserAgent": user_agent
            }
        )
        raise errors.bad_request(error="InvalidCredentials",message= "Пароль не верный")

    # Проверяем пользователь на активность
    if not student["IsActive"]:
        logger.warning(f"Попытка входа {student_login.Login} не активного пользователь!")
        send_log(
            StudentID=student["ID"],
            StudentLogin=student_login.Login,
            action="UserNoActive",
            details={
                "DescriptionEvent": "Неуспешный вход",
                "Reason": "InvalidCredentials",
                "IPAddress": ip,
                "UserAgent": user_agent,
            }
        )
        raise errors.bad_request(error="InvalidCredentials", message="Пользователь не активен!")

    # Создаём токен
    try:
        access_token = create_access_token(data={"sub": student["Login"]})
    except Exception:
        logger.exception("Ошибка при создании токена")
        raise errors.internal_server(error="TokenGenerationError", message="Ошибка при создании токена доступа")

    # Создаём Pydantic-модель из словаря (Селеризация)
    student_short = StudentAuth(
        ID=student["ID"],
        Login=student["Login"],
        last_name=student["Last_Name"],
        first_name=student["First_Name"],
        email=student["Email"],
        role_name=student["RoleName"]
    )
    # отправляем лог в kafka
    send_log(
        StudentID=student["ID"],
        StudentLogin=student["Login"],
        action="login_success",
        details={
            "DescriptionEvent": "Успешный вход",
            "IPAddress": ip,
            "UserAgent": user_agent,
            #"Metadata": {"extra": "value"}  # по желанию
        }
    )
    return TokenWithStudent (
        access_token = access_token,
        token_type = "bearer",
        student = student_short
    )



# /
'''страница home без префикса'''
'''@home_router.get("/")
def home_page(request: Request, current_student = Depends(get_current_student_or_redirect)):
    client_ip = request.headers.get("X-Forwarded-For") or request.client.host
    path = request.url.path

    if isinstance(current_student, RedirectResponse):
        logger.info(f"[{client_ip}] Неавторизованный доступ к {path} — выполняется редирект на страницу входа")
        return current_student

    # kafka + логирование
    logger.info(f"[{client_ip}] Студент {current_student.Login} открыл корневую страницу")
    send_log(
        producer,
        StudentID=current_student.ID,
        StudentLogin=current_student.Login,
        action="login",
        details={
            "DescriptionEvent": "Пользователь успешно вошёл в систему",
            "IPAddress": client_ip,
            "UserAgent": request.headers.get("user-agent"),
            "Metadata":"пока просто текст"})

    return templates.TemplateResponse("home.html", {"request": request, "student": current_student})'''



# /home/
'''Домашняя страница (после авторизации)'''
@auth_router.get("/")
def home_page(request: Request, current_student = Depends(get_current_student_or_redirect)):
    # Проверим: если редирект, то возвращаем его
    client_ip = request.headers.get("X-Forwarded-For") or request.client.host
    path = request.url.path
    print(current_student.__dict__)
    if isinstance(current_student, RedirectResponse):
        logger.info(f"[{client_ip}] Неавторизованный доступ к {path} — выполняется редирект на страницу входа")
        return current_student

    # kafka + логирование
    logger.info(f"[{client_ip}] Студент {current_student.Login} открыл главную страницу")
    send_log(
        producer,
        current_student.Login, "login",
        {
            "DescriptionEvent": "Пользователь успешно вошёл в систему", "IPAddress": client_ip,
            "UserAgent": request.headers.get("user-agent"), "Metadata": "пока просто текст"})

    return templates.TemplateResponse("home.html", {"request": request, "student": current_student})

# /home/login_in/ (POST)
'''Страница входа (отправка данных)'''
@auth_router.post("/login_in/")
async def login_in(
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
    current_student=Depends(permission_required("admin_panel"))
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


"""Роли и разрешения"""

# /admin/roles (GET)
@admin_router.get("/roles", summary="Получить список всех ролей",)
def read_roles(db: Session = Depends(get_db)):
    roles = db.execute(text("SELECT * FROM Roles")).mappings().all()
    return roles

# /admin/students/{student_id}/assign-role (POST)
@admin_router.post("/students/{student_id}/assign-role", summary="Назначить роль студенту по его id")
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


# /admin/permission
@admin_router.get("/permission", summary="Получить список всех разрешений ")
def read_permission(db: Session = Depends(get_db)):
    permission = db.execute(text("select * from Permissions")).mappings().all()
    return permission

# /admin/roles/{role_id}/assign-permission
@admin_router.get("/roles/{role_id}/assign-permission" , summary="Получить список разрешения для роли по её id")
def exists_permissions_role(role_id: int, db: Session = Depends(get_db)):
    role_exists = db.execute(text("SELECT * FROM Roles where RoleID = :role_id"),
                             {"role_id": role_id}).mappings().fetchone()
    if not role_exists:
        return HTTPException(status_code=404, detail="Роль не найдена")

    role_permissions = db.execute(text("""SELECT r.RoleID, r.Name as RoleName, p.PermissionID, p.Name as PermissionName
                                            FROM RolePermissions rp
                                            JOIN Roles r ON rp.RoleID = r.RoleID
                                            JOIN Permissions p ON rp.PermissionID = p.PermissionID
                                            WHERE r.RoleID = 1
                                            ORDER BY r.RoleID"""),
                             {"role_id": role_id}).mappings().all()
    if not role_permissions:
        return HTTPException(status_code=404, detail="Разрешений у выбранной роли не найдено")

    # Формируем результат, для выбранно роли выводим
    role_info = {
        "role_id": role_permissions[0]["RoleID"], # её id
        "role_name": role_permissions[0]["RoleName"], # её имя
        "permission_ids": [row["PermissionID"] for row in role_permissions], # генератором перебираем все строки из результата запроса и добавляем все разрешения для неё
        "permission_names": [row["PermissionName"] for row in role_permissions], # тоже самое только с именами
    }
    return role_info




# /admin/roles/{role_id}/assign-permission
@admin_router.post("/roles/{role_id}/assign-permission", summary="Назначить разрешения для роли")
def assign_permission_for_role (role_id: int, data: AssignPermissionsRequest, db: Session = Depends(get_db)):
    # проверяем что такая роль существует
    role_exists = db.execute(text("SELECT * FROM Roles where RoleID = :role_id"),
                             {"role_id": role_id}).mappings().fetchone()
    if not role_exists:
        return  HTTPException(status_code=404, detail="Роль не найдена")

    # находим текущие разраешения для данной роли
    current_permission =  db.execute(text("SELECT PermissionID FROM RolePermissions where RoleID = :role_id"),
                                     {"role_id": role_id}).scalars().all()

    current_permission_set = set(current_permission)
    new_permissions_set = set(data.permission_ids)
    to_add = new_permissions_set - current_permission_set # роли для добавления
    to_delete = current_permission_set - new_permissions_set # роли для удаления

    # удаляем разрешения, которые больше не нужны
    for permission in to_delete:
        db.execute(text("delete RolePermissions where RoleID = :role_id and PermissionID = :permission"),
                   {"role_id": role_id, "permission": permission})
    # добавляем новые разрешения
    for permission in to_add:
        db.execute(text("insert into RolePermissions (RoleID, PermissionID) values (:role_id, :permission)"),
                   {"role_id": role_id, "permission": permission})
    db.commit()

    return {
        "message": f"Роль '{role_exists['Name']}' обновлена",
        "added": list(to_add),
        "removed": list(to_delete)
    }

# /home/change-password
@auth_router.post("/change-password", summary = "Сменить пароль текущего пользователя")
def change_password(data: ChangePasswordRequest, db: Session = Depends(get_db), current_student =  Depends(get_current_student)):
    # Получаем текущий хеш пароля из базы
    stored_password = db.execute(text("select Password from students where ID = :id"), {"id": current_student["ID"]}).scalar()


    # Проверка старого пароля
    if not verify_password(data.old_password, stored_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Старый пароль неверен"
        )

    # хешуруем новый пароль
    new_hashed_password = hash_password(data.new_password)
    db.execute(text("update Students set Password = :new_hashed_password where ID = :id" ), {"new_hashed_password": new_hashed_password, "id": current_student["ID"]})
    db.commit()
    return {"message": "Пароль успешно изменён"}


# /admin/students/{student_id}/change-password
@admin_router.post("/students/{student_id}/change-password", summary = "Сменить пароль выбранного студента по его id")
def admin_change_password(
        student_id: int,
        data: AdminChangePasswordRequest, # новый пароль
        db: Session = Depends(get_db),
        current_user=Depends(permission_required("edit_students")) # Проверка на разрешение
):
    # Проверим, существует ли студент
    student = db.execute(text("select * from Students where id = :id"), {"id": student_id}).mappings().fetchone()
    print(student)
    if not student:
        raise  HTTPException(status_code=404, detail="Студент не найден")

    # хешуруем новый пароль
    new_hashed_password = hash_password(data.new_password)
    db.execute(text("update Students set Password = :new_hashed_password where ID = :id" ), {"new_hashed_password": new_hashed_password, "id": student_id})
    db.commit()
    return  {"message": f"Пароль студента {student["Login"]} успешно изменён"}

"""роут с историей пользователя (его надо перенести либо доработать) и надо сделать такой же
только id берется от текущего пользователя"""
# /admin/logs
@admin_router.get("/logs", summary = "Вывод истории входов пользователя по его ID")
#def get_logs(current_user: Student = Depends(get_current_student), db_log: Session = Depends(get_log_db)):
def get_logs(studentID: int, db_log: Session = Depends(get_log_db)):
    result = db_log.execute(text("""
        SELECT TOP 50 * FROM StudentActionLogs
        WHERE StudentID = :student_id
        ORDER BY EventTime DESC
    """), {'student_id': studentID})

    logs = result.mappings().all()
    return JSONResponse(content=jsonable_encoder(logs))

