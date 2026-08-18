from pydantic import BaseModel, ConfigDict
from typing import Optional

class LessonBase(BaseModel):
    name: str
    title: str
    details: Optional[str] = None
    expected_output: Optional[str] = None
    forbidden_scope: Optional[str] = None
    allowed_scope: Optional[str] = None
    tech_stack: Optional[str] = None
    session_id: int

class LessonCreate(LessonBase):
    pass

class LessonUpdate(BaseModel):
    name: Optional[str] = None
    title: Optional[str] = None
    details: Optional[str] = None
    expected_output: Optional[str] = None
    forbidden_scope: Optional[str] = None
    allowed_scope: Optional[str] = None
    tech_stack: Optional[str] = None

class LessonResponse(LessonBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

