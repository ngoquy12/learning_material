# **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 1] Sửa lỗi đóng gói dữ liệu đặt phòng khách sạn và tính phụ thu check-in sớm — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ rõ dòng code sử dụng sai cú pháp Bracket Notation thiếu dấu nháy chuỗi (`booking[roomPrice]`) và dòng code gán `undefined` thay vì sử dụng toán tử `delete`.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Điền đầy đủ và chính xác các ô còn thiếu (`...`) trong bảng Test Case (hàng 2 và hàng 3), thể hiện rõ sự khác biệt giữa Buggy Output và Expected Output.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sửa thành công cú pháp truy cập `booking.roomPrice` (hoặc `booking["roomPrice"]`) để tính phụ thu check-in sớm 30% chính xác khi `checkInHour < 12`.
*   **[20 điểm] Xử lý xóa thuộc tính đúng chuẩn ES6:** Sử dụng câu lệnh `delete booking.tempToken;` (hoặc `delete booking["tempToken"];`) loại bỏ hoàn toàn key ra khỏi đối tượng trước khi thực hiện `JSON.stringify`.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Kiểm tra đối tượng `rawBooking` hợp lệ và thuộc tính `roomPrice` phải là số lớn hơn 0.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Đảm bảo hàm xử lý an toàn, không làm biến đổi (mutate) đối tượng gốc `rawBooking` truyền vào.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích ngắn gọn tại sao việc gán `booking.tempToken = undefined` vẫn làm thuộc tính tồn tại khi duyệt key đối tượng (`"tempToken" in booking` là `true`) và lý do toán tử `delete` giải quyết triệt để vấn đề này.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến rõ ràng, thụt lùi dòng chuẩn, không có lỗi cú pháp console.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định `[Tên Lớp]_[Môn Học]_Session12_Ex1`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết đoạn mã kiểm thử tự động:** Viết thêm hàm kiểm thử tự động chạy qua nhiều trường hợp (check-in trước 12h, đúng 12h, sau 12h) và in thông báo kiểm chứng "PASS/FAIL" trên Console log.
