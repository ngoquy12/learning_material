from pydantic import BaseModel, ConfigDict
from typing import Optional

class ProgramBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProgramCreate(ProgramBase):
    pass

class ProgramResponse(ProgramBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

