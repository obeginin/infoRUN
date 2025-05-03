from pydantic import BaseModel
from typing import Optional
'''В данном файле описываем какие типы переменных должны передаваться по api'''
# описываем какие именно данные мы хотим вернуть
# для задач
class TaskRead(BaseModel):
    TaskID: int
    TaskNumber: int
    TaskTitle: str

    class Config:
        from_attributes = True

# для подзадач
# optional значит что поле можт быть не заполнено
class SubTaskRead(BaseModel):
    SubTaskID: int
    TaskID: int
    SubTaskNumber: str
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