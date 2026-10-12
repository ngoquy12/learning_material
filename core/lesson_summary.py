"""Tóm tắt nội dung bài đã sinh để làm ngữ cảnh cho tài nguyên cấp session."""

from __future__ import annotations

from typing import Any, Dict, List

from bs4 import BeautifulSoup


def _from_html(html: str, max_chars: int) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.extract()

    parts: List[str] = []
    for heading in soup.find_all(["h2", "h3"]):
        title = heading.get_text(" ", strip=True)
        if not title:
            continue
        para = heading.find_next("p")
        snippet = para.get_text(" ", strip=True)[:180] if para else ""
        parts.append(f"- {title}: {snippet}" if snippet else f"- {title}")
        if sum(len(p) for p in parts) >= max_chars:
            break
    return "\n".join(parts)[:max_chars]


def build_lesson_summary(lesson_title: str, final_state: Dict[str, Any], max_chars: int = 1500) -> str:
    """
    Tóm tắt thật từ bài đọc đã sinh (đề mục + câu mở đầu từng mục).

    Bản trước tìm khóa `reading_sections` mà `master_content` không bao giờ có, rồi nhồi
    thêm một khối ```python cố định, nên slide/bài tập/mindmap của mọi môn chỉ nhận
    được tên bài cộng một đoạn mã không liên quan.
    """
    summary = f"Bài học: {lesson_title}\n"
    html = str(final_state.get("html_content") or "")
    if html and "Empty outline" not in html and "ĐANG KHỞI TẠO" not in html:
        body = _from_html(html, max_chars)
        if body:
            return summary + body

    master = final_state.get("master_content")
    if isinstance(master, dict):
        concepts = master.get("key_concepts") or master.get("concepts") or []
        if isinstance(concepts, list) and concepts:
            names = [str(c.get("name", c)) if isinstance(c, dict) else str(c) for c in concepts]
            return summary + "Khái niệm chính: " + "; ".join(names)[:max_chars]
    return summary
