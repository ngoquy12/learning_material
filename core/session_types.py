"""
core/session_types.py
Standardized Session Types & Deliverables Schema for Elearning Agent Framework.

Supported Session Types & Deliverables:
1. THEORY (Session Lý Thuyết):
   - Per-Lesson: Interactive Reading HTML, Slide HTML, Lesson Labs (3-5 exercises)
   - Per-Session: Entry Quiz, Session Comprehensive Practice (5 large exercises), Session Quiz Excel (.xlsx), Session Homework, reading_all.html, session_slides.html, Hyperframes Narration Script
2. PRACTICE (Session Thực Hành):
   - Practice Labs (Basic -> Advanced), Homework, Data Tasks
3. MINI_PROJECT (Session Mini Project):
   - 4 Entry Tests, SRS Spec, Mini Project Prompt & Rubric (100 pts)
4. FINAL_PROJECT (Session Dự Án Cuối Khóa):
   - Capstone Spec, Full SRS, System Architecture, Capstone Rubric (100 pts)
"""

import os
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class SessionType(str, Enum):
    THEORY = "THEORY"
    PRACTICE = "PRACTICE"
    MINI_PROJECT = "MINI_PROJECT"
    FINAL_PROJECT = "FINAL_PROJECT"
    # Buổi định hướng/nhập môn: giới thiệu lộ trình, demo sản phẩm cuối khoá, cài đặt
    # môi trường. Chưa dạy kiến thức chuyên môn nào nên không có gì để khảo thí.
    ORIENTATION = "ORIENTATION"


# Từ khoá nhận diện buổi định hướng, so trên TÊN và HÌNH THỨC buổi học.
#
# Vì sao không dùng số thứ tự: bản trước nhận diện bằng 'SESSION 01' nằm trong mã
# buổi, tức MỌI môn học đều bị coi là có buổi định hướng ở buổi đầu. Điều đó sai với
# phần lớn môn: rất nhiều môn vào thẳng kiến thức ngay buổi 1, và khi đó toàn bộ
# quiz, bài thực hành và câu hỏi bài đọc của buổi 1 bị bỏ qua trong im lặng. Ngược
# lại, môn nào đặt buổi định hướng ở buổi 2 (sau một buổi kiểm tra đầu vào chẳng
# hạn) thì lại không được nhận ra.
#
# Bộ từ khoá này cố ý thiên về ĐỘ CHÍNH XÁC hơn độ bao phủ, vì hai loại sai có hậu
# quả rất khác nhau: nhận nhầm một buổi kiến thức thành buổi định hướng sẽ âm thầm
# xoá sổ quiz, bài thực hành và câu hỏi đọc hiểu của buổi đó; còn bỏ sót một buổi
# định hướng thật thì cùng lắm sinh thừa vài tài nguyên, người biên soạn nhìn ra ngay.
# Vì vậy KHÔNG đưa "nhập môn" vào danh sách mặc định: trong học thuật Việt Nam đó
# thường là một phần TÊN MÔN HỌC ("Nhập môn Lập trình", "Nhập môn Cơ sở dữ liệu"),
# không phải buổi định hướng.
#
# Bổ sung từ khoá cho môn học đặc thù qua biến môi trường ORIENTATION_SESSION_KEYWORDS
# (ngăn cách bằng dấu phẩy) thay vì sửa mã nguồn.
_DEFAULT_ORIENTATION_KEYWORDS: List[str] = [
    "định hướng",
    "tổng quan lộ trình",
    "giới thiệu môn học",
    "giới thiệu khóa học",
    "giới thiệu khoá học",
    "khai giảng",
    "orientation",
    "onboarding",
    "course introduction",
    "kick-off",
    "kickoff",
]


def get_orientation_keywords() -> List[str]:
    """Danh sách từ khoá nhận diện buổi định hướng, có thể mở rộng qua môi trường."""
    extra = os.getenv("ORIENTATION_SESSION_KEYWORDS", "")
    custom = [kw.strip().lower() for kw in extra.split(",") if kw.strip()]
    return _DEFAULT_ORIENTATION_KEYWORDS + custom

# Full list of deliverables mapped per session type
SESSION_DELIVERABLES: Dict[SessionType, List[str]] = {
    SessionType.THEORY: [
        "1. Bài đọc HTML tương tác (Per-Lesson)",
        "2. Slide bài giảng HTML + Narration Script (Per-Lesson)",
        "3. Bài thực hành cho từng Lesson (Số lượng linh hoạt theo nội dung trọng tâm)",
        "4. Quiz trắc nghiệm cho từng Lesson (Đúng 5 câu / Lesson)",
        "5. Bài kiểm tra trắc nghiệm đầu giờ (Entry Quiz / Đúng 45 câu Excel .xlsx)",
        "6. Bài kiểm tra trắc nghiệm cuối giờ (Exit Quiz / Đúng 45 câu Excel .xlsx)",
        "7. Bài tập về nhà Session (5 bài tập phân 5 cấp độ + 1 bài tập tổng hợp)",
        "8. File gộp bài đọc Session (reading_all.html)",
        "9. File gộp Slide Session (session_slides.html)"
    ],
    SessionType.PRACTICE: [
        "1. Bộ bài tập thực hành phân cấp (Phân loại Nhận biết -> Vận dụng cao)",
        "2. Bài tập thực hành xử lý dữ liệu thực tế",
        "3. Bài tập về nhà (Session Homework + Lời giải mẫu AST check)",
        "4. Kịch bản kiểm tra trạng thái bài tập"
    ],
    SessionType.MINI_PROJECT: [
        "1. 4 Bài kiểm tra đầu giờ (Entry Tests)",
        "2. Tài liệu đặc tả yêu cầu phần mềm SRS tinh gọn",
        "3. Đề bài Mini Project (Task Cards)",
        "4. Thang điểm Rubric chấm AI (Đúng 100 điểm)"
    ],
    SessionType.ORIENTATION: [
        "1. Bài đọc HTML tương tác giới thiệu lộ trình môn học",
        "2. Slide bài giảng định hướng",
        "3. Kịch bản thuyết minh video giới thiệu"
    ],
    SessionType.FINAL_PROJECT: [
        "1. Đề tài Đồ án Capstone cuối khóa",
        "2. Sơ đồ Kiến trúc hệ thống tổng thể & CSDL",
        "3. Tài liệu đặc tả yêu cầu phần mềm SRS đầy đủ",
        "4. Thang điểm Rubric chấm Đồ án tốt nghiệp (Đúng 100 điểm)",
        "5. Hướng dẫn báo cáo & Trình chiếu bảo vệ Đồ án"
    ]
}

