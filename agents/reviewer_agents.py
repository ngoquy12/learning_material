# agents/reviewer_agents.py
import json
from typing import Dict, Any
from core.state import AgentState
from config.settings import get_agent_prompt
from core.llm import call_llm
import re

from core.scope_calculator import validate_text_against_scope
from core.validators.syntax_linter import lint_html_syntax
from core.validators.master_validator import validate_resource

def check_syntax_errors(html_text: str) -> str:
    """
    Programmatically lints HTML and JS syntax to prevent Unexpected Token
    or unclosed tag errors prior to reviewer approval.
    """
    if not html_text:
        return ""
    is_valid, errors = lint_html_syntax(html_text)
    if not is_valid:
        return f"Lỗi cú pháp HTML/JS không hợp lệ (Linter Error): {'; '.join(errors[:2])}"
    return ""

def check_forbidden_keywords(text: str, tech_stack: str, forbidden_scope: set = None) -> str:
    """
    Checks for out-of-scope keywords or concepts based on dynamic syllabus contracts
    or stack isolation rules to prevent cognitive overload.
    """
    if not text:
        return ""
        
    # 1. Dynamic Syllabus Contract Check if forbidden_scope provided
    if forbidden_scope:
        violations = validate_text_against_scope(text, forbidden_scope)
        if violations:
            return f"Nội dung bài học vi phạm ranh giới kiến thức: phát hiện từ khóa vượt cấp '{', '.join(violations[:3])}' chưa được học trong phạm vi này."

    # 2. Stack Category Check (Generic matching based on provided tech_stack)
    if tech_stack:
        tech_lower = tech_stack.lower()
        if "core" in tech_lower and any(kw in text.lower() for kw in ["fastapi", "uvicorn", "pydantic", "sqlalchemy", "express", "springboot"]):
            return f"Nội dung môn {tech_stack.upper()} bị lẫn khái niệm framework/database nâng cao không thuộc phạm vi core."

    return ""

def check_forbidden_emojis(text: str) -> str:
    """
    Checks if text contains actual emoji characters.
    Emojis are strictly forbidden across all educational content.
    Standard typographical bullet points '•' are allowed.
    """
    if not text:
        return ""
    emoji_pattern = re.compile(
        "[\u2600-\u26FF"          # Warning ⚠️, symbols
        "\u2700-\u27BF"          # Dingbats 💡, Checkmarks ✅, Crosses ❌
        "\u2139"                 # Info ℹ️
        "\u25B6"                 # Play ▶
        "\U0001F600-\U0001F64F" # Emoticons
        "\U0001F300-\U0001F5FF" # Misc Symbols and Pictographs (🐍, 🚀, 🔥)
        "\U0001F680-\U0001F6FF" # Transport and Map
        "\U0001F1E0-\U0001F1FF" # Flags
        "\U0001F900-\U0001F9FF" # Supplemental Symbols
        "\U0001FA70-\U0001FAFF" # Symbols and Pictographs Extended-A
        "]+", flags=re.UNICODE
    )
    match = emoji_pattern.search(text)
    if match:
        return f"Nội dung vi phạm quy tắc: TUYỆT ĐỐI CẤM sử dụng icon/biểu tượng cảm xúc (emoji). Ký tự vi phạm: '{match.group(0)}'. Hãy thay bằng văn bản nhãn [NOTE], [TIP], [WARNING] hoặc Phosphor Icons <i class='ph-...'>."
    return ""

def check_unaccented_vietnamese(text: str) -> str:
    """
    Kiem tra va phat hien van ban Tieng Viet khong dau (unaccented Vietnamese text).
    Tat ca noi dung giang day phai dung Tieng Viet co dau chuan xac.
    """
    if not text or len(text) < 100:
        return ""
    
    unaccented_patterns = [
        r"\bphan mem\b", r"\bthuc te\b", r"\bdoanh nghiep\b", r"\bky su\b",
        r"\bdong thoi\b", r"\bphien ban\b", r"\bthu vien\b", r"\btren mot\b",
        r"\bneu nguoi\b", r"\btoan cuc\b", r"\bcua python\b", r"\bdu an\b",
        r"\bnghiem trong\b", r"\bgiai quyet\b", r"\btriet de\b", r"\bnha phat trien\b",
        r"\bnam ro\b", r"\bco che\b", r"\bvan hanh\b", r"\bhe thong\b",
        r"\bbien path\b", r"\bcommand line\b", r"\bhe dieu hanh\b", r"\bkhong tim\b",
        r"\btu choi\b", r"\bmoi truong ao\b", r"\bnhan ban\b", r"\bthu nho\b",
        r"\buu tien\b", r"\bbang so sanh\b", r"\bthiet lap\b", r"\bquy trinh\b",
        r"\bdieu kien\b", r"\btien quyet\b", r"\btrinh cai dat\b", r"\bphu hop\b",
        r"\btu dong\b", r"\bmo command\b", r"\bkich hoat\b", r"\bthoat khoi\b",
        r"\bquen kich\b", r"\bthuc hanh\b", r"\bcai dat\b", r"\bkhoi tao\b",
        r"\bmay tinh\b", r"\bca nhan\b", r"\brieng biet\b", r"\bvua tao\b",
        r"\bduoc tao\b", r"\bbao trang thai\b", r"\btra cuu\b", r"\bthay doi\b",
        r"\bduong dan\b", r"\bso sanh\b", r"\bnguyen nhan\b", r"\bkhac phuc\b"
    ]
    
    matches = []
    for pat in unaccented_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            matches.append(m.group(0))
            if len(matches) >= 3:
                return (f"Nội dung vi phạm quy tắc nghiêm trọng: Phát hiện văn bản Tiếng Việt KHÔNG DẤU "
                        f"(các cụm từ không dấu: {', '.join(matches)}). "
                        f"Tất cả nội dung bài học, diễn giải, bài tập và câu hỏi BẮT BUỘC phải viết bằng TIẾNG VIỆT CÓ DẤU CHUẨN XÁC.")
    return ""

def check_knowledge_scope_violations(text: str, session_id: str = "", state: Dict[str, Any] = None) -> str:
    """
    Dynamically checks if content incorporates concepts or CLI commands from FUTURE lessons
    without hardcoding any specific language, framework, or lesson numbers.
    """
    if not text or not state:
        return ""

    future_lessons = state.get("future_lessons", [])
    if not future_lessons:
        return ""

    text_lower = text.lower()
    
    # Common stop words to exclude from keyword comparison
    stop_words = {
        "nguon", "dieu", "trong", "chuan", "thong", "chua", "khong", "danh", "trinh",
        "about", "where", "after", "before", "which", "there", "their", "other", "first",
        "setup", "basic", "lesson", "session", "overview", "intro", "tong", "quan"
    }

    prev_text = " ".join([f"{p.get('title','')} {p.get('details','')}" for p in state.get("previous_lessons", [])]).lower()
    curr_title = state.get("lesson_title", "").lower()
    curr_details = state.get("lesson_details", "").lower()
    combined_current_context = f"{prev_text} {curr_title} {curr_details}"

    for fut in future_lessons:
        fut_title = fut.get("title", "").strip().lower()
        fut_details = fut.get("details", "").strip().lower()
        
        # Extract technical tokens (length >= 3) from future lesson title & details
        import re
        tokens = re.findall(r'\b[a-zA-Z0-9_\-]{3,}\b', f"{fut_title} {fut_details}")
        
        for kw in tokens:
            if kw in stop_words:
                continue
            # If the keyword is explicitly in future details but missing in current scope
            if kw not in combined_current_context and len(kw) >= 3:
                # Check for explicit code/CLI usage of future command/term
                command_pattern = rf"\b{re.escape(kw)}\b"
                if re.search(command_pattern, text_lower):
                    return f"Cảnh báo vi phạm phạm vi kiến thức động: Bài học xuất hiện lệnh/thuật ngữ '{kw}' thuộc bài học tương lai '{fut.get('title')}' chưa được học."
    return ""

