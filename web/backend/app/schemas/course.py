from pydantic import BaseModel
from typing import Optional

class CourseBase(BaseModel):
    name: str
    technology_stack: Optional[str] = None
    semester_id: int

class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: int
    
    class Config:
        from_attributes = True
