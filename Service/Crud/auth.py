
from utils.config import settings

from Service.Database import get_db
from Service.Models import Student
from Service.Schemas.auth import StudentOut, StudentAuth, StudentBase, StudentCreate

from utils import errors,general

#from Service.Crud.students import get_student_by_login
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, HTTPBasic, HTTPBasicCredentials
from Service.producer import send_log
import uuid
from datetime import datetime
from jose.exceptions import ExpiredSignatureError
from passlib.context import CryptContext # объект, который помогает удобно хешировать и проверять пароли.
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_401_UNAUTHORIZED
from typing import Optional
from sqlalchemy.exc import SQLAlchemyError
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select

import logging
logger = logging.getLogger(__name__) # создание логгера для текущего модуля
# Crud\auth.py




# TODO переведен на асинхронный postgres (hash_password не трогаем так как это CPU-bound операции.

security = HTTPBasic()

async def get_swagger_user(
    credentials: HTTPBasicCredentials = Depends(security),
    db = Depends(get_db),
):
    """функция для проверки пароля в swagger"""
    logging.info(f"Вход в Swagger : username={credentials.username}")
    student = await get_student_by_login(db=db, login=credentials.username)
    logging.info(f"student={student}")
    if not student or not verify_password(credentials.password, student["Password"]):
        logging.warning(f"User {credentials.username} not found or invalid password")
        raise errors.unauthorized(message="Неверные учётные данные")

    logging.info(f"User {credentials.username} authenticated successfully")
    return student



# шифрование пароля
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
# Функция для хеширования пароля (принимает обычный и возвращает хэшированный)
def hash_password(password: str) -> str:
    logging.info(f"Хэшируем пароль")
    return pwd_context.hash(password)

# Функция для проверки пароля (сравнивает введённый пользователем пароль и хеш из базы,)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    logging.info(f"Проверяем хэш пароля")
    return pwd_context.verify(plain_password, hashed_password)

# Создание пароля вручную:
'''
raw_password = "standart_password"

raw_password = "1111"
hashed_password = hash_password(raw_password)
print("Хешированный пароль:", hashed_password)
#$pbkdf2-sha256$29000$HWPMube2tnYuZYwRwngPQQ$eSDzbZ3puIYCkdzcU94.2a5.ZvXUWXlIGjuSuM4ij/Y (standart_password)
$pbkdf2-sha256$29000$dm7NmZNSqpWyVmqNEYJQyg$Z6gDFsYkqd5xLDxIytx2n5C9moMIc4voTVKqwVUwj68  (1111)
'''


async def get_hash_password(db: AsyncSession, student_id: int):
    """Получение хэш пароля из базы"""
    logging.info(f"Проверяем хэш пароля")

    return await general.run_query_select(
        db,
        query="""
                select "Password" from "Students" where "ID" = :student_id;
            """,
        params={"student_id": student_id},
        mode="scalar",
        error_message=f"Ошибка при получении хэш пароля студента с id={student_id}"
    )




