from Service.config_app import *
from Service.dependencies import get_db
from Service.Models import Student
from Service.Schemas.auth import StudentOut, StudentAuth, StudentBase, StudentCreate
from Service.Security.token import SECRET_KEY, ALGORITHM
from Service.Crud import errors,general

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
from sqlalchemy.orm import Session

import logging

# Crud\auth.py


logger = logging.getLogger(__name__) # создание логгера для текущего модуля



security = HTTPBasic()
"""функция для проверки пароля в swagger"""
def get_swagger_user(
    credentials: HTTPBasicCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    logging.info(f"Swagger auth attempt: username={credentials.username}")
    user = db.query(Student).filter(Student.Login == credentials.username).first()
    if not user or not verify_password(credentials.password, user.Password):
        logging.warning(f"User {credentials.username} not found in DB or Invalid password")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учетные данные",
            headers={"WWW-Authenticate": "Basic"},
        )
    logging.info(f"User {credentials.username} authenticated successfully")
    return user



# шифрование пароля
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
# Функция для хеширования пароля (принимает обычный и возвращает хэшированный)
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Функция для проверки пароля (сравнивает введённый пользователем пароль и хеш из базы,)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Создание пароля вручную:
'''
raw_password = "standart_password"
raw_password = "standart_password"
hashed_password = hash_password(raw_password)
print("Хешированный пароль:", hashed_password)
#$pbkdf2-sha256$29000$HWPMube2tnYuZYwRwngPQQ$eSDzbZ3puIYCkdzcU94.2a5.ZvXUWXlIGjuSuM4ij/Y
'''





