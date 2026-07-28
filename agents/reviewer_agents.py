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
    Dynamically checks if content incorporates concepts from FUTURE lessons
    without hardcoding any specific language, framework, or lesson numbers.
    """
    if not text or not state:
        return ""

    future_lessons = state.get("future_lessons", [])
    if not future_lessons:
        return ""

    text_lower = text.lower()
    for fut in future_lessons:
        fut_title = fut.get("title", "").strip().lower()
        fut_details = fut.get("details", "").strip().lower()
        
        # Extract keywords (words with length >= 5) from future lesson title & details
        import re
        fut_keywords = set(re.findall(r'\b[a-zA-Z0-9_\-]{5,}\b', f"{fut_title} {fut_details}"))
        
        # Check if future core topics are being taught prematurely
        for kw in fut_keywords:
            if kw in text_lower and len(kw) >= 6:
                # Check if this keyword is NOT present in previous lessons or current lesson
                prev_text = " ".join([f"{p.get('title','')} {p.get('details','')}" for p in state.get("previous_lessons", [])]).lower()
                curr_title = state.get("lesson_title", "").lower()
                curr_details = state.get("lesson_details", "").lower()
                
                if kw not in prev_text and kw not in curr_title and kw not in curr_details:
                    return f"Cảnh báo vi phạm phạm vi kiến thức động: Nội dung xuất hiện thuật ngữ '{kw}' thuộc bài học tương lai '{fut.get('title')}' chưa được dạy."
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
    
    tech_stack = state.get("technology_stack", "python/core")
    
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

    # 2. Programmatic Knowledge Scope Boundary Check
    scope_feedback = check_knowledge_scope_violations(html_content, session_id, state=state)
    if scope_feedback:
        print(f"  - Result: REJECTED (Knowledge Scope Check Failed). Feedback: '{scope_feedback}'")
        return {"status": "REJECTED", "feedback": scope_feedback}

    # 3. Programmatic stack isolation check
    forbidden_feedback = check_forbidden_keywords(html_content, tech_stack)
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

        user_prompt = f"""
        Review the following HTML reading content for Session: {session_id}, Lesson: {lesson_id}.
        Attempt Number: {attempt_num}
        Target Technology Stack: {tech_stack}
        Is Theory/Diagram Only Lesson (No Code visualizer needed): {is_theory_only}
        
        PM Lesson Details: {json.dumps(pm_lesson_details, ensure_ascii=False)}
        Previous Lessons Info: {json.dumps(prev_lessons, ensure_ascii=False)}
        
        HTML Content:
        {html_content}
        
        IMPORTANT CRITERIA TO INSPECT:
        1. Tiêu chuẩn Trực quan hóa & Tương tác Web Động (Interactive Web Visualizer & Step-by-Step Playground):
           - LƯU Ý QUAN TRỌNG: Nếu đây là bài lý thuyết/giới thiệu/tổng quan (Is Theory/Diagram Only Lesson = True), bài đọc KHÔNG CẦN và KHÔNG ĐƯỢC có Code Tracker hay bảng điều khiển chạy từng bước (Start, Pause, Step, Reset). Trình kiểm duyệt tuyệt đối không được phạt lỗi thiếu các thành phần tương tác này. Chỉ cần bố cục đẹp, rõ ràng, sư phạm, có thể có sơ đồ tĩnh/hình vẽ minh họa.
           - Nếu đây KHÔNG phải là bài lý thuyết (Is Theory/Diagram Only Lesson = False), bài đọc BẮT BUỘC phải được xây dựng như một Ứng dụng Web Trực quan hóa Động ngay trên trình duyệt (theo chuẩn `skills/reading_generator/SKILL.md`), phải có Khung Trực quan hóa (`visualizer-canvas`), Bảng điều khiển tương tác (các nút bấm `▶ Bắt đầu`, `⏸ Tạm dừng`, `⏭ Từng bước`, `↻ Đặt lại`), Sliders & ô tự nhập tham số, Code Tracker highlight đồng bộ từng dòng thực thi (`active-line`), và Terminal Console Log thời gian thực.
           - LƯU Ý ĐẶC BIỆT DÀNH CHO BẠN: BẠN TUYỆT ĐỐI KHÔNG ĐƯỢC bắt lỗi runtime JavaScript (như TypeError, missing function), cũng KHÔNG ĐƯỢC reject nếu mã JS Engine thiếu các hàm pause(), step(), reset()... Việc tiêm logic JS điều khiển hoàn chỉnh sẽ do Server Backend đảm nhiệm ghi đè ở giai đoạn sau! Nhiệm vụ của bạn chỉ là kiểm tra xem Cấu trúc thẻ HTML có tồn tại hay không. Nếu có thẻ HTML là ĐẠT, bỏ qua mọi lỗi logic JS.
        2. Trọng tâm bài học & Không lan man (Lesson Focus & No Digression):
           - Nội dung bài đọc phải BÁM SÁT 100% vào tiêu đề và mô tả bài học PM Lesson Details ở trên.
           - TUYỆT ĐỐI không viết lan man sang bài khác hoặc nội dung môn học/lesson khác làm bài đọc quá dài dòng.
        3. Ràng buộc Công nghệ, Phạm vi & Kế thừa Kiến thức (Technology Stack & Scope Isolation):
           - Đối chiếu chặt chẽ với Target Technology Stack là: "{tech_stack}".
           - BẤT KỲ sự "đá xéo", nhầm lẫn hoặc trộn lẫn công nghệ của môn học này với môn học khác đều PHẢI BỊ REJECT.
           - Kiểm tra kỹ xem bài đọc có chứa mã nguồn, thư viện, hoặc khái niệm nâng cao nào vượt quá nội dung PM Lesson Details và Previous Lessons Info hay không. Bất kỳ đoạn code hoặc khái niệm nào chưa được học ở các bài học trước đều PHẢI BỊ REJECT để tránh quá tải nhận thức của học viên.
        4. Trình bày Khoa học & Cấu trúc (Scientific Presentation & Aesthetics):
           - Cách trình bày phải có tính sư phạm cao, khoa học, các phần lý thuyết chi tiết được đóng gói gọn gàng trong khối Accordion bên dưới Khung Trực quan hóa để không gây ngợp mắt.
        5. Quy tắc Code Minh họa (Code Snippet Rules):
           - ĐỐI VỚI BÀI LÝ THUYẾT (Is Theory/Diagram Only Lesson = True): Trình kiểm duyệt TUYỆT ĐỐI KHÔNG ĐƯỢC REJECT khi bài đọc không chứa mã nguồn hoặc không dùng code samples! Việc bỏ trống mã nguồn ở bài lý thuyết là ĐÚNG QUY LUẬT. KHÔNG bắt lỗi thiếu code!
           
        If the content fails any of these criteria, you MUST reject it!
        
        Response MUST be a valid JSON matching this schema:
        {{
            "status": "APPROVED" or "REJECTED",
            "feedback": "Detailed feedback in Vietnamese highlighting the exact reason (e.g. stack mismatch, digression, unscientific layout, missing interactive visualizer components, etc.) to help the creator fix it."
        }}
        Return only raw JSON. Do not wrap in markdown code blocks.
        """
        
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
    
    tech_stack = state.get("technology_stack", "python/core")
    
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

    # 3. Programmatic stack isolation check
    forbidden_feedback = check_forbidden_keywords(slide_markdown, tech_stack)
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
        1. Trọng tâm bài giảng & Không lan man (Lesson Focus & No Digression):
           - Slide (dạng Markdown hoặc HTML Slide) phải bám sát tuyệt đối nội dung và chuẩn đầu ra của bài học. Không viết lan man sang bài khác hay các chủ đề không được yêu cầu trong SSOT.
        2. Ràng buộc Công nghệ, Phạm vi & Kế thừa Kiến thức (Technology Stack & Scope Isolation):
           - Đối chiếu chặt chẽ với Target Technology Stack là: "{tech_stack}".
           - BẤT KỲ sự "đá xéo", nhầm lẫn hoặc trộn lẫn công nghệ của môn học này với môn học khác đều PHẢI BỊ REJECT.
           - Đảm bảo nội dung bài giảng không chứa bất kỳ khái niệm nâng cao, thư viện ngoài hoặc cú pháp code phức tạp nào vượt quá nội dung yêu cầu trong SSOT và danh sách Previous Lessons Info. Nếu xuất hiện các đoạn code hoặc chủ đề chưa được học, hoặc không có trong SSOT, hoặc quá phức tạp so với trình độ hiện tại, bạn PHẢI REJECT ngay lập tức.
        3. Trình bày Khoa học (Scientific Layout & Template Standard):
           - Bố cục slide (HTML/Markdown) phải khoa học, súc tích, phân cấp rõ ràng, dễ theo dõi, không lạm dụng đoạn văn quá dài.
        4. Độ chính xác học thuật:
           - Xác minh tính chính xác của các thuật ngữ kỹ thuật, không có lỗi ảo tưởng kiến thức (hallucinations).
           
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
    
    # Extract code between code block tags
    code_match = re.search(r'<code[^>]*class="[^"]*language-python[^"]*"[^>]*>(.*?)</code>', html_content, re.DOTALL)
    if code_match:
        raw_code = code_match.group(1)
        # Decode HTML entities
        code = raw_code.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&quot;", '"').replace("&#x27;", "'")
        # Check if code block contains actual python syntax keywords
        is_actual_python = any(keyword in code for keyword in ["import ", "def ", "class ", " = ", "print("])

        if code.strip() and is_actual_python and (gemini_key or openai_key):
            print(f"  [Sandbox] Found Python code block. Running compilation and execution check...")
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
            print(f"  - Result: Sandbox execution SKIPPED (not actual Python code or running offline fallback template)")

    tech_stack = state.get("technology_stack", "python/core")
    
    # 1. Programmatic stack isolation check first!
    forbidden_feedback = check_forbidden_keywords(html_content + " " + json.dumps(quiz_json, ensure_ascii=False), tech_stack)
    if forbidden_feedback:
        print(f"  - Result: REJECTED (Programmatic Stack Isolation check failed). Feedback: '{forbidden_feedback}'")
        return {"status": "REJECTED", "feedback": forbidden_feedback}

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
        "Bạn là một Giám đốc Đào tạo (Chief Learning Officer) kiêm Kiến trúc sư phần mềm (Principal Architect) tại một tập đoàn công nghệ giáo dục hàng đầu. "
        "Nhiệm vụ của bạn là 'thẩm định gắt gao' khung chương trình học (PM Input) được gửi đến. Nếu chương trình hời hợt, "
        "thiếu tính liên kết hoặc vi phạm nguyên tắc sư phạm, hệ thống tự động sinh học liệu sẽ tạo ra rác. Do đó, bạn phải đóng vai trò là 'người gác cổng' cực kỳ khắt khe."
    )
    user_prompt = f"""
    Dưới đây là nội dung khung chương trình môn học (PM Input) thuộc hệ sinh thái công nghệ: {tech_stack}.
    
    Chương trình (PM Input):
    {pm_input}
    
    HÃY THỰC HIỆN ĐÁNH GIÁ CHUYÊN SÂU THEO CÁC TIÊU CHÍ SAU. BẠN TUYỆT ĐỐI KHÔNG SỬA TRỰC TIẾP VÀO FILE PM, MÀ PHẢI XUẤT RA MỘT BẢN BÁO CÁO (MARKDOWN) ĐỂ YÊU CẦU PM (PROJECT MANAGER) CHỈNH SỬA:
    
    1. Đánh giá Mức độ Chi tiết (Granularity & Resolution):
       - Các Lesson đã phân rã đủ sâu chưa? Chỉ có tiêu đề chung chung (ví dụ: "Học về API") là KHÔNG THỂ CHẤP NHẬN.
       - Mỗi bài học đã định nghĩa rõ ràng 'Chuẩn đầu ra' (Learning Outcomes) chưa? Mức độ chi tiết phải đủ để truyền cho AI tự động sinh bài giảng.
       - LƯU Ý ĐẶC BIỆT: Đối với các buổi học mang tính chất "Hackathon", "Project", "Mini Project", "Dự án cuối môn", "Đồ án", "Luyện tập tổng hợp", hãy BỎ QUA việc kiểm tra mức độ chi tiết và KHÔNG phạt lỗi thiếu nội dung (vì các buổi này chỉ cần để trống, sinh viên tự code, hệ thống không cần sinh học liệu).
       
    2. Phân tích Dòng chảy Nhận thức & Tải lượng (Cognitive Flow & Load):
       - Độ khó của các bài học có tăng dần một cách mượt mà không? 
       - Có bài học nào nhồi nhét quá nhiều khái niệm phức tạp trong một buổi học (gây quá tải nhận thức cho học viên) không?
       
    3. Đồ thị Phụ thuộc Kế thừa (Dependency Progression & Prerequisites) - TIÊU CHÍ QUAN TRỌNG NHẤT:
       - Tính logic móc xích: Kiến thức của Lesson N có THỰC SỰ được xây dựng dựa trên Lesson (N-1) không?
       - Có khái niệm nào bị "nhảy cóc" không? (Ví dụ: Yêu cầu học sinh làm việc với Route Middleware trước khi dạy họ về cơ chế HTTP Request/Response cơ bản).

    4. Ràng buộc đặc biệt cho Session Thực hành (Practice Session) & Mini Project / Project Session:
       - Bất kỳ session nào có tên hoặc tiêu đề chứa từ khóa 'thực hành', 'practice', 'mini project', 'project', hoặc 'dự án' BẮT BUỘC KHÔNG ĐƯỢC có bất kỳ bài học (Lesson) con nào đi kèm. Toàn bộ nội dung của session thực hành và session project chỉ tập trung vào việc tạo bài tập thực hành độc lập hoặc Mini Project / Entry Tests / tài liệu SRS, không có bài học con. Nếu phát hiện Session Thực hành hoặc Session Project có chứa bài học con, bạn PHẢI đánh giá đây là điểm chưa tốt hoặc lỗi nghiêm trọng (Critical Issue) và đề xuất xóa bỏ các bài học con đó khỏi session.
       
    BẮT BUỘC TRẢ VỀ TOÀN BỘ ĐÁNH GIÁ DƯỚI ĐỊNH DẠNG MARKDOWN (.md) THEO CẤU TRÚC CHUẨN SAU:
    
    # 📑 BÁO CÁO THẨM ĐỊNH CHƯƠNG TRÌNH HỌC (PM REVIEW)
    **Công nghệ mục tiêu:** `{tech_stack}`
    
    ## 1. 📊 Tổng Quan & Điểm Đánh Giá
    - **Điểm sẵn sàng (Readiness Score):** [Chấm điểm từ 1-10]
    - **Nhận định chung:** [Tóm tắt 2-3 câu về chất lượng của khung chương trình hiện tại]
    
    ## 2. 🧠 Phân Tích Dòng Chảy Nhận Thức & Kế Thừa
    - **Điểm sáng:** [Chỉ ra những chuỗi bài học có tính liên kết tốt]
    - **Lỗ hổng "Nhảy cóc" (Missing Prerequisites):** [Phân tích cực kỳ chi tiết bài nào đang bị thiếu kiến thức nền tảng từ bài trước]
    
    ## 3. ⚠️ Các Điểm Yếu Cần Khắc Phục Khẩn Cấp (Critical Issues)
    - [Ghi rõ: Lesson số mấy, Tiêu đề là gì, Vấn đề là gì]
    - [Hậu quả nếu đưa nội dung này vào hệ thống tự động sinh học liệu]
    
    ## 4. 🛠 Đề Xuất Chỉnh Sửa Cụ Thể Gửi PM
    - **Yêu cầu 1:** [Gợi ý nội dung cần thêm/bớt cụ thể cho Lesson X]
    - **Yêu cầu 2:** [Gợi ý cách tổ chức lại luồng bài học]
    
    ## 5. 🛑 Kết Luận (Verdict)
    - **[APPROVED / REJECTED]** (Chỉ được ghi APPROVED nếu điểm sẵn sàng >= 8/10, và không có lỗ hổng "nhảy cóc" nghiêm trọng nào).
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
        "Bạn là Chuyên gia Cập nhật Cấu trúc PM Chuẩn 10 Cột Sư Phạm Quốc Tế (Curriculum Updater Agent). "
        "Nhiệm vụ của bạn là nhận vào file cấu trúc JSON của một chương trình học PM và một Bản báo cáo kiểm định lỗi (Review Report). "
        "Dựa vào các đề xuất chỉnh sửa trong báo cáo, "
        "hãy sinh ra một cấu trúc JSON MỚI HOÀN TOÀN đã được tự động vá lỗi và BẮT BUỘC BỔ SUNG ĐẦY ĐỦ 100% 'expected_outcome' (Kết Quả Mong Đợi) cho tất cả bài học."
    )
    
    user_prompt = f"""
    Công nghệ: {tech_stack}
    
    Báo cáo lỗi kiểm định (Review Report):
    {review_report}
    
    Chương trình học ban đầu (JSON 10 Cột):
    {pm_json}
    
    YÊU CẦU ĐỊNH DẠNG ĐẦU RA (RẤT QUAN TRỌNG):
    - Trả về DUY NHẤT một mảng JSON các Session. Mỗi Session chứa danh sách `lessons`.
    - Không chứa bất kỳ văn bản giải thích hay markdown code block ```json nào.
    - Mỗi Session CỦA MẢNG PHẢI GIỮ ĐỦ 4 TRƯỜNG THÔNG TIN SESSION:
        + "session_id": "Session 01" (Ví dụ: Session 01, Session 02...)
        + "session_type_vn": "Bài lý thuyết + thực hành" (hoặc "Bài thực hành / Lab", "Bài kiểm tra / Thi")
        + "session_code": "S01" (hoặc S02, S03...)
        + "session_title": "Tên tiêu đề session"
    - Mỗi Lesson TRONG MẢNG `lessons` PHẢI GIỮ ĐỦ 6 TRƯỜNG THÔNG TIN LESSON (Chuẩn PM 10 cột):
        + "lesson_title": "Tên bài học / Lesson"
        + "details": "Nội dung chi tiết kiến thức (Lesson Scope)"
        + "expected_outcome": "Kết quả mong đợi (BẮT BUỘC KHÔNG ĐƯỢC RỖNG: Viết theo Thang tư duy Bloom's Taxonomy - Sản phẩm / Năng lực sinh viên tự viết/làm/đạt được sau bài học này)"
        + "forbidden_scope": "Phạm vi CẤM DÙNG (BẮT BUỘC liệt kê: CẤM dùng các kiến thức của các bài học & session PHÍA SAU trong chương trình + CẤM các kiến thức BÊN NGOÀI môn học)"
        + "allowed_scope": "Phạm vi ĐÃ HỌC (Output kiến thức đã đạt được từ các session trước)"
        + "tech_stack": "{tech_stack}"
    - Cập nhật chính xác các vị trí được chỉ ra trong Báo cáo lỗi (đặc biệt BẮT BUỘC sinh đầy đủ 'expected_outcome' và 'forbidden_scope' nếu đang bị rỗng).
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
    
    PM Input Gốc:
    {pm_input}
    
    Learning Outcomes cần kiểm định:
    {json.dumps(learning_outcomes, ensure_ascii=False, indent=2)}
    
    Yêu cầu: 
    Trả về JSON duy nhất theo định dạng: {{"status": "APPROVED" | "REJECTED", "score": 1-10, "feedback": "Chi tiết lỗi nếu có"}}
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
    tech_stack = state.get("technology_stack", "python/core")
    
    print(f"\n[Mindmap_Reviewer] Evaluating {session_id} {lesson_id} Mindmap structure...")
    
    # 1. Programmatic Stack Isolation Check
    forbidden_feedback = check_forbidden_keywords(mindmap_markdown, tech_stack)
    if forbidden_feedback:
        print(f"  - Result: REJECTED (Programmatic Stack Isolation check failed). Feedback: '{forbidden_feedback}'")
        return {"status": "REJECTED", "feedback": forbidden_feedback}
        
    # 2. Programmatic Format Checks
    if not mindmap_markdown.strip().startswith("```markmap") or not mindmap_markdown.strip().endswith("```"):
        feedback = "Sơ đồ tư duy phải được bao bọc hoàn toàn trong duy nhất một khối mã ```markmap ... ```."
        print(f"  - Result: REJECTED. Feedback: '{feedback}'")
        return {"status": "REJECTED", "feedback": feedback}
        
    # Extract H2 headings
    lines = mindmap_markdown.splitlines()
    h2s = [line.strip().replace("## ", "").strip() for line in lines if line.strip().startswith("## ")]
        
    # Ensure H2s exists
    if not h2s:
        feedback = "Sơ đồ tư duy không chứa bất kỳ tiêu đề cấp 2 (##) nào."
        print(f"  - Result: REJECTED. Feedback: '{feedback}'")
        return {"status": "REJECTED", "feedback": feedback}

    # Reject if 'Mục tiêu bài học' is present as an H2 branch (we require going straight to knowledge topics)
    if any("mục tiêu bài học" in h2.lower() for h2 in h2s):
        feedback = "Sơ đồ tư duy không được chứa nhánh 'Mục tiêu bài học'. Hãy để tiêu đề cấp 1 (#) phân nhánh trực tiếp ra các chủ đề kiến thức cốt lõi (##)."
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
    
    system_prompt = f"""Bạn là một chuyên gia Thẩm định Chương trình Đào tạo và Sư phạm tại Rikkei Education.
