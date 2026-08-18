### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 6] Sửa lỗi tính tổng chi phí đăng ký khám bệnh — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra đúng dòng thực hiện phép cộng hai biến kiểu String trả về từ `prompt()` mà chưa qua ép kiểu `Number()`.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thành đầy đủ 2 trường hợp kiểm thử còn thiếu (STT 2 và STT 3) trong bảng HTML với đầy đủ các cột Input, Buggy Output, Expected Output, Dòng code lỗi và Giải thích nguyên nhân.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sửa tệp mã nguồn để thực hiện chính xác phép cộng số học giữa phí khám và phí dịch vụ bổ sung, cho ra tổng tiền thanh toán chuẩn xác.
*   **[20 điểm] Ép kiểu dữ liệu minh bạch:** Sử dụng hàm `Number()` đúng vị trí khi đọc giá trị từ `prompt()` để chuyển đổi từ dạng chuỗi sang dạng số.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Tối ưu hóa luồng nhập dữ liệu:** Đảm bảo mã nguồn ngắn gọn, dễ đọc, ép kiểu trực tiếp hoặc gián tiếp một cách nhất quán.
*   **[10 điểm] Sử dụng chuỗi Template Literals chuẩn xác:** Sử dụng cú pháp dấu backtick (`` ` ``) và biểu thức `${}` để đóng gói chuỗi thông báo kết quả hóa đơn chuyên nghiệp.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Giải thích nguyên nhân lỗi toán tử `+`:** Trả lời rõ ràng cơ chế ép kiểu tự động (implicit type coercion) của JavaScript khi gặp toán tử `+` với dữ liệu kiểu String.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến theo chuẩn `camelCase`, mã nguồn trình bày ngắn gọn, thụt lùi dòng nhất quán, comment giải thích rõ ràng.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub repository đúng cấu trúc thư mục quy định (`[Tên Lớp]_[Môn Học]_Session02_Ex6`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Kiểm tra trường hợp nhập NaN:** Bổ sung logic kiểm tra giá trị người dùng nhập vào nếu không phải là số hợp lệ thì cảnh báo hoặc gán giá trị mặc định là 0.