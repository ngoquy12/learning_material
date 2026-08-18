from pydantic import BaseModel, ConfigDict

class SessionBase(BaseModel):
    name: str
    title: str
    course_id: int

class SessionCreate(SessionBase):
    pass

class SessionResponse(SessionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

