import os
import json
import re
import html
from pathlib import Path
from core.state import AgentState, require_tech_stack
from core.llm import call_llm
from agents.creators.common_utils import log_agent_tokens

def get_session_dir_path(state: AgentState) -> Path:
    """
    Xác định đường dẫn thư mục Session chuẩn.
    """
    from cli.curriculum_parser import get_or_rename_sanitized_folder, format_full_folder_name
    course_dir = Path(state.get("course_dir", "output/courses/Lập_trình_Python"))
    session_id = state.get("session_id", "Session 01")
    core_ssot = state.get("core_ssot", {})
    session_title = core_ssot.get("session_title") or state.get("session_title", "")
    folder_name = format_full_folder_name(session_id, session_title)
    session_dir = get_or_rename_sanitized_folder(course_dir, session_id, folder_name)
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir

def format_session_inclass_exercise_to_markdown(data: dict, tech_stack: str = "") -> str:
    """
    Format bài tập tổng hợp trên lớp (Session In-Class Synthesis Exercise) theo chuẩn Markdown 4 phần.
    """
    title = data.get("title", "Bài tập tổng hợp trên lớp").replace("#", "").strip()
    objectives = data.get("objectives", [])
    obj_md = "\n".join([f"- {o}" for o in objectives]) if objectives else "- Vận dụng tổng hợp toàn bộ kiến thức trong Session.\n- Triển khai bài toán nghiệp vụ doanh nghiệp với dữ liệu đầu vào và đầu ra xác định.\n- Đảm bảo quy chuẩn Clean Code và xử lý an toàn dữ liệu đầu vào."
    
    biz_context = data.get("business_context", "Phát triển mô đun xử lý nghiệp vụ tự động hóa cho hệ thống doanh nghiệp.")
    inputs_text = data.get("inputs_text", "Dữ liệu thông số nghiệp vụ do người dùng nhập từ Console / Terminal.")
    outputs_text = data.get("outputs_text", "Kết quả tính toán và trạng thái xử lý in ra màn hình.")
    
    io_examples = data.get("io_examples", [])
    table_rows = []
    if io_examples:
        for idx, item in enumerate(io_examples, 1):
            c_type = item.get("case", f"Trường hợp {idx}")
            c_in = str(item.get("input", "N/A")).replace("\n", "<br>")
            c_out = str(item.get("output", "N/A")).replace("\n", "<br>")
            c_note = item.get("note", "Xử lý thành công")
            table_rows.append(f"| **{c_type}** | `{c_in}` | `{c_out}` | {c_note} |")
    else:
        table_rows = [
            "| **Trường hợp 1 (Chuẩn)** | `input_data = 100` | `result = Thành công` | Xử lý luồng thành công. |",
            "| **Trường hợp 2 (Ngoại lệ)** | `input_data = -1` | `result = Lỗi dữ liệu` | Bắt lỗi và thông báo hợp lệ. |"
        ]
    
    table_md = "\n".join(table_rows)
    
    tech_reqs = data.get("technical_requirements", [])
    if tech_reqs:
        tech_req_md = "\n".join([f"- {r}" for r in tech_reqs])
    else:
        tech_req_md = "- Kết hợp sử dụng các cấu trúc điều khiển và cú pháp cốt lõi đã học trong Session.\n- Bắt lỗi ngoại lệ và xử lý dữ liệu đầu vào không hợp lệ an toàn.\n- Tuân thủ quy chuẩn đặt tên biến/hàm và trình bày mã nguồn rõ ràng."
        
    checklist = data.get("checklist", [])
    if checklist:
        checklist_md = "\n".join([f"- [ ] {c.replace('[ ]', '').strip()}" for c in checklist])
    else:
        checklist_md = "- [ ] Xây dựng hoàn chỉnh chương trình đáp ứng đúng bối cảnh nghiệp vụ doanh nghiệp.\n- [ ] Trả về kết quả Output chính xác theo đúng bảng ví dụ minh họa cho các trường hợp dữ liệu đầu vào.\n- [ ] Bắt lỗi ngoại lệ và xử lý dữ liệu biên an toàn không gây crash chương trình.\n- [ ] Mã nguồn đạt chuẩn Clean Code, đặt tên biến/hàm đúng quy chuẩn và có chú thích rõ ràng."

    lang = tech_stack.split("/")[0].lower() if tech_stack else "python"

    md_content = f"""# Bài tập tổng hợp trên lớp: {title}

## 1. Mục tiêu bài tập
{obj_md}

## 2. Mô tả bối cảnh & Yêu cầu bài toán (Input / Output)
- **Bối cảnh doanh nghiệp**: {biz_context}
- **Dữ liệu đầu vào (Input)**: {inputs_text}
- **Kết quả đầu ra (Output)**: {outputs_text}

### Bảng ví dụ minh họa Input/Output:
| Trường hợp (Case) | Dữ liệu đầu vào (Input) | Kết quả kỳ vọng (Expected Output) | Ghi chú nghiệp vụ |
| :--- | :--- | :--- | :--- |
{table_md}

## 3. Các bước thực hiện & Quy định kỹ thuật
- **Tài nguyên & Môi trường**: Thực thi trên môi trường `{tech_stack if tech_stack else 'Python 3.10+'}`.
- **Yêu cầu kỹ thuật**:
{tech_req_md}
  *(LƯU Ý: Học viên tự chủ động thiết kế giải thuật và cấu trúc chương trình. Không cung cấp mã nguồn gợi ý).*

## 4. Checklist đánh giá kết quả (Nghiệm thu)
{checklist_md}
"""
    return md_content.strip()

