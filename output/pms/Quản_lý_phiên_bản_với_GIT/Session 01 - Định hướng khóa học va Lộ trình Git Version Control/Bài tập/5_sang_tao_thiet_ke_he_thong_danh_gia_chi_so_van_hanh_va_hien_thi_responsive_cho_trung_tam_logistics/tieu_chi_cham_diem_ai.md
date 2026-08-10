### **Tiêu chí chấm điểm (AI)**
**[Sáng tạo] Thiết kế hệ thống đánh giá chỉ số vận hành và hiển thị Responsive cho trung tâm Logistics — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Định nghĩa đầy đủ, minh bạch cấu trúc dữ liệu đầu vào và đầu ra cho phân hệ đánh giá SLA vận đơn và phân hệ tính toán responsive layout; tên trường chuẩn tiếng Anh, đúng kiểu dữ liệu.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Phân tích và chỉ ra tối thiểu 3 bẫy dữ liệu hợp lý trong thực tế kho vận (như trọng số không hợp lệ, điểm số vượt dải 0-10, kích thước màn hình không chuẩn, tham số rỗng).

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Xây dựng sơ đồ Mermaid chi tiết, chính sở cú pháp, thể hiện rõ luồng dịch chuyển dữ liệu qua từng bước xử lý logic.
*   **[10 điểm] Thiết kế vòng đời tính năng:** Trình bày rõ ràng các trạng thái vận hành của đơn hàng/chuyến xe và các ngưỡng điều kiện chuyển đổi trạng thái SLA.

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Cài đặt lớp hoặc hàm tính toán điểm tổng kết SLA theo đúng trọng số nghiệp vụ, làm tròn 2 chữ số thập phân và đánh giá điều kiện đạt chuẩn vận hành (Passed/Failed).
*   **[15 điểm] Xử lý lọc dữ liệu và cấu hình hiển thị:** Triển khai chính xác logic phân loại thiết bị theo viewport width, trả về đúng số lượng thẻ hiển thị và số cột layout tương ứng. Triển khai đúng mẫu Prompt RCTC hỗ trợ báo cáo.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Viết đầy đủ các mã kiểm tra (guards/validations) để chặn các trường hợp bẫy lỗi đã phát hiện ở Phần 2 kèm thông báo lỗi rõ ràng.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Hướng đối tượng:** Mã nguồn viết sạch sẻ, phân tách hàm/lớp rõ ràng, đặt tên biến/hàm 100% bằng tiếng Anh, chú thích giải thích logic bằng tiếng Việt có dấu.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Nộp bài đúng cấu trúc thư mục quy định (`[Tên Lớp]_[Môn Học]_Session01_Ex05`), lịch sử commit rõ ràng, README mô tả đầy đủ cách chạy dự án.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Triển khai thêm mô-đun lưu trữ nhật ký kiểm toán (Audit Log) ghi lại lịch sử thay đổi trọng số SLA hoặc lịch sử đánh giá vận đơn của trung tâm điều hành.