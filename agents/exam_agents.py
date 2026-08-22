# agents/exam_agents.py
"""
Midterm / Final Exam Generator & Reviewer.
Reuses the exact same Systemic Course Architecture Governance Engine
(core/course_architecture.py) that already powers Mini Project generation, so the practical exam
format automatically adapts to the course's real nature (CLI_CORE -> terminal menu app,
WEB_BACKEND -> REST API endpoints, WEB_FRONTEND -> UI build, etc.) instead of being hardcoded per
course. See skills/exam_generator/SKILL.md for the full design standard.
"""
import json
import re
from typing import Dict, Any, List, Optional
from pathlib import Path

from core.llm import call_llm
from core.course_architecture import resolve_course_architecture, lint_document_architecture
from core.utils.llm_parser import extract_json_from_response
from agents.project_agents import (
    _build_domain_prompt_block,
    parse_xml_robust,
    sanitize_vietnamese_filename,
    generate_and_link_srs_diagram,
)


def _exam_label(is_final: bool) -> str:
    return "Thi Cuối Môn" if is_final else "Thi Giữa Môn"


def _mcq_quota(is_final: bool) -> int:
    return 30 if is_final else 20


def _oral_quota_range(is_final: bool) -> str:
    return "8 đến 10" if is_final else "6 đến 8"


