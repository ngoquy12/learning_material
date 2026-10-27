# Harness học liệu: thiết kế tổng thể

Ngày: 2026-10-27. Trạng thái: chờ duyệt.

## 1. Vấn đề

Kho Learning-Material có hai cách sinh học liệu:

1. **Pipeline Python** (`main.py` → LangGraph trong `core/graph.py`), gọi Gemini.
2. **Agent trong IDE** (Claude Code, Codex, Antigravity) làm theo `skills/<tên>/SKILL.md`.

Hai đường dùng chung tên tài nguyên nhưng không dùng chung "cổng" kiểm chứng:

- Mỗi skill tự có script kiểm tra riêng (`check_reading.py`, `deck_lint.py`, `check_deck.py`, `check_slides_html.py`).
- Pipeline có validator riêng (`core/validators/*`, `quality_gates.py`). Hai bên lệch nhau: anchor cũ và id `section-N`, mục 2.4 mô phỏng, khuyến nghị `[NOTE]`.
- Phần chạy thật (Vitest, MySQL tạm, tests.html trong trình duyệt) chỉ tồn tại dưới dạng script dùng một lần trong scratchpad khi làm môn ReactJS và NodeJS.
- Danh sách từ cấm, emoji, thẻ ngoặc vuông bị chép ở nhiều nơi.

Hệ quả: agent "tự cho là xong" mà không có cổng nào bắt buộc. Một harness chuẩn cần: đặc tả nhiệm vụ rõ, công cụ xác định, cổng kiểm chứng tự động, ranh giới quyền, nhật ký chạy và bộ hồi quy.

## 2. Quyết định đã chốt

- **Lõi chung cho cả hai đường**: một gói Python `core/harness/` vừa là thư viện cho pipeline, vừa là CLI `python -m core.harness` cho agent trong IDE.
- **Dự án con đầu tiên: cổng kiểm chứng** (`harness verify`).
- Ràng buộc giữ nguyên: chỉ dùng model Gemini có sẵn; không thiết kế lại phong cách bài đọc và slide; không hardcode giá trị riêng của một môn; không tạo user MySQL, không đụng cổng 3306.

## 3. Lộ trình các dự án con

| # | Dự án con | Đầu ra | Phụ thuộc |
|---|---|---|---|
| 1 | **Cổng kiểm chứng** | `python -m core.harness verify <đường dẫn>`: nhận diện loại tài nguyên, chạy đúng cổng, báo cáo JSON và Markdown, mã thoát 0/1/2 | không |
| 2 | Đặc tả môn và bộ lập lịch | `course_spec.yaml` (session, lesson, phạm vi cho phép, công nghệ), `harness plan` sinh danh sách nhiệm vụ theo đợt, trạng thái từng nhiệm vụ lưu trong `storage/harness/` | 1 |
| 3 | Một nguồn cho skill và prompt | Prompt `templates/prompts/*.j2` nạp quy tắc từ SKILL.md thay vì chép lại; validator đọc `text_rules` chung | 1 |
| 4 | Ranh giới quyền | `source_guard` thành hook dùng chung: khi sinh học liệu chỉ ghi `output/` và `storage/`; hook Claude Code gọi cùng hàm | 1 |
| 5 | Sổ ghi lần chạy | Mỗi lần `verify`/`plan` ghi một dòng JSONL (ai chạy, tài nguyên, cổng, kết quả, thời gian) vào `storage/harness/ledger.jsonl` | 1 |
| 6 | Bộ hồi quy | Hai môn đã duyệt (`reactjs_ai_driven`, `nodejs_ai_driven`) rút gọn thành fixture vàng; CI chạy `verify` trên fixture và so điểm | 1, 5 |

Mỗi dự án con có spec và plan riêng. Tài liệu này chỉ chi tiết dự án con 1.

## 4. Dự án con 1: cổng kiểm chứng

### 4.1 Hợp đồng

```
python -m core.harness verify <path> [--kind KIND] [--runtime] [--render] [--json] [--report-dir DIR]
```

- `<path>`: một tệp, thư mục một tài nguyên, thư mục session hoặc thư mục môn. Thư mục được duyệt đệ quy và mỗi tài nguyên nhận diện được chạy một cổng.
- `--kind`: ép loại khi đường dẫn không theo quy ước thư mục.
- `--runtime`: chạy phần thực thi (Vitest, MySQL tạm, trình duyệt). Mặc định chỉ kiểm tĩnh để nhanh và chạy được ở mọi máy.
- `--render`: với `.pptx`, xuất ảnh bằng PowerPoint COM (chỉ Windows).
- `--json`: in báo cáo JSON ra stdout thay cho bản tóm tắt.
- Báo cáo luôn được ghi vào `storage/harness_reports/<dấu thời gian>_<tên>/report.json` và `report.md` (hoặc `--report-dir`).
- **Mã thoát**: `0` không có lỗi; `1` có ít nhất một lỗi; `2` không có lỗi nhưng có cổng không chạy được vì thiếu công cụ (Playwright, Node, mysqld, PowerPoint). Mã 2 không bao giờ được hiểu là "đạt".

