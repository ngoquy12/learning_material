### **Tiêu chí chấm điểm (AI)**
**[Sáng tạo] Thiết kế hệ thống đối soát giao dịch thanh toán và cảnh báo rủi ro Fintech — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Định nghĩa đầy đủ, minh bạch cấu trúc Request (danh sách giao dịch đợt) và Response (báo cáo chốt sổ đối soát) bằng kiểu dữ liệu Python chuẩn (list, dict).
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Phân tích và mô tả chi tiết tối thiểu 3 kịch bản lỗi nghiệp vụ (ví dụ: giao dịch âm tiền, mã trạng thái không xác định, đợt giao dịch rỗng, vượt hạn mức cho phép).

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid thể hiện chính xác tiến trình xử lý từ dữ liệu đầu vào, qua nhánh bỏ qua `continue`, đến khối chốt đợt `for...else`.
*   **[10 điểm] Thiết kế vòng đời tính năng:** Giải thích rõ ràng cơ chế tính toán tổng tiền, đếm số lượng giao dịch thành công và cơ chế phân loại trạng thái rủi ro.

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Viết mã nguồn xử lý đợt giao dịch sử dụng vòng lặp `for` và khối `else` đi kèm. Tuân thủ tuyệt đối quy định không dùng `while` và `break`.
*   **[15 điểm] Xử lý lọc dữ liệu nâng cao:** Sử dụng hiệu quả câu lệnh `continue` để lọc và bỏ qua chính xác các giao dịch không hợp lệ hoặc có dấu hiệu rủi ro theo đúng quy tắc thiết kế.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Cài đặt các câu lệnh kiểm tra (if/elif) để phát hiện và xử lý gọn gàng các trường hợp dữ liệu biên đã đề xuất, in cảnh báo mô tả rõ lý do bỏ qua.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Hướng đối tượng:** Đạt chuẩn PEP 8 (thụt lề 4 khoảng trắng, snake_case), có Type Hints đầy đủ, tên biến/hàm hoàn toàn bằng tiếng Anh.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Khởi tạo cấu trúc thư mục đúng tên `[Tên Lớp]_[Môn Học]_Session06_Ex05`, có tệp README.md hướng dẫn chi tiết cách chạy chương trình.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Tích hợp bộ ghi nhật ký đối soát (Audit Trail Log) tự động lưu trữ thông tin chi tiết của các giao dịch bị bỏ qua để phục vụ công tác truy vết sau này.