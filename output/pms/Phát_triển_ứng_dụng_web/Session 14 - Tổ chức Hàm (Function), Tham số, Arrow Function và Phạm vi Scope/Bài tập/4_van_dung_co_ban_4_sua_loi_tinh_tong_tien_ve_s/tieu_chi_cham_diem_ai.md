### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 4] Sửa lỗi tính tổng tiền vé sự kiện khi áp dụng mức chiết khấu 0% — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ rõ dòng lệnh `const finalDiscountRate = discountRate || 0.15;` trong mã nguồn cũ là nguyên nhân gây ra sự cố.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Điền đầy đủ và chính xác dữ liệu 2 testcase còn thiếu (STT 2 và STT 3) với các thông số đầu ra hiện tại (bị lỗi), đầu ra mong đợi và lời giải thích ngắn gọn.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Chuyển đổi thành công sang khai báo Tham số mặc định ES6 trên signature của Arrow Function: `(ticketPrice, ticketQuantity = 1, discountRate = 0.15, serviceFee = 30000) => { ... }`.
*   **[20 điểm] Xử lý chính xác giá trị 0%:** Kết quả tính toán cho trường hợp `discountRate = 0` trả về chính xác tổng tiền nguyên giá (không bị trừ 15%).

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Kiểm tra các trường hợp giá vé hoặc số lượng vé không hợp lệ (ví dụ: `ticketPrice <= 0` hoặc `ticketQuantity <= 0`).
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Hàm xử lý mượt mà khi người dùng truyền thiếu tham số `ticketPrice` mà không làm sập ứng dụng.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Trả lời rõ ràng sự khác nhau giữa Tham số mặc định ES6 và toán tử `||` đối với các giá trị falsy (`0`, `""`, `false`, `null`, `undefined`).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Mã nguồn viết bằng Arrow Function gọn gàng, biến đặt tên theo chuẩn camelCase tiếng Anh, chú thích Tiếng Việt rõ ràng.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định (`[Tên Lớp]_[Môn Học]_Session14_Ex4`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Viết thêm file test nhỏ hoặc tập hợp các câu lệnh `console.assert()` để tự động kiểm định hàm `calculateTicketOrderTotal` qua các kịch bản đợt bán Early Bird và Standard.