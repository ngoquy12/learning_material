"""Kiểm tra slides.html (bài giảng chiếu trên lớp): vừa khung, lỗi console, phong cách bị cấm, cỡ chữ.

  python skills/slide_html/scripts/check_slides_html.py slides.html [--viewports 1366x768,1920x1080,1280x720]
                                                         [--shots thư_mục_ảnh] [--clicks 15]

Với từng độ phân giải: kích hoạt lần lượt từng slide bằng go(i), đo chiều cao nội dung so với khung (tràn DỌC
là lỗi hay gặp nhất), bấm thử các nút trong slide và đo lại sau mỗi lần bấm. Cần Playwright và Chrome.
Mã thoát 1 nếu có LỖI.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import List

HERE = Path(__file__).resolve().parent
_REPO = next((p for p in [HERE, *HERE.parents] if (p / "core" / "harness" / "text_rules.py").exists()), None)
if _REPO is not None and str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))
try:
    from core.harness.text_rules import BANNED_WORDS, EMOJI_RE as EMOJI  # noqa: E402
    from core.harness.runners.browser import (  # noqa: E402,F401
        CHROME_PATHS, CLICKABLE_JS, MEASURE_JS, SMALL_FONT_JS, TOLERANCE_PX, ToolUnavailable, measure_slides,
    )
except ImportError as _exc:
    raise SystemExit(f"Không nạp được core.harness ({_exc}): chạy script bên trong kho dự án.")

BANNED_STYLE = ["backdrop-filter", "linear-gradient", "radial-gradient", "glass-card", "gradient-text",
                "animate-pulse", "animate-bounce", "blur(", "neon"]
MIN_FONT_ERROR_PX = 15


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("html")
    parser.add_argument("--viewports", default="1366x768,1920x1080,1280x720")
    parser.add_argument("--shots", default=None, help="Thư mục lưu ảnh từng slide ở độ phân giải đầu tiên")
    parser.add_argument("--clicks", type=int, default=15, help="Số nút tối đa bấm thử mỗi slide")
    args = parser.parse_args()

    path = Path(args.html).resolve()
    source = path.read_text(encoding="utf-8", errors="replace")
    errors: List[str] = []
    warnings: List[str] = []

    # --- kiểm tĩnh ---
    if "{{" in source:
        errors.append("còn chỗ giữ chỗ {{...}} chưa thay")
    if re.search(r'href="#"', source):
        errors.append('có thẻ <a href="#">')
    for token in BANNED_STYLE:
        if token in source:
            errors.append(f"có phong cách bị cấm '{token}' (kính mờ, gradient, hoạt ảnh nhấp nháy)")
    visible = re.sub(r"<script.*?</script>|<style.*?</style>", "", source, flags=re.S)
    visible = re.sub(r"<[^>]+>", " ", visible)
    if EMOJI.search(visible):
        errors.append("có emoji hoặc ký tự biểu tượng trong nội dung")
    low = visible.lower()
    for word in BANNED_WORDS:
        if word in low:
            errors.append(f"có từ bị cấm '{word}'")

    viewports = [tuple(map(int, v.lower().split("x"))) for v in args.viewports.split(",")]
    shots_dir = Path(args.shots) if args.shots else None
    if shots_dir:
        shots_dir.mkdir(parents=True, exist_ok=True)
        for old in shots_dir.glob("slide_*.png"):
            old.unlink()

    try:
        m = measure_slides(path, viewports=viewports, clicks=args.clicks, shots_dir=shots_dir)
    except ToolUnavailable as exc:
        raise SystemExit(f"Không đo được slide: {exc}")
    total = m["slides"]
    small = {k: v for k, v in m["font_sizes"].items() if float(k) < MIN_FONT_ERROR_PX}
    if small:
        errors.append(f"chữ nhỏ hơn {MIN_FONT_ERROR_PX}px: " + ", ".join(f"{k}px x{v}" for k, v in sorted(small.items())))
    if not m["has_go"]:
        errors.append("không có hàm go(i) để chuyển slide")
    for w, h in viewports:
        tag = f"{w}x{h}"
        for o in m["horizontal_overflow"]:
            if o["viewport"] == tag:
                errors.append(f"[{tag}] slide {o['slide']}: tràn ngang")
        seen = [o for o in m["slide_overflow"] if o["viewport"] == tag]
        if seen:
            detail = ", ".join(f"slide {o['slide']} (+{o['over_px']}px, {o['state']})" for o in seen[:12])
            more = "" if len(seen) <= 12 else f" và {len(seen) - 12} slide khác"
            errors.append(f"[{tag}] {len(seen)}/{total} slide tràn dọc: {detail}{more}")
        for msg in m["console_errors"]:
            if msg.startswith(f"[{tag}] "):
                errors.append(f"[{tag}] lỗi console: {msg[len(tag) + 3:]}")

    if not 15 <= total <= 20:
        warnings.append(f"{total} slide; AGENTS.md quy định 15-20 slide mỗi buổi (buổi nhiều lesson có thể nhiều hơn, cần lý do)")

    if shots_dir:
        try:
            from PIL import Image
            files = sorted(shots_dir.glob("slide_*.png"))
            for k in range(0, len(files), 6):
                group = files[k:k + 6]
                rows = (len(group) + 1) // 2
                sheet = Image.new("RGB", (1600, 450 * rows), "white")
                for j, f in enumerate(group):
                    sheet.paste(Image.open(f).convert("RGB").resize((800, 450)), ((j % 2) * 800, (j // 2) * 450))
                out = shots_dir / f"sheet_{k // 6 + 1}.png"
                sheet.save(out)
                print("ẢNH", out)
        except Exception as exc:  # noqa: BLE001
            warnings.append(f"không ghép được ảnh: {exc}")

    print(f"Đã kiểm {total} slide ở {len(viewports)} độ phân giải.")
    for w in warnings:
        print("CẢNH BÁO", w)
    for e in errors:
        print("LỖI", e)
    print(f"{len(errors)} lỗi, {len(warnings)} cảnh báo")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