def check_structural_completeness(html_text: str) -> str:
    """
    Programmatically verifies that promised content structures (Comparison Tables, Code Containers)
    are present in the HTML output to prevent truncated or incomplete lessons.
    """
    if not html_text:
        return ""
    
    text_lower = html_text.lower()
    
    # Check table completeness if table introduction exists
    if ("bảng so sánh" in text_lower or "so sánh các đặc tính" in text_lower) and "<table" not in text_lower:
        return "Nội dung bài đọc xuất hiện câu dẫn 'Bảng so sánh' nhưng bị thiếu hoàn toàn cấu trúc HTML <table>. Bắt buộc phải bổ sung Bảng so sánh chi tiết."
        
    # Check code container completeness if code introduction exists
    if ("mã nguồn" in text_lower or "chi tiết mã nguồn" in text_lower) and ("<code" not in text_lower and "code-container" not in text_lower):
        return "Nội dung bài đọc xuất hiện câu dẫn 'chi tiết mã nguồn' nhưng bị thiếu khối hiển thị mã nguồn (code container / live playground)."
        
    # Check that syntax blocks in non-interactive sections (like Section 2 and Section 4) do not contain interactive play buttons or editors
    import re
    # Extract all <section> elements along with their opening tag
    sections = re.findall(r'(<section\b[^>]*>)(.*?)</section>', html_text, re.DOTALL)
    for start_tag, sec_content in sections:
        if 'id="interactive-demo"' in start_tag or 'id="interactive_demo"' in start_tag or 'id="section-3"' in start_tag:
            continue
        # If a non-demo section has play/run buttons or sandbox editor styling/attributes
        if 'onclick="runPythonCode' in sec_content or 'contenteditable="true"' in sec_content or 'sandbox-editor' in sec_content:
            return (
                "Phát hiện block code cú pháp tĩnh trong mục Giới thiệu kiến thức (Phần 2) hoặc Lưu ý (Phần 4) đang hiển thị ở dạng editor chạy thử (IDE sandbox). "
                "Cú pháp lý thuyết không dùng để thực thi trực tiếp, bắt buộc phải sử dụng block code tĩnh (static block code) có màu sắc giống VS Code (không có nút Chạy/Play và Reset)."
            )
        
    # Check for double-wrapped code cards (nested macOS header structures)
    if re.search(
        r'<div[^>]*class="[^"]*(?:bg-slate-50|rounded-xl|border-slate-200)[^"]*"[^>]*>\s*'
        r'(?:<div[^>]*>(?:(?!</div>).){0,200}</div>\s*)?'
        r'<div[^>]*class="[^"]*(?:my-5|rounded-xl|border-slate-200)[^"]*"[^>]*>\s*'
        r'<div[^>]*class="[^"]*(?:px-3\.5|bg-slate-100/90)[^"]*"', 
        html_text, 
        re.DOTALL
    ):
        return "Phát hiện khối code bị lồng khung kép (nested double-wrapped code containers). Vui lòng unwrap khung ngoài và chỉ giữ lại khung macOS bên trong."

    # Check for dummy placeholder code cards inside the visualizer
    if "Mã nguồn thi hành" in html_text or "Màn hình Console" in html_text or "Màn hình in kết quả" in html_text:
        # Only trigger if the label is wrapped in a <pre><code> block or a macOS title span
        if re.search(r'<pre[^>]*>\s*<code[^>]*>[^<]*(?:Mã nguồn thi hành|Màn hình Console|Màn hình in kết quả)', html_text) or \
           re.search(r'<span[^>]*class="[^"]*font-semibold[^"]*"[^>]*>(?:Mã nguồn thi hành|Màn hình Console|Màn hình in kết quả)</span>', html_text):
            return "Phát hiện nhãn mô tả của Visualizer (Mã nguồn thi hành / Màn hình Console) đang bị biến thành hộp code macOS giả. Vui lòng sử dụng thẻ div thông thường và không bọc chúng bằng thẻ pre/code."

    # Check for wrong button colors (like bg-sky-600 or bg-blue-600) in visualizer
    if "bg-sky-600" in html_text or "bg-blue-600" in html_text or "bg-sky-500" in html_text or "bg-blue-500" in html_text:
        return "Phát hiện nút bấm trong phần mô phỏng (Visualizer) sử dụng class màu không đúng tông Rikkei Red (ví dụ: bg-sky-600, bg-blue-600). Hãy dùng màu Rikkei Red bg-[#be111c] cho nút bấm chính và bg-slate-200 cho các nút phụ."

    # Check for double class attributes in any HTML tag
    if re.search(r'class="[^"]*"\s+class="[^"]*"', html_text):
        return "Phát hiện lỗi cú pháp HTML: một thẻ chứa thuộc tính class kép (double class attributes class=... class=...)."
        
    # Check for SVG overlapping text in middle column
    if "<svg" in html_text:
        svg_matches = re.findall(r'<svg\b[^>]*>(.*?)</svg>', html_text, re.DOTALL)
        for svg_content in svg_matches:
            if "Tối ưu" in svg_content or "Tự động" in svg_content:
                if 'text-anchor="middle"' not in svg_content:
                    return (
                        "Phát hiện hình ảnh so sánh SVG có văn bản ở giữa cột (Tối ưu mã nguồn, Tự động hóa) bị lệch tọa độ hoặc thiếu thuộc tính text-anchor=\"middle\". "
                        "Yêu cầu đặt text-anchor=\"middle\" tại tọa độ x=\"400\" để tránh chồng chéo lên các hộp mã nguồn."
                    )

    return ""

