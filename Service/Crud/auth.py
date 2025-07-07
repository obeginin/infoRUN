from Service.config import *
from Service.dependencies import get_db
from Service.Models import Student
from Service.Schemas.students import StudentSafe

from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status, Request
from passlib.context import CryptContext # объект, который помогает удобно хешировать и проверять пароли.
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_401_UNAUTHORIZED
from typing import Optional
from sqlalchemy import text
import logging

# Crud\auth.py
''' 
CRUD - основная логика работы запроса
Основные функции для авторизации
'''

logger = logging.getLogger(__name__) # создание логгера для текущего модуля


# шифрование пароля
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
# Функция для хеширования пароля (принимает обычный и возвращает хэшированный)
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Функция для проверки пароля (сравнивает введённый пользователем пароль и хеш из базы,)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Создание пароля вручную:
''''''
raw_password = "standart_password"
raw_password = "standart_password"
hashed_password = hash_password(raw_password)
print("Хешированный пароль:", hashed_password)
#$pbkdf2-sha256$29000$HWPMube2tnYuZYwRwngPQQ$eSDzbZ3puIYCkdzcU94.2a5.ZvXUWXlIGjuSuM4ij/Y


# редирект на страницу логина при неавторизованном доступе
async def get_current_student_or_redirect(
    request: Request,
    db: Session = Depends(get_db)
) -> Optional[StudentSafe]:
    try:
        #print(Student)
        #print(type(Student))
        #logging.warning(f"Авторизован студент: {Student.Login}")
        student = get_current_student(request, db)
        return StudentSafe.model_validate(student)
    except HTTPException as e:
        if e.status_code == HTTP_401_UNAUTHORIZED:
            #logging.warning("Редирект, так как студент не авторизован")
            return RedirectResponse(url=f"/home/login_in/?next={request.url.path}", status_code=302)
            #return RedirectResponse(url="/home/login_in")
        raise e

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Функция для получения токена из заголовка Authorization
def get_token_from_header(authorization: str = Depends(oauth2_scheme)) -> str:
    return authorization

# функция получения студента по токену
def get_current_student(request: Request, db: Session = Depends(get_db)) -> Student:
    token = request.cookies.get("access_token")
    print("ACCESS TOKEN >>>", token)

    if not token:
        print("Нет access_token в cookies!")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Если ты сохраняешь токен как "Bearer <token>", нужно его распарсить
    try:
        scheme, _, param = token.partition(" ")
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme",
                headers={"WWW-Authenticate": "Bearer"},
            )

        payload = jwt.decode(param, SECRET_KEY, algorithms=[ALGORITHM])
        login: str = payload.get("sub")
        if login is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    #student = db.query(Student).filter(Student.Login == login).first()
    student = db.execute(text("""select s.ID, s.Login, r.RoleID, r.Name as RoleName 
                                    from Students s 
                                    left join Roles r on s.RoleID = r.RoleID
                                    where s.Login = :login"""),
                             {"login": login}).mappings().fetchone()
    print(student)
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Student not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    permissions = db.execute(text("""SELECT p.Name
        FROM RolePermissions rp
        JOIN Permissions p ON rp.PermissionID = p.PermissionID
        WHERE rp.RoleID = :role_id
    """), {"role_id": student["RoleID"]}).scalars().all()
    student = dict(student)
    student["permissions"] = permissions
    return student


def permission_required(permission_name: str):
    def decorator(current_student=Depends(get_current_student)):
        if permission_name not in current_student["permissions"]:
            raise HTTPException(
                status_code=403,
                detail="Недостаточно прав"
            )
        return current_student
    return decorator

# Функция для аутентификации студента
'''вроде сейчас используется только в swagger'''
def authenticate_student(db: Session, login: str, password: str):
    student = db.query(Student).filter(Student.Login == login).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Студент с таким логином не найден"
        )
    if not verify_password(password, student.Password):  # Проверка пароля
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный пароль"
        )
    return student  # Возвращаем студента, если логин и пароль верны


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

'''def get_current_student(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Student:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login: str = payload.get("sub")
        if login is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    student = db.query(Student).filter(Student.Login == login).first()
    if student is None:
        raise credentials_exception
    return student
'''

'''# Получаем текущего студента по токену
def get_current_student_from_cookie(token: str = Cookie(None), db: Session = Depends(get_db)) -> Student:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if token is None or not token.startswith("Bearer "):
        raise credentials_exception
    token = token[7:]  # Remove 'Bearer '

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login = payload.get("sub")
        if login is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    student = db.query(Student).filter(Student.Login == login).first()
    if student is None:
        raise credentials_exception
    return student'''