def exam_practical_creator(
    session_id: str, session_title: str, tech_stack: str, curriculum_context_title: str,
    is_final: bool, previous_lessons_text: str = "", forbidden_scope: str = "",
    allowed_scope: str = "", chosen_domain: str = ""
) -> Dict[str, Any]:
    """Generates the Đề thi thực hành (Practical Exam) — format adapts to the resolved
    course architecture pattern (CLI menu app / REST API / UI build / etc.)."""
    print(f"    -> [Exam Creator] Generating Đề thi thực hành ({_exam_label(is_final)}) for '{session_title}'...")

    arch_info = resolve_course_architecture(curriculum_context_title, tech_stack, forbidden_scope, allowed_scope)
    naming_convention = arch_info["naming_guidelines"]
    error_model = arch_info["error_model"]
    domain_prompt_block = _build_domain_prompt_block(session_id, session_title, chosen_domain)

    n_features = "6 đến 10" if is_final else "4 đến 6"
    duration = "120 đến 180 phút" if is_final else "90 đến 120 phút"

    scope_rules = ""
    if forbidden_scope:
        scope_rules += f"\nPHẠM VI CẤM DÙNG (FORBIDDEN SCOPE): {forbidden_scope}.\nTUYỆT ĐỐI CẤM RA ĐỀ YÊU CẦU HOẶC GỢI Ý SỬ DỤNG CÁC KIẾN THỨC BỊ CẤM NÀY.\n"
    if allowed_scope:
        scope_rules += f"\nPHẠM VI ĐÃ HỌC (ALLOWED SCOPE — TOÀN BỘ kiến thức được phép sử dụng, TÍCH LŨY từ đầu môn tới thời điểm thi): {allowed_scope}.\n"
    if previous_lessons_text:
        scope_rules += f"\nDANH SÁCH BÀI HỌC ĐÃ HỌC TRƯỚC ĐÓ:\n{previous_lessons_text}\n"

    system_prompt = f"""You are a Senior Technical Examiner and Curriculum Architect at Rikkei Education, authoring
a formal {_exam_label(is_final)} PRACTICAL EXAM for:
Session: {session_id} - {session_title}
Technology Stack: {tech_stack}
Designated Architecture Model: {arch_info["arch_name"]}
{domain_prompt_block}
{scope_rules}

{naming_convention}

{error_model}

MANDATORY EXAM DESIGN DIRECTIVES:
0. STRICT PROGRESSIVE KNOWLEDGE BOUNDARY (NO FUTURE TOPIC LEAKAGE):
   - The exam MUST ONLY require knowledge, syntax, runtime environments, and concepts explicitly
     listed in Allowed Scope above. ABSOLUTELY FORBIDDEN to require or hint at anything in
     Forbidden Scope, even as an "advanced/optional" bonus task.
1. Architecture-Faithful Deliverable Shape:
   - The exam's deliverable format MUST match '{arch_info["arch_name"]}' exactly. If CLI_CORE:
     the exam is a menu-driven terminal application (numbered menu loop reading user input,
     dispatching to functions, console-only I/O). If WEB_BACKEND: the exam is a set of REST API
     endpoints with request/response schemas and HTTP status codes. If WEB_FRONTEND: the exam is
     a UI screen/component build with layout, form validation and inline error states. Never mix
     deliverable shapes from a different architecture pattern.
2. Single Unified Business Domain: the exam's scenario is one concrete module of the unified
   session domain above — not a generic disconnected toy problem.
3. Progressive Difficulty Within The Spec Table: order the {n_features} required
   functions/endpoints/screen-elements from simplest (data setup / basic CRUD) to most complex
   (validation, aggregation, edge-case handling), so students can build incrementally under time
   pressure.
4. Time-Boxed Scope: the total workload MUST be realistically completable within {duration} by a
   student who has genuinely mastered the Allowed Scope — do not over-scope.
5. Professional Academic Tone: FORBIDDEN informal words, AI/assistant mentions, or student-ability
   tiering labels.
6. 100% Full-Width HTML Specification Table under section 2:
   `<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">`
   Column 1: Function/Endpoint/Screen-element name (Bold Vietnamese + English identifier in `<code>`).
   Column 2: Input / Parameters. Column 3: Processing Logic & Rules. Column 4: Output / Expected Result.
7. Mandatory Document Structure:
   - Title: `## <center>[{_exam_label(is_final)}] — [Tên nghiệp vụ] ([English Name])</center>`
   - `### **1. Mục tiêu bài thi**`
   - `### **2. Đề bài và Yêu cầu**` (contains the 100%-width spec table)
   - `### **3. Ràng buộc kỹ thuật**` (restate the allowed/forbidden knowledge boundary in plain language)
   - `### **4. Tiêu chí chấm điểm**` (100-point rubric, 5 groups + bonus, embedded inline)
   - `### **5. Yêu cầu nộp bài**`

MANDATORY OUTPUT FORMAT — SINGLE VALID XML BLOCK ENCLOSED IN <practical_exam>...</practical_exam>:
<practical_exam>
  <title>Exam Title in Accented Vietnamese</title>
  <content><![CDATA[
Full Markdown exam content here, including the embedded 100-point rubric under section 4...
  ]]></content>
</practical_exam>
"""
    user_prompt = f"Author the {_exam_label(is_final)} practical exam for {session_id} ({session_title}), technology stack {tech_stack}, strictly within Allowed Scope."

    data = None
    for attempt in range(3):
        try:
            response = call_llm(system_prompt, user_prompt, json_mode=False, agent_name="Exam Practical Creator", session_id=session_id)
            if not response:
                continue
            parsed = parse_xml_robust(response, ["title", "content"])
            if parsed.get("title") and parsed.get("content"):
                data = {"title": parsed["title"], "content": parsed["content"]}
                break
        except Exception as e:
            print(f"      [Warning] Attempt {attempt+1} failed to parse Practical Exam XML: {e}")

    if not data:
        raise ValueError(f"Không thể sinh được Đề thi thực hành cho session {session_id} sau 3 lần thử.")
    return data


