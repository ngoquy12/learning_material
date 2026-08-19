"""
core/pm_validators/structure_validator.py
Validates PM Syllabus Structure, Pacing, Session Numbering, and Budget Alignment.
"""

from typing import Dict, Any, List, Tuple
from core.pm_validators.constants import (
    get_hinh_thuc,
    get_session_num,
    is_programming_language_course
)

def validate_syllabus_structure(
    pm_data: List[Dict[str, Any]],
    tech_stack: str = "",
    sessions_per_day: int = 1,
    session_budget: Dict[str, Any] = None,
    main_content: str = ""
) -> Tuple[int, List[str], List[Dict[str, Any]]]:
    """
    Validates structural rules and pacing of PM Syllabus.
    Returns: (penalty_score_deductions, rule_violations, review_logs)
    """
    rule_violations: List[str] = []
    review_logs: List[Dict[str, Any]] = []
    deductions = 0
    total_sessions = len(pm_data)

    if not pm_data:
        return 100, ["Lỗi nghiêm trọng: PM rỗng, không chứa session nào."], [{"level": "CRITICAL", "message": "PM rỗng."}]

    # Rule 1: Session 01 MUST be Orientation / Lý thuyết
    s1 = pm_data[0]
    ht1 = get_hinh_thuc(s1)
    if "Lý thuyết" not in ht1:
        msg = f"Session 01 phải là 'Lý thuyết' (Định hướng & Lộ trình), nhưng hiện tại là '{ht1}'."
        rule_violations.append(msg)
        review_logs.append({"level": "ERROR", "message": msg})
        deductions += 15

    # Rule 2: Session 02 MUST be Theory
    if total_sessions >= 2:
        s2 = pm_data[1]
        ht2 = get_hinh_thuc(s2)
        if "Lý thuyết" not in ht2:
            msg = f"Session 02 PHẢI là 'Lý thuyết' kỹ thuật đầu tiên, nhưng hiện tại là '{ht2}'."
            rule_violations.append(msg)
            review_logs.append({"level": "ERROR", "message": msg})
            deductions += 15

    # Rule 4: Final Session MUST be Exam / Project
    last_session = pm_data[-1]
    ht_last = get_hinh_thuc(last_session)
    valid_finals = ["Thi cuối môn", "Project", "Dự án cuối khóa", "Hackathon"]
    if not any(vf.lower() in ht_last.lower() for vf in valid_finals):
        msg = f"Buổi cuối cùng (Session {total_sessions:02d}) phải là Thi cuối môn hoặc Project, nhưng hiện tại là '{ht_last}'."
        rule_violations.append(msg)
        review_logs.append({"level": "ERROR", "message": msg})
        deductions += 10

    # Rule 4.5: Session 01 Fixed Consolidated Lesson Check
    if len(pm_data) > 0:
        s01 = pm_data[0]
        s01_lessons = s01.get("lessons", [])
        expected_title = "Tổng quan lộ trình và Demo sản phẩm"
        if len(s01_lessons) != 1:
            msg = f"Session 01 phải có chính xác 1 lesson duy nhất ('{expected_title}'), nhưng thực tế có {len(s01_lessons)} lessons."
            rule_violations.append(msg)
            review_logs.append({"level": "ERROR", "message": msg})
            deductions += 5
        elif "tổng quan lộ trình" not in str(s01_lessons[0].get("title", "")).lower():
            msg = f"Session 01 Lesson 01 tiêu đề sai lệch. Yêu cầu chính xác: '{expected_title}', thực tế: '{s01_lessons[0].get('title', '')}'."
            rule_violations.append(msg)
            review_logs.append({"level": "ERROR", "message": msg})
            deductions += 5

    # Rule 4.6: Session 02 Lesson 1 Technology Overview Check
    if len(pm_data) > 1:
        s02 = pm_data[1]
        s02_lessons = s02.get("lessons", [])
        if len(s02_lessons) > 0:
            l1_title = str(s02_lessons[0].get("title", "")).lower()
            if not any(w in l1_title for w in ["tổng quan", "giới thiệu", "overview", "introduction"]):
                msg = f"Session 02 Lesson 1 ('{s02_lessons[0].get('title', '')}') KHÔNG PHẢI là bài Giới thiệu tổng quan công nghệ. Yêu cầu Bài 1 của Session 02 luôn phải là phần Giới thiệu tổng quan về công nghệ."
                rule_violations.append(msg)
                review_logs.append({"level": "ERROR", "message": msg})
                deductions += 10

    # Rule 4.7: Advanced Topics Deferral Check
    for idx, s in enumerate(pm_data):
        snum = get_session_num(s, idx)
        if snum <= 16:
            all_s_text = f"{s.get('title', '')} {s.get('content_scope', '')}".lower()
            for testing_kw in ["unit test", "unittest", "testing framework", "test suite"]:
                if testing_kw in all_s_text:
                    msg = f"Session {snum:02d} vi phạm quy tắc hoãn chủ đề nâng cao: '{testing_kw}' xuất hiện quá sớm. Unit testing BẮT BUỘC hoãn sang nửa sau (Sessions 17-23)."
                    rule_violations.append(msg)
                    review_logs.append({"level": "WARNING", "message": msg})
                    deductions += 5
                    break

    # Helper check: determine if target course is a programming language / coding course
    is_coding = is_programming_language_course(tech_stack, main_content, pm_data)

    # Rule 4.8: Mandatory Subprograms / Functions Check (ONLY for Programming Courses)
    if is_coding:
        part1_text = " ".join([f"{s.get('title', '')} {s.get('content_scope', '')}" for s in pm_data[:16]]).lower()
        if not any(fn_kw in part1_text for fn_kw in ["hàm", "function", "subprogram", "method", "thủ tục"]):
            msg = "Phần 1 (Sessions 01-16) thiếu kiến thức cốt lõi về Hàm / Subprograms (Functions). BẮT BUỘC đưa chủ đề Hàm vào Nửa đầu môn học trước khi thi giữa kỳ."
            rule_violations.append(msg)
            review_logs.append({"level": "ERROR", "message": msg})
            deductions += 20

    # Rule 4.9: Collection CRUD Operations Cramming Check (ONLY for Programming Courses)
    if is_coding:
        for idx, s in enumerate(pm_data):
            lessons = s.get("lessons", [])
            for l in lessons:
                ltitle = str(l.get("title", "")).lower()
                lscope = str(l.get("content_scope", "")).lower()
                comb_text = f"{ltitle} {lscope}"
                if sum(1 for kw in ["duyệt", "thêm", "sửa", "xóa"] if kw in comb_text) >= 3:
                    msg = f"Session {idx+1:02d} Lesson '{l.get('title', '')}' gom quá nhiều thao tác (Duyệt, Thêm, Sửa, Xóa) vào 1 lesson. Yêu cầu phân rã thao tác tập hợp dữ liệu thành các bài học nguyên tử riêng biệt."
                    rule_violations.append(msg)
                    review_logs.append({"level": "ERROR", "message": msg})
                    deductions += 10
                    break

    # Rule 5 & 6 & 7: Lessons count & sequential session numbering
    for idx, s in enumerate(pm_data):
        snum = get_session_num(s, idx)
        ht = get_hinh_thuc(s)
        lessons = s.get("lessons", [])

        # Sequential check
        if snum != idx + 1:
            msg = f"Session numbering rớt số: mong đợi Session {idx + 1:02d}, nhận Session {snum}."
            rule_violations.append(msg)
            review_logs.append({"level": "ERROR", "message": msg})
            deductions += 10
            break

        # Non-theory lessons check
        if "Lý thuyết" not in ht and len(lessons) > 0:
            msg = f"Session {snum:02d} ({ht}) không được chứa lesson con, nhưng hiện có {len(lessons)} lessons."
            rule_violations.append(msg)
            review_logs.append({"level": "ERROR", "message": msg})
            deductions += 5

        # Theory lessons count & purity check
        if "Lý thuyết" in ht and snum > 1:
            if len(lessons) < 2 or len(lessons) > 7:
                msg = f"Session {snum:02d} (Lý thuyết) có {len(lessons)} lessons — phải từ 2 đến 7 lessons linh động."
                rule_violations.append(msg)
                review_logs.append({"level": "ERROR", "message": msg})
                deductions += 5

            for l in lessons:
                ltitle = str(l.get("title", "")).lower()
                lscope = str(l.get("content_scope", "")).lower()
                forbidden_task_terms = ["thực hành bài tập", "luyện tập viết", "thực hành làm", "bài tập thực hành"]
                for term in forbidden_task_terms:
                    if term in ltitle or term in lscope:
                        msg = f"Session {snum:02d} Lesson '{l.get('title', '')}' vi phạm tính thuần lý thuyết. CẤM đưa nhiệm vụ/bài tập thực hành vào nội dung lesson lý thuyết."
                        rule_violations.append(msg)
                        review_logs.append({"level": "ERROR", "message": msg})
                        deductions += 5
                        break

    # Rule 8: Delivery pacing
    if sessions_per_day == 2 and total_sessions >= 4:
        for day_idx in range(1, total_sessions // 2):
            s_a = pm_data[day_idx * 2]
            s_b = pm_data[day_idx * 2 + 1] if (day_idx * 2 + 1) < total_sessions else None
            if s_b:
                ht_a = get_hinh_thuc(s_a)
                ht_b = get_hinh_thuc(s_b)
                if "Lý thuyết" in ht_a and "Lý thuyết" in ht_b:
                    msg = (f"Ngày {day_idx + 1} (Session {day_idx*2+1:02d} & {day_idx*2+2:02d}) bị xếp 2 buổi Lý thuyết liên tiếp. "
                           f"Bắt buộc xen kẽ 1 Lý thuyết + 1 Thực hành.")
                    rule_violations.append(msg)
                    review_logs.append({"level": "WARNING", "message": msg})
                    deductions += 5

    # Rule 8.5: STRICT NON-THEORY ADJACENCY ISOLATION CHECK
    for idx in range(len(pm_data) - 1):
        s_curr = pm_data[idx]
        s_next = pm_data[idx + 1]
        ht_curr = get_hinh_thuc(s_curr)
        ht_next = get_hinh_thuc(s_next)
        snum_curr = get_session_num(s_curr, idx)
        snum_next = get_session_num(s_next, idx + 1)

        if "Thực hành" in ht_curr and "Thực hành" in ht_next:
            msg = f"Vi phạm nhịp độ sư phạm: Session {snum_curr:02d} ({ht_curr}) và Session {snum_next:02d} ({ht_next}) là 2 buổi Thực hành xếp sát nhau. TUYỆT ĐỐI CẤM xếp 2 buổi Thực hành liên tiếp."
            rule_violations.append(msg)
            review_logs.append({"level": "ERROR", "message": msg})
            deductions += 20

        if ("Thực hành" in ht_curr and "Mini project" in ht_next) or ("Mini project" in ht_curr and "Thực hành" in ht_next):
            msg = f"Vi phạm nhịp độ sư phạm: Session {snum_curr:02d} ({ht_curr}) và Session {snum_next:02d} ({ht_next}) đứng sát nhau. TUYỆT ĐỐI CẤM xếp Thực hành và Mini Project liền kề nhau."
            rule_violations.append(msg)
            review_logs.append({"level": "ERROR", "message": msg})
            deductions += 20

        if "Mini project" in ht_curr and "Mini project" in ht_next:
            msg = f"Vi phạm nhịp độ sư phạm: Session {snum_curr:02d} ({ht_curr}) và Session {snum_next:02d} ({ht_next}) là 2 buổi Mini Project đứng sát nhau."
            rule_violations.append(msg)
            review_logs.append({"level": "ERROR", "message": msg})
            deductions += 20

    # Rule 9: Session Budget & Capstone Project Alignment Check
    if session_budget:
        expected_total = session_budget.get("total_sessions")
        if expected_total and total_sessions != expected_total:
            msg = f"Tổng số buổi trong PM ({total_sessions} buổi) bị LỆCH so với session_budget ({expected_total} buổi trong Khung Excel PTIT)."
            rule_violations.append(msg)
            review_logs.append({"level": "ERROR", "message": msg})
            deductions += 30

        expected_capstone = session_budget.get("capstone_project", 0)
        actual_capstone_count = sum(1 for s in pm_data if get_hinh_thuc(s).lower() in ["project", "capstone project", "dự án", "dự án cuối khóa", "capstone"])
        if expected_capstone == 0 and actual_capstone_count > 0:
            msg = f"Khung môn học quy định capstone_project = 0 nhưng PM lại tự ý sinh ra {actual_capstone_count} buổi Project/Capstone."
            rule_violations.append(msg)
            review_logs.append({"level": "ERROR", "message": msg})
            deductions += 20

        expected_mini = session_budget.get("mini_projects", 0)
        if expected_mini > 0:
            actual_mini_count = sum(1 for s in pm_data if "mini project" in get_hinh_thuc(s).lower())
            if actual_mini_count < expected_mini:
                msg = f"Khung môn học yêu cầu {expected_mini} buổi Mini project nhưng PM chỉ sinh ra {actual_mini_count} buổi Mini project."
                rule_violations.append(msg)
                review_logs.append({"level": "ERROR", "message": msg})
                deductions += 15

    # Check for Thin Practice Sessions
    for idx, s in enumerate(pm_data):
        stype = get_hinh_thuc(s)
        snum = get_session_num(s, idx + 1)
        if stype in ["Thực hành", "PRACTICE"] and idx > 0:
            prev_s = pm_data[idx - 1]
            prev_type = get_hinh_thuc(prev_s)
            if prev_type in ["Lý thuyết", "THEORY"]:
                prev_text = (prev_s.get("title", "") + " " + prev_s.get("content_scope", "")).lower()
                for l in prev_s.get("lessons", []):
                    prev_text += " " + (l.get("title", "") + " " + l.get("content_scope", "")).lower()
                
                has_only_setup = any(w in prev_text for w in ["cài đặt", "môi trường", "sdk", "runtime", "compiler", "linter", "setup", "config", "cấu hình"])
                has_code_depth = any(w in prev_text for w in ["biến", "kiểu dữ liệu", "toán tử", "nhập", "xuất", "print", "input", "rẽ nhánh", "vòng lặp", "hàm", "dữ liệu", "cú pháp", "code", "lập trình"])
                
                if has_only_setup and not has_code_depth:
                    msg = f"Session {snum:02d} (Thực hành) có nguy cơ bị nông/rỗng: Session Lý thuyết {snum-1:02d} chỉ chứa nội dung Cài đặt/Môi trường mà chưa có kiến thức lập trình (Biến/Kiểu dữ liệu/Nhập xuất). Cần tăng hàm lượng kiến thức hoặc chuyển thành buổi Lý thuyết."
                    rule_violations.append(msg)
                    review_logs.append({"level": "WARNING", "message": msg})
                    deductions += 3

    return deductions, rule_violations, review_logs
