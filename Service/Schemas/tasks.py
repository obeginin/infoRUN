from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
# Schemas\tasks.py
''' 
Данные схемы описывают структуру данных, которые мы получаем или отправляем через API
сериализация (преобразование в JSON и обратно)
'''

# описываем какие именно данные мы хотим вернуть
# для задач
class TaskRead(BaseModel):
    TaskID: int
    TaskNumber: int
    TaskTitle: str
    SubjectID: int

    class Config:
        from_attributes = True

class TaskListResponse(BaseModel):
    message: str
    count: Optional[int] = None
    tasks: List[TaskRead]





# для подзадач
# optional значит что поле может быть не заполнено
class SubTaskRead(BaseModel):
    SubTaskID: int
    TaskID: int
    VariantID: Optional[int] = None
    VariantName: Optional[str] = None
    SubTaskNumber: int
    ImagePath: Optional[str] = None
    Description: Optional[str] = None
    Answer: Optional[str] = None
    SolutionPath: Optional[str] = None

    class Config:
        from_attributes = True


class TaskSubtaskRelation(BaseModel):
    task_id: int
    subtask_id: int

class SubTaskCreate(BaseModel):
    TaskID: int
    SubTaskNumber: str
    ImagePath: Optional[str] = None
    Description: str
    Answer: str
    SolutionPath: Optional[str] = None