def build_dynamic_fallback(session_title: str, tech_stack: str) -> dict:
    """
    Sinh dữ liệu bài tập tổng hợp trên lớp fallback tự động nếu LLM không trả về đúng định dạng.
    """
    clean_title = re.sub(r'^Session\s*\d+[\s\:-]*', '', session_title).strip()
    return {
        "title": f"Quản lý & Xử lý luồng dữ liệu {clean_title}",
        "objectives": [
            f"Vận dụng tổng hợp toàn bộ kiến thức về {clean_title} trong Session.",
            "Xây dựng chương trình xử lý nghiệp vụ thực tế với dữ liệu Input/Output xác định.",
            "Tối ưu mã nguồn theo quy chuẩn Clean Code và bắt lỗi ngoại lệ an toàn."
        ],
        "business_context": f"Xây dựng mô đun nghiệp vụ tự động hóa quản lý luồng dữ liệu cho hệ thống doanh nghiệp, áp dụng kiến thức {clean_title}. Chương trình chạy trên giao diện Console/Terminal với thời lượng thực hiện khoảng 30 phút.",
        "inputs_text": "Thông số dữ liệu nghiệp vụ nhập từ bàn phím (ví dụ: số lượng, mã định danh, hoặc danh sách thông số).",
        "outputs_text": "Kết quả xử lý nghiệp vụ in ra màn hình Console (ví dụ: tổng chi phí, trạng thái xử lý, hoặc danh sách đã lọc).",
        "io_examples": [
            {
                "case": "Trường hợp 1 (Chuẩn)",
                "input": "val = 50",
                "output": "Trạng thái: Hợp lệ | Chi phí: 50,000 VNĐ",
                "note": "Xử lý thành công luồng nghiệp vụ chuẩn."
            },
            {
                "case": "Trường hợp 2 (Ngoại lệ biên)",
                "input": "val = -5",
                "output": "Lỗi: Giá trị đầu vào không hợp lệ",
                "note": "Bắt lỗi dữ liệu âm và thông báo chính xác."
            }
        ],
        "technical_requirements": [
            f"Kết hợp vận dụng các cấu trúc điều khiển và cú pháp cốt lõi về {clean_title}.",
            "Kiểm soát dữ liệu đầu vào và bắt ngoại lệ an toàn không để crash chương trình.",
            "Tuân thủ quy chuẩn đặt tên và trình bày mã nguồn rõ ràng."
        ],
        "checklist": [
            "Hoàn thành mã nguồn đáp ứng đúng bài toán nghiệp vụ doanh nghiệp.",
            "Kết quả Output khớp 100% với bảng ví dụ minh họa cho các trường hợp dữ liệu.",
            "Xử lý ngoại lệ an toàn và tuân thủ quy chuẩn Clean Code."
        ]
    }

