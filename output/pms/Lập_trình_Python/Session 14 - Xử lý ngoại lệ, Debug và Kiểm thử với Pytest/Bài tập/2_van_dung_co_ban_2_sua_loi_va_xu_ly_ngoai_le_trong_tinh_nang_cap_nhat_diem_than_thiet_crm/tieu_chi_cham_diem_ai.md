### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 2] Sửa lỗi và xử lý ngoại lệ trong tính năng cập nhật điểm thân thiết CRM — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra đúng dòng mã nguồn legacy gặp 3 lỗi nghiệp vụ (thiếu kiểm tra sự tồn tại key, thiếu validate điểm số, thiếu kiểm tra trạng thái tài khoản).
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Trình bày bảng báo cáo HTML tối thiểu 3 test cases phân biệt rõ Input, Buggy Output hiện tại và Expected Output đúng nghiệp vụ.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sửa triệt để lỗi logic trong hàm `update_loyalty_points`, bảo đảm điểm chỉ được cộng cho tài khoản active và số điểm cộng lớn hơn 0.
*   **[20 điểm] Xử lý ngoại lệ chuẩn ngôn ngữ:** Chủ động `raise` đúng loại ngoại lệ chuẩn của Python 3.12 (`KeyError`, `ValueError`, `TypeError`) kèm thông điệp giải thích rõ ràng.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Chặn các kiểu dữ liệu không hợp lệ của `points_to_add` (ví dụ chuỗi chữ, số thực float hoặc giá trị None).
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Sử dụng đầy đủ cấu trúc `try-except-else-finally` ở luồng gọi hàm, bắt riêng biệt từng ngoại lệ mà không làm dừng đột ngột chương trình.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích được tầm quan trọng của việc chủ động raise ngoại lệ trong hệ thống CRM thực tế thay vì lặng lẽ trả về `False` hoặc `None`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Mã nguồn viết sạch sẻ, đặt tên chuẩn `snake_case`, có Type Hints đầy đủ (`dict[str, str | int]`), comment giải thích bằng tiếng Việt có dấu.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định `[Tên Lớp]_[Môn Học]_Session14_Ex02`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Viết script kiểm thử tự động sử dụng framework `pytest 8.3` với `pytest.raises()` để kiểm tra các trường hợp ném ngoại lệ của hàm `update_loyalty_points`.