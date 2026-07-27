### **Tiêu chí chấm điểm (AI)**
**[Bài tập sửa lỗi tính toán dung tích ô kệ kho hàng Warehouse] — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:**
    *   Chỉ ra được phép cộng `current_volume + new_item_volume` đang là phép nối chuỗi (String Concatenation) chứ không phải phép cộng số học.
    *   Chỉ ra được phép trừ `max_volume - total_volume_expected` gây ra lỗi `TypeError` vì không thể trừ chuỗi cho chuỗi trong Python.
    *   Phân tích được nguy cơ so sánh chuỗi ở biến `is_overloaded` (ví dụ: chuỗi `"12.0"` so sánh với `"9.0"` có thể trả về `False` do so sánh theo thứ tự bảng chữ cái Alpahbet chứ không phải giá trị số học).
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Em cần hoàn thành đầy đủ thông tin của 3 Test case trong đề bài với dữ liệu thực tế bị crash được ghi nhận chính xác và kết quả tính toán mong muốn chuẩn xác.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sửa đổi thành công việc ép kiểu từ chuỗi sang `float` cho cả 3 biến đầu vào: `max_volume`, `current_volume`, và `new_item_volume`.
*   **[20 điểm] Trả về chính xác HTTP Status Code giả lập:** Thực hiện thành công việc gán và tính toán biến `status_code` (200 khi an toàn, 409 khi quá tải) bằng thuật toán logic mà không sử dụng câu lệnh `if-else`.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Định dạng số thực đầu ra:** Sử dụng f-string định dạng hiển thị số thực lấy 2 chữ số thập phân (`:.2f`) cho các kết quả thể tích giúp báo cáo hiển thị tối ưu trực quan.
*   **[10 điểm] Tối ưu hóa biến lưu trữ:** Đảm bảo kiểu dữ liệu đầu ra của các biến trung gian như `is_overloaded` là Boolean gốc (`True`/`False`), chứ không phải lưu trữ dưới dạng chuỗi chữ `"True"`/`"False"`.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Sinh viên viết câu trả lời ngắn giải thích lý do tại sao hàm `input()` trong Python luôn trả về một chuỗi ký tự (`str`), và điều gì sẽ xảy ra nếu người dùng cố tình nhập một ký tự chữ (ví dụ: "mười") vào hệ thống (lỗi `ValueError` khi ép kiểu và hướng phòng tránh cơ bản).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến rõ ràng, tuân thủ nguyên tắc viết code sạch, thụt lề chuẩn, không dư thừa mã rác.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy toàn bộ mã nguồn và báo cáo lên GitHub Repo đúng cấu trúc thư mục quy định (`[Tên Lớp]_[Môn Học]_Session01_Ex01`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết cơ chế tự động Validation định dạng số:** Sử dụng phương thức xử lý chuỗi (như `.replace('.', '', 1).isdigit()`) để kiểm tra dữ liệu nhập vào có phải số hay không trước khi ép kiểu, từ đó in ra mã HTTP 400 (Bad Request) nếu dữ liệu nhập vào là chữ mà không làm sập (crash) chương trình giữa chừng (vẫn tuân thủ không dùng `if-else` bằng các biểu thức logic thông minh).