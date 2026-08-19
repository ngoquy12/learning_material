"""
core/schemas/course_schemas.py
Enterprise Pydantic v2 Schemas for Elearning Content Factory.
Enforces strict type safety and schema validation across Quizzes, Labs, Homework, and Visualizers.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator

# =============================================================================
# 1. Enhanced Quiz Schemas
# =============================================================================
class EnhancedQuizItemSchema(BaseModel):
    stt: int = Field(..., description="Số thứ tự câu hỏi (1-5)")
    question_type: str = Field(default="SYNTAX", description="Loại câu hỏi: SYNTAX, EXECUTION_FLOW, CODE_TRACE, COMPARISON, TRAP_PREDICTION")
    question: str = Field(..., description="Nội dung câu hỏi trắc nghiệm")
    options: List[str] = Field(..., description="Danh sách 4 phương án lựa chọn")
    correct_option_index: int = Field(..., description="Chỉ mục đáp án đúng (0, 1, 2, hoặc 3)")
    explanation: str = Field(default="", description="Giải thích lý do đáp án đúng")
    instant_feedback: Optional[str] = Field(default="", description="Phản hồi tức thì khi chọn sai")
    time_limit_sec: Optional[int] = Field(default=30, description="Thời gian làm bài tính bằng giây")

    @field_validator("correct_option_index")
    @classmethod
    def validate_correct_index(cls, v: int, info) -> int:
        if v < 0 or v > 3:
            return max(0, min(3, v))
        return v

    @field_validator("options")
    @classmethod
    def validate_options(cls, v: List[str]) -> List[str]:
        if len(v) < 4:
            # Pad options if LLM returned fewer than 4
            padded = list(v)
            while len(padded) < 4:
                padded.append(f"Phương án {chr(65 + len(padded))}")
            return padded
        return v[:4]


class LessonQuizSuiteSchema(BaseModel):
    quiz: List[EnhancedQuizItemSchema] = Field(default_factory=list, description="Danh sách 5 câu hỏi trắc nghiệm của bài học")


# =============================================================================
# 2. Enhanced Practical Lab Schemas
# =============================================================================
class LabDescriptionSchema(BaseModel):
    inputs: str = Field(default="Môi trường phát triển và tài nguyên thực hành.", description="Tài nguyên và môi trường đầu vào")
    steps: List[str] = Field(default_factory=list, description="Các bước thực hiện tuần tự")

class LabEvaluationSchema(BaseModel):
    checklist: List[str] = Field(default_factory=list, description="Checklist đánh giá kết quả")

class EnhancedPracticalLabSchema(BaseModel):
    title: str = Field(..., description="Tiêu đề bài thực hành")
    objectives: List[str] = Field(default_factory=list, description="Danh sách mục tiêu cần đạt")
    problem_statement: Optional[str] = Field(default="", description="Mô tả bài toán nghiệp vụ")
    description: LabDescriptionSchema = Field(default_factory=LabDescriptionSchema, description="Mô tả chi tiết các bước")
    code_demo: Optional[str] = Field(default="", description="Mã nguồn tham khảo")
    reference_code: Optional[str] = Field(default="", description="Alias cho mã nguồn tham khảo")
    evaluation: LabEvaluationSchema = Field(default_factory=LabEvaluationSchema, description="Đánh giá kết quả")


# =============================================================================
# 3. Enhanced Homework Schemas
# =============================================================================
class EnhancedHomeworkExerciseSchema(BaseModel):
    idx: int = Field(..., description="Số thứ tự bài tập (1-6 hoặc 1-15)")
    level_name: str = Field(default="Basic Application", description="Mức độ nhận thức Bloom")
    chosen_domain: Optional[str] = Field(default="E-Commerce", description="Lĩnh vực nghiệp vụ thực tế")
    de_bai_content: str = Field(..., description="Nội dung đề bài chi tiết (Markdown 5 phần)")
    tieu_chi_content: str = Field(..., description="Tiêu chí đánh giá thang điểm 100đ")


# =============================================================================
# 4. Enhanced Visualizer Schemas
# =============================================================================
class EnhancedVisualizerSchema(BaseModel):
    canvas_title: str = Field(..., description="Tiêu đề khung trực quan hóa")
    legend_html: Optional[str] = Field(default="", description="HTML chú giải màu sắc trạng thái")
    stats_html: Optional[str] = Field(default="", description="HTML thẻ đếm chỉ số động")
    code_tracker_html: Optional[str] = Field(default="", description="HTML dòng code tracker có class code-line")
    input_label: Optional[str] = Field(default="Nhập dữ liệu test:", description="Nhãn ô input test")
    input_default: Optional[str] = Field(default="", description="Giá trị test mặc định")
    engine_js: str = Field(..., description="Mã nguồn JavaScript chứa class InteractiveVisualizerEngine")


# =============================================================================
# 5. Enhanced Classroom Lecture Slide Schemas
# =============================================================================
class ClassroomSlideItemSchema(BaseModel):
    slide_num: int = Field(..., description="Số thứ tự slide (1-20)")
    slide_type: str = Field(default="THEORY_DEMO", description="Loại slide: COVER, AGENDA, THEORY_DEMO, SUMMARY, QA")
    title: str = Field(..., description="Tiêu đề slide")
    action_title: Optional[str] = Field(default="", description="Tiêu đề hành động/ngữ cảnh")
    bullets: List[str] = Field(default_factory=list, description="Danh sách tối đa 3 điểm chính (quy tắc 3-30-300)")
    code_sample: Optional[str] = Field(default="", description="Mã nguồn demo hoặc lệnh CLI")
    diagram: Optional[str] = Field(default="", description="Sơ đồ Mermaid hoặc SVG")

class ClassroomSlideDeckSchema(BaseModel):
    session_id: str = Field(..., description="Mã Session (ví dụ: Session 01)")
    session_title: str = Field(..., description="Chủ đề buổi học")
    module_name: Optional[str] = Field(default="", description="Tên môn học / Tech stack")
    total_slides: int = Field(default=18, description="Tổng số slide trong deck (15-20 slides)")
    slides: List[ClassroomSlideItemSchema] = Field(default_factory=list, description="Danh sách các slide chi tiết")

