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
    Last_Name: str
    First_Name: str
    Email: str | None
    RoleName: str | None
    IsActive: bool
    IsDeleted: date | None

    class Config:
        from_attributes = True # для моделей без orm_mode в Pydantic v2

class StudentOut(StudentAuth):
    Middle_Name: str
    Sex: str
    BirthDate: date | None
    Comment: str
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