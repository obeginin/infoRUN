from Service.config import TEMPLATES_DIR, ACCESS_TOKEN_EXPIRE_MINUTES, TIME_NOW
from Service.Models import Student
from Service.Schemas import auth

from Service.Crud.auth import get_current_student, permission_required, verify_password, hash_password, get_student_by_login, get_logs_student, get_logs_all
from Service.Crud.auth import change_password, get_all_roles, get_all_permission, get_role_id, assign_role, get_permission_role, update_role_permissions
from Service.Crud.auth import get_student_by_email, add_new_register_student, confirm_student_email, del_student_email
from Service.Crud.students import  get_student_id, get_all_students
from Service.Security.token import create_access_token, verify_token
from Service.dependencies import get_db,get_log_db, get_producer_dep
from Service.producer import send_log, send_email_event
from Service.Crud import errors

from pydantic import EmailStr
from datetime import datetime
from datetime import timedelta
from typing import List
from fastapi import APIRouter, Depends,Form, Request, HTTPException, status, Response, Query
from fastapi.concurrency import run_in_threadpool
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
auth_router = APIRouter(prefix="/api/auth", tags=["auth"]) # страница для пользователей
admin_router = APIRouter(prefix="/api/admin", tags=["admin"]) # страница для админа
templates = Jinja2Templates(directory=TEMPLATES_DIR)
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")



"""Роут с аутентификацией (логирование в kafka)"""
# /api/auth/login
@auth_router.post("/login", response_model=auth.TokenWithStudent,
                  summary="Аутентификация (запрос токена для пользователя)",
                  description="Возвращает токен, тип заколовка и небольшую информацию о пользователе, если логин и пароль корректны и пользователь активен.")
def login(
    request: Request,
    student_login: auth.StudentLogin,
    db: Session = Depends(get_db),
):
    ip = request.headers.get("X-Forwarded-For") or request.client.host
    user_agent = request.headers.get("User-Agent")

    # Ищем студента в базе по логину
    student = get_student_by_login(db, student_login.Login)
    if not student:
        logger.warning(f"Попытка входа с несуществующим логином: {student_login.Login}")
        send_log(
            StudentID=None,  # Или 0
            StudentLogin=student_login.Login,
            action="LoginFailed",
            details={
                "DescriptionEvent": "Неуспешный вход",
                "Reason": "LoginNotFound",
                "IPAddress": ip,
                "UserAgent": user_agent
            }
        )
        raise errors.unauthorized(error="LoginNotFound", message ="Пользователь с таким логином не найден")
    logger.info(f"Аутентифицирован студент: ({student['ID']}) {student['Login']} ")

    # Проверяем пользователь на активность
    if not student["IsActive"]:
        logger.warning(f"Попытка входа {student_login.Login} не активного пользователь!")
        send_log(
            StudentID=student["ID"],
            StudentLogin=student_login.Login,
            action="LoginFailed",
            details={
                "DescriptionEvent": "Неуспешный вход",
                "Reason": "StudentNoActive",
                "IPAddress": ip,
                "UserAgent": user_agent,
            }
        )
        raise errors.access_denied(error="StudentNoActive", message="Пользователь не активен!")

    # Проверяем пароль
    if not verify_password(student_login.Password, student["Password"]):
        logger.warning(f"Попытка входа {student_login.Login} с неправильным паролем!")
        send_log(
            StudentID=student["ID"],
            StudentLogin=student_login.Login,
            action="LoginFailed",
            details={
                "DescriptionEvent": "Неуспешный вход",
                "Reason": "PasswordFailed",
                "IPAddress": ip,
                "UserAgent": user_agent
            }
        )
        raise errors.unauthorized(error="PasswordFailed",message= "Пароль не верный")

    # Создаём токен
    try:
        access_token = create_access_token(data={"sub": student["Login"]})
    except Exception:
        logger.exception("Ошибка при создании токена")
        raise errors.internal_server(error="TokenGenerationError", message="Ошибка при создании токена доступа")

    # Создаём Pydantic-модель из словаря (Селеризация)
    student_short = auth.StudentAuth(**student)

    # отправляем лог в kafka
    send_log(
        StudentID=student["ID"],
        StudentLogin=student["Login"],
        action="LoginSuccess",
        details={
            "DescriptionEvent": "Успешный вход",
            "IPAddress": ip,
            "UserAgent": user_agent,
            #"Metadata": {"extra": "value"}  # по желанию
        }
    )
    return auth.TokenWithStudent (
        access_token = access_token,
        token_type = "bearer",
        student = student_short
    )


