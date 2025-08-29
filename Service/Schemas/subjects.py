from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
# Schemas\subjects.py


class SubjectRead(BaseModel):
    ID: int
    Name: str
    Description: str

    class Config:
        from_attributes = True

class SubjectListResponse(BaseModel):
    message: str
    count: Optional[int] = None
    subjects: List[SubjectRead]


class SubjectOut(BaseModel):
    ID: int
    Name: str
    Description: str | None = None