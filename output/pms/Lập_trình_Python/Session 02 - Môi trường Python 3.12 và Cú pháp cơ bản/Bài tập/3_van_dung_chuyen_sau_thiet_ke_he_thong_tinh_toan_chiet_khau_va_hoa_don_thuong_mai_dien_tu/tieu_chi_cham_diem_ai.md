### **Tiêu chí chấm điểm (AI)**
**[Vận dụng chuyên sâu] Thiết kế hệ thống tính toán chiết khấu và hóa đơn thương mại điện tử — Tổng điểm: 100 điểm**

#### **1. Báo cáo phân tích và Thiết kế giải pháp — 20 điểm**
*   **[10 điểm] Xác định cấu trúc I/O:** Lập bảng thiết kế cấu trúc I/O (Data Schema Table) chi tiết, đầy đủ tên biến, kiểu dữ liệu trước và sau chuyển đổi (`str` -> `float`, `str` -> `int`), các điều kiện ràng buộc tài chính.
*   **[10 điểm] Mô tả giải thuật xử lý nghiệp vụ:** Trình bày mã giả (Pseudocode) hoặc sơ đồ luồng (Flowchart) thể hiện logic tuần tự: Nhận input -> Chuyển đổi kiểu -> Validate dữ liệu âm/vượt ngưỡng -> Tính toán tổng chi phí -> Formatting xuất dữ liệu ra Console.

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Schema:** Nhận dữ liệu dòng lệnh bằng `input()`, thực hiện ép kiểu chính xác từ chuỗi sang `float` và `int` theo đúng thiết kế schema.
*   **[15 điểm] Xử lý nghiệp vụ tài chính thương mại điện tử:** Viết chính xác các biểu thức tính toán giá trị đơn hàng chưa giảm (`subtotal`), giá trị giảm giá (`discount_amount`) và tổng chi phí thanh toán (`total_payment`).

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy dữ liệu âm và không hợp lệ:** Kiểm tra chính xác các điều kiện biên: đơn giá `unit_price > 0`, số lượng `quantity > 0`, tỷ lệ chiết khấu `0.0 <= discount_rate <= 100.0`, và phí vận chuyển `shipping_fee >= 0`.
*   **[15 điểm] Validate dữ liệu đầu vào nâng cao:** Sử dụng cấu trúc điều kiện để phát hiện vi phạm và chủ động nâng ngoại lệ `raise ValueError` hoặc dừng chương trình an toàn với thông báo phù hợp.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:** Sử dụng khối `try...except ValueError` để bắt lỗi ép kiểu khi người dùng nhập chuỗi ký tự vào các trường dữ liệu số, hiển thị thông điệp hướng dẫn rõ ràng bằng Tiếng Việt.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Tên biến/hàm đặt bằng Tiếng Anh chuẩn PEP 8 (`snake_case`), có Type Hints đầy đủ, comment giải thích bằng Tiếng Việt có dấu, tận dụng hiệu quả các tham số `sep` và `end` trong hàm `print()`.
*   **[5 điểm] Nộp bài GitHub:** Tạo kho lưu trữ trên GitHub và nộp bài đúng cấu trúc thư mục quy định: `[Tên Lớp]_[Môn Học]_Session02_Ex03`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ và định dạng số:** Định dạng kết quả hiển thị số tiền có 2 chữ số thập phân chuẩn xác và bọc luồng nhập liệu trong vòng lặp thử lại (`while loop`) giúp người dùng nhập lại khi gặp lỗi thay vì dừng chương trình đột ngột.