def session_inclass_exercise_creator_agent(state: AgentState) -> AgentState:
    """
    Session In-Class Exercise Creator Agent:
    Sinh Bài tập tổng hợp trên lớp (30 phút) cho cả Session lý thuyết,
    tổng hợp kiến thức toàn bộ các Lesson trong Session thành 1 kịch bản doanh nghiệp thống nhất.
    Sử dụng nguyên tắc 'Closed How - Open What & Why' (Input/Output rõ ràng, CẤM gợi ý code).
    """
    session_id = state.get("session_id", "Session 01")
    tech_stack = require_tech_stack(state, "session_inclass_exercise_creator_agent")

    core_ssot = state.get("core_ssot", {})
    session_title = core_ssot.get("session_title") or state.get("session_title") or "Lập trình Python"
    lessons_summary = state.get("previous_lessons_text", "") or core_ssot.get("lesson_details", "")

    print(f"\n[Session_InClass_Exercise_Agent] Formulating 30-Min Synthesis Exercise for {session_id}: {session_title}")

    system_prompt = f"""You are a Senior Curriculum Architect at Rikkei Education.
Your task is to design a 30-minute in-class synthesis exercise (Bài tập tổng hợp trên lớp 30 phút) for a complete theory session ({session_id}: {session_title}).

CRITICAL PEDAGOGICAL DIRECTIVES:
1. SYNTHESIZE ALL LESSONS IN SESSION: The exercise MUST require students to apply ALL key technical concepts taught across all lessons in this session.
2. 30-MINUTE IN-CLASS EXECUTION TIME & BASIC DIFFICULTY: Designed for students to complete in class within ~30 minutes. Keep business requirements focused, realistic, and non-bloated.
3. CLOSED HOW - OPEN WHAT & WHY (INPUT/OUTPUT CONTRACT):
   - Provide EXPLICIT Input data specifications and Expected Output format.
   - ABSOLUTELY FORBIDDEN to provide code skeletons, algorithm execution hints, or step-by-step code instructions. Students must autonomously design the solution logic.
4. UNIFIED ENTERPRISE SCENARIO DOMAIN: Must strictly use the exact same enterprise business scenario domain established for this session (e.g. ShopeeFood Order Checkout, E-commerce Cart, Student Scholarship Evaluation, Banking Fraud Detection...).
5. STRICT QUALITY RULES & BAN ON AI MARKERS & EMOJIS:
   - ⛔ FORBIDDEN Cliché Words: "nhé", "bẫy lập trình", "thần thánh", "bí kíp", "tất tần tật", "thân mến". Use formal technical terms.
   - ⛔ FORBIDDEN Text Emojis: Absolutely NO emojis (❌, ✅, ⚠️, 🔴, 🟢, ▶).
6. LANGUAGE: 100% Accented Vietnamese (Tiếng Việt có dấu chuẩn sản xuất).
7. OUTPUT FORMAT: Return strictly a valid JSON object matching the requested schema.
"""

    user_prompt = f"""Session Metadata & Scope:
- Session: {session_id} - {session_title}
- Target Tech Stack: {tech_stack}
- Content Summary of Lessons in Session:
{lessons_summary[:5000]}

OUTPUT JSON SCHEMA:
{{
  "title": "Tên bài tập tổng hợp nghiệp vụ doanh nghiệp (VD: Quản lý Luồng Thanh toán & Mã Giảm giá ShopeeFood)",
  "objectives": [
    "Vận dụng tổng hợp toàn bộ các kiến thức [Nêu tên các khái niệm trong session] để giải quyết bài toán nghiệp vụ.",
    "Xây dựng chương trình xử lý với dữ liệu Input/Output xác định.",
    "Rèn luyện kỹ năng Clean Code, đặt tên biến/hàm đúng quy chuẩn và xử lý ngoại lệ an toàn."
  ],
  "business_context": "Mô tả chi tiết 2-3 câu bối cảnh nghiệp vụ doanh nghiệp thực tế...",
  "inputs_text": "Mô tả rõ ràng định dạng, kiểu dữ liệu và các thông số dữ liệu đầu vào người dùng nhập...",
  "outputs_text": "Mô tả rõ ràng kết quả trả về / console output in ra màn hình...",
  "io_examples": [
    {{
      "case": "Trường hợp 1 (Dữ liệu hợp lệ chuẩn)",
      "input": "Nêu ví dụ cụ thể dữ liệu nhập vào...",
      "output": "Nêu ví dụ cụ thể kết quả in ra màn hình...",
      "note": "Xử lý luồng thành công."
    }},
    {{
      "case": "Trường hợp 2 (Ngoại lệ / Dữ liệu biên)",
      "input": "Nêu ví dụ cụ thể dữ liệu biên hoặc không hợp lệ...",
      "output": "Nêu thông báo lỗi / xử lý ngoại lệ...",
      "note": "Bắt lỗi an toàn."
    }}
  ],
  "technical_requirements": [
    "Kết hợp áp dụng đầy đủ các cấu trúc điều khiển và cú pháp cốt lõi trong Session.",
    "Kiểm soát dữ liệu đầu vào và xử lý ngoại lệ an toàn.",
    "Tuân thủ quy chuẩn đặt tên biến/hàm (snake_case/camelCase) và trình bày mã nguồn sạch."
  ],
  "checklist": [
    "Hoàn thành mã nguồn đáp ứng đúng bài toán nghiệp vụ doanh nghiệp.",
    "Kết quả Output khớp 100% với bảng ví dụ minh họa cho các trường hợp dữ liệu.",
    "Xử lý ngoại lệ an toàn và tuân thủ quy chuẩn Clean Code."
  ]
}}
"""

    response_str = call_llm(
        system_prompt,
        user_prompt,
        json_mode=True,
        agent_name="Session_InClass_Exercise_Agent",
        session_id=session_id
    )

    try:
        data = json.loads(response_str)
        if not isinstance(data, dict):
            raise ValueError("Invalid JSON object format")
    except Exception:
        data = build_dynamic_fallback(session_title, tech_stack)

    ex_md = format_session_inclass_exercise_to_markdown(data, tech_stack)
    
    state["session_inclass_exercise_json"] = data
    state["session_inclass_exercise_markdown"] = ex_md
    
    # Save file to Session 'Bài tập' directory if session_dir exists
    try:
        session_dir = get_session_dir_path(state)
        ex_dir = session_dir / "Bài tập"
        ex_dir.mkdir(parents=True, exist_ok=True)
        
        ex_file = ex_dir / "exercise.md"
        with open(ex_file, "w", encoding="utf-8") as f:
            f.write(ex_md)
        print(f"  [Session In-Class Exercise Saved] -> {ex_file}")
    except Exception as err:
        print(f"  [Warning] Could not write exercise file to disk: {err}")

    log_agent_tokens("Session_InClass_Exercise_Agent", state, ex_md)
    return state