# Standardized exact quantity parameters
SESSION_QUANTITIES: Dict[str, int] = {
    "LESSON_QUIZ_COUNT": 5,
    "ENTRY_QUIZ_COUNT": 45,
    "EXIT_QUIZ_COUNT": 45,
    "HOMEWORK_LEVEL_COUNT": 5,
    "HOMEWORK_COMPREHENSIVE_COUNT": 1,
    "TOTAL_HOMEWORK_COUNT": 6
}

def detect_session_type(session_data: Dict[str, Any]) -> SessionType:
    """
    Detects the explicit SessionType based on session title, type field, or metadata.
    """
    explicit_type = str(session_data.get("session_type", "")).upper().strip()
    if explicit_type in SessionType.__members__:
        return SessionType[explicit_type]
        
    title = str(session_data.get("session_title", "") or session_data.get("title", "")).lower()
    
    explicit_code = str(session_data.get("session_code", "")).upper().strip()
    if explicit_code in SessionType.__members__:
        return SessionType[explicit_code]

    raw_type = str(session_data.get("session_type", "")).lower().strip()

    # Buổi định hướng xét TRƯỚC các loại khác: tên buổi định hướng thường kèm chữ
    # "giới thiệu"/"tổng quan" về lộ trình hoặc sản phẩm, dễ bị luật khác bắt nhầm.
    orientation_keywords = get_orientation_keywords()
    if any(kw in title for kw in orientation_keywords) or any(
        kw in raw_type for kw in orientation_keywords
    ):
        return SessionType.ORIENTATION

    if any(kw in title for kw in ["dự án cuối khóa", "capstone", "final project", "đồ án cuối môn"]):
        return SessionType.FINAL_PROJECT
    elif any(kw in title for kw in ["mini project", "mini-project", "tiểu luận"]):
        return SessionType.MINI_PROJECT
    elif any(kw in title for kw in ["thực hành", "practice", "lab", "luyện tập"]):
        return SessionType.PRACTICE
        
    return SessionType.THEORY


# ─────────────────────────────────────────────────────────────────────────────
# Phần học liệu cấp lesson được sinh cho từng loại buổi
# ─────────────────────────────────────────────────────────────────────────────
#
# Trước đây chính sách này nằm rải rác dưới dạng if-else lặp lại trong 4 pipeline
# của core/graph.py, mỗi nơi một bản sao cùng một điều kiện. Thêm một loại tài
# nguyên mới là phải nhớ sửa đủ 4 chỗ. Gom về một bảng khai báo để đọc được chính
# sách trong một cái nhìn và sửa ở đúng một nơi.
#
# None nghĩa là KHÔNG giới hạn: sinh mọi phần mà người dùng yêu cầu.
SESSION_KIND_PARTS: Dict[SessionType, Optional[Tuple[str, ...]]] = {
    # Buổi định hướng chưa dạy kiến thức chuyên môn nào, nên không có gì để khảo
    # thí: không quiz, không bài thực hành, không câu hỏi đọc hiểu.
    SessionType.ORIENTATION: ("html", "slide", "video_script"),
    SessionType.THEORY: None,
    SessionType.PRACTICE: None,
    SessionType.MINI_PROJECT: None,
    SessionType.FINAL_PROJECT: None,
}


def allowed_parts_for(session_kind: Any) -> Optional[Tuple[str, ...]]:
    """
    Trả về bộ phần học liệu được phép sinh cho loại buổi này, hoặc None nếu không
    giới hạn. Loại buổi lạ cũng trả None: không nhận ra thì sinh đầy đủ còn hơn là
    âm thầm bỏ bớt tài nguyên của một buổi học bình thường.
    """
    if isinstance(session_kind, SessionType):
        return SESSION_KIND_PARTS.get(session_kind)
    try:
        return SESSION_KIND_PARTS.get(SessionType(str(session_kind).upper().strip()))
    except ValueError:
        return None


def is_part_allowed(session_kind: Any, part: str) -> bool:
    """Phần học liệu `part` có được sinh cho loại buổi này không."""
    allowed = allowed_parts_for(session_kind)
    return True if allowed is None else part in allowed
