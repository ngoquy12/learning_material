from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class ArtifactBase(BaseModel):
    type: str
    content: Optional[str] = None
    content_json: Optional[Dict[str, Any]] = None
    status: Optional[str] = "Pending"
    lesson_id: Optional[int] = None
    session_id: Optional[int] = None

class ArtifactCreate(ArtifactBase):
    pass

class ArtifactResponse(ArtifactBase):
    id: int
    created_at: datetime
    versions: Optional[Any] = None
    
    class Config:
        from_attributes = True

class ArtifactUpdate(BaseModel):
    content: Optional[str] = None
    content_json: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
