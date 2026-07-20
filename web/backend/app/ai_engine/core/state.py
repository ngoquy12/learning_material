from typing import List, Dict, Any
from typing_extensions import TypedDict, NotRequired

class AgentState(TypedDict):
    session_id: str                     # Mã Session hiện tại (ví dụ: Session 01)
    lesson_id: str                      # Mã Lesson hiện tại (nếu có)
    pm_input: str                       # Văn bản PM thô đầu vào hoặc mô tả môn học
    time_reference: Dict[str, Any]      # Thời gian tham khảo (ví dụ: số tuần, số giờ)
    learning_outcomes: Dict[str, Any]   # Chuẩn đầu ra (Bloom's Taxonomy)
    program_structure: Dict[str, Any]   # Cấu trúc cây thư mục môn học
    core_ssot: Dict[str, Any]           # Bản đồ tri thức gốc trung tâm của Session
    artifacts_status: Dict[str, str]    # Trạng thái từng tài nguyên (Pending/Approved/Outdated)
    html_content: str                   # Mã nguồn HTML hiện tại
    slide_markdown: str                 # Cấu trúc slide hiện tại
    quiz_json: Dict[str, Any]           # Dữ liệu câu hỏi hiện tại
    video_script_markdown: str          # Kịch bản quay video cho từng lesson
    mindmap_markdown: str               # Sơ đồ tư duy cho từng lesson
    review_logs: List[Dict[str, Any]]   # Nhật ký sửa đổi và feedback của Reviewers

    # Optional / transient pipeline keys
    previous_lessons: NotRequired[List[Dict[str, Any]]]
    master_content: NotRequired[Dict[str, Any]]
    video_script_json: NotRequired[Dict[str, Any]]
    video_lesson_slug: NotRequired[str]
    self_test_markdown: NotRequired[str]
    course_dir_name: NotRequired[str]
    technology_stack: NotRequired[str]
    force_rebuild: NotRequired[bool]
    pm_approved: NotRequired[bool]
    requested_parts: NotRequired[List[str]]
    full_curriculum: NotRequired[str]
    hyperframes_project_path: NotRequired[str | None]
    prerequisite_data: NotRequired[Dict[str, Any]]
    prerequisite_checked: NotRequired[bool]