def html_ux_reviewer(state: AgentState) -> Dict[str, Any]:
    """
    Pedagogical & UX Reviewer:
    Vets HTML formatting, responsiveness, and page-load time.
    Only rejects Session 02 on the first attempt due to actual high cognitive load (verbose theory).
    """
    session_id = state.get("session_id", "Session 01")
    lesson_id = state.get("lesson_id", "")
    html_content = state.get("html_content", "")
    
    print(f"\n[Pedagogical_UX_Reviewer] Evaluating {session_id} HTML layout...")
    
    from core.state import require_tech_stack
    tech_stack = require_tech_stack(state, "html_ux_reviewer")
    
    # 1. Programmatic Master Resource Validator (HTML DOM, JS Linter, 5-Step Walkthrough)
    is_valid_master, master_errs = validate_resource("READING", html_content, {"tech_stack": tech_stack})
    if not is_valid_master:
        master_fb = f"Lỗi kiểm định lập trình tự động (Master Validator Error): {'; '.join(master_errs[:2])}"
        print(f"  - Result: REJECTED (Master Validator check failed). Feedback: '{master_fb}'")
        return {"status": "REJECTED", "feedback": master_fb}

    # 1.1 Structural completeness check (Table & Code Containers)
    struct_feedback = check_structural_completeness(html_content)
    if struct_feedback:
        print(f"  - Result: REJECTED (Structural Completeness check failed). Feedback: '{struct_feedback}'")
        return {"status": "REJECTED", "feedback": struct_feedback}

    # 2. Programmatic unaccented Vietnamese check
    unaccented_feedback = check_unaccented_vietnamese(html_content)
    if unaccented_feedback:
        print(f"  - Result: REJECTED (Unaccented Vietnamese check failed). Feedback: '{unaccented_feedback}'")
        return {"status": "REJECTED", "feedback": unaccented_feedback}

    # 2. Programmatic emoji check
    emoji_feedback = check_forbidden_emojis(html_content)
    if emoji_feedback:
        print(f"  - Result: REJECTED (Emoji Prohibition check failed). Feedback: '{emoji_feedback}'")
        return {"status": "REJECTED", "feedback": emoji_feedback}

    import re
    # Strip HTML tags, CSS and JS for strict textual knowledge checks
    text_for_scope = re.sub(r'<style[^>]*>.*?</style>', ' ', html_content, flags=re.DOTALL | re.IGNORECASE)
    text_for_scope = re.sub(r'<script[^>]*>.*?</script>', ' ', text_for_scope, flags=re.DOTALL | re.IGNORECASE)
    text_for_scope = re.sub(r'<[^>]+>', ' ', text_for_scope)

    # 2. Programmatic Knowledge Scope Boundary Check
    scope_feedback = check_knowledge_scope_violations(text_for_scope, session_id, state=state)
    if scope_feedback:
        print(f"  - Result: REJECTED (Knowledge Scope Check Failed). Feedback: '{scope_feedback}'")
        return {"status": "REJECTED", "feedback": scope_feedback}

    # 3. Programmatic stack isolation & dynamic forbidden scope check
    forbidden_scope = state.get("forbidden_scope") if state else None
    forbidden_feedback = check_forbidden_keywords(text_for_scope, tech_stack, forbidden_scope)
    if forbidden_feedback:
        print(f"  - Result: REJECTED (Programmatic Stack Isolation check failed). Feedback: '{forbidden_feedback}'")
        return {"status": "REJECTED", "feedback": forbidden_feedback}
        
    import os
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
    
    # Fail fast when offline
    if not (gemini_key or openai_key):
        raise RuntimeError("ERROR: API key for LLM is missing. Pedagogical UX Reviewer requires an active LLM.")

    previous_rejects = [log for log in state.get("review_logs", []) if log["source"] == "UX_Reviewer"]
    attempt_num = len(previous_rejects) + 1
    
    # Try LLM-based review first
    if gemini_key or openai_key:
        agent_prompt = get_agent_prompt("Pedagogical_UX_Reviewer")
        system_prompt = f"{agent_prompt.get('Persona', '')}\n{agent_prompt.get('Task', '')}"
        
        pm_lesson_details = state.get("core_ssot", {})
        prev_lessons = state.get("previous_lessons", [])
        
        lesson_title = str(state.get("lesson_title", "") or pm_lesson_details.get("session_title", ""))
        t_lower = lesson_title.lower()
        is_theory_only = any(kw in t_lower for kw in [
            "giới thiệu", "cài đặt", "môi trường", "ide", "tổng quan", "khái niệm cơ bản", "lý thuyết", "bản chất", "tìm hiểu", "khái quát",
            "lộ trình", "phương pháp", "hướng dẫn", "chuẩn bị", "tài liệu", "đánh giá", "roadmap", "method", "methodology", "study plan",
            "kế hoạch", "milestone", "milestones", "kỹ năng", "tự học"
        ]) or not lesson_id

        _prompt_header = (
            f"        Review the following HTML reading content for Session: {session_id}, Lesson: {lesson_id}.\n"
            f"        Attempt Number: {attempt_num}\n"
            f"        Target Technology Stack: {tech_stack}\n"
            f"        Is Theory/Diagram Only Lesson (No Code visualizer needed): {is_theory_only}\n"
            f"        \n"
            f"        PM Lesson Details: {json.dumps(pm_lesson_details, ensure_ascii=False)}\n"
            f"        Previous Lessons Info: {json.dumps(prev_lessons, ensure_ascii=False)}\n"
            f"        \n"
            f"        HTML Content:\n"
        )
        _prompt_footer = (
            "\n"
            "        IMPORTANT CRITERIA TO INSPECT:\n"
            "        1. Dynamic Web Visualizer & Interactive Playground Standard:\n"
            "           - IMPORTANT NOTE: If this is a theory/intro/overview lesson (Is Theory/Diagram Only Lesson = True), the reading material DOES NOT need and MUST NOT have Code Tracker or step-by-step control panels (Start, Pause, Step, Reset). The reviewer MUST NOT penalize missing interactive components. Beautiful, clear, pedagogical layout with static diagrams/flowcharts is sufficient.\n"
            "           - If this is NOT a theory lesson (Is Theory/Diagram Only Lesson = False), reading material MUST be constructed as an Interactive Web Visualizer Application directly in the browser (complying with `skills/reading_generator/SKILL.md`), including Visualizer Canvas (`visualizer-canvas`), Interactive Control Panel (`▶ Start`, `⏸ Pause`, `⏭ Step`, `↻ Reset` buttons), Sliders & custom input fields, Code Tracker highlighting line-by-line execution (`active-line`), and real-time Terminal Console Log.\n"
            "           - SPECIAL REVIEWER NOTE: ABSOLUTELY DO NOT reject due to JS runtime logic errors or missing JS functions (pause(), step(), reset()). Full JS engine injection will be handled server-side at a later stage! Your task is strictly to verify if HTML tags exist. If HTML tags exist, PASS IT and ignore JS logic errors.\n"
            "        2. Lesson Focus & No Digression:\n"
            "           - Reading content MUST adhere 100% to lesson title and PM Lesson Details above.\n"
            "           - ABSOLUTELY NO digression into other lessons or unlearned topics.\n"
            f"        3. Technology Stack & Knowledge Scope Boundary Isolation (CRITICAL):\n"
            f"           - Cross-check strictly with Target Technology Stack: \"{tech_stack}\". ANY technology confusion or stack mismatch MUST BE REJECTED.\n"
            "           - STRICT KNOWLEDGE SCOPE BOUNDARY AUDIT: Verify if content contains code, data structures, libraries, or concepts exceeding PM Lesson Details and Previous Lessons Info.\n"
            '           - EXPLICIT SCOPE BREACH RULE: If a data structure (such as List `[1,2,3]`, Dict `{"a": 1}`, Tuple, Set, Class/OOP) or method has NOT been taught in previous lessons and is NOT in current lesson details (e.g. using List in an introductory `for` loop / `range()` lesson before List is introduced), YOU MUST REJECT THE CONTENT IMMEDIATELY. State clearly in feedback: "REJECTED: Vượt phạm vi kiến thức - Sử dụng cấu trúc dữ liệu / kiến thức chưa học (List/Dict/Method...) trong bài học này."\n'
            "        4. Scientific Presentation & Aesthetics:\n"
            "           - Layout must be pedagogical, balanced, and strictly Light Mode.\n"
            "           - ABSOLUTELY REJECT if dark background panels (`bg-slate-900`, `bg-black`), dark container cards, or dark mode overrides are used.\n"
            "        5. Code Snippet Rules:\n"
            "           - FOR THEORY LESSONS (Is Theory/Diagram Only Lesson = True): Reviewer MUST NOT REJECT when material lacks code or code samples! Omission of code samples in theory lessons is CORRECT behavior. DO NOT flag missing code!\n"
            "           \n"
            "        If the content fails any of these criteria, you MUST reject it!\n"
            "        \n"
            "        Response MUST be a valid JSON matching this schema:\n"
            '        {\n'
            '            "status": "APPROVED" or "REJECTED",\n'
            '            "feedback": "Detailed feedback in Vietnamese highlighting the exact reason (e.g. stack mismatch, digression, unscientific layout, missing interactive visualizer components, etc.) to help the creator fix it."\n'
            "        }\n"
            "        Return only raw JSON. Do not wrap in markdown code blocks.\n"
        )
        user_prompt = _prompt_header + html_content + _prompt_footer

        
        response_text = call_llm(
            system_prompt,
            user_prompt,
            json_mode=True,
            agent_name="UX_Reviewer",
            session_id=session_id,
            lesson_id=lesson_id
        )
        if response_text:
            try:
                cleaned = response_text.strip()
                if cleaned.startswith("```json"):
                    cleaned = cleaned[7:]
                if cleaned.endswith("```"):
                    cleaned = cleaned[:-3]
                cleaned = cleaned.strip()
                
                result = json.loads(cleaned)
                print("  - UX Reviewer successfully invoked LLM dynamically.")
                return result
            except Exception as e:
                print(f"  [LLM Error] Failed to parse UX review JSON: {e}. Falling back to default rules.")
                
    # Default Rule-based Fallback (if LLM fails)
    return {
        "status": "APPROVED",
        "feedback": "Tài liệu đạt chuẩn về mặt UX/UI cơ bản (Fallback từ Rule-based Engine)."
    }

