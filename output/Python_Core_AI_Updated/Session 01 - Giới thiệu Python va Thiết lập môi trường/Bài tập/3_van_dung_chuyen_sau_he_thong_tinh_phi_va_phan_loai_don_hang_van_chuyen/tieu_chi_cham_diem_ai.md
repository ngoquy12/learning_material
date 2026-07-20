### **Tiêu chí chấm điểm (AI)**
**[Hệ thống tính phí và phân loại đơn hàng vận chuyển] — Tổng điểm: 100 điểm**

#### **1. Báo cáo phân tích và Thiết kế giải pháp — 20 điểm**
*   **[10 điểm] Xác định cấu trúc I/O:** Khai báo đầy đủ tên biến, ý nghĩa, và kiểu dữ liệu gốc (trước khi ép kiểu) và sau khi ép kiểu cho mọi tham số đầu vào và đầu ra của chương trình.
*   **[10 điểm] Mô tả giải thuật xử lý nghiệp vụ:** Viết mã giả (Pseudocode) hoặc lưu đồ thuật toán (Flowchart) mô tả tường minh luồng kiểm tra logic mã vận đơn, tìm giá trị lớn nhất cho `Chargeable weight` và kiểm tra điều kiện biên để xác định trạng thái quá tải cước vận chuyển.

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Schema:** Tổ chức lưu trữ dữ liệu đầu vào thông qua các tên biến tự tường minh, đúng quy tắc đặt tên của PEP 8 (snake_case), thực hiện ép kiểu dữ liệu từ `str` (từ hàm `input()`) sang đúng kiểu `float` hoặc `int` để phục vụ tính toán số học.
*   **[15 điểm] API xử lý nghiệp vụ tích hợp:** Xây dựng thành công luồng xử lý tính toán đúng công thức Trọng lượng quy đổi theo thể tích, xác định đúng Trọng lượng tính cước lớn nhất bằng hàm tích hợp (ví dụ: `max()`), và tính chính xác Phí vận chuyển gốc cũng như Phí vận chuyển sau thuế VAT (8%).

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy dữ liệu trùng lặp / Vượt ngưỡng:** Thực hiện chính xác biểu thức logic để so sánh trọng lượng thực tế với mức trần $150\text{ kg}$, trả về kết quả kiểu `bool` (`True` hoặc `False`) chuẩn xác để thiết lập cờ cảnh báo quá tải cho đội điều vận.
*   **[15 điểm] Validate dữ liệu đầu vào nâng cao:** Sử dụng các phương thức xử lý chuỗi cơ bản của Python (như `startswith()`) để kiểm tra tiền tố mã vận đơn đầu vào xem có bắt đầu bằng `"LGT-"` hay không và lưu trạng thái vào một biến boolean độc lập.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về mã lỗi định danh:** Chương trình có các thông báo hướng dẫn hoặc thông báo lỗi tường minh khi người dùng nhập dữ liệu không hợp lệ (ví dụ: nhập chuỗi vào trường yêu cầu số thực dẫn đến lỗi ép kiểu dữ liệu).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Viết mã nguồn rõ ràng, có chú thích (comment) giải thích các bước tính toán công thức nghiệp vụ, không dùng các ký tự viết tắt khó hiểu làm mờ nghĩa của biến.
*   **[5 điểm] Nộp bài GitHub:** Đẩy mã nguồn lên đúng cấu trúc thư mục quy chuẩn: `[Tên Lớp]_[Môn Học]_Session01_Ex03` trên GitHub bế bọc đúng tên file yêu cầu.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý concurrency:** Đưa ra giải pháp thiết kế hoặc ý tưởng mở rộng mã nguồn bằng cách sử dụng cấu trúc dữ liệu cấu trúc (ví dụ: các biến được đóng gói trong một `dictionary`) để sẵn sàng cho việc cập nhật đồng thời nhiều đơn hàng mà không gây xung đột ghi đè các biến toàn cục.