"""
После аутентификации фронт будет в заголовке отправлять токен, по нему с помощью функции get_current_student()
получаем информации о пользователе (данный роут нужен для Backend)
"""
# /api/auth/check-token
@auth_router.get("/check-token", response_model=auth.StudentOut, summary="Образец получения данных пользователя по токену (с разрешениями)")
def check_token(request: Request, current_student = Depends(get_current_student)):
    return current_student


# /api/auth/register
'''Регистрация'''
@auth_router.post("/register", summary="Регистрация пользователя",
                 description="после ввода данных на указанный email отправляется письмо с подтверждением почты")
def register_user(user_data: auth.UserCreate, db: Session = Depends(get_db)):
    student = get_student_by_email(db, user_data.email)
    if student:
        raise errors.bad_request(message="Пользователь с таким Email уже зарегистрирован")
    student = get_student_by_login(db, user_data.login)
    if student:
        raise errors.bad_request(message="Пользователь с таким Login уже зарегистрирован")
    # хэшируем пароль
    hashed_password = hash_password(user_data.password)
    # Генерация токена подтверждения
    token = create_access_token(
        data={"sub": user_data.email}, # закладываем в токен email
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # Подготовка параметров для вставки
    params = {
        "Email": user_data.email,
        "Login": user_data.login,
        "Password": hashed_password,
        "IsConfirmed": False,
    }
    add_new_register_student(db, params)

    logger.info(f"Новый пользователь зарегистрирован: {user_data.email}")

    # Отправка события Kafka на email-сервис
    send_email_event(
        event_type="email_registration",
        email=user_data.email,
        subject="Подтверждение регистрации",
        template="registration_confirmation",
        data={"confirmation_link": f"https://info-run.ru/auth/confirm-email?token={token}"}
    )
    logger.info(f"Письмо с подтверждением отправлено: {user_data.email}")
    return  {"message": f"Письмо с подтверждением отправлено на почту {params["Email"]}"}


# /api/auth/register
'''Регистрация'''
@auth_router.post("/register/v2", summary="Регистрация пользователя",
                 description="после ввода данных на указанный email отправляется письмо с подтверждением почты")
def register_user(user_data: auth.UserCreate, db: Session = Depends(get_db)):
    student = get_student_by_email(db, user_data.email)
    if student:
        raise errors.bad_request(message="Пользователь с таким Email уже зарегистрирован")
    student = get_student_by_login(db, user_data.login)
    if student:
        raise errors.bad_request(message="Пользователь с таким Login уже зарегистрирован")
    # хэшируем пароль
    hashed_password = hash_password(user_data.password)
    # Генерация токена подтверждения
    token = create_access_token(
        data={"sub": user_data.email}, # закладываем в токен email
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # Подготовка параметров для вставки
    params = {
        "Email": user_data.email,
        "Login": user_data.login,
        "Password": hashed_password,
        "IsConfirmed": False,
    }
    add_new_register_student(db, params)

    logger.info(f"аааааааНовый пользователь зарегистрирован: {user_data.email}")
    confirmation_link = f"http://localhost:5177/auth/confirm-email?token={token}"
    logger.warning(f"!!!!!!!send_email_event called with confirmation_link: {confirmation_link}")
    logger.info(f"Привеееееееет")
    # Отправка события Kafka на email-сервис
    send_email_event(
        event_type="email_registration",
        email=user_data.email,
        subject="Подтверждение регистрации",
        template="registration_confirmation",
        data={"confirmation_link": f"https://info-run.ru/api/auth/confirm-email?token={token}"}
    )
    logger.info(f"Письмо с подтверждением отправлено: {user_data.email}")

    return  {"message": f"Письмо с подтверждением отправлено на почту {params["Email"]}"}

@auth_router.post("/delete_student", summary="Удаление студента по email")
def confirm_email(email: EmailStr, db: Session = Depends(get_db)):
    # try:
    student = get_student_by_email(db, email)
    logger.info(f"Студент cccccc {student}")
    if student == None:
        logger.warning(f"Студент с email {email} не найден")
        raise errors.bad_request(message=f"Студент с email {email} не найден")
    del_student_email(db, email)
    logger.info(f"Студент с email {email} успешно удалён")
    return {"message": f"Студент с email {email} успешно удалён"}
    # except Exception as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail=str(e)
    #     )

'''Подтверждение email'''
@auth_router.get("/confirm-email", summary="Подтверждение email",
                 description="""данный роут вызывается после открытия ссылки из письма с подтверждением email""")
def confirm_email(token: str, db: Session = Depends(get_db)):
    # Декодируем и верифицируем токен
    payload = verify_token(token)
    if not payload:
        # либо истёк, либо неверная подпись
        logger.warning(f"Недействительный или просроченный токен: {token}")
        raise errors.bad_request(message="Недействительный или просроченный токен")

    # Извлекаем email из поля sub
    email = payload.get("sub")
    if not email:
        logger.warning(f"В токене отсутствует поле 'sub': {payload}")
        raise errors.bad_request(message="Неверные данные в токене")


    # обновляем данные
    result = confirm_student_email(db, {"email": email, "now": TIME_NOW})
    if result != 1:
        logger.warning(f"Пользователь не найден или уже подтверждён")
        raise errors.bad_request(message="Пользователь не найден или уже подтверждён")

    logger.info(f"Email успешно подтверждён: {email}")
    return {"message": "Email успешно подтверждён"}



# /api/auth/logout
'''Реализация выхода (удаления cookie с токеном)'''
@auth_router.get("/logout", summary="Выход, удаление токена при использовании 'HttpOnly cookie'",
                 description="Необходимо в заголовке отправлять токен (требуется для логироания выхода пользователя")
async def logout(
        request: Request,
        response: Response,
        current_student=Depends(get_current_student)):
    ip = request.headers.get("X-Forwarded-For") or request.client.host
    user_agent = request.headers.get("User-Agent")
    await run_in_threadpool(
        logger.info,f"Пользователь вышел из системы: {current_student.Login} (ID: {current_student.ID})"
    )

    # Лог в Kafka
    await run_in_threadpool(
        send_log,
        StudentID=current_student.ID,
        StudentLogin=current_student.Login,
        action="LOGOUT",
        details={
            "DescriptionEvent": "Пользователь вышел из системы",
            "IPAddress": ip,
            "UserAgent": user_agent,
        }
    )
    # Удаление куки (если используется cookie-based auth)
    response.delete_cookie("access_token")
    print("detail LOGOUT")
    logger.info (f"detail LOGOUT")
    return {"detail": "LOGOUT"}

# /api/auth/change-password
@auth_router.post("/change-password", summary = "Сменить пароль текущего пользователя (меняет сам пользователь)",
                  description="пользователя получаем по токену, который передается из заголовка с frontend. Требуется проверка студента.")
def student_change_password(data: auth.ChangePasswordRequest, db: Session = Depends(get_db), current_student =  Depends(get_current_student)):
    # Получаем текущий хеш пароля из базы
    stored_password = db.execute(text("select Password from students where ID = :id"), {"id": current_student.ID}).scalar()

    # Проверка старого пароля
    if not verify_password(data.old_password, stored_password):
        logger.warning(f"Ошибка смены пароля студента {current_student.Login}! Cтарый пароль неверный!: ")
        send_log(
            StudentID=current_student.ID,  # Или 0
            StudentLogin=current_student.Login,
            action="PasswordChanged",
            details={
                "DescriptionEvent": "Cтарый пароль неверный",
                "Reason": "OldPasswordIncorrect",
            }
        )
        raise errors.bad_request(error="OldPasswordIncorrect", message="Cтарый пароль неверный")

    if data.new_password != data.repeat_new_password:
        logger.warning(f"Ошибка смены пароля студента {current_student.Login}! Введенные пароли не совпадают!: ")
        send_log(
            StudentID=current_student.ID,  # Или 0
            StudentLogin=current_student.Login,
            action="PasswordChanged",
            details={
                "DescriptionEvent": "Cтарый пароль неверный",
                "Reason": "NewPasswordsMismatch",
            }
        )
        raise errors.bad_request(error="NewPasswordsMismatch", message="Введенные пароли не совпадают!")

    # хешуруем новый пароль
    new_hashed_password = hash_password(data.new_password)
    update_password = change_password(db, current_student.ID, new_hashed_password)

    if update_password != 1:
        logger.warning(f"Не удалось обновить пароль для студента {current_student.Login}")
        # отправляем лог в kafka
        send_log(
            StudentID=current_student.ID,
            StudentLogin=current_student.Login,
            action="ServerError",
            details={
                "DescriptionEvent": "Ошибка при обновлении пароля",
                "Reason": "UpdatePasswordFailed"
                # "Metadata": {"extra": "value"}  # по желанию
            }
        )
        raise errors.internal_server(error="UpdatePasswordFailed", message="Ошибка при обновлении пароля")


    logger.info(f"Пароль студента {current_student.Login} успешно обновлен!")
    send_log(
        StudentID=current_student.ID,
        StudentLogin=current_student.Login,
        action="PASSWORD_CHANGED",
        details={
            "DescriptionEvent": "Пароль успешно изменён",
            # "Metadata": {"extra": "value"}  # по желанию
        }
    )
    return {"message": "Пароль успешно изменён"}




"""Роли и разрешения"""

# /api/admin/roles (GET)
@admin_router.get("/roles", response_model=List[auth.Roles], summary="Получить список всех ролей", description="требуется токен авторизации")
def read_roles(db: Session = Depends(get_db), current_student=Depends(permission_required("admin_panel"))):
    logger.info(f"[ADMIN] Пользователь '{current_student.Login}' запросил список ролей")
    send_log(
        StudentID=current_student.ID,
        StudentLogin=current_student.Login,
        action="AdminViewRoles",
        details={
            "DescriptionEvent": "Запрос списка всех ролей"
        }
    )
    return get_all_roles(db)


# /api/admin/roles/{role_id}
@admin_router.get("/roles/{role_id}" , summary="Получить список разрешения для роли по её id")
def read_permissions_role(role_id: int, db: Session = Depends(get_db),
                            current_student=Depends(permission_required("admin_panel"))):
    # ищем роль по id
    role = get_role_id(db, role_id)
    if not role:
        logger.warning(f"[ADMIN] Пользователь '{current_student.Login}' попытался запросить несуществующую роль ID={role_id}")
        return errors.not_found(message=f"Не удалось найти роль с id {role_id}")
    # ищем разрешения для данной роли
    role_permissions = get_permission_role(db, role_id)
    if not role_permissions:
        logger.warning(f"[ADMIN] Пользователь '{current_student.Login}' запросил роль '{role.Name}' (ID={role_id}), но у неё нет разрешений")
        return errors.not_found(message=f"Разрешений у роли {role.Name} не найдено")

    role_permissions_dict = [dict(row) for row in role_permissions]
    # Формируем результат, для выбранной роли выводим
    role_info = {
        "role_id": role_permissions_dict[0]["RoleID"], # её id
        "role_name": role_permissions_dict[0]["RoleName"], # её имя
        "permissions": [
        row["PermissionName"] for row in role_permissions_dict
        ]
    }
    logger.info(f"[ADMIN] Пользователь '{current_student.Login}' запросил разрешения для роли '{role_info['role_name']}' (ID={role_id}), всего {len(role_info['permissions'])} разрешений")
    logger.debug(f"Детали разрешений роли: {role_info}")
    send_log(
        StudentID=current_student.ID,
        StudentLogin=current_student.Login,
        action="AdminViewRolePermissions",
        details={
            "DescriptionEvent": f"Запрос разрешений для роли '{role.Name}' (ID={role_id})",
            "PermissionsCount": len(role_info["permissions"])
        }
    )
    return role_info


# /api/admin/roles/{role_id}/assign-permission
@admin_router.post("/roles/{role_id}/assign-permission", summary="Назначить разрешения для роли",
                   description="""для выбранной роли по её id необходимо передать массив из id разрашений, данный массив и будет назначен для данной роли
                   список разрешений можно посмотреть по роуту: /api/admin/permission""")
def assign_permission_for_role (role_id: int,
                                data: auth.AssignPermissionsRequest,
                                db: Session = Depends(get_db),
                                current_student=Depends(permission_required("admin_panel"))):
    # ищем роль по id
    role = get_role_id(db, role_id)

    # находим текущие разрешения для данной роли
    permissions = get_permission_role(db,role_id)
    # из списка словарей достаем только сами разрешения
    current_permissions  =  set([row["PermissionID"] for row in permissions])
    # новые разрешения для роли
    new_permissions = set(data.permission_ids)
    # роли для добавления
    to_add = new_permissions - current_permissions
    # роли для удаления
    to_delete = current_permissions  - new_permissions
    # обновляем
    update_role_permissions(db, role_id, to_delete, to_add)

    logger.info(f"[ADMIN] Обновлены разрешения роли {role_id}: добавлены {to_add}, удалены {to_delete}")
    send_log(
        StudentID=current_student.ID,
        StudentLogin=current_student.Login,
        action="AssignPermissionsToRole",
        details={
            "DescriptionEvent": "Назначение разрешений для роли",
            "TargetRoleID": role_id,
            "TargetRoleName": role["Name"],
            "PermissionsAdded": list(to_add),
            "PermissionsRemoved": list(to_delete)
        }
    )
    return {
        "message": f"Роль '{role['Name']}' обновлена",
        "added": list(to_add),
        "removed": list(to_delete)
    }


# /api/admin/permission
@admin_router.get("/permission", response_model=List[auth.Permission], summary="Получить список всех разрешений", description="требуется токен авторизации")
def read_permission(db: Session = Depends(get_db), current_student=Depends(permission_required("admin_panel"))):

    logger.info(f"[ADMIN] Пользователь '{current_student.Login}' запросил список разрешений")
    send_log(
        StudentID=current_student.ID,
        StudentLogin=current_student.Login,
        action="AdminViewPermission",
        details={
            "DescriptionEvent": "Запрос списка всех разрешений"
        }
    )
    return get_all_permission(db)

# /api/admin/students
@admin_router.get(
    "/students",
    response_model=list[auth.StudentOut],
    summary="Получить список студентов в формате JSON (для админа)",
)
def read_all_students(db: Session = Depends(get_db), current_student=Depends(permission_required("admin_panel"))):
    return get_all_students(db)

# /api/admin/students/{studentID}/assign-role (POST)
@admin_router.post("/students/{studentID}/assign-role", summary="Назначить роль студенту по его id с указанием id роли",
                   description="""требуется токен авторизации  
                   studentID передается как path **/students/4**  
                   RoleID передается как query параметр **/assign-role?RoleID=2**""")
def assign_role_to_student(studentID: int,
                           params: auth.AssignRoleQuery = Depends(),
                           db: Session = Depends(get_db),
                           current_student=Depends(permission_required("admin_panel"))):
    # ищем роль по id
    role = get_role_id(db, params.RoleID)
    # ищем студента по id
    student= get_student_id(db, studentID)
    # обновляем роль
    update_role = assign_role(db, student.ID, role.RoleID)

    if update_role != 1:
        logger.warning(f"Не удалось обновить роль для студента {current_student.Login}")
        # отправляем лог в kafka
        send_log(
            StudentID=current_student.ID,
            StudentLogin=current_student.Login,
            action="ServerError",
            details={
                "DescriptionEvent": "Ошибка при назначении роли студенту",
                "Reason": "UpdateRoleFailed",
                "TargetStudentID": student.ID,
                "TargetRoleID": role.RoleID
                # "Metadata": {"extra": "value"}  # по желанию
            }
        )
        raise errors.internal_server(error="UpdateRoleFailed", message="Ошибка при назначении роли студенту")

    return  {"message": f" Студенту {student.Login} успешно назначена роль {role.Name}"}


# /admin/students/{student_id}/change-password
@admin_router.post("/students/{student_id}/change-password", summary = "Сменить пароль выбранного студента по его id",
                   description="пароль смены студента администратором")
def admin_change_password(
        student_id: int,
        data: auth.AdminChangePasswordRequest, # новый пароль
        db: Session = Depends(get_db),
        current_user=Depends(permission_required("admin_panel")) # Проверка на разрешение
):
    # ищем студента по id
    student = get_student_id(db, student_id)
    # хешуруем новый пароль
    new_hashed_password = hash_password(data.new_password)
    # обновляем пароль
    change_password(db, student.ID , new_hashed_password)

    logger.info(f"[ADMIN] Пользователь '{current_user.Login}' изменил пароль студента '{student.Login}' (ID: {student.ID})")
    send_log(
        StudentID=current_user.ID,
        StudentLogin=current_user.Login,
        action="AdminChangeStudentPassword",
        details={
            "DescriptionEvent": "Изменение пароля студента",
            "TargetStudentID": student.ID,
            "TargetStudentLogin": student.Login
        }
    )
    return  {"message": f"Пароль студента {student.Login} успешно изменён"}


"""роут с историей всех пользователя"""
# /api/admin/students/logs
@admin_router.get("/students/logs", summary = "Вывод истории действий всех пользователей",
                  description="""Роут доступен только пользователям с разрешением `admin_panel`.  
                  `limit`: Сколько логов вернуть (по умолчанию 50, максимум 10000)  
                  `offset`: Смещение от начала выборки""")
def get_logs(limit: int = Query(50, ge=1, le=10000),
             offset: int = Query(0, ge=0),
             db_log: Session = Depends(get_log_db),
             current_student=Depends(permission_required("admin_panel"))):

    # выбираем логи для пользователя по id
    logs = get_logs_all(db_log, limit=limit, offset=offset)

    logger.info(f"[LOGS] Пользователь '{current_student.Login}' запросил историю действий всех пользователей")
    send_log(
        StudentID=current_student.ID,
        StudentLogin=current_student.Login,
        action="ViewAllStudentLogs",
        details={
            "DescriptionEvent": "Запрос истории действий всех пользователей",
            "Limit": limit,
            "Offset": offset
        }
    )
    return logs

"""роут с историей пользователя"""
# /api/admin/students/{studentID}/logs
@admin_router.get("/students/{studentID}/logs", summary = "Вывод истории действий пользователя по его ID",
                  description="""данный роут работает для администратора (может смотреть логи любого студента по его id)  
                  и для текущего авторизованного пользователя (если совпадает его id с studentID из адреса)""")
def get_logs(studentID: int, db_log: Session = Depends(get_log_db), current_student=Depends(get_current_student)):

    # Если текущий пользователь не админ и пытается получить логи другого пользователя — ошибка
    if "admin_panel" not in current_student.permissions and current_student.ID != studentID:
        logger.warning(
            f"[LOGS] Пользователь '{current_student.Login}' пытался получить логи другого пользователя с ID {studentID}")
        raise errors.access_denied(message="Доступ к логам другого пользователя запрещён")

    # выбираем логи для пользователя по id
    logs = get_logs_student(db_log, studentID)

    logger.info(f"[LOGS] Пользователь '{current_student.Login}' запросил историю действий студента с ID {studentID}")
    send_log(
        StudentID=current_student.ID,
        StudentLogin=current_student.Login,
        action="ViewStudentLogs",
        details={
            "DescriptionEvent": "Запрос истории действий студента",
            "TargetStudentID": studentID
        }
    )
    return logs


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
'''Домашняя страница (после авторизации)
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
'''
# /home/login_in/ (POST)
'''Страница входа (отправка данных)
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
'''




# /login/me
'''Доступ только для пользователей
@auth_router.get("/me", summary="Получить информацию о текущем студенте")
def read_students_me(current_student: Student = Depends(get_current_student)):
    return {
        "id": current_student.ID,
        "login": current_student.Login,
        "email": current_student.Email if hasattr(current_student, "Email") else None
    }
'''
# /admin/ @
'''Роут, доступный только администраторам
@admin_router.get("/", response_class=HTMLResponse)
def admin_dashboard(
    request: Request,
    current_student=Depends(permission_required("admin_panel"))
):
    return templates.TemplateResponse("Admin/dashboard.html", {
        "request": request,
        "student": current_student
    })
'''

'''вывод списка студентов в формате JSON
# /api/admin/api/students @
@admin_router.get("/students", summary="Получить список студентов в формате JSON")
def api_get_students(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM Students")).fetchall()
    students = [dict(row._mapping) for row in result]
    return JSONResponse(content=jsonable_encoder(students))
'''
'''
summary="Получить список студентов в формате JSON",
                  description="""Если передан параметр **subjectID**, то возвращаются категории только для указанного предмета.  
                      Если параметр не передан, возвращаются задачи по всем предметам.  
                      **subjectID** передается как Query-параметр   
                              "`/api/tasks` — все задачи"  
                              "`/api/tasks?subjectID=10` — задачи для предмета с ID 10"  
                              так же необходимо передавать в заголовке **токен** пользователя
                      """
'''
# /api/admin/api/students/{StudentID}/subtasks
'''Возвращем список задач выбранного студента в формате JSON'''
@admin_router.get("/students/{StudentID}/subtasks", summary="Получить список задач выбранного студента в формате JSON")
def api_get_student_subtasks(StudentID: int, db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM StudentTasks WHERE StudentID = :StudentID"), {"StudentID": StudentID}).fetchall()
    subtasks = [dict(row._mapping) for row in result]
    #print(subtasks)
    return JSONResponse(content=jsonable_encoder(subtasks))

# /admin/ListStudents @
'''Возвращем html страницу со списком всех студентов
@admin_router.get("/ListStudents",  response_class=HTMLResponse)
def admin_read_all_students(
        request: Request,
        current_student=Depends(get_current_student_or_redirect)):
    logger.debug("Получен запрос на список студентов")

    # Проверям что пользователь авторизован и отправляем на страницу с логином
    if isinstance(current_student, RedirectResponse):
        return current_student
    return templates.TemplateResponse("Admin/ListStudents.html", {"request": request, "student": current_student})
'''







