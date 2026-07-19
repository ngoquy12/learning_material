from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Semester(Base):
    __tablename__ = "semesters"
    id = Column(Integer, primary_key=True, index=True)
    major_id = Column(Integer, ForeignKey("majors.id"), nullable=False)
    name = Column(String(255), nullable=False)
    
    major = relationship("Major", back_populates="semesters")
    courses = relationship("Course", back_populates="semester")
