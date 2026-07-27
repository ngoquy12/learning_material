"""
agents/pm_generator_agent.py

AI Curriculum Architect Agent that generates a complete, pedagogically-sound 
10-Column PM Standard Curriculum from scratch given high-level course parameters:
- course_name
- description (Short description)
- tech_stack
- total_sessions
- target_persona
- course_outcomes
- capstone_target
"""

import json
from typing import Dict, Any, List
from core.llm import call_llm

SYSTEM_PROMPT = """Bạn là một Kiến trúc sư Chương trình (Curriculum Architect) và Giám đốc Học thuật (Senior Academic Director) hàng đầu với 15 năm kinh nghiệm thiết kế khóa học công nghệ chuẩn quốc tế.
Nhiệm vụ của bạn là xây dựng TOÀN BỘ cấu trúc chương trình môn học (PM Syllabus) 10 CỘT CHUẨN SƯ PHẠM từ buổi đầu tiên đến buổi cuối cùng dựa trên tên môn học và mô tả ngắn được cung cấp.

BẮT BUỘC TUÂN THỦ TỰ ĐỘNG CÁC QUY TẮC SƯ PHẠM VÀ NHỊP ĐỘ HỌC TẬP SAU:

1. QUY TẮC NHỊP ĐỘ SESSION (SESSION CADENCE DISTRIBUTION):
   - Session 01: BẮT BUỘC là "Orientation" (Mã session: ORIENTATION, session_type_vn: "Định hướng & Cài đặt").
   - Nhịp độ học tập: Cứ 2 đến 3 Session Lý thuyết ("THEORY") BẮT BUỘC phải có 1 Session Thực hành ("PRACTICE") tổng hợp bài tập.
   - Khoảng mốc 25% và 75% tổng thời lượng: Chèn 1 Session "MINI_PROJECT" (Dự án nhỏ thực chiến tích lũy).
   - Session cuối cùng (Session N): BẮT BUỘC là "FINAL_PROJECT" (Đồ án Capstone cuối khóa).

2. QUY TẮC COGNITIVE LOAD (GIỚI HẠN TẢI NHẬN THỨC):
   - Mỗi Session Lý thuyết ("THEORY") chỉ chứa từ 2 đến 4 Lessons nhỏ. Mỗi Lesson có phạm vi vừa đủ học trong 45-60 phút.

3. QUY TẮC SCOPE SANDWICH (KẸP 3 LỚP RANH GIỚI):
   - `details`: Mô tả chi tiết các chủ đề, từ khóa, cú pháp dạy trong lesson này.
   - `expected_outcome`: Kết quả mong đợi theo Thang đo tư duy Bloom's Taxonomy (Ghi rõ sản phẩm / Năng lực sinh viên tự viết/làm/đạt được sau bài học này).
   - `allowed_scope`: Phạm vi ĐÃ HỌC (Tích lũy các kiến thức/kỹ năng sinh viên đã làm chủ từ các Session 1 đến N-1).
   - `forbidden_scope`: Phạm vi CẤM DÙNG (CẤM dùng các kiến thức/khái niệm của các bài học & session PHÍA SAU trong chương trình + CẤM các kiến thức BÊN NGOÀI môn học).

4. ĐỊNH DẠNG ĐẦU RA BẮT BUỘC: Trả về duy nhất 1 JSON object hợp lệ (Không chứa mã markdown ```json), cấu trúc như sau:
[
  {
    "session_id": "Session 01",
    "session_type_vn": "Định hướng & Cài đặt",
    "session_code": "ORIENTATION",
    "session_title": "Session 01 - Định hướng khóa học & Cài đặt môi trường",
    "lessons": [
      {
        "lesson_title": "Lesson 01: ...",
        "details": "...",
        "expected_outcome": "...",
        "forbidden_scope": "CẤM: ...",
        "allowed_scope": "ĐÃ HỌC: ...",
        "tech_stack": "..."
      }
    ]
  }
]
"""

def pm_generator_agent(
    course_name: str,
    description: str = "",
    tech_stack: str = "",
    total_sessions: int = 30,
    target_persona: str = "",
    course_outcomes: str = "",
    capstone_target: str = ""
) -> str:
    """
    Invokes LLM to generate the complete 10-column PM curriculum array.
    Automatically enriches and infers missing technical attributes from course_name and description.
    """
    user_prompt = f"""Hãy thiết kế toàn bộ cấu trúc PM môn học 10 Cột cho môn học sau:

- Tên môn học: {course_name}
- Mô tả ngắn của môn học: {description or 'Khóa học lập trình chuyên nghiệp từ căn bản tới nâng cao.'}
- Tech Stack & Quy chuẩn: {tech_stack or 'Tự động suy luận Tech Stack chuẩn nhất theo tên môn học'}
- Tổng số buổi học (Sessions): {total_sessions} buổi
- Chân dung sinh viên Target: {target_persona or 'Tự động xây dựng Chân dung sinh viên chuẩn phù hợp nhất với môn học này'}
- Mục tiêu môn học (CLO): {course_outcomes or 'Tự động làm rõ các Mục tiêu kiến thức/kỹ năng chuẩn đầu ra'}
- Sản phẩm Capstone Target: {capstone_target or 'Tự động đề xuất Đồ án Capstone ấn tượng phù hợp'}

LƯU Ý QUAN TRỌNG: Bạn hãy TỰ ĐỘNG PHÂN TÍCH Tên môn học và Mô tả ngắn để tự suy luận, làm rõ và hoàn thiện 100% các thông số Chân dung sinh viên, Mục tiêu môn học CLO, Capstone Target và Tech Stack phù hợp nhất trước khi phân bổ 10 cột chương trình PM.
Hãy sinh chính xác mảng JSON chứa đầy đủ {total_sessions} Sessions từ Session 01 đến Session {total_sessions:02d} theo 10 cột chuẩn sư phạm đã quy định.
"""

    response = call_llm(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
        json_mode=True,
        agent_name="PM Generator Agent"
    )
    return response