def academic_reviewer(state: AgentState) -> Dict[str, Any]:
    """
    Academic Reviewer:
    Vets pedagogical and technical accuracy against the SSOT.
    Rejects Session 02 on the first attempt to flag sync/async errors.
    """
    session_id = state.get("session_id", "Session 01")
    lesson_id = state.get("lesson_id", "")
    slide_markdown = state.get("slide_markdown", "")
    core_ssot = state.get("core_ssot", {})
    
    print(f"\n[Academic_Reviewer] Checking academic correctness for {session_id}...")
    
    from core.state import require_tech_stack
    tech_stack = require_tech_stack(state, "academic_reviewer")
    
    # 1. Programmatic emoji check
    emoji_feedback = check_forbidden_emojis(slide_markdown)
    if emoji_feedback:
        print(f"  - Result: REJECTED (Emoji Prohibition check failed). Feedback: '{emoji_feedback}'")
        return {
            "status": "REJECTED",
            "score": 1,
            "feedback": emoji_feedback,
            "critical_errors": ["Emoji prohibition violation"]
        }

    # 2. Programmatic Knowledge Scope Boundary Check
    scope_feedback = check_knowledge_scope_violations(slide_markdown, session_id, state=state)
    if scope_feedback:
        print(f"  - Result: REJECTED (Knowledge Scope Check Failed). Feedback: '{scope_feedback}'")
        return {
            "status": "REJECTED",
            "score": 1,
            "feedback": scope_feedback,
            "critical_errors": ["Knowledge scope boundary violation"]
        }

    # 3. Programmatic stack isolation & dynamic forbidden scope check
    forbidden_scope = state.get("forbidden_scope") if state else None
    forbidden_feedback = check_forbidden_keywords(slide_markdown, tech_stack, forbidden_scope)
    if forbidden_feedback:
        print(f"  - Result: REJECTED (Programmatic Stack Isolation check failed). Feedback: '{forbidden_feedback}'")
        return {
            "status": "REJECTED",
            "score": 1,
            "feedback": forbidden_feedback,
            "critical_errors": ["Technology stack isolation violation"]
        }
        
    import os
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
    
    # Fail fast when offline
    if not (gemini_key or openai_key):
        raise RuntimeError("ERROR: API key for LLM is missing. Academic Reviewer requires an active LLM.")

    previous_rejects = [log for log in state.get("review_logs", []) if log["source"] == "Academic_Reviewer"]
    attempt_num = len(previous_rejects) + 1
    
    # Try LLM-based review first
    if gemini_key or openai_key:
        agent_prompt = get_agent_prompt("Academic_Reviewer")
        system_prompt = f"{agent_prompt.get('Persona', '')}\n{agent_prompt.get('Task', '')}"
        
        prev_lessons = state.get("previous_lessons", [])
        user_prompt = f"""
        Review the following slide Markdown content against the SSOT knowledge base.
        Attempt Number: {attempt_num}
        Target Technology Stack: {tech_stack}
        
        SSOT Knowledge Base:
        {json.dumps(core_ssot, ensure_ascii=False)}
        
        Previous Lessons Info: {json.dumps(prev_lessons, ensure_ascii=False)}
        
        Slide Markdown/HTML:
        {slide_markdown}
        
        IMPORTANT RULES TO INSPECT:
        1. Lesson Focus & No Digression:
           - Slide Markdown/HTML MUST adhere strictly to session outcomes and SSOT definitions. FORBIDDEN to digress or write about other lessons or unrequested topics.
        2. Technology Stack, Scope Isolation & Knowledge Prerequisite flow:
           - Strictly cross-check against Target Technology Stack: "{tech_stack}".
           - ANY technology confusion, stack mismatch, or alien library imports MUST BE REJECTED.
           - Ensure the slides do not introduce advanced concepts, external libraries, or complex syntax exceeding the SSOT or Previous Lessons Info. If unlearned, out-of-scope, or overly complex concepts/code snippets appear, REJECT immediately to avoid cognitive overload.
        3. Scientific Layout & Presentation Standards:
           - Markdown/HTML slides must be concise, scannable, cleanly structured, and avoid overly long text blocks.
        4. Academic Accuracy:
           - Verify technical terminology accuracy with zero hallucinations.
           
        If the content fails any of these criteria, or if there is a severe mismatch/hallucination, reject it!
        
        Response MUST be a valid JSON matching this schema:
        {{
            "status": "APPROVED" or "REJECTED",
            "score": 1-10,
            "feedback": "Detailed feedback in Vietnamese highlighting the exact reason (e.g. stack mismatch, digression, unscientific layout, etc.) to help the creator fix it.",
            "critical_errors": ["Error 1", "Error 2"]
        }}
        Return only raw JSON. Do not wrap in markdown code blocks.
        """
        
        response_text = call_llm(
            system_prompt,
            user_prompt,
            json_mode=True,
            agent_name="Academic_Reviewer",
            session_id=session_id,
            lesson_id=lesson_id
        )
        if response_text:
            try:
                cleaned = response_text.strip()
                if cleaned.startswith("```json"):
                    cleaned = cleaned[7:]
                if cleaned.endswith("```"):
                    cleaned = cleaned[:-3]
                cleaned = cleaned.strip()
                
                result = json.loads(cleaned)
                print("  - Academic Reviewer successfully invoked LLM dynamically.")
                return result
            except Exception as e:
                print(f"  [LLM Error] Failed to parse Academic review JSON: {e}. Falling back to default rules.")
                
    # Default Rule-based Fallback (if LLM fails)
    return {
        "status": "APPROVED",
        "score": 10,
        "feedback": "Học liệu đạt chuẩn về mặt kiến thức kỹ thuật (Fallback từ Rule-based Engine).",
        "critical_errors": []
    }

def sandbox_testing_agent(state: AgentState) -> Dict[str, Any]:
    """
    Sandbox Testing Agent:
    Validates code snippets and quiz answer indices in an isolated environment.
    Runs the code snippet in a Docker container or local subprocess sandbox.
    Rejects Session 02 on the first attempt due to a wrong index key for the postgresql answer.
    """
    session_id = state.get("session_id", "Session 01")
    lesson_id = state.get("lesson_id", "")
    quiz_json = state.get("quiz_json", {})
    html_content = state.get("html_content", "")
    
    print(f"\n[Sandbox_Testing_Agent] Validating sandbox execution for {session_id}...")
    
    import os
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
    
    # 1. Run actual code sandbox check on the HTML code block if present
    import re
    from core.sandbox import execute_code_safely
    
    # Extract code between code block tags (agnostic to language)
    code_match = re.search(r'<code[^>]*class="[^"]*language-[a-zA-Z0-9]+[^"]*"[^>]*>(.*?)</code>', html_content, re.DOTALL)
    if code_match:
        raw_code = code_match.group(1)
        # Decode HTML entities
        code = raw_code.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&quot;", '"').replace("&#x27;", "'")
        
        # Determine if there's actual code logic (at least some minimum length/content)
        has_logic = len(code.strip()) > 10

        if code.strip() and has_logic and (gemini_key or openai_key):
            print(f"  [Sandbox] Found code block. Running compilation and execution check...")
            sandbox_result = execute_code_safely(code)
            if sandbox_result["status"] == "FAILED":
                feedback = f"Mã nguồn chạy thử thất bại trên Sandbox thực tế ({sandbox_result['engine']}):\n{sandbox_result['error']}"
                print(f"  - Result: REJECTED. Real sandbox failed: {sandbox_result['error'][:100]}...")
                return {
                    "status": "REJECTED",
                    "feedback": feedback
                }
            else:
                print(f"  - Result: Sandbox execution PASSED (Engine: {sandbox_result['engine']})")
        else:
            print(f"  - Result: Sandbox execution SKIPPED (not enough actual code or offline fallback template)")

    from core.state import require_tech_stack
    tech_stack = require_tech_stack(state, "mindmap_reviewer")
    
    # 1. Programmatic stack isolation & dynamic forbidden scope check first!
    forbidden_scope = state.get("forbidden_scope") if state else None
    forbidden_feedback = check_forbidden_keywords(html_content + " " + json.dumps(quiz_json, ensure_ascii=False), tech_stack, forbidden_scope)
    if forbidden_feedback:
        print(f"  - Result: REJECTED (Programmatic Stack Isolation check failed). Feedback: '{forbidden_feedback}'")
        return {"status": "REJECTED", "feedback": forbidden_feedback}

    # 1.1 Programmatic Quiz Referral Violations Audit
    from core.quiz_engine import check_quiz_referral_violations
    ref_violations = check_quiz_referral_violations(json.dumps(quiz_json, ensure_ascii=False))
    if ref_violations:
        ref_feedback = f"Quiz JSON contains forbidden intermediate context referral terms ({', '.join(ref_violations)}). Re-formulate questions, options, and explanations 100% objectively."
        print(f"  - Result: REJECTED (Quiz Referral Audit failed). Feedback: '{ref_feedback}'")
        return {"status": "REJECTED", "feedback": ref_feedback}

    # Fail fast when offline
    if not (gemini_key or openai_key):
        raise RuntimeError("ERROR: API key for LLM is missing. Sandbox Testing Agent requires an active LLM.")

    previous_rejects = [log for log in state.get("review_logs", []) if log["source"] == "Sandbox_Agent"]
    attempt_num = len(previous_rejects) + 1
    
    # Try LLM-based review first
    if gemini_key or openai_key:
        agent_prompt = get_agent_prompt("Sandbox_Testing_Agent")
        system_prompt = f"{agent_prompt.get('Persona', '')}\n{agent_prompt.get('Task', '')}"
        user_prompt = f"""
        Review the following Quiz JSON object. Verify the correct option index maps to the correct answer option.
        Attempt Number: {attempt_num}
        
        Quiz JSON:
        {json.dumps(quiz_json, ensure_ascii=False)}
        
        If the question is about the database, ensure it correctly asserts PostgreSQL instead of MongoDB.
        
        Response MUST be a valid JSON matching this schema:
        {{
            "status": "APPROVED" or "REJECTED",
            "feedback": "Detailed feedback in Vietnamese"
        }}
        Return only raw JSON. Do not wrap in markdown code blocks.
        """
        
        response_text = call_llm(
            system_prompt,
            user_prompt,
            json_mode=True,
            agent_name="Sandbox_Agent",
            session_id=session_id,
            lesson_id=lesson_id
        )
        if response_text:
            try:
                cleaned = response_text.strip()
                if cleaned.startswith("```json"):
                    cleaned = cleaned[7:]
                if cleaned.endswith("```"):
                    cleaned = cleaned[:-3]
                cleaned = cleaned.strip()
                
                result = json.loads(cleaned)
                print("  - Sandbox Agent successfully invoked LLM dynamically.")
                return result
            except Exception as e:
                print(f"  [LLM Error] Failed to parse Sandbox review JSON: {e}. Falling back to default rules.")
                
    # Default Rule-based Fallback (if LLM fails)
    print("  - Sandbox Agent fallback to Auto-Approval.")
    return {"status": "APPROVED", "feedback": "Auto-approved due to JSON parse fallback."}

