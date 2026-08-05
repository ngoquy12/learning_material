"""
core/schemas/llm_schemas.py
Pydantic Schemas for Structured Outputs.
Defines schemas for Creator Stage 1 & 2, Objectives, Video Blueprint, and Visualizer.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

# =============================================================================
# 1. Creator Agent - Stage 1 Reading Schema
# =============================================================================
class CreatorStage1Schema(BaseModel):
    problem_title: str = Field(..., description="Tiêu đề ngắn gọn cho phần 1 Đặt Vấn Đề")
    problem: str = Field(..., description="Nội dung đặt vấn đề dạng Markdown Bullet List & Sublist (250-400 từ), kèm bối cảnh thực tế doanh nghiệp")
    analysis_title: str = Field(..., description="Tiêu đề ngắn gọn cho phần 2 Phân Tích")
    analysis: str = Field(..., description="Phân tích cơ chế vận hành nội bộ dạng List/Sublist kèm BẢNG SO SÁNH MARKDOWN KỸ THUẬT (250-400 từ)")
    solution_title: str = Field(..., description="Tiêu đề ngắn gọn cho phần 3 Giải Pháp")
    solution: str = Field(..., description="Giải pháp kỹ thuật chi tiết dạng List kèm SƠ ĐỒ MERMAID ```mermaid ... ```")
    example: str = Field(..., description="Mã nguồn minh họa chính tuân thủ coding convention (snake_case tiếng Anh)")
    example_good: str = Field(..., description="Ví dụ mã chuẩn Best Practice (GOOD Practice) kèm comment giải thích chi tiết")
    example_bad: str = Field(..., description="Ví dụ mã sai/Anti-pattern (BAD Practice) kèm comment cảnh báo bẫy lỗi và giải thích hậu quả")
    resolve_title: str = Field(..., description="Tiêu đề ngắn gọn cho phần 4 Phân Tích Luồng Chạy")
    resolve: str = Field(..., description="Phân tích chi tiết luồng chạy thực thi dạng List và Console Output")
    summary: str = Field(..., description="Tổng kết bài học dạng List và bôi đậm tên các sai lầm runtime thường gặp")

# =============================================================================
# 2. Creator Agent - Stage 2 Components Schema
# =============================================================================
class SelfTestItem(BaseModel):
    question: str = Field(..., description="Câu hỏi tự kiểm tra khảo thí bám sát bài đọc")
    answer: str = Field(..., description="Gợi ý trả lời chi tiết sâu sắc cho câu hỏi tự kiểm tra")

class ReferenceItem(BaseModel):
    title: str = Field(..., description="Tên tài liệu tham khảo uy tín chính thức")
    url: str = Field(..., description="Đường dẫn url liên kết đến tài liệu tham khảo")

class QuizItem(BaseModel):
    question: str = Field(..., description="Nội dung câu hỏi trắc nghiệm")
    options: List[str] = Field(..., description="Danh sách chính xác 4 phương án lựa chọn (A, B, C, D)")
    correct_option_index: int = Field(..., description="Chỉ mục của đáp án đúng (0 cho A, 1 cho B, 2 cho C, 3 cho D)")
    explanation: str = Field(..., description="Giải thích chi tiết lý do đáp án được chọn là đúng và các đáp án khác là sai")

class LabSchema(BaseModel):
    title: str = Field(..., description="Tiêu đề bài thực hành Lab")
    objectives: List[str] = Field(..., description="Danh sách các mục tiêu thực hành cần đạt")
    steps: List[str] = Field(..., description="Các bước thực hiện chi tiết theo thứ tự tuần tự")
    checklist: List[str] = Field(..., description="Tiêu chí đánh giá định lượng dưới dạng bảng kiểm [ ]")

class VisualizerSchema(BaseModel):
    canvas_title: str = Field(..., description="Tiêu đề của khung trực quan hóa tương tác")
    legend_html: str = Field(..., description="HTML hiển thị các chú giải trạng thái màu sắc")
    stats_html: str = Field(..., description="HTML hiển thị các thẻ đếm chỉ số động")
    code_tracker_html: str = Field(..., description="Mã HTML chứa code. Mỗi dòng code bắt buộc nằm trong một thẻ div có class 'code-line' và id tăng dần 'line-0', 'line-1'...")
    input_label: str = Field(..., description="Nhãn hiển thị cho ô nhập dữ liệu chạy thử")
    input_default: str = Field(..., description="Giá trị dữ liệu chạy thử mặc định ban đầu")
    engine_js: str = Field(..., description="Mã nguồn JavaScript chứa định nghĩa class InteractiveVisualizerEngine hoàn chỉnh")

class CreatorStage2Schema(BaseModel):
    self_test: List[SelfTestItem] = Field(..., description="Danh sách chính xác 3 câu hỏi tự đánh giá kèm câu trả lời")
    references: List[ReferenceItem] = Field(..., description="Danh sách tài liệu tham khảo")
    quiz: List[QuizItem] = Field(..., description="Danh sách câu hỏi trắc nghiệm")
    lab: LabSchema = Field(..., description="Tài nguyên bài thực hành Lab hoàn chỉnh")
    visualizer: VisualizerSchema = Field(..., description="Cấu phần trực quan hóa Interactive Visualizer")

# =============================================================================
# 3. Objective Outcome Schema (Bloom's Taxonomy)
# =============================================================================
class BloomTaxonomySchema(BaseModel):
    remembering_understanding: List[str] = Field(..., description="Danh sách các chuẩn đầu ra ở mức Nhớ và Hiểu")
    applying_analyzing: List[str] = Field(..., description="Danh sách các chuẩn đầu ra ở mức Vận dụng và Phân tích")
    evaluating_creating: List[str] = Field(..., description="Danh sách các chuẩn đầu ra ở mức Đánh giá và Sáng tạo")

class ObjectiveOutcomeSchema(BaseModel):
    session_title: str = Field(..., description="Tiêu đề chính của Session")
    student_profile_outcome: str = Field(..., description="Mô tả chi tiết chân dung và kết quả học viên đạt được sau session")
    blooms_taxonomy: BloomTaxonomySchema = Field(..., description="Phân bổ ma trận Bloom's Taxonomy")

# =============================================================================
# 4. Video Blueprint Schema (HyperFrames Script)
# =============================================================================
class VideoSceneItem(BaseModel):
    scene_id: str = Field(..., description="Mã phân cảnh duy nhất, ví dụ Scene_01, Scene_02...")
    scene_title: str = Field(..., description="Tiêu đề phân cảnh hiển thị")
    start_at_root: float = Field(..., description="Thời điểm bắt đầu của scene trên tổng trục thời gian (giây)")
    duration: float = Field(..., description="Thời lượng giây của scene đó (từ 25 đến 50 giây)")
    track_index: int = Field(..., description="Chỉ mục track hiển thị tăng dần tuần tự từ 1")
    layout_type: str = Field(..., description="Layout sử dụng: comparison, code_editor, terminal_cli, process_flow, pitfall_alert, summary_recap")
    pacing_mode: str = Field(..., description="Chế độ nhịp điệu của scene: fast_hook, dense_code, normal, recap_outro")
    narration: str = Field(..., description="Kịch bản lời giảng chi tiết chuẩn giọng đọc TTS (100-180 từ)")
    director_cues: str = Field(..., description="Chỉ dẫn đạo diễn hình ảnh/âm thanh như nhấn âm, phóng to...")
    visual_description: str = Field(..., description="Mô tả chi tiết hình ảnh sẽ hiển thị trên canvas")
    html_structure: str = Field(..., description="Mã HTML tự do thiết kế của card nội dung trong scene")
    animation_timeline: List[str] = Field(..., description="Danh sách các bước diễn hoạt timeline GSAP")

class VideoBlueprintSchema(BaseModel):
    lesson_slug: str = Field(..., description="Mã định danh slug của bài học")
    lesson_title: str = Field(..., description="Tiêu đề chính của bài học")
    pedagogy_type: str = Field(..., description="Phân loại sư phạm: HANDSON_SETUP, LIVE_CODING, CONCEPTUAL, SYSTEM_ARCHITECTURE")
    total_duration: float = Field(..., description="Tổng thời lượng của toàn bộ video (bằng tổng duration các scenes)")
    scenes: List[VideoSceneItem] = Field(..., description="Danh sách toàn bộ các scene chi tiết")
    tts_scripts: Dict[str, str] = Field(..., description="Bản đồ ánh xạ scene_id tương ứng với narration thoại")

# =============================================================================
# 5. Visualizer Payload Schema
# =============================================================================
class VisualizerPayloadSchema(BaseModel):
    canvas_title: str = Field(..., description="Tiêu đề khung trực quan hóa")
    legend_html: str = Field(..., description="HTML hiển thị các chú giải trạng thái màu sắc")
    stats_html: str = Field(..., description="HTML hiển thị các thẻ đếm chỉ số")
    code_tracker_html: str = Field(..., description="Mã HTML chứa code. Mỗi dòng code nằm trong <div class='code-line' id='line-N'>...</div>")
    input_label: str = Field(..., description="Nhãn ô nhập liệu test")
    input_default: str = Field(..., description="Giá trị mặc định test")
    engine_js: str = Field(..., description="Mã JavaScript chứa class InteractiveVisualizerEngine hoàn chỉnh")
