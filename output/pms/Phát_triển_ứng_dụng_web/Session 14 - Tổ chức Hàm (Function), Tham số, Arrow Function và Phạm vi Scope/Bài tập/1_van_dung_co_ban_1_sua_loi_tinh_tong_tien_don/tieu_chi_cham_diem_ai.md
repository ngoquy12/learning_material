### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 1] Sửa lỗi tính tổng tiền đơn hàng vé concert trong hệ thống Ticketbox — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra chính xác dòng mã nguồn gán gượng ép `const finalDiscount = discountRate || 0.15;` khiến giá trị `0` bị coi là falsy.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thiện 100% dữ liệu chính xác cho dòng 2 và dòng 3 trong bảng báo cáo kiểm thử (Input, Buggy Output, Expected Output, Failing Line, Logic Note).

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Chuyển đổi thành công hàm tính tổng tiền sang cú pháp Arrow Function ES6; tính toán đúng tổng tiền cho cả 3 kịch bản (không bị trừ nhầm 15% khi discountRate = 0).
*   **[20 điểm] Sử dụng chuẩn xác ES6 Default Parameters:** Khai báo tham số mặc định trực tiếp trên chữ ký của hàm (function signature) thay vì kiểm tra bằng toán tử `||` hoặc mệnh đề `if` thủ công.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Kiểm tra và ném ngoại lệ khi `basePrice <= 0` hoặc `quantity <= 0`.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Kiểm tra điều kiện biên của `discountRate` (nằm trong khoảng từ `0` đến `1`), ném ra ngoại lệ `Error` với thông điệp rõ ràng khi dữ liệu không hợp lệ.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích ngắn gọn vì sao toán tử `||` không an toàn khi làm việc với dữ liệu số (number) trong JavaScript và sự khác biệt khi dùng `Default Parameters ES6`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến/hàm tiếng Anh theo chuẩn `camelCase`, comment tiếng Việt rõ ràng, mã nguồn trình bày đúng thụt lề chuẩn ES6.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định: `[Tên Lớp]_[Môn Học]_Session14_Ex1`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Bọc khối try...catch kiểm thử:** Viết thêm khối `try...catch` gọi hàm với dữ liệu lỗi (ví dụ: `basePrice = -100` hoặc `discountRate = 1.5`) để chứng minh ứng dụng bắt lỗi an toàn không bị crash ngột ngạt.