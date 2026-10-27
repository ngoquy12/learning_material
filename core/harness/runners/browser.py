"""Bộ chạy trình duyệt (Playwright): đo vừa khung slides.html và chạy tests.html + harness.js.

Chromium của Playwright, dự phòng Chrome cài sẵn trên máy. Thiếu Playwright hoặc trình duyệt → ToolUnavailable.
Hằng số JS ở đây cũng được `skills/slide_html/scripts/check_slides_html.py` dùng lại.
"""
from __future__ import annotations

from pathlib import Path

from core.harness.runners import RunnerError, ToolUnavailable, tooling

DEFAULT_VIEWPORTS = [(1366, 768), (1920, 1080), (1280, 720)]
TOLERANCE_PX = 2
TESTS_TIMEOUT_S = 30
CHROME_PATHS = tooling.CHROME_PATHS

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


def _sync_playwright():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise ToolUnavailable(f"Chưa cài Playwright cho Python ({exc})") from exc
    return sync_playwright


def launch_browser(playwright):
    """Chromium của Playwright; nếu chưa tải trình duyệt thì dùng Chrome cài sẵn trên máy."""
    try:
        return playwright.chromium.launch(headless=True)
    except Exception as first:  # noqa: BLE001
        chrome = tooling.find_chrome()
        if not chrome:
            raise ToolUnavailable(f"Không mở được Chromium của Playwright và không tìm thấy Chrome: {first}") from first
        try:
            return playwright.chromium.launch(headless=True, executable_path=chrome)
        except Exception as exc:  # noqa: BLE001
            raise ToolUnavailable(f"Không mở được Chrome tại {chrome}: {exc}") from exc


def _watch_console(page, sink: list[str]) -> None:
    page.on("pageerror", lambda e: sink.append(str(e)))
    page.on("console", lambda m: sink.append(m.text) if m.type == "error"
            and "Failed to load resource" not in m.text and "net::" not in m.text else None)


def measure_slides(html: Path, viewports=None, clicks: int = 15, shots_dir: Path | None = None,
                   settle_ms: int = 2500) -> dict:
    """Kích hoạt từng slide bằng go(i), đo tràn dọc/ngang ở mỗi độ phân giải, bấm thử nút và đo lại.

    Trả về `{slides, slide_overflow: [{slide, viewport, over_px, state}], horizontal_overflow: [{slide, viewport}],
    console_errors: ["[WxH] ..."], font_sizes: {px: số nút chữ} (độ phân giải đầu), has_go}`.
    `slide_overflow` giữ mức tràn lớn nhất của mỗi (slide, độ phân giải) khi vượt TOLERANCE_PX.
    """
    viewports = list(viewports or DEFAULT_VIEWPORTS)
    path = Path(html).resolve()
    sync_playwright = _sync_playwright()
    out = {"slides": 0, "slide_overflow": [], "horizontal_overflow": [], "console_errors": [],
           "font_sizes": {}, "has_go": True}
    with sync_playwright() as p:
        browser = launch_browser(p)
        try:
            for vi, (w, h) in enumerate(viewports):
                tag = f"{w}x{h}"
                page = browser.new_page(viewport={"width": w, "height": h})
                console: list[str] = []
                _watch_console(page, console)
                page.goto(path.as_uri())
                page.wait_for_timeout(settle_ms)
                total = page.evaluate("document.querySelectorAll('.slide').length")
                out["slides"] = total
                if vi == 0:
                    out["font_sizes"] = page.evaluate(SMALL_FONT_JS)
                    out["has_go"] = bool(page.evaluate("typeof go === 'function'"))
                if not out["has_go"]:
                    page.close()
                    break
                worst: dict[int, tuple[int, str]] = {}
                horizontal: set[int] = set()

                def record(i: int, m: dict | None, state: str) -> None:
                    if not m:
                        return
                    over = m["sh"] - m["ch"]
                    if over > TOLERANCE_PX and (i not in worst or over > worst[i][0]):
                        worst[i] = (over, state)
                    if m["sw"] > m["cw"] + TOLERANCE_PX or m["dw"] > m["iw"] + TOLERANCE_PX:
                        horizontal.add(i)

                for i in range(total):
                    page.evaluate(f"go({i})")
                    page.wait_for_timeout(120)
                    record(i + 1, page.evaluate(MEASURE_JS), "mặc định")
                    if shots_dir and vi == 0:
                        page.screenshot(path=str(Path(shots_dir) / f"slide_{i + 1:02d}.png"))
                    for idx in page.evaluate(CLICKABLE_JS)[:clicks]:
                        try:
                            page.evaluate(
                                "(k) => document.querySelector('.slide.active').querySelectorAll('button')[k].click()",
                                idx)
                        except Exception as exc:  # noqa: BLE001
                            console.append(f"slide {i + 1}: bấm nút {idx} lỗi: {exc}")
                            continue
                        page.wait_for_timeout(60)
                        if not page.evaluate("!!document.querySelector('.slide.active')"):
                            page.evaluate(f"go({i})")
                        record(i + 1, page.evaluate(MEASURE_JS), f"sau khi bấm nút {idx}")
                    page.evaluate(f"go({i})")
                out["slide_overflow"] += [{"slide": s, "viewport": tag, "over_px": o, "state": st}
                                          for s, (o, st) in sorted(worst.items())]
                out["horizontal_overflow"] += [{"slide": s, "viewport": tag} for s in sorted(horizontal)]
                out["console_errors"] += [f"[{tag}] {msg[:160]}" for msg in sorted(set(console))[:8]]
                page.close()
        finally:
            browser.close()
    return out


def run_tests_html(html: Path) -> dict:
    """Mở tests.html, gọi `window.report()`, đợi `window.__results.done`; trả `{passed, total, results}`."""
    path = Path(html).resolve()
    sync_playwright = _sync_playwright()
    with sync_playwright() as p:
        browser = launch_browser(p)
        try:
            page = browser.new_page()
            console: list[str] = []
            _watch_console(page, console)
            page.goto(path.as_uri())
            if not page.evaluate("typeof window.report === 'function'"):
                raise RunnerError("tests.html không có hàm window.report() (thiếu harness.js?)")
            page.evaluate("() => { window.report(); }")
            try:
                page.wait_for_function("() => window.__results && window.__results.done === true",
                                       timeout=TESTS_TIMEOUT_S * 1000)
            except Exception as exc:  # noqa: BLE001
                raise RunnerError(f"tests.html chưa xong sau {TESTS_TIMEOUT_S} giây") from exc
            data = page.evaluate("() => window.__results")
        finally:
            browser.close()
    results = list(data.get("results") or [])
    passed = int(data.get("passed", 0))
    total = int(data.get("total", len(results)))
    return {"passed": passed, "failed": total - passed, "total": total,
            "ok": total > 0 and passed == total, "results": results,
            "failed_tests": [r.get("name", "") for r in results if not r.get("ok")],
            "suite_errors": [], "console_errors": sorted(set(console))[:8]}
