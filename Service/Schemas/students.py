from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum
from fastapi import Query
from pydantic import ConfigDict
# Schemas\students.py
''' Данные схемы описывают структуру данных, которые мы получаем или отправляем через API
сериализация (преобразование в JSON и обратно)
'''




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
class StudentTaskRead(BaseModel):
    StudentTaskID: int
    StudentID: int
    SubTaskID: int
    StudentAnswer: Optional[str] = None
    CompletionStatus: Optional[str] = None
    Score: Optional[int] = None
    StartDate: Optional[datetime] = None
    ModifiedDate: Optional[datetime] = None
    CompletionDate: Optional[datetime] = None
    DeadlineDate: Optional[datetime] = None
    Attempts: Optional[int] = None
    Login: Optional[str] = None
    ID: Optional[int] = None
    Name: Optional[str] = None
    TaskID: Optional[int] = None
    TaskTitle: Optional[str] = None
    SubTaskNumber: Optional[int] = None
    ImagePath: Optional[str] = None
    SolutionStudentPath: Optional[str] = None
    Description: Optional[str] = None
    VariantID: Optional[int] = None
    VariantName: Optional[str] = None
    TypeVariant: Optional[str] = None
    YearVariant: Optional[int] = None
    NumberVarinat: Optional[int] = None
    DifficultyLevel: Optional[int] = None
    Comment: Optional[str] = None

#  (наследуем от StudentTaskRead)
#class StudentTaskDetails(StudentTaskRead):

class SortableFields(str, Enum):
    StudentTaskID = "StudentTaskID"
    StudentID = "StudentID"
    SubTaskID = "SubTaskID"
    TaskID = "TaskID"
    SubjectID = "SubjectID"
    VariantID = "VariantID"
    StartDate = "StartDate"
    ModifiedDate = "ModifiedDate"
    CompletionDate = "CompletionDate"
    DeadlineDate = "DeadlineDate"
    TypeVariant = "TypeVariant"
    YearVariant = "YearVariant"
    NumberVarinat = "NumberVarinat"
    DifficultyLevel = "DifficultyLevel"
    Attempts = "Attempts"

# Направление сортировки
class SortDirection(str, Enum):
    ASC = "ASC"
    DESC = "DESC"

class StudentTasksQueryParams(BaseModel):
    StudentTaskID: Optional[int] = None
    SubTaskID: Optional[int] = None
    TaskID: Optional[int] = None
    SubjectID: Optional[int] = None
    VariantID: Optional[int] = None
    CompletionStatus: Optional[int] = None
    Search: Optional[str] = Field(default='Крылов', description="поиск по полю")
    SortColumn1: Optional[SortableFields] = Field(default=SortableFields.StartDate, description="Колонка для сортировки уровня 1")
    SortColumn2: Optional[SortableFields] = Field(default=None, description="Колонка для сортировки уровня 1")
    SortDirection1: Optional[SortDirection] = Field(default="ASC", description="Направление сортировки (ASC или DESC) для уровня 1")
    SortDirection2: Optional[SortDirection] = Field(default=None, description="Направление сортировки (ASC или DESC) для уровня 2")
    limit: Optional[int] = None # сколько записей вернуть
    offset: Optional[int] = None # с какого элемента начинать



class AnswerInput(BaseModel):
    subtaskId: int
    studentId: int
    student_answer: str

class SolutionInput(BaseModel):
    student_id: int
    subtask_id: int
    solution_text: Optional[str] = None