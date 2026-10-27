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
