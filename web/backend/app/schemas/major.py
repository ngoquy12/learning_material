from pydantic import BaseModel

class MajorBase(BaseModel):
    name: str
    program_id: int

class MajorCreate(MajorBase):
    pass

class MajorResponse(MajorBase):
    id: int
    
    class Config:
        from_attributes = True
