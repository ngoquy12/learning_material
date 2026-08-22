import os
import json
from pathlib import Path
import jinja2
from core.state import AgentState, require_tech_stack
from core.llm import call_llm
from core.utils.text_sanitizer import extract_and_parse_json, strip_markdown_fence
from core.renderers.lecture.text_sanitizer import detect_file_info_for_tech_stack
from agents.creators.common_utils import get_lesson_content, get_lesson_dir, log_agent_tokens

from core.prompts import render_prompt
from core.domain_knowledge import get_domain_for_session, format_domain_rules_for_prompt


def _extract_real_reading_content(state: AgentState) -> tuple:
    """
    Trích xuất TRỰC TIẾP nội dung + code từ file `reading.html` THẬT của lesson này — thay vì dùng
    blueprint trung gian (`master_content`), vốn có thể lệch domain/nội dung so với bài đọc thật đã
    hoàn thiện (đã xác nhận thực tế: blueprint dùng domain khác hẳn reading.html cùng lesson).
    Ưu tiên `state["html_content"]` (nếu đã sinh trong cùng lượt chạy tuần tự), fallback đọc file
    `Bài đọc/reading.html` trên đĩa (đã tồn tại từ lần chạy trước). Trả về (plain_text, code_snippets).
    """
    html_content = state.get("html_content", "")
    if not html_content:
        try:
            lesson_dir = get_lesson_dir(state)
            reading_file = lesson_dir / "Bài đọc" / "reading.html"
            if reading_file.exists():
                html_content = reading_file.read_text(encoding="utf-8")
        except Exception:
            html_content = ""

    if not html_content:
        return "", []

    try:
        from bs4 import BeautifulSoup
    except ImportError:
        return "", []

    soup = BeautifulSoup(html_content, "html.parser")
    article = soup.find("article") or soup

    # Trích code THẬT trong các sandbox (thuộc tính data-original giữ nguyên bản gốc chưa qua
    # highlight.js) và các block code tĩnh (hljs, không có sandbox) — đây là code sinh viên thực sự
    # nhìn thấy trong bài đọc.
    code_snippets = []
    for code_el in article.find_all("code", attrs={"data-original": True}):
        raw = code_el.get("data-original", "").strip()
        if raw and raw not in code_snippets:
            code_snippets.append(raw)
    for pre_el in article.find_all("pre"):
        code_el = pre_el.find("code")
        if code_el and not code_el.get("data-original"):
            text = code_el.get_text().strip()
            if text and text not in code_snippets:
                code_snippets.append(text)

    for tag in article.find_all(["script", "style"]):
        tag.decompose()
    plain_text = article.get_text(separator="\n", strip=True)

    return plain_text, code_snippets

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
    KHÔNG có section "Tình huống & Mã nguồn kiểm tra" riêng — mỗi câu hỏi tự chứa code/dữ liệu
    liên quan trực tiếp trong nội dung câu hỏi (nếu cần), bám sát đúng bài đọc thật.
    """
    if isinstance(data, dict):
        questions = data.get("questions") or data.get("cases") or []
    elif isinstance(data, list):
        questions = data
    else:
        questions = []

    md_lines = ["# Bộ câu hỏi kiểm tra bài đọc (Reading Comprehension Questions)\n"]

    for idx, q in enumerate(questions, 1):
        if isinstance(q, dict):
            q_text = q.get("question") or q.get("content") or f"Câu hỏi kiểm tra trường hợp {idx}"
            explanation = q.get("explanation") or q.get("answer_guide") or "Phân tích và giải thích chi tiết dựa trên nội dung bài đọc."
        else:
            q_text = str(q)
            explanation = "Phân tích và giải thích chi tiết dựa trên nội dung bài đọc."

        clean_text = q_text.strip()
        heading = f"Câu {idx}: {clean_text}"

        md_lines.append(f"### {heading}")
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
        code_snippet = """const score = 8.5;
let rank;

if (score >= 9.0) {
  rank = "Xuất sắc";
} else if (score >= 8.0) {
  rank = "Giỏi";
} else if (score >= 6.5) {
  rank = "Khá";
} else {
  rank = "Trung bình";
}

console.log(`Học lực: ${rank}`);"""
        fence_lang = "javascript"
    elif lang == "python":
        code_snippet = """score = 8.5

if score >= 9.0:
    rank = "Xuất sắc"
elif score >= 8.0:
    rank = "Giỏi"
elif score >= 6.5:
    rank = "Khá"
else:
    rank = "Trung bình"

print(f"Học lực: {rank}")"""
        fence_lang = "python"
    else:
        code_snippet = f"""# score = 8.5
