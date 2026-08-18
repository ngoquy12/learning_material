---
name: lecture_ui_reviewer
description: Visual and Layout Reviewer Agent for Interactive Classroom Lecture Dashboards (Visualizer / Bài giảng trên lớp). Automatically captures full-page browser screenshots using Playwright, detects layout overflow, console runtime errors, raw Jinja2 leaks, and performs Vision AI visual quality auditing against Rikkei Education standards.
---

# Classroom Lecture UI Reviewer Skill (Thẩm định Giao diện Bài giảng Trực quan)

This skill specifies the automated visual and structural review process for **Interactive Classroom Lecture Dashboards (`Visualizer/index.html` / `slides.html`)**.

---

## 1. PURPOSE & CAPABILITIES

1. **Automated Screenshot Capture**: Uses headless Chromium via Playwright at desktop viewports (`1680x1050` and `1920x1080`) to capture full-page rendering.
2. **Console Error Trapping**: Intercepts and records any uncaught JavaScript runtime exceptions or missing DOM element errors (`document.getElementById(...) is null`).
3. **Horizontal Layout Overflow Detection**: Programmatically evaluates `scrollWidth > innerWidth` to ensure zero horizontal scrollbar or clipped cards on wide screens.
4. **Template Integrity Check**: Verifies that no raw unrendered Jinja2 template tags (`{{ ... }}` or `undefined`) leaked into the final HTML output.
5. **AI Vision Quality Inspection**: Performs deep multimodal vision analysis against Rikkei Education UI standards (Contrast, Glassmorphism, Typography, Responsive Spacing, Simulators).
6. **Pass/Fail Certification**: Generates `lecture_ui_review_report.json` and `lecture_ui_review_report.md` with actionable fixes.

---

## 2. 10 CORE REVIEW CRITERIA

| # | Tiêu chí | Trọng số | Mô tả kiểm tra |
|---|---|---|---|
| 1 | **Khung chứa & Bố cục** | Critical (-25) | Max-width 1680px, căn giữa, không vỡ layout, không tràn viền màn hình ngang. |
| 2 | **Menu Mục lục bên trái** | Major (-15) | Cố định khi cuộn (`sticky top-24`), đồng bộ 100% tiêu đề với section, có active highlight. |
| 3 | **Thẻ Lý thuyết Glass-Card** | Major (-15) | Nền sáng mờ (`glass-card`), tương phản chữ tối trên nền sáng, đạn danh sách rõ ràng. |
| 4 | **Bộ Mô phỏng Tương tác** | Major (-20) | Điều khiển input đầy đủ, code box tối màu có highlight cú pháp, trace console hiển thị realtime. |
| 5 | **Không Rò rỉ Ký tự Raw** | Critical (-25) | Tuyệt đối không còn thẻ `{{`, `}}`, `undefined`, `NaN`, `[object Object]`. |
| 6 | **Độ tương phản & Font chữ** | Critical (-25) | Sử dụng Inter, Montserrat, JetBrains Mono. Cấm chữ xám mờ khó đọc trên nền tối. |
| 7 | **Tính Trực quan Sinh động** | Major (-15) | Có animation trực quan hóa luồng dữ liệu (`pulse-active`, sơ đồ chuyển trạng thái). |
| 8 | **Tính Sư phạm & Giải thích** | Minor (-10) | Tiến trình thực thi giải thích chi tiết, 100% Tiếng Việt có dấu chuẩn sản xuất. |
| 9 | **Tình huống Doanh nghiệp** | Minor (-10) | Dữ liệu mô phỏng gắn liền bài toán thực tế (E-commerce, auth, tính tiền...). |
| 10 | **Ổn định Script Runtime** | Critical (-25) | 0 lỗi console, không crash khi thay đổi input/select. |

---

## 3. AUDIT REPORT OUTPUT CONTRACT

Each review produces:
- `screenshots/index_preview.png`: High-resolution full-page screenshot.
- `lecture_ui_review_report.json`: Machine-readable audit scores and issues list.
- `lecture_ui_review_report.md`: Human-readable Markdown summary with approval badge.

---

## 4. USAGE EXAMPLE

```python
from agents.lecture_ui_reviewer_agent import lecture_ui_reviewer_agent

report = lecture_ui_reviewer_agent.review_lecture_ui(
    html_path="output/pms/Phát_triển_ứng_dụng_web/Session 04/Visualizer/index.html",
    session_title="Session 04 - Toán tử Số học, Toán tử So sánh và Biểu thức Logic trong JavaScript",
    tech_stack="JavaScript Vanilla (ES6+), HTML5/CSS3, DOM API"
)

if report["passed"]:
    print("UI Review Approved! Score:", report["ui_score"])
else:
    print("UI Review Needs Revision! Issues:", report["issues"])
```
