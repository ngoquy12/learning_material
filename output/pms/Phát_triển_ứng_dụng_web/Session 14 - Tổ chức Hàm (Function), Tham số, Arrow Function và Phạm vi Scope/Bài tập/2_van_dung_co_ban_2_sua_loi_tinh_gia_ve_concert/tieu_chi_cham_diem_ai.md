### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 2] Sửa Lỗi Tính Giá Vé Concert Khi Khuyết Hoặc Tùy Chỉnh Chiết Khấu Mặc Định — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra chính xác các dòng lệnh gán `finalDiscount` và `finalServiceFee` đang lạm dụng toán tử `||` để gán giá trị mặc định trong mã nguồn.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thiện 100% dữ liệu cho các ô `...` ở STT 2 và STT 3 với Buggy Output, Expected Output, dòng code gây lỗi và giải thích rõ bản chất toán tử `||` coi số `0` là giá trị Falsy nên bị nhảy sang nhánh mặc định.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Chuyển đổi thành công sang cú pháp Tham số mặc định ES6 chuẩn (`(basePrice, discountRate = 0.15, serviceFee = 30000) => ...`), đảm bảo tính chính xác kết quả cho cả 3 kịch bản testcase (đặc biệt khi truyền `0`).
*   **[20 điểm] Xử lý ngoại lệ chuẩn ngôn ngữ:** Sử dụng câu lệnh rẽ nhánh kiểm tra dữ liệu đầu vào (`basePrice > 0`, `discountRate` từ 0 đến 1, `serviceFee >= 0`) và ném ra thông báo lỗi thích hợp bằng `throw new Error(...)`.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Chặn các trường hợp truyền `basePrice` là số âm, không phải là kiểu số (`NaN`, `string`), hoặc các tham số không hợp lệ.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Hàm xử lý an toàn, không làm ứng dụng bị treo khi gặp tham số sai định dạng.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích rõ lý do vì sao trong JavaScript ES6+, việc sử dụng Tham số mặc định (Default Parameters) an toàn hơn nhiều so với toán tử logic `||` khi xử lý các tham số có thể nhận giá trị bằng `0` hoặc `false`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến/hàm theo chuẩn camelCase trong tiếng Anh, khai báo biến với `const`/`let`, mã nguồn có chú thích logic đầy đủ bằng tiếng Việt có dấu.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục yêu cầu `[Tên Lớp]_[Môn Học]_Session14_Ex2`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Viết bộ các câu lệnh kiểm thử tự động (sử dụng `console.assert`) để xác minh tự động tính đúng đắn của hàm `calculateTicketPayment` trên nhiều biên dữ liệu khác nhau.