from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime
from fastapi import Depends, Query
from datetime import date


class Block(BaseModel):
    type: str
    content: Any  # может быть str или list (например, для choice)

# class SubTaskResponse(BaseModel):
#     SubTaskID: int
#     TaskID: int
#     SubTaskNumber: int
#     VariantID: int = None
#     Description: str = ""
#     Answer: str = ""
#     SolutionPath: str = ""
#     Blocks: List[Block]

class SubTaskCreate(BaseModel):
    TaskID: int
    SubTaskNumber: Optional[int] = None
    VariantID: Optional[int] = None
    Description: Optional[str] = None
    Answer: Optional[str] = None
    SolutionPath: Optional[str] = None
    Blocks: List[Block]
    Creator: str

class SubTaskUpdate(BaseModel):
    TaskID: int
    VariantID: int
    SubTaskNumber: int
    ImagePath: str | None = None
    Description: str | None = None
    Answer: str | None = None
    SolutionPath: str | None = None

# Схема для фильтров и сортировки
class SubTaskFilter(BaseModel):
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
    Limit: Optional[int] = None


# Функция, которая превращает Pydantic-схему в query-параметры
def get_subtask_filters(
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
    )
class FileSchema(BaseModel):
    ID: int
    FileName: str
    FilePath: str
    UploadDate: Optional[datetime] = None

    class Config:
        model_config = {
            "from_attributes": True
        }
