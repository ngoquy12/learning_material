from pydantic import BaseModel
from typing import Optional, Dict, Any, Union, List
from datetime import datetime

class ArtifactBase(BaseModel):
    type: str
    content: Optional[str] = None
    content_json: Optional[Union[Dict[str, Any], List[Any], Any]] = None
    status: Optional[str] = "Pending"
    lesson_id: Optional[int] = None
    session_id: Optional[int] = None

class ArtifactCreate(ArtifactBase):
    pass

class ArtifactResponse(ArtifactBase):
    id: int
    created_at: Optional[datetime] = None
    versions: Optional[Any] = None
    
    class Config:
        from_attributes = True

class ArtifactUpdate(BaseModel):
    content: Optional[str] = None
    content_json: Optional[Union[Dict[str, Any], List[Any], Any]] = None
    status: Optional[str] = None