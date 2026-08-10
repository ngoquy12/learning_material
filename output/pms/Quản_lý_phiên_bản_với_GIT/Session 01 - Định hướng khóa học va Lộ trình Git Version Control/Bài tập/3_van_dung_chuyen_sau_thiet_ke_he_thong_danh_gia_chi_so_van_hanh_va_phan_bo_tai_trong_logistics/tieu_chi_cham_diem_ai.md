### **Tiêu chí chấm điểm (AI)**
**[Vận dụng chuyên sâu] Thiết kế hệ thống đánh giá chỉ số vận hành và phân bổ tải trọng Logistics — Tổng điểm: 100 điểm**

#### **1. Báo cáo phân tích và Thiết kế giải pháp — 20 điểm**
*   **[10 điểm] Xác định cấu trúc I/O:** Liệt kê đầy đủ kiểu dữ liệu, tên tham số đầu vào và cấu trúc đối tượng trả về cho phương thức tính SLA và hàm phân bổ tải trọng.
*   **[10 điểm] Mô tả giải thuật xử lý nghiệp vụ:** Trình bày rõ ràng các bước logic bằng mã giả (Pseudocode) hoặc sơ đồ luồng môt tả quá trình tính điểm trọng số 20-30-50, kiểm tra điều kiện 80% chặng đường và phân loại tải trọng.

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Schema:** Thiết kế lớp `LogisticsEvaluationEngine` lưu giữ cấu hình trọng số minh bạch (0.20, 0.30, 0.50) và hằng số phân loại tải trọng (`WEIGHT_BREAKPOINTS`).
*   **[15 điểm] Hàm/Module xử lý nghiệp vụ tích hợp:** Triển khai chính xác công thức tính điểm làm tròn 2 chữ số thập phân và hàm `calculatePayloadLayout` tính đúng số kiện hàng/làn xếp hàng theo trọng lượng cargo.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy dữ liệu trùng lặp / Vượt ngưỡng:** Xử lý chính xác trường hợp số chặng đã hoàn thành lớn hơn tổng số chặng (`completedMilestones > totalMilestones`) và tính toán đúng ngưỡng 80% số chặng tối thiểu.
*   **[15 điểm] Validate dữ liệu đầu vào nâng cao:** Đảm bảo điểm thành phần (`onTimeScore`, `safetyScore`, `deliveryScore`) nằm trong phạm vi từ 0 đến 10 điểm, cảnh báo hoặc dừng xử lý nếu dữ liệu không hợp lệ.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:** Trả về đối tượng báo cáo chi tiết chứa thông điệp rõ ràng (`"ĐẠT CHUẨN VẬN HÀNH SLA"` hoặc `"KHÔNG ĐẠT CHUẨN VẬN HÀNH SLA"`) đi kèm các chỉ số thống kê minh bạch.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Danh xưng biến, hàm, lớp sử dụng Tiếng Anh chuẩn (như `LogisticsEvaluationEngine`, `calculatePayloadLayout`, `isSlaPassed`), phần chú thích giải thích thuật toán bằng Tiếng Việt có dấu.
*   **[5 điểm] Nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định (`[Tên Lớp]_[Môn Học]_Session01_Ex03`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ:** Đóng gói module linh hoạt, cho phép truyền cấu hình trọng số tùy chỉnh để mở rộng cho các loại hình vận tải đặc thù (Đường sắt, Đường thủy, Đường hàng không).