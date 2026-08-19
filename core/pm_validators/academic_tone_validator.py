"""
core/pm_validators/academic_tone_validator.py
Validates Academic Tone, Bloom Action Verbs, Anti-Hype, Atomic Lesson Purity, and Formatting Rules.
"""

import re
from typing import Dict, Any, List, Tuple
from core.pm_validators.constants import (
    HYPE_WORDS,
    DIFFICULTY_BADGES,
    VAGUE_OUTCOME_VERBS,
    get_session_num,
    get_hinh_thuc
)
from agents.reviewer_agents import check_forbidden_emojis, check_unaccented_vietnamese

def validate_academic_tone(
    pm_data: List[Dict[str, Any]],
    tech_stack: str = "",
    main_content: str = ""
) -> Tuple[int, List[str], List[Dict[str, Any]]]:
    """
    Validates academic tone, typography, bloom action verbs, and atomic lesson purity.
    Returns: (penalty_score_deductions, rule_violations, review_logs)
    """
    rule_violations: List[str] = []
    review_logs: List[Dict[str, Any]] = []
    deductions = 0

    for s in pm_data:
        snum = get_session_num(s, 0)
        s_title = str(s.get("title", ""))

        # Check ALL CAPS in Session title
        if s_title.isupper() and len(s_title) > 5:
            msg = f"Session {snum:02d} tiêu đề dùng VIẾT HOA TOÀN BỘ (ALL CAPS): '{s_title}'. Bắt buộc dùng Sentence case."
            rule_violations.append(msg)
            review_logs.append({"level": "WARNING", "message": msg})
            deductions += 3

        # Check Emoji in Session title / scope
        all_s_text = f"{s_title} {s.get('content_scope', '')} {s.get('expected_outcome', '')}"
        emoji_err = check_forbidden_emojis(all_s_text)
        if emoji_err:
            msg = f"Session {snum:02d} chứa Emoji/Icon cấm: {emoji_err}"
            rule_violations.append(msg)
            review_logs.append({"level": "ERROR", "message": msg})
            deductions += 5

        # Check Difficulty Badges in Session title
        for badge in DIFFICULTY_BADGES:
            if re.search(badge, s_title, re.IGNORECASE):
                msg = f"Session {snum:02d} tiêu đề chứa hậu tố phân loại cấm: '{s_title}'."
                rule_violations.append(msg)
                review_logs.append({"level": "ERROR", "message": msg})

        # Check unwarranted domain injection
        main_content_lower = str(main_content).lower()
        if "backend" not in (main_content_lower + tech_stack.lower()) and "backend" in s_title.lower():
            msg = f"Session {snum:02d} vi phạm phạm vi môn học: Tự ý dán nhãn 'backend' trong khi môn học là lập trình cơ bản."
            rule_violations.append(msg)
            review_logs.append({"level": "ERROR", "message": msg})
            deductions += 10

        # Check Hype Words (Academic Tone)
        for hw in HYPE_WORDS:
            if hw in all_s_text.lower():
                msg = f"Session {snum:02d} chứa từ giật tít/không chuẩn sư phạm: '{hw}'."
                rule_violations.append(msg)
                review_logs.append({"level": "WARNING", "message": msg})
                deductions += 3

        # Check Vague Action Verbs in expected_outcome
        s_outcome = s.get("expected_outcome", "").lower().strip()
        for vague_v in VAGUE_OUTCOME_VERBS:
            if vague_v in s_outcome:
                msg = f"Session {snum:02d} outcome dùng động từ nhận thức mơ hồ cấm ('{vague_v}'): '{s.get('expected_outcome', '')}'. Bắt buộc dùng động từ đo lường được theo Bloom (ví dụ: 'Phân biệt được...', 'Khởi tạo thành công...')."
                rule_violations.append(msg)
                review_logs.append({"level": "ERROR", "message": msg})
                deductions += 4
                break

        # Check unaccented Vietnamese
        unaccented_err = check_unaccented_vietnamese(all_s_text)
        if unaccented_err:
            msg = f"Session {snum:02d} vi phạm tiếng Việt không dấu: {unaccented_err}"
            rule_violations.append(msg)
            review_logs.append({"level": "ERROR", "message": msg})
            deductions += 5

        # Check Lessons within session
        lessons = s.get("lessons", [])
        for l in lessons:
            lnum = l.get("lesson_num", 0)
            ltitle = str(l.get("title", ""))
            l_scope = l.get("content_scope", "").strip()
            l_text = f"{ltitle} {l_scope} {l.get('expected_outcome', '')}"

            if ltitle.isupper() and len(ltitle) > 5:
                msg = f"Session {snum:02d} Lesson {lnum} tiêu đề dùng ALL CAPS: '{ltitle}'."
                rule_violations.append(msg)
                review_logs.append({"level": "WARNING", "message": msg})
                deductions += 2

            emoji_l_err = check_forbidden_emojis(l_text)
            if emoji_l_err:
                msg = f"Session {snum:02d} Lesson {lnum} chứa Emoji: {emoji_l_err}"
                rule_violations.append(msg)
                review_logs.append({"level": "ERROR", "message": msg})
                deductions += 5

            for hw in HYPE_WORDS:
                if hw in l_text.lower():
                    msg = f"Session {snum:02d} Lesson {lnum} chứa từ giật tít: '{hw}'."
                    rule_violations.append(msg)
                    review_logs.append({"level": "WARNING", "message": msg})
                    deductions += 2

            l_outcome = l.get("expected_outcome", "").lower().strip()
            for vague_v in VAGUE_OUTCOME_VERBS:
                if vague_v in l_outcome:
                    msg = f"Session {snum:02d} Lesson {lnum} outcome dùng động từ mơ hồ cấm ('{vague_v}'): '{l.get('expected_outcome', '')}'."
                    rule_violations.append(msg)
                    review_logs.append({"level": "ERROR", "message": msg})
                    deductions += 3
                    break

            # Rule 12: Single Concept Per Lesson (Atomic Purity Check)
            if snum > 1:
                conjunction_parts = re.split(r'\s+và\s+', ltitle, flags=re.IGNORECASE)
                if len(conjunction_parts) >= 2:
                    part_a = conjunction_parts[0].strip()
                    part_b = conjunction_parts[-1].strip()
                    same_family_markers = [
                        ("toán tử", "toán tử"), ("operator", "operator"),
                        ("git ", "git "), ("hàm ", "hàm "),
                        ("kiểu ", "kiểu "), ("biến ", "biến "),
                        ("câu lệnh ", "câu lệnh "),
                        ("nhập", "xuất"), ("xuất", "nhập"),
                        ("nhập", "chuyển đổi"), ("xuất", "chuyển đổi"),
                        ("input", "output"), ("output", "input"),
                        ("cài đặt", "cấu hình"), ("cấu hình", "cài đặt"),
                        ("cài đặt", "môi trường"), ("môi trường", "cài đặt"),
                        ("cài đặt", "thiết lập"), ("thiết lập", "cài đặt"),
                        ("setup", "config"), ("install", "setup"),
                        ("khai báo", "quy tắc"), ("khai báo", "kiểu"),
                        ("biến", "kiểu"), ("variable", "type"),
                        ("select", "insert"), ("create", "alter"),
                        ("bảng", "cột"), ("table", "column"),
                    ]
                    is_same_family = any(
                        m_a in part_a.lower() and m_b in part_b.lower()
                        for m_a, m_b in same_family_markers
                    )
                    if len(part_a) > 8 and len(part_b) > 8 and not is_same_family:
                        msg = (f"Session {snum:02d} Lesson {lnum} tiêu đề ôm đồm 2 khái niệm lớn riêng biệt: "
                               f"'{ltitle}'. Bắt buộc tách thành 2 bài học nguyên tử riêng biệt "
                               f"(Lesson A: '{part_a}', Lesson B: '{part_b}').")
                        rule_violations.append(msg)
                        review_logs.append({"level": "WARNING", "message": msg})
                        deductions += 3

            # Rule 13: Filler / Non-Employable Content Detection
            filler_indicators = [
                "lịch sử phát triển", "history of", "triết lý lập trình",
                "so sánh ngôn ngữ", "language comparison", "lý thuyết thuần túy",
                "tiểu sử", "biography", "sự ra đời", "origin story"
            ]
            combined_scope_text = f"{ltitle} {l_scope}".lower()
            for filler in filler_indicators:
                if filler in combined_scope_text:
                    msg = (f"Session {snum:02d} Lesson {lnum} có dấu hiệu nội dung nhồi nhét / không ứng dụng thực tế: "
                           f"'{filler}' trong '{ltitle}'. Nội dung phải có giá trị thực tế giúp sinh viên đi làm được.")
                    rule_violations.append(msg)
                    review_logs.append({"level": "WARNING", "message": msg})
                    deductions += 3
                    break

            # Rule 14: Anti-Rambling Orientation Check
            if snum > 2 or (snum == 2 and lnum > 1):
                intro_only_markers = ["giới thiệu tổng quan", "tổng quan về", "overview of", "introduction to"]
                is_intro_only = any(m in ltitle.lower() for m in intro_only_markers)
                has_executable_content = any(
                    kw in l_scope.lower() for kw in [
                        "cú pháp", "syntax", "lệnh", "command", "khai báo", "declare",
                        "hàm", "function", "def ", "class ", "create ", "select ",
                        "insert", "git ", "npm ", "pip ", "import"
                    ]
                )
                if is_intro_only and not has_executable_content:
                    msg = (f"Session {snum:02d} Lesson {lnum} lan man giới thiệu tổng quan mà không chứa kiến thức kỹ thuật thực thi được: "
                           f"'{ltitle}'. Bài học sau Session 02 Lesson 1 phải đi thẳng vào kiến thức thực hành.")
                    rule_violations.append(msg)
                    review_logs.append({"level": "WARNING", "message": msg})
                    deductions += 3

            # Rule 15: Professional Title Naming Check
            title_fluff_keywords = [
                "vấn đề tính toán", "vấn đề rẽ nhánh", "vấn đề xử lý", "vấn đề khi", "vấn đề ",
                "tư duy lập trình", "tư duy ", "khám phá ", "tìm hiểu về ", "cách sử dụng ", "cách dùng "
            ]
            ltitle_lower = ltitle.lower()
            for fluff in title_fluff_keywords:
                if fluff in ltitle_lower:
                    msg = (f"Session {snum:02d} Lesson {lnum} chứa từ rườm rà/nghiệp dư cấm trong tiêu đề ('{fluff.strip()}'): "
                           f"'{ltitle}'. Tiêu đề bài học phải chuẩn chỉnh, chuyên nghiệp và đi thẳng vào kiến thức kỹ thuật chính.")
                    rule_violations.append(msg)
                    review_logs.append({"level": "WARNING", "message": msg})
                    deductions += 4
                    break

        # Session level title fluff check
        s_title_lower = s_title.lower()
        sess_fluff_keywords = [
            "vấn đề tính toán", "vấn đề rẽ nhánh", "vấn đề xử lý", "vấn đề khi", "vấn đề ",
            "tư duy lập trình", "tư duy ", "khám phá ", "tìm hiểu về ", "cách sử dụng ", "cách dùng "
        ]
        for s_fluff in sess_fluff_keywords:
            if s_fluff in s_title_lower:
                msg = (f"Session {snum:02d} tiêu đề chứa từ rườm rà/nghiệp dư cấm ('{s_fluff.strip()}'): "
                       f"'{s_title}'. Tiêu đề Session phải chuẩn chỉnh, chuyên nghiệp và đi thẳng vào kiến thức kỹ thuật chính.")
                rule_violations.append(msg)
                review_logs.append({"level": "WARNING", "message": msg})
                deductions += 4
                break

        # Adaptive Pedagogical Structure for Theory Sessions
        if "Lý thuyết" in get_hinh_thuc(s) and len(lessons) >= 3 and snum > 1:
            s_full_title = (s_title + " " + s.get("content_scope", "")).lower()
            is_setup_topic = any(kw in s_full_title for kw in ["cài đặt", "môi trường", "thiết lập", "cấu hình", "setup", "installation", "config", "kho lưu trữ", "giao diện"])

            if is_setup_topic:
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
                    deductions += 3

            else:
                l1_text = (lessons[0].get("title", "") + " " + lessons[0].get("content_scope", "")).lower()
                l2_text = (lessons[1].get("title", "") + " " + lessons[1].get("content_scope", "")).lower()
                l3_text = (lessons[2].get("title", "") + " " + lessons[2].get("content_scope", "")).lower()
                intent_hooks = ["vấn đề", "bài toán", "giới thiệu", "tại sao", "khái niệm", "mô hình", "tầm quan trọng", "nhập môn", "ý nghĩa", "tổng quan", "bản chất", "vai trò", "định hướng", "nền tảng", "tổng thể", "lộ trình", "lý do"]
                intent_mechs = ["cú pháp", "kiến trúc", "cấu hình", "thao tác", "khai báo", "cấu trúc", "cơ chế", "cài đặt", "lệnh", "kỹ thuật", "phương pháp", "quy trình", "cách dùng", "cách viết", "thiết lập", "tích hợp", "xác thực", "liên kết", "mô tả", "hoạt động", "vận hành", "nguyên lý", "bộ nhớ", "luồng", "commit", "branch"]
                intent_apps  = ["ứng dụng", "thực tế", "quy trình", "dự án", "tối ưu", "thực hành", "kịch bản", "tái sử dụng", "đồng bộ", "hợp nhất", "giải quyết", "triển khai", "quản lý", "xử lý", "phối hợp", "chuẩn hóa", "bài tập", "tối ưu hóa", "module", "hệ thống", "xây dựng", "lập trình", "pull request", "phân nhánh"]

                all_lessons_text = " ".join([l.get("title", "") + " " + l.get("content_scope", "") for l in lessons]).lower()
                has_hook = any(w in l1_text for w in intent_hooks)
                has_mech = any(w in l2_text or w in all_lessons_text for w in intent_mechs)
                has_app  = any(w in l3_text or w in all_lessons_text for w in intent_apps)

                if not (has_hook or has_mech or has_app):
                    msg = f"Session {snum:02d} (Lý thuyết) thiếu trật tự dẫn dắt sư phạm (Lesson 1: Khái niệm/Vấn đề ➔ Lesson 2: Cơ chế/Cú pháp ➔ Lesson 3: Ứng dụng/Quy trình)."
                    rule_violations.append(msg)
                    review_logs.append({"level": "WARNING", "message": msg})
                    deductions += 3

    return deductions, rule_violations, review_logs
