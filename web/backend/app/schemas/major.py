from pydantic import BaseModel, ConfigDict

class MajorBase(BaseModel):
    name: str
    program_id: int

class MajorCreate(MajorBase):
    pass

class MajorResponse(MajorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

