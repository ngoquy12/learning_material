"""
core/schemas/agent_state_schema.py — Kiểm định runtime cho AgentState.

AgentState (core/state.py) là TypedDict(total=False) — thuần chú thích kiểu ở mức
biên dịch (type-checker), KHÔNG có gì kiểm tra lúc chạy thật. Không gì ngăn một node
gán một chuỗi vào field lẽ ra phải là dict, hay quên set field bắt buộc — sai lệch đó
chỉ lộ ra khi crash sâu trong một renderer không liên quan, cách xa nơi gây ra lỗi.

Module này thêm một lớp kiểm định TÙY CHỌN dùng ở ranh giới node, không thay thế
AgentState (đổi cả hệ thống dict-based hiện có sang Pydantic model là refactor có rủi
ro cao, không cần thiết để đạt mục tiêu "phát hiện sai lệch schema sớm"). `extra="allow"`
được bật có chủ đích: state có nhiều key ad-hoc (allowed_scope, chosen_domain,
lesson_blueprint...) mà không phải mọi field ad-hoc đều xứng đáng lên AgentState chính
thức — validator này bắt SAI KIỂU DỮ LIỆU trên field đã biết, không cấm field lạ.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, ValidationError


class AgentStateSchema(BaseModel):
    """
    Ánh xạ lỏng theo AgentState — mọi field đều Optional vì AgentState là total=False
    (không có field nào bắt buộc phải có mặt ngay từ đầu pipeline).

    Đây là công cụ BẮT LỖI KIỂU DỮ LIỆU, không phải hợp đồng đầy đủ: `extra="allow"`
    để các key ad-hoc chưa lên AgentState chính thức (allowed_scope, chosen_domain,
    lesson_blueprint, ...) không bị từ chối.
    """

    model_config = ConfigDict(extra="allow")

    # Core Session & Lesson Identity
    session_id: Optional[str] = None
    lesson_id: Optional[str] = None
    pm_input: Optional[str] = None
    time_reference: Optional[Dict[str, Any]] = None
    learning_outcomes: Optional[Dict[str, Any]] = None
    program_structure: Optional[Dict[str, Any]] = None
    core_ssot: Optional[Dict[str, Any]] = None
    artifacts_status: Optional[Dict[str, str]] = None

    # Tier 2: Lesson-level Core Artifacts
    html_content: Optional[str] = None
    quiz_json: Optional[Any] = None
    practical_lab_markdown: Optional[str] = None
    practical_lab_html: Optional[str] = None
    lab_json: Optional[Any] = None
    reading_questions_markdown: Optional[str] = None
    reading_questions_json: Optional[Any] = None

    # Tier 1: Session-level Core Artifacts & Shared Components
    classroom_lecture_html: Optional[str] = None
    session_quizzes_json: Optional[Any] = None
    homework_markdown: Optional[str] = None
    mindmap_markdown: Optional[str] = None

    # Reviewer Logs & Metadata
    review_logs: Optional[List[Dict[str, Any]]] = None
    scope_audits: Optional[Dict[str, Any]] = None
    previous_lessons: Optional[List[Dict[str, Any]]] = None
    master_content: Optional[Dict[str, Any]] = None
    course_dir_name: Optional[str] = None
    technology_stack: Optional[str] = None
    force_rebuild: Optional[bool] = None
    pm_approved: Optional[bool] = None
    requested_parts: Optional[List[str]] = None
    full_curriculum: Optional[str] = None
    prerequisite_data: Optional[Dict[str, Any]] = None
    prerequisite_checked: Optional[bool] = None
    self_test_markdown: Optional[str] = None

    # Domain Anchor
    session_domain: Optional[Dict[str, Any]] = None
    chosen_domain: Optional[str] = None

    # Legacy compatibility fields
    slide_markdown: Optional[str] = None
    video_script_markdown: Optional[str] = None


class StateValidationError(ValueError):
    """Raised khi state vi phạm kiểu dữ liệu đã khai báo trong AgentStateSchema."""


def validate_state(state: Dict[str, Any], caller: str = "unknown") -> None:
    """
    Kiểm định state tại một ranh giới node.

    Raise ngay với thông báo chỉ rõ node gọi và field sai, thay vì để lỗi trôi tới
    tận một renderer không liên quan rồi mới crash — cùng triết lý với
    require_tech_stack() trong core/state.py: fail lớn tiếng, đúng chỗ, thay vì âm
    thầm sai rồi phát hiện muộn.

    Không raise khi state rỗng/None: đó là input hợp lệ ở một số node (ví dụ state
    khởi tạo trước khi set field đầu tiên).
    """
    if not state:
        return

    try:
        AgentStateSchema.model_validate(state)
    except ValidationError as e:
        field_errors = "; ".join(
            f"{'.'.join(str(p) for p in err['loc'])}: {err['msg']}" for err in e.errors()
        )
        raise StateValidationError(
            f"❌ [STATE KHÔNG HỢP LỆ] Gọi từ '{caller}': {field_errors}"
        ) from e
