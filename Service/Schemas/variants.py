
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
# Schemas\variants.py

class readVariants(BaseModel):
    VariantID: int
    VariantName: str
    Type: Optional[str] = None
    Year: Optional[str] = None
    Number: Optional[int] = None
    DifficultyLevel: Optional[int] = None
    Comment: Optional[str] = None
    SubjectID: int

    class Config:
        from_attributes = True


class VariantsListResponse(BaseModel):
    message: str
    count: Optional[int] = None
    variants: List[readVariants]