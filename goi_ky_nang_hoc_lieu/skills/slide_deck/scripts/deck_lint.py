"""Kiểm tra dữ liệu slide (JSON) TRƯỚC khi dựng: cấu trúc, mật độ chữ, giới hạn của bộ dựng.

Bộ dựng `core/renderers/pptx/deck_engine.py` cắt âm thầm danh sách dài (tối đa 5 mục, 150 ký tự mỗi mục;
bài tập tối đa 3 mục, 95 ký tự), nên mọi vượt giới hạn ở đây là LỖI: nội dung sẽ mất, không phải cảnh báo.

Dùng độc lập:  python deck_lint.py slides.json
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

# Quy tắc văn bản (từ cấm, emoji, thẻ [NOTE]) dùng chung một nguồn: core/harness/text_rules.py.
_HERE = Path(__file__).resolve().parent
_REPO = next((p for p in [_HERE, *_HERE.parents] if (p / "core" / "harness" / "text_rules.py").exists()), None)
if _REPO is not None and str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))
try:
    from core.harness.text_rules import (  # noqa: E402
        BANNED_WORDS as BANNED, BRACKET_TAG_RE as BRACKET_TAG, EMOJI_RE as EMOJI,
    )
except ImportError as _exc:
    raise SystemExit(f"Không nạp được core.harness ({_exc}): chạy script bên trong kho dự án.")

TYPES = {
    "cover", "agenda", "objectives", "comparison_2col", "code_right_card", "code_trace_table",
    "grid2x2", "glossary_table", "summary_2col", "exercises", "interactive", "flowchart",
    "timeline", "closing",
}
NEEDS_H2 = TYPES - {"cover", "agenda", "objectives", "closing"}
CONTENT_TYPES = TYPES - {"cover", "agenda", "objectives", "closing", "glossary_table", "summary_2col", "exercises"}


# (số mục tối đa, số ký tự tối đa mỗi mục) mà bộ dựng giữ lại; vượt là bị cắt.
LIST_LIMITS = {
    "comparison_2col": {"left_items": (5, 150), "right_items": (5, 150)},
    "code_right_card": {"card_items": (5, 150)},
    "summary_2col": {"left_items": (5, 150), "right_items": (5, 150)},
    "exercises": {"exercises": (3, 95), "references": (3, 95)},
}


def _walk_strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for v in value.values():
            yield from _walk_strings(v)
    elif isinstance(value, list):
        for v in value:
            yield from _walk_strings(v)


def _item_text(item: Any) -> str:
    return item.get("text", "") if isinstance(item, dict) else str(item)


def lint_slides(slides: List[Dict[str, Any]]) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []
    n = len(slides)

    def err(i, msg):
        errors.append(f"slide {i + 1}: {msg}")

    def warn(i, msg):
        warnings.append(f"slide {i + 1}: {msg}")

    if n < 10 or n > 22:
        errors.append(f"tổng số slide {n} ngoài khoảng 10-22")
    elif n < 14 or n > 18:
        warnings.append(f"tổng số slide {n} ngoài khoảng khuyến nghị 14-18")

    types = [s.get("type", "") for s in slides]
    if types[:3] != ["cover", "agenda", "objectives"]:
        errors.append("ba slide đầu phải là cover, agenda, objectives theo thứ tự")
    if types and types[-1] != "closing":
        errors.append("slide cuối phải là closing")
    if n >= 3 and types[-2] != "summary_2col":
        errors.append("slide kế cuối phải là summary_2col")
    if n >= 4 and types[-3] != "exercises":
        errors.append("slide thứ ba từ cuối phải là exercises")
    if "glossary_table" in types and "exercises" in types and types.index("glossary_table") > types.index("exercises"):
        errors.append("glossary_table phải đứng trước exercises")

    seen_h2: Dict[str, int] = {}
    since_interactive = 0
    for i, s in enumerate(slides):
        t = s.get("type", "")
        if t not in TYPES:
            err(i, f"type '{t}' không được hỗ trợ (chỉ dùng: {', '.join(sorted(TYPES))})")
            continue

        text_all = " ".join(_walk_strings({k: v for k, v in s.items() if k != "notes"}))
        if EMOJI.search(text_all + " " + str(s.get("notes", ""))):
            err(i, "có emoji hoặc ký tự biểu tượng")
        low = (text_all + " " + str(s.get("notes", ""))).lower()
        for word in BANNED:
            if word in low:
                err(i, f"có từ bị cấm '{word}'")
        if BRACKET_TAG.search(text_all):
            err(i, "có thẻ ngoặc vuông kiểu [NOTE]")

        notes = str(s.get("notes", s.get("speaker_notes", ""))).strip()
        if not notes:
            err(i, "thiếu notes (ghi chú giảng)")
        elif "[~" not in notes:
            warn(i, "notes chưa có thời lượng dạng [~N phút]")

        h1, h2 = str(s.get("h1", "")), str(s.get("h2", ""))
        if t in NEEDS_H2:
            if not h2.strip():
                err(i, "thiếu h2 (mệnh đề khẳng định)")
            else:
                key = re.sub(r"\W+", " ", h2.lower()).strip()
                if key in seen_h2:
                    err(i, f"h2 trùng với slide {seen_h2[key] + 1}")
                seen_h2[key] = i
                if len(h2.split()) < 5:
                    warn(i, "h2 quá ngắn, chưa là mệnh đề khẳng định")
                if len(h2) > 100:
                    warn(i, f"h2 dài {len(h2)} ký tự (khuyến nghị dưới 100)")
        if len(h1) > 60:
            warn(i, f"h1 dài {len(h1)} ký tự (khuyến nghị dưới 60)")
        m = re.search(r"(\d+)\s*/\s*(\d+)\s*$", h1)
        if m and int(m.group(1)) > int(m.group(2)):
            err(i, f"h1 đánh số {m.group(1)}/{m.group(2)} sai")

        # Danh sách bị cắt
        for field, (max_items, max_chars) in LIST_LIMITS.get(t, {}).items():
            items = s.get(field, [])
            if len(items) > max_items:
                err(i, f"{field} có {len(items)} mục, bộ dựng chỉ giữ {max_items}")
            for item in items[:max_items]:
                if len(_item_text(item)) > max_chars:
                    err(i, f"mục trong {field} dài {len(_item_text(item))} ký tự, bộ dựng cắt ở {max_chars}")

        if t == "agenda" and len(s.get("items", [])) > 7:
            warn(i, "agenda quá 7 mục, có thể tràn khung")
        if t == "objectives" and len(s.get("goals", [])) > 5:
            err(i, "objectives chỉ giữ 5 mục tiêu")
        if t == "grid2x2" and len(s.get("items", [])) > 4:
            err(i, "grid2x2 chỉ giữ 4 ô")
        if t == "flowchart" and len(s.get("nodes", [])) > 7:
            err(i, "flowchart chỉ giữ 7 nút")
        if t == "timeline" and len(s.get("milestones", [])) > 6:
            err(i, "timeline chỉ giữ 6 mốc")
        if t == "comparison_2col":
            for side in ("left_code", "right_code"):
                if len(str(s.get(side, "")).strip().splitlines()) > 5:
                    err(i, f"{side} quá 5 dòng, bộ dựng chỉ giữ 5 dòng đầu")
        for field in ("code_snippet",):
            if len(str(s.get(field, "")).strip().splitlines()) > 12:
                err(i, f"{field} quá 12 dòng, sẽ tràn khối mã")
        if t in ("code_trace_table", "glossary_table"):
            rows = s.get("table_rows" if t == "code_trace_table" else "rows", [])
            if len(rows) > 8:
                err(i, f"bảng có {len(rows)} hàng, tối đa 8")
            elif len(rows) > 7:
                warn(i, "bảng 8 hàng sát mép dưới")
            for row in rows:
                for cell in row:
                    if len(str(cell)) > 45:
                        warn(i, f"ô bảng dài {len(str(cell))} ký tự, dễ xuống nhiều dòng")
                        break

        if t == "interactive":
            if not s.get("prompt"):
                err(i, "interactive thiếu prompt")
            if not s.get("answer"):
                err(i, "interactive thiếu answer (đáp án chỉ vào notes)")
            pattern = s.get("pattern", "quick_quiz")
            if pattern not in ("predict_outcome", "find_the_bug", "quick_quiz"):
                err(i, f"pattern '{pattern}' không hợp lệ")
            opts = s.get("options", [])
            if pattern == "quick_quiz" and not 3 <= len(opts) <= 5:
                err(i, "quick_quiz cần 3-5 phương án")
            if s.get("answer") and str(s["answer"]).strip() and str(s["answer"]).strip() in str(s.get("prompt", "")):
                warn(i, "đáp án xuất hiện trong prompt")

        if t == "interactive":
            since_interactive = 0
        elif t in CONTENT_TYPES:
            since_interactive += 1
            if since_interactive >= 4:
                warn(i, "đã 4 slide nội dung liên tiếp chưa có slide interactive")
                since_interactive = 0

    return errors, warnings


def load_slides(path: Path) -> List[Dict[str, Any]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return data["slides"] if isinstance(data, dict) else data


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("Cách dùng: python deck_lint.py slides.json")
    errs, warns = lint_slides(load_slides(Path(sys.argv[1])))
    for w in warns:
        print("CẢNH BÁO", w)
    for e in errs:
        print("LỖI", e)
    print(f"{len(errs)} lỗi, {len(warns)} cảnh báo")
    sys.exit(1 if errs else 0)
