### **Tiêu chí chấm điểm (AI)**
**[Sáng tạo] Thiết kế Hệ thống Nhật ký Kiểm toán Check-in và Điều phối Khách hàng CRM — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Định nghĩa rõ ràng kiểu dữ liệu Input/Output của hệ thống CRM (Tuple GPS, List Session Logs, Tuple Rep Status), giải thích rõ vai trò từng trường dữ liệu trong nghiệp vụ.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Nhận diện đủ 3 kịch bản lỗi nghiệp vụ (ví dụ: lỗi ghi đè Tuple `TypeError`, cắt lát quá chỉ số, gán dữ liệu Unpacking không tương thích) và nêu hướng xử lý logic cụ thể.

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid chính xác, hiển thị đầy đủ các bước xử lý từ khởi tạo, Unpacking, Swap đến Slicing danh sách.
*   **[10 điểm] Thiết kế vòng đời tính năng:** Mô tả rõ cơ chế bảo vệ dữ liệu bất biến của Tuple và cơ chế cập nhật trạng thái List không phá vỡ cấu trúc bộ nhớ.

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Thực hiện đúng kỹ thuật Tuple Unpacking trích xuất dữ liệu, hoán đổi biến trực tiếp (Variable Swap) không dùng biến trung gian, và cập nhật giá trị List qua Index.
*   **[15 điểm] Xử lý lọc dữ liệu nâng cao bằng Slicing:** Sử dụng chính xác cú pháp Slicing `[start:end]` để trích xuất phân đoạn lịch sử tương tácCRM mà không dùng vòng lặp hay các hàm bị cấm.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Triển khai mã nguồn có cơ chế phòng ngừa lỗi (như sử dụng khối `try-except TypeError` để chứng minh tính bất biến của Tuple kiểm toán vị trí).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Chuẩn Python 3.12:** Mã nguồn tuân thủ PEP 8, đặt tên biến/hàm tiếng Anh chuẩn snake_case, có Type Hints rõ ràng và comment giải thích tiếng Việt đầy đủ.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Tạo thư mục nộp bài đúng cấu trúc `[Tên Lớp]_[Môn Học]_Session08_Ex05`, tệp tin trình bày sạch đẹp và có mô tả README chi tiết.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Đóng gói kết quả kiểm toán sau cập nhật thành một Tuple báo cáo tổng hợp bất biến mới (Immutable Audit Snapshot) để sao lưu trạng thái hệ thống.