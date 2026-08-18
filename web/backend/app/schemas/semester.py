from pydantic import BaseModel, ConfigDict

class SemesterBase(BaseModel):
    name: str
    major_id: int

class SemesterCreate(SemesterBase):
    pass

class SemesterResponse(SemesterBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

