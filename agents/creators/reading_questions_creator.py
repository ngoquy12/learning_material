import os
import json
from pathlib import Path
import jinja2
from core.state import AgentState, require_tech_stack
from core.llm import call_llm
from core.utils.text_sanitizer import extract_and_parse_json, strip_markdown_fence
from core.renderers.lecture.text_sanitizer import detect_file_info_for_tech_stack
from agents.creators.common_utils import get_lesson_content, log_agent_tokens

from core.prompts import render_prompt
from core.domain_knowledge import get_domain_for_session, format_domain_rules_for_prompt

def _load_system_prompt(
    tech_stack: str,
    session_id: str = "",
    session_title: str = "",
    chosen_domain: str = "",
    forbidden_scope: str = "",
    allowed_scope: str = ""
) -> str:
    """Loads system prompt from Jinja2 template via PromptManager."""
    session_domain_data = get_domain_for_session(session_id, session_title, chosen_domain or "")
    active_domain = chosen_domain or session_domain_data.get("name_vi", "")
    domain_prompt_block = format_domain_rules_for_prompt(session_domain_data) if active_domain else ""
    return render_prompt("reading_questions_system.j2", {
        "tech_stack": tech_stack,
        "chosen_domain": active_domain,
        "domain_prompt_block": domain_prompt_block,
        "forbidden_scope": forbidden_scope,
        "allowed_scope": allowed_scope
    })

def format_reading_questions_to_markdown(data, tech_stack: str = "") -> str:
    """
    Format bộ câu hỏi bài đọc đa trường hợp (Multi-case Code Tracing) theo chuẩn Markdown.
    """
    if isinstance(data, dict):
        code_snippet = data.get("code_snippet") or data.get("anchored_code") or ""
        questions = data.get("questions") or data.get("cases") or []
    elif isinstance(data, list):
        code_snippet = ""
        questions = data
    else:
        code_snippet = ""
        questions = []

    md_lines = ["# Bộ câu hỏi kiểm tra bài đọc (Reading Comprehension Questions)\n"]

    if code_snippet:
        md_lines.append("## Tình huống & Mã nguồn kiểm tra")
        md_lines.append("Dựa trên mã nguồn nghiệp vụ được trích dẫn từ bài đọc:\n")
        lang = tech_stack.split("/")[0].lower() if tech_stack else "text"
        md_lines.append(f"```{lang}\n{code_snippet.strip()}\n```\n")
        md_lines.append("---\n")

    for idx, q in enumerate(questions, 1):
        if isinstance(q, dict):
            q_title = q.get("title") or f"Câu {idx}:"
            q_text = q.get("question") or q.get("content") or f"Câu hỏi kiểm tra trường hợp {idx}"
            explanation = q.get("explanation") or q.get("answer_guide") or "Phân tích và giải thích chi tiết dựa trên mã nguồn bài đọc."
        else:
            q_title = f"Câu {idx}:"
            q_text = str(q)
            explanation = "Phân tích và giải thích chi tiết dựa trên mã nguồn bài đọc."

        clean_text = q_text.strip()
        if clean_text.startswith(q_title):
            full_heading = clean_text
        else:
            full_heading = f"{q_title} {clean_text}".strip()

        md_lines.append(f"### {full_heading}")
        exp_lines = explanation.strip().split("\n")
        formatted_exp = "\n> ".join(exp_lines)
        md_lines.append(f"> **Gợi ý trả lời & Định hướng đáp án:**\n> {formatted_exp}\n")
        md_lines.append("---\n")

    return "\n".join(md_lines).strip()

