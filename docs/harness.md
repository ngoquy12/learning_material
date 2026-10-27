# Harness kiểm chứng học liệu

Harness (`core/harness/`) kiểm tra học liệu đã sinh theo chuẩn của dự án trước khi báo xong. Thiết kế: `docs/superpowers/specs/2026-10-27-harness-design.md`.

## Cách dùng

```bash
python -m core.harness verify <đường dẫn> [--kind K] [--runtime] [--render] [--json] [--report-dir DIR]
```

- `<đường dẫn>`: một tệp, một thư mục bài (bài tập, quiz) hoặc cả thư mục môn. Với thư mục môn, harness tự duyệt và chạy cổng phù hợp cho từng tài nguyên.
- `--kind K`: với một tệp hoặc một thư mục chứa một tài nguyên (thư mục bài tập, thư mục quiz): ép loại khi không nhận diện được từ tên. Với thư mục môn có nhiều tài nguyên: chỉ chạy các tài nguyên thuộc loại `K` (không có tài nguyên nào loại `K` thì báo lỗi).
- `--runtime`: chạy thật (Vitest, MySQL tạm, trình duyệt).
- `--render`: đo chữ tràn bằng PowerPoint (chỉ slide `.pptx`, chỉ Windows).
- `--json`: in báo cáo JSON ra màn hình thay cho bản tóm tắt.
- `--report-dir DIR`: ghi báo cáo vào `DIR` thay cho thư mục mặc định. `DIR` không được nằm trong thư mục đang kiểm chứng (lệnh từ chối, mã 1).

## Loại tài nguyên (`--kind`)

| Kind | Nhận diện | Kiểm tra |
| --- | --- | --- |
| `reading` | `Bài đọc/*.html` | Cấu trúc 5 mục, từ cấm, emoji, ngân sách từ |
| `slide_pptx` | `Slide bài giảng/*.pptx` | Kiểm tĩnh bộ slide; `--render` đo chữ tràn bằng PowerPoint |
| `slide_html` | `Bài giảng trên lớp/slides.html` | Kiểm tĩnh; `--runtime` đo vừa khung và lỗi console |
| `quiz_lesson` | `Quizz lesson/` (`quiz.md`, `.xlsx`) | Định dạng và quy tắc câu hỏi quiz bài |
| `quiz_session` | `Quizz session/` (`.md`, `.xlsx`) | Định dạng và quy tắc câu hỏi quiz buổi |
| `exercise` | `Bài tập/<số>_<tên>/` | Kiểm tĩnh đề, rubric, starter; `--runtime` chạy test của đáp án mẫu và starter |
| `lab` | `Bài thực hành/lab_guide.md` | Có mục `## Lab N - ... (K phút)` với số Lab tăng dần, không trùng; mỗi Lab có "Kết quả mong đợi" ngoài khối mã; có mục `Tổng kết` và `Rubric` |

Nhận diện theo tên thư mục cha, không phân biệt hoa thường và dấu tiếng Việt.

Tệp không nhận diện được trong một cây có tài nguyên chỉ được liệt kê ở mức `info` (trạng thái `unknown`, đếm riêng, không tính là đạt). Một tệp lẻ không nhận diện được (không có `--kind`), hoặc một thư mục không có tài nguyên nào được nhận diện, là lỗi (mã 1).

## Mã thoát

| Mã | Ý nghĩa |
| --- | --- |
| 0 | Mọi cổng đạt |
| 1 | Có ít nhất một lỗi (error); đường dẫn không tồn tại; không nhận diện được tài nguyên nào; hoặc `--report-dir` nằm trong đích |
| 2 | Không có lỗi nhưng một cổng bị bỏ qua vì thiếu công cụ. Không bao giờ được coi là đạt |

Cảnh báo (warning) không làm hỏng lần chạy.

## Báo cáo

Mỗi lần chạy ghi `storage/harness_reports/<thời điểm>_<tên>/report.json` và `report.md`. Nếu thư mục đang kiểm chứng chứa `storage/harness_reports/` (ví dụ kiểm chứng cả kho), báo cáo được ghi vào `harness_reports/` trong thư mục tạm của hệ thống. Dòng cuối của lệnh in đường dẫn thư mục báo cáo. Thư mục `storage/harness_reports/` và `storage/harness_cache/` không được commit.

Ảnh do `slide_pptx --render` xuất ra nằm ở `storage/harness_cache/render/deck_*`. Sau mỗi lần render thành công, harness chỉ giữ 5 thư mục mới nhất (`RENDER_KEEP` trong `core/harness/gates/slide_pptx.py`), tính chung mọi bộ slide; các thư mục cũ hơn bị xóa.

