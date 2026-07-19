from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.session import Base

class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    name = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    details = Column(Text, nullable=True)
    expected_output = Column(Text, nullable=True)
    order_index = Column(Integer, default=0)
    
    session = relationship("Session", back_populates="lessons")
    artifacts = relationship("Artifact", back_populates="lesson")
