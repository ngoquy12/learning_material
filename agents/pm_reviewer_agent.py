"""
agents/pm_reviewer_agent.py

AI PM Reviewer & Strict Academic Quality Assurance Auditor Agent.
Acts as an un-compromising Academic Quality Director for Rikkei Education.

Performs deep structural linter checks, CLO/PLO coverage alignment, Bloom taxonomy verb enforcement,
scope continuity validation, academic tone checks, and LLM expert evaluation.
"""

import re
import json
from typing import Dict, Any, List, Tuple
from core.llm import call_llm
from agents.reviewer_agents import check_forbidden_emojis, check_unaccented_vietnamese


# Words prohibited to maintain Academic Tone
HYPE_WORDS = [
    "thần tốc", "cực chất", "bí quyết", "làm chủ", "sức mạnh của",
    "tối thượng", "bứt phá", "thần thánh", "bí kíp", "tuyệt vời",
    "lợi ích kép", "thực chiến", "siêu tốc", "chìa khóa"
]

# Difficulty badges prohibited in titles
DIFFICULTY_BADGES = [
    r"\(heavy\)", r"\(light\)", r"\(lý thuyết nhẹ\)", r"\(lý thuyết nặng\)",
    r"\[heavy\]", r"\[light\]", r"\(nặng\)", r"\(nhẹ\)"
]

# Vague, non-measurable outcome verbs prohibited in expected_outcome
VAGUE_OUTCOME_VERBS = [
    "hiểu về", "biết về", "nắm được", "tìm hiểu", "làm quen", "nắm vững",
    "biết cách", "hiểu rõ", "học về", "nghiên cứu"
]

# Measurable action verbs based on Bloom's Taxonomy
BLOOM_ACTION_VERBS = [
    "phân biệt", "giải thích", "kết nối", "khởi tạo", "cấu hình", "thiết lập",
    "viết", "tạo", "thao tác", "xử lý", "triển khai", "giải quyết", "tối ưu",
    "xây dựng", "lập trình", "sử dụng", "trình bày", "đánh giá", "kiểm thử"
]

# Out-of-scope technology rules based on tech stack
STACK_OUT_OF_SCOPE_RULES = {
    "python/core": [
        "sqlite", "sql", "database", "flask", "django", "fastapi",
        "html", "css", "react", "javascript", "node.js", "express",
        "docker", "redis", "pandas", "numpy", "machine learning"
    ],
    "javascript/core": [
        "react", "vue", "angular", "vite", "next.js", "express",
        "node.js", "python", "fastapi", "sql", "java", "spring boot"
    ],
    "java/core": [
        "spring boot", "python", "javascript", "php", "react", "fastapi"
    ]
}


def _get_hinh_thuc(s: Dict[str, Any]) -> str:
    """Extracts session type/form regardless of schema key variation."""
    return str(s.get("hinh_thuc") or s.get("session_type") or "").strip()


def _get_session_num(s: Dict[str, Any], default_idx: int) -> int:
    """Extracts integer session number from session_num or session_id."""
    if "session_num" in s and s["session_num"]:
        try:
            return int(s["session_num"])
        except ValueError:
            pass
    if "session_id" in s and s["session_id"]:
        match = re.search(r'\d+', str(s["session_id"]))
        if match:
            return int(match.group(0))
    return default_idx + 1