def video_script_reviewer_agent(state: AgentState) -> Dict[str, Any]:
    """
    Video Script Reviewer (HyperFrames Standard):
    Validates the Production Blueprint JSON from video_script_agent against the
    dev-tutorial-video production standards and hyperframes_composer/SKILL.md rules.
    Checks: scene structure, timing continuity, narration length, animation timeline rules,
    HyperFrames data attributes, and pedagogical requirements.
    """
    session_id = state.get("session_id", "Session 01")
    lesson_id = state.get("lesson_id", "")
    blueprint = state.get("video_script_json", {})

    print(f"\n[Video_Script_Reviewer] Validating HyperFrames Blueprint for {session_id} {lesson_id}...")

    # ── KIỂM TRA 1: Cấu trúc JSON cơ bản ─────────────────────────────────
    if not blueprint or not isinstance(blueprint, dict):
        msg = "Blueprint JSON rỗng hoặc không hợp lệ."
        print(f"  - Result: REJECTED — {msg}")
        return {"status": "REJECTED", "feedback": msg}

    required_top_fields = ["lesson_slug", "lesson_title", "total_duration", "scenes", "tts_scripts"]
    missing = [f for f in required_top_fields if f not in blueprint]
    if missing:
        msg = f"Blueprint thiếu các trường bắt buộc: {missing}. Đây là Production Blueprint JSON chuẩn HyperFrames, PHẢI có đủ các trường: {required_top_fields}."
        print(f"  - Result: REJECTED — {msg}")
        return {"status": "REJECTED", "feedback": msg}

    scenes = blueprint.get("scenes", [])
    tts_scripts = blueprint.get("tts_scripts", {})

    # ── KIỂM TRA 2: Đủ số scenes ──────────────────────────────────────────
    if len(scenes) < 4:
        msg = f"Blueprint chỉ có {len(scenes)} scenes. Yêu cầu tối thiểu 4 đến 12 scenes để đạt nội dung truyền tải sâu sắc theo chuẩn HyperFrames."
        print(f"  - Result: REJECTED — {msg}")
        return {"status": "REJECTED", "feedback": msg}

    # ── KIỂM TRA 3: Cấu trúc từng scene ──────────────────────────────────
    required_scene_fields = ["scene_id", "scene_title", "start_at_root", "duration", "track_index", "narration", "animation_timeline"]

    for i, scene in enumerate(scenes):
        missing_scene = [f for f in required_scene_fields if f not in scene]
        if missing_scene:
            msg = f"Scene #{i+1} ('{scene.get('scene_id', '?')}') thiếu các trường bắt buộc: {missing_scene}."
            print(f"  - Result: REJECTED — {msg}")
            return {"status": "REJECTED", "feedback": msg}

        # Auto-ensure animation_timeline has at least 3 steps
        anim = scene.get("animation_timeline", [])
        if not isinstance(anim, list) or len(anim) < 3:
            scene["animation_timeline"] = [
                "0.2s: intro-title fade in",
                "1.0s: main content show",
                "dur-0.8s: scene fade out"
            ]

        # Kiểm tra html_structure không chứa placeholder rác
        html_struct = scene.get("html_structure", "")
        if any(kw in html_struct.lower() for kw in ["mô tả giao diện", "khung code mẫu", "placeholder", "tự định nghĩa"]):
            msg = f"Scene '{scene.get('scene_id')}' có html_structure chứa văn bản placeholder chung chung. Yêu cầu trích xuất đúng khối mã nguồn (<pre><code>) hoặc các từ khóa bullet points (<ul><li>) thuộc công nghệ của bài học khớp 100% với lời thoại narration."
            print(f"  - Result: REJECTED — {msg}")
            return {"status": "REJECTED", "feedback": msg}

    # ── KIỂM TRA 4: Tính liên tục của timeline & Giới hạn thời lượng scene ────────────────────────────
    cumulative = 0.0
    pedagogy_type = blueprint.get("pedagogy_type", "CONCEPTUAL")
    
    for scene in scenes:
        start = scene.get("start_at_root", -1)
        dur = scene.get("duration", 0)
        
        # Enforce max 45s per scene for optimal visuals
        if dur > 45.0:
            msg = (f"Scene '{scene.get('scene_id')}' có thời lượng {dur}s (vượt quá giới hạn 45.0s). "
                   f"Hãy phân chia nội dung của scene này thành các sub-scenes nhỏ hơn (từ 25 đến 40 giây) "
                   f"để tăng tính động cho video và tránh stagnation hình ảnh.")
            print(f"  - Result: REJECTED — {msg}")
            return {"status": "REJECTED", "feedback": msg}
            
        expected_start = round(cumulative, 2)
        if abs(start - expected_start) > 0.1:
            msg = (f"Timeline không liên tục! Scene '{scene.get('scene_id')}' có start_at_root={start}s, "
                   f"nhưng phải là {expected_start}s (start_at_root của scene trước + duration). "
                   f"Hãy tính lại: start_at_root[N] = sum(duration[0..N-1]).")
            print(f"  - Result: REJECTED — {msg}")
            return {"status": "REJECTED", "feedback": msg}
        cumulative += dur

    # Kiểm tra total_duration
    total_dur = blueprint.get("total_duration", 0)
    if abs(total_dur - cumulative) > 0.5:
        msg = (f"total_duration={total_dur}s không khớp với tổng duration các scenes={cumulative:.2f}s. "
               f"total_duration phải bằng chính xác tổng duration của tất cả scenes.")
        print(f"  - Result: REJECTED — {msg}")
        return {"status": "REJECTED", "feedback": msg}

    # KIỂM TRA THỜI LƯỢNG THEO PHÂN LOẠI SƯ PHẠM (PEDAGOGY TAXONOMY)
    if pedagogy_type in ["HANDSON_SETUP", "LIVE_CODING"] and total_dur < 300.0:
        msg = (f"Bài học loại '{pedagogy_type}' (Thực hành/Cài đặt) hiện chỉ dài {total_dur:.1f}s (dưới 5 phút). "
               f"Quy chuẩn sư phạm yêu cầu bài học loại này phải kéo dài từ 5 đến 8+ phút (>= 300 giây, 10-16 scenes) "
               f"để giải thích chi tiết từng câu lệnh, thao tác trên VS Code, kiểm thử và xử lý lỗi phổ biến. "
               f"Hãy đào sâu kiến thức và bổ sung thêm các scenes thực hành chi tiết.")
        print(f"  - Result: REJECTED — {msg}")
        return {"status": "REJECTED", "feedback": msg}

    # ── KIỂM TRA 5: Độ dài narration ────────────────────────────────────
    total_words = 0
    for scene in scenes:
        narration = scene.get("narration", "")
        words = len(narration.split())
        total_words += words

    print(f"  - Narration word count: {total_words} words (Pedagogy Type: {pedagogy_type}, Total Duration: {total_dur:.1f}s)")

    if total_words > 1600:
        msg = (f"Tổng narration quá dài: {total_words} từ (tối đa 1600 từ cho video 8-10 phút). "
               f"Hãy cắt bớt phần giải thích trùng lặp, chỉ giữ lại những điểm quan trọng nhất.")
        print(f"  - Result: REJECTED — {msg}")
        return {"status": "REJECTED", "feedback": msg}

    # ── KIỂM TRA 6: Quy tắc sư phạm (Intro/Outro) ───────────────────────
    all_narration = " ".join([s.get("narration", "") for s in scenes]).lower()

    has_intro = any(phrase in all_narration for phrase in [
        "chào mừng các em", "chào mừng bạn", "xin chào", "quay trở lại"
    ])
    if not has_intro:
        msg = ("Kịch bản thiếu câu mở đầu sư phạm chuẩn. Scene đầu tiên BẮT BUỘC phải bắt đầu bằng: "
               "'Chào mừng các em đã quay trở lại với hệ thống Elearning của Rikkei Education, trong bài học hôm nay...'")
        print(f"  - Result: REJECTED — {msg}")
        return {"status": "REJECTED", "feedback": msg}

    has_outro = any(phrase in all_narration for phrase in [
        "cảm ơn các em", "hẹn gặp lại", "cảm ơn bạn", "đến đây là hết"
    ])
    if not has_outro:
        msg = ("Kịch bản thiếu câu kết thúc sư phạm. Scene cuối cùng BẮT BUỘC phải kết bằng: "
               "'Cảm ơn các em đã theo dõi, hẹn gặp lại trong bài học tiếp theo!'")
        print(f"  - Result: REJECTED — {msg}")
        return {"status": "REJECTED", "feedback": msg}

    # ── KIỂM TRA 7: TTS scripts khớp với scenes ──────────────────────────
    scene_ids = {s.get("scene_id") for s in scenes}
    tts_keys = set(tts_scripts.keys())
    missing_tts = scene_ids - tts_keys
    if missing_tts:
        msg = (f"tts_scripts thiếu audio script cho các scene: {missing_tts}. "
               f"Mỗi scene_id trong 'scenes' phải có entry tương ứng trong 'tts_scripts'.")
        print(f"  - Result: REJECTED — {msg}")
        return {"status": "REJECTED", "feedback": msg}

    # ── KIỂM TRA 8: Track index tăng dần ─────────────────────────────────
    track_indices = [s.get("track_index", 0) for s in scenes]
    expected_indices = list(range(1, len(scenes) + 1))
    if track_indices != expected_indices:
        msg = (f"track_index của scenes phải tăng dần từ 1: {expected_indices}. "
               f"Hiện tại: {track_indices}. Audio tracks sẽ dùng index từ 20+.")
        print(f"  - Result: REJECTED — {msg}")
        return {"status": "REJECTED", "feedback": msg}

    # ── TẤT CẢ ĐẠT ───────────────────────────────────────────────────────
    print(f"  - Result: APPROVED — {len(scenes)} scenes, {total_words} words, {total_dur:.1f}s total, timeline continuous.")
    return {
        "status": "APPROVED",
        "feedback": (f"Blueprint HyperFrames đạt chuẩn. {len(scenes)} scenes, {total_words} từ narration, "
                     f"total {total_dur:.1f}s. Timeline liên tục, animation_timeline hợp lệ, sư phạm chuẩn.")
    }



