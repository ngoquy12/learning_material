# Kế Hoạch Triển Khai: Tác Nhân Tự Động Thiết Kế Chương Trình Học Chi Tiết (Syllabus PM Generator Agent)

Tài liệu này trình bày kế hoạch chi tiết để lập trình và tích hợp tác nhân **Syllabus PM Generator Agent (SPGA)** vào hệ thống Elearning Content Factory, giải quyết triệt để 13 thử thách thực tế đã nêu trong tài liệu phân tích kỹ thuật.

---

## User Review Required

> [!IMPORTANT]
> **Định dạng Xuất Excel**: Để đảm bảo định dạng file Excel đầu ra đẹp mắt và chuẩn hóa như tệp mẫu PTIT 2026, chúng tôi sẽ sử dụng một tệp Excel mẫu trống (`templates/PM_Template.xlsx`) đã được cấu hình sẵn các style, font chữ (Montserrat/Inter), căn lề và border. Agent sẽ điền dữ liệu vào bản sao của tệp mẫu này thay vì tự khởi tạo từ đầu nhằm tránh lỗi font chữ và định dạng.

---

## Open Questions

> [!NOTE]
> 1. **Dữ liệu Mẫu của Học Kỳ**: ĐÃ THỐNG NHẤT - Sử dụng cơ chế tự động quét tất cả các sheet Kỳ học để tìm kiếm Mã môn và tự động lấy PLO/CLO.
> 2. **Chế độ Refactor (Đồng bộ lũy tiến)**: ĐÃ THỐNG NHẤT - Xuất ra tệp Excel mới có hậu tố `_Updated.xlsx` để so sánh và kiểm chứng, tránh ghi đè trực tiếp lên tệp cũ.
> 3. **Mô hình ngôn ngữ lớn (LLM Model)**: ĐÃ THỐNG NHẤT - Hệ thống sử dụng 100% mô hình Gemini (Gemini 1.5/2.0/3.0/3.5 Flash), tuyệt đối không dùng OpenAI, DeepSeek hay OpenRouter.

---

## Proposed Changes

Chúng ta sẽ chỉnh sửa các thành phần chính của hệ thống, phân chia theo các cấu phần nghiệp vụ:

### 1. Cấu Phần Cào & Phân Tích Dữ Liệu (Parser Component)

#### [MODIFY] [curriculum_parser.py](file:///d:/Rikkei%20Education/Elearning_Agent/Learning-Material/cli/curriculum_parser.py)
- Bổ sung hàm `parse_program_structure_from_ptit(excel_path: str, target_course_id: str)`:
  - Đọc 5 sheet Khung chương trình học kỳ để tìm kiếm `target_course_id` (ví dụ `IT-106`).
  - Phục hồi các ô gộp (Merged Cells) bằng thuật toán Fill-Forward để lấy chính xác PLOs và CLOs tương ứng với môn học.
  - Bóc tách danh sách CLO chi tiết và ghi nhớ ma trận đầu vào.

---

### 2. Cấu Phần Tác Nhân Thiết Kế (Syllabus AI Agent Component)

#### [NEW] [pm_generator_agent.py](file:///d:/Rikkei%20Education/Elearning_Agent/Learning-Material/agents/pm_generator_agent.py)
- Khai báo các Pydantic Schemas đầu vào/đầu ra chuẩn hóa (`StudentProfile`, `SyllabusPM`, `SessionBlock`, `LessonBlock`).
- Lập trình **Syllabus PM Generator Agent (SPGA)** thực thi luồng tư duy 3 giai đoạn:
  - **Giai đoạn 1**: Trích xuất KUs và lập đồ thị Dependency DAG từ CLOs.
  - **Giai đoạn 2**: Tính toán chỉ số Pacing Index ($PI$) để phân chia phân bổ KUs vào số lượng buổi học (thêm buổi Thực hành nếu $PI$ thấp).
  - **Giai đoạn 3**: Phân rã Micro-lessons chi tiết cho các buổi Lý thuyết (không quá 4 bài/buổi nếu trình độ beginner).
