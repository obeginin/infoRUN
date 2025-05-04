# schemas/users.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

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
    Login: str
    SubTaskID: int
    StudentAnswer: Optional[str] = None
    CompletionStatus: str
    Score: Optional[float] = None
    CompletionDate: Optional[datetime] = None

    class Config:
        from_attributes = True

        