from pydantic import BaseModel, constr, EmailStr, Field, field_validator, validator
from typing import List
from datetime import date
from enum import Enum
from typing import Optional
import re


class StudentField(str, Enum):
    ID = "ID"
    Login = "Login"
    Email = "Email"
    Phone = "Phone"

# старая авторизация по логину
class StudentLogin(BaseModel):
    Login: str
    Password: str

    class Config:
        from_attributes = True

# старая авторизация по логин / email / телефон
class AuthRequest(BaseModel):
    identifier: str  # логин / email / телефон
    password: str

# для регистрации
class UserCreate(BaseModel):
    email: EmailStr
    login: str
    password: str
    phone: str



class DeleteStudent(BaseModel):
    ID: int = None
    Login: str = None
    Email: EmailStr = None

class SearchStudentQuery(BaseModel):
    field_name: Optional[StudentField] = None
    value: str

# Общие поля для создания/обновления
class StudentBase(BaseModel):
    Login: str
    Last_Name:  str = None
    First_Name:  str = None
    Middle_Name:  str = None
    Email: EmailStr = None # EmailStr проверяет, что строка — корректный email
    Phone: str = None
    Sex:  str = None
    BirthDate:  date = None
    Comment:  str = None
    RoleID:  int = None
    IsActive:  bool = None

    @validator('Login')
    def login_no_cyrillic(cls, v):
        if re.search(r'[а-яА-Я]', v):
            raise ValueError('Логин не должен содержать русские буквы (кириллицу)')
        return v

    # Провекар пола
    @field_validator("Sex")
    @classmethod
    def validate_sex(cls, v):
        allowed = {"М", "Ж", None}
        if v not in allowed:
            raise ValueError("Пол может быть только 'М', 'Ж' или не указан")
        return v

    # Проверка что телефон состоит только из цифр
    @validator("Phone")
    def phone_must_be_digits(cls, v):
        if v is None:
            return v
        if not v.isdigit():
            raise ValueError("Телефон должен содержать только цифры")
        return v


# Используется при создании (без ID, IsDeleted и т.д.)
class StudentCreate(StudentBase):
    Password: str = None
    pass

# Используется при регистрации/авторизации/выдаче данных
class StudentAuth(BaseModel):
    ID: int
    Login: str | None
    Last_Name: str | None
    First_Name: str | None
    Email: EmailStr | None
    RoleName: str | None
    IsActive: bool | None
    IsDeleted: date | None

    class Config:
        from_attributes = True # для моделей без orm_mode в Pydantic v2

# Расширенный вывод студента с правами
class StudentOut(StudentAuth):
    Middle_Name: str | None
    Sex: str | None
    BirthDate: date | None
    Comment: str | None
    permissions: List[str] = []

    class Config:
        from_attributes = True # для моделей без orm_mode в Pydantic v2


class TokenWithStudent(BaseModel):
    access_token: str
    token_type: str
    student: StudentAuth

# Модель данных для токена
class TokenData(BaseModel):
    id: int
    Login: str

    class Config:
        from_attributes = True



# для валидности отправленного списка с выбранными разрешеними с фронта на бэк
class AssignPermissionsRequest(BaseModel):
    permission_ids: List[int]

# для валидного email
class PasswordReset(BaseModel):
    Email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: constr(min_length=6)
    repeat_new_password: constr(min_length=6)

# для самостоятельной смены
class ChangePasswordRequest(BaseModel):
    old_password: constr(min_length=6)
    new_password: constr(min_length=6)
    # для прода
    '''
    new_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#+=\-_]).+$",
        description="Пароль должен содержать минимум 8 символов, включая заглавные и строчные буквы, цифры и спецсимволы"
    )'''
    repeat_new_password: constr(min_length=6)

# для смены админом
class AdminChangePasswordRequest(BaseModel):
    new_password: constr(min_length=6)
    #new_password: str = Field(min_length=6)

class Roles(BaseModel):
    RoleID: int
    Name: str


class Permission(BaseModel):
    PermissionID: int
    Name: str
    Description: str

class AssignRoleQuery(BaseModel):
    RoleID: int