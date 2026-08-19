# core/state.py
from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict, NotRequired

# 2-Tier Standard Resource Constants
DEFAULT_LESSON_PARTS = ["html", "quiz", "lab", "reading_questions"]
DEFAULT_SESSION_PARTS = ["classroom_lecture", "quiz_session", "homework", "mindmap"]
ALL_REQUESTED_PARTS = DEFAULT_LESSON_PARTS + DEFAULT_SESSION_PARTS

class AgentState(TypedDict, total=False):
    # Core Session & Lesson Identity
    session_id: str                     # Mã Session hiện tại (ví dụ: Session 01)
    lesson_id: str                      # Mã Lesson hiện tại (ví dụ: Lesson 01)
    pm_input: str                       # Văn bản PM thô đầu vào hoặc mô tả môn học
    time_reference: Dict[str, Any]      # Thời gian tham khảo (ví dụ: số tuần, số giờ)
    learning_outcomes: Dict[str, Any]   # Chuẩn đầu ra (Bloom's Taxonomy)
    program_structure: Dict[str, Any]   # Cấu trúc cây thư mục môn học
    core_ssot: Dict[str, Any]           # Bản đồ tri thức gốc trung tâm của Session
    artifacts_status: Dict[str, str]    # Trạng thái từng tài nguyên (Pending/Approved/Outdated)
    
    # Tier 2: Lesson-level Core Artifacts
    html_content: str                   # Mã nguồn Bài đọc HTML (reading.html)
    quiz_json: Dict[str, Any]           # Dữ liệu Quizz trắc nghiệm Lesson (quiz.json)
    practical_lab_markdown: str         # Nội dung Bài thực hành Lab (practical_lab.md)
    practical_lab_html: str             # Mã nguồn HTML Bài thực hành Lab
    lab_json: Dict[str, Any]            # Cấu trúc JSON bài thực hành
    reading_questions_markdown: str     # Nội dung Câu hỏi bài đọc (reading_questions.md)
    reading_questions_json: Dict[str, Any] # Cấu trúc JSON câu hỏi bài đọc
    
    # Tier 1: Session-level Core Artifacts & Shared Components
    classroom_lecture_html: str         # Bài giảng trực quan trên lớp (classroom_lecture.html)
    session_quizzes_json: Dict[str, Any]# Quizz đầu giờ & Quizz cuối giờ Session
    homework_markdown: str              # 15 Bài tập phân cấp độ + 1 Bài tổng hợp trên lớp
    mindmap_markdown: str               # Sơ đồ tư duy Markmap cho Lesson/Session
    
    # Reviewer Logs & Metadata
    review_logs: List[Dict[str, Any]]   # Nhật ký sửa đổi và feedback của Reviewers
    previous_lessons: NotRequired[List[Dict[str, Any]]]
    master_content: NotRequired[Dict[str, Any]]
    course_dir_name: NotRequired[str]
    technology_stack: NotRequired[str]
    force_rebuild: NotRequired[bool]
    pm_approved: NotRequired[bool]
    requested_parts: NotRequired[List[str]]
    full_curriculum: NotRequired[str]
    prerequisite_data: NotRequired[Dict[str, Any]]
    prerequisite_checked: NotRequired[bool]
    self_test_markdown: NotRequired[str]

    # Domain Anchor (Single Unified Domain per Session)
    session_domain: NotRequired[Dict[str, Any]]
    chosen_domain: NotRequired[str]

    # Legacy compatibility fields (soft-deprecated)
    slide_markdown: NotRequired[str]
    video_script_markdown: NotRequired[str]


def require_tech_stack(state: Any, caller_name: str = "Agent") -> str:
    """
    Strict Technology Stack Validator.
    Extracts technology_stack from state or tech_stack key.
    STRICTLY FORBIDS hardcoded fallback defaults (no fallback to python/fastapi, python/core, etc.).
    If technology_stack is missing or empty, raises an explicit ValueError immediately.
    """
    if not state or not isinstance(state, dict):
        raise ValueError(
            f"❌ [LỖI THIẾU TECHNOLOGY STACK] {caller_name}: AgentState bị None hoặc không phải dict hợp lệ. "
            f"Hệ thống TUYỆT ĐỐI KHÔNG fallback/hardcode bất kỳ công nghệ nào. Vui lòng truyền --tech-stack chính xác."
        )

    stack = state.get("technology_stack") or state.get("tech_stack")
    if not stack or not str(stack).strip():
        raise ValueError(
            f"❌ [LỖI THIẾU TECHNOLOGY STACK] {caller_name}: Không tìm thấy 'technology_stack' trong AgentState. "
            f"Hệ thống TUYỆT ĐỐI KHÔNG fallback/hardcode bất kỳ công nghệ nào. Vui lòng truyền --tech-stack chính xác."
        )
    return str(stack).strip()