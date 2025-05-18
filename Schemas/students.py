from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Schemas\students.py
''' Данные схемы описывают структуру данных, которые мы получаем или отправляем через API
сериализация (преобразование в JSON и обратно)
'''

class StudentsRead(BaseModel):
    ID: int
    Login: str
    Last_Name: str
    First_Name: str
    Middle_Name: str
    Email: str
    Sex: str
    BirthDate: datetime
    Comment: str

    class Config:
        from_attributes = True

class StudentTaskRead(BaseModel):
    StudentTaskID: int
    StudentID: int
    Login: Optional[str] = None
    SubTaskID: int
    StudentAnswer: Optional[str] = None
    CompletionStatus: str
    Score: Optional[float] = None
    CompletionDate: Optional[datetime] = None

    class Config:
        from_attributes = True

        