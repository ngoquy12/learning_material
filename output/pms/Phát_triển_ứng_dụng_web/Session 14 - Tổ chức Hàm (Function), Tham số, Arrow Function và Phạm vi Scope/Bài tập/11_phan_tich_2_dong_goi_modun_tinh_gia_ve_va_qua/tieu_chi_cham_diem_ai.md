### **Tiêu chí chấm điểm (AI)**
**[Phân tích 2] Đóng Gói Mô-đun Tính Giá Vé và Quản Lý Hạn Ngạch Đặt Vé Concert — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:** Học viên tự khám phá và trình bày rõ ràng 2 phương án thiết kế kiến trúc hàm/scope/closure khác nhau (ví dụ: Phương án sử dụng Factory Function trả về Closure Object độc lập vs Phương án tổ chức hàm Module lồng nhau với biến đóng gói nội bộ), không trùng lặp logic.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:** Thiết lập bảng HTML chuẩn format, so sánh 2 giải pháp trên đủ 5 tiêu chí (Tốc độ thực thi, Bộ nhớ, Bảo trì, Độ dễ đọc, Mức độ đóng gói). Đánh giá có chiều sâu kĩ thuật.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:** Giải thích phục phục được lý do chọn phương án tối ưu dựa trên bài toán thực tế của Ticketbox (chống gian lận hạn ngạch, an toàn bộ nhớ khi mở rộng).
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:** Vẽ sơ đồ Mermaid Flowchart chuẩn 100% hình dạng quy chuẩn (Terminator `([ ])`, Input/Output `[/ /]`, Decision `?`, Process `[" "]`). Luồng logic kiểm tra hạn ngạch và tính tiền được thể hiện chặt chẽ.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:** Viết mã nguồn JavaScript ES6+ hoàn chỉnh. Sử dụng đúng Arrow Function, Default Parameters, Closure để bảo vệ biến đếm vé không bị lộ ra Global Scope.
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:** Xử lý triệt để tất cả rào chắn dữ liệu: kiểm tra số lượng vé hợp lệ (số nguyên dương), kiểm tra tổng số vé đã mua không vượt quá 4, xử lý an toàn giá trị mặc định khi truyền đối số bằng `0`.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:** Hàm tính toán hoặc closure trả về đối tượng kết quả rõ ràng (gồm: số tiền gốc, chiết khấu, thuế, phí dịch vụ, tổng thanh toán, số vé còn lại có thể mua) không chứa thuộc tính thừa.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:** Đặt tên hàm, tham số, biến tiếng Anh theo chuẩn camelCase (ví dụ: `calculateTicketPrice`, `purchasedTicketsCount`, `maxTicketQuota`). Mã nguồn trình bày sạch đẹp, có ghi chú giải thích logic bằng tiếng Việt có dấu.
*   **[5 điểm] Nộp bài GitHub:** Khởi tạo repository và nộp đúng cấu trúc thư mục `[Tên Lớp]_[Môn Học]_Session14_Ex11`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Benchmark Script:** Viết đoạn mã script đo lường thời gian xử lý và mức tiêu hao tài nguyên khi gọi hàm đếm vé/tính giá tiền 100,000 lần liên tiếp giữa 2 phương án để chứng minh tính vượt trội của phương án được chọn.