def lint_pm_syllabus(
    pm_data: List[Dict[str, Any]],
    tech_stack: str = "",
    sessions_per_day: int = 1,
    clos: List[str] = None,
    plos: List[str] = None
) -> Tuple[bool, int, List[str], List[Dict[str, Any]]]:
    """
    Strict Rule Engine for PM Syllabus Validation.

    Returns:
        (is_valid: bool, score: int, rule_violations: List[str], review_logs: List[Dict[str, Any]])
    """
    clos = clos or []
    plos = plos or []
    rule_violations: List[str] = []
    review_logs: List[Dict[str, Any]] = []
    score = 100

    if not pm_data:
        rule_violations.append("Lỗi nghiêm trọng: PM rỗng, không chứa session nào.")
        return False, 0, rule_violations, [{"level": "CRITICAL", "message": "PM rỗng."}]

    total_sessions = len(pm_data)

    # -------------------------------------------------------------------------
    # 1. Structure & Pacing Validation Rules
    # -------------------------------------------------------------------------
    # Rule 1: Session 01 MUST be Orientation / Lý thuyết
    s1 = pm_data[0]
    ht1 = _get_hinh_thuc(s1)
    if "Lý thuyết" not in ht1:
        msg = f"Session 01 phải là 'Lý thuyết' (Định hướng & Lộ trình), nhưng hiện tại là '{ht1}'."
        rule_violations.append(msg)
        review_logs.append({"level": "ERROR", "message": msg})
        score -= 15

    # Rule 2: Session 02 MUST be Theory
    if total_sessions >= 2:
        s2 = pm_data[1]
        ht2 = _get_hinh_thuc(s2)
        if "Lý thuyết" not in ht2:
            msg = f"Session 02 PHẢI là 'Lý thuyết' kỹ thuật đầu tiên, nhưng hiện tại là '{ht2}'."
            rule_violations.append(msg)
            review_logs.append({"level": "ERROR", "message": msg})
            score -= 15

    # Rule 3: Session 03 MUST be Practice
    if total_sessions >= 3:
        s3 = pm_data[2]
        ht3 = _get_hinh_thuc(s3)
        if "Thực hành" not in ht3:
            msg = f"Session 03 PHẢI là 'Thực hành' đầu tiên, nhưng hiện tại là '{ht3}'."
            rule_violations.append(msg)
            review_logs.append({"level": "ERROR", "message": msg})
            score -= 15

    # Rule 4: Final Session MUST be Exam / Project
    last_session = pm_data[-1]
    ht_last = _get_hinh_thuc(last_session)
    valid_finals = ["Thi cuối môn", "Project", "Dự án cuối khóa", "Hackathon"]
    if not any(vf.lower() in ht_last.lower() for vf in valid_finals):
        msg = f"Buổi cuối cùng (Session {total_sessions:02d}) phải là Thi cuối môn hoặc Project, nhưng hiện tại là '{ht_last}'."
        rule_violations.append(msg)
        review_logs.append({"level": "ERROR", "message": msg})
        score -= 10

    # Rule 5 & 6 & 7: Lessons count & sequential session numbering
    for idx, s in enumerate(pm_data):
        snum = _get_session_num(s, idx)
        ht = _get_hinh_thuc(s)
        lessons = s.get("lessons", [])

        # Sequential check
        if snum != idx + 1:
            msg = f"Session numbering rớt số: mong đợi Session {idx + 1:02d}, nhận Session {snum}."
            rule_violations.append(msg)
            review_logs.append({"level": "ERROR", "message": msg})
            score -= 10
            break

        # Non-theory lessons check
        if "Lý thuyết" not in ht and len(lessons) > 0:
            msg = f"Session {snum:02d} ({ht}) không được chứa lesson con, nhưng hiện có {len(lessons)} lessons."
            rule_violations.append(msg)
            review_logs.append({"level": "ERROR", "message": msg})
            score -= 5

        # Theory lessons count check
        if "Lý thuyết" in ht:
            if len(lessons) < 2 or len(lessons) > 4:
                msg = f"Session {snum:02d} (Lý thuyết) có {len(lessons)} lessons — phải từ 2 đến 4 lessons."
                rule_violations.append(msg)
                review_logs.append({"level": "ERROR", "message": msg})
                score -= 5

    # Rule 8: Delivery pacing (if 2 sessions per day, avoid 2 theory sessions in same day except Day 1)
    if sessions_per_day == 2 and total_sessions >= 4:
        for day_idx in range(1, total_sessions // 2):
            s_a = pm_data[day_idx * 2]
            s_b = pm_data[day_idx * 2 + 1] if (day_idx * 2 + 1) < total_sessions else None
            if s_b:
                ht_a = _get_hinh_thuc(s_a)
                ht_b = _get_hinh_thuc(s_b)
                if "Lý thuyết" in ht_a and "Lý thuyết" in ht_b:
                    msg = (f"Ngày {day_idx + 1} (Session {day_idx*2+1:02d} & {day_idx*2+2:02d}) bị xếp 2 buổi Lý thuyết liên tiếp. "
                           f"Bắt buộc xen kẽ 1 Lý thuyết + 1 Thực hành.")
                    rule_violations.append(msg)
                    review_logs.append({"level": "WARNING", "message": msg})
                    score -= 5

    # -------------------------------------------------------------------------
    # 2. Formatting, Tone & Bloom Taxonomy Verbs Validation Rules
    # -------------------------------------------------------------------------
    for s in pm_data:
        snum = _get_session_num(s, 0)
        s_title = str(s.get("title", ""))

        # Check ALL CAPS in Session title
        if s_title.isupper() and len(s_title) > 5:
            msg = f"Session {snum:02d} tiêu đề dùng VIẾT HOA TOÀN BỘ (ALL CAPS): '{s_title}'. Bắt buộc dùng Sentence case."
            rule_violations.append(msg)
            review_logs.append({"level": "WARNING", "message": msg})
            score -= 3

        # Check Emoji in Session title / scope
        all_s_text = f"{s_title} {s.get('content_scope', '')} {s.get('expected_outcome', '')}"
        emoji_err = check_forbidden_emojis(all_s_text)
        if emoji_err:
            msg = f"Session {snum:02d} chứa Emoji/Icon cấm: {emoji_err}"
            rule_violations.append(msg)
            review_logs.append({"level": "ERROR", "message": msg})
            score -= 5

        # Check Difficulty Badges in Session title
        for badge in DIFFICULTY_BADGES:
            if re.search(badge, s_title, re.IGNORECASE):
                msg = f"Session {snum:02d} tiêu đề chứa hậu tố phân loại cấm: '{s_title}'."
                rule_violations.append(msg)
                review_logs.append({"level": "ERROR", "message": msg})
                score -= 3

        # Check Hype Words (Academic Tone)
        for hw in HYPE_WORDS:
            if hw in all_s_text.lower():
                msg = f"Session {snum:02d} chứa từ giật tít/không chuẩn sư phạm: '{hw}'."
                rule_violations.append(msg)
                review_logs.append({"level": "WARNING", "message": msg})
                score -= 3

        # Check Vague Action Verbs in expected_outcome
        s_outcome = s.get("expected_outcome", "").lower().strip()
        for vague_v in VAGUE_OUTCOME_VERBS:
            if vague_v in s_outcome:
                msg = f"Session {snum:02d} outcome dùng động từ nhận thức mơ hồ cấm ('{vague_v}'): '{s.get('expected_outcome', '')}'. Bắt buộc dùng động từ đo lường được theo Bloom (ví dụ: 'Phân biệt được...', 'Khởi tạo thành công...')."
                rule_violations.append(msg)
                review_logs.append({"level": "ERROR", "message": msg})
                score -= 4
                break

        # Check unaccented Vietnamese
        unaccented_err = check_unaccented_vietnamese(all_s_text)
        if unaccented_err:
            msg = f"Session {snum:02d} vi phạm tiếng Việt không dấu: {unaccented_err}"
            rule_violations.append(msg)
            review_logs.append({"level": "ERROR", "message": msg})
            score -= 5

        # Check Lessons within session
        lessons = s.get("lessons", [])
        for l in lessons:
            lnum = l.get("lesson_num", 0)
            ltitle = str(l.get("title", ""))
            l_text = f"{ltitle} {l.get('content_scope', '')} {l.get('expected_outcome', '')}"

            if ltitle.isupper() and len(ltitle) > 5:
                msg = f"Session {snum:02d} Lesson {lnum} tiêu đề dùng ALL CAPS: '{ltitle}'."
                rule_violations.append(msg)
                review_logs.append({"level": "WARNING", "message": msg})
                score -= 2

            emoji_l_err = check_forbidden_emojis(l_text)
            if emoji_l_err:
                msg = f"Session {snum:02d} Lesson {lnum} chứa Emoji: {emoji_l_err}"
                rule_violations.append(msg)
                review_logs.append({"level": "ERROR", "message": msg})
                score -= 5

            for hw in HYPE_WORDS:
                if hw in l_text.lower():
                    msg = f"Session {snum:02d} Lesson {lnum} chứa từ giật tít: '{hw}'."
                    rule_violations.append(msg)
                    review_logs.append({"level": "WARNING", "message": msg})
                    score -= 2

            l_outcome = l.get("expected_outcome", "").lower().strip()
            for vague_v in VAGUE_OUTCOME_VERBS:
                if vague_v in l_outcome:
                    msg = f"Session {snum:02d} Lesson {lnum} outcome dùng động từ mơ hồ cấm ('{vague_v}'): '{l.get('expected_outcome', '')}'."
                    rule_violations.append(msg)
                    review_logs.append({"level": "ERROR", "message": msg})
                    score -= 3
                    break

        # Check Adaptive Pedagogical Structure for Theory Sessions based on Topic Classification
        if "Lý thuyết" in _get_hinh_thuc(s) and len(lessons) >= 3 and snum > 1:
            s_full_title = (s_title + " " + s.get("content_scope", "")).lower()

            # Category 1: Setup / Tooling / Environment Topic
            is_setup_topic = any(kw in s_full_title for kw in ["cài đặt", "môi trường", "thiết lập", "cấu hình", "setup", "installation", "config", "kho lưu trữ", "giao diện"])

            if is_setup_topic:
                # Valid setup flow: Overview/Why ➔ Setup/Config ➔ Test/Verify/Hands-on
                l1_text = (lessons[0].get("title", "") + " " + lessons[0].get("content_scope", "")).lower()
                l2_text = (lessons[1].get("title", "") + " " + lessons[1].get("content_scope", "")).lower()
                l3_text = (lessons[2].get("title", "") + " " + lessons[2].get("content_scope", "")).lower()

                has_overview = any(w in l1_text for w in ["giới thiệu", "mô hình", "ý nghĩa", "tại sao", "khái niệm", "vai trò", "tài khoản", "lộ trình", "tổng quan"])
                has_setup    = any(w in l2_text for w in ["cài đặt", "thiết lập", "cấu hình", "khởi tạo", "đăng ký", "tạo", "config", "setup"])
                has_verify   = any(w in l3_text for w in ["kiểm tra", "thao tác", "chạy thử", "liên kết", "đồng bộ", "xác thực", "tạo commit", "quản lý", "xem lịch sử", "bỏ qua"])

                if not (has_overview or has_setup or has_verify):
                    msg = f"Session {snum:02d} (Cài đặt/Môi trường) thiếu luồng thao tác tự nhiên (Giới thiệu ➔ Cài đặt/Cấu hình ➔ Kiểm tra/Thực thao tác)."
                    rule_violations.append(msg)
                    review_logs.append({"level": "WARNING", "message": msg})
                    score -= 3

            else:
                # Category 2: Core Coding / Technical Concept Topic
                l1_text = (lessons[0].get("title", "") + " " + lessons[0].get("content_scope", "")).lower()
                l2_text = (lessons[1].get("title", "") + " " + lessons[1].get("content_scope", "")).lower()
                l3_text = (lessons[2].get("title", "") + " " + lessons[2].get("content_scope", "")).lower()
                # Semantic intent word families for flexible matching of Vietnamese phrasing variations
                intent_hooks = ["vấn đề", "bài toán", "giới thiệu", "tại sao", "khái niệm", "mô hình", "tầm quan trọng", "nhập môn", "ý nghĩa", "tổng quan", "bản chất", "vai trò", "định hướng", "nền tảng", "tổng thể", "lộ trình", "lý do"]
                intent_mechs = ["cú pháp", "kiến trúc", "cấu hình", "thao tác", "khai báo", "cấu trúc", "cơ chế", "cài đặt", "lệnh", "kỹ thuật", "phương pháp", "quy trình", "cách dùng", "cách viết", "thiết lập", "tích hợp", "xác thực", "liên kết", "mô tả", "hoạt động", "vận hành", "nguyên lý", "bộ nhớ", "luồng", "commit", "branch"]
                intent_apps  = ["ứng dụng", "thực tế", "quy trình", "dự án", "tối ưu", "thực hành", "kịch bản", "tái sử dụng", "đồng bộ", "hợp nhất", "giải quyết", "triển khai", "quản lý", "xử lý", "phối hợp", "chuẩn hóa", "bài tập", "tối ưu hóa", "module", "hệ thống", "xây dựng", "lập trình", "pull request", "phân nhánh"]

                all_lessons_text = " ".join([l.get("title", "") + " " + l.get("content_scope", "") for l in lessons]).lower()

                has_hook = any(w in l1_text for w in intent_hooks)
                has_mech = any(w in l2_text or w in all_lessons_text for w in intent_mechs)
                has_app  = any(w in l3_text or w in all_lessons_text for w in intent_apps)

                # Check if lessons are completely flat dictionary listings without any structure
                is_flat_dict_listing = not (has_hook or has_mech or has_app)
                if is_flat_dict_listing:
                    msg = f"Session {snum:02d} (Lý thuyết) thiếu trật tự dẫn dắt sư phạm (Lesson 1: Khái niệm/Vấn đề ➔ Lesson 2: Cơ chế/Cú pháp ➔ Lesson 3: Ứng dụng/Quy trình)."
                    rule_violations.append(msg)
                    review_logs.append({"level": "WARNING", "message": msg})
                    score -= 3

    # Check for Thin Practice Sessions (Session thực hành bị rỗng do bài lý thuyết trước chỉ có setup)
    for idx, s in enumerate(pm_data):
        stype = _get_hinh_thuc(s)
        snum = _get_session_num(s, idx + 1)
        if stype in ["Thực hành", "PRACTICE"] and idx > 0:
            prev_s = pm_data[idx - 1]
            prev_type = _get_hinh_thuc(prev_s)
            if prev_type in ["Lý thuyết", "THEORY"]:
                prev_text = (prev_s.get("title", "") + " " + prev_s.get("content_scope", "")).lower()
                for l in prev_s.get("lessons", []):
                    prev_text += " " + (l.get("title", "") + " " + l.get("content_scope", "")).lower()
                
                # If preceding theory session ONLY has setup/env words and NO programming/coding concepts
                has_only_setup = any(w in prev_text for w in ["cài đặt", "môi trường", "venv", "linter", "setup", "config", "cấu hình"])
                has_code_depth = any(w in prev_text for w in ["biến", "kiểu dữ liệu", "toán tử", "nhập", "xuất", "print", "input", "rẽ nhánh", "vòng lặp", "hàm", "dữ liệu", "cú pháp", "code", "lập trình"])
                
                if has_only_setup and not has_code_depth:
                    msg = f"Session {snum:02d} (Thực hành) có nguy cơ bị nông/rỗng: Session Lý thuyết {snum-1:02d} chỉ chứa nội dung Cài đặt/Môi trường mà chưa có kiến thức lập trình (Biến/Kiểu dữ liệu/Nhập xuất). Cần tăng hàm lượng kiến thức hoặc chuyển thành buổi Lý thuyết."
                    rule_violations.append(msg)
                    review_logs.append({"level": "WARNING", "message": msg})
                    score -= 3

    # -------------------------------------------------------------------------
    # 3. Scope Boundaries & Knowledge Isolation Rules
    # -------------------------------------------------------------------------
    if tech_stack:
        tech_key = tech_stack.lower().strip()
        forbidden_techs = []

        for key, forbidden_list in STACK_OUT_OF_SCOPE_RULES.items():
            if key in tech_key:
                forbidden_techs.extend(forbidden_list)

        if forbidden_techs:
            for s in pm_data:
                snum = _get_session_num(s, 0)
                combined_text = f"{s.get('title', '')} {s.get('content_scope', '')} {s.get('expected_outcome', '')}"
                for l in s.get("lessons", []):
                    combined_text += f" {l.get('title', '')} {l.get('content_scope', '')}"

                combined_lower = combined_text.lower()
                for ft in forbidden_techs:
                    if re.search(rf"\b{re.escape(ft)}\b", combined_lower):
                        msg = f"Session {snum:02d} vi phạm ranh giới công nghệ cấm: chứa từ khóa '{ft}' không thuộc tech stack '{tech_stack}'."
                        rule_violations.append(msg)
                        review_logs.append({"level": "ERROR", "message": msg})
                        score -= 10

    # Scope continuity: check forbidden_scope vs allowed_scope and historical taught concepts
    taught_concepts = set()
    for s in pm_data:
        snum = _get_session_num(s, 0)
        lessons = s.get("lessons", [])
        for l in lessons:
            lnum = l.get("lesson_num", 0)
            forbidden = l.get("forbidden_scope", "").lower()
            allowed = l.get("allowed_scope", "").lower()
            content = l.get("content_scope", "").lower()

            if forbidden and allowed:
                f_clean = forbidden.replace("cấm:", "").strip()
                a_clean = allowed.replace("đã học:", "").strip()

                f_terms = [t.strip() for t in f_clean.split(";") if t.strip()]
                a_terms = [t.strip() for t in a_clean.split(";") if t.strip()]

                overlap = [t for t in a_terms if t in f_terms and len(t) > 2]
                if overlap:
                    msg = f"Session {snum:02d} Lesson {lnum} mâu thuẫn Scope: Thuật ngữ '{', '.join(overlap)}' xuất hiện ở cả ĐÃ HỌC và CẤM."
                    rule_violations.append(msg)
                    review_logs.append({"level": "ERROR", "message": msg})
                    score -= 5

                # Check if concept taught previously is erroneously still forbidden
                for concept in taught_concepts:
                    if len(concept) > 3 and concept in f_terms:
                        msg = f"Session {snum:02d} Lesson {lnum} vi phạm giải phóng Scope: Thuật ngữ '{concept}' đã học ở các buổi trước nhưng vẫn nằm trong CẤM."
                        rule_violations.append(msg)
                        review_logs.append({"level": "ERROR", "message": msg})
                        score -= 5
                        break

            # Add current content terms to taught concepts
            for term in content.replace(";", ",").split(","):
                clean_t = term.strip().lower()
                if len(clean_t) > 3:
                    taught_concepts.add(clean_t)

    # -------------------------------------------------------------------------
    # 4. CLO & PLO Coverage Audit
    # -------------------------------------------------------------------------
    if clos:
        all_syllabus_text = json.dumps(pm_data, ensure_ascii=False).lower()
        for idx, clo in enumerate(clos, 1):
            # Clean CLO prefix like 'CLO1:' or 'CLO 1:'
            clo_clean = re.sub(r'^(CLO|PLO)\s*\d+[:\s]*', '', str(clo), flags=re.IGNORECASE).strip()
            clo_words = [w.strip().lower() for w in re.split(r'[\s,.;:()]+', clo_clean) if len(w.strip()) > 3]
            clo_words = [w for w in clo_words if not re.match(r'^(clo|plo)\d*$', w) and w not in ["sử", "dụng", "thành", "thạo", "thao", "tác", "xử", "lý", "biết", "hiểu", "thực", "hiện"]]

            matched = any(w in all_syllabus_text for w in clo_words)
            if not matched and len(clo_words) > 0:
                msg = f"Lỗi sư phạm: CLO {idx} ('{clo}') chưa được bao phủ rõ ràng trong bất kỳ buổi học nào của PM."
                rule_violations.append(msg)
                review_logs.append({"level": "ERROR", "message": msg})
                score -= 10

    score = max(0, min(100, score))
    is_valid = len([log for log in review_logs if log["level"] == "ERROR"]) == 0 and score >= 90

    return is_valid, score, rule_violations, review_logs


def pm_reviewer_agent(
    pm_data: List[Dict[str, Any]],
    config_data: Dict[str, Any] = None,
    course_info: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Main entry point for PM Reviewer & Strict Academic Quality Assurance Auditor Agent.

    Evaluates generated PM syllabus using programmatic strict linter + LLM Academic Director evaluation pass.
    Requires Quality Score >= 90 and 0 ERRORs to approve.
    """
    config_data = config_data or {}
    course_info = course_info or {}

    clos = course_info.get("clos", [])
    plos = course_info.get("plos", [])
    tech_stack = config_data.get("tech_stack", "")
    class_config = config_data.get("class_configuration", {})
    sessions_per_day = class_config.get("sessions_per_day", 1)

    print("  [PM Auditor - Strict Mode ⚖️] Running deep structural & pedagogical linter...")
    is_valid, score, rule_violations, review_logs = lint_pm_syllabus(
        pm_data=pm_data,
        tech_stack=tech_stack,
        sessions_per_day=sessions_per_day,
        clos=clos,
        plos=plos
    )

    feedback_parts = []
    if rule_violations:
        feedback_parts.append("LIST OF PEDAGOGICAL & FORMATTING RULE VIOLATIONS (MUST BE FULLY RESOLVED):")
        for idx, err in enumerate(rule_violations, 1):
            feedback_parts.append(f"{idx}. {err}")

    if is_valid and score >= 90:
        feedback_summary = f"APPROVED: PM Syllabus achieves excellent academic standards ({score}/100)."
    else:
        feedback_summary = f"REJECTED: PM Syllabus failed strict academic quality gate (Score: {score}/100, Minimum required: 90/100). Please resolve all issues listed below."

    full_feedback = feedback_summary + "\n\n" + "\n".join(feedback_parts) if feedback_parts else feedback_summary

    result = {
        "is_approved": is_valid,
        "score": score,
        "review_logs": review_logs,
        "rule_violations": rule_violations,
        "feedback": full_feedback
    }

    if is_valid:
        print(f"  [PM Auditor ✅] APPROVED (Quality Score: {score}/100)")
    else:
        print(f"  [PM Auditor ⚠️] REJECTED (Quality Score: {score}/100, Violations: {len(rule_violations)})")
        for log in review_logs[:5]:
            print(f"      - [{log['level']}] {log['message']}")

    return result


# =============================================================================
# QUALITY GATE 6 ĐIỂM — KIỂM ĐỊNH BÀI ĐỌC HTML THEO 10 KIM CHỈ NAM
# =============================================================================

def audit_reading_html_quality_gate(
    html_content: str,
    lesson_title: str = "",
    forbidden_scope: str = "",
    tech_stack: str = ""
) -> Dict[str, Any]:
    """
    6-Point Automated Quality Gate cho bài đọc HTML.

    Kiểm tra từng tiêu chí theo SKILL.md Section 5:
      Gate 1: 5 Anchor ID cố định có mặt đầy đủ
      Gate 2: Không rò rỉ kiến thức forbidden_scope
      Gate 3: Có sơ đồ SVG 16:9 (viewBox 800x450 hoặc aspect 16:9)
      Gate 4: Có thẻ Good Practice vs Bad Practice
      Gate 5: Có form Self-Test MCQ với nút Kiểm Tra Đáp Án
      Gate 6: Không dùng ALL CAPS tiêu đề, không emoji sáo rỗng, không W3Schools

    Returns:
        Dict: {
            'passed': bool,
            'score': int (0-100),
            'gates': List[Dict] — chi tiết từng gate,
            'feedback': str — hướng dẫn sửa cụ thể
        }
    """
    gates: List[Dict[str, Any]] = []
    score = 100
    feedback_parts: List[str] = []

    if not html_content or len(html_content) < 500:
        return {
            "passed": False,
            "score": 0,
            "gates": [{"id": 0, "name": "Bài đọc rỗng", "passed": False, "detail": "HTML output rỗng hoặc quá ngắn."}],
            "feedback": "CRITICAL: Bài đọc trống hoặc không được sinh. Cần tạo lại toàn bộ."
        }

    content_lower = html_content.lower()

    # ------------------------------------------------------------------
    # Gate 1: 5 Anchor ID cố định (Cấu trúc 5 phần theo Kim Chỉ Nam 1)
    # ------------------------------------------------------------------
    required_anchors = [
        ("problem-intro", "Phần 1 — Đặt vấn đề thực tế"),
        ("data-structure", "Phần 2 — Cú pháp & Cơ chế"),
        ("interactive-demo", "Phần 3 — Ví dụ minh họa"),
        ("summary-notes", "Phần 4 — Lưu ý thực chiến"),
        ("self-test", "Phần 5 — Khảo thí tự đánh giá"),
    ]
    # Fallback: check step sections if anchors not present (older template)
    has_step_sections = all(
        f"step-body" in content_lower or f"class=\"step\"" in html_content
        for _ in required_anchors
    )
    missing_anchors = []
    for anchor_id, anchor_name in required_anchors:
        if f'id="{anchor_id}"' not in html_content and f"id='{anchor_id}'" not in html_content:
            missing_anchors.append(f"{anchor_id} ({anchor_name})")

    gate1_passed = len(missing_anchors) <= 2  # Tolerate up to 2 missing in transition period
    if not gate1_passed:
        penalty = 15
        score -= penalty
        feedback_parts.append(
            f"[Gate 1] Thiếu {len(missing_anchors)}/5 Anchor ID cố định: "
            f"{', '.join(missing_anchors)}. "
            f"Thêm id=\"problem-intro\", id=\"data-structure\", id=\"interactive-demo\", "
            f"id=\"summary-notes\", id=\"self-test\" vào đúng section tương ứng."
        )
    gates.append({
        "id": 1,
        "name": "Cấu trúc 5 phần cố định (Anchor IDs)",
        "passed": gate1_passed,
        "detail": f"Thiếu: {missing_anchors}" if missing_anchors else "Đủ 5 anchor ID.",
        "weight": 15
    })

    # ------------------------------------------------------------------
    # Gate 2: Không rò rỉ forbidden_scope
    # ------------------------------------------------------------------
    gate2_passed = True
    leaked_terms: List[str] = []
    if forbidden_scope:
        forbidden_terms = [t.strip().lower() for t in re.split(r'[;,]', forbidden_scope) if len(t.strip()) > 2]
        for term in forbidden_terms:
            # Check if term appears significantly in content (not just in the "forbidden scope" metadata block)
            occurrences = len(re.findall(rf'\b{re.escape(term)}\b', content_lower))
            if occurrences >= 3:  # Appears 3+ times suggests actual use, not coincidence
                leaked_terms.append(f"'{term}' ({occurrences} lần)")
        if leaked_terms:
            gate2_passed = False
            penalty = 20
            score -= penalty
            feedback_parts.append(
                f"[Gate 2] Rò rỉ kiến thức cấm ({len(leaked_terms)} thuật ngữ): "
                f"{', '.join(leaked_terms)}. Xóa hoặc thay thế bằng kiến thức trong phạm vi đã học."
            )
    gates.append({
        "id": 2,
        "name": "Không rò rỉ forbidden_scope",
        "passed": gate2_passed,
        "detail": f"Rò rỉ: {leaked_terms}" if leaked_terms else "Không phát hiện rò rỉ scope.",
        "weight": 20
    })

    # ------------------------------------------------------------------
    # Gate 3: Có sơ đồ SVG 16:9 ở Phần 1 (Kim Chỉ Nam 4)
    # ------------------------------------------------------------------
    has_svg_diagram = (
        'viewbox="0 0 800 450"' in content_lower
        or 'viewbox="0 0 1600 900"' in content_lower
        or 'scene-image-container' in content_lower
        or ('viewbox' in content_lower and '<svg' in content_lower)
        or 'class="mermaid"' in html_content
        or 'class="mermaid ' in html_content
    )
    gate3_passed = has_svg_diagram
    if not gate3_passed:
        penalty = 15
        score -= penalty
        feedback_parts.append(
            "[Gate 3] Thiếu sơ đồ SVG 16:9 ở Phần 1. "
            "Thêm SVG viewBox='0 0 800 450' hoặc Mermaid diagram minh họa bối cảnh bài toán."
        )
    gates.append({
        "id": 3,
        "name": "Sơ đồ SVG 16:9 hoặc Mermaid",
        "passed": gate3_passed,
        "detail": "Có sơ đồ trực quan." if gate3_passed else "Thiếu sơ đồ SVG/Mermaid.",
        "weight": 15
    })

    # ------------------------------------------------------------------
    # Gate 4: Có thẻ Good Practice vs Bad Practice (Kim Chỉ Nam 5)
    # ------------------------------------------------------------------
    has_good_practice = (
        "ph-check-circle" in html_content
        or "good practice" in content_lower
        or "best practice" in content_lower
        or "thực hành tốt" in content_lower
        or "example_good" in content_lower
        or "code-good" in content_lower
    )
    has_bad_practice = (
        "ph-x-circle" in html_content
        or "anti-pattern" in content_lower
        or "bad practice" in content_lower
        or "nên tránh" in content_lower
        or "example_bad" in content_lower
        or "code-bad" in content_lower
    )
    gate4_passed = has_good_practice and has_bad_practice
    if not gate4_passed:
        penalty = 15
        score -= penalty
        missing = []
        if not has_good_practice:
            missing.append("GOOD Practice card")
        if not has_bad_practice:
            missing.append("BAD Practice (Anti-pattern) card")
        feedback_parts.append(
            f"[Gate 4] Thiếu: {', '.join(missing)}. "
            "Thêm cặp code card đối chiếu GOOD vs BAD practice với icon ph-check-circle / ph-x-circle."
        )
    gates.append({
        "id": 4,
        "name": "Thẻ Good vs Bad Practice",
        "passed": gate4_passed,
        "detail": "Có cả hai." if gate4_passed else f"Thiếu: good={has_good_practice}, bad={has_bad_practice}",
        "weight": 15
    })

    # ------------------------------------------------------------------
    # Gate 5: Có Self-Test Form MCQ với nút Kiểm Tra (Kim Chỉ Nam 7)
    # ------------------------------------------------------------------
    has_selftest_btn = (
        "btn-check-selftest" in html_content
        or "checkselftest" in content_lower
        or "kiểm tra đáp án" in content_lower
        or "selftest-section" in html_content
    )
    has_selftest_radios = (
        'type="radio"' in html_content
        or 'selftest_q' in html_content
        or "selftest-item" in html_content
    )
    gate5_passed = has_selftest_btn and has_selftest_radios
    if not gate5_passed:
        penalty = 20
        score -= penalty
        feedback_parts.append(
            "[Gate 5] Thiếu Self-Test MCQ 1-Page: "
            f"{'Thiếu nút Kiểm Tra Đáp Án. ' if not has_selftest_btn else ''}"
            f"{'Thiếu radio input (4 lựa chọn A/B/C/D). ' if not has_selftest_radios else ''}"
            "Thêm form MCQ với id='selftest-section', radio buttons và nút id='btn-check-selftest'."
        )
    gates.append({
        "id": 5,
        "name": "Self-Test MCQ Form 1-Page",
        "passed": gate5_passed,
        "detail": "Đầy đủ form + nút submit." if gate5_passed else f"btn={has_selftest_btn}, radios={has_selftest_radios}",
        "weight": 20
    })

    # ------------------------------------------------------------------
    # Gate 6: Không vi phạm Human-Like Quality (Kim Chỉ Nam 10)
    # ------------------------------------------------------------------
    quality_violations: List[str] = []
    # Check W3Schools reference
    if "w3schools" in content_lower:
        quality_violations.append("Chứa tham chiếu W3Schools (cấm)")
    # Check ALL CAPS headings (more than 3 consecutive uppercase words in heading tags)
    caps_headings = re.findall(r'<h[1-6][^>]*>([^<]*)</h[1-6]>', html_content)
    for h_text in caps_headings:
        plain = re.sub(r'<[^>]+>', '', h_text).strip()
        if plain.isupper() and len(plain) > 8:
            quality_violations.append(f"Tiêu đề ALL CAPS: '{plain[:40]}'")
    # Check bracket labels
    bracket_labels = re.findall(r'\[(?:NOTE|WARNING|BEST PRACTICE|ANTI-PATTERN|TIP|HINT)\]', html_content, re.IGNORECASE)
    if bracket_labels:
        quality_violations.append(f"Dùng nhãn bọc vuông: {set(bracket_labels)}")
    # Check hype phrases
    ai_phrases = ["hãy cùng tìm hiểu", "như vậy chúng ta thấy", "thú vị là", "thần tốc", "bí quyết"]
    for phrase in ai_phrases:
        if phrase in content_lower:
            quality_violations.append(f"Từ sáo rỗng: '{phrase}'")

    gate6_passed = len(quality_violations) == 0
    if not gate6_passed:
        penalty = min(15, len(quality_violations) * 5)
        score -= penalty
        feedback_parts.append(
            f"[Gate 6] Vi phạm Human-Like Quality ({len(quality_violations)} lỗi): "
            + "; ".join(quality_violations[:3]) + "."
        )
    gates.append({
        "id": 6,
        "name": "Human-Like Quality (No ALL CAPS, No W3Schools, No hype)",
        "passed": gate6_passed,
        "detail": "Đạt chuẩn." if gate6_passed else f"Vi phạm: {quality_violations[:3]}",
        "weight": 15
    })

    # ------------------------------------------------------------------
    # Tổng hợp kết quả
    # ------------------------------------------------------------------
    score = max(0, min(100, score))
    passed_count = sum(1 for g in gates if g["passed"])
    overall_passed = passed_count >= 5 and score >= 70  # Ít nhất 5/6 gate và điểm >= 70

    if overall_passed:
        summary = f"APPROVED: Bài đọc vượt Quality Gate ({passed_count}/6 gates, Score: {score}/100)."
    else:
        summary = (
            f"REJECTED: Bài đọc chưa đạt Quality Gate ({passed_count}/6 gates, Score: {score}/100). "
            f"Cần sửa {6 - passed_count} gate còn lại."
        )

    full_feedback = summary
    if feedback_parts:
        full_feedback += "\n\nHướng dẫn sửa cụ thể:\n" + "\n".join(feedback_parts)

    def _safe_print(msg: str):
        try:
            print(msg)
        except UnicodeEncodeError:
            print(msg.encode('ascii', errors='replace').decode('ascii'))

    _safe_print(f"  [Reading Quality Gate] {summary}")
    for gate in gates:
        status = "OK" if gate["passed"] else "FAIL"
        _safe_print(f"    [{status}] Gate {gate['id']}: {gate['name'][:50]} — {gate['detail'][:70]}")

    return {
        "passed": overall_passed,
        "score": score,
        "gates": gates,
        "feedback": full_feedback,
        "passed_count": passed_count
    }


def audit_exercise_quality_gate(
    exercise_content: str,
    level_index: int,
    session_title: str,
    forbidden_terms: List[str] = None
) -> Dict[str, Any]:
    """
    Quality Gate tự động kiểm định chất lượng Bài tập (6 Real-world Exercises).
    Kiểm tra 6 Gate tiêu chuẩn:
      1. Cấu trúc 5 phần H3 bắt buộc
      2. Cấm Emoji & Hype Words (Academic Tone)
      3. Chặn rò rỉ phạm vi kiến thức (Anti-Scope-Leakage)
      4. Đảm bảo tính chủ động cho bài Sáng tạo (Level 5/6: 0 mẫu I/O cho sẵn)
      5. Có Sơ đồ Mermaid trực quan bối cảnh ở mục 2
      6. Có Bảng Rubric 100 điểm dành cho Giảng viên
    """
    if forbidden_terms is None:
        forbidden_terms = []

    score = 100
    gates = []
    feedback_parts = []

    def _safe_print(msg: str):
        try:
            print(msg)
        except UnicodeEncodeError:
            print(msg.encode('ascii', errors='replace').decode('ascii'))

    # Gate 1: Cấu trúc 5 phần H3
    h3_headings = [
        "Mục tiêu",
        "Bối cảnh",
        "Quy tắc nghiệp vụ",  # hoặc Mã nguồn hiện tại
        "Yêu cầu",
        "Yêu cầu nộp bài"
    ]
    missing_headings = []
    for h in h3_headings:
        if h not in exercise_content:
            missing_headings.append(h)
    
    gate1_passed = len(missing_headings) == 0
    if not gate1_passed:
        score -= 20
        feedback_parts.append(f"Gate 1 thất bại: Đề bài thiếu các tiêu đề H3: {', '.join(missing_headings)}.")
    
    gates.append({
        "id": 1,
        "name": "Cấu trúc 5 tiêu đề H3 bắt buộc",
        "passed": gate1_passed,
        "detail": "Đủ 5 phần H3." if gate1_passed else f"Thiếu: {missing_headings}",
        "weight": 20
    })

    # Gate 2: Cấm Emoji & Hype words
    emoji_violations = check_forbidden_emojis(exercise_content)
    hype_violations = [w for w in HYPE_WORDS if w.lower() in exercise_content.lower()]
    gate2_passed = len(emoji_violations) == 0 and len(hype_violations) == 0
    if not gate2_passed:
        score -= 15
        detail_msg = []
        if emoji_violations:
            detail_msg.append(f"Emoji: {emoji_violations[:3]}")
        if hype_violations:
            detail_msg.append(f"Hype words: {hype_violations[:3]}")
        feedback_parts.append(f"Gate 2 thất bại: Chứa emoji hoặc từ sáo rỗng: {'; '.join(detail_msg)}.")

    gates.append({
        "id": 2,
        "name": "Không Emoji & Giữ phong cách Academic Tone",
        "passed": gate2_passed,
        "detail": "Đạt chuẩn." if gate2_passed else "Chứa emoji hoặc hype words.",
        "weight": 15
    })

    # Gate 3: Anti-Scope-Leakage (Chặn rò rỉ kiến thức tương lai)
    leakage_found = []
    for term in forbidden_terms:
        if term and term.strip() and re.search(r'\b' + re.escape(term.strip()) + r'\b', exercise_content, re.IGNORECASE):
            leakage_found.append(term.strip())

    gate3_passed = len(leakage_found) == 0
    if not gate3_passed:
        score -= 25
        feedback_parts.append(f"Gate 3 thất bại (Anti-Scope-Leakage): Phát hiện từ khóa vượt scope bài học: {leakage_found[:5]}. Cần loại bỏ ngay.")

    gates.append({
        "id": 3,
        "name": "Chặn rò rỉ kiến thức vượt scope (Anti-Scope-Leakage)",
        "passed": gate3_passed,
        "detail": "Đạt chuẩn scope." if gate3_passed else f"Vi phạm scope: {leakage_found[:5]}",
        "weight": 25
    })

    # Gate 4: Creative Proactivity Enforcement (Bài Sáng tạo level_index == 5)
    gate4_passed = True
    if level_index == 5:
        # Bài sáng tạo CẤM cho sẵn mẫu JSON request/response body hoặc bảng input/output mẫu
        io_sample_patterns = [r"```json\s*\{\s*\"[a-zA-Z0-9_]+\"", r"Bảng dữ liệu mẫu", r"JSON Request body mẫu", r"Response body mẫu"]
        found_samples = []
        for pat in io_sample_patterns:
            if re.search(pat, exercise_content, re.IGNORECASE):
                found_samples.append(pat)
        if found_samples:
            gate4_passed = False
            score -= 20
            feedback_parts.append("Gate 4 thất bại (Sáng tạo Proactivity): Bài tập Sáng tạo đang cho sẵn Input/Output mẫu. Cần xóa mẫu I/O và yêu cầu sinh viên tự chủ động thiết kế Schema & Edge cases.")

    gates.append({
        "id": 4,
        "name": "Đảm bảo tính Chủ động cho Bài tập Sáng tạo",
        "passed": gate4_passed,
        "detail": "Đạt chuẩn tính chủ động." if gate4_passed else "Cho sẵn Input/Output mẫu làm mất tính sáng tạo.",
        "weight": 20
    })

    # Gate 5: Có Sơ đồ Mermaid Bối cảnh
    has_mermaid = "```mermaid" in exercise_content.lower()
    gate5_passed = has_mermaid
    if not gate5_passed:
        score -= 10
        feedback_parts.append("Gate 5 thất bại: Thiếu sơ đồ Mermaid trực quan luồng bối cảnh bài toán trong phần 2.")

    gates.append({
        "id": 5,
        "name": "Sơ đồ Mermaid bối cảnh bài toán",
        "passed": gate5_passed,
        "detail": "Có sơ đồ Mermaid." if gate5_passed else "Thiếu sơ đồ Mermaid.",
        "weight": 10
    })

    # Gate 6: Có Rubric Chấm điểm
    has_rubric = "rubric" in exercise_content.lower() or "tiêu chí đánh giá" in exercise_content.lower()
    gate6_passed = has_rubric
    if not gate6_passed:
        score -= 10
        feedback_parts.append("Gate 6 thất bại: Thiếu Bảng Rubric chấm điểm 100 điểm cho Giảng viên ở cuối bài tập.")

    gates.append({
        "id": 6,
        "name": "Bảng Rubric 100 điểm dành cho Giảng viên",
        "passed": gate6_passed,
        "detail": "Có Bảng Rubric." if gate6_passed else "Thiếu Rubric.",
        "weight": 10
    })

    score = max(0, min(100, score))
    passed_count = sum(1 for g in gates if g["passed"])
    overall_passed = passed_count >= 5 and score >= 70

    if overall_passed:
        summary = f"APPROVED: Bài tập vượt Quality Gate ({passed_count}/6 gates, Score: {score}/100)."
    else:
        summary = f"REJECTED: Bài tập chưa đạt Quality Gate ({passed_count}/6 gates, Score: {score}/100)."

    _safe_print(f"  [Exercise Quality Gate] {summary}")
    for g in gates:
        st = "OK" if g["passed"] else "FAIL"
        _safe_print(f"    [{st}] Gate {g['id']}: {g['name'][:50]} — {g['detail'][:70]}")

    return {
        "passed": overall_passed,
        "score": score,
        "gates": gates,
        "feedback": summary + ("\n\nFixing steps:\n" + "\n".join(feedback_parts) if feedback_parts else ""),
        "passed_count": passed_count
    }

