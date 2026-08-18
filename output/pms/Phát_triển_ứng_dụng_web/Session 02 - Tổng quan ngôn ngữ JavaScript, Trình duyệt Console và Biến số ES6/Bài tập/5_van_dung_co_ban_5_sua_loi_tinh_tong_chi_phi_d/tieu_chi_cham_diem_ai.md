### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 5] Sửa lỗi tính tổng chi phí dịch vụ đặt lịch khám bệnh — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ rõ vị trí dòng code thực hiện phép tính `totalPayment` thiếu ép kiểu số từ `prompt()`.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Điền đầy đủ và chính xác các giá trị bị lỗi (Buggy Output), giá trị mong đợi (Expected Output) và giải thích nguyên nhân cho 2 trường hợp Test Case còn lại trong bảng.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Chuyển đổi chính xác dữ liệu đầu vào bằng `Number()` giúp tính tổng chi phí khám bệnh chính xác trong mọi tình huống.
*   **[20 điểm] Xử lý ngoại lệ chuẩn ngôn ngữ:** Tách biệt rõ ràng biến nhận dữ liệu chuỗi từ `prompt()` và biến lưu giá trị số sau khi ép kiểu (hoặc ép kiểu ngay tại câu lệnh nhập).

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Đảm bảo dữ liệu nhập từ `prompt()` được xử lý an toàn, tránh lỗi tính toán ra `NaN` khi dữ liệu rỗng.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Định dạng thông điệp xuất ra bằng Template Literals đúng cú pháp ES6, không gây lỗi cú pháp hiển thị.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích rõ cơ chế ép kiểu ngầm định (Implicit Type Coercion) trong JavaScript khi kết hợp toán tử số học `+` giữa các kiểu dữ liệu `Number` và `String`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Mã nguồn viết sạch đẹp, đặt tên biến theo chuẩn `camelCase`, tuyệt đối không dùng từ khóa cũ `var`.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên repository GitHub theo đúng cấu trúc thư mục được yêu cầu: `[Tên Lớp]_[Môn Học]_Session02_Ex5`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Bổ sung kiểm tra hợp lệ:** Viết thêm câu lệnh kiểm tra giá trị nhập vào nếu không phải là số hợp lệ (`isNaN`) thì cảnh báo người dùng nhập lại.