async def get_current_student(request: Request, db = Depends(get_db)) -> StudentOut:
    '''функция получения студента по токену (токен приходит с фронта в заголовке)'''
    # Получение токена из куки:
    token = request.headers.get("Authorization") or request.cookies.get("access_token")
    #print("ACCESS TOKEN >>>", token)
    ip = request.headers.get("X-Forwarded-For") or request.client.host
    user_agent = request.headers.get("User-Agent")
    if not token:
        logging.warning(f"[AUTH] Отсутствует токен. IP: {ip}, UA: {user_agent}")
        send_log(
            StudentID=0,  # Или 0
            StudentLogin="Unknown",
            action="TOKEN_ERROR",
            details={
                "DescriptionEvent": "Отсутствует токен",
                "Reason": "TokenMissing",
                "IPAddress": ip,
                "UserAgent": user_agent
            }
        )
        raise errors.unauthorized (error="TokenMissing", message="Отсутствует токен")

    # Проверка и парсинг схемы: "Bearer <token>"
    scheme, _, param = token.partition(" ")
    if scheme.lower() != "bearer" or not param:
        logging.warning(f"[AUTH] Неверная схема токена. IP: {ip}, UA: {user_agent}, TOKEN: {token}")
        send_log(
            StudentID=0,
            StudentLogin="Unknown",
            action="TOKEN_ERROR",
            details={
                "DescriptionEvent": "Неверная схема токена",
                "Reason": "TokenMalformed",
                "IPAddress": ip,
                "UserAgent": user_agent,
                #"Metadata": {"raw_token": token}
            }
        )
        raise errors.unauthorized(error="TokenMalformed", message="Неверная схема аутентификации")

    try:
        #Расшифровка JWT токена и получение логина и проверка срока его действия
        payload = jwt.decode(param, settings.SECRET_KEY, algorithms=[settings.ALGORITHM], options={"verify_exp": True})
        login: str = payload.get("sub")
        if login is None:
            logging.warning(f"[AUTH] Токен не содержит логин. IP: {ip}, UA: {user_agent}")
            send_log(
                StudentID=0,
                StudentLogin="Unknown",
                action="TOKEN_ERROR",
                details={
                    "DescriptionEvent": "Токен не содержит логин",
                    "Reason": "TokenInvalidPayload",
                    "IPAddress": ip,
                    "UserAgent": user_agent,
                    #"Metadata": {"payload": payload}
                }
            )
            raise errors.unauthorized(error="TokenInvalidPayload", message="Некорректный токен")

    except ExpiredSignatureError:
        logging.warning(f"[AUTH] Срок действия токена истёк. IP: {ip}, UA: {user_agent}")
        send_log(
            StudentID=0,
            StudentLogin="Unknown",
            action="TOKEN_ERROR",
            details={
                "DescriptionEvent": "Срок действия токена истёк",
                "Reason": "TokenExpired",
                "IPAddress": ip,
                "UserAgent": user_agent,
                #"Metadata": {"token": param}
            }
        )
        raise errors.unauthorized(error="TokenExpired", message="Срок действия токена истёк")

    except JWTError as e:
        logging.warning(f"[AUTH] JWT ошибка. IP: {ip}, UA: {user_agent}, Ошибка: {e}")
        send_log(
            StudentID=0,
            StudentLogin="Unknown",
            action="TOKEN_ERROR",
            details={
                "DescriptionEvent": "Недействительный токен",
                "Reason": "TokenInvalid",
                "IPAddress": ip,
                "UserAgent": user_agent,
                #"Metadata": {"token": param}
            }
        )
        raise errors.unauthorized(error="TokenInvalid", message="Недействительный токен")
    # ищем студента в базе по логину
    student = await get_student_by_login(db=db, login=login)
    #print(student)
    if student is None:
        logging.warning(f"Извлеченный из токена логин не найден в бд: {login}")
        send_log(
            StudentID= None,  # Или 0
            StudentLogin=login,
            action="LoginFailed",
            details={
                "DescriptionEvent": "Неуспешный вход",
                "Reason": "StudentNotFound",
                "IPAddress": ip,
                "UserAgent": user_agent
            }
        )
        raise errors.unauthorized(error="StudentNotFound", message="Пользователь с таким логином не найден")

    #смотрим разрешения для данного студента по его роли
    permissions = await get_permission_role(db, student["RoleID"])
    student = dict(student)
    student["permissions"] = [row["PermissionName"] for row in permissions]
    # student["BirthDate"] = student["BirthDate"].isoformat()
    logging.info(f"Получение текущего студента: {student}") # TODO может бть ошибка!
    '''if isinstance(student["BirthDate"], datetime):
        student["BirthDate"] = student["BirthDate"].date()'''
    return StudentOut(**dict(student))

"""НЕ ИСПОЛЬЗУЕТСЯ, сделано через разрешения permission_required"""
async def admin_required(student: StudentOut = Depends(get_current_student)):
    if student.RoleName != "Админ":
        logger.warning(f"Доступ закрыт. Только для администраторов!")
        raise errors.access_denied(message="Только для администраторов")
    return student


async def superadmin_required(current_user=Depends(get_current_student)):
    '''проверка на суперадмина'''
    if "SuperAdmin" not in current_user.Roles:  # предполагаем, что current_user.Roles — список ролей
        logger.warning(f"Доступ закрыт. Только для Супер Админа!")
        raise errors.access_denied(message="Только для Супер Админа")
    logger.debug(f"проверка студента {current_user.Login} на суперадмина")
    return current_user

async def can_edit_admin(target_role_id: int, db = Depends(get_db), current_student=Depends(get_current_student)):
    logger.debug(f"проверка изменения роли на role_id:{target_role_id} суперадмина и админов) ")
    target_role = await get_role_id(db, target_role_id)  # возвращает объект роли с Name

    # Проверяем, если цель — Админ, а текущий не СуперАдмин
    if target_role.Name == "Админ" and current_student.RoleName != "SuperAdmin":
        logger.warning(f"Доступ закрыт. Только для Супер Админа!")
        raise errors.access_denied(message="Вы не можете изменять админов")

    # Проверяем, если цель — SuperAdmin, а текущий не СуперАдмин
    if target_role.Name == "SuperAdmin" and current_student.RoleName != "SuperAdmin":
        logger.warning(f"Вы не можете изменять супер-админов!")
        raise errors.access_denied(message="Вы не можете изменять супер-админов")

    return True