'''функция получения студента по токену (токен приходит с фронта в заголовке)'''
def get_current_student(request: Request, db: Session = Depends(get_db)) -> StudentOut:
    # Получение токена из куки:
    token = request.headers.get("Authorization") or request.cookies.get("access_token")
    #print("ACCESS TOKEN >>>", token)
    ip = request.headers.get("X-Forwarded-For") or request.client.host
    user_agent = request.headers.get("User-Agent")
    if not token:
        logger.warning(f"[AUTH] Отсутствует токен. IP: {ip}, UA: {user_agent}")
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
        logger.warning(f"[AUTH] Неверная схема токена. IP: {ip}, UA: {user_agent}, TOKEN: {token}")
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
        payload = jwt.decode(param, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": True})
        login: str = payload.get("sub")
        if login is None:
            logger.warning(f"[AUTH] Токен не содержит логин. IP: {ip}, UA: {user_agent}")
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
        logger.warning(f"[AUTH] Срок действия токена истёк. IP: {ip}, UA: {user_agent}")
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
        logger.warning(f"[AUTH] JWT ошибка. IP: {ip}, UA: {user_agent}, Ошибка: {e}")
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
    student = get_student_by_login(db, login)
    #print(student)
    if student is None:
        logger.warning(f"Извлеченный из токена логин не найден в бд: {login}")
        send_log(
            StudentID=None,  # Или 0
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
    permissions = get_permission_role(db, student["RoleID"])
    student = dict(student)
    student["permissions"] = [row["PermissionName"] for row in permissions]
    # student["BirthDate"] = student["BirthDate"].isoformat()

    '''if isinstance(student["BirthDate"], datetime):
        student["BirthDate"] = student["BirthDate"].date()'''
    return StudentOut(**dict(student))

"""НЕ ИСПОЛЬЗУЕТСЯ, сделано через разрешения permission_required"""
def admin_required(student: StudentOut = Depends(get_current_student)):
    if student.RoleName != "Админ":
        raise errors.access_denied(message="Только для администраторов")
    return student


'''Функция для проверки разрешения у авторизованного студента'''
def permission_required(permission_name: str):
    def decorator(student=Depends(get_current_student)):
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
'''Проверяет наличия разрешения у переданного ей пользователя'''
def check_permission(student, permission_name: str):
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
"""Универсальная функция получения студента"""
def get_student_by_field(db: Session, field_name: str, value: str):
    allowed_fields = {"ID", "Login", "Email", "Phone"} # белый список (он же помогает от sql инъекций)
    if field_name not in allowed_fields:
        raise ValueError(f"Недопустимое поле для поиска студента: {field_name}")

    if field_name == "ID":
        try:
            value = int(value)
        except ValueError:
            raise errors.bad_request(message=f"Некорректный ID: {value}")

    return general.run_query_select(
        db,
        query=f"""SELECT s.*, r.Name as RoleName FROM Students s
        LEFT JOIN Roles r ON s.RoleID = r.RoleID
        WHERE s.{field_name} = :value""",
        params={"value": value},
        mode="mappings_first",
        error_message=f"Ошибка при получении студента по {field_name}: {value}"
    )

"""Выбор студента из базы по его логину (Аутентификация)"""
def get_student_by_login(db: Session, login: str):
    return general.run_query_select(
        db,
        query="""
                SELECT s.*, r.Name as RoleName
                FROM Students s
                LEFT JOIN Roles r ON s.RoleID = r.RoleID
                WHERE s.Login = :login
            """,
        params={"login": login},
        mode="mappings_first",
        error_message=f"Ошибка при получении студента: {login}"
    )


"""Выбор студента из базы по его логину (Аутентификация)"""
def get_student_by_email(db: Session, email: str):
    return general.run_query_select(
        db,
        query="""
                SELECT * FROM Students 
                WHERE Email = :email
            """,
        params={"email": email},
        mode="mappings_first",
        error_message=f"Ошибка при получении студента по email: {email}"
    )



def add_new_register_student(db: Session, params: dict):
    return general.run_query_insert(
        db,
        query="""
        Insert Students (Login, Email, Password,IsConfirmed)
        VALUES (:Login, :Email, :Password, :IsConfirmed)
        """,
        params=params,
        error_message="Ошибка добавления нового студента (через регистрацию)"
    )

'''функция подтвержения email'''
def confirm_student_email(db: Session, params: dict):
    return general.run_query_update(
        db,
        query="""UPDATE Students SET IsConfirmed = 1, RegisterDate = :now WHERE Email = :email AND IsConfirmed = 0""",
        params=params,
        error_message="Ошибка добавления нового студента (через регистрацию)"
    )

'''Создаем временный токен для сброса пароля и деактивируем все предыдущие'''
def save_password_reset_token(db: Session, student_id: int, token: str, expires_at: datetime):
    # 1. Деактивируем старые токены
    general.run_query_update(
        db,
        query="""
            UPDATE PasswordResetTokens
            SET Used = 1
            WHERE StudentID = :student_id AND Used = 0
        """,
        params={"student_id": student_id},
        error_message="Ошибка при пометке старых токенов как использованных"
    )

    # 2. Вставляем новый токен
    general.run_query_insert(
        db,
        query="""
                INSERT INTO PasswordResetTokens (StudentID, Token, ExpiresAt)
                VALUES (:student_id, :token, :expires_at)
            """,
        params={
            "student_id": student_id,
            "token": token,
            "expires_at": expires_at
        },
        error_message="Ошибка при сохранении токена сброса пароля"
    )

'''Функция получения токена для сброса пароля'''
def get_token_record(db: Session, token: str):
    query = """
        SELECT ID, StudentID, Token, ExpiresAt, Used
        FROM PasswordResetTokens
        WHERE Token = :token
    """
    record = general.run_query_select(
        db,
        query=query,
        params={"token": token},
        mode="mappings_first",  # Получаем один словарь с данными
        required=False
    )
    return record

'''Функция отмечает токен сброса пароля как использованный'''
def mark_token_used(db: Session, token: str):
    query = """
        UPDATE PasswordResetTokens
        SET Used = 1
        WHERE Token = :token
    """
    updated_rows = general.run_query_update(
        db,
        query=query,
        params={"token": token},
        error_message="Ошибка при пометке токена как использованного"
    )
    return updated_rows

"""Выбор из базы разрешений для роли по её ID """
def get_permission_role(db: Session, RoleID: int):
    return general.run_query_select(
        db,
        query="""
                SELECT p.Name
                FROM RolePermissions rp
                JOIN Permissions p ON rp.PermissionID = p.PermissionID
                WHERE rp.RoleID = :role_id
                """,
        params={"role_id": RoleID},
        mode="scalars_all",
        error_message=f"Ошибка при получения разрешений для роли с id:{RoleID}"
    )


"""Смена пароля пользователя"""
def change_password(db: Session, student_ID: int, new_password: str):
    return general.run_query_update(
        db,
        query="""
                update Students 
                set Password = :new_password 
                where ID = :id
                """,
        params={"id": student_ID, "new_password": new_password},
        error_message=f"Ошибка обновления пароля для студента с id:{student_ID}"
    )

def get_all_roles(db: Session):
    return general.run_query_select(
        db,
        query= """SELECT * FROM Roles""",
        mode="mappings_all",
        params= None,
        error_message=f"Ошибка при получения ролей"
    )

def get_all_permission(db: Session):
    return general.run_query_select(
        db,
        query= """SELECT * FROM Permissions""",
        mode="mappings_all",
        params= None,
        error_message=f"Ошибка при получения разрешений"
    )

def get_role_id(db: Session, RoleID: int):
    return general.run_query_select(
        db,
        query= """SELECT * FROM Roles where RoleID = :role_id""",
        mode="mappings_first",
        params= {"role_id": RoleID},
        required=True,
        error_message=f"Ошибка при получения роли с id={RoleID} "
    )

def get_permission_role(db: Session, RoleID: int):
    return general.run_query_select(
        db,
        query= """SELECT r.RoleID, r.Name as RoleName, p.PermissionID, p.Name as PermissionName
                                            FROM RolePermissions rp
                                            JOIN Roles r ON rp.RoleID = r.RoleID
                                            JOIN Permissions p ON rp.PermissionID = p.PermissionID
                                            WHERE r.RoleID = :role_id
                                            ORDER BY r.RoleID""",
        mode="mappings_all",
        params= {"role_id": RoleID},
        #required=True,
        error_message=f"Ошибка при получения разрешений роли с id={RoleID} "
    )
''' Назначение роли студенту'''
def assign_role(db: Session, student_id: int, role_id: int):
    return general.run_query_update(
        db,
        query= """update students set RoleID = :role_id where ID = :student_id""",
        params= {"role_id":role_id, "student_id": student_id},
        error_message=f"Ошибка при назначении роли с id={role_id} для студента с id={student_id}"
    )

def update_role_permissions (db: Session, role_id: int, to_delete: set, to_add: set):
    try:
        # удаляем разрешения, которые больше не нужны
        for permission in to_delete:
            general.run_query_delete(
                db,
                query="DELETE FROM RolePermissions WHERE RoleID = :role_id AND PermissionID = :permission",
                params={"role_id": role_id, "permission": permission},
                error_message=f"Ошибка при удалении разрешения {permission} у роли {role_id}",
                commit=False  # добавим этот флаг
            )

        # добавляем новые разрешения
        for permission in to_add:
            general.run_query_insert(
                db,
                query="INSERT INTO RolePermissions (RoleID, PermissionID) VALUES (:role_id, :permission)",
                params={"role_id": role_id, "permission": permission},
                error_message=f"Ошибка при добавлении разрешения {permission} роли {role_id}",
                commit=False
            )
        db.commit()

    except SQLAlchemyError:
        db.rollback()
        logger.exception(f"[DB ERROR] Ошибка при обновлении разрешений роли")
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

def get_logs_all(db: Session, limit: int = 50, offset: int = 0):
    return general.run_query_select(
        db,
        query= """SELECT * FROM StudentActionLogs
            ORDER BY EventTime DESC
            OFFSET :offset ROWS
            FETCH NEXT :limit ROWS ONLY""",
        mode="mappings_all",
        params= {"limit": limit, "offset": offset},
        error_message=f"Ошибка при получении истории действий пользователей"
    )

def get_logs_student(db: Session, studentID: int):
    return general.run_query_select(
        db,
        query= """SELECT TOP 50 * FROM StudentActionLogs 
        WHERE StudentID = :student_id
        ORDER BY EventTime DESC
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