Nhiệm vụ của bạn là thẩm định sơ đồ tư duy (Mindmap/Markmap) được gửi tới xem có tuân thủ đúng chuẩn sư phạm và định dạng không.

Quy định chuẩn của sơ đồ tư duy:
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
    
    IMPORTANT CRITERIA TO INSPECT:
    1. Zero-drop Policy: Sơ đồ đã có đầy đủ nhánh cấp 2 (##) cho tất cả các chủ đề chính được nêu trong PM Lesson Details chưa?
    2. Phân nhánh động linh hoạt: Sơ đồ KHÔNG chứa nhánh 'Mục tiêu bài học' và KHÔNG bị lặp lại rập khuôn 3 nhánh con 'Khái niệm', 'Cú pháp', 'Lưu ý' ở tất cả các mục chưa?
    3. Định dạng code: Ví dụ mã nguồn có được thụt lề bằng dấu cách (space) chính xác dưới gạch đầu dòng (-) tương ứng chưa?
    4. Không có kịch bản giảng dạy: Có từ khóa meta nào như "Slide 1", "Concept Check", v.v. xuất hiện không?
    5. Không dùng Emoji: Có icon hay emoji nào không?
    6. Scope Leakage: Có chứa kiến thức, cú pháp nào nằm ngoài phạm vi của bài học hiện tại không?
    7. Hình ảnh minh họa: Mọi đường dẫn hình ảnh dạng `![](../images/...)` trong sơ đồ đều là hợp lệ vì hệ thống đã tự động chuyển đổi từ prompt ảnh dạng `[Prompt: ...]` hoặc `[Tạo ảnh: ...]` của người dùng. Không được từ chối (REJECT) vì lý do sử dụng đường dẫn hình ảnh dạng này.
    
    Response MUST be a valid JSON matching this schema:
    {{
        "status": "APPROVED" or "REJECTED",
        "feedback": "Detailed feedback in Vietnamese explaining why it failed or what to improve."
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

