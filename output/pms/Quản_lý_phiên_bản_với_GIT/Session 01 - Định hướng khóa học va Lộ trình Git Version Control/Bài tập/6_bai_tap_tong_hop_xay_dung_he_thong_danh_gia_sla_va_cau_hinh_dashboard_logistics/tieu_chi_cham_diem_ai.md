### **Tiêu chí chấm điểm (AI)**
**[Bài tập tổng hợp] Xây dựng Hệ thống Đánh giá SLA và Cấu hình Dashboard Logistics — Tổng điểm: 100 điểm**

#### **1. Khởi tạo Dự án & Schema dữ liệu — 20 điểm**
*   **[10 điểm] Thiết lập cấu trúc file và mô tả đối tượng dữ liệu SLA/Breakpoint:** Tạo đúng file `logistics_system.js`, cấu trúc mã nguồn rõ ràng, khai báo các hằng số trọng số minh bạch.
*   **[10 điểm] Định nghĩa đối tượng chứa trọng số và ngưỡng kiểm tra SLA hợp lệ:** Khởi tạo Class `LogisticsEvaluationEngine` có thuộc tính `partnerCode`, `totalAssignedTrips` và đối tượng `weights` chứa các tỷ lệ `0.50`, `0.30`, `0.20`.

#### **2. Hiện thực hóa các Chức năng cơ bản — 40 điểm**
*   **[20 điểm] Hiện thực hóa phương thức tính điểm tổng kết SLA theo đúng trọng số:** Phương thức `calculateSLAScore` tính toán chính xác theo công thức trọng số `50% - 30% - 20%` và sử dụng `toFixed(2)` chuẩn xác.
*   **[20 điểm] Hiện thực hóa hàm tính toán quy chuẩn hiển thị Layout Responsive Dashboard:** Hàm `calculateLogisticsLayoutMetrics` phân loại đúng 3 thiết bị (MOBILE, TABLET, DESKTOP) với số lượng `maxOrdersPerPage` (4, 8, 12) và `layoutColumns` (1, 2, 4) chính xác theo `viewportWidth`.

#### **3. Kiểm chuẩn logic & Chặn bẫy dữ liệu cơ bản — 20 điểm**
*   **[10 điểm] Kiểm tra chính xác điều kiện hoàn thành chuyến xe tối thiểu (80%) và ngưỡng điểm đạt SLA (>= 5.0):** Phương thức `verifySLACompliance` tính đúng số chuyến xe tối thiểu (`totalAssignedTrips * 0.8`) và xác định đúng biến boolean `isSLACompliant`.
*   **[10 điểm] Xây dựng chuẩn xác cấu trúc Prompt RCTC 4 thành phần hỗ trợ tra cứu báo cáo vận đơn:** Chuỗi `LOGISTICS_PROMPT_TEMPLATE` có đầy đủ 4 phần `[Role]`, `[Context]`, `[Task]`, `[Constraint]` đúng quy chuẩn RCTC đã học.

#### **4. Chất lượng mã nguồn và Đóng gói Response — 10 điểm**
*   **[10 điểm] Định dạng dữ liệu đầu ra sạch:** Mã nguồn sử dụng 100% tên biến/hàm bằng tiếng Anh (`calculateSLAScore`, `verifySLACompliance`, `calculateLogisticsLayoutMetrics`), chú thích tiếng Việt có dấu đầy đủ, output `console.log` rõ ràng, không sử dụng emoji.

#### **5. Quy chuẩn nộp bài GitHub — 10 điểm**
*   **[10 điểm] Nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng quy chuẩn tên thư mục `[Tên Lớp]_[Môn Học]_Session01_Ex06` (Ví dụ: `HNKS25CNTT1_Tooling_Session01_Ex06`).