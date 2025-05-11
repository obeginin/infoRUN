from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from dependencies import get_db
from Models import Student
from Security.token import SECRET_KEY, ALGORITHM
from fastapi import Depends, HTTPException, status, Request
from Security.password import verify_password, get_student_by_login
from fastapi import Cookie

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# Функция для получения токена из заголовка Authorization
def get_token_from_header(authorization: str = Depends(oauth2_scheme)) -> str:
    return authorization

# функция получения студента по токену
def get_current_student(request: Request, db: Session = Depends(get_db)) -> Student:
    token = request.cookies.get("access_token")
    if not token:
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

    student = db.query(Student).filter(Student.Login == login).first()
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Student not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return student

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