from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime
from fastapi import Depends, Query
from datetime import date




class Block(BaseModel):
    type: str
    content: Any  # может быть str или list (например, для choice)


class SubTaskCreate(BaseModel):
    TaskID: int
    SubTaskNumber: Optional[str] = None
    VariantID: Optional[int] = None
    Description: Optional[str] = None
    Answer: Optional[str] = None
    SolutionPath: Optional[str] = None
    Blocks: List[Block]
    Creator: str


'''Использую её!!!!!'''
# Фильтры для просмотра задач
class SubTaskQueryParams(BaseModel):
    subtask_id: Optional[int] = Query(None, description="ID подзадачи")
    task_id: Optional[int] = Query(None, description="ID задачи")
    subject_id: Optional[int] = Query(None, description="ID предмета")
    variant_id: Optional[int] = Query(None, description="ID варианта")
    search: Optional[str] = Query(None, description="Поиск по тексту")
    created_date: Optional[date] = Query(None, description="Дата создания")
    creator: Optional[str] = Query(None, description="Создатель")
    sort_column1: Optional[str] = Query("SubTaskID", description="Колонка для сортировки 1")
    sort_column2: Optional[str] = Query("SubTaskID", description="Колонка для сортировки 2")
    sort_direction1: Optional[str] = Query("ASC", description="Направление сортировки 1")
    sort_direction2: Optional[str] = Query("ASC", description="Направление сортировки 2")
    p_offset: Optional[int] = Query(0, description="Смещение для пагинации")
    p_limit: Optional[int] = Query(500000, description="Лимит записей")










'''class FileSchema(BaseModel):
    ID: int
    FileName: str
    FilePath: str
    UploadDate: Optional[datetime] = None

    class Config:
        model_config = {
            "from_attributes": True
        }'''



# Схема для фильтров и сортировки
'''class SubTaskFilter(BaseModel):
    SubTaskID: Optional[int] = None
    TaskID: Optional[int] = None
    SubjectID: Optional[int] = None
    VariantID: Optional[int] = None
    Search: Optional[str] = None
    UploadDate: Optional[date] = None
    Creator: Optional[str] = None
    SortColumn1: Optional[str] = None
    SortColumn2: Optional[str] = None
    SortDirection1: str = Field("ASC", pattern="^(ASC|DESC)$")  # вместо regex
    SortDirection2: str = Field("ASC", pattern="^(ASC|DESC)$")
    Offset: Optional[int] = None
    Limit: Optional[int] = None'''

# Функция, которая превращает Pydantic-схему в query-параметры
'''def get_subtask_filters(
    SubTaskID: Optional[int] = Query(None),
    TaskID: Optional[int] = Query(None),
    SubjectID: Optional[int] = Query(None),
    VariantID: Optional[int] = Query(None),
    Search: Optional[str] = Query(None, max_length=100),
    UploadDate: Optional[str] = Query(None),
    Creator: Optional[str] = Query(None, max_length=50),
    SortColumn1: Optional[str] = Query(None),
    SortColumn2: Optional[str] = Query(None),
    SortDirection1: str = Query("ASC", regex="^(ASC|DESC)$"),
    SortDirection2: str = Query("ASC", regex="^(ASC|DESC)$"),
    Offset: Optional[int] = Query(None),
    Limit: Optional[int] = Query(None),
) -> SubTaskFilter:
    return SubTaskFilter(
        SubTaskID=SubTaskID,
        TaskID=TaskID,
        SubjectID=SubjectID,
        VariantID=VariantID,
        Search=Search,
        UploadDate=UploadDate,
        Creator=Creator,
        SortColumn1=SortColumn1,
        SortColumn2=SortColumn2,
        SortDirection1=SortDirection1,
        SortDirection2=SortDirection2,
        Offset=Offset,
        Limit=Limit
    )'''
