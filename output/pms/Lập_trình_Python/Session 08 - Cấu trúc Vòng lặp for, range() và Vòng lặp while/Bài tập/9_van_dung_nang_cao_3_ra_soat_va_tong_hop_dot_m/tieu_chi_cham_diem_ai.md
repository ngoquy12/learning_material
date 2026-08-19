# **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 3] Rà soát và Tổng hợp Đợt mượn trả Sách Thư viện LIBRARY_WMS — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:** Trình bày đầy đủ, chính xác các biến đầu vào (`start_id`: int, `end_id`: int) và đầu ra (`valid_count`: int, `skipped_count`: int, `total_fine`: int, thông báo trạng thái).
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:** Đề xuất được thuật toán điều khiển luồng hợp lý. Vẽ sơ đồ luồng Mermaid chính xác, đúng 100% quy chuẩn ký hiệu (Oval cho Start/End, Parallelogram cho I/O, Diamond cho Điều kiện, Rectangle cho Tiến trình/Tính toán).

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Schema:** Khởi tạo đúng các biến tích lũy trạng thái trong bộ nhớ (`valid_count = 0`, `skipped_count = 0`, `total_fine = 0`) trước khi đi vào vòng lặp.
*   **[15 điểm] Hàm/Module xử lý nghiệp vụ tích hợp:** Duyệt dải mã bằng `for borrow_id in range(start_id, end_id + 1)`. Xử lý chính xác logic `break` khi mã chia hết cho 21, logic `continue` khi mã chia hết cho 5, và tính tiền phạt tích lũy cho các mã hợp lệ. Kích hoạt khối `else` của vòng lặp `for` đúng thời điểm.

#### **3. Kiểm chuẩn dữ liệu và Chặn sai sót biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn sai sót dữ liệu trùng lặp / Vượt ngưỡng:** Xử lý chính xác trường hợp `start_id > end_id` (in thông báo lỗi dữ liệu đầu vào không hợp lệ trước khi thực thi lặp).
*   **[15 điểm] Validate dữ liệu đầu vào nâng cao:** Chặn sai sót trường hợp dải mã chứa số âm hoặc số 0, đưa ra cảnh báo yêu cầu nhập số nguyên dương hợp lệ.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:** Hiển thị thông báo trạng thái rõ ràng phân biệt giữa hai kịch bản: dừng khẩn cấp do nghi ngờ gian lận (kèm mã `borrow_id` vi phạm) và hoàn thành an toàn qua khối `else`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Tên biến bằng tiếng Anh theo quy chuẩn `snake_case`. Chú thích code rõ ràng bằng tiếng Việt có dấu. Tuân thủ 100% giới hạn kiến thức (KHÔNG dùng `while`, `def`, `list`, `dict`, `tuple`, `set`, `class`).
*   **[5 điểm] Nộp bài GitHub:** Tạo repository và đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định (`[Tên Lớp]_[Môn Học]_SessionSession 08_Ex9`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ:** Tối ưu hóa các câu lệnh điều khiển điều kiện, tránh lặp lại các phép toán chia lấy dư không cần thiết và in báo cáo định dạng rõ ràng, chuyên nghiệp.
