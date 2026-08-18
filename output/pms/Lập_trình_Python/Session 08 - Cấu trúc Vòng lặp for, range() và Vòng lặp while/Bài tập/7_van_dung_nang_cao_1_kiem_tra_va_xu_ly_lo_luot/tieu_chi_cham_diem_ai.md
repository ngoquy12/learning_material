### **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 1] Kiểm tra và xử lý lô lượt mượn sách thư viện — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:**
    *   Xác định chính xác các biến đầu vào (`total_records: int`, `critical_code: int`, `overdue_days: int`) và biến đầu ra (`total_fine: int`, thông báo hệ thống).
    *   Mô tả rõ vai trò nghiệp vụ của từng biến trong bài toán LIBRARY_WMS.
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:**
    *   Trình bày logic xử lý tuần tự hợp lý, làm rõ vị trí sử dụng `continue`, `break` và khối `else` của `for`.
    *   Vẽ sơ đồ Mermaid đúng cú pháp chuẩn 5 hình dạng (Oval cho Start/End, Parallelogram cho I/O, Rectangle cho Process, Diamond cho Condition).

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Nhập liệu:**
    *   Khai báo và nhận dữ liệu tổng số lượt mượn, mã vi phạm an ninh từ bàn phím chính xác.
    *   Khởi tạo biến tích lũy tổng tiền phạt (`total_fine = 0`) trước vòng lặp.
*   **[15 điểm] Cấu trúc vòng lặp for và Bộ điều khiển luồng:**
    *   Sử dụng `for record_id in range(1, total_records + 1):` đúng chuẩn.
    *   Sử dụng `continue` khi `record_id % 5 == 0` (bỏ qua lượt mượn tài liệu đặc biệt).
    *   Sử dụng `break` khi `record_id == critical_code` (ngắt hệ thống do rủi ro an ninh).
    *   Sử dụng khối `else` gắn với vòng lặp `for` để thông báo hoàn thành an toàn khi không bị `break`.

#### **3. Kiểm chuẩn dữ liệu và Chặn sai sót biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn sai sót dữ liệu đầu vào không hợp lệ:**
    *   Kiểm tra `total_records <= 0`, hiển thị thông báo lỗi và dừng chương trình sớm.
    *   Kiểm tra và xử lý nếu `overdue_days < 0` (coi như 0 ngày quá hạn, không tính phạt âm).
*   **[15 điểm] Tính toán chính xác nghiệp vụ phạt:**
    *   Tính đúng tiền phạt từng lượt = `overdue_days * 5000` (khi `overdue_days > 0`).
    *   Cập nhật cộng dồn chính xác vào `total_fine` đối với các lượt mượn được xử lý thành công.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:**
    *   Thông báo lỗi dữ liệu đầu vào rõ ràng, dễ hiểu.
    *   In cảnh báo an ninh chi tiết khi kích hoạt `break` (nêu rõ mã lượt mượn vi phạm).
    *   In báo cáo tổng kết chuyên nghiệp sau khi kết thúc ca làm việc.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:**
    *   Tên biến tiếng Anh đúng chuẩn `snake_case` (ví dụ: `total_records`, `critical_code`, `overdue_days`, `total_fine`).
    *   Có chú thích mã nguồn bằng tiếng Việt có dấu. Tuân thủ tuyệt đối phạm vi kiến thức (KHÔNG dùng `while`, `list`, `dict`, `def`, `class`).
*   **[5 điểm] Nộp bài GitHub:**
    *   Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định: `[Tên Lớp]_[Môn Học]_SessionSession 08_Ex7`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Thống kê tối ưu:**
    *   Thống kê chính xác số lượng lượt mượn đã xử lý thành công, số lượt mượn đã bỏ qua và tổng tiền phạt thu được khi lô kiểm tra kết thúc an toàn.