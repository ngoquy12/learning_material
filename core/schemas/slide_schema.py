"""
core/schemas/slide_schema.py
Declarative JSON Schema for Elearning Presentation Slides.
Forces Slide Generator Agent to output pure content payload instead of raw mixed HTML code.
"""

from typing import List, Optional
from pydantic import BaseModel, Field

class SlideSceneSchema(BaseModel):
    action_title: str = Field(..., description="Tiêu đề hành động/mục đích slide")
    scene_title: str = Field(..., description="Tiêu đề hiển thị trên slide")
    short_title: str = Field(..., description="Tiêu đề thu gọn cho thanh điều hướng")
    narration: str = Field(..., description="Kịch bản lời giảng chi tiết")
    layout_type: str = Field(default="STANDARD", description="Mẫu layout slide: STANDARD, MERMAID_DIAGRAM, TABLE_COMPARISON, WARNING_GOTCHAS, TIMELINE_RECAP")
    bullets: Optional[List[str]] = Field(default_factory=list, description="Danh sách các ý chính")
    mermaid: Optional[str] = Field(default=None, description="Mã sơ đồ Mermaid.js nếu có")

class SlidePayloadSchema(BaseModel):
    session_title: str
    lesson_title: str
    tech_stack: str
    scenes: List[SlideSceneSchema] = Field(default_factory=list, description="Danh sách các slide trong bài")
