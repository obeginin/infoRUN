from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from pydantic import ConfigDict
# Schemas\students.py
''' Данные схемы описывают структуру данных, которые мы получаем или отправляем через API
сериализация (преобразование в JSON и обратно)
'''


# для передачи информации о авторизованном студенте
class StudentSafe(BaseModel):
    ID: int
    Login: str
    Last_Name: str
    First_Name: str
    Role: str

    model_config = ConfigDict(from_attributes=True)

# Базовая модель студента
class StudentBase(BaseModel):
    Login: str
    Last_Name: str
    First_Name: str
    Middle_Name: str
    Email: str
    Sex: str
    BirthDate: datetime
    Comment: str


class StudentsRead(StudentBase):
    ID: int

    class Config:
        from_attributes = True


# Базовая модель StudentTask
class StudentTaskBase(BaseModel):
    StudentTaskID: int
    StudentID: int
    SubTaskID: int
    CompletionStatus: Optional[str] = None
    Score: Optional[float] = None
    CompletionDate: Optional[datetime] = None
    StudentAnswer: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={datetime: lambda v: v.isoformat() if v else None}
    )

# 🔍 Расширение для отображения задачи с деталями (наследуем от StudentTaskBase)
class StudentTaskRead(StudentTaskBase):
    Login: Optional[str] = None
    Role: Optional[str] = None
    TaskID: Optional[int] = None
    TaskTitle: Optional[str] = None
    SubTaskNumber: Optional[int] = None
    ImagePath: Optional[str] = None
    Description: Optional[str] = None
    Answer: Optional[str] = None
    SolutionPath: Optional[str] = None
    TotalSubTasks: Optional[int] = None
    CompletedSubTasks: Optional[int] = None
    TotalCount: Optional[int] = None

#  (наследуем от StudentTaskRead)
class StudentTaskDetails(StudentTaskRead):
    SolutionStudentPath: Optional[str] = None



class AnswerInput(BaseModel):
    subtaskId: int
    studentId: int
    student_answer: str

class SolutionInput(BaseModel):
    student_id: int
    subtask_id: int
    solution_text: Optional[str] = None