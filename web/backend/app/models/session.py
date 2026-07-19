from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    name = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    order_index = Column(Integer, default=0)
    
    course = relationship("Course", back_populates="sessions")
    lessons = relationship("Lesson", back_populates="session")
    artifacts = relationship("Artifact", back_populates="session", cascade="all, delete-orphan")
