from pydantic import BaseModel, constr, EmailStr
from typing import List
from datetime import date

class StudentLogin(BaseModel):
    Login: str
    Password: str

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    login: str
    password: str

class StudentAuth(BaseModel):
    ID: int
    Login: str | None
    Last_Name: str | None
    First_Name: str | None
    Email: str
    RoleName: str | None
    IsActive: bool
    IsDeleted: date | None

    class Config:
        from_attributes = True # для моделей без orm_mode в Pydantic v2

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


# для самостоятельной смены
class ChangePasswordRequest(BaseModel):
    old_password: constr(min_length=6)
    new_password: constr(min_length=6)
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