import json
from core.state import AgentState
from core.llm import call_llm
from agents.creators.common_utils import get_lesson_content, log_agent_tokens

def format_reading_questions_to_markdown(questions: list) -> str:
    md_lines = ["# Bộ câu hỏi tự luận kiểm tra bài đọc (Reading Comprehension Essay Questions)\n"]
    for idx, q in enumerate(questions, 1):
        if isinstance(q, dict):
            q_text = q.get("question") or q.get("title") or f"Câu hỏi tự luận {idx}"
            explanation = q.get("explanation") or q.get("answer_guide") or q.get("guide") or "Phân tích và giải thích chi tiết dựa trên nội dung bài đọc."
        else:
            q_text = str(q)
            explanation = "Phân tích và giải thích chi tiết dựa trên nội dung bài đọc."
        
        md_lines.append(f"### Câu {idx}: {q_text}")
        md_lines.append(f"> **Gợi ý trả lời & Định hướng đáp án:** {explanation}\n")
        md_lines.append("---\n")
        
    return "\n".join(md_lines).strip()

def reading_questions_creator_agent(state: AgentState) -> AgentState:
    """
    Reading Questions Creator Agent:
    Trích xuất hoặc tự động sinh bộ câu hỏi kiểm tra tự đánh giá bài đọc DẠNG TỰ LUẬN (Open-ended Essay Questions)
    được format chuẩn Markdown (reading_questions.md) và lưu vào state['reading_questions_markdown'].
    """
    session_id = state.get("session_id", "Session 01")
    lesson_id = state.get("lesson_id", "")
    from core.state import require_tech_stack
    tech_stack = require_tech_stack(state, "reading_questions_creator_agent")
    
    core_ssot = state.get("core_ssot", {})
    lesson_title = core_ssot.get("session_title") or core_ssot.get("lesson_title") or "Lập trình Python Doanh Nghiệp"
    lesson_details = core_ssot.get("lesson_details", "")
    expected_output = core_ssot.get("expected_output", "")
    
    print(f"\n[Reading_Questions_Agent] Extracting/Formulating Open-ended Essay Reading Questions Markdown for {session_id} - {lesson_id}: {lesson_title}")
    
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
Your task is to generate 3 to 4 open-ended essay reading comprehension questions (Dạng tự luận) based strictly on the provided lesson reading article.

PRIMARY EVALUATION OBJECTIVE:
- This question suite is specifically designed to verify whether students have ACTUALLY READ and DEEPLY UNDERSTOOD the lesson article.

CRITICAL ANTI-AI & ANTI-SEARCH SHORTCUT RULES:
1. ABSOLUTELY FORBIDDEN to ask high-level generic textbook questions (e.g. "What is Git?", "Explain why virtual environments are important", "Present syntax of loop", "List PEP 8 rules").
2. MANDATORY DATA BINDING: EVERY question MUST extract and reference specific concrete data from the provided reading text: exact enterprise scenarios, variable/file names (e.g., `stock_inbound.csv`, `db_credentials.env`), specific CLI commands/parameters, error output messages, step sequences, or Gotcha traps presented in the text.
3. Anti-AI Guarantee: External search engines (Google) or generic AI queries MUST NOT be able to answer the question without analyzing the exact scenario details given only in the provided reading text.
4. Format: Open-ended Essay (Dạng Tự Luận). NO multiple-choice options (NO A/B/C/D options).
5. Output Language: 100% Accented Vietnamese (Tiếng Việt có dấu chuẩn sản xuất). No text emojis, no ALL CAPS.
6. Return ONLY a valid JSON array of essay question objects.
"""

    user_prompt = f"""Full Lesson Reading Article Text (Extract specific scenario variables, file names, code lines, gotchas, and execution steps from this text to formulate data-bound questions):

=== LESSON READING ARTICLE CONTENT ===
{full_article_context[:7000]}

Lesson Metadata:
- Session: {session_id}
- Lesson: {lesson_id} - {lesson_title}
- Target Tech Stack: {tech_stack}

OUTPUT JSON SCHEMAS (Array of 3-4 objects):
[
  {{
    "id": 1,
    "question": "Câu hỏi tự luận phân tích bối cảnh/dữ liệu cụ thể từ Phần 1 (trích dẫn tên file/biến/tình huống cụ thể từ bài đọc)...",
    "explanation": "Gợi ý trả lời & định hướng đáp án chi tiết dựa trên dữ liệu bài đọc..."
  }},
  {{
    "id": 2,
    "question": "Câu hỏi tự luận phân tích luồng vận hành/thao tác cụ thể từ Phần 2 (trích dẫn cơ chế/bảng tham số cụ thể)...",
    "explanation": "Gợi ý trả lời & định hướng đáp án chi tiết..."
  }},
  {{
    "id": 3,
    "question": "Câu hỏi tự luận trích dẫn kịch bản lệnh/mã nguồn ở Phần 3, yêu cầu chỉ ra dòng lỗi hoặc kết quả thực thi cụ thể...",
    "explanation": "Gợi ý trả lời & định hướng đáp án chi tiết..."
  }},
  {{
    "id": 4,
    "question": "Câu hỏi tự luận phân tích bẫy lỗi Gotcha từ Phần 4 và nêu biện pháp khắc phục chuẩn...",
    "explanation": "Gợi ý trả lời & định hướng đáp án chi tiết..."
  }}
]
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
        essay_questions = json.loads(response_str)
        if isinstance(essay_questions, dict) and "questions" in essay_questions:
            essay_questions = essay_questions["questions"]
    except Exception:
        essay_questions = [
            {
                "id": 1,
                "question": f"Trong kịch bản khởi tạo và quản lý kho lưu trữ ở bài đọc môn {tech_stack}, hãy phân tích hậu quả xảy ra khi lập trình viên thực thi lệnh mà quên sử dụng cờ `--global` và nêu cách kiểm tra lại file cấu hình.",
                "explanation": f"Khi không có cờ `--global`, cấu hình chỉ áp dụng cho local repository hiện tại. Cần kiểm tra lại bằng lệnh `{tech_stack} config --list` hoặc xem file `.git/config` để xác nhận phạm vi."
            },
            {
                "id": 2,
                "question": f"Phân tích lý do tại sao việc sử dụng lệnh gom toàn bộ tệp vào Staging Area mà không kiểm tra trạng thái lại vô tình đưa cả các tệp nhạy cảm (như `.env` hoặc tệp nhật ký tạm) vào mốc snapshot và đề xuất giải pháp cách ly.",
                "explanation": "Việc gom toàn bộ tệp không kiểm tra dễ đưa các tệp chứa thông tin bảo mật vào kho lưu trữ. Giải pháp là thiết lập tệp cấu hình loại trừ `.gitignore` và rà soát kỹ bằng lệnh kiểm tra trạng thái trước khi commit."
            },
            {
                "id": 3,
                "question": f"Trích dẫn kịch bản thực thi bị lỗi trong bài đọc, hãy chỉ ra điểm không an toàn khi sử dụng giao thức HTTP cho địa chỉ Remote và viết lại câu lệnh chuyển sang giao thức HTTPS/SSH chuẩn.",
                "explanation": "Giao thức HTTP không mã hóa dữ liệu truyền tải trên đường truyền. Cần đổi sang giao thức HTTPS hoặc SSH bằng câu lệnh cập nhật URL remote chuẩn doanh nghiệp."
            }
        ]

    rq_md = format_reading_questions_to_markdown(essay_questions)
    state["reading_questions_json"] = essay_questions
    state["reading_questions_markdown"] = rq_md
    log_agent_tokens("Reading_Questions_Agent", state, rq_md)
    return state
