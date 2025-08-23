from pydantic import BaseModel
from typing import Optional, List, Any

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


