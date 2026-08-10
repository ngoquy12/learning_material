## <center>[Phân tích] Thiết kế Hệ thống Đánh giá SLA Vận chuyển và Cấu hình Bảng điều khiển Logistics</center>

### **1. Mục tiêu**
*   **Về kiến thức:** Hiểu và áp dụng phương pháp thiết kế cấu trúc dữ liệu minh bạch, xây dựng ma trận trọng số đánh giá chất lượng dịch vụ vận chuyển (SLA) và tính toán thông số hiển thị giao diện đa thiết bị (Responsive Layout Metrics) cho hệ thống điều hành kho vận.
*   **Về kỹ năng phân tích:** Đánh giá, so sánh trade-off giữa phương pháp xử lý logic rẽ nhánh tuần tự (Imperative Conditional Logic) và phương pháp quản lý bằng sơ đồ cấu hình khai báo tập trung (Declarative Schema-driven Mapping).
*   **Về kỹ năng thực hành:** Viết báo cáo so sánh giải pháp, xây dựng lưu đồ thuật toán và triển khai mã nguồn tối ưu đáp ứng chuẩn quy định doanh nghiệp logistics.

### **2. Bối cảnh & Vấn đề**
Công ty Logistics "LogiTrack Enterprise" đang vận hành hệ thống giám sát đội xe và phân bổ vận đơn theo thời gian thực. Để đảm bảo chất lượng dịch vụ vận tải kho vận, bộ phận kỹ thuật cần phát triển một phân hệ chịu trách nhiệm kép:
1. Tính toán điểm đánh giá tổng hợp chất lượng giao hàng của từng tài xế/đội xe dựa trên 3 tiêu chí trọng số: Tỷ lệ giao hàng đúng giờ (50%), Tỷ lệ nguyên vẹn hàng hóa (30%), và Điểm đánh giá hài lòng từ khách hàng (20%). Đồng thời, hệ thống phải xác nhận điều kiện "ĐẠT CHUẨN SLA LOGISTICS" nếu điểm tổng kết từ 5.0 trở lên và số chuyến xe hoàn thành đạt tối thiểu 80% mục tiêu phân bổ.
2. Tính toán quy cách hiển thị bảng điều khiển giám sát đội xe (Responsive Dashboard) tương ứng với kích thước màn hình thiết bị của người điều phối (Mobile dưới 768px, Tablet từ 768px đến dưới 1024px, Desktop từ 1024px trở lên) nhằm đảm bảo thông tin hiển thị trực quan và tối ưu trải nghiệm vận hành.

Hiện tại, đội ngũ phát triển đang phân vân giữa việc viết mã xử lý bằng các câu lệnh điều kiện lồng nhau đơn lẻ hoặc thiết kế một cấu hình Schema tập trung để quản lý toàn bộ quy tắc nghiệp vụ. Học viên đóng vai trò Chuyên viên Phân tích Giải pháp CNTT (Solution Analyst) để đánh giá và triển khai phương án kỹ thuật tối ưu.



<p align="center">
  <img src="../images/bai_04_phan_tich_thiet_ke_he_thong_danh_gia_sla_van_chuyen_va_cau_hinh_bang_dieu_khien_logistics_diagram.png" alt="Sơ đồ luồng nghiệp vụ" width="80%">
</p>



### **3. Quy tắc nghiệp vụ**
*   **Quy tắc 1: Trọng số đánh giá SLA vận chuyển**
    *   Điểm Đúng giờ (On-Time Delivery Score): Trọng số 0.50 (50%).
    *   Điểm Nguyên vẹn hàng hóa (Cargo Integrity Score): Trọng số 0.30 (30%).
    *   Điểm Hài lòng khách hàng (Customer Rating Score): Trọng số 0.20 (20%).
    *   Điểm tổng kết SLA phải được làm tròn 2 chữ số thập phân.
