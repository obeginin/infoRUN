from Service.config import *
from Service.dependencies import get_db
from Service.Models import Student
from Service.Schemas.auth import StudentOut, StudentAuth
from Service.Security.token import SECRET_KEY, ALGORITHM
from Service.Crud import errors,general

#from Service.Crud.students import get_student_by_login
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, HTTPBasic, HTTPBasicCredentials
from Service.producer import send_log

from datetime import datetime
from jose.exceptions import ExpiredSignatureError
from passlib.context import CryptContext # объект, который помогает удобно хешировать и проверять пароли.
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_401_UNAUTHORIZED
from typing import Optional
from sqlalchemy import text
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
    student["permissions"] = permissions
    # student["BirthDate"] = student["BirthDate"].isoformat()

    '''if isinstance(student["BirthDate"], datetime):
        student["BirthDate"] = student["BirthDate"].date()'''
    return StudentOut(**dict(student))












def permission_required(permission_name: str):
    def decorator(current_student=Depends(get_current_student)):
        if permission_name not in current_student["permissions"]:
            raise HTTPException(
                status_code=403,
                detail="Недостаточно прав"
            )
        return current_student
    return decorator


# Проверка на роль "admin" (заменил на permission_required("admin_panel"))
def admin_required(
    current_student=Depends(get_current_student),
):
    if current_student.RoleName != "Админ":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав"
        )
    return current_student

# редирект на страницу логина при неавторизованном доступе
async def get_current_student_or_redirect(
    request: Request,
    db: Session = Depends(get_db)
) -> Optional[StudentAuth]:
    try:

        student = get_current_student(request, db)
        return StudentAuth.model_validate(student)
    except HTTPException as e:
        if e.status_code == HTTP_401_UNAUTHORIZED:
            #logging.warning("Редирект, так как студент не авторизован")
            return RedirectResponse(url=f"/home/login_in/?next={request.url.path}", status_code=302)
            #return RedirectResponse(url="/home/login_in")
        raise e

'''
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# Функция для получения токена из заголовка Authorization
def get_token_from_header(authorization: str = Depends(oauth2_scheme)) -> str:
    return authorization
'''