# TODO поменяли функция после перехода на асинхронку
def permission_required(permission_name: str):
    """Функция для проверки разрешения у авторизованного студента"""
    async def decorator(student=Depends(get_current_student)):
        if permission_name not in student.permissions:
            logger.warning(f"[PERMISSION] '{student.Login}' без разрешения '{permission_name}'")

            send_log(
                StudentID=student.ID,
                StudentLogin=student.Login,
                action="PermissionDenied",
                details={
                    "DescriptionEvent": "Попытка доступа без разрешения",
                    "Reason": f"MissingPermission:{permission_name}"
                }
            )
            raise errors.access_denied(message="Недостаточно прав")

        logger.info(f"[PERMISSION] '{student.Login}' успешно прошёл проверку на '{permission_name}'")

        send_log(
            StudentID=student.ID,
            StudentLogin=student.Login,
            action="PermissionGranted",
            details={
                "DescriptionEvent": "Успешная проверка разрешения",
                "Permission": permission_name
            }
        )
        return student
    return decorator


# Зависимость (пока не используется)
async def check_permission(student, permission_name: str):
    '''Проверяет наличия разрешения у переданного ей пользователя'''
    if permission_name not in student.permissions:
        logger.warning(f"[PERMISSION] '{student.Login}' без разрешения '{permission_name}'")

        send_log(
            StudentID=student.ID,
            StudentLogin=student.Login,
            action="PermissionDenied",
            details={
                "DescriptionEvent": "Попытка доступа без разрешения",
                "Reason": f"MissingPermission:{permission_name}"
            }
        )
        raise errors.access_denied(message="Недостаточно прав")
    logger.info(f"[PERMISSION] '{student.Login}' успешно прошёл проверку на '{permission_name}'")

    send_log(
        StudentID=student.ID,
        StudentLogin=student.Login,
        action="PermissionGranted",
        details={
            "DescriptionEvent": "Успешная проверка разрешения",
            "Permission": permission_name
        }
    )


async def get_student_by_field(db: AsyncSession, field_name: str, value: str):
    """Универсальная функция получения студента"""
    allowed_fields = {"ID", "Login", "Email", "Phone"} # белый список (он же помогает от sql инъекций)
    if field_name not in allowed_fields:
        logger.warning(f"Недопустимое поле для поиска студента: {field_name}")
        raise errors.bad_request(message=f"Недопустимое поле для поиска студента: {field_name}")

    if field_name == "ID":
        try:
            value = int(value)
        except ValueError:
            logger.exception(f"Некорректный ID: {value}")
            raise errors.bad_request(message=f"Некорректный ID: {value}")
    logger.info(f"Поиск студента: field={field_name}, value={value}")
    return await general.run_query_select(
        db,
        query=f"""SELECT s.*, r."Name" as "RoleName" FROM "Students" s
        LEFT JOIN "Roles" r ON s."RoleID" = r."RoleID"
        WHERE s."{field_name}" = :value;""",
        params={"value": value},
        mode="mappings_first",
        error_message=f"Ошибка при получении студента по {field_name}: {value}"
    )


async def get_student_by_login(db: AsyncSession, login: str):
    """Выбор студента из базы по его логину (Аутентификация)"""
    logger.debug(f"Поиск студента по логину: {login}")
    return await general.run_query_select(
        db,
        query="""
                SELECT s.*, r."Name" as "RoleName"
                FROM "Students" s
                LEFT JOIN "Roles" r ON s."RoleID" = r."RoleID"
                WHERE s."Login" = :login;
            """,
        params={"login": login},
        mode="mappings_first",
        error_message=f"Ошибка при получении студента: {login}"
    )



async def get_student_by_email(db: AsyncSession, email: str):
    """Выбор студента из базы по его логину (Аутентификация)"""
    logger.debug(f"Поиск студента по email: {email}")
    return await general.run_query_select(
        db,
        query="""
                SELECT * FROM "Students" 
                WHERE "Email" = :email;
            """,
        params={"email": email},
        mode="mappings_first",
        error_message=f"Ошибка при получении студента по email: {email}"
    )

