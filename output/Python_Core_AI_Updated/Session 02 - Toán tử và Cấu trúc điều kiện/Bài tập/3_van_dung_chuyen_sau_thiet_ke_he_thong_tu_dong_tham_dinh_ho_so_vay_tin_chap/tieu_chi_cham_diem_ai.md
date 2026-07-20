### **Tiêu chí chấm điểm (AI)**
**[Thẩm định hồ sơ vay tín chấp] — Tổng điểm: 100 điểm**

#### **1. Báo cáo phân tích và Thiết kế giải pháp — 20 điểm**
*   **[10 điểm] Xác định cấu trúc I/O:** Xác định và mô tả đầy đủ các tham số kiểm thử, ràng buộc kiểu dữ liệu đầu vào và các trường thông tin đầu ra cho cả hai trường hợp APPROVED/REJECTED.
*   **[10 điểm] Mô tả giải thuật xử lý nghiệp vụ:** Vẽ sơ đồ giải thuật (Flowchart) hoặc tài liệu Pseudocode thể hiện rõ logic nhánh rẽ lồng nhau và vị trí sử dụng toán tử logic (`and`, `or`), so sánh cùng `match-case`.

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Áp dụng đúng cấu trúc điều kiện nâng cao:** Triển khai được `match-case` để phân nhóm lãi suất cơ bản theo mục đích vay và lồng logic điều chỉnh lãi suất theo điểm tín dụng mà không có lỗi cú pháp.
*   **[15 điểm] Tính toán chính xác các toán tử số học:** Thực hiện chuẩn xác công thức tính toán `monthly_payment` và tỷ lệ `DTI` bằng cách dùng đúng toán tử chia (`/`), nhân (`*`), cộng (`+`).

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Xử lý ngoại lệ hạn mức và điều kiện cứng:** Bắt chuẩn các điều kiện như tuổi biên (`age == 18`, `age == 65`), thu nhập không hợp lệ, hoặc lỗi chia cho 0 khi kỳ hạn vay (`loan_term_months`) bị gửi lên giá trị `0`.
*   **[15 điểm] Ràng buộc logic nghiệp vụ lồng nhau:** Thực thi chính xác logic phê duyệt tại phân nhóm điểm tín dụng từ `[500 - 600)` (yêu cầu DTI và không có nợ hiện tại), các điều kiện phức tạp của nhóm `[600 - 750)`.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về mã lỗi định danh:** Trả về thông báo lỗi rõ ràng hoặc mã lỗi nghiệp vụ khi gặp dữ liệu không hợp lý đầu vào (ví dụ: điểm tín dụng nằm ngoài miền từ 300 đến 850 hoặc mục đích vay không tồn tại).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Biến, hàm được đặt tên tiếng Anh mang tính gợi nhớ theo nghiệp vụ tài chính (ví dụ: `dti_ratio`, `estimated_monthly_payment`, `credit_score`).
*   **[5 điểm] Nộp bài GitHub:** Tạo repository đúng chuẩn cấu trúc đặt tên thư mục bài học `[Tên Lớp]_[Môn Học]_Session02_Ex03` và đẩy đầy đủ mã nguồn kèm theo tệp tài liệu thiết kế.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý concurrency:** Đề xuất được giải pháp hoặc mô tả phương án tối ưu (ví dụ: ghi log hồ sơ bất đồng bộ, sử dụng lock) khi có nhiều yêu cầu thẩm định được gửi tới xử lý cùng một thời điểm.