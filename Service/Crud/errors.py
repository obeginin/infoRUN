
from fastapi import HTTPException
from typing import Optional
'''
Аутентификация и доступ:
+ InvalidCredentials — Неверный логин или пароль  
LoginFailed — Ошибка при входе  
TokenExpired — Срок действия токена истёк  
TokenInvalid — Неверный токен  
Unauthorized — Не авторизован  
AccessDenied — Доступ запрещён (нет прав)

Ошибки валидации и данных:
MissingField — Отсутствует обязательное поле  
InvalidEmail — Некорректный email  
InvalidFormat — Неверный формат данных  
ValueTooShort — Значение слишком короткое  
InvalidInput — Некорректный ввод

Работа с сущностями (ресурсами):
StudentNotFound — Студент не найден  
TaskNotFound — Задание не найдено  
AlreadyExists — Уже существует  
ResourceConflict — Конфликт данных (например, дубликат)

Системные и внутренние ошибки:
+ TokenGenerationError - ошибка генерации токена
ServerError — Внутренняя ошибка сервера  
DatabaseError — Ошибка базы данных  
TokenError — Ошибка при генерации токена  
KafkaSendFailed — Не удалось отправить сообщение в Kafka  
UnknownError — Неизвестная ошибка
'''
# шаблон
def _error(status_code: int, error: str, message: str, field: Optional[str] = None):
    detail = {"error": error, "message": message}
    if field:
        detail["field"] = field
    return HTTPException(status_code=status_code, detail=detail)

# 400 — Неверный запрос
def bad_request(
    error: str = "BadRequest",
    message: str = "Некорректный запрос",
    field: Optional[str] = None
):
    return _error(400, error, message, field)

# 401 — Неавторизован
def unauthorized(
    error: str = "Unauthorized",
    message: str = "Пользователь не авторизован"
):
    return _error(401, error, message)

# 403 — Нет доступа
def access_denied(
    error: str = "AccessDenied",
    message: str = "Доступ запрещён"
):
    return _error(403, error, message)

# 404 — Не найдено
def not_found(
    error: str = "NotFound",
    message: str = "Ресурс не найден"
):
    return _error(404, error, message)

# 500 — Внутренняя ошибка сервера
def internal_server(
    error: str = "ServerError",
    message: str = "Внутренняя ошибка сервера"
):
    return _error(500, error, message)

