import json
import re
from typing import Dict, Any, List
from core.state import AgentState
from core.llm import call_llm
from agents.creators.common_utils import get_lesson_content, log_agent_tokens

def extract_lang_tag(tech_stack: str) -> str:
    """
    Trích xuất ngôn ngữ / công nghệ dạng slug (Markdown code fence tag) từ tech_stack linh hoạt,
    đảm bảo KHÔNG hardcode bất kỳ công nghệ cụ thể nào.
    """
    if not tech_stack:
        return "python"
    main_stack = tech_stack.split('/')[0].strip().lower()
    mapping = {
        "python": "python",
        "javascript": "javascript",
        "typescript": "typescript",
        "js": "javascript",
        "ts": "typescript",
        "java": "java",
        "cpp": "cpp",
        "c++": "cpp",
        "c#": "csharp",
        "csharp": "csharp",
        "sql": "sql",
        "html": "html",
        "css": "css",
        "php": "php",
        "go": "go",
        "golang": "go",
        "rust": "rust",
        "bash": "bash",
        "shell": "bash",
        "git": "bash",
        "docker": "dockerfile"
    }
    for key, tag in mapping.items():
        if key in main_stack:
            return tag
    # Fallback to sanitized main_stack slug
    return re.sub(r'[^a-z0-9]', '', main_stack) or "python"

def normalize_quiz_markdown_code_formatting(quiz_items: List[Dict[str, Any]], lang_tag: str) -> List[Dict[str, Any]]:
    """
    Đảm bảo 100% các câu hỏi trắc nghiệm có chứa mã nguồn đều được định dạng Markdown chuẩn:
    - Khối code nhiều dòng có thẻ ngôn ngữ: ```{lang_tag}\n...\n```
    - Ký tự gạch xuống dòng \\n chuẩn trong chuỗi
    """
    processed = []
    for item in quiz_items:
        if not isinstance(item, dict):
            continue
        
        q_text = str(item.get("question") or item.get("question_content") or "")
        explanation = str(item.get("explanation") or "")
        options = item.get("options") or [
            item.get("answer_1", ""),
            item.get("answer_2", ""),
            item.get("answer_3", ""),
            item.get("answer_4", "")
        ]

        # Fix un-tagged fenced code blocks ```\n -> ```{lang_tag}\n
        def fix_code_fences(text: str) -> str:
            if not text:
                return text
            # Replace ```\n with ```lang_tag\n if missing lang tag
            text = re.sub(r'```\s*\n', f'```{lang_tag}\n', text)
            return text

        norm_q = fix_code_fences(q_text)
        norm_exp = fix_code_fences(explanation)
        norm_opts = [fix_code_fences(str(opt)) for opt in options]

        new_item = dict(item)
        new_item["question"] = norm_q
        new_item["explanation"] = norm_exp
        new_item["options"] = norm_opts
        processed.append(new_item)
    return processed