*   **Quy tắc 2: Điều kiện công nhận Đạt chuẩn SLA (SLA Compliance Pass Condition)**
    *   Số chuyến xe hoàn thành thực tế phải đạt tối thiểu 80% so với tổng số chuyến được giao (`targetTrips * 0.8`).
    *   Điểm tổng kết SLA phải đạt tối thiểu từ 5.0 trở lên.
    *   Nếu vi phạm 1 trong 2 điều kiện, trạng thái kết quả trả về là `"KHÔNG ĐẠT CHUẨN SLA LOGISTICS"`, ngược lại là `"ĐẠT CHUẨN SLA LOGISTICS"`.
*   **Quy tắc 3: Cấu hình Responsive Bảng điều khiển Giám sát (Dashboard Layout Metrics)**
    *   Màn hình Mobile (dưới 768px): Loại thiết bị `"MOBILE"`, tối đa 4 xe/trang, hiển thị layout 1 cột.
    *   Màn hình Tablet (từ 768px đến dưới 1024px): Loại thiết bị `"TABLET"`, tối đa 8 xe/trang, hiển thị layout 2 cột.
    *   Màn hình Desktop (từ 1024px trở lên): Loại thiết bị `"DESKTOP"`, tối đa 12 xe/trang, hiển thị layout 4 cột.

### **4. Yêu cầu bài toán**
Học viên thực hiện bài tập phân tích theo 3 phần bắt buộc sau (Tối đa 100 điểm):

**Phần 1: Báo cáo Phân tích & So sánh Giải pháp (Trade-off Report)**
Lập báo cáo nghiên cứu đề xuất **2 giải pháp kỹ thuật khác nhau** giải quyết bài toán nghiệp vụ logistics trên:
*   *Giải pháp A (Imperative Hardcoded Approach):* Viết các hàm xử lý rẽ nhánh điều kiện lồng nhau ghép nối trực tiếp các tham số.
*   *Giải pháp B (Declarative Schema-driven Approach):* Xây dựng đối tượng ma trận cấu hình (Config Schema) tập trung quản lý trọng số, ngưỡng đạt và thông số Breakpoint giao diện.
Trình bày bảng so sánh chi tiết giữa 2 giải pháp theo 5 tiêu chí: Dung lượng bộ nhớ (Memory), Tốc độ xử lý (Speed), Độ đọc hiểu (Readability), Khả năng bảo trì & Mở rộng (Maintainability & Extensibility), Mức độ phù hợp quy định doanh nghiệp (Suitability). Bảng so sánh phải trình bày dưới dạng HTML Table với thuộc tính style đúng quy định.

**Phần 2: Giải trình Lựa chọn và Mã giả / Lưu đồ Thuật toán (Architecture Justification & Pseudocode)**
*   Đưa ra lập luận kỹ thuật phản biện để chọn ra giải pháp tối ưu nhất cho hệ thống LogiTrack Enterprise khi mở rộng quy mô đội xe.
*   Biểu diễn lưu đồ thuật toán (Flowchart) hoặc mã giả (Pseudocode) chi tiết cho giải pháp tối ưu đã chọn.

**Phần 3: Triển khai Mã nguồn Tối ưu (Implementation)**
*   Hiện thực hóa mã nguồn cho giải pháp tối ưu đã chọn (sử dụng cú pháp ngôn ngữ lập trình phù hợp với nội dung bài học).
*   Mã nguồn phải bao gồm đầy đủ việc kiểm tra điều kiện biên, tính toán chính xác điểm SLA và xuất kết quả thông số Responsive Dashboard.
*   Chạy thử nghiệm kiểm tra với ít nhất 2 bộ dữ liệu mẫu (1 trường hợp Đạt chuẩn SLA và 1 trường hợp Không đạt chuẩn SLA trên màn hình Mobile và Desktop).

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session01_Ex04`.
    Ví dụ: `HNKS25CNTT1_Tooling_Session01_Ex04`