from passlib.context import CryptContext # объект, который помогает удобно хешировать и проверять пароли.
from sqlalchemy.orm import Session
from Models import Student

"""Авторизация и аутентификация"""
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Функция для получаения пользователя по логину
def get_student_by_login(db: Session, login: str):
    return db.query(Student).filter(Student.Login == login).first()

# Функция для хеширования пароля (принимает обычный и возвращает хэшированный)
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Функция для проверки пароля (сравнивает введённый пользователем пароль и хеш из базы,)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

"""Аутентификация"""
def authenticate_student(db: Session, login: str, password: str):
    student = get_student_by_login(db, login)
    if not student:
        return None
    if not verify_password(password, student.HashedPassword):
        return None
    return student
