### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 5] Sửa lỗi tính tổng tiền vé sự kiện khi áp dụng chiết khấu mặc định và phí tiện ích — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra đúng dòng mã sử dụng toán tử gán mặc định `||` (`const finalDiscountRate = discountRate || 0.15;` và `const finalServiceFee = serviceFee || 30000;`).
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thành đầy đủ 3 dòng trong bảng báo cáo test case với các giá trị Input, Output thực tế, Output mong đợi và lời giải thích bản chất toán tử `||` coi `0` là giá trị falsy.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Tái cấu trúc hàm thành công sử dụng ES6 Default Parameters: `(ticketPrice, quantity, discountRate = 0.15, serviceFee = 30000) => { ... }`.
*   **[20 điểm] Tính toán chính xác các kịch bản biên:** Đơn hàng có `discountRate = 0` trả về đúng giá không giảm; đơn hàng có `serviceFee = 0` trả về đúng tổng tiền không bị cộng 30,000 VNĐ; đơn hàng mua quá 4 vé trả về `-1`.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Kiểm tra chính xác điều kiện hạn ngạch mua vé `quantity <= 0 || quantity > 4` và trả về mã lỗi thích hợp.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Xử lý an toàn các trường hợp không truyền tham số `discountRate` hoặc `serviceFee` (hệ thống tự lấy giá trị mặc định `0.15` và `30000`).

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích ngắn gọn sự khác biệt giữa ES6 Default Parameters và toán tử `||` (hoặc toán tử `??` Nullish Coalescing) khi làm việc với các giá trị như `0`, `""`, `false`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến chuẩn tiếng Anh camelCase (`ticketPrice`, `discountRate`, `serviceFee`), mã nguồn trình bày rõ ràng, thụt lùi dòng chuẩn mực.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định `[Tên Lớp]_[Môn Học]_SessionSession 14_Ex5`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Viết tập lệnh tự động in bảng so sánh kết quả mong đợi và kết quả thực tế cho 5 trường hợp kiểm thử khác nhau.