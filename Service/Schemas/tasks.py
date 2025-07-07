from pydantic import BaseModel
from typing import Optional
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

    class Config:
        from_attributes = True

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

'''!!!!!!!!!'''
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

class SubTaskUpdate(BaseModel):
    TaskID: int
    VariantID: int
    SubTaskNumber: int
    ImagePath: str | None = None
    Description: str | None = None
    Answer: str | None = None
    SolutionPath: str | None = None

class FileSchema(BaseModel):
    ID: int
    FileName: str
    FilePath: str
    UploadDate: Optional[datetime] = None

    class Config:
        model_config = {
            "from_attributes": True
        }

class SubjectOut(BaseModel):
    ID: int
    Name: str
    Description: str | None = None