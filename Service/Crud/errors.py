from fastapi import HTTPException
from typing import Optional

#ActionEvent
'''
LOGIN_SUCCESS = "LoginSuccess"
PASSWORD_CHANGED = "PasswordChanged"
LOGOUT = "logout"
'''

# LOGIN_FAILED = "LoginFailed"
'''
LoginNotFound
PasswordFailed 
StudentNoActive
StudentNotFound
StudentRemoved НЕ РЕАЛИЗОВАНО!
'''

# TOKEN_ERROR = "TokenError"
''' 
TokenExpired (токен истек)
TokenMissing (токен отсутствует)
TokenInvalid (Недействительный токен)
TokenInvalidPayload (токен не содержит логин)
TokenMalformed (Неправильный формат токена)
TokenGenerationError (ошибка генерации токена)
- NotAuthenticated (Пользователь не аутентифицирован, не залогинен)
'''

#PERMISSION_DENIED = "PermissionDenied"
'''
AccessDenied (доступ запрещен, нет прав)
RoleRestricted (действие запрещено для роли)
'''

# PASSWORD_CHANGED = "PasswordChanged"
'''
OldPasswordIncorrect (Cтарый пароль неверный)
NewPasswordsMismatch (Введенные пароли не совпадают)
WeakPassword (слишком простой пароль) НЕ РЕАЛИЗОВАНО!
SameAsOldPassword (новый пароль совпадает со старым)  НЕ РЕАЛИЗОВАНО!
'''

# VALIDATION_ERROR = "ValidationError"
'''
InvalidFormat (неверный формат ответа)
InvalidDate (дата в недопустимом формате)
EmptyAnswer (пустой ответ)
MissingRequiredField (Отсутствует обязательное поле)
AlreadyExists (Уже существует) 
TaskNotFound  (Задание не найдено)
LateSubmission (просрочена отправка)
'''

# SERVER_ERROR = "ServerError"
'''
UnhandledException (необработанное исключение)
DatabaseUnavailable (БД недоступна)
KafkaUnavailable (Kafka недоступна)
ExternalServiceTimeout (таймаут внешнего сервиса)

UpdatePasswordFailed (Ошибка при обновлении пароля)
'''

# EMAIL_ERROR = "EmailError"
''' 
Ошибки валидации и данных:
InvalidEmail — Некорректный email  
ValueTooShort — Значение слишком короткое  
InvalidInput — Некорректный ввод
MissingField  (Отсутствует обязательное поле)
'''



# шаблон
def _error(status_code: int, error: str, message: str, field: Optional[str] = None, headers: dict = None):
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
    return _error(401, error, message, headers={"WWW-Authenticate": "Bearer"})

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

