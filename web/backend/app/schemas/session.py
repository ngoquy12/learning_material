from pydantic import BaseModel

class SessionBase(BaseModel):
    name: str
    title: str
    course_id: int

class SessionCreate(SessionBase):
    pass

class SessionResponse(SessionBase):
    id: int
    
    class Config:
        from_attributes = True
