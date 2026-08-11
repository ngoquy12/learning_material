### **Tiêu chí chấm điểm (AI)**
**[Sáng tạo] Thiết kế hệ thống đánh giá điều kiện khuyến mãi và phân hạng đơn hàng E-Commerce — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Chủ động định nghĩa đầy đủ các trường dữ liệu đầu vào (tổng tiền, hạng hội viên, khoảng cách, mã voucher...) và dữ liệu đầu ra (mức giảm, phí ship, trạng thái duyệt) rõ ràng, hợp lý.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Mô tả chi tiết tối thiểu 3 trường hợp biên đặc thù trong E-Commerce (ví dụ: giá trị đơn hàng âm, xung đột giảm giá vượt quá giá trị đơn, hội viên bị khóa tài khoản).

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Sử dụng đúng cú pháp Mermaid biểu diễn chính xác luồng xử lý dữ liệu và logic rẽ nhánh.
*   **[10 điểm] Thiết kế vòng đời tính năng:** Thể hiện rõ các trạng thái phê duyệt (APPROVED, REJECTED, SUSPICIOUS) và điều kiện chuyển dịch giữa các trạng thái.

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Phẳng hóa hoàn toàn cấu trúc rẽ nhánh (xóa bỏ Arrow Code) bằng các toán tử logic `and`, `or`, `not`, tuân thủ 100% quy chuẩn PEP 8.
*   **[15 điểm] Xử lý lọc dữ liệu nâng cao:** Đề xuất và cài đặt thành công ít nhất 1 tính năng logic mở rộng sáng tạo (ví dụ: tính điểm hoàn tiền linh hoạt, tự động hạ cấp ưu đãi khi vi phạm khoảng cách).

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Triển khai các câu lệnh kiểm tra dữ liệu đầu vào (Data Validation) cho các kịch bản biên đã liệt kê, đảm bảo chương trình không bị lỗi gián đoạn.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Hướng đối tượng:** Mã nguồn viết sạch sẽ, tên biến/hàm đặt bằng tiếng Anh theo chuẩn `snake_case`, thụt lề 4 khoảng trắng chuẩn PEP 8.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định, commit message rõ ràng và kèm tệp README mô tả giải pháp.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Xây dựng cơ chế ghi nhật ký thẩm định (Audit Log / Trace Details) giải thích chi tiết lý do tại sao đơn hàng được chấp nhận hoặc bị từ chối ưu đãi.