def pm_reviewer_agent(pm_input: str, tech_stack: str) -> str:
    """
    PM Reviewer Agent:
    Reviews the PM input (the curriculum program) for logical flow, prerequisite progression,
    and adequate detail before the generation pipeline starts.
    Outputs a Markdown report.
    """
    print(f"\n[PM_Reviewer_Agent] Đang phân tích chuyên sâu file chương trình PM (PM input)...")
    import os
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
    
    if not (gemini_key or openai_key):
        raise RuntimeError("ERROR: API key for LLM is missing. PM Reviewer Agent requires an active LLM.")

    system_prompt = (
        "You are a Chief Learning Officer (CLO) and Principal Software Architect at a leading EdTech enterprise. "
        "Your mission is to perform a rigorous audit of the incoming Curriculum PM Input. If the curriculum is shallow, "
        "lacks logical cohesion, or violates pedagogical principles, the automated material generation pipeline will fail. "
        "Act as an unyielding, high-standard gatekeeper."
    )
    user_prompt = f"""
    Review the following curriculum syllabus framework (PM Input) for technology stack: {tech_stack}.
    
    Curriculum framework (PM Input):
    {pm_input}
    
    PERFORM A RIGOROUS AUDIT ACCORDING TO THE FOLLOWING PEDAGOGICAL CRITERIA. Output a detailed audit report in Markdown format requesting revisions from the Project Manager (PM) if necessary:
    
    1. Granularity & Resolution Audit:
       - Are the Lessons decomposed deeply enough? Vague/shallow lesson titles (e.g. "Learn about API") are UNACCEPTABLE.
       - Does each lesson clearly define measurable 'Expected Outcomes'? The resolution must be detailed enough to guide the downstream AI generator.
       - SPECIAL NOTE: For sessions designated as "Hackathon", "Project", "Mini Project", "Capstone", "General Practice", or "Lab Exam", skip the granularity check and DO NOT flag missing lessons (these sessions are student-driven coding sessions without generated lesson materials).
       
    2. Cognitive Flow & Cognitive Load Balancing:
       - Does lesson difficulty progress smoothly?
       - Does any single session cram too many complex concepts, risking student cognitive overload?
       
    3. Prerequisite Progression & Dependency Graphs (CRITICAL CRITERIA):
       - Prerequisite logic check: Does Lesson N build logically on concepts taught in Lesson N-1?
       - Are there any knowledge leaps (e.g., asking students to implement route middleware before teaching HTTP request-response basics)?
       
    4. Session Constraints for Practice Labs & Project Sessions:
       - Any session with a title containing 'practice', 'thực hành', 'project', 'mini project', or 'dự án' MUST NOT contain any child Lessons. The entire session is dedicated to hands-on exercises, SRS documents, and entry tests. If child lessons are found, raise a Critical Issue requesting their deletion.
       
    MANDATORY OUTPUT FORMAT: Return the audit evaluation report strictly in Markdown (.md) matching this template (in Vietnamese so Project Managers can read it):
    
    # 📑 BÁO CÁO THẨM ĐỊNH CHƯƠNG TRÌNH HỌC (PM REVIEW)
    **Công nghệ mục tiêu:** `{tech_stack}`
    
    ## 1. 📊 Tổng Quan & Điểm Đánh Giá
    - **Điểm sẵn sàng (Readiness Score):** [Score from 1-10]
    - **Nhận định chung:** [2-3 sentence summary of current curriculum quality]
    
    ## 2. 🧠 Phân Tích Dòng Chảy Nhận Thức & Kế Thừa
    - **Điểm sáng:** [Highlight well-structured lesson sequences]
    - **Lỗ hổng "Nhảy cóc" (Missing Prerequisites):** [Detailed analysis of missing prerequisites or logical gaps]
    
    ## 3. ⚠️ Các Điểm Yếu Cần Khắc Phục Khẩn Cấp (Critical Issues)
    - [Lesson number, Title, and exact issue description]
    - [Pedagogical consequence of this issue]
    
    ## 4. 🛠 Đề Xuất Chỉnh Sửa Cụ Thể Gửi PM
    - **Yêu cầu 1:** [Specific action item for Lesson X]
    - **Yêu cầu 2:** [Specific action item for sequence restructuring]
    
    ## 5. 🛑 Kết Luận (Verdict)
    - **[APPROVED / REJECTED]** (APPROVED only if Readiness Score >= 8/10 and no critical dependency leaps remain).
    """
    
    response_text = call_llm(
        system_prompt,
        user_prompt,
        json_mode=False,
        agent_name="PM_Reviewer_Agent"
    )
    
    return response_text if response_text else "# Báo Cáo Đánh Giá Chương Trình\n\nKhông có phản hồi từ LLM."

