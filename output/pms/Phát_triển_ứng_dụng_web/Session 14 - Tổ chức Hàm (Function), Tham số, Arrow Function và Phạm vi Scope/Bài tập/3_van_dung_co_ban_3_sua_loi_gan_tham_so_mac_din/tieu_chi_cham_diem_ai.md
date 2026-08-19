### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 3] Sửa lỗi gán tham số mặc định và scope tính tiền vé sự kiện — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ rõ các dòng code xử lý gán mặc định sai bằng toán tử `||` (`discountRate || 0.15` và `bookingFee || 20000`).
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thiện đầy đủ thông tin dòng 2 và dòng 3 trong bảng Test Case, tính toán chính xác Output lỗi và Output kỳ vọng khi `discountRate = 0` và khi khuyết tham số.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Sử dụng đúng ES6 Default Parameters:** Chuyển đổi hàm sang Arrow Function và khai báo tham số mặc định trực tiếp trên chữ ký hàm `(ticketPrice, discountRate = 0.15, bookingFee = 20000) => { ... }`.
*   **[20 điểm] Đóng gói an toàn bằng Closure:** Đưa biến tích lũy tổng doanh thu vào trong scope của Closure, không còn biến toàn cục (global variable) bị xâm nhập trực tiếp.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng giá vé:** Kiểm tra giá vé `ticketPrice` phải là kiểu số (`typeof ticketPrice === 'number'`) và có giá trị lớn hơn 0.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Ném ngoại lệ `Error` với thông điệp tiếng Việt có dấu rõ ràng khi tham số truyền vào không hợp lệ.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích được sự khác nhau giữa việc kiểm tra giá trị mặc định bằng toán tử `||` (Falsy values: `0`, `""`, `false`, `null`, `undefined`) và cú pháp ES6 Default Parameters (chỉ kích hoạt khi tham số là `undefined`).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến/hàm theo tiếng Anh chuẩn `camelCase`, comment giải thích bằng tiếng Việt có dấu, trình bày thụt lề chuẩn ES6+.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định `[Tên Lớp]_[Môn Học]_Session14_Ex3`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Viết các câu lệnh kiểm thử tự động (assert/console.assert) kiểm tra các kịch bản mua vé Regular (`discountRate = 0`), Early Bird (khuyết tham số) và VIP (`discountRate = 0.1`).