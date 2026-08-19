# **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 6] Sửa lỗi tính phí hành lý ký gửi quá cước Vietjet — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ rõ vị trí thiếu lệnh `break;` trong khối `case 1` của cấu trúc `switch-case` (dòng 9-13).
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Điền đầy đủ và chính xác dữ liệu cho Row 2 và Row 3 trong bảng Test Case (Input, Buggy Output, Expected Output, Dòng lỗi, Logic Note).

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sửa lỗi thiếu từ khóa `break;` trong `switch-case`, giúp hệ thống gán chính xác `ticketClassName` và `freeAllowance` cho hạng vé Eco, Deluxe và Business.
*   **[20 điểm] Tính toán chính xác chi phí:** Số kg quá cước (`excessWeight`) và tổng phí phạt (`excessFee`) được tính đúng theo mức giá 50.000 VNĐ/kg và không bị giá trị âm khi hành lý nhỏ hơn hạn mức.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate mã hạng vé đầu vào:** Khối `default` xử lý chính xác các trường hợp mã hạng vé không hợp lệ (ví dụ: `ticketClassCode = 99` hoặc âm).
*   **[10 điểm] An toàn hệ thống:** Chương trình ngắt tính toán hoặc hiển thị cảnh báo phù hợp khi mã hạng vé không hợp lệ, không gây tính toán ra số tiền sai.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Giải thích hiện tượng Fall-through:** Giải thích rõ bản chất của hiện tượng trôi lệnh (fall-through) trong `switch-case` và lý do vì sao luôn cần từ khóa `break;` cuối mỗi nhánh case nếu không có ý định gộp nhánh.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến chuẩn tiếng Anh (`ticketClassCode`, `freeAllowance`, `excessFee`), căn lề chuẩn 2 spaces, mã nguồn rõ ràng.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub repository theo đúng cấu trúc thư mục quy định: `[Tên Lớp]_[Môn Học]_Session06_Ex6`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết hàm/kịch bản kiểm thử tự động:** Viết đoạn mã gọi thử nghiệm nhiều bộ dữ liệu đầu vào khác nhau để tự động in ra thông báo PASS/FAIL cho từng case.
