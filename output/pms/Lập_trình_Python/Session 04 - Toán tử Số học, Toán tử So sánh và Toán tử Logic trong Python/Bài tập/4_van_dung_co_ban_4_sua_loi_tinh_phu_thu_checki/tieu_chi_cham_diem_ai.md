# **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 4] Sửa lỗi tính phụ thu check-in sớm trong tổng chi phí đặt phòng — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ rõ dòng mã nguồn tính sai phụ thu `early_checkin_surcharge` do nhân với `base_room_cost` thay vì `room_rate`.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Điền đầy đủ và chính xác số liệu cho 2 dòng còn lại (STT 2 và STT 3) trong bảng Test Case Report HTML, thể hiện rõ sự chênh lệch giữa kết quả thực tế bị lỗi và kết quả kỳ vọng đúng nghiệp vụ.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Điều chỉnh biểu thức tính `early_checkin_surcharge` về đúng công thức `room_rate * 0.30 * is_early_checkin`.
*   **[20 điểm] Tuân thủ phạm vi kiến thức cho phép:** Không sử dụng các từ khóa bị cấm (`if`, `else`, `and`, `or`, `not`, `for`, `while`, `list`, `dict`). Chỉ sử dụng các phép toán số học và nhân giá trị kiểu Boolean.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Ép kiểu và kiểm tra kiểu dữ liệu:** Đảm bảo các tham số truyền vào hàm đúng kiểu khai báo (`float`, `int`, `bool`).
*   **[10 điểm] Đảm bảo tính toán số thực chính xác:** Kết quả tính toán tổng tiền thanh toán trả về đúng kiểu `float` và không bị lỗi tràn số hoặc làm tròn sai số.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích được ảnh hưởng của việc nhân trực tiếp biến Boolean (`is_early_checkin`) vào biểu thức số học trong Python (chuyển đổi ngầm định `True` -> `1`, `False` -> `0`).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến chuẩn `snake_case`, comment Tiếng Việt rõ ràng, tuân thủ PEP 8 và khai báo Type Hints đầy đủ.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Nộp bài đúng cấu trúc thư mục yêu cầu `[Tên Lớp]_[Môn Học]_SessionSession 04_Ex4`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết đoạn mã kiểm thử tự động:** Viết thêm các câu lệnh `assert` ở phần main để kiểm tra tự động các test case kỳ vọng mà không cần dùng `if/else`.
