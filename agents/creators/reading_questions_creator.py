import json
from core.state import AgentState
from core.llm import call_llm
from agents.creators.common_utils import get_lesson_content, log_agent_tokens

def format_reading_questions_to_markdown(data, tech_stack: str = "python") -> str:
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
        lang = tech_stack.lower() if tech_stack else "python"
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

        # Avoid repeating title prefix if already in question text
        clean_text = q_text.strip()
        if clean_text.startswith(q_title):
            full_heading = clean_text
        else:
            full_heading = f"{q_title} {clean_text}".strip()

        md_lines.append(f"### {full_heading}")
        
        # Format multi-line explanation nicely
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
    from core.state import require_tech_stack
    tech_stack = require_tech_stack(state, "reading_questions_creator_agent")

    core_ssot = state.get("core_ssot", {})
    lesson_title = core_ssot.get("session_title") or core_ssot.get("lesson_title") or "Lập trình Python Doanh Nghiệp"
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

    system_prompt = f"""You are a Senior E-Learning Pedagogical QA Specialist at Rikkei Education.
Your task is to generate a multi-case reading comprehension question set (Bộ câu hỏi kiểm tra bài đọc theo ví dụ thực tế) anchored strictly on 1 code snippet / scenario extracted from the provided lesson reading article.

CRITICAL DIRECTIVES & MULTI-CASE CODE TRACING CONTRACT:
1. NO HIGH-LEVEL ABSTRACT TEXTBOOK QUESTIONS: Absolutely forbidden to ask generic theoretical essay questions like "Explain why loops are used" or "List PEP 8 rules".
2. SINGLE ANCHORED CODE SNIPPET / SCENARIO: Extract 1 concrete code snippet or CLI/config scenario card directly from the provided reading text (Section 2 or Section 3).
3. 4-CASE EVALUATION STRUCTURE (Chia thành 4 trường hợp thử nghiệm):
   - Case 1 (Xung hướng - Forward Tracing Input X1): Provide specific input X1 -> Ask student which lines/branches execute and what output/variable value is produced.
   - Case 2 (Xung hướng - Alternative Input Tracing Input X2): Provide alternative input X2 -> Ask student how execution flow and output change.
   - Case 3 (Nghịch hướng - Reverse Deduction Target Output Y3): Provide target output Y3 -> Ask student what input value / condition range is required.
   - Case 4 (Trường hợp biên / Bẫy lỗi Gotcha): Provide boundary/invalid input or code mutation (wrong condition order / operator trap) -> Ask student to analyze the logic bug, unreachable code, or error output and state the fix.
4. DOMAIN AGNOSTIC: Works for all tech stacks ({tech_stack}). DO NOT hardcode Git or unrelated topics unless the lesson is specifically about Git.
5. LANGUAGE: 100% Accented Vietnamese (Tiếng Việt có dấu chuẩn sản xuất). No text emojis, no ALL CAPS.
6. OUTPUT FORMAT: Return strictly a valid JSON object matching the requested schema.
"""

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

    try:
        data = json.loads(response_str)
        if isinstance(data, list):
            reading_data = {"code_snippet": "", "questions": data}
        elif isinstance(data, dict):
            reading_data = data
        else:
            raise ValueError("Invalid JSON output format")
    except Exception:
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