## Công cụ tùy chọn

Chỉ cần khi dùng `--runtime` hoặc `--render`. Thiếu công cụ thì cổng báo bỏ qua và lệnh trả mã 2.

| Công cụ | Dùng cho | Cách cài |
| --- | --- | --- |
| Playwright (Python) và Chromium hoặc Chrome cài sẵn | `slide_html --runtime`, chạy `tests.html` của bài tập | `pip install playwright` rồi `python -m playwright install chromium`; hoặc cài Google Chrome |
| Node.js và npm | Vitest cho bài tập `--runtime` | Cài Node.js LTS. Lần chạy đầu cần mạng để `npm install`; kết quả lưu ở `storage/harness_cache/node_ws` |
| MySQL Server 8 (`mysqld`) | Bài tập có cơ sở dữ liệu `--runtime` | Cài MySQL Server 8. Harness dựng một phiên bản tạm trên cổng trống, không bao giờ dùng cổng 3306, không tạo người dùng, xóa sau khi chạy |
| PowerPoint (Windows) | `slide_pptx --render` | Cài Microsoft PowerPoint |

## Đặc tả môn và lập lịch

Thiết kế: `docs/superpowers/specs/2026-10-27-harness-plan-design.md`. Mỗi môn có `course_spec.yaml` ở gốc thư mục môn. Từ đặc tả, harness suy ra danh sách nhiệm vụ (một nhiệm vụ = một tài nguyên cần có), phụ thuộc, đợt, và trạng thái (từ đĩa cộng kết quả `verify`). Không có lệnh đánh dấu xong: xong nghĩa là cổng đạt.

### Định dạng

```yaml
course_id: ten_thu_muc_mon          # trùng tên thư mục môn
title: Tên môn
tech_stack: ""                      # tùy chọn
notes: course_spec.md               # tùy chọn, tệp ghi chú tương đối từ thư mục môn
defaults:
  lesson_resources: [reading, reading_questions, quiz_lesson]
sessions:
  - folder: "Session 01 - ..."
    kind: theory                    # theory | practice
    resources: [quiz_session, exercises, slide_html, slide_pptx, mindmap]
    exercises: 6                    # bắt buộc >= 1 khi có `exercises`
    lessons:
      - folder: "Lesson 01 - ..."
        title: Tên bài
        allowed: []                 # tùy chọn, phạm vi được dạy
        forbidden: []               # tùy chọn
        resources: [reading]        # tùy chọn, ghi đè defaults.lesson_resources
  - folder: "Session 02 - ..."
    kind: practice
    resources: [lab, exercises]
    exercises: 6
    depends_on_sessions: [0]        # tùy chọn; mặc định: session theory ngay trước
```

Tên thư mục so khớp không phân biệt hoa thường và dấu (`Bai doc` khớp `Bài đọc`). Lỗi đặc tả in ra kèm vị trí, ví dụ `sessions[1].lessons[0].resources`.

### Tài nguyên

| Tài nguyên | Id nhiệm vụ | Đích (tương đối thư mục môn) | Cổng | Skill | Phụ thuộc |
| --- | --- | --- | --- | --- | --- |
| `reading` | `s01/l01/reading` | `<session>/<lesson>/Bai doc/reading.html` | `reading` | `reading_generator` | không |
| `reading_questions` | `s01/l01/reading_questions` | `<session>/<lesson>/Cau hoi bai doc/reading_questions.md` | tồn tại | `reading_questions_generator` | reading của lesson |
| `quiz_lesson` | `s01/l01/quiz_lesson` | `<session>/<lesson>/Quizz lesson/` | `quiz_lesson` | `quiz_generator` | reading của lesson |
| `quiz_session` | `s01/quiz_session` | `<session>/Quizz session/` | `quiz_session` | `quizz_session` | mọi reading của session |
| `exercises` | `s01/exercise_1` … `s01/exercise_N` | `<session>/Bai tap/<i>_*/` | `exercise` | `exercise_generator` | reading của session (theory) hoặc của session phụ thuộc (practice) |
| `slide_html` | `s01/slide_html` | `<session>/Bai giang tren lop/slides.html` | `slide_html` | `slide_html` | mọi reading của session |
| `slide_pptx` | `s01/slide_pptx` | `<session>/Slide bai giang/*.pptx` | `slide_pptx` | `slide_deck` | mọi reading của session |
| `mindmap` | `s01/mindmap` | `<session>/So do tu duy/mindmap.md` | tồn tại | `session_mindmap_compiler` | mọi reading của session |
| `lab` | `s02/lab` | `<session>/Bai thuc hanh/lab_guide.md` | `lab` | `lab_generator` | mọi reading của session phụ thuộc |

