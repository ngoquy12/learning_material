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
from typing import Dict, List

CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "/usr/bin/google-chrome", "/usr/bin/chromium", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B05\u2B06\u2B07\u21A9\uFE0F]")
BANNED_STYLE = ["backdrop-filter", "linear-gradient", "radial-gradient", "glass-card", "gradient-text",
                "animate-pulse", "animate-bounce", "blur(", "neon"]
BANNED_WORDS = ["nhé", "bẫy lập trình", "thần thánh", "bí kíp", "tất tần tật", "thân mến", "thực chiến",
                "gotcha", "anti-pattern", "khám phá", "tuyệt vời"]
MIN_FONT_ERROR_PX = 15
TOLERANCE_PX = 2

MEASURE_JS = """() => {
  const s = document.querySelector('.slide.active');
  if (!s) return null;
  return {sh: s.scrollHeight, ch: s.clientHeight, sw: s.scrollWidth, cw: s.clientWidth,
          dw: document.documentElement.scrollWidth, iw: window.innerWidth};
}"""

SMALL_FONT_JS = """() => {
  const out = {};
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n;
  while ((n = walker.nextNode())) {
    const t = n.textContent.trim();
    if (!t) continue;
    const el = n.parentElement;
    if (!el || ['SCRIPT', 'STYLE', 'NOSCRIPT'].includes(el.tagName)) continue;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    const px = parseFloat(cs.fontSize);
    const key = Math.round(px * 10) / 10;
    out[key] = (out[key] || 0) + 1;
  }
  return out;
}"""

CLICKABLE_JS = """() => {
  const s = document.querySelector('.slide.active');
  if (!s) return [];
  const list = [];
  s.querySelectorAll('button').forEach((b, idx) => {
    const on = b.getAttribute('onclick') || '';
    if (b.classList.contains('map-row') || /\\bgo\\(/.test(on)) return;
    if (b.offsetParent === null) return;
    list.push(idx);
  });
  return list;
}"""


def launch(p):
    try:
        return p.chromium.launch()
    except Exception:  # noqa: BLE001
        for path in CHROME_PATHS:
            if Path(path).exists():
                return p.chromium.launch(executable_path=path)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("html")
    parser.add_argument("--viewports", default="1366x768,1920x1080,1280x720")
    parser.add_argument("--shots", default=None, help="Thư mục lưu ảnh từng slide ở độ phân giải đầu tiên")
    parser.add_argument("--clicks", type=int, default=15, help="Số nút tối đa bấm thử mỗi slide")
    args = parser.parse_args()

    from playwright.sync_api import sync_playwright

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

    total = 0
    with sync_playwright() as p:
        browser = launch(p)
        for vi, (w, h) in enumerate(viewports):
            page = browser.new_page(viewport={"width": w, "height": h})
            console: List[str] = []
            page.on("pageerror", lambda e: console.append(str(e)))
            page.on("console", lambda m: console.append(m.text) if m.type == "error"
                    and "Failed to load resource" not in m.text and "net::" not in m.text else None)
            page.goto(path.as_uri())
            page.wait_for_timeout(2500)
            total = page.evaluate("document.querySelectorAll('.slide').length")
            tag = f"{w}x{h}"
            if vi == 0:
                sizes: Dict[float, int] = page.evaluate(SMALL_FONT_JS)
                small = {k: v for k, v in sizes.items() if float(k) < MIN_FONT_ERROR_PX}
                if small:
                    errors.append(f"chữ nhỏ hơn {MIN_FONT_ERROR_PX}px: " + ", ".join(f"{k}px x{v}" for k, v in sorted(small.items())))
                if not page.evaluate("typeof go === 'function'"):
                    errors.append("không có hàm go(i) để chuyển slide")
            bad_fit = []
            for i in range(total):
                page.evaluate(f"go({i})")
                page.wait_for_timeout(120)
                m = page.evaluate(MEASURE_JS)
                if m and m["sh"] > m["ch"] + TOLERANCE_PX:
                    bad_fit.append((i + 1, m["sh"] - m["ch"], "mặc định"))
                if m and (m["sw"] > m["cw"] + TOLERANCE_PX or m["dw"] > m["iw"] + TOLERANCE_PX):
                    errors.append(f"[{tag}] slide {i + 1}: tràn ngang")
                if shots_dir and vi == 0:
                    page.screenshot(path=str(shots_dir / f"slide_{i + 1:02d}.png"))
                # bấm thử các nút
                idxs = page.evaluate(CLICKABLE_JS)[: args.clicks]
                for idx in idxs:
                    try:
                        page.evaluate(
                            "(k) => document.querySelector('.slide.active').querySelectorAll('button')[k].click()", idx)
                    except Exception as exc:  # noqa: BLE001
                        console.append(f"slide {i + 1}: bấm nút {idx} lỗi: {exc}")
                        continue
                    page.wait_for_timeout(60)
                    if not page.evaluate("!!document.querySelector('.slide.active')"):
                        page.evaluate(f"go({i})")
                    mm = page.evaluate(MEASURE_JS)
                    if mm and mm["sh"] > mm["ch"] + TOLERANCE_PX:
                        bad_fit.append((i + 1, mm["sh"] - mm["ch"], f"sau khi bấm nút {idx}"))
                page.evaluate(f"go({i})")
            # gom lỗi tràn dọc
            seen = {}
            for slide, over, when in bad_fit:
                prev = seen.get(slide)
                if prev is None or over > prev[0]:
                    seen[slide] = (over, when)
            if seen:
                detail = ", ".join(f"slide {s} (+{o}px, {wh})" for s, (o, wh) in sorted(seen.items())[:12])
                more = "" if len(seen) <= 12 else f" và {len(seen) - 12} slide khác"
                errors.append(f"[{tag}] {len(seen)}/{total} slide tràn dọc: {detail}{more}")
            for msg in sorted(set(console))[:8]:
                errors.append(f"[{tag}] lỗi console: {msg[:160]}")
            page.close()
        browser.close()

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