def _build_offline_fallback_reading_data(tech_stack: str, lesson_title: str) -> dict:
    """
    Tech-stack-aware offline fallback used ONLY when the LLM call fails/returns invalid JSON.
    Previously this always returned Python `if/elif/else` syntax regardless of tech_stack.
    """
    _, lang = detect_file_info_for_tech_stack(tech_stack, lesson_title)

    if lang in ("javascript", "typescript"):
        code_snippet = f"""// Mã nguồn minh họa nghiệp vụ cho bài học: {lesson_title}
const score = 8.5;
let rank;

if (score >= 9.0) {{
  rank = "Xuất sắc";
}} else if (score >= 8.0) {{
  rank = "Giỏi";
}} else if (score >= 6.5) {{
  rank = "Khá";
}} else {{
  rank = "Trung bình";
}}

console.log(`Học lực: ${{rank}}`);"""
    elif lang == "python":
        code_snippet = f"""# Mã nguồn minh họa nghiệp vụ cho bài học: {lesson_title}
score = 8.5

if score >= 9.0:
    rank = "Xuất sắc"
elif score >= 8.0:
    rank = "Giỏi"
elif score >= 6.5:
    rank = "Khá"
else:
    rank = "Trung bình"

print(f"Học lực: {{rank}}")"""
    else:
        code_snippet = f"""# Mã nguồn minh họa nghiệp vụ cho bài học: {lesson_title} (cú pháp {tech_stack})
# score = 8.5
# Rẽ nhánh theo các mốc: >= 9.0 -> "Xuất sắc"; >= 8.0 -> "Giỏi"; >= 6.5 -> "Khá"; else -> "Trung bình"
# In/log kết quả rank theo cú pháp chuẩn của {tech_stack}"""

    return {
        "code_snippet": code_snippet,
        "questions": [
            {
                "id": 1,
                "title": "Câu 1 (Xung hướng - Tính toán kết quả với dữ liệu X):",
                "question": "Nếu giá trị đầu vào là `score = 8.5`, chương trình sẽ thực thi qua những nhánh điều kiện nào và kết quả `rank` là gì?",
                "explanation": "- Điều kiện `score >= 9.0` (8.5 >= 9.0) là sai.\n- Điều kiện `score >= 8.0` (8.5 >= 8.0) là đúng.\n- Gán `rank = \"Giỏi\"` và kết quả xuất ra là `Học lực: Giỏi`."
            },
            {
                "id": 2,
                "title": "Câu 2 (Xung hướng - Thử nghiệm với mốc dữ liệu Y):",
                "question": "Nếu sửa giá trị thành `score = 7.0`, nhánh rẽ nào sẽ được kích hoạt và kết quả `rank` thay đổi ra sao?",
                "explanation": "- Các điều kiện `>= 9.0` và `>= 8.0` đều sai.\n- Điều kiện `score >= 6.5` (7.0 >= 6.5) là đúng.\n- Gán `rank = \"Khá\"` và kết quả xuất ra là `Học lực: Khá`."
            },
            {
                "id": 3,
                "title": "Câu 3 (Nghịch hướng - Suy luận dữ liệu đầu vào từ kết quả Z):",
                "question": "Để hệ thống xếp loại `rank = \"Giỏi\"`, giá trị biến `score` phải thỏa mãn khoảng giá trị toán học nào?",
                "explanation": "- Biến `score` phải thỏa mãn điều kiện `8.0 <= score < 9.0` (từ 8.0 đến dưới 9.0)."
            },
            {
                "id": 4,
                "title": "Câu 4 (Phân tích bẫy lỗi & Trường hợp biên):",
                "question": "Nếu nhập `score = -1.0` hoặc `score = 11.0`, hãy chỉ ra điểm bất hợp lý của mã nguồn hiện tại và đề xuất cách cải tiến.",
                "explanation": "- Mã nguồn chưa có nhánh kiểm tra tính hợp lệ dữ liệu (0 <= score <= 10).\n- Khi `score = 11.0`, hệ thống vẫn xếp loại \"Xuất sắc\"; khi `score = -1.0`, xếp loại \"Trung bình\".\n- Cần bổ sung điều kiện kiểm tra biên ở đầu để báo lỗi dữ liệu không hợp lệ."
            }
        ]
    }

