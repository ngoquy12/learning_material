"""
agents/pm_schemas.py

Pydantic schemas for the PM Generator Agent.
Provides type-safe data models for curriculum generation input/output.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class SessionType(str, Enum):
    """Enumeration of valid session types in a curriculum."""
    THEORY = "Lý thuyết"
    PRACTICE = "Thực hành"
    MINI_PROJECT = "Mini project"
    PROJECT = "Project"
    HACKATHON = "Hackathon"
    MIDTERM = "Thi giữa môn"
    FINAL = "Thi cuối môn"


class LessonBlock(BaseModel):
    """A single lesson within a theory session."""
    lesson_num: int = Field(..., ge=1, description="Lesson number within the session")
    title: str = Field(..., min_length=1, description="Lesson title")
    content_scope: str = Field(default="", description="Detailed lesson scope/content description")
    expected_outcome: str = Field(default="", description="What student can do after this lesson")
    forbidden_scope: str = Field(default="", description="Concepts NOT YET allowed (not yet taught)")
    allowed_scope: str = Field(default="", description="Concepts already taught (cumulative)")


class SessionBlock(BaseModel):
    """A single session (buổi học) in the curriculum."""
    session_num: int = Field(..., ge=1, description="Session number in the course")
    hinh_thuc: str = Field(..., description="Session type (Lý thuyết, Thực hành, Mini project, etc.)")
    title: str = Field(..., min_length=1, description="Session title")
    content_scope: str = Field(default="", description="Session-level content scope (for non-theory)")
    expected_outcome: str = Field(default="", description="Session-level expected outcome (for non-theory)")
    forbidden_scope: str = Field(default="", description="Session-level forbidden scope (for non-theory)")
    allowed_scope: str = Field(default="", description="Session-level allowed scope (for non-theory)")
    lessons: List[LessonBlock] = Field(default_factory=list, description="Lessons list (empty for non-theory)")


class StudentProfile(BaseModel):
    """Profile of the target student audience."""
    entry_level: str = Field(default="beginner", description="Student entry level (beginner, intermediate, advanced)")
    background: str = Field(default="non-it", description="Student background (it-student, non-it, professional)")
    cognitive_speed: float = Field(default=1.0, ge=0.1, le=2.0, description="Learning speed factor (0.1-2.0)")


class ClassConfiguration(BaseModel):
    """Physical class delivery configuration."""
    session_duration_hours: float = Field(default=2.0, ge=1.0, le=4.0, description="Duration per session in hours")
    delivery_mode: str = Field(default="offline", description="Delivery mode (offline, online, hybrid)")
    sessions_per_day: int = Field(default=1, ge=1, le=3, description="Number of sessions per day")
    weekly_frequency: int = Field(default=3, ge=1, le=7, description="Number of class days per week")


class SessionBudget(BaseModel):
    """Budget allocation for different session types."""
    total_sessions: int = Field(default=25, ge=10, le=60, description="Total number of sessions")
    theory_sessions: int = Field(default=12, ge=1, description="Number of theory sessions")
    practice_sessions: int = Field(default=10, ge=1, description="Number of practice sessions")
    mini_projects: int = Field(default=2, ge=0, description="Number of mini project sessions")
    final_exam: int = Field(default=1, ge=0, le=2, description="Number of final exam sessions")
    capstone_project: int = Field(default=0, ge=0, le=6, description="Number of capstone project sessions")


class PMGeneratorConfig(BaseModel):
    """Complete configuration for PM generation, parsed from JSON config file."""
    curriculum_excel_path: str = Field(..., description="Path to the PTIT curriculum Excel file")
    course_id: str = Field(..., description="Course ID (e.g. IT-204)")
    student_profile: StudentProfile = Field(default_factory=StudentProfile)
    session_budget: SessionBudget = Field(default_factory=SessionBudget)
    class_configuration: ClassConfiguration = Field(default_factory=ClassConfiguration)
    tech_stack: str = Field(default="", description="Target technology stack (e.g. python/core, typescript/nestjs)")


class SyllabusPM(BaseModel):
    """Complete generated syllabus for a course."""
    course_id: str
    course_name: str
    clos: List[str] = Field(default_factory=list)
    plos: List[str] = Field(default_factory=list)
    sessions: List[SessionBlock] = Field(default_factory=list)
