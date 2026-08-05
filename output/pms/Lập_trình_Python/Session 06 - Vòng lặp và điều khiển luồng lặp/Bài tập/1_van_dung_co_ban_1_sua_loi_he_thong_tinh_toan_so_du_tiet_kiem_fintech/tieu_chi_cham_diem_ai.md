### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 1] Sửa lỗi hệ thống tính toán số dư tiết kiệm FinTech — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra đúng vị trí lỗi off-by-one trong hàm `range(1, total_months)`, vị trí đặt sai lệnh `continue` trước khi tính lãi, và việc thiếu đoạn code validate ngoại lệ.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Cung cấp đầy đủ bảng gồm 3 Test Cases trình bày đúng mẫu (Mã TC, Input, Actual Buggy Output, Expected Correct Output).

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sửa thành công phạm vi lặp `range(1, total_months + 1)` để duyệt đủ các tháng. Xử lý chính xác việc cộng tiền lãi trước khi dùng `continue` để bỏ qua phí dịch vụ tháng 3.
*   **[20 điểm] Xử lý ngoại lệ chuẩn ngôn ngữ:** Sử dụng câu lệnh `raise ValueError` với thông điệp rõ ràng khi dữ liệu đầu vào vi phạm điều kiện (`initial_balance <= 0`, `monthly_rate <= 0`, hoặc `total_months < 1`).

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Ngăn chặn các tham số đầu vào có giá trị không hợp lệ (số âm hoặc bằng 0).
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Đảm bảo hàm ném ngoại lệ đúng loại `ValueError` theo tiêu chuẩn Python core mà không làm sập chương trình đột ngột.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích chi tiết bản chất của lỗi Off-by-one khi làm việc với tham số `stop` của hàm `range()` trong Python và nêu quy tắc phòng tránh trong các bài toán tài chính/fintech.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Mã nguồn đạt chuẩn PEP 8, có Type Hints đầy đủ (`float`, `int`), biến đặt tên tiếng Anh dạng `snake_case`, chú thích logic bằng tiếng Việt có dấu. Không dùng `while` hay `break`.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục yêu cầu `[Tên Lớp]_[Môn Học]_Session06_Ex01`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Viết thêm đoạn mã kiểm thử tự động (sử dụng `try/except` kết hợp `assert`) để kiểm tra lại các trường hợp đầu vào lỗi và kiểm tra tính chính xác của kết quả số dư cuối kỳ.