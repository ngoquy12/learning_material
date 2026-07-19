from pydantic import BaseModel

class SemesterBase(BaseModel):
    name: str
    major_id: int

class SemesterCreate(SemesterBase):
    pass

class SemesterResponse(SemesterBase):
    id: int
    
    class Config:
        from_attributes = True
