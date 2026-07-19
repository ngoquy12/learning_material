from pydantic import BaseModel
from typing import Optional

class ProgramBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProgramCreate(ProgramBase):
    pass

class ProgramResponse(ProgramBase):
    id: int
    
    class Config:
        from_attributes = True
