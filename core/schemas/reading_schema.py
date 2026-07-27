"""
core/schemas/reading_schema.py
Declarative JSON Schema for Elearning Reading Materials.
Forces Creator Agent to output pure content data instead of raw mixed HTML/JS code.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class VisualizerStep(BaseModel):
    step_number: int
    title: str
    description: str
    active_line_id: Optional[str] = None
    node_index: Optional[int] = 0

class VisualizerPayload(BaseModel):
    archetype: str = Field(default="GENERIC_PROCESS_FLOW", description="Visualizer Archetype: STEPPER_FLOW, NODE_LINK_GRAPH, COMPARISON_GRID")
    steps: List[VisualizerStep] = Field(default_factory=list)
    custom_input_label: Optional[str] = "Nhập dữ liệu chạy thử:"
    custom_input_default: Optional[str] = "10, 20, 30"

class ComparisonTableSchema(BaseModel):
    headers: List[str] = Field(default_factory=list, description="Danh sách tiêu đề cột bảng so sánh")
    rows: List[List[str]] = Field(default_factory=list, description="Các hàng dữ liệu so sánh")

class ReadingPayloadSchema(BaseModel):
    lesson_id: str
    lesson_title: str
    tech_stack: str
    problem_breakdown: str = Field(..., description="Nội dung Đặt vấn đề (Step 1)")
    deep_dive_internals: str = Field(..., description="Phân tích Bản chất Nguyên lý (Step 2)")
    comparison_table: Optional[ComparisonTableSchema] = Field(None, description="Bảng so sánh chi tiết các đặc tính cốt lõi")
    mermaid_diagram: str = Field(..., description="Sơ đồ luồng Mermaid.js (Step 3)")
    code_example: str = Field(..., description="Mã nguồn thực hành minh họa (Step 4)")
    visualizer: Optional[VisualizerPayload] = None
    gotchas_and_summary: str = Field(..., description="Tóm tắt & Lưu ý quan trọng (Step 5)")
    references: List[str] = Field(default_factory=list, description="Danh sách liên kết tham khảo")