def exam_mcq_creator(
    session_id: str, session_title: str, tech_stack: str, curriculum_context_title: str,
    is_final: bool, forbidden_scope: str = "", allowed_scope: str = "", chosen_domain: str = ""
) -> List[Dict[str, Any]]:
    """Generates the Đề thi trắc nghiệm (MCQ Exam) -- same JSON schema as the lesson quiz_agent
    so downstream tooling (Excel export) is reusable without modification."""
    quota = _mcq_quota(is_final)
    print(f"    -> [Exam Creator] Generating Đề thi trắc nghiệm ({quota} questions, {_exam_label(is_final)}) for '{session_title}'...")

    domain_prompt_block = _build_domain_prompt_block(session_id, session_title, chosen_domain)
    arch_info = resolve_course_architecture(curriculum_context_title, tech_stack, forbidden_scope, allowed_scope)

    system_prompt = f"""You are a Senior Technical Examiner at Rikkei Education, authoring a {quota}-question
{_exam_label(is_final)} MULTIPLE-CHOICE EXAM for:
Session: {session_id} - {session_title}
Technology Stack: {tech_stack}
Architecture Model: {arch_info["arch_name"]}
{domain_prompt_block}

Allowed Knowledge Scope (cumulative, TOÀN BỘ nội dung được phép ra đề): {allowed_scope or 'Fundamentals up to this exam'}
Forbidden Knowledge Scope (STRICTLY PROHIBITED): {forbidden_scope or 'None remaining'}

MANDATORY DIRECTIVES:
1. EXACTLY {quota} questions, distributed EVENLY across ALL topics in Allowed Scope -- never
   concentrate questions on only the most recent 1-2 sessions.
2. Distribute roughly evenly across 5 question_type categories: SYNTAX, EXECUTION_FLOW, CODE_TRACE,
   COMPARISON, TRAP_PREDICTION.
3. ZERO forbidden-scope leakage -- every question, option, and explanation stays within Allowed Scope.
4. No duplicate questions (same concept + same code snippet tested twice).
5. 100% Accented Vietnamese. Code snippets use Markdown fences with a language tag.
6. Return ONLY a raw JSON array of EXACTLY {quota} objects, no prose, no markdown fence wrapper.

SCHEMA (each array item):
{{
  "stt": 1,
  "question_type": "SYNTAX | EXECUTION_FLOW | CODE_TRACE | COMPARISON | TRAP_PREDICTION",
  "question": "Câu hỏi tiếng Việt...",
  "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
  "correct_option_index": 0,
  "explanation": "Giải thích đáp án đúng...",
  "instant_feedback": "Gợi ý ôn lại phần kiến thức liên quan nếu chọn sai...",
  "time_limit_sec": 45
}}
"""
    user_prompt = f"Author {quota} MCQ questions for the {_exam_label(is_final)} exam of {session_id} ({session_title}), tech stack {tech_stack}."

    questions = None
    for attempt in range(3):
        try:
            response = call_llm(system_prompt, user_prompt, json_mode=True, agent_name="Exam MCQ Creator", session_id=session_id)
            if not response:
                continue
            data = extract_json_from_response(response)
            if isinstance(data, dict) and "questions" in data:
                data = data["questions"]
            if isinstance(data, list) and len(data) == quota:
                questions = data
                break
            print(f"      [Warning] Attempt {attempt+1}: expected {quota} questions, got {len(data) if isinstance(data, list) else type(data)}")
        except Exception as e:
            print(f"      [Warning] Attempt {attempt+1} failed to parse MCQ JSON: {e}")

    if not questions:
        raise ValueError(f"Không thể sinh được Đề thi trắc nghiệm cho session {session_id} sau 3 lần thử.")
    return questions


