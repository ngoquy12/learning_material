"""Quy tắc văn bản dùng chung cho các cổng kiểm chứng."""
from __future__ import annotations

import re

# Hợp của danh sách trong check_slides_html.py và deck_lint.py (đã khử trùng lặp).
BANNED_WORDS: tuple[str, ...] = (
    "nhé", "bẫy lập trình", "thần thánh", "bí kíp", "tất tần tật", "thân mến",
    "thực chiến", "gotcha", "anti-pattern", "khám phá", "tuyệt vời",
)
EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B05\u2B06\u2B07\u21A9\uFE0F]")
# Chỉ bắt thẻ viết hoa kiểu [NOTE], [TIP]; không bắt mảng trong mã như [userId].
BRACKET_TAG_RE = re.compile(r"\[[A-ZÀ-Ỹ][A-ZÀ-Ỹ ]{1,19}\]")


def find_banned_words(text: str) -> list[str]:
    low = text.lower()
    return [w for w in BANNED_WORDS if w in low]


def find_emoji(text: str) -> list[str]:
    return EMOJI_RE.findall(text)


def find_bracket_tags(text: str) -> list[str]:
    return BRACKET_TAG_RE.findall(text)


def find_all_caps(text: str, min_letters: int = 10) -> list[str]:
    """Các cụm chữ IN HOA liền nhau có từ min_letters chữ cái trở lên."""
    out: list[str] = []
    run: list[str] = []

    def flush() -> None:
        s = "".join(run).strip()
        if sum(ch.isalpha() for ch in s) >= min_letters:
            out.append(s)
        run.clear()

    for ch in text:
        if ch.isalpha() and ch.isupper() or (run and ch == " "):
            run.append(ch)
        else:
            flush()
    flush()
    return out
