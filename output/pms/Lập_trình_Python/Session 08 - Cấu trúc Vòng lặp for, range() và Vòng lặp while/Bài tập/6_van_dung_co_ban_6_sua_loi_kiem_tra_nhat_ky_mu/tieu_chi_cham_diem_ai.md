# **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 6] Sửa lỗi kiểm tra nhật ký mượn sách bằng vòng lặp và điều khiển luồng — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra chính xác 2 vị trí dòng code bị đặt sai thứ tự (dòng cộng `valid_count` và dòng in thông báo thành công trước khi kiểm tra `break`).
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Điền đầy đủ và chính xác dữ liệu kiểm thử vào các hàng còn thiếu (STT 2 và STT 3) trong bảng HTML báo cáo test case.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Điều chỉnh vị trí câu lệnh `continue`, `break` và in thông báo sao cho lượt mượn 104 không tăng biến đếm và lượt mượn 108 không xuất dòng thông báo xử lý thành công.
*   **[20 điểm] Sử dụng chuẩn khối for...else:** Bảo toàn và vận dụng đúng tính năng khối `else` kết hợp với vòng lặp `for`, hiển thị thông báo kết thúc lô chỉ khi không bị ngắt bởi `break`.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Khai báo khoảng lặp chính xác:** Sử dụng đúng tham số `range(start_id, end_id + 1)` để đảm bảo duyệt đủ từ mã 101 đến 110.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Đảm bảo biến đếm `valid_count` phản ánh đúng số lượng thực tế đạt chuẩn (Ví dụ: khi gặp 108 dừng lại thì `valid_count` chỉ tính các mã hợp lệ 101, 102, 103, 105, 106, 107).

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích ngắn gọn tại sao việc đặt câu lệnh tăng biến đếm trước `continue` lại gây sai lệch dữ liệu và tác dụng của khối `else` trong vòng lặp `for` so với việc dùng một biến cờ (flag).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Mã nguồn viết rõ ràng, tuân thủ quy tắc PEP 8 (thụt lùi 4 khoảng trắng, tên biến rõ nghĩa bằng tiếng Anh, chú thích bằng tiếng Việt có dấu).
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên repository GitHub đúng cấu trúc thư mục yêu cầu (`[Tên Lớp]_[Môn Học]_Session08_Ex6`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Linh hoạt cấu hình đầu vào:** Cho phép người dùng nhập vào mã cần bỏ qua và mã rủi ro từ phím thay vì cố định số 104 và 108, đồng thời vẫn giữ đúng nguyên lý `break`/`continue`/`else`.