### 4.2 Loại tài nguyên và cổng

Quy ước thư mục lấy từ hai môn đã duyệt. Nhận diện theo tên thư mục cha và tên tệp, không theo tên môn. So khớp sau khi bỏ dấu tiếng Việt và không phân biệt hoa thường, vì các môn cũ dùng tên có dấu (`Slide bài giảng/`). Tệp không nhận diện được không chặn kết quả; báo cáo liệt kê chúng ở mức `info`.

| Kind | Nhận diện | Cổng tĩnh | Cổng chạy thật (`--runtime`) |
|---|---|---|---|
| `reading` | `Bai doc/*.html` | `validate_reading_material` + kiểm tra bổ sung của `check_reading.py` + `text_rules` | không |
| `slide_pptx` | `Slide bai giang/*.pptx` (kèm `slides.json` nếu có) | `deck_lint.lint_slides` trên `slides.json`; `check_deck.static_checks` trên `.pptx` | `--render`: `render_with_powerpoint` + `measured_checks` |
| `slide_html` | `Bai giang tren lop/slides.html` | phong cách cấm, emoji, `{{`, `href="#"`, từ cấm | đo vừa khung từng slide ở 1366x768, 1920x1080, 1280x720; lỗi console |
| `quiz_lesson` | `Quizz lesson/quiz.md` và `*.xlsx` | 5 câu, mỗi câu có loại trong {SYNTAX, EXECUTION_FLOW, CODE_TRACE, COMPARISON, TRAP_PREDICTION}, 4 phương án A–D, dòng `**Đáp án đúng:**`, `**Giải thích:**`, `**Phản hồi khi chọn sai:**`; xlsx sheet "Template Import Quiz", đúng 16 cột tiêu đề, số dòng câu = số câu md, đáp án khớp | không |
| `quiz_session` | `Quizz session/*.md` và `*.xlsx` | md 45 câu `### Câu N`, mỗi câu 4 phương án và `**Đáp án đúng:**`; xlsx sheet "Quiz Bank", 13 cột tiêu đề, 45 dòng câu, đáp án khớp md | không |
| `exercise` | `Bai tap/<N>_*/` | có `de_bai_bai_tap.md`, `tieu_chi_cham_diem_ai.md`, `starter/`; đề có 5 tiêu đề H3, 350–700 từ; có đáp án mẫu và `huong_dan_bai_N.md` dưới `tai_lieu_giang_vien/` | đáp án mẫu đạt 100% test; starter chạy được nhưng chưa đạt hết |
| `lab` | `Bai thuc hanh/lab_guide.md` | có các mục `## Lab N` có thời lượng, có `Tổng kết`, `Rubric`; mỗi Lab có "Kết quả mong đợi" | không |

Bộ chạy thật chọn theo nội dung `starter/` và đáp án, không theo tên môn:

- Có `package.json` với `vitest` → **runner Vitest** (workspace `node_modules` dùng chung, khóa theo tập dependency).
- Có thêm thư mục SQL khởi tạo hoặc biến `DB_*` trong `.env.example` → bật **MySQL tạm** (mysqld riêng, `--initialize-insecure`, chỉ 127.0.0.1, cổng trống ≠ 3306, xóa sau khi chạy).
- Có `tests.html` + `harness.js` → **runner trình duyệt** (gọi `window.report()`, đọc `window.__results`).
- Không khớp gì → cổng chạy thật báo `skipped` kèm lý do.

### 4.3 Mô hình kết quả

- `Finding(severity: "error"|"warning"|"info", gate: str, message: str, location: str = "")`.
- `GateResult(kind, path, gate, status: "pass"|"fail"|"skipped", findings, duration_s, detail: dict)`. `status = "fail"` khi có ít nhất một `error`; `"skipped"` khi thiếu công cụ.
- `Report(target, results, started_at)` với `exit_code`, `to_json()`, `to_markdown()`.

### 4.4 Một nguồn quy tắc văn bản

`core/harness/text_rules.py` giữ danh sách từ cấm, mẫu emoji, mẫu thẻ ngoặc vuông in hoa và mẫu chữ in hoa toàn bộ. Các script trong `skills/*/scripts/` và cổng đều nhập từ đây. Không đổi validator của pipeline trong dự án con này (thuộc dự án con 3).

### 4.5 Quan hệ với skill và pipeline

- Script trong skill (`check_reading.py`, `check_slides_html.py`, `check_deck.py`) giữ dòng lệnh cũ nhưng gọi cổng tương ứng, để hướng dẫn trong SKILL.md không đổi.
- `AGENTS.md` thêm một quy tắc: tài nguyên chỉ được báo "xong" khi `python -m core.harness verify <thư mục>` trả mã 0 (hoặc 2 kèm lý do công cụ thiếu được nêu rõ).
- Pipeline chưa gọi harness trong dự án con này; nối vào `final_compiler_and_publish` là việc của dự án con 2.

### 4.6 Ngoài phạm vi

Chấm chất lượng nội dung bằng LLM; sửa tự động; nối vào LangGraph; CI.
