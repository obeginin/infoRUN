from pydantic import BaseModel

class StudentLogin(BaseModel):
    Login: str
    Password: str

    class Config:
        from_attributes = True

class StudentCreate(BaseModel):
    Login: str
    Password: str

class StudentOut(BaseModel):
    id: int
    Login: str

    class Config:
        from_attributes = True