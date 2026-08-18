import os
import json
from pathlib import Path
import jinja2
from core.state import AgentState, require_tech_stack
from core.llm import call_llm
from core.utils.text_sanitizer import extract_and_parse_json, strip_markdown_fence
from agents.creators.common_utils import get_lesson_content, log_agent_tokens

_TEMPLATE_DIR = Path(__file__).resolve().parent.parent.parent / "templates" / "prompts"

def _load_system_prompt(tech_stack: str) -> str:
    """Loads system prompt from Jinja2 template or fallback."""
    template_path = _TEMPLATE_DIR / "reading_questions_system.j2"
    if template_path.exists():
        with open(template_path, "r", encoding="utf-8") as f:
            template = jinja2.Template(f.read())
            return template.render(tech_stack=tech_stack)
    return (
        "You are a Senior E-Learning Pedagogical QA Specialist at Rikkei Education.\n"
        "Your task is to generate a multi-case reading comprehension question set anchored strictly on 1 code snippet."
    )

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

    system_prompt = _load_system_prompt(tech_stack)

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
        reading_data = {
            "code_snippet": f"""# Mã nguồn minh họa nghiệp vụ cho bài học: {lesson_title}
score = 8.5

if score >= 9.0:
    rank = "Xuất sắc"
elif score >= 8.0:
    rank = "Giỏi"
elif score >= 6.5:
    rank = "Khá"
else:
    rank = "Trung bình"

print(f"Học lực: {{rank}}")""",
            "questions": [
                {
                    "id": 1,
                    "title": "Câu 1 (Xung hướng - Tính toán kết quả với dữ liệu X):",
                    "question": f"Nếu giá trị đầu vào là `score = 8.5`, chương trình sẽ thực thi qua những câu lệnh rẽ nhánh nào và in kết quả `rank` ra màn hình là gì?",
                    "explanation": "- Điều kiện `score >= 9.0` (8.5 >= 9.0) trả về `False`.\n- Điều kiện `score >= 8.0` (8.5 >= 8.0) trả về `True`.\n- Gán `rank = 'Giỏi'` và kết quả in ra màn hình là `Học lực: Giỏi`."
                },
                {
                    "id": 2,
                    "title": "Câu 2 (Xung hướng - Thử nghiệm với mốc dữ liệu Y):",
                    "question": "Nếu sửa giá trị thành `score = 7.0`, nhánh rẽ nào sẽ được kích hoạt và kết quả `rank` thay đổi ra sao?",
                    "explanation": "- Các điều kiện `>= 9.0` và `>= 8.0` đều `False`.\n- Điều kiện `score >= 6.5` (7.0 >= 6.5) trả về `True`.\n- Gán `rank = 'Khá'` và in ra màn hình `Học lực: Khá`."
                },
                {
                    "id": 3,
                    "title": "Câu 3 (Nghịch hướng - Suy luận dữ liệu đầu vào từ kết quả Z):",
                    "question": "Để hệ thống xếp loại `rank = 'Giỏi'`, giá trị biến `score` phải thỏa mãn khoảng giá trị toán học nào?",
                    "explanation": "- Biến `score` phải thỏa mãn điều kiện `8.0 <= score < 9.0` (từ 8.0 đến dưới 9.0)."
                },
                {
                    "id": 4,
                    "title": "Câu 4 (Phân tích bẫy lỗi & Trường hợp biên):",
                    "question": "Nếu nhập `score = -1.0` hoặc `score = 11.0`, hãy chỉ ra điểm bất hợp lý của mã nguồn hiện tại và đề xuất cách cải tiến.",
                    "explanation": "- Mã nguồn chưa có nhánh kiểm tra tính hợp lệ dữ liệu (0 <= score <= 10).\n- Khi `score = 11.0`, hệ thống vẫn xếp loại 'Xuất sắc', khi `score = -1.0` xếp loại 'Trung bình'.\n- Cần bổ sung câu lệnh `if score < 0 or score > 10:` ở đầu để báo lỗi dữ liệu không hợp lệ."
                }
            ]
        }

    rq_md = format_reading_questions_to_markdown(reading_data, tech_stack)
    state["reading_questions_json"] = reading_data
    state["reading_questions_markdown"] = rq_md
    log_agent_tokens("Reading_Questions_Agent", state, rq_md)
    return state