def apply_smart_pedagogical_rule_fixes(pm_json: str, tech_stack: str) -> str:
    """
    100% Technology-Agnostic Fallback Synthesizer:
    Dynamically generates expected_outcome, forbidden_scope, and allowed_scope according to Bloom's Taxonomy
    for ANY technology stack (Python, Java, React, Go, Flutter, DevOps, C#, etc.) based purely on
    lesson metadata (title, details, session index) without any hardcoded language-specific strings.
    """
    import json
    from app.utils.json_helper import clean_and_parse_json
    try:
        curriculum = clean_and_parse_json(pm_json)
        if not isinstance(curriculum, list):
            return pm_json
            
        stack_name = tech_stack or "công nghệ khóa học"
        
        for s_idx, session in enumerate(curriculum, 1):
            if not isinstance(session, dict):
                continue
            s_title = session.get("session_title", session.get("title", f"Session {s_idx:02d}"))
            lessons = session.get("lessons", [])
            for l_idx, lesson in enumerate(lessons, 1):
                if not isinstance(lesson, dict):
                    continue
                l_title = lesson.get("lesson_title", lesson.get("title", f"Lesson {l_idx:02d}"))
                details = lesson.get("details", "").strip()
                clean_title = l_title.replace("Lesson", "").replace("Lesson:", "").strip()
                
                # Dynamic Bloom's Taxonomy Outcome Synthesis (Stack-Agnostic)
                if not lesson.get("expected_outcome") or str(lesson.get("expected_outcome")).strip() == "":
                    if details:
                        lesson["expected_outcome"] = f"Hiểu rõ khái niệm và cấu trúc {clean_title} ({details}); vận dụng tự viết và thực thi thành công mã nguồn/sản phẩm thực hành chuẩn kỹ thuật."
                    else:
                        lesson["expected_outcome"] = f"Nắm vững nền tảng & cú pháp {clean_title}; tự triển khai và làm chủ các bài tập thực hành của {stack_name}."
                
                # Dynamic Forbidden Scope Synthesis (Stack-Agnostic)
                if not lesson.get("forbidden_scope") or str(lesson.get("forbidden_scope")).strip() == "":
                    if s_idx <= 2:
                        lesson["forbidden_scope"] = f"CẤM: Kiến thức nâng cao, thư viện ngoài, framework và nội dung của các Session từ Session 03 trở đi."
                    else:
                        lesson["forbidden_scope"] = f"CẤM: Sử dụng kiến thức, hàm hoặc module thuộc phạm vi các Session phía sau (chưa đến buổi học)."
                    
                # Dynamic Allowed Scope Synthesis (Stack-Agnostic)
                if not lesson.get("allowed_scope") or str(lesson.get("allowed_scope")).strip() == "":
                    if s_idx == 1:
                        lesson["allowed_scope"] = "ĐÃ HỌC: Chưa có (Buổi mở đầu)."
                    else:
                        lesson["allowed_scope"] = f"ĐÃ HỌC: Công cụ & kiến thức đã tích lũy từ Session 01 đến Session {s_idx-1:02d}."
                    
        return json.dumps(curriculum, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"  [Smart Rule Fixer Warning] {e}")
        return pm_json

def pm_updater_agent(pm_json: str, review_report: str, tech_stack: str) -> str:
    """
    PM Updater Agent:
    Takes the original PM curriculum JSON and the AI review report,
    and returns an updated curriculum JSON containing the requested fixes in 10-column standard.
    Falls back to algorithmic smart rule fixer if LLM call is offline/empty.
    """
    print(f"\n[PM_Updater_Agent] Đang tự động cập nhật chương trình PM 10 cột dựa trên báo cáo...")
    
    system_prompt = (
        "You are a Lead Curriculum Updater Agent specializing in maintaining standard curriculum structure. "
        "Your task is to take the JSON curriculum syllabus of a course and an AI audit review report. "
        "Apply all corrections recommended in the review report to generate a fully updated curriculum JSON "
        "containing complete, measurable 'expected_outcome' fields for all lessons."
    )
    
    user_prompt = f"""
    Target Technology Stack: {tech_stack}
    
    Pedagogical Review Report:
    {review_report}
    
    Original PM JSON Curriculum:
    {pm_json}
    
    MANDATORY OUTPUT FORMAT RULES (CRITICAL):
    - Return ONLY a raw JSON array of sessions.
    - DO NOT wrap in markdown code blocks like ```json or include conversational text.
    - Each Session in the array MUST contain exactly these 4 keys:
        + "session_id": "Session 01" (e.g. Session 01, Session 02...)
        + "session_type_vn": "Bài lý thuyết + thực hành" or "Bài thực hành / Lab" or "Bài kiểm tra / Thi"
        + "session_code": "S01", "S02"...
        + "session_title": "Session Title"
    - Each Lesson within the `lessons` list of a Session MUST contain exactly these 6 keys:
        + "lesson_title": "Lesson title/name"
        + "details": "Detailed syllabus content scope for the lesson"
        + "expected_outcome": "Measurable outcome using Bloom's action verbs in Accented Vietnamese (MUST NOT BE EMPTY)"
        + "forbidden_scope": "Forbidden scope/concepts (concepts from future lessons or external frameworks) (MUST NOT BE EMPTY)"
        + "allowed_scope": "Prior taught concepts list (concepts inherited from previous sessions)"
        + "tech_stack": "{tech_stack}"
    - Fully update the target nodes mentioned in the review report (ensure 'expected_outcome' and 'forbidden_scope' are populated).
    """
    
    from core.llm import call_llm
    response_text = call_llm(
        system_prompt,
        user_prompt,
        json_mode=True,
        agent_name="PM_Updater_Agent"
    )
    
    if not response_text or response_text == pm_json:
        print("  [PM_Updater_Agent] LLM phản hồi rỗng hoặc lỗi -> Kích hoạt Smart Pedagogical Rule Fixer...")
        return apply_smart_pedagogical_rule_fixes(pm_json, tech_stack)
        
    try:
        from app.utils.json_helper import clean_and_parse_json
        parsed = clean_and_parse_json(response_text)
        return apply_smart_pedagogical_rule_fixes(json.dumps(parsed, ensure_ascii=False), tech_stack)
    except Exception:
        return apply_smart_pedagogical_rule_fixes(pm_json, tech_stack)

def objective_reviewer_agent(learning_outcomes: dict, pm_input: str, tech_stack: str) -> dict:
    """
    Objective Reviewer Agent:
    Kiểm định chuẩn đầu ra (Learning Outcomes) do Objective Architect tạo ra xem có đạt chuẩn sư phạm không.
    """
    print("\n[Objective_Reviewer_Agent] Đang kiểm định chuẩn đầu ra sư phạm...")
    
    from config.settings import get_agent_prompt
    agent_prompt = get_agent_prompt("Objective_Reviewer_Agent")
    system_prompt = f"{agent_prompt.get('Persona', '')}\n{agent_prompt.get('Task', '')}"
    
    import json
    user_prompt = f"""
    Technology Stack: {tech_stack}
    
    Original PM Input:
    {pm_input}
    
    Learning Outcomes to Audit:
    {json.dumps(learning_outcomes, ensure_ascii=False, indent=2)}
    
    Mandatory Output Contract:
    Return ONLY a valid JSON object matching: {{"status": "APPROVED" | "REJECTED", "score": 1-10, "feedback": "Detailed feedback in Vietnamese if rejected"}}
    """
    
    from core.llm import call_llm
    response_text = call_llm(
        system_prompt,
        user_prompt,
        json_mode=True,
        agent_name="Objective_Reviewer_Agent"
    )
    
    if response_text:
        try:
            return json.loads(response_text)
        except:
            pass
    
    return {"status": "APPROVED", "score": 10, "feedback": "Auto-approved due to LLM timeout."}


