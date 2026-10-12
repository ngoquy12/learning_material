"""So khớp từ khóa theo ranh giới từ, để phân loại không bị bắt nhầm bởi chuỗi con."""

import re
from typing import Iterable


def has_any_term(text: str, terms: Iterable[str]) -> bool:
    """
    True nếu `text` chứa một trong các `terms` như MỘT TỪ/CỤM TỪ nguyên vẹn.

    Khớp chuỗi con làm "ide" khớp "identifier", "lab" khớp "label", "go" khớp
    "algorithm", khiến bài bị xếp sai loại mà không có cảnh báo nào.
    """
    lowered = (text or "").lower()
    return any(re.search(r"(?<!\w)" + re.escape(t.lower()) + r"(?!\w)", lowered) for t in terms)