def exam_oral_questions_creator(
    session_id: str, session_title: str, tech_stack: str, practical_exam_content: str,
    is_final: bool, forbidden_scope: str = "", allowed_scope: str = "", chosen_domain: str = ""
) -> str:
    """Generates Câu hỏi vấn đáp (Oral Defense Questions) tied to the practical exam's own
    concrete requirements -- an anti-plagiarism check, not a re-run of the MCQ theory exam."""
    n_range = _oral_quota_range(is_final)
    print(f"    -> [Exam Creator] Generating Câu hỏi vấn đáp ({n_range} questions, {_exam_label(is_final)}) for '{session_title}'...")

    domain_prompt_block = _build_domain_prompt_block(session_id, session_title, chosen_domain)

    system_prompt = f"""You are a Senior Technical Examiner at Rikkei Education, authoring {n_range} ORAL DEFENSE
QUESTIONS for the {_exam_label(is_final)} of:
Session: {session_id} - {session_title}
Technology Stack: {tech_stack}
{domain_prompt_block}

Allowed Knowledge Scope: {allowed_scope or 'Fundamentals up to this exam'}
Forbidden Knowledge Scope (STRICTLY PROHIBITED): {forbidden_scope or 'None remaining'}

THE STUDENT'S PRACTICAL EXAM (the questions below MUST reference concrete design decisions or
code elements that would plausibly appear in a correct solution to THIS exact exam -- never
generic textbook questions unrelated to this submission):
---
{practical_exam_content[:6000]}
---

MANDATORY DIRECTIVES:
1. Each question MUST reference a concrete function/endpoint/screen-element or design decision
   from the practical exam above (e.g. "Giải thích lý do bạn chọn cấu trúc dữ liệu X cho tính năng
   Y", "Nếu yêu cầu Z đổi thành ..., bạn sẽ sửa đoạn code nào và vì sao?").
2. Include a short "Định hướng đáp án đạt" note per question describing what a competent, genuine
   answer sounds like, to help the instructor score consistently.
3. Professional academic tone, 100% Accented Vietnamese, no AI mentions, no informal words.
4. Return ONLY raw Markdown, exactly this structure per question:

### Câu N: [Câu hỏi vấn đáp cụ thể]
> **Định hướng đáp án đạt:** [Mô tả ngắn gọn câu trả lời hợp lệ]

---

Start with heading: # Bộ câu hỏi vấn đáp — {_exam_label(is_final)}
"""
    user_prompt = f"Author the oral defense question set for the {_exam_label(is_final)} of {session_id} ({session_title})."

    content = None
    for attempt in range(3):
        try:
            response = call_llm(system_prompt, user_prompt, json_mode=False, agent_name="Exam Oral Questions Creator", session_id=session_id)
            if response and response.count("### Câu ") >= 5:
                content = response.strip()
                break
        except Exception as e:
            print(f"      [Warning] Attempt {attempt+1} failed to generate Oral Questions: {e}")

    if not content:
        raise ValueError(f"Không thể sinh được Câu hỏi vấn đáp cho session {session_id} sau 3 lần thử.")
    return content


_BANNED_CASUAL_WORDS = ["nhé", "thân mến", "nhé các bạn", "nhe", "nha", "assistant", "chatgpt", "openai", "gemini", "llm", "copilot"]
_DISCRIMINATORY_LABELS = ["dành cho sinh viên", "dành cho học viên", "mức độ:", "độ khó:", "yếu/trung bình", "học lực"]
_VN_BOUNDARY = r"(?<![a-zA-Z0-9_àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđĐ])"
_VN_BOUNDARY_END = r"(?![a-zA-Z0-9_àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđĐ])"


