from pydantic import BaseModel, constr
from typing import List
from datetime import date

class StudentLogin(BaseModel):
    Login: str
    Password: str

    class Config:
        from_attributes = True

class StudentCreate(BaseModel):
    Login: str
    Password: str

class StudentAuth(BaseModel):
    ID: int
    Login: str
    last_name: str
    first_name: str
    email: str | None
    role_name: str | None

    class Config:
        from_attributes = True # для моделей без orm_mode в Pydantic v2

class StudentOut(StudentAuth):
    first_name: str
    last_name: str
    birth_date: date | None

    class Config:
        from_attributes = True # для моделей без orm_mode в Pydantic v2


# Модель данных для токена
class TokenData(BaseModel):
    id: int
    Login: str

    class Config:
        from_attributes = True

# для валидности отправленного списка с выбранными разрешеними с фронта на бэк
class AssignPermissionsRequest(BaseModel):
    permission_ids: List[int]


# для самостоятельной смены
class ChangePasswordRequest(BaseModel):
    old_password: constr(min_length=6)
    new_password: constr(min_length=6)

# для смены админом
class AdminChangePasswordRequest(BaseModel):
    new_password: constr(min_length=6)
    #new_password: str = Field(min_length=6)