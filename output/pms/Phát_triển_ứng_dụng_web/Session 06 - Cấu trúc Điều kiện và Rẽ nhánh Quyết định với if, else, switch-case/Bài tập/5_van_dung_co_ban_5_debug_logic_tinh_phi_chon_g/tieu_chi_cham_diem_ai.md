# **Tiêu chí chấm điểm (AI)**
**[Sửa lỗi code] Debug Logic Tính Phí Chọn Ghế Và Hành Lý Máy Bay — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra chính xác dòng thiếu lệnh `break` trong `switch-case` và dòng điều kiện tính sai phí hành lý quá cước.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thành đầy đủ các dòng còn thiếu trong bảng Test Case với đầy đủ thông số đầu vào, đầu ra thực tế bị lỗi, đầu ra kỳ vọng và giải thích nguyên nhân.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sử dụng đúng cấu trúc `switch-case` có đầy đủ `break` cho từng trường hợp hạng vé (Eco, Deluxe, Business) và tính đúng `seatFee`.
*   **[20 điểm] Xử lý chính xác điều kiện hành lý quá cước:** Áp dụng câu lệnh điều kiện `if (baggageWeight > 7)` hoặc toán tử ba ngôi để tính đúng phí `(baggageWeight - 7) * 50000` và gán 0 cho trường hợp `<= 7 kg`.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Xử lý trường hợp `ticketClass` không thuộc tập `[1, 2, 3]` bằng khối `default` trong `switch-case` hoặc kiểm tra điều kiện bảo vệ (guard clause).
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Kiểm tra trọng lượng hành lý âm (`baggageWeight < 0`) và không làm sập chương trình.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích ngắn gọn khái niệm "Fall-through" trong `switch-case`, khi nào nên chủ động dùng và khi nào là lỗi lập trình.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến rõ ràng bằng tiếng Anh (`seatFee`, `excessBaggageFee`, `ticketClass`), căn lề chuẩn 2 spaces, comment bằng tiếng Việt có dấu.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục yêu cầu `[Tên Lớp]_[Môn Học]_SessionSession 06_Ex5`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Kịch bản Kiểm thử Tự động:** Viết hàm tự động chạy qua mảng dữ liệu test case và so sánh kết quả trả về với kết quả kỳ vọng (sử dụng câu lệnh `console.assert` hoặc `console.table`).
