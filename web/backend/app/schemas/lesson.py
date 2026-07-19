from pydantic import BaseModel
from typing import Optional

class LessonBase(BaseModel):
    name: str
    title: str
    details: Optional[str] = None
    expected_output: Optional[str] = None
    session_id: int

class LessonCreate(LessonBase):
    pass

class LessonResponse(LessonBase):
    id: int
    
    class Config:
        from_attributes = True
