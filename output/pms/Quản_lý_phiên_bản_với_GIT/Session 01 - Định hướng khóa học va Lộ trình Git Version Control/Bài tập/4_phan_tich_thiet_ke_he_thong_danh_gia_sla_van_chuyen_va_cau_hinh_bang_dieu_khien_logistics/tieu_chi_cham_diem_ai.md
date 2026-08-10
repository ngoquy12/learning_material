### **Tiêu chí chấm điểm (AI)**
**[Phân tích] Thiết kế Hệ thống Đánh giá SLA Vận chuyển và Cấu hình Bảng điều khiển Logistics — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:** Trình bày rõ ràng và chi tiết sự khác biệt về mặt cấu trúc và tư duy thuật toán giữa giải pháp rẽ nhánh tuần tự (Imperative Hardcoded) và giải pháp quản lý theo sơ đồ cấu hình khai báo (Declarative Schema-driven).
*   **[15 điểm] Bảng so sánh Trade-off trực quan:** Lập bảng so sánh đầy đủ 5 tiêu chí (Tốc độ xử lý, Dung lượng bộ nhớ, Khả năng bảo trì, Độ đọc hiểu, Mức độ phù hợp doanh nghiệp) với định dạng thẻ HTML Table có thuộc tính `style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%"`.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:** Giải trình thuyết phục lý do chọn giải pháp Declarative Schema nhằm phục vụ khả năng bảo trì và mở rộng quy mô nghiệp vụ kho vận của doanh nghiệp.
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:** Trình bày chi tiết mã giả (Pseudocode) hoặc lưu đồ thuật toán (Flowchart) thể hiện chính xác luồng xử lý tính điểm SLA và quy đổi Responsive Breakdown.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:** Viết mã nguồn hoàn chỉnh theo giải pháp đã chọn, tính toán chính xác trọng số 50% - 30% - 20% và phân loại đúng loại thiết bị (Mobile < 768px, Tablet 768-1023px, Desktop >= 1024px).
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:** Kiểm tra đầy đủ điều kiện biên (chuyến xe đạt tối thiểu 80%, điểm SLA tối thiểu 5.0, làm tròn 2 chữ số thập phân).

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:** Trả về đối tượng (Object/Dictionary) chứa thông tin kết quả SLA và thông số Responsive Layout đầy đủ, chính xác, không thừa thiếu thuộc tính.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:** Tên biến, danh xưng hàm viết bằng Tiếng Anh chuẩn Clean Code; các câu lệnh ghi chú giải thích logic bằng Tiếng Việt có dấu chuẩn sản xuất.
*   **[5 điểm] Nộp bài GitHub:** Nộp đường dẫn repository GitHub đúng cấu trúc thư mục quy định: `[Tên Lớp]_[Môn Học]_Session01_Ex04`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Benchmark Script:** Xây dựng kịch bản kiểm thử đo lường thời gian thực thi (execution time) giữa 2 phương pháp xử lý khi duyệt qua mảng dữ liệu thử nghiệm lớn.