"""
core/pedagogy/bloom.py — Bloom's Cognitive Taxonomy: một nguồn định nghĩa duy nhất.

Bối cảnh: hệ thống hiện có ÍT NHẤT 2 bộ tên tầng độ khó KHÔNG THỐNG NHẤT, mỗi loại
tài nguyên tự đặt lại tên:

    - AGENTS.md §2.1 (chuẩn 6-bài tập cũ):
      "BASIC APPLICATION" / "ADVANCED APPLICATION" / "ANALYSIS" / "CREATIVE"
    - agents/creators/homework_creator.py (bộ 15 bài hiện hành):
      "Mức độ 1: Cơ bản - Debug lỗi" ... "Mức độ 5: Sáng tạo - Thiết kế Mini Module"

Cả hai đều THỰC SỰ diễn đạt đúng thang Bloom, chỉ khác cách đặt tên — nhưng vì không
có một bộ từ vựng chung, không cách nào audit tự động xem một session có phủ đủ các
cấp độ nhận thức mục tiêu hay không mà không phải đọc tay từng tên tầng.

Module này KHÔNG đổi hành vi sinh nội dung (không đụng tới prompt hay bộ tên hiện có).
Nó chỉ cung cấp: (1) định nghĩa 6 cấp Bloom chuẩn, (2) bộ phân loại ánh xạ các tên tầng
ĐANG DÙNG THẬT trong repo về đúng cấp Bloom, và (3) một validator tính độ phủ để phát
hiện khi nào một cấp bị bỏ sót — điều không ai nhìn ra được nếu chỉ đọc từng tên riêng lẻ.

Cố ý KHÔNG ép "Dễ / Trung bình / Khá / Giỏi / Xuất sắc" (agents/practice_agents.py) vào
đây: đó là thang ĐỘ KHÓ (difficulty), một trục khác hẳn quá trình NHẬN THỨC (cognitive
process) mà Bloom mô tả. Một bài "Xuất sắc" có thể vẫn chỉ yêu cầu ghi nhớ (Remember) ở
mức khó hơn, không tự động là "Sáng tạo" (Create). Gán nhầm 2 trục này vào nhau là ngụy
tạo sư phạm, nên hàm classify_tier() trả None cho các tên không thực sự mô tả một quá
trình nhận thức, thay vì đoán bừa.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence


@dataclass(frozen=True)
class BloomLevel:
    """Một cấp trong thang Bloom, theo đúng thứ tự từ thấp đến cao."""

    order: int
    key: str            # slug ổn định, dùng làm khoá tra cứu
    name_vi: str
    name_en: str
    description_vi: str


# 6 cấp Bloom chuẩn (phiên bản 2001, Anderson & Krathwohl) — thứ tự CỐ ĐỊNH từ thấp
# đến cao. Đây là NGUỒN DUY NHẤT định nghĩa thang này trong toàn bộ hệ thống.
BLOOM_LEVELS: List[BloomLevel] = [
    BloomLevel(1, "remember", "Ghi nhớ", "Remember",
               "Nhắc lại được cú pháp, khái niệm, định nghĩa đã học."),
    BloomLevel(2, "understand", "Hiểu", "Understand",
               "Giải thích được cơ chế hoạt động, phát hiện lỗi trong code có sẵn (debug)."),
    BloomLevel(3, "apply", "Vận dụng", "Apply",
               "Áp dụng kiến thức vào tình huống nghiệp vụ cụ thể, xử lý I/O và luồng hoàn chỉnh."),
    BloomLevel(4, "analyze", "Phân tích", "Analyze",
               "So sánh nhiều giải pháp, phân tích trade-off, tối ưu hệ thống có sẵn."),
    BloomLevel(5, "evaluate", "Đánh giá", "Evaluate",
               "Đánh giá và lựa chọn giải pháp tốt nhất dựa trên tiêu chí rõ ràng."),
    BloomLevel(6, "create", "Sáng tạo", "Create",
               "Tự thiết kế kiến trúc/schema mới từ đầu, không có khuôn mẫu sẵn."),
]

_LEVEL_BY_KEY: Dict[str, BloomLevel] = {lvl.key: lvl for lvl in BLOOM_LEVELS}


def get_level(key: str) -> BloomLevel:
    if key not in _LEVEL_BY_KEY:
        raise KeyError(f"Không có cấp Bloom nào với key='{key}'. Hợp lệ: {list(_LEVEL_BY_KEY)}")
    return _LEVEL_BY_KEY[key]


# =============================================================================
# Ánh xạ các bộ tên tầng ĐANG DÙNG THẬT trong repo về đúng cấp Bloom.
#
# Đây KHÔNG phải suy đoán — mỗi khoá dưới đây là chuỗi (hoặc từ khoá con) trích trực
# tiếp từ agents/creators/homework_creator.py::SESSION_HOMEWORK_TIERS và
# .agents/AGENTS.md §2.1. Khi một trong hai nơi đó đổi tên tầng, cập nhật tại đây —
# test_bloom.py sẽ đỏ nếu bộ tên thực tế trôi khỏi bảng ánh xạ này.
# =============================================================================

# Chuẩn 15-bài hiện hành (homework_creator.py) — khớp theo `pdf_level`, ổn định hơn
# nhiều so với khớp theo `level_name` (vốn có thể đổi câu chữ mà giữ nguyên ý nghĩa).
PDF_LEVEL_TO_BLOOM: Dict[str, str] = {
    "co_ban": "understand",     # Debug lỗi / Kiểm thử I&O — đọc hiểu code có sẵn
    "chuyen_sau": "apply",      # Xây dựng tính năng mới trên nghiệp vụ cụ thể
    "phan_tich": "analyze",     # So sánh giải pháp, trade-off, tối ưu
    "sang_tao": "create",       # Thiết kế Mini Module từ đầu, không khuôn mẫu
}

# Chuẩn 6-bài cũ (AGENTS.md §2.1) — khớp theo từ khoá con, không phân biệt hoa/thường.
_LEGACY_KEYWORD_TO_BLOOM: Dict[str, str] = {
    "basic application": "understand",
    "advanced application": "apply",
    "analysis": "analyze",
    "creative": "create",
}


def classify_tier(label: str, pdf_level: Optional[str] = None) -> Optional[BloomLevel]:
    """
    Phân loại một tên tầng (hoặc `pdf_level`) về đúng cấp Bloom.

    Args:
        label: Tên tầng hiển thị (vd "Mức độ 3: Nâng cao - Xây dựng tính năng mới").
        pdf_level: Khoá nội bộ ổn định nếu có (vd "chuyen_sau") — ưu tiên dùng khoá
            này khi có, vì nó không đổi ngay cả khi câu chữ hiển thị được viết lại.

    Returns:
        BloomLevel tương ứng, hoặc None nếu không nhận diện được — trả None thay vì
        đoán bừa, vì một cấp bị gán sai còn tệ hơn một cấp không phân loại được.
    """
    if pdf_level and pdf_level in PDF_LEVEL_TO_BLOOM:
        return get_level(PDF_LEVEL_TO_BLOOM[pdf_level])

    if not label:
        return None

    label_lower = label.strip().lower()
    for keyword, level_key in _LEGACY_KEYWORD_TO_BLOOM.items():
        if keyword in label_lower:
            return get_level(level_key)

    return None


@dataclass
class BloomCoverageReport:
    """Kết quả kiểm tra độ phủ nhận thức của một bộ tầng độ khó."""

    covered: List[BloomLevel] = field(default_factory=list)
    missing: List[BloomLevel] = field(default_factory=list)
    unclassified: List[str] = field(default_factory=list)

    @property
    def is_full_coverage(self) -> bool:
        return not self.missing

    @property
    def coverage_ratio(self) -> float:
        return len(self.covered) / len(BLOOM_LEVELS)

    def summary(self) -> str:
        covered_names = ", ".join(lvl.name_vi for lvl in self.covered) or "(không có)"
        if self.is_full_coverage:
            return f"Phủ đủ {len(BLOOM_LEVELS)}/{len(BLOOM_LEVELS)} cấp Bloom: {covered_names}."
        missing_names = ", ".join(lvl.name_vi for lvl in self.missing)
        return (
            f"Chỉ phủ {len(self.covered)}/{len(BLOOM_LEVELS)} cấp Bloom ({covered_names}). "
            f"THIẾU: {missing_names}."
        )


def audit_bloom_coverage(
    tiers: Sequence[Dict[str, Optional[str]]],
    expected_levels: Optional[Sequence[str]] = None,
) -> BloomCoverageReport:
    """
    Kiểm tra một danh sách tầng (mỗi tầng là dict có 'label' và/hoặc 'pdf_level') đã
    phủ đủ các cấp Bloom mong đợi hay chưa.

    Args:
        tiers: Danh sách dict, mỗi dict có khoá 'label' (tên hiển thị) và tuỳ chọn
            'pdf_level' (khoá nội bộ ổn định).
        expected_levels: Tập key cấp Bloom cần đạt (mặc định: cả 6 cấp). Một course
            CLO cụ thể có thể chỉ yêu cầu tới "apply" cho môn nhập môn — truyền
            ["remember", "understand", "apply"] trong trường hợp đó thay vì đòi hỏi
            "create" một cách phi thực tế.

    Không đoán bừa: tầng nào không phân loại được thì liệt vào `unclassified`, KHÔNG
    tính là đã phủ cấp nào cả.
    """
    expected_keys = list(expected_levels) if expected_levels is not None else [
        lvl.key for lvl in BLOOM_LEVELS
    ]

    covered_keys: set = set()
    unclassified: List[str] = []

    for tier in tiers:
        label = tier.get("label", "") or ""
        pdf_level = tier.get("pdf_level")
        level = classify_tier(label, pdf_level=pdf_level)
        if level is None:
            unclassified.append(label or str(pdf_level) or "(không rõ)")
        else:
            covered_keys.add(level.key)

    covered = [get_level(k) for k in expected_keys if k in covered_keys]
    missing = [get_level(k) for k in expected_keys if k not in covered_keys]

    return BloomCoverageReport(covered=covered, missing=missing, unclassified=unclassified)

# =============================================================================
# PHẦN 2: Đối chiếu CLO với độ phủ nhận thức thực tế
#
# Bộ kiểm định CLO sẵn có (core/pm_validators/clo_coverage_validator.py) chỉ kiểm
# ĐỘ PHỦ TỪ KHOÁ: thuật ngữ trong CLO có xuất hiện đâu đó trong chương trình không.
# Nó bỏ lọt loại lệch chuẩn nghiêm trọng hơn nhiều về mặt sư phạm:
#
#     CLO tuyên bố "Phân tích và đánh giá hiệu năng truy vấn", nhưng toàn bộ bài tập
#     phủ CLO đó chỉ dừng ở mức Vận dụng (viết được câu truy vấn chạy đúng).
#
# Từ khoá khớp hoàn hảo — "truy vấn", "hiệu năng" đều có mặt — nên bộ kiểm cũ cho
# qua. Nhưng chuẩn đầu ra đã hứa với người học và với hội đồng kiểm định một mức
# nhận thức mà chương trình không hề đưa họ tới. Đây chính là điều mà constructive
# alignment (Biggs) đòi hỏi phải khớp: chuẩn đầu ra ↔ hoạt động ↔ đánh giá.
# =============================================================================

# Động từ chỉ hành động trong chuẩn đầu ra, ánh xạ về cấp Bloom.
#
# Chỉ đưa vào đây những động từ có cấp RÕ RÀNG. Động từ đa nghĩa bị cố ý bỏ ra
# ngoài — xem _AMBIGUOUS_CLO_VERBS bên dưới.
CLO_VERB_TO_BLOOM: Dict[str, str] = {
    # Ghi nhớ
    "liệt kê": "remember",
    "kể tên": "remember",
    "nêu tên": "remember",
    "nhắc lại": "remember",
    "nhận biết": "remember",
    "gọi tên": "remember",
    "định nghĩa": "remember",
    # Hiểu
    "trình bày": "understand",
    "giải thích": "understand",
    "mô tả": "understand",
    "diễn giải": "understand",
    "tóm tắt": "understand",
    "minh hoạ": "understand",
    "minh họa": "understand",
    "phân biệt": "understand",
    "chỉ ra": "understand",
    # Vận dụng
    "vận dụng": "apply",
    "áp dụng": "apply",
    "sử dụng": "apply",
    "triển khai": "apply",
    "cài đặt": "apply",
    "thực hiện": "apply",
    "cấu hình": "apply",
    "tính toán": "apply",
    "viết được": "apply",
    "lập trình": "apply",
    # Phân tích
    "phân tích": "analyze",
    "đối chiếu": "analyze",
    "phân loại": "analyze",
    "phân rã": "analyze",
    "chẩn đoán": "analyze",
    "gỡ lỗi": "analyze",
    "truy vết": "analyze",
    "khảo sát": "analyze",
    # Đánh giá
    "đánh giá": "evaluate",
    "thẩm định": "evaluate",
    "phê bình": "evaluate",
    "nhận xét": "evaluate",
    "biện luận": "evaluate",
    "lựa chọn": "evaluate",
    "kiểm định": "evaluate",
    # Sáng tạo
    "thiết kế": "create",
    "sáng tạo": "create",
    "kiến tạo": "create",
    "đề xuất giải pháp": "create",
    "tổng hợp": "create",
    "phát triển": "create",
}

# Động từ ĐA NGHĨA — cố ý KHÔNG phân loại.
#
# "so sánh" là ví dụ điển hình: Anderson & Krathwohl xếp "comparing" vào cấp HIỂU,
# nhưng "so sánh các giải pháp và trade-off" trong repo này lại được coi là PHÂN
# TÍCH (xem PDF_LEVEL_TO_BLOOM["phan_tich"]). Cùng một động từ, hai cấp khác nhau
# tuỳ ngữ cảnh. Gán bừa một cấp còn tệ hơn để không phân loại được — đúng nguyên
# tắc đã áp dụng cho classify_tier() ở phần trên.
_AMBIGUOUS_CLO_VERBS: List[str] = [
    "so sánh",
    "xây dựng",   # xây dựng theo mẫu = Vận dụng; xây dựng từ đầu = Sáng tạo
    "giải quyết", # giải quyết bài tập mẫu = Vận dụng; giải quyết vấn đề mở = Sáng tạo
]

# Động từ KHÔNG ĐO ĐƯỢC — không mô tả hành vi nào quan sát hay khảo thí được.
#
# Đây không phải suy đoán: kho kinh nghiệm của chính hệ thống
# (skills/lessons_learned/SKILL.md) đã ghi lại nhiều lần rằng chuẩn đầu ra dùng
# những từ này bị reviewer trả về. Đưa vào code để biến một bài học lặp đi lặp lại
# thành ràng buộc kiểm được, thay vì tiếp tục nhắc LLM bằng lời.
NON_MEASURABLE_CLO_VERBS: List[str] = [
    "hiểu được",
    "hiểu rõ",
    "nắm được",
    "nắm vững",
    "nắm rõ",
    "ghi nhớ",
    "biết được",
    "làm quen",
    "ý thức được",
    "nhận thức được",
]


def find_non_measurable_verbs(clo_text: str) -> List[str]:
    """Trả về các động từ không đo được xuất hiện trong một CLO."""
    if not clo_text:
        return []
    lowered = clo_text.lower()
    return [v for v in NON_MEASURABLE_CLO_VERBS if v in lowered]


def classify_clo(clo_text: str) -> Optional[BloomLevel]:
    """
    Xác định cấp Bloom mà một chuẩn đầu ra ĐÒI HỎI, dựa trên động từ hành động.

    Khi một CLO chứa nhiều động từ ở các cấp khác nhau ("phân tích và thiết kế
    được kiến trúc"), lấy cấp CAO NHẤT: chuẩn đầu ra chỉ coi là đạt khi người học
    làm được phần khó nhất trong đó.

    Trả None khi không nhận ra động từ nào đã phân loại — không đoán bừa.
    """
    if not clo_text:
        return None

    lowered = clo_text.lower()
    matched = [
        _LEVEL_BY_KEY[level_key]
        for verb, level_key in CLO_VERB_TO_BLOOM.items()
        if verb in lowered
    ]
    if not matched:
        return None
    return max(matched, key=lambda lvl: lvl.order)


def find_ambiguous_verbs(clo_text: str) -> List[str]:
    """Các động từ đa nghĩa trong CLO — cần người viết nói rõ mức độ mong muốn."""
    if not clo_text:
        return []
    lowered = clo_text.lower()
    return [v for v in _AMBIGUOUS_CLO_VERBS if v in lowered]


@dataclass(frozen=True)
class CloAlignmentIssue:
    """Một điểm lệch giữa chuẩn đầu ra và độ phủ nhận thức thực tế."""

    clo_text: str
    kind: str          # "under_covered" | "non_measurable" | "unclassifiable" | "ambiguous"
    required_level: Optional[BloomLevel] = None
    highest_covered: Optional[BloomLevel] = None
    detail: str = ""

    def message(self) -> str:
        short = self.clo_text.strip()
        if len(short) > 90:
            short = short[:87] + "..."
        if self.kind == "under_covered":
            req = self.required_level.name_vi if self.required_level else "?"
            cov = self.highest_covered.name_vi if self.highest_covered else "(không có)"
            return (
                f"CLO đòi hỏi mức nhận thức '{req}' nhưng hệ bài tập chỉ phủ tới "
                f"'{cov}': \"{short}\""
            )
        if self.kind == "non_measurable":
            return (
                f"CLO dùng động từ không đo được ({self.detail}) — không khảo thí "
                f"được: \"{short}\""
            )
        if self.kind == "ambiguous":
            return (
                f"CLO dùng động từ đa nghĩa ({self.detail}), không xác định được mức "
                f"nhận thức mong muốn: \"{short}\""
            )
        return f"Không xác định được mức nhận thức của CLO: \"{short}\""


def covered_levels_from_tiers(
    tiers: Sequence[Dict[str, Optional[str]]]
) -> List[BloomLevel]:
    """Các cấp Bloom mà một bộ tầng bài tập thực sự phủ, sắp theo thứ tự tăng dần."""
    report = audit_bloom_coverage(tiers)
    return sorted(report.covered, key=lambda lvl: lvl.order)


def audit_clo_alignment(
    clos: Sequence[str],
    covered_levels: Sequence[BloomLevel],
) -> List[CloAlignmentIssue]:
    """
    Đối chiếu từng CLO với cấp Bloom cao nhất mà chương trình thực sự đưa người học tới.

    Args:
        clos: Danh sách phát biểu chuẩn đầu ra.
        covered_levels: Các cấp Bloom mà hệ bài tập/đánh giá phủ được — lấy từ
            covered_levels_from_tiers() trên đúng bộ tầng đang dùng thật.

    Returns:
        Danh sách điểm lệch. Rỗng nghĩa là mọi CLO đều được chương trình đưa tới
        đúng mức nhận thức đã tuyên bố.
    """
    issues: List[CloAlignmentIssue] = []
    highest = max(covered_levels, key=lambda lvl: lvl.order) if covered_levels else None

    for clo in clos:
        text = str(clo or "").strip()
        if not text:
            continue

        non_measurable = find_non_measurable_verbs(text)
        if non_measurable:
            issues.append(
                CloAlignmentIssue(
                    clo_text=text,
                    kind="non_measurable",
                    detail=", ".join(non_measurable),
                )
            )
            continue

        required = classify_clo(text)
        if required is None:
            ambiguous = find_ambiguous_verbs(text)
            issues.append(
                CloAlignmentIssue(
                    clo_text=text,
                    kind="ambiguous" if ambiguous else "unclassifiable",
                    detail=", ".join(ambiguous),
                )
            )
            continue

        if highest is None or required.order > highest.order:
            issues.append(
                CloAlignmentIssue(
                    clo_text=text,
                    kind="under_covered",
                    required_level=required,
                    highest_covered=highest,
                )
            )

    return issues