# Rẽ nhánh theo các mốc: >= 9.0 -> "Xuất sắc"; >= 8.0 -> "Giỏi"; >= 6.5 -> "Khá"; else -> "Trung bình"
# In/log kết quả rank theo cú pháp chuẩn của {tech_stack}"""
        fence_lang = "text"

    code_block = f"```{fence_lang}\n{code_snippet}\n```"

    return {
        "questions": [
            {
                "id": 1,
                "question": f"Cho đoạn mã sau:\n{code_block}\nĐoạn code trên có chức năng gì? Với `score = 8.5`, chương trình sẽ thực thi qua nhánh điều kiện nào và giá trị `rank` cuối cùng là gì?",
                "explanation": "- Điều kiện `score >= 9.0` (8.5 >= 9.0) là sai.\n- Điều kiện `score >= 8.0` (8.5 >= 8.0) là đúng.\n- Gán `rank = \"Giỏi\"` và kết quả xuất ra là `Học lực: Giỏi`."
            },
            {
                "id": 2,
                "question": "Nếu sửa giá trị thành `score = 7.0`, nhánh rẽ nào sẽ được kích hoạt và kết quả `rank` thay đổi ra sao?",
                "explanation": "- Các điều kiện `>= 9.0` và `>= 8.0` đều sai.\n- Điều kiện `score >= 6.5` (7.0 >= 6.5) là đúng.\n- Gán `rank = \"Khá\"` và kết quả xuất ra là `Học lực: Khá`."
            },
            {
                "id": 3,
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

    # Ưu tiên tuyệt đối: trích xuất TRỰC TIẾP từ reading.html THẬT (state["html_content"] hoặc file
    # trên đĩa) — không dùng blueprint trung gian (master_content), vì đã xác nhận thực tế blueprint
    # có thể lệch hẳn domain/nội dung so với bài đọc đã hoàn thiện.
    full_article_context, real_code_snippets = _extract_real_reading_content(state)

    if not full_article_context:
        # Fallback CUỐI CÙNG: reading.html thật sự chưa tồn tại (chưa từng sinh lần nào) — dùng
        # blueprint trung gian như phương án dự phòng duy nhất.
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
        problem_text = content.get("problem", "") if isinstance(content, dict) else ""
        analysis_text = content.get("analysis", "") if isinstance(content, dict) else ""
        solution_text = content.get("solution", "") if isinstance(content, dict) else ""
        example_text = content.get("example", "") if isinstance(content, dict) else ""
        summary_text = content.get("summary", "") if isinstance(content, dict) else ""
        full_article_context = f"{problem_text}\n\n{analysis_text}\n\n{solution_text}\n\n{example_text}\n\n{summary_text}".strip()
        real_code_snippets = [example_text] if example_text else []

    code_snippets_block = "\n\n".join(
        f"--- Code snippet #{i} (nguyên văn từ bài đọc) ---\n{snippet}"
        for i, snippet in enumerate(real_code_snippets[:6], 1)
    ) if real_code_snippets else "Không có code snippet riêng biệt — bài học thiên lý thuyết/khái niệm."

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

    user_prompt = f"""Full Lesson Reading Article Content (trích trực tiếp từ reading.html thật):
=== LESSON READING ARTICLE CONTENT ===
{full_article_context[:7000]}

=== REAL CODE SNIPPETS EXTRACTED FROM reading.html (dùng chính xác nguyên văn các đoạn này, KHÔNG bịa code mới) ===
{code_snippets_block[:4000]}

Lesson Metadata:
- Session: {session_id}
- Lesson: {lesson_id} - {lesson_title}
- Target Tech Stack: {tech_stack}

OUTPUT JSON SCHEMA (mỗi câu hỏi PHẢI tự chứa code/dữ liệu liên quan ngay trong "question" bằng
markdown code span/block — KHÔNG có field "code_snippet" hay "title" riêng, KHÔNG dùng nhãn kiểu
"(Xung hướng...)"/"(Nghịch hướng...)" — câu hỏi phải rõ ràng, trực tiếp, đi thẳng vào trọng tâm):
{{
  "questions": [
    {{
      "id": 1,
      "question": "(Mức Thông hiểu — KHÔNG in nhãn mức độ ra output) Câu hỏi trực tiếp, trích nguyên văn 1 dòng/đoạn code THẬT từ bài đọc rồi hỏi thẳng bản chất/chức năng của nó — ví dụ: 'Trong đoạn code sau: `for i in items:` dòng lệnh này có chức năng gì?'",
      "explanation": "- Giải thích bản chất/cơ chế của dòng lệnh, bám sát đúng code thật vừa trích..."
    }},
    {{
      "id": 2,
      "question": "(Mức Vận dụng — KHÔNG in nhãn mức độ ra output) Câu hỏi thay đổi 1 giá trị cụ thể trong CHÍNH đoạn code câu 1 (ví dụ đổi biến/tham số từ A thành B) và hỏi thẳng dự đoán kết quả mới là gì — ví dụ: 'Nếu đổi giá trị của `a` từ 3 thành 4 thì kết quả in ra là gì?'",
      "explanation": "- Phân tích sự thay đổi và kết quả mới, dựa trên đúng code thật đã trích..."
    }},
    {{
      "id": 3,
      "question": "(Mức Phân tích — KHÔNG in nhãn mức độ ra output) Câu hỏi về trường hợp biên/bẫy lỗi thực tế của CHÍNH đoạn code đã trích (dữ liệu biên, sai thứ tự tham số...) — hỏi thẳng hiện tượng lỗi xảy ra và cách sửa.",
      "explanation": "- Phân tích nguyên nhân lỗi và cách khắc phục đúng chuẩn..."
    }}
  ]
}}
Lưu ý: các nhãn "(Mức ...)" trên chỉ là chú thích cho việc thiết kế nội bộ trong ví dụ này — TUYỆT ĐỐI KHÔNG chép các nhãn đó vào field "question" thật khi sinh output, "question" thật phải bắt đầu thẳng vào nội dung câu hỏi.
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