def exam_reviewer_agent(
    practical_exam: Dict[str, Any], mcq_questions: List[Dict[str, Any]], oral_md: str,
    tech_stack: str, forbidden_scope: str, allowed_scope: str, session_title: str,
    curriculum_context_title: str, is_final: bool
) -> Dict[str, Any]:
    """Reviews all 3 exam artifacts before publish. Mirrors project_reviewer_agent's checks plus
    exam-specific structural/quota validation."""
    print("  [Exam Reviewer] Verifying exam artifacts via Systemic Architecture Governance Engine...")

    pe_content = practical_exam.get("content", "")

    # 1. Banned words / discriminatory labels across all 3 artifacts
    all_texts = [("Đề thi thực hành", pe_content), ("Câu hỏi vấn đáp", oral_md)]
    for word in _BANNED_CASUAL_WORDS:
        pattern = rf"{_VN_BOUNDARY}{re.escape(word)}{_VN_BOUNDARY_END}"
        for title, text in all_texts:
            if re.search(pattern, text, re.IGNORECASE):
                return {"status": "REJECTED", "feedback": f"Tài liệu '{title}' chứa từ cấm suồng sã hoặc liên quan đến AI: '{word}'."}
    for label in _DISCRIMINATORY_LABELS:
        for title, text in all_texts:
            if label in text.lower():
                return {"status": "REJECTED", "feedback": f"Tài liệu '{title}' chứa nhãn phân loại học lực hoặc mức độ '{label}'."}

    # 2. 100%-width table check
    if "<table" in pe_content and "width: 100%" not in pe_content and 'width="100%"' not in pe_content:
        return {"status": "REJECTED", "feedback": "Đề thi thực hành sử dụng bảng HTML nhưng chưa cấu hình chiều rộng 100% màn hình."}

    # 3. Architecture / scope linting (reused verbatim from Mini Project governance engine)
    arch_info = resolve_course_architecture(curriculum_context_title, tech_stack, forbidden_scope, allowed_scope)
    for title, text in all_texts:
        violations = lint_document_architecture(title, text, arch_info, forbidden_scope)
        if violations:
            return {"status": "REJECTED", "feedback": "; ".join(violations)}
    mcq_text_blob = json.dumps(mcq_questions, ensure_ascii=False)
    mcq_violations = lint_document_architecture("Đề thi trắc nghiệm", mcq_text_blob, arch_info, forbidden_scope)
    if mcq_violations:
        return {"status": "REJECTED", "feedback": "; ".join(mcq_violations)}

    # 4. Practical exam structural completeness
    pe_required = [
        r"### \*\*1\.\s+Mục tiêu bài thi",
        r"### \*\*2\.\s+Đề bài và Yêu cầu",
        r"### \*\*3\.\s+Ràng buộc kỹ thuật",
        r"### \*\*4\.\s+Tiêu chí chấm điểm",
        r"### \*\*5\.\s+Yêu cầu nộp bài",
    ]
    for r_hdr in pe_required:
        if not re.search(r_hdr, pe_content, re.IGNORECASE):
            return {"status": "REJECTED", "feedback": f"Đề thi thực hành thiếu tiêu đề bắt buộc: '{r_hdr.replace(chr(92), '')}'."}

    # 5. MCQ quota + schema completeness
    quota = _mcq_quota(is_final)
    if len(mcq_questions) != quota:
        return {"status": "REJECTED", "feedback": f"Đề thi trắc nghiệm phải có đúng {quota} câu, hiện có {len(mcq_questions)} câu."}
    valid_types = {"SYNTAX", "EXECUTION_FLOW", "CODE_TRACE", "COMPARISON", "TRAP_PREDICTION"}
    for i, q in enumerate(mcq_questions, 1):
        if not isinstance(q, dict) or not q.get("question") or len(q.get("options", [])) != 4:
            return {"status": "REJECTED", "feedback": f"Câu trắc nghiệm số {i} thiếu nội dung hoặc không đủ 4 phương án trả lời."}
        if q.get("question_type") not in valid_types:
            return {"status": "REJECTED", "feedback": f"Câu trắc nghiệm số {i} có question_type không hợp lệ: '{q.get('question_type')}'."}

    # 6. Oral question count + structure
    oral_count = oral_md.count("### Câu ")
    min_oral, max_oral = (8, 10) if is_final else (6, 8)
    if not (min_oral <= oral_count <= max_oral):
        return {"status": "REJECTED", "feedback": f"Câu hỏi vấn đáp phải có {min_oral}-{max_oral} câu, hiện có {oral_count} câu."}
    if oral_md.count("**Định hướng đáp án đạt:**") < oral_count:
        return {"status": "REJECTED", "feedback": "Một số câu hỏi vấn đáp thiếu ghi chú 'Định hướng đáp án đạt'."}

    return {"status": "APPROVED", "feedback": "Bộ đề thi đạt tất cả tiêu chuẩn chất lượng và phạm vi kiến thức."}


