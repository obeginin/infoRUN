from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from dependencies import get_db
from Models import Student
from Security.token import SECRET_KEY, ALGORITHM
from fastapi import Depends, HTTPException, status
from Security.password import verify_password, get_student_by_login


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# Функция для получения токена из заголовка Authorization
def get_token_from_header(authorization: str = Depends(oauth2_scheme)) -> str:
    return authorization


# Получаем текущего студента по токену
def get_current_student(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Student:
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

# Функция для аутентификации студента
def authenticate_student(db: Session, login: str, password: str):
    student = get_student_by_login(db, login)
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


# Проверка на роль "admin"
def admin_required(
    current_student=Depends(get_current_student),
):
    if current_student.Role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав"
        )
    return current_student