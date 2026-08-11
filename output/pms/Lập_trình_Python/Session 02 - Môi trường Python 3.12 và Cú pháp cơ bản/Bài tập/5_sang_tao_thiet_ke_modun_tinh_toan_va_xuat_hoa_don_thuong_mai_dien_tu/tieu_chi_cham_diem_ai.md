### **Tiêu chí chấm điểm (AI)**
**[Sáng tạo] Thiết kế mô-đun tính toán và xuất hóa đơn thương mại điện tử — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Chủ động định nghĩa đầy đủ danh sách dữ liệu vào/ra cho bài toán thương mại điện tử (đơn giá, số lượng, voucher, phí ship) kèm kiểu dữ liệu tương ứng.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Phát hiện tối thiểu 3 kịch bản bẫy dữ liệu biên khi thao tác với console và ép kiểu (ví dụ: lỗi ép kiểu chuỗi chữ sang `float`/`int`, dữ liệu đầu vào mang giá trị âm, sai lệch logic dính chuỗi khi quên ép kiểu).

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid chính xác, mô tả rõ nét quy trình biến đổi dữ liệu từ dạng chuỗi (`str`) sang dạng số (`int`/`float`), qua các bước tính toán số học và xuất ra console.
*   **[10 điểm] Thiết kế vòng đời tính năng:** Trình bày rõ ràng các bước thực thi của mô-đun tính toán từ tiếp nhận dữ liệu đến hiển thị kết quả.

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Lập trình tính toán chính xác tổng tiền hàng, số tiền chiết khấu voucher và tổng chi phí thanh toán cuối cùng của đơn hàng E-commerce.
*   **[15 điểm] Xử lý định dạng đầu ra dữ liệu nâng cao:** Ứng dụng sáng tạo các tham số `sep` và `end` trong hàm `print()` để tạo giao diện hóa đơn console có đường phân cách, tiêu đề cột và định dạng tiền tệ rõ ràng.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Viết các thông báo hướng dẫn nhập liệu rõ ràng trên console để định hướng người dùng nhập đúng định dạng, hạn chế lỗi phát sinh khi ép kiểu.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Chuẩn Python 3.12:** Mã nguồn viết từ đầu không chứa mã rác, tên biến chuẩn tiếng Anh (`snake_case`), chú thích giải thích logic bằng tiếng Việt rõ ràng, đúng chuẩn PEP 8.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Cấu trúc thư mục đúng quy định `[Tên Lớp]_[Môn Học]_Session02_Ex05`, có tệp README mô tả kịch bản test và hướng dẫn chạy chương trình.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế xem trước và lưu vết tính toán:** Thiết kế thêm phần hiển thị tóm tắt nhật ký tính toán chi tiết (Audit Trail) bao gồm mã dấu thời gian mô phỏng hoặc hiển thị bảng phân tích dòng tiền minh bạch trên console.