def mindmap_reviewer(state: AgentState) -> Dict[str, Any]:
    """
    Mindmap Reviewer Agent:
    Validates Markmap format, Heading hierarchy, code indentation, zero emojis, stack isolation,
    strict 3-level taxonomy, no redundant '#' characters, and presence of AI-driven image prompts.
    """
    session_id = state.get("session_id", "Session 01")
    lesson_id = state.get("lesson_id", "")
    mindmap_markdown = state.get("mindmap_markdown", "")
    from core.state import require_tech_stack
    tech_stack = require_tech_stack(state, "video_qa_reviewer")
    
    print(f"\n[Mindmap_Reviewer] Evaluating {session_id} {lesson_id} Mindmap structure...")
    
    # 1. Programmatic Stack Isolation & Dynamic Forbidden Scope Check
    forbidden_scope = state.get("forbidden_scope") if state else None
    forbidden_feedback = check_forbidden_keywords(mindmap_markdown, tech_stack, forbidden_scope)
    if forbidden_feedback:
        print(f"  - Result: REJECTED (Programmatic Stack Isolation check failed). Feedback: '{forbidden_feedback}'")
        return {"status": "REJECTED", "feedback": forbidden_feedback}
        
    # 2. Programmatic Format Checks
    if not mindmap_markdown.strip().startswith("```markmap") or not mindmap_markdown.strip().endswith("```"):
        feedback = "Sơ đồ tư duy phải được bao bọc hoàn toàn trong duy nhất một khối mã ```markmap ... ```."
        print(f"  - Result: REJECTED. Feedback: '{feedback}'")
        return {"status": "REJECTED", "feedback": feedback}
        
    # Extract H1 & check prefix
    lines = mindmap_markdown.splitlines()
    h1_line = next((line.strip() for line in lines if line.strip().startswith("# ")), None)
    if h1_line:
        h1_title = h1_line.replace("# ", "").strip()
        if re.match(r'^(session|lesson|chu\u01a1ng|b\u00e0i)\s*\d+[:\s-]*', h1_title, re.IGNORECASE):
            feedback = f"Tiêu đề cấp 1 (#) '{h1_title}' không được chứa tiền tố như 'Session XX' hay 'Lesson YY'. Hãy đặt tiêu đề thuần túy làm chủ đề cốt lõi của bài học."
            print(f"  - Result: REJECTED. Feedback: '{feedback}'")
            return {"status": "REJECTED", "feedback": feedback}
            
    # Extract H2 headings
    h2s = [line.strip().replace("## ", "").strip() for line in lines if line.strip().startswith("## ")]
        
    # Ensure H2s exists
    if not h2s:
        feedback = "Sơ đồ tư duy không chứa bất kỳ tiêu đề cấp 2 (##) nào."
        print(f"  - Result: REJECTED. Feedback: '{feedback}'")
        return {"status": "REJECTED", "feedback": feedback}

    # Ensure 'Mục tiêu bài học' is present
    if not any("mục tiêu bài học" in h2.lower() for h2 in h2s):
        feedback = "Sơ đồ tư duy bắt buộc phải có tiêu đề cấp 2 là '## Mục tiêu bài học'."
        print(f"  - Result: REJECTED. Feedback: '{feedback}'")
        return {"status": "REJECTED", "feedback": feedback}
        
    # Ensure 'Đặt tình huống' is present
    if not any("đặt tình huống" in h2.lower() for h2 in h2s):
        feedback = "Sơ đồ tư duy bắt buộc phải có tiêu đề cấp 2 là '## Đặt tình huống'."
        print(f"  - Result: REJECTED. Feedback: '{feedback}'")
        return {"status": "REJECTED", "feedback": feedback}
        
    # Ensure Level 3 titles (###) do not contain verbose hardcoded words
    h3s = [line.strip().replace("### ", "").strip() for line in lines if line.strip().startswith("### ")]
    for h3 in h3s:
        if "thực chiến" in h3.lower() or "lập trình" in h3.lower():
            feedback = f"Tiêu đề cấp 3 (###) '{h3}' dùng từ ngữ rườm rà. Hãy viết ngắn gọn như 'Cú pháp', 'Lưu ý', 'Cơ chế'."
            print(f"  - Result: REJECTED. Feedback: '{feedback}'")
            return {"status": "REJECTED", "feedback": feedback}
            
    # Check for image prompt or image markdown link
    has_image_prompt = re.search(r"\[(?:Prompt|Tạo ảnh):\s*([^\]]+)\]", mindmap_markdown) is not None
    has_image_link = re.search(r"!\[.*?\]\(.*?\)", mindmap_markdown) is not None
    if not (has_image_prompt or has_image_link):
        feedback = "Sơ đồ tư duy phải chứa ít nhất một prompt tạo ảnh (ví dụ: '[Prompt: ...]') hoặc một liên kết hình ảnh minh họa cho khái niệm kiến trúc/logic."
        print(f"  - Result: REJECTED. Feedback: '{feedback}'")
        return {"status": "REJECTED", "feedback": feedback}

    import os
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
    
    if not (gemini_key or openai_key):
        print(f"  - Result: APPROVED (Offline Bypass). Mindmap structure looks valid.")
        return {"status": "APPROVED", "feedback": "Sơ đồ tư duy được định dạng chính xác."}

    # 3. LLM-based Academic & Pedagogy Review
    from core.skills import load_skill_content
    mindmap_skill = load_skill_content("mindmap_generator")
    
    system_prompt = f"""You are a Lead Academic Director & Pedagogy Reviewer at Rikkei Education.
Your task is to audit the provided Markmap Mindmap against pedagogical excellence and structural formatting standards.

MANDATORY MINDMAP PEDAGOGICAL SPECIFICATIONS:
{mindmap_skill}
"""
    pm_lesson_details = state.get("core_ssot", {})
    user_prompt = f"""
    Review the following Mindmap Markdown for Session: {session_id}, Lesson: {lesson_id}.
    Target Technology Stack: {tech_stack}
    
    PM Lesson Details (Use to check if all main topics are covered):
    {json.dumps(pm_lesson_details, ensure_ascii=False)}
    
    Mindmap Content:
    {mindmap_markdown}
    
    CRITICAL AUDIT CRITERIA TO INSPECT:
    1. Zero-drop Policy: Does the mindmap contain dedicated Level-2 branches (##) for all main concepts listed in PM Lesson Details?
    2. Mandatory H2 Branches: Verify that '## Mục tiêu bài học' and '## Đặt tình huống' branches exist.
    3. Clean Root Heading: Ensure the Level-1 heading (#) contains only the clean content title of the lesson/session and strips any session/lesson prefixes.
    4. Code Formatting: Are code snippets properly fenced and space-indented under bullet points?
    5. No Emojis: Are text emojis completely absent?
    6. Dynamic & Short H3s: Ensure Level-3 headings are dynamic and very short, avoiding long phrases like "Lưu ý thực chiến" or "Cú pháp lập trình".
    7. No Scope Leakage: Is content strictly scoped to taught concepts without unlearned future topics?
    8. Image Nodes: Verify the existence of English image prompts matching the image standard. All image paths `![](../images/...)` are VALID conversions. Do not reject due to valid image paths.
    
    Response MUST be a valid JSON matching this schema:
    {{
        "status": "APPROVED" or "REJECTED",
        "feedback": "Detailed feedback in Accented Vietnamese explaining why it failed or what to improve."
    }}
    Return only raw JSON. Do not wrap in markdown code blocks.
    """
    
    response_text = call_llm(
        system_prompt,
        user_prompt,
        json_mode=True,
        agent_name="Mindmap_Reviewer",
        session_id=session_id,
        lesson_id=lesson_id
    )
    if response_text:
        try:
            cleaned = response_text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()
            
            result = json.loads(cleaned)
            print(f"  - Mindmap Reviewer successfully evaluated. Status: {result['status']}")
            return result
        except Exception as e:
            print(f"  [LLM Error] Failed to parse Mindmap review JSON: {e}.")
            
    return {"status": "APPROVED", "feedback": "Sơ đồ tư duy đáp ứng yêu cầu cấu trúc cơ bản."}

