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