def reading_questions_creator_agent(state: AgentState) -> AgentState:
    """
    Reading Questions Creator Agent:
    Tạo bộ câu hỏi kiểm tra bài đọc đa trường hợp (Multi-Case Practical Code Tracing Questions)
    neo trực tiếp trên mã nguồn/kịch bản thực tế từ bài đọc (reading.html),
    xuất file Markdown (reading_questions.md) lưu vào state['reading_questions_markdown'].
    """
    session_id = state.get("session_id", "Session 01")
    lesson_id = state.get("lesson_id", "")
    tech_stack = require_tech_stack(state, "reading_questions_creator_agent")

    core_ssot = state.get("core_ssot", {})
    lesson_title = core_ssot.get("session_title") or core_ssot.get("lesson_title") or "Lập trình Ứng dụng Doanh Nghiệp"
    lesson_details = core_ssot.get("lesson_details", "")
    expected_output = core_ssot.get("expected_output", "")

    print(f"\n[Reading_Questions_Agent] Formulating Multi-Case Code Tracing Reading Questions for {session_id} - {lesson_id}: {lesson_title}")

    content = state.get("lesson_content")
    if not content:
        content = get_lesson_content(
            session_id=session_id,
            lesson_id=lesson_id,
            lesson_title=lesson_title,
            lesson_details=lesson_details,
            expected_output=expected_output,
            attempt_num=1,
            core_ssot=core_ssot,
            state=state
        )

    # Extract full article text from lesson content for data-bound question generation
    problem_text = content.get("problem", "") if isinstance(content, dict) else ""
    analysis_text = content.get("analysis", "") if isinstance(content, dict) else ""
    solution_text = content.get("solution", "") if isinstance(content, dict) else ""
    example_text = content.get("example", "") if isinstance(content, dict) else ""
    summary_text = content.get("summary", "") if isinstance(content, dict) else ""

    full_article_context = f"{problem_text}\n\n{analysis_text}\n\n{solution_text}\n\n{example_text}\n\n{summary_text}".strip()

    chosen_domain = state.get("chosen_domain", "")
    forbidden_scope = state.get("forbidden_scope", "")
    allowed_scope = state.get("allowed_scope", "")

    system_prompt = _load_system_prompt(
        tech_stack,
        session_id=session_id,
        session_title=lesson_title,
        chosen_domain=chosen_domain,
        forbidden_scope=forbidden_scope,
        allowed_scope=allowed_scope
    )

    user_prompt = f"""Full Lesson Reading Article Content:
=== LESSON READING ARTICLE CONTENT ===
{full_article_context[:7000]}

Lesson Metadata:
- Session: {session_id}
- Lesson: {lesson_id} - {lesson_title}
- Target Tech Stack: {tech_stack}

OUTPUT JSON SCHEMA:
{{
  "code_snippet": "# Trích dẫn đoạn mã nguồn / kịch bản ví dụ thực tế chính từ bài đọc (10-25 dòng code)",
  "questions": [
    {{
      "id": 1,
      "title": "Câu 1 (Xung hướng - Tính toán kết quả với dữ liệu X):",
      "question": "Nếu dữ liệu đầu vào là X, chương trình sẽ thực thi qua những nhánh điều kiện nào và trả về kết quả biến / console output là bao nhiêu?",
      "explanation": "- Chi tiết các bước thực thi, từng nhánh rẽ và giá trị kết quả thu được..."
    }},
    {{
      "id": 2,
      "title": "Câu 2 (Xung hướng - Thử nghiệm với mốc dữ liệu Y):",
      "question": "Nếu người dùng thay đổi dữ liệu đầu vào thành Y, hãy chỉ ra nhánh rẽ được kích hoạt và kết quả thu được.",
      "explanation": "- Chi tiết nhánh điều kiện được kích hoạt và kết quả mới..."
    }},
    {{
      "id": 3,
      "title": "Câu 3 (Nghịch hướng - Suy luận dữ liệu đầu vào từ kết quả Z):",
      "question": "Để hệ thống trả về kết quả Z (hoặc nhánh Z được kích hoạt), dữ liệu đầu vào cần phải thỏa mãn điều kiện toán học nào?",
      "explanation": "- Điều kiện logic / khoảng giá trị của dữ liệu đầu vào..."
    }},
    {{
      "id": 4,
      "title": "Câu 4 (Phân tích bẫy lỗi & Trường hợp biên):",
      "question": "Nếu nhập dữ liệu đầu vào biên/không hợp lệ hoặc đảo thứ tự điều kiện/toán tử, phân tích hậu quả lỗi và nêu cách khắc phục.",
      "explanation": "- Phân tích bẫy lỗi Gotcha / Unreachable Code và cách sửa chuẩn..."
    }}
  ]
}}
"""

    response_str = call_llm(
        system_prompt,
        user_prompt,
        json_mode=True,
        agent_name="Reading_Questions_Agent",
        session_id=session_id,
        lesson_id=lesson_id
    )

    data = extract_and_parse_json(response_str, default=None)
    if isinstance(data, list):
        reading_data = {"code_snippet": "", "questions": data}
    elif isinstance(data, dict):
        reading_data = data
    else:
        reading_data = _build_offline_fallback_reading_data(tech_stack, lesson_title)

    rq_md = format_reading_questions_to_markdown(reading_data, tech_stack)
    state["reading_questions_json"] = reading_data
    state["reading_questions_markdown"] = rq_md
    log_agent_tokens("Reading_Questions_Agent", state, rq_md)
    return state