async def add_new_register_student(db: AsyncSession, params: dict):
    logger.debug(f"Добавляем нового студента params: {params}")
    return await general.run_query_insert(
        db,
        query="""
        Insert INTO "Students" ("Login", "Email", "Password","IsConfirmed")
        VALUES (:Login, :Email, :Password, :IsConfirmed);
        """,
        params=params,
        error_message="Ошибка добавления нового студента (через регистрацию)"
    )


async def confirm_student_email(db: AsyncSession, params: dict):
    '''функция подтвержения email'''
    logger.debug(f"Обновляем информацию о подтвержденном emai, params={params}")
    return await general.run_query_update(
        db,
        query="""UPDATE "Students" SET "IsConfirmed" = True, "RegisterDate" = :now 
        WHERE "Email" = :email AND "IsConfirmed" = False;""",
        params=params,
        error_message="Ошибка добавления нового студента (через регистрацию)"
    )


async def save_password_reset_token(db: AsyncSession, student_id: int, token: str, expires_at: datetime):
    '''Создаем временный токен для сброса пароля и деактивируем все предыдущие'''
    logger.debug(f"Создание временного токена для сброса пароля и деактивация всех предыдущих для студента с id={student_id}")
    # 1. Деактивируем старые токены
    await general.run_query_update(
        db,
        query="""
            UPDATE "PasswordResetTokens"
            SET "Used" = TRUE
            WHERE "StudentID" = :student_id AND "Used" = FALSE;
        """,
        params={"student_id": student_id},
        error_message="Ошибка при пометке старых токенов как использованных"
    )

    # 2. Вставляем новый токен
    await general.run_query_insert(
        db,
        query="""
                INSERT INTO "PasswordResetTokens" ("StudentID", "Token", "ExpiresAt")
                VALUES (:student_id, :token, :expires_at);
            """,
        params={
            "student_id": student_id,
            "token": token,
            "expires_at": expires_at
        },
        error_message="Ошибка при сохранении токена сброса пароля"
    )


async def get_token_record(db: AsyncSession, token: str):
    '''Функция получения токена для сброса пароля'''
    logger.debug(f"функция get_token_record")
    query = """
        SELECT "ID", "StudentID", "Token", "ExpiresAt", "Used"
        FROM "PasswordResetTokens"
        WHERE "Token" = :token;
    """
    record = await general.run_query_select(
        db,
        query=query,
        params={"token": token},
        mode="mappings_first",  # Получаем один словарь с данными
        required=False
    )
    return record


async def mark_token_used(db: AsyncSession, token: str):
    '''Функция отмечает токен сброса пароля как использованный'''
    logger.debug(f"Помечаем токен сброса пароля как использованный")
    query = """
        UPDATE "PasswordResetTokens"
        SET "Used" = 1
        WHERE "Token" = :token;
    """
    updated_rows = await general.run_query_update(
        db,
        query=query,
        params={"token": token},
        error_message="Ошибка при пометке токена как использованного"
    )
    return updated_rows


async def get_permission_role(db: AsyncSession, RoleID: int):
    """Выбор из базы разрешений для роли по её ID """
    logger.debug(f"Получаем из базы разрешений для роли по её ID={RoleID}")
    return await general.run_query_select(
        db,
        query="""
                SELECT p."Name"
                FROM "RolePermissions" rp
                JOIN "Permissions" p ON rp."PermissionID" = p."PermissionID"
                WHERE rp."RoleID" = :role_id;
                """,
        params={"role_id": RoleID},
        mode="scalars_all",
        error_message=f"Ошибка при получения разрешений для роли с id:{RoleID}"
    )



async def change_password(db: AsyncSession, student_ID: int, new_password: str):
    """Смена пароля пользователя"""
    logger.debug(f"Меняем пароль пользователя с id:{student_ID}")
    return await general.run_query_update(
        db,
        query="""
                update "Students" 
                set "Password" = :new_password 
                where "ID" = :id;
                """,
        params={"id": student_ID, "new_password": new_password},
        error_message=f"Ошибка обновления пароля для студента с id:{student_ID}"
    )

async def get_all_roles(db: AsyncSession):
    logger.debug(f"Получаем все роли")
    return await general.run_query_select(
        db,
        query= '''SELECT * FROM "Roles"''',
        mode="mappings_all",
        params= None,
        error_message=f"Ошибка при получения ролей"
    )

async def get_all_permission(db: AsyncSession):
    logger.debug(f"Получаем все разрешения")
    return await general.run_query_select(
        db,
        query= '''SELECT * FROM "Permissions"''',
        mode="mappings_all",
        params= None,
        error_message=f"Ошибка при получения разрешений"
    )

