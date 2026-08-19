# **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 4] Sửa lỗi cập nhật và xóa chuyến đi GrabRide — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra chính xác các dòng mã nguồn truy cập trực tiếp bằng `stt_cap_nhat` và `stt_xoa` mà không trừ đi 1.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thiện đầy đủ thông tin cho Test Case 2 và Test Case 3 trong bảng báo cáo (Input, Buggy Output, Expected Output, Failing Line và Logic Note).

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Chuyển đổi chính xác số thứ tự nghiệp vụ (1-based) thành chỉ số mảng (0-based) qua công thức `stt - 1` trước khi thực hiện cập nhật và xóa.
*   **[20 điểm] Kết quả đầu ra chính xác:** Danh sách sau xử lý và số lượng chuyến đi còn lại được in ra màn hình khớp hoàn toàn với yêu cầu nghiệp vụ.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Đảm bảo các biến nhập vào đúng kiểu dữ liệu số nguyên `int`.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Đảm bảo chỉ số sau khi chuyển đổi nằm trong phạm vi hợp lệ của danh sách (`0 <= index < len(danh_sach)`).

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích được vì sao lỗi Off-by-one thường xảy ra khi chuyển giao giữa yêu cầu nghiệp vụ của người dùng và lập trình hệ thống, đưa ra giải pháp phòng ngừa trong thực tế.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến rõ ràng theo chuẩn `snake_case`, ghi chú code ngắn gọn bằng tiếng Việt có dấu, tuân thủ PEP 8 và có Type Hints (`list[int]`).
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định `[Tên Lớp]_[Môn Học]_SessionSession 10_Ex4`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý thứ tự thao tác:** Viết thêm câu lệnh kiểm tra thứ tự xóa để tránh làm thay đổi chỉ số của các phần tử đứng sau khi thực hiện liên tiếp nhiều thao tác xóa/cập nhật.
