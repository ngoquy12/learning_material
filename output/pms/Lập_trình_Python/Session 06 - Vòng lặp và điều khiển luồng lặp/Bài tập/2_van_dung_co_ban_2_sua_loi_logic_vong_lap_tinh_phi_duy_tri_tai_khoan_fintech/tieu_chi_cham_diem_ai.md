### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 2] Sửa Lỗi Logic Vòng Lặp Tính Phí Duy Trì Tài Khoản Fintech — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra chính xác lỗi nằm ở tham số dừng của câu lệnh `range(1, total_months)` khiến vòng lặp dừng lại ngay trước giá trị `total_months`.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Cung cấp bảng HTML gồm tối thiểu 3 test cases thể hiện rõ Input, Actual Output bị thiếu tiền phí và Expected Output đúng quy tắc nghiệp vụ.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Điều chỉnh phạm vi vòng lặp `for` thành `range(1, total_months + 1)`, đảm bảo tháng cuối cùng trong chu kỳ được tính toán chính xác.
*   **[20 điểm] Xử lý ngoại lệ chuẩn ngôn ngữ:** Sử dụng đúng từ khóa `continue` để bỏ qua tính phí tháng VIP và phát ra ngoại lệ `raise ValueError(...)` khi tham số đầu vào không hợp lệ.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Kiểm tra điều kiện `monthly_fee < 0` hoặc `total_months <= 0` ngay từ đầu hàm.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Thông báo lỗi ngoại lệ ghi nhận thông điệp rõ ràng bằng tiếng Việt, ngăn chặn việc tính toán dữ liệu rác.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích cơ chế hoạt động của tham số `stop` trong hàm `range()` và rủi ro thất thoát tài chính khi xảy ra lỗi Off-by-one trong hệ thống Fintech.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Tuân thủ quy chuẩn PEP 8 (thụt lề 4 khoảng trắng, đặt tên biến/hàm dạng `snake_case`, sử dụng Type Hints đầy đủ). Không sử dụng các từ khóa bị cấm (`while`, `break`).
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Khởi tạo repository và đẩy mã nguồn đúng cấu trúc thư mục `[Tên Lớp]_[Môn Học]_Session06_Ex02`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Viết thêm script kiểm thử tự động sử dụng khối `try...except` để verify hành vi `ValueError` khi truyền phí âm và số tiền quyết toán đúng cho 6 tháng.