### **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 2] Xây dựng Trình Quản lý Đặt vé Sự kiện và Hạn ngạch theo Khu vực — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:** Liệt kê đầy đủ tên tham số, kiểu dữ liệu, giá trị mặc định và xác định chính xác phạm vi biến (Global Scope, Local Scope, Closure State Scope) trong ứng dụng.
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:** Mô tả kiến trúc Closure đóng gói dữ liệu và vẽ sơ đồ luồng Mermaid đầy đủ 5 hình khối chuẩn (Terminator, Input/Output, Decision, Process, Flowline).

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Scope Closure:** Định nghĩa hàm tạo bộ quản lý khu vực vé (Zone Manager) sử dụng Closure để lưu trữ biến cục bộ `remainingQuota` và danh sách vé, không làm lộ biến ra Global Scope.
*   **[15 điểm] Hàm/Module xử lý nghiệp vụ tích hợp:** Sử dụng Arrow Function và Default Parameters (`earlyBirdRate = 0.15`, `serviceFee = 20000`) để tính toán hóa đơn và quản lý lượt check-in chính xác theo công thức nghiệp vụ.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy dữ liệu vượt ngưỡng:** Kiểm tra và từ chối xử lý khi khách hàng đặt ít hơn 1 vé, nhiều hơn 4 vé, hoặc khi số vé yêu cầu vượt quá số lượng vé còn lại trong khu vực.
*   **[15 điểm] Validate dữ liệu đầu vào nâng cao & Check-in:** Đảm bảo mỗi mã vé chỉ được check-in 1 lần duy nhất; chặn các thao tác check-in với mã vé giả lập không tồn tại.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:** Ném ra các lỗi rõ ràng bằng `throw new Error(...)` kèm mô tả Tiếng Việt nguyên nhân thất bại chi tiết cho từng kịch bản lỗi biên.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Sử dụng tên hàm/biến bằng Tiếng Anh chuẩn `camelCase`, comment giải thích logic bằng Tiếng Việt có dấu, cấu trúc mã nguồn mạch lạc không dùng các từ khóa/khái niệm cấm.
*   **[5 điểm] Nộp bài GitHub:** Đẩy báo cáo và mã nguồn lên repository GitHub đúng cấu trúc tên thư mục quy định `[Tên Lớp]_[Môn Học]_SessionSession 14_Ex8`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ & Mở rộng:** Đề xuất được giải pháp quản lý danh sách nhiều sự kiện khác nhau hoặc xây dựng cơ chế hủy đặt vé (ticket cancellation) hoàn trả hạn ngạch an toàn trong phạm vi Closure.