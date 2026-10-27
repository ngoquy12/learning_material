---
name: lecture_ui_reviewer
description: Visual and layout reviewer for in-class lecture pages. Reviews the lecture dashboard (Visualizer/index.html) and projected slide decks (slides.html): measures per-slide vertical fit at 1366x768, 1536x864 and 1920x1080, horizontal overflow, console errors, raw template leaks and forbidden styles (blur, gradient, pulsing animation, emoji), then adds a vision review of a screenshot. Writes lecture_ui_review_report.json and .md.
---

# Lecture UI Reviewer Skill (Thẩm định giao diện bài giảng trên lớp)

Automated visual and structural review for **`Visualizer/index.html`** (scrolling dashboard) and **`Bai giang tren lop/slides.html`** (slide deck). The implementation is `agents/lecture_ui_reviewer_agent.py`; the generators are `classroom_lecture_generator` (dashboard) and `slide_html` (slides, which has its own stricter checker `skills/slide_html/scripts/check_slides_html.py`).

---

## 1. Checks and what each one measures

Deterministic checks run first, then a vision model reviews a screenshot. A deterministic failure cannot be outvoted by the vision score.

| Check | How | Effect |
|---|---|---|
| Screenshot | Headless browser at 1680x1050, full page | Input for the vision review |
| Console errors | Collects `pageerror` and `console.error` (network 404s ignored) | Critical (-25), blocks approval |
| Raw template leak | Searches for `{{ name }}` and `{% tag` | Critical (-25), blocks approval |
| Horizontal overflow | `scrollWidth > innerWidth` at 1680x1050, then at 1366x768, 1536x864, 1920x1080 | Major (-15) |
| **Slide vertical fit** | Deck mode: the page has at least 3 `.slide` blocks and a `go(i)` function. Activates each slide, compares `scrollHeight` with `clientHeight`, in the default state and after clicking each `.pane-tabs` button, at the three laptop and projector resolutions (tolerance 2 px) | Critical (-25), blocks approval |
| **Forbidden styles** | Static scan: `backdrop-filter`, `linear-gradient`, `radial-gradient`, `animate-pulse`, `animate-bounce`, `href="#"`, emoji in visible text | Major (-10 each, at most -20) |
| Layout not measurable | No browser available | Minor issue `Không đo được bố cục`; the result must not be read as "fits" |
| Vision review | Model scores the screenshot against the criteria below | Score is the minimum of the deterministic and the vision score |

Approval needs a score of at least 90, no script runtime error, no template leak and no slide overflow.

Notes:
- The browser is the Playwright Chromium, or the Chrome installed on the machine when Playwright's browsers were not downloaded.
- In deck mode only the active slide is visible, so the screenshot shows one slide; the per-slide measurement is what covers the whole deck.
- For slides, run `check_slides_html.py` as well: it also checks font size, button behavior and ALL CAPS.

---

## 2. Vision criteria (10 core)

| # | Tiêu chí | Trọng số | Mô tả kiểm tra |
|---|---|---|---|
| 1 | **Khung chứa và bố cục** | Critical (-25) | Chiều rộng tối đa 1680px, căn giữa, không vỡ layout, không tràn ngang. |
| 2 | **Menu mục lục bên trái** | Major (-15) | Cố định khi cuộn, đồng bộ tiêu đề với section, có active highlight. |
| 3 | **Thẻ lý thuyết phẳng** | Major (-15) | Thẻ nền trắng, viền slate (lớp `glass-card` chỉ là tên cũ), chữ tối trên nền sáng, danh sách rõ ràng. Không kính mờ, không gradient. |
| 4 | **Bộ mô phỏng tương tác** | Major (-20) | Điều khiển input đầy đủ, code box tối có highlight cú pháp, trace hiển thị theo thời gian thực. |
| 5 | **Không rò rỉ ký tự raw** | Critical (-25) | Không còn `{{`, `}}`, `undefined`, `NaN`, `[object Object]`. |
| 6 | **Độ tương phản và font chữ** | Critical (-25) | Inter, Montserrat, JetBrains Mono. Cấm chữ xám mờ khó đọc, nhất là trên nền tối. |
| 7 | **Tính trực quan** | Major (-15) | Có sơ đồ hoặc đánh dấu bước đang chạy (`pulse-active` nay là viền tĩnh). Phạt hoạt ảnh nhấp nháy, kính mờ và gradient. |
| 8 | **Tính sư phạm và giải thích** | Minor (-10) | Tiến trình thực thi giải thích chi tiết, 100% tiếng Việt có dấu. |
| 9 | **Tình huống doanh nghiệp** | Minor (-10) | Dữ liệu mô phỏng gắn bài toán thực tế. |
| 10 | **Ổn định script runtime** | Critical (-25) | 0 lỗi console, không crash khi đổi input hoặc select. |

---

## 3. Report contract

Each review writes next to the HTML file:
- `screenshots/<tên>_preview.png`: full-page screenshot.
- `lecture_ui_review_report.json`: `ui_score`, `passed`, `issues`, and the deterministic fields `slide_overflow` (list of `{slide, viewport, over_px, state}`), `horizontal_overflow_viewports`, `style_findings`, `layout_error`, `console_errors`, `raw_tag_leak`.
- `lecture_ui_review_report.md`: human-readable summary with the approval badge.

---

## 4. Usage

```python
from agents.lecture_ui_reviewer_agent import lecture_ui_reviewer_agent

report = lecture_ui_reviewer_agent.review_lecture_ui(
    html_path="<session folder>/Bai giang tren lop/slides.html",
    session_title="Session 01",
    tech_stack="JavaScript",
)
if not report["passed"]:
    for issue in report["issues"]:
        print(issue["severity"], issue["criterion"], issue["description"])
```
