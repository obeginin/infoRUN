from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum
from datetime import date
from fastapi import Query
from pydantic import ConfigDict
# Schemas\students.py
''' Данные схемы описывают структуру данных, которые мы получаем или отправляем через API
сериализация (преобразование в JSON и обратно)
'''





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
    student_task_id: Optional[int] = None
    sub_task_id: Optional[int] = None
    task_id: Optional[int] = None
    subject_id: Optional[int] = None
    variant_id: Optional[int] = None
    completion_status: Optional[str] = None
    search: Optional[str] = None
    sort_column1: Optional[SortableFields] = Field(default=SortableFields.StartDate)
    sort_column2: Optional[SortableFields] = None
    sort_direction1: Optional[SortDirection] = Field(default="ASC")
    sort_direction2: Optional[SortDirection] = None
    limit: Optional[int] = None
    offset: Optional[int] = None



class AnswerInput(BaseModel):
    subtaskId: int
    studentId: int
    student_answer: str

class SolutionInput(BaseModel):
    student_id: int
    subtask_id: int
    solution_text: Optional[str] = None