- Tích hợp lớp kiểm định **Prerequisite Guard** để tự sửa lỗi tuần tự tri thức thông qua vòng lặp phản biện ngắn (tối đa 3 lần).
- Viết các hàm xuất dữ liệu:
  - `export_pm_to_markdown(pm: SyllabusPM, filepath: str)`: Xuất file Markdown có cấu trúc đẹp mắt.
  - `export_pm_to_excel(pm: SyllabusPM, template_path: str, filepath: str)`: Ghi dữ liệu vào tệp Excel sử dụng thư viện `openpyxl`, áp dụng format khối ô gộp, tô màu dòng tiêu đề Session theo chuẩn và điền các bài học con.

---

### 3. Cấu Phần Orchestration & CLI (Runner Component)

#### [MODIFY] [args.py](file:///d:/Rikkei%20Education/Elearning_Agent/Learning-Material/cli/args.py)
- Bổ sung các tham số dòng lệnh mới:
  - `--generate-pm`: Kích hoạt chế độ tự động sinh chương trình học.
  - `--pm-config`: Đường dẫn tới file cấu hình hồ sơ thiết kế (mặc định: `config/pm_generator_config.json`).
  - `--output-pm-name`: Tên file PM đầu ra (mặc định: `PM_Generated`).

#### [NEW] [pm_generator_config.json](file:///d:/Rikkei%20Education/Elearning_Agent/Learning-Material/config/pm_generator_config.json)
- File cấu hình chứa thông số thực tế của sinh viên (Entry level, Background, Speed), mã môn mục tiêu (`IT-106`), và tổng số buổi được giao để làm đầu vào cho Agent.

#### [MODIFY] [runner.py](file:///d:/Rikkei%20Education/Elearning_Agent/Learning-Material/cli/runner.py)
- Tích hợp bước sinh PM vào đầu chu trình chạy của `main_entry()`:
  - Nếu phát hiện cờ `--generate-pm`, hệ thống sẽ gọi `pm_generator_agent.py` để sinh file PM (ở cả dạng `.md` và `.xlsx`) và lưu vào thư mục `output/<course_name>`.
  - Thay thế tham số đường dẫn tệp Excel đầu vào bằng tệp Excel vừa sinh để pipeline phía sau (HTML, Slide, Quiz, Mindmap) tự động biên dịch trực tiếp trên tài nguyên mới mà không cần khởi động lại.

---

## Verification Plan

Chúng ta sẽ chạy các kịch bản kiểm thử sau để kiểm chứng tính đúng đắn của Agent:

### Automated Tests
- Viết unit test trong `tests/test_pm_generator.py`:
  - Kiểm tra hàm tính toán `Pacing Index` xem có chia đúng số buổi lý thuyết/thực hành khi thay đổi profile học viên từ `it-student` sang `non-it beginner`.
  - Kiểm tra tính hợp lệ của file JSON xuất ra chống lỗi parse ngoặc kép hoặc thoát dòng.

### Manual Verification
1. **Kiểm tra xuất tệp tin**:
   - Chạy lệnh CLI sinh chương trình học:
     ```powershell
     python main.py --generate-pm --pm-config config/pm_generator_config.json --tech-stack python/core
     ```
   - Xác thực sự xuất hiện của hai tệp tin trong thư mục đầu ra:
     - `output/Phát_triển_ứng_dụng_web/PM_Generated.md`
     - `output/Phát_triển_ứng_dụng_web/PM_Generated.xlsx`
2. **Kiểm tra định dạng**:
   - Mở tệp Excel được sinh ra bằng Microsoft Excel/Google Sheets để kiểm tra xem định dạng ô gộp, font chữ và căn lề có khớp chính xác 100% với tệp mẫu PTIT 2026 hay không.
3. **Kiểm tra tính nhất quán tuần tự**:
   - Quét file Markdown đầu ra để xác thực không có khái niệm nâng cao nào (như bất đồng bộ Promise/Fetch) xuất hiện trước các bài lý thuyết căn bản (biến, câu điều kiện).
