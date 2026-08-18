### **Tiêu chí chấm điểm (AI)**
**[Phân tích 1] Thiết kế luồng kiểm tra nhật ký mượn trả và tự động xử lý ngoại lệ trong LIBRARY_WMS — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:**
    *   Nêu rõ sự khác biệt về cấu trúc logic giữa ít nhất 02 phương án điều khiển vòng lặp (ví dụ: Cấu trúc sử dụng cú pháp đặc thù `for...else` ngắn gọn kết hợp `break`/`continue` trực tiếp VS Cấu trúc dùng biến cờ hiệu `flag` kết hợp `if-else` truyền thống).
    *   Phân tích ưu điểm và nhược điểm của từng phương án trong bối cảnh ứng dụng LIBRARY_WMS.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:**
    *   Trình bày đầy đủ 5 tiêu chí: Thời gian thực thi, Dung lượng bộ nhớ, Khả năng bảo trì, Độ dễ đọc, Mức độ phù hợp.
    *   Định dạng bảng tuân thủ đúng chuẩn bảng HTML với style bắt buộc.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:**
    *   Đưa ra lập luận thuyết phục, có căn cứ kỹ thuật giải thích lý do chọn phương án tối ưu (ví dụ: tận dụng tính năng đặc trưng `for...else` của Python giúp mã nguồn ngắn gọn, loại bỏ biến cờ hiệu thừa, dễ đọc và tối ưu hiệu năng).
*   **[10 điểm] Thiết kế Lưu đồ thuật toán (Mermaid Flowchart):**
    *   Sử dụng đúng 100% quy chuẩn 5 hình dạng trong Mermaid: Oval cho Start/End, Parallelogram cho Input/Output, Diamond cho Condition check, Rectangle cho Action/Process calculations.
    *   Biểu diễn chính xác các nhánh điều kiện `break`, `continue`, khối `else` và luồng tăng biến đếm tự động của vòng lặp `for`.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:**
    *   Sử dụng đúng cấu trúc vòng lặp `for` với `range(1, total_records + 1)`.
    *   Áp dụng chính xác câu lệnh `continue` để bỏ qua bản ghi có `borrow_id % 4 == 0`.
    *   Áp dụng chính xác câu lệnh `break` khi `borrow_id == critical_flag_id`.
    *   Tận dụng khối `else` gắn liền với vòng lặp `for` để thông báo hoàn thành khi duyệt hết danh sách không bị ngắt.
    *   Tuân thủ tuyệt đối giới hạn kiến thức: KHÔNG dùng `while`, `list`, `dict`, `def`, `class`.
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:**
    *   Kiểm tra và xử lý trường hợp `total_records <= 0` ngay trước khi vào vòng lặp.
    *   Xử lý biến `overdue_days_unit < 0` để đảm bảo phí phạt không bao giờ bị tính giá trị âm.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:**
    *   In đầy đủ các thông điệp cảnh báo nghiệp vụ (Bỏ qua bản ghi lỗi nhẹ, Cảnh báo dừng khẩn cấp do vi phạm an ninh, Tính phí phạt quá hạn hợp lệ).
    *   Xuất đúng tổng tiền phạt tích lũy khi tiến trình chạy tới khối `else` an toàn.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:**
    *   Tên biến đúng chuẩn `snake_case` bằng tiếng Anh (vd: `total_records`, `critical_flag_id`, `total_fine`, `overdue_days_unit`).
    *   Mã nguồn thụt lề 4 dấu cách (PEP 8), chú thích logic đầy đủ bằng tiếng Việt có dấu.
*   **[5 điểm] Nộp bài GitHub:**
    *   Cung cấp link GitHub repository hợp lệ, đúng cấu trúc thư mục quy định (`[Tên Lớp]_[Môn Học]_SessionSession 08_Ex10`).

---

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Kịch bản Phân tích Hiệu năng Thực nghiệm (Benchmark Script):**
    *   Viết kịch bản kiểm thử giả lập đo đạc thời gian thực thi (sử dụng module `time`) so sánh hiệu năng chạy giữa giải pháp dùng `for...else` trực tiếp và giải pháp dùng biến cờ hiệu `flag` trung gian khi số lượng bản ghi $N = 100.000$.