`s01`, `l01` là số thứ tự theo vị trí trong đặc tả. Cổng "tồn tại": đạt khi tệp đích có và không rỗng. Đợt của nhiệm vụ = 1 + đợt lớn nhất của các phụ thuộc.

### Lệnh

```bash
python -m core.harness init <thư mục môn> [--force]
python -m core.harness plan <course_spec.yaml> [--json]
python -m core.harness status <course_spec.yaml> [--runtime] [--json]
python -m core.harness next <course_spec.yaml> [--limit N] [--json]
```

- `init`: dựng `course_spec.yaml` nháp từ thư mục môn đã có (session, lesson, tài nguyên, số bài tập theo những gì đang có trên đĩa). Chỉ ghi đúng tệp này; đã có tệp thì từ chối (mã 1) trừ khi `--force`. Bản nháp cần người đọc lại: thêm `tech_stack`, `allowed`/`forbidden`.
- `plan`: chỉ đọc đặc tả, không chạy cổng; mỗi dòng `[đợt] id  kind  đích  ← phụ thuộc`.
- `status`: chạy cổng trên mọi đích đang có, ghi `storage/harness/<course_id>/state.json`, in số nhiệm vụ theo trạng thái (`done`, `missing`, `failed`, `blocked_tool`), rồi các nhiệm vụ chưa `done` kèm lỗi đầu tiên. `--runtime` chỉ áp cho bài tập và slide HTML.
- `next`: in các nhiệm vụ sẵn sàng (chưa `done`, mọi phụ thuộc đã `done`), theo đợt rồi id. Mỗi khối có đích tuyệt đối, skill `skills/<tên>/SKILL.md`, phụ thuộc, tệp ghi chú của môn, `allowed`/`forbidden`, lỗi đầu tiên và lệnh kiểm `verify`. Đọc `state.json`; tự chạy lại `status` (chế độ tĩnh) khi chưa có, khác `course_id`, hoặc đặc tả sửa sau lần chạy trước. `blocked_tool` không tính là xong cho phụ thuộc.

Lỗi đặc tả, thư mục không tồn tại hoặc tệp đã có: in thông báo ra stderr, mã 1. Với `--json`, stdout chỉ chứa JSON.

### Mã thoát của `status`

| Mã | Ý nghĩa |
| --- | --- |
| 0 | Mọi nhiệm vụ `done` |
| 1 | Có nhiệm vụ `failed`, hoặc đặc tả lỗi |
| 3 | Còn nhiệm vụ `missing`, không có `failed` (chưa xong, không phải lỗi) |
| 2 | Chỉ còn nhiệm vụ `blocked_tool` (thiếu công cụ); không được coi là xong |

## Kết quả đã biết (2026-10-27)

Mục này là ảnh chụp tại ngày ghi ở tiêu đề, không tự cập nhật; chạy lại lệnh trên dữ liệu hiện tại trước khi dựa vào.

- Các khóa NodeJS và ReactJS đã duyệt đạt kiểm chứng tĩnh.
- Bài tập có số từ ngoài khoảng 350-700 chỉ bị cảnh báo, không làm hỏng.
- Khóa cũ dùng định dạng quiz json không đạt cổng quiz; cần đổi sang định dạng hiện hành.

## Xử lý sự cố

- Mã 2: đọc dòng "Bỏ qua" trong kết quả để biết công cụ thiếu, cài theo bảng trên rồi chạy lại.
- "Không nhận diện được loại tài nguyên": thêm `--kind`, hoặc kiểm tra tên thư mục cha.
- `npm install` treo hoặc lỗi: kiểm tra mạng, xóa `storage/harness_cache/node_ws` rồi chạy lại.
- Khóa `.lock` còn sót trong `storage/harness_cache/` sau khi bị ngắt: tệp khóa ghi `<PID> <thời điểm>` của tiến trình giữ khóa. Nếu tiến trình đó không còn chạy, lần chạy sau chiếm khóa ngay; nếu không đọc được PID, khóa cũ hơn 30 phút mới bị bỏ qua. Có thể xóa tay khi chắc chắn không còn lần chạy nào.