def generate_exam_session(
    session_id: str, session_title: str, session_dir_path: str, tech_stack: str,
    previous_lessons_text: str, curriculum_context_title: str, is_final: bool,
    session_info: Optional[Dict[str, Any]] = None, chosen_domain: str = ""
) -> Dict[str, Any]:
    """Orchestrates the generate -> review -> retry(up to 3x) -> publish loop for a full exam
    session (Đề thi thực hành + Đề thi trắc nghiệm + Câu hỏi vấn đáp)."""
    session_dir = Path(session_dir_path)
    session_dir.mkdir(parents=True, exist_ok=True)

    pe_dir = session_dir / "Đề thi thực hành"
    mcq_dir = session_dir / "Đề thi trắc nghiệm"
    oral_dir = session_dir / "Câu hỏi vấn đáp"
    pe_dir.mkdir(exist_ok=True)
    mcq_dir.mkdir(exist_ok=True)
    oral_dir.mkdir(exist_ok=True)

    forbidden_scope = session_info.get("forbidden_scope", "") if session_info else ""
    allowed_scope = session_info.get("allowed_scope", "") if session_info else ""

    final_practical = None
    final_mcq = None
    final_oral = None
    practical_exam = mcq_questions = oral_md = None

    for attempt in range(3):
        practical_exam = exam_practical_creator(
            session_id, session_title, tech_stack, curriculum_context_title, is_final,
            previous_lessons_text, forbidden_scope, allowed_scope, chosen_domain
        )
        mcq_questions = exam_mcq_creator(
            session_id, session_title, tech_stack, curriculum_context_title, is_final,
            forbidden_scope, allowed_scope, chosen_domain
        )
        oral_md = exam_oral_questions_creator(
            session_id, session_title, tech_stack, practical_exam["content"], is_final,
            forbidden_scope, allowed_scope, chosen_domain
        )

        review_result = exam_reviewer_agent(
            practical_exam, mcq_questions, oral_md, tech_stack, forbidden_scope, allowed_scope,
            session_title, curriculum_context_title, is_final
        )
        if review_result["status"] == "APPROVED":
            final_practical, final_mcq, final_oral = practical_exam, mcq_questions, oral_md
            print(f"  [Exam Reviewer] APPROVED: {review_result['feedback']}")
            break
        else:
            print(f"  [Exam Reviewer] REJECTED (Attempt {attempt+1}): {review_result['feedback']}")

    if not (final_practical and final_mcq and final_oral):
        print(f"  [CẢNH BÁO TỪ PM] Không thể sinh bộ đề thi đạt tiêu chuẩn 100% cho session {session_id} sau nhiều lượt tạo/đánh giá. BỎ QUA LỖI và dùng bản nháp cuối cùng (Pending Human Review).")
        final_practical, final_mcq, final_oral = practical_exam, mcq_questions, oral_md

    from agents.creators.common_utils import clean_markdown_formulas

    pe_content = clean_markdown_formulas(
        generate_and_link_srs_diagram(final_practical["content"], pe_dir, "so_do_de_thi", session_title, tech_stack, forbidden_scope)
    )
    (pe_dir / "de_thi_thuc_hanh.md").write_text(pe_content, encoding="utf-8")
    print(f"  [Success] Saved Đề thi thực hành: {pe_dir / 'de_thi_thuc_hanh.md'}")

    (mcq_dir / "de_thi_trac_nghiem.json").write_text(json.dumps(final_mcq, ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        from core.quiz_excel import export_lesson_quiz_to_excel
        s_num_str = session_id.replace(" ", "")
        excel_path = mcq_dir / f"De_Thi_Trac_Nghiem_{s_num_str}.xlsx"
        export_lesson_quiz_to_excel(final_mcq, str(excel_path))
    except Exception as e:
        print(f"  [Exam Excel Warning] Could not export MCQ Excel: {e}")
    print(f"  [Success] Saved Đề thi trắc nghiệm: {mcq_dir / 'de_thi_trac_nghiem.json'}")

    (oral_dir / "cau_hoi_van_dap.md").write_text(final_oral, encoding="utf-8")
    print(f"  [Success] Saved Câu hỏi vấn đáp: {oral_dir / 'cau_hoi_van_dap.md'}")

    return {"practical_exam": final_practical, "mcq": final_mcq, "oral": final_oral}
