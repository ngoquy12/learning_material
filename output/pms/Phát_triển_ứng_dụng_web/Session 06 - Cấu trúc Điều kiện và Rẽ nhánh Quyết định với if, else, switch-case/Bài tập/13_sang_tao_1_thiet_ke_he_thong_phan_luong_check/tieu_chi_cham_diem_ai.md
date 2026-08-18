### **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 1] Thiết Kế Hệ Thống Phân Luồng Check-in và Tính Phí Hành Lý Hàng Không — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Định nghĩa danh sách biến đầu vào và đầu ra đầy đủ, hợp lý, phục vụ chính xác bài toán rẽ nhánh phân hạng vé, tuyến bay và hành lý check-in.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Phát hiện tối thiểu 3 kịch bản bẫy lỗi biên nghiệp vụ (Ví dụ: trọng lượng âm, cước phí vượt quá mức tối đa an toàn bay, mã tuyến bay không khớp switch-case default).

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ đúng sơ đồ Mermaid minh họa luồng rẽ nhánh qua các tầng xử lý `switch-case` và `if-else`. Tuân thủ tuyệt đối quy chuẩn 5 hình khối chuẩn (Oval cho Start/End, Parallelogram cho Input/Output, Diamond cho Condition, Rectangle cho Action).
*   **[10 điểm] Thiết kế vòng đời tính năng:** Trình bày mạch lạc logic xử lý từ bước nhận diện thông tin khách hàng đến bước đưa ra quyết định phí và luồng ưu tiên.

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Kết hợp chuẩn xác `switch-case` để phân loại đơn giá theo tuyến bay và `if-else if-else` để tính cước phí hành lý quá cân theo hạn mức hạng vé + hạng thẻ.
*   **[15 điểm] Áp dụng Toán tử ba ngôi và Tối ưu mã nguồn:** Sử dụng toán tử ba ngôi `? :` đúng cách cho các câu gán nhãn ưu tiên và trạng thái hóa đơn; tuyệt đối không vi phạm bẫy lồng ghép quá mức (nested ternary).

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Triển khai các câu lệnh kiểm tra đầu vào (data guards) để phát hiện và cảnh báo dữ liệu không hợp lệ trước khi tính toán.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Chuẩn đặt tên:** Mã nguồn sạch sẻ, căn lề chuẩn 2 spaces, biến đặt bằng tiếng Anh theo chuẩn `camelCase`, comment giải thích logic bằng Tiếng Việt có dấu đầy đủ.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Tạo cấu trúc thư mục chuẩn theo yêu cầu, commit rõ ràng và có README mô tả kịch bản test.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Xây dựng mô-đun in ra bảng tóm tắt nhật ký giao dịch check-in (Audit Log Text) ghi nhận chi tiết thời gian và lý do tính phí quá cước/cấp quyền ưu tiên cho khách hàng.