async def get_role_id(db: AsyncSession, RoleID: int):
    logger.debug(f"Получаем роль по её id:{RoleID}")
    return await general.run_query_select(
        db,
        query= '''SELECT * FROM "Roles" where "RoleID" = :role_id;''',
        mode="mappings_first",
        params= {"role_id": RoleID},
        required=True,
        error_message=f"Ошибка при получения роли с id={RoleID} "
    )

async def get_permission_role(db: AsyncSession, RoleID: int):
    logger.debug(f"Получаем разрешения для роли по её id:{RoleID}")
    return await general.run_query_select(
        db,
        query= """SELECT r."RoleID", r."Name" as "RoleName", p."PermissionID", p."Name" as "PermissionName"
                                            FROM "RolePermissions" rp
                                            JOIN "Roles" r ON rp."RoleID" = r."RoleID"
                                            JOIN "Permissions" p ON rp."PermissionID" = p."PermissionID"
                                            WHERE r."RoleID" = :role_id
                                            ORDER BY r."RoleID";
                                            """,
        mode="mappings_all",
        params= {"role_id": RoleID},
        #required=True,
        error_message=f"Ошибка при получения разрешений роли с id={RoleID} "
    )

async def assign_role(db: AsyncSession, student_id: int, role_id: int):
    ''' Назначение роли пользователю'''
    logger.debug(f"Назначаем роль role_id={role_id} студенту student_id={student_id}")
    return await general.run_query_update(
        db,
        query= """update "Students" set "RoleID" = :role_id where "ID" = :student_id;""",
        params= {"role_id":role_id, "student_id": student_id},
        error_message=f"Ошибка при назначении роли с id={role_id} для студента с id={student_id}"
    )

async def update_role_permissions (db: AsyncSession, role_id: int, to_delete: set, to_add: set):
    try:
        # удаляем разрешения, которые больше не нужны
        for permission in to_delete:
            await general.run_query_delete(
                db,
                query='''DELETE FROM "RolePermissions" WHERE "RoleID" = :role_id AND "PermissionID" = :permission;''',
                params={"role_id": role_id, "permission": permission},
                error_message=f"Ошибка при удалении разрешения {permission} у роли {role_id}",
                commit=False  # добавим этот флаг
            )

        # добавляем новые разрешения
        for permission in to_add:
            await general.run_query_insert(
                db,
                query='''INSERT INTO "RolePermissions" ("RoleID", "PermissionID") VALUES (:role_id, :permission);''',
                params={"role_id": role_id, "permission": permission},
                error_message=f"Ошибка при добавлении разрешения {permission} роли {role_id}",
                commit=False
            )
        db.commit()
        logger.debug(f"Обновили разрешения для роли с role_id={role_id} удалили: {to_delete}, добавили {to_add}")
    except SQLAlchemyError:
        await db.rollback()
        logger.exception(f"[DB ERROR] Ошибка при обновлении разрешений роли с role_id={role_id} к удалению: {to_delete}, к добавлению {to_add}")
        send_log(
            StudentID=0,
            StudentLogin="System",
            action="AssignPermissionsToRoleFailed",
            details={
                "DescriptionEvent": "Ошибка при обновлении разрешений у роли",
                "Reason": "UpdatePermissionsFailed",
                "TargetRoleID": role_id,
                "PermissionsToAdd": list(to_add),
                "PermissionsToRemove": list(to_delete)
            }
        )
        raise errors.internal_server(message="Ошибка при обновлении разрешений роли")

async def get_logs_all(db: AsyncSession, limit: int = 50, offset: int = 0):
    logger.debug(f"Получение всех логов |  limit={limit} | offset={offset}")
    return await general.run_query_select(
        db,
        query= """SELECT * FROM "StudentActionLogs"
                    ORDER BY "EventTime" DESC
                    OFFSET :offset
                    LIMIT :limit;""",
        mode="mappings_all",
        params= {"limit": limit, "offset": offset},
        error_message=f"Ошибка при получении истории действий пользователей"
    )

async def get_logs_student(db: AsyncSession, studentID: int):
    logger.debug(f"Получение логов студента id={studentID}")
    return await general.run_query_select(
        db,
        query= """SELECT * FROM "StudentActionLogs"
                WHERE "StudentID" = :student_id ORDER BY "EventTime" DESC
                LIMIT 50;
        """,
        mode="mappings_all",
        params= {'student_id': studentID},
        error_message=f"Ошибка при получения истории действий пользователя"
    )




'''
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# Функция для получения токена из заголовка Authorization
def get_token_from_header(authorization: str = Depends(oauth2_scheme)) -> str:
    return authorization
'''