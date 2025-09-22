from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime

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


class FileSchema(BaseModel):
    ID: int
    FileName: str
    FilePath: str
    UploadDate: Optional[datetime] = None

    class Config:
        model_config = {
            "from_attributes": True
        }