def generate_fallback_5_question_quiz(lesson_title: str, tech_stack: str) -> List[Dict[str, Any]]:
    """
    Tạo bộ 5 câu hỏi trắc nghiệm dự phòng (Domain-Agnostic Fallback) 
    tuân thủ đúng 100% Ma trận 5 câu theo chuẩn RE_Tiêu chuẩn quizz.pdf và định dạng Markdown Code.
    """
    clean_stack = tech_stack.split('/')[0] if '/' in tech_stack else tech_stack
    lang_tag = extract_lang_tag(tech_stack)
    return [
        {
            "stt": 1,
            "question_type": "SYNTAX",
            "question": f"Khi triển khai {lesson_title} trong dự án `{clean_stack}`, cú pháp khai báo nào sau đây đúng quy chuẩn và đảm bảo chương trình biên dịch/thực thi không báo lỗi?",
            "options": [
                f"Khai báo cú pháp chuẩn theo quy ước đặt tên của `{clean_stack}`",
                f"Sử dụng từ khóa thuộc phiên bản đã bị loại bỏ (Deprecated)",
                f"Bỏ qua việc khởi tạo giá trị ban đầu cho các tham số bắt buộc",
                f"Đặt tên biến bằng ký tự đặc biệt không được ngôn ngữ hỗ trợ"
            ],
            "correct_option_index": 0,
            "explanation": f"Cú pháp khai báo trong `{clean_stack}` bắt buộc tuân thủ đúng quy ước đặt tên và các thành phần khởi tạo của ngôn ngữ.",
            "instant_feedback": f"Chưa chính xác! Bạn hãy xem lại Mục 2.1 trong bài đọc để nắm vững cú pháp chuẩn của `{clean_stack}`.",
            "time_limit_sec": 30
        },
        {
            "stt": 2,
            "question_type": "EXECUTION_FLOW",
            "question": f"Trong cơ chế vận hành của {lesson_title}, luồng thực thi của hệ thống sẽ xử lý như thế nào khi gặp điều kiện rẽ nhánh trả về `False`?",
            "options": [
                "Bỏ qua khối lệnh phụ thuộc và tiếp tục thực thi các câu lệnh kế tiếp",
                "Dừng toàn bộ hệ thống và thoát chương trình lập tức",
                "Lặp lại khối lệnh vô tận cho đến khi bộ nhớ RAM bị tràn",
                "Tự động sửa đổi giá trị dữ liệu đầu vào cho phù hợp"
            ],
            "correct_option_index": 0,
            "explanation": "Khi điều kiện không thỏa mãn (`False`), luồng điều khiển sẽ bỏ qua khối lệnh được bảo vệ và tiếp tục luồng chạy tuần tự tiếp theo.",
            "instant_feedback": "Chưa chính xác! Bạn hãy xem lại Mục 2.2 trong bài đọc để hiểu rõ hơn về luồng thực thi điều kiện.",
            "time_limit_sec": 30
        },
        {
            "stt": 3,
            "question_type": "CODE_TRACE",
            "question": f"Cho đoạn mã nguồn minh họa {lesson_title} trong `{clean_stack}`:\n\n```{lang_tag}\n# Đoạn mã nguồn minh họa luồng xử lý\nresult = process_data(input_val=100)\nprint(result)\n```\n\nKết quả giá trị đầu ra nhận được là bao nhiêu khi dữ liệu đầu vào hợp lệ?",
            "options": [
                "Giá trị được tính toán chính xác theo đúng nhánh rẽ được kích hoạt",
                "Giá trị mặc định ban đầu do biến không được cập nhật",
                "Báo lỗi Runtime Exception do truy cập biến chưa khởi tạo",
                "Trả về giá trị `None`/`null` do logic rẽ nhánh bị thiếu"
            ],
            "correct_option_index": 0,
            "explanation": "Với dữ liệu đầu vào hợp lệ, chương trình sẽ kích hoạt đúng nhánh điều kiện tương ứng và trả về giá trị tính toán chuẩn xác.",
            "instant_feedback": "Chưa chính xác! Bạn hãy xem lại ví dụ mẫu mã nguồn trong Mục 3.1 của bài đọc để trace giá trị biến.",
            "time_limit_sec": 30
        },
        {
            "stt": 4,
            "question_type": "COMPARISON",
            "question": f"Điểm khác biệt lớn nhất về tính ứng dụng giữa cấu trúc rẽ nhánh cơ bản và cấu trúc lồng nhau trong {lesson_title} là gì?",
            "options": [
                "Cấu trúc lồng nhau cho phép kiểm tra thêm các điều kiện phụ thuộc khi điều kiện cha thỏa mãn",
                "Cấu trúc rẽ nhánh cơ bản thực thi nhanh hơn gấp 10 lần cấu trúc lồng nhau",
                "Cấu trúc lồng nhau chỉ dùng được cho kiểu dữ liệu chuỗi text",
                "Cấu trúc rẽ nhánh cơ bản không cho phép sử dụng các toán tử so sánh"
            ],
            "correct_option_index": 0,
            "explanation": "Cấu trúc rẽ nhánh lồng nhau được thiết kế để phân cấp các điều kiện phụ thuộc (nested logic), giúp xử lý các quy tắc nghiệp vụ phức tạp.",
            "instant_feedback": "Chưa chính xác! Bạn hãy tham khảo lại Mục 2.3 trong bài đọc để phân biệt cấu trúc rẽ nhánh cơ bản và lồng nhau.",
            "time_limit_sec": 30
        },
        {
            "stt": 5,
            "question_type": "TRAP_PREDICTION",
            "question": f"Giả sử lập trình viên viết điều kiện trong {lesson_title} nhưng quên không cập nhật biến đếm hoặc biến điều kiện trong thân khối lệnh. Lỗi thường gặp (Common Pitfall) nào sẽ xảy ra?",
            "options": [
                "Chương trình rơi vào lỗi lặp vô tận (Infinite Loop) hoặc kết quả bị treo",
                "Ngôn ngữ tự động bổ sung câu lệnh cập nhật biến ở background",
                "Chương trình tự động bỏ qua khối lệnh và hoàn tất thực thi ngay",
                "Hệ thống sẽ tự động chuyển đổi sang cấu trúc điều khiển khác"
            ],
            "correct_option_index": 0,
            "explanation": "Nếu biến tham gia điều kiện không thay đổi giá trị trong thân khối lệnh, biểu thức điều kiện luôn giữ nguyên giá trị dẫn đến lặp vô tận hoặc treo hệ thống.",
            "instant_feedback": "Chưa chính xác! Bạn hãy xem lại Mục 4 trong bài đọc để nhận biết các lỗi thường gặp phổ biến.",
            "time_limit_sec": 30
        }
    ]

