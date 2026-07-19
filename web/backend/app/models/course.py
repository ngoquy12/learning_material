from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    semester_id = Column(Integer, ForeignKey("semesters.id"), nullable=False)
    name = Column(String(255), nullable=False)
    technology_stack = Column(String(100), nullable=True)
    
    semester = relationship("Semester", back_populates="courses")
    sessions = relationship("Session", back_populates="course")
