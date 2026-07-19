from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, JSON
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class Artifact(Base):
    __tablename__ = "artifacts"
    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=True)
    type = Column(String(50), nullable=False)
    content = Column(LONGTEXT, nullable=True)
    content_json = Column(JSON, nullable=True)
    status = Column(String(50), default="Pending")
    versions = Column(JSON, nullable=True) # List of dicts: [{"version_id": int, "content": str, "content_json": dict, "created_at": str}]
    created_at = Column(DateTime, default=datetime.utcnow)
    
    lesson = relationship("Lesson", back_populates="artifacts")
    session = relationship("Session", back_populates="artifacts")
