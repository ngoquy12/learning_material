"""
Đưa kinh nghiệm đã học (kho tri thức KMA) tới creator và reviewer, và lọc nhật ký
reviewer trước khi học từ chúng.

Trước đây `state["lessons_learned_prompt"]` được ghi ở node_generate_master_content
nhưng chỉ bước sinh master_content đọc nó; bài đọc, quiz, lab và reviewer không bao
giờ thấy. Ngược lại kho tri thức học từ MỌI dòng nhật ký, kể cả traceback của batch,
báo lỗi phạm vi riêng từng bài và câu "không đọc được phán quyết", nên quy tắc học
được là nhiễu.
"""

from __future__ import annotations

from typing import Any, Dict, List, Mapping

MAX_MEMORY_CHARS = 1500

# Chỉ các nguồn này phản ánh lỗi CHẤT LƯỢNG NỘI DUNG có tính tái diễn.
LEARNABLE_SOURCES = frozenset(
    {"UX_Reviewer", "Academic_Reviewer", "Sandbox_Agent", "Objective_Reviewer"}
)

_NOISE_MARKERS = ("không trả về phán quyết đọc được",)


def memory_prompt_block(state: Mapping[str, Any], max_chars: int = MAX_MEMORY_CHARS) -> str:
    """Khối kinh nghiệm để nối vào prompt; rỗng khi chưa có."""
    text = str(state.get("lessons_learned_prompt") or "").strip()
    if not text:
        return ""
    if len(text) > max_chars:
        text = text[:max_chars].rsplit("\n", 1)[0]
    return f"\n{text}\n"


def learnable_review_logs(logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Giữ lại nhật ký đáng học: đúng nguồn reviewer nội dung, có lý do, không phải nhiễu."""
    kept = []
    for log in logs or []:
        source = str(log.get("source", ""))
        feedback = str(log.get("feedback", "")).strip()
        if source not in LEARNABLE_SOURCES or not feedback:
            continue
        if any(marker in feedback for marker in _NOISE_MARKERS):
            continue
        kept.append(log)
    return kept
