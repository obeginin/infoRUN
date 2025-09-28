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







class AnswerInput(BaseModel):
    subtaskId: int
    studentId: int
    student_answer: str

class SolutionInput(BaseModel):
    student_id: int
    subtask_id: int
    solution_text: Optional[str] = None