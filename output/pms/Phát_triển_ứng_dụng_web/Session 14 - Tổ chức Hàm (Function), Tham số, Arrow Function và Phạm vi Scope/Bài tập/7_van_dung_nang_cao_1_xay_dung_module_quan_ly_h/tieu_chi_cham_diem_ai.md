### **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 1] Xây dựng Module Quản lý Hạn ngạch và Chiết khấu Vé Concert — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:** Trình bày đầy đủ kiểu dữ liệu của các tham số (bao gồm tham số mặc định `maxQuota = 4`, `zoneType = 'GA'`, `isEarlyBird = false`) và cấu trúc đối tượng dữ liệu trả về sau khi giao dịch thành công hoặc thất bại.
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:** Giải thích rõ ràng nguyên lý hoạt động của Closure trong việc bảo vệ state `accumulatedTickets` và vẽ sơ đồ luồng xử lý (Mermaid hoặc các bước Pseudocode) logic mua vé đúng quy chuẩn.

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Closure:** Triển khai đúng hàm khởi tạo quản lý vé sử dụng Closure để đóng gói biến nội bộ `accumulatedTickets`, chứng minh tính độc lập dữ liệu giữa các khách hàng khác nhau.
*   **[15 điểm] Hàm/Module xử lý nghiệp vụ tích hợp:** Viết phương thức mua vé bằng Arrow Function, tính toán chuẩn xác giá vé theo hệ số Zone (`VIP`, `ZONE_A`, `GA`) và trừ phần trăm chiết khấu Early Bird (15%).

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy dữ liệu trùng lặp / Vượt ngưỡng:** Kiểm tra chính xác điều kiện `accumulatedTickets + ticketQuantity > maxQuota`. Từ chối giao dịch và không cộng dồn vé nếu vi phạm hạn ngạch.
*   **[15 điểm] Validate dữ liệu đầu vào nâng cao:** Kiểm tra giá vé cơ bản `basePrice > 0`, số lượng vé `ticketQuantity` phải là số nguyên nằm trong khoảng từ 1 đến 4, xử lý trường hợp mã Zone không hợp lệ một cách an toàn.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:** Khi giao dịch thất bại (do vượt hạn ngạch hoặc dữ liệu không hợp lệ), trả về thông báo lỗi rõ ràng, mô tả đúng lý do từ chối mà không làm sập ứng dụng.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Sử dụng tên biến/hàm bằng tiếng Anh chuẩn camelCase (ví dụ: `createTicketManager`, `calculateTicketPrice`, `accumulatedTickets`), comment giải thích logic bằng tiếng Việt có dấu.
*   **[5 điểm] Nộp bài GitHub:** Tạo đúng cấu trúc thư mục `[Tên Lớp]_[Môn Học]_Session14_Ex7` và đẩy đầy đủ file báo cáo + mã nguồn lên GitHub.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ:** Viết mã nguồn ngắn gọn, tối ưu cú pháp Arrow Function (implicit return phù hợp), đóng gói thông tin báo cáo giao dịch chi tiết bao gồm cả số dư hạn ngạch còn lại của khách hàng ngay sau mỗi lần mua.