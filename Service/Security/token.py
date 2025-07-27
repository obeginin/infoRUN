from Service.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES # импорт из конфига токена

from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional

"""Функции для генерации JWT-токена"""

# Функция для создания JWT токена
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Функция для расшифровки и проверки токена
def verify_token(token: str):
    try:
        # проверяет подпись токена и его срок жизни
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Если всё ок, возвращает payload — словарь с теми полями, которые залили при генерации
        return payload
    # Если токен просрочен
    except jwt.ExpiredSignatureError:
        return None
    # При любой другой ошибке декодирования (подмена, неверная структура)
    except jwt.JWTError:
        return None



