"""
core/pm_validators/quality_gates.py
Automated Quality Gates for Reading HTML and 6-Suite Homework Exercises.
"""

import re
from typing import Dict, Any, List
from core.pm_validators.constants import HYPE_WORDS
from agents.reviewer_agents import check_forbidden_emojis

def audit_reading_html_quality_gate(
    html_content: str,
    lesson_title: str = "",
    forbidden_scope: str = "",
    tech_stack: str = ""
) -> Dict[str, Any]:
    """
    6-Point Automated Quality Gate cho bài đọc HTML theo Rikkei Education Golden Standards.
    Gate 1: 5 Anchor ID cố định có mặt đầy đủ
    Gate 2: Không rò rỉ kiến thức forbidden_scope
    Gate 3: Có sơ đồ SVG 16:9 hoặc Mermaid
    Gate 4: Có thẻ Good Practice vs Bad Practice
    Gate 5: Có form Self-Test MCQ với nút Kiểm Tra Đáp Án
    Gate 6: Không dùng ALL CAPS tiêu đề, không emoji sáo rỗng, không W3Schools
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

    # Gate 1: 5 Anchor ID cố định
    required_anchors = [
        ("problem-intro", "Phần 1 — Đặt vấn đề thực tế"),
        ("data-structure", "Phần 2 — Cú pháp & Cơ chế"),
        ("interactive-demo", "Phần 3 — Ví dụ minh họa"),
        ("summary-notes", "Phần 4 — Lưu ý thực chiến"),
        ("self-test", "Phần 5 — Khảo thí tự đánh giá"),
    ]
    missing_anchors = []
    for anchor_id, anchor_name in required_anchors:
        if f'id="{anchor_id}"' not in html_content and f"id='{anchor_id}'" not in html_content:
            missing_anchors.append(f"{anchor_id} ({anchor_name})")

    gate1_passed = len(missing_anchors) <= 2
    if not gate1_passed:
        score -= 15
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

    # Gate 2: Không rò rỉ forbidden_scope
    gate2_passed = True
    leaked_terms: List[str] = []
    if forbidden_scope:
        forbidden_terms = [t.strip().lower() for t in re.split(r'[;,]', forbidden_scope) if len(t.strip()) > 2]
        for term in forbidden_terms:
            occurrences = len(re.findall(rf'\b{re.escape(term)}\b', content_lower))
            if occurrences >= 3:
                leaked_terms.append(f"'{term}' ({occurrences} lần)")
        if leaked_terms:
            gate2_passed = False
            score -= 20
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

    # Gate 3: Sơ đồ SVG 16:9 hoặc Mermaid
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
        score -= 15
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

    # Gate 4: Thẻ Good Practice vs Bad Practice
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
        score -= 15
        missing = []
        if not has_good_practice:
            missing.append("GOOD Practice card")
        if not has_bad_practice:
            missing.append("BAD Practice card")
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

    # Gate 5: Self-Test Form MCQ 1-Page
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
        score -= 20
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

    # Gate 6: Human-Like Quality
    quality_violations: List[str] = []
    if "w3schools" in content_lower:
        quality_violations.append("Chứa tham chiếu W3Schools (cấm)")
    caps_headings = re.findall(r'<h[1-6][^>]*>([^<]*)</h[1-6]>', html_content)
    for h_text in caps_headings:
        plain = re.sub(r'<[^>]+>', '', h_text).strip()
        if plain.isupper() and len(plain) > 8:
            quality_violations.append(f"Tiêu đề ALL CAPS: '{plain[:40]}'")
    bracket_labels = re.findall(r'\[(?:NOTE|WARNING|BEST PRACTICE|ANTI-PATTERN|TIP|HINT)\]', html_content, re.IGNORECASE)
    if bracket_labels:
        quality_violations.append(f"Dùng nhãn bọc vuông: {set(bracket_labels)}")
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

    score = max(0, min(100, score))
    passed_count = sum(1 for g in gates if g["passed"])
    overall_passed = passed_count >= 5 and score >= 70

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

    # Gate 1: Cấu trúc 5 phần H3
    h3_headings = [
        "Mục tiêu",
        "Bối cảnh",
        "Quy tắc nghiệp vụ",
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

    # Gate 3: Anti-Scope-Leakage
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

    # Gate 4: Creative Proactivity Enforcement
    gate4_passed = True
    if level_index == 5:
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

    # Gate 5: Sơ đồ Mermaid Bối cảnh
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

    summary = f"{'APPROVED' if overall_passed else 'REJECTED'}: Bài tập {'vượt' if overall_passed else 'chưa đạt'} Quality Gate ({passed_count}/6 gates, Score: {score}/100)."

    return {
        "passed": overall_passed,
        "score": score,
        "gates": gates,
        "feedback": summary + ("\n\nFixing steps:\n" + "\n".join(feedback_parts) if feedback_parts else ""),
        "passed_count": passed_count
    }