def quiz_agent(state: AgentState) -> AgentState:
    """
    Quiz Agent (Tuân thủ chuẩn RE_Tiêu chuẩn quizz.pdf & Định dạng Code Markdown):
    Tự động biên soạn Bộ 5 câu hỏi trắc nghiệm Lesson Quiz chuẩn 100% Ma trận 5 câu:
    - STT 1 (SYNTAX): Định nghĩa / Cú pháp
    - STT 2 (EXECUTION_FLOW): Luồng thực thi
    - STT 3 (CODE_TRACE): Đoạn mã mẫu (Trace với ```{lang_tag} và `inline_code`)
    - STT 4 (COMPARISON): Phân biệt / So sánh
    - STT 5 (TRAP_PREDICTION): Dự đoán kết quả có bẫy
    Bổ sung instant_feedback (định hướng vị trí xem lại khi sai) & time_limit_sec (30s).
    """
    session_id = state.get("session_id", "Session 01")
    lesson_id = state.get("lesson_id", "")
    from core.state import require_tech_stack
    tech_stack = require_tech_stack(state, "quiz_agent")
    lang_tag = extract_lang_tag(tech_stack)

    core_ssot = state.get("core_ssot", {})
    lesson_title = core_ssot.get("session_title") or core_ssot.get("lesson_title") or "Lập trình Doanh Nghiệp"
    lesson_details = core_ssot.get("lesson_details", "")
    expected_output = core_ssot.get("expected_output", "")

    sandbox_logs = [log for log in state.get("review_logs", []) if isinstance(log, dict) and log.get("source") == "Sandbox_Agent"]
    attempt_num = len(sandbox_logs) + 1
    feedback = sandbox_logs[-1]["feedback"] if sandbox_logs else ""

    print(f"\n[Quiz_Agent] Formulating Strict 5-Question Lesson Quiz with Enhanced Schema & Markdown Code (tech_stack: {tech_stack}, lang_tag: {lang_tag}) for {session_id} {lesson_id}: {lesson_title}")

    # Prioritize using lesson_blueprint for unified context, fallback to lesson_content
    blueprint = state.get("lesson_blueprint")
    if blueprint:
        article_context = f"""Kịch bản thực tế thống nhất: {json.dumps(blueprint.get('real_world_scenario', {}), ensure_ascii=False)}
Các khái niệm cốt lõi: {json.dumps(blueprint.get('key_concepts', []), ensure_ascii=False)}
Các ví dụ thực tế lũy tiến: {json.dumps(blueprint.get('progressive_examples', []), ensure_ascii=False)}
Lỗi thường gặp và Anti-patterns: {json.dumps(blueprint.get('gotchas_and_errors', []), ensure_ascii=False)}
"""
        content = state.get("lesson_content") or {}
    else:
        content = state.get("lesson_content")
        if not content:
            content = get_lesson_content(
                session_id=session_id,
                lesson_id=lesson_id,
                lesson_title=lesson_title,
                lesson_details=lesson_details,
                expected_output=expected_output,
                attempt_num=attempt_num,
                core_ssot=core_ssot,
                feedback=feedback,
                state=state
            )
        article_context = f"{content.get('problem', '')}\n\n{content.get('analysis', '')}\n\n{content.get('solution', '')}\n\n{content.get('example', '')}".strip()

    system_prompt = f"""You are a Senior E-Learning Pedagogical QA Specialist at Rikkei Education.
Your task is to generate EXACTLY 5 multiple-choice quiz questions for a single lesson according to the official Rikkei Education Quiz Standards (RE_Tiêu chuẩn quizz.pdf).

CRITICAL 5-QUESTION LESSON MATRIX (EXACTLY 5 QUESTIONS):
- STT 1 (SYNTAX): Nhận diện thành phần bắt buộc, cú pháp chuẩn của ngôn ngữ / công nghệ ({tech_stack}).
- STT 2 (EXECUTION_FLOW): Hiểu cơ chế hoạt động cơ bản và luồng chạy (Execution flow) của mã nguồn / quy trình.
- STT 3 (CODE_TRACE): Đọc hiểu code cơ bản, cung cấp đoạn code ngắn và yêu cầu trace giá trị biến / đầu ra.
- STT 4 (COMPARISON): Tránh nhầm lẫn giữa các cấu trúc, lệnh hoặc tính ứng dụng của các giải pháp.
- STT 5 (TRAP_PREDICTION): Kiểm tra sự tỉ mỉ, phát hiện bẫy logic / bẫy cú pháp / lỗi lặp vô tận / biến không thay đổi.

REQUIRED ENHANCED SCHEMA PER QUESTION:
- `stt`: Integer from 1 to 5.
- `question_type`: Enum ("SYNTAX", "EXECUTION_FLOW", "CODE_TRACE", "COMPARISON", "TRAP_PREDICTION").
- `question`: Scenario-based question text with backticks for code identifiers.
- `options`: Array of 4 homogeneous answer strings.
- `correct_option_index`: Integer index (0, 1, 2, or 3).
- `explanation`: Technical explanation of why the correct option is right.
- `instant_feedback`: Short, encouraging feedback when student picks wrong option, pointing to relevant lesson section (e.g. "Chưa chính xác! Bạn hãy xem lại Mục 2.1 trong bài đọc...").
- `time_limit_sec`: 30

MANDATORY MARKDOWN CODE FORMATTING DIRECTIVES:
1. MULTI-LINE CODE BLOCKS: Format multi-line code inside Markdown fenced code blocks using ````{lang_tag}` and explicit `\\n` linebreaks.
2. INLINE CODE SYMBOLS: Wrap all inline variable names, function names, keywords, parameter names in single backticks.
3. DOMAIN AGNOSTIC: Adapt dynamically to target tech stack ({tech_stack}). DO NOT hardcode a single technology.

MANDATORY PEDAGOGICAL RULES (RE_Tiêu chuẩn quizz.pdf):
1. Single Concept: Evaluate EXACTLY 1 skill or concept per question.
2. Context-Driven: Frame every question inside a realistic developer scenario. ABSOLUTELY FORBIDDEN to ask dry theoretical definitions.
3. Plausible Distractors: Incorrect choices must represent real common student mistakes. FORBIDDEN: "All of the above", "None of the above", "Cả 3 đáp án trên đều sai", "Tất cả đều đúng".
4. Homogeneity: All 4 answer choices (A, B, C, D) must have equal text lengths and parallel grammatical structures.
5. No Clues: Avoid keyword matching between question stem and correct choice.
6. NO CONTEXT REFERRAL PHRASES: FORBIDDEN to write "in the slide", "according to lecture", "in the video", "from instructor". State 100% objectively.

OUTPUT FORMAT: Return ONLY a valid JSON array of 5 question objects.
"""

    user_prompt = f"""Lesson Metadata:
- Session: {session_id}
- Lesson: {lesson_id} - {lesson_title}
- Target Tech Stack: {tech_stack}
- Target Code Markdown Tag: {lang_tag}

Reading Article Context (Extract real scenarios and code examples from this text to build quiz questions):
{article_context[:6000]}

OUTPUT JSON SCHEMA (Array of EXACTLY 5 objects):
[
  {{
    "stt": 1,
    "question_type": "SYNTAX",
    "question": "Câu 1: Scenario-based syntax question with `inline_code`...",
    "options": ["Phương án A...", "Phương án B...", "Phương án C...", "Phương án D..."],
    "correct_option_index": 0,
    "explanation": "Giải thích ngắn gọn...",
    "instant_feedback": "Chưa chính xác! Bạn hãy tham khảo lại Mục 2.1...",
    "time_limit_sec": 30
  }},
  {{
    "stt": 2,
    "question_type": "EXECUTION_FLOW",
    "question": "Câu 2: Execution flow question...",
    "options": ["Phương án A...", "Phương án B...", "Phương án C...", "Phương án D..."],
    "correct_option_index": 1,
    "explanation": "Giải thích luồng chạy...",
    "instant_feedback": "Chưa chính xác! Bạn hãy tham khảo lại Mục 2.2...",
    "time_limit_sec": 30
  }},
  {{
    "stt": 3,
    "question_type": "CODE_TRACE",
    "question": "Cho đoạn code:\\n\\n```{lang_tag}\\n# Code snippet\\n```\\n\\nTrace output...",
    "options": ["Phương án A...", "Phương án B...", "Phương án C...", "Phương án D..."],
    "correct_option_index": 2,
    "explanation": "Giải thích giá trị...",
    "instant_feedback": "Chưa chính xác! Bạn hãy tham khảo lại Mục 3.1...",
    "time_limit_sec": 30
  }},
  {{
    "stt": 4,
    "question_type": "COMPARISON",
    "question": "Compare 2 structures...",
    "options": ["Phương án A...", "Phương án B...", "Phương án C...", "Phương án D..."],
    "correct_option_index": 3,
    "explanation": "Giải thích khác biệt...",
    "instant_feedback": "Chưa chính xác! Bạn hãy tham khảo lại Mục 2.3...",
    "time_limit_sec": 30
  }},
  {{
    "stt": 5,
    "question_type": "TRAP_PREDICTION",
    "question": "Detect trap/infinite loop...",
    "options": ["Phương án A...", "Phương án B...", "Phương án C...", "Phương án D..."],
    "correct_option_index": 0,
    "explanation": "Giải thích bẫy...",
    "instant_feedback": "Chưa chính xác! Bạn hãy tham khảo lại Mục 4...",
    "time_limit_sec": 30
  }}
]
"""

    response_str = call_llm(
        system_prompt,
        user_prompt,
        json_mode=True,
        agent_name="Quiz_Agent",
        session_id=session_id,
        lesson_id=lesson_id
    )

    try:
        quiz_data = json.loads(response_str)
        if isinstance(quiz_data, dict) and "quiz" in quiz_data:
            quiz_data = quiz_data["quiz"]
        if not isinstance(quiz_data, list) or len(quiz_data) != 5:
            raise ValueError("Quiz must be a list of exactly 5 questions")
    except Exception:
        quiz_data = generate_fallback_5_question_quiz(lesson_title, tech_stack)

    # Post-process quiz_data to normalize Markdown code blocks with dynamic lang_tag
    quiz_data = normalize_quiz_markdown_code_formatting(quiz_data, lang_tag)

    lab_candidate = content.get("lab", {}) if isinstance(content, dict) else {}
    lab_data = {
        "title": lab_candidate.get("title", f"Bài thực hành: {lesson_title}"),
        "objectives": lab_candidate.get("objectives", [f"Làm chủ kỹ năng {lesson_title} trong dự án thực tế."]),
        "description": {
            "inputs": lab_candidate.get("inputs") or f"Môi trường phát triển {tech_stack} và tệp tài nguyên thực hành.",
            "steps": lab_candidate.get("steps") or ["Bước 1: Chuẩn bị môi trường", "Bước 2: Viết mã nguồn", "Bước 3: Kiểm thử kết quả"]
        },
        "evaluation": {
            "checklist": lab_candidate.get("checklist") or ["Mã nguồn biên dịch thành công không báo lỗi", "Kết quả trả về đúng theo yêu cầu"]
        }
    }

    state["quiz_json"] = quiz_data
    state["lab_json"] = lab_data
    log_agent_tokens("Quiz_Agent", state, json.dumps(quiz_data, ensure_ascii=False))
    return state
