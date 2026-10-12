"""
Phản hồi của reviewer cho lần sinh lại kế tiếp.

Trước đây vòng "sinh -> duyệt -> sinh lại" chỉ ghi phản hồi vào `review_logs` mà
không creator nào đọc nó: lần sinh lại dùng đúng prompt cũ, nên (a) không có gì
buộc mô hình sửa lỗi đã bị chỉ ra, và (b) bộ nhớ đệm có thể trả lại chính bản đã
bị từ chối. Module này là kênh duy nhất đưa phản hồi từ vòng duyệt sang creator.
"""

from __future__ import annotations

from typing import Any, MutableMapping

_KEY = "retry_feedback"


def set_retry_feedback(state: MutableMapping[str, Any], part: str, feedback: str) -> None:
    """Ghi phản hồi cần sửa cho `part`; chuỗi rỗng nghĩa là xóa."""
    bucket = state.setdefault(_KEY, {})
    if feedback and feedback.strip():
        bucket[part] = feedback.strip()
    else:
        bucket.pop(part, None)


def clear_retry_feedback(state: MutableMapping[str, Any], part: str) -> None:
    set_retry_feedback(state, part, "")


def get_retry_feedback(state: MutableMapping[str, Any], part: str) -> str:
    return str((state.get(_KEY) or {}).get(part, "") or "")


def retry_feedback_block(state: MutableMapping[str, Any], part: str) -> str:
    """Khối văn bản chèn vào user prompt; rỗng khi đây là lần sinh đầu tiên."""
    feedback = get_retry_feedback(state, part)
    if not feedback:
        return ""
    return (
        "\n=== PHẢN HỒI TỪ LẦN DUYỆT TRƯỚC (BẮT BUỘC SỬA) ===\n"
        "Bản trước đã bị reviewer từ chối vì các lý do dưới đây. Bản mới PHẢI khắc phục "
        "từng điểm, không lặp lại lỗi cũ:\n"
        f"{feedback}\n"
        "=================================================\n"
    )
