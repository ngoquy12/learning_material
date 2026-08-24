"""
core/pm_validators/clo_bloom_validator.py
Đối chiếu cấp Bloom của chuẩn đầu ra với độ phủ nhận thức thực tế của hệ bài tập.

Bổ sung cho clo_coverage_validator.py — nơi chỉ kiểm ĐỘ PHỦ TỪ KHOÁ. Một CLO tuyên
bố "Phân tích và đánh giá hiệu năng" mà chỉ được phủ bởi bài tập mức Vận dụng thì
qua được bộ kiểm từ khoá (thuật ngữ khớp hết) nhưng vi phạm constructive alignment:
chuẩn đầu ra hứa một mức nhận thức mà chương trình không đưa người học tới.
"""

from typing import Any, Dict, List, Optional, Sequence, Tuple

from core.pedagogy.bloom import (
    audit_clo_alignment,
    covered_levels_from_tiers,
)


def _default_tiers() -> List[Dict[str, Optional[str]]]:
    """
    Bộ tầng bài tập ĐANG DÙNG THẬT, đọc trực tiếp từ nguồn thay vì chép tay.

    Chép tay một bản sao ở đây thì khi homework_creator đổi tầng, bộ kiểm này vẫn
    báo cáo theo bản cũ và không ai biết.
    """
    try:
        from agents.creators.homework_creator import SESSION_HOMEWORK_TIERS

        return [
            {"label": label, "pdf_level": pdf_level}
            for label, pdf_level in SESSION_HOMEWORK_TIERS
        ]
    except Exception:
        return []


def validate_clo_bloom_alignment(
    clos: Optional[Sequence[str]] = None,
    tiers: Optional[Sequence[Dict[str, Optional[str]]]] = None,
) -> Tuple[int, List[str], List[Dict[str, Any]]]:
    """
    Returns: (điểm trừ, danh sách vi phạm, nhật ký review)

    Mức phạt cố ý phân biệt theo mức nghiêm trọng:
      - CLO vượt quá độ phủ của chương trình: lỗi thiết kế chương trình, trừ nặng.
      - CLO dùng động từ không đo được: lỗi cách viết, trừ nhẹ nhưng vẫn phải sửa.
      - CLO không phân loại được: cảnh báo, không trừ điểm — có thể do bộ động từ
        của hệ thống chưa phủ hết cách diễn đạt, không chắc là lỗi của người viết.
    """
    clos = [c for c in (clos or []) if str(c or "").strip()]
    rule_violations: List[str] = []
    review_logs: List[Dict[str, Any]] = []
    deductions = 0

    if not clos:
        return 0, [], []

    tier_list = list(tiers) if tiers is not None else _default_tiers()
    covered = covered_levels_from_tiers(tier_list)

    issues = audit_clo_alignment(clos, covered)

    for issue in issues:
        message = issue.message()
        if issue.kind == "under_covered":
            deductions += 8
            level = "ERROR"
        elif issue.kind == "non_measurable":
            deductions += 3
            level = "ERROR"
        else:
            level = "WARNING"

        rule_violations.append(message)
        review_logs.append(
            {
                "level": level,
                "rule": "CLO_BLOOM_ALIGNMENT",
                "message": message,
            }
        )

    if covered:
        from core.pedagogy.bloom import BLOOM_LEVELS

        highest = max(covered, key=lambda lvl: lvl.order)
        covered_keys = {lvl.key for lvl in covered}
        gaps = [lvl for lvl in BLOOM_LEVELS if lvl.key not in covered_keys and lvl.order < highest.order]

        message = (
            f"Hệ bài tập phủ tới cấp Bloom '{highest.name_vi}' "
            f"({len(covered)}/{len(BLOOM_LEVELS)} cấp)."
        )
        if gaps:
            # Khoảng trống Ở GIỮA đáng nói hơn nhiều so với con số "4/6": nó cho biết
            # người học nhảy cóc qua một quá trình nhận thức. Ví dụ thực tế của hệ
            # hiện tại: có Phân tích, có Sáng tạo, nhưng không có bài nào yêu cầu
            # Đánh giá — chọn giải pháp tốt nhất theo tiêu chí rõ ràng.
            message += (
                " Khoảng trống ở giữa: "
                + ", ".join(lvl.name_vi for lvl in gaps)
                + " (người học nhảy cóc qua các quá trình nhận thức này)."
            )

        review_logs.append(
            {"level": "INFO", "rule": "CLO_BLOOM_ALIGNMENT", "message": message}
        )

    return deductions, rule_violations, review_logs
