### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 1] Sửa lỗi tính toán hiển thị danh sách Lead CRM — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra chính xác dòng điều kiện `elif viewport_width > mobile_limit ...` bỏ sót trường hợp giá trị ranh giới `viewport_width == 768` và thiếu bước validate số âm/bằng 0.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Cung cấp đầy đủ tối thiểu 3 test case trong bảng HTML (gồm các giá trị biên như 768, 1024 và giá trị không hợp lệ như -100 hoặc 0) làm rõ sự sai biệt giữa Buggy Output và Expected Output.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Điều chỉnh chính xác toán tử so sánh để phân loại đúng `MOBILE` (`< 768`), `TABLET` (`>= 768` và `< 1024`), `DESKTOP` (`>= 1024`).
*   **[20 điểm] Xử lý ngoại lệ chuẩn ngôn ngữ:** Triển khai đúng cú pháp `raise ValueError(...)` khi dữ liệu `viewport_width <= 0` với thông điệp rõ ràng theo đúng yêu cầu bài toán.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Sử dụng `isinstance(viewport_width, int)` hoặc `type()` để chặn các kiểu dữ liệu không hợp lệ (`str`, `float`, `None`) và ném ra `TypeError`.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Đảm bảo hàm xử lý an toàn, không làm ứng dụng bị nghẽn (crash) ngoài ý muốn khi nhận các tham số biên hoặc sai định dạng.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích ngắn gọn tác hại của lỗi ranh giới (Boundary Bug / Off-by-one Error) trong giao diện phần mềm doanh nghiệp và nguyên tắc thiết kế điều kiện kiểm thử ranh giới.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Tuân thủ chuẩn PEP 8, thụt lề 4 dấu cách, đặt tên biến dạng `snake_case`, bổ sung Type Hints đầy đủ (`viewport_width: int -> dict[str, int | str]`).
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Nộp bài đúng cấu trúc thư mục `[Tên Lớp]_[Môn Học]_Session01_Ex01` trên GitHub repository.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Viết kèm kịch bản kiểm thử tự động sử dụng module `unittest` hoặc `pytest` của Python để tự động xác minh tất cả các trường hợp kiểm thử nêu trên.