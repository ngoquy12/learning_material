# <center>[Vận dụng nâng cao 2] Xây dựng Trình Quản lý Đặt vé Sự kiện và Hạn ngạch theo Khu vực</center>

### **1. Mục tiêu**
*   **Vận dụng chuyên sâu Closure**: Đóng gói thành công trạng thái private (hạn ngạch vé, danh sách mã vé đã check-in) cho từng khu vực khán đài (Zone A, VIP, GA) trong hệ thống Ticketbox, ngăn chặn tuyệt đối việc ghi đè dữ liệu từ môi trường toàn cục (Global Scope).
*   **Thành thạo Arrow Function & Default Parameters**: Thiết kế các mô-đun tính toán giá tiền vé, áp dụng chính sách giảm giá mua sớm (Early Bird) và phí xuất vé tự động dựa trên tham số mặc định.
*   **Tư duy kiến trúc hàm & Phạm vi biến**: Tổ chức cấu trúc code đạt chuẩn ES6+, phân tách rõ ràng giữa tham số đầu vào, biến cục bộ (Local Scope) và biến đóng gói (Closure Scope).
*   **Xử lý bẫy lỗi biên nghiệp vụ**: Thiết kế cơ chế kiểm chuẩn dữ liệu đặt vé (giới hạn lượt mua, kiểm tra số lượng vé khả dụng) và ném ra thông điệp lỗi phù hợp.

### **2. Bối cảnh & Vấn đề**
Hệ thống Ticketbox chuẩn bị mở bán vé cho đêm nhạc đại hội. Ban tổ chức đặt ra yêu cầu quản lý vận hành khắt khe cho từng khu vực khán đài:
1. Mỗi khu vực vé (ví dụ: `VIP`, `ZONE_A`, `GA`) có mức giá và hạn ngạch tổng số lượng vé khác nhau.
2. Trạng thái số vé còn dư của khu vực và danh sách các mã vé đã quét vào cổng (Check-in) tuyệt đối không được khai báo dưới dạng biến toàn cục (`global variable`) để tránh bị đè dữ liệu do lỗi từ các script khác trên trang.
3. Mỗi giao dịch mua vé của khách hàng phải qua khâu kiểm duyệt hạn ngạch nghiêm ngặt và tính toán đúng số tiền theo quy định mở bán sớm (Early Bird).

### **3. Quy tắc nghiệp vụ**
1.  **Đóng gói bộ quản lý khu vực vé (Zone Manager Scope)**:
    *   Mỗi khu vực vé được khởi tạo thông qua một hàm đóng gói (Closure) lưu trữ thông tin: Mã khu vực (`zoneId`), Đơn giá gốc (`basePrice`), Hạn ngạch tổng vé (`totalQuota`), Số vé còn lại (`remainingQuota`), và Danh sách vé đã phát hành.
    *   Biến `remainingQuota` và dữ liệu vé phải được cô lập hoàn toàn trong Lexical Scope của trình quản lý khu vực, chỉ cho phép thao tác đọc/ghi thông qua các hàm con được trả về.
2.  **Quy định hạn ngạch và giới hạn đặt vé (Booking Limits)**:
    *   Mỗi lượt đặt vé của khách hàng chỉ được phép mua từ `1` đến tối đa `4` vé cho 1 đơn hàng. Nếu khách hàng nhập số lượng vé `<= 0` hoặc `> 4`, hệ thống phải từ chối giao dịch.
    *   Nếu số vé khách hàng muốn mua vượt quá số vé còn lại trong khu vực (`remainingQuota`), hệ thống từ chối và giữ nguyên trạng thái hạn ngạch.
3.  **Tính toán giá vé và chiết khấu Early Bird (Default Parameters)**:
    *   Sử dụng Arrow Function để tính tổng tiền với các tham số mặc định: Tỷ lệ chiết khấu Early Bird (`earlyBirdRate = 0.15`, tương đương 15%) và Phí xuất vé mặc định (`serviceFee = 20000` VNĐ / đơn hàng).
    *   Công thức tổng tiền: `Tổng tiền = (Số vé * Đơn giá * (1 - Tỷ lệ chiết khấu)) + Phí dịch vụ`.
4.  **Quản lý quét mã Check-in vào cổng (Ticket Check-in Control)**:
    *   Mỗi vé được phát hành sẽ có một mã định danh duy nhất (Ticket Code).
    *   Bộ đóng gói cung cấp hàm check-in mã vé. Một mã vé chỉ được check-in thành công đúng 1 lần. Nếu quét lại mã đã check-in hoặc mã vé không tồn tại, hệ thống phải phát tín hiệu lỗi.

### **4. Yêu cầu bài toán**
Học viên hoàn thành bài tập qua 2 phần bắt buộc:

#### **Phần 1 - Báo cáo Phân tích I/O & Thiết kế Giải pháp (Analysis & Design Report)**
*   **Phân tích I/O**: Liệt kê các tham số đầu vào, kiểu dữ liệu, giá trị trả về và phạm vi biến (Global / Local / Closure) của hệ thống quản lý vé.
*   **Giải pháp kiến trúc**: Mô tả cách áp dụng Closure để đóng gói biến private và cách phối hợp Arrow Function + Default Parameters.
*   **Sơ đồ quy trình (Mermaid Flowchart)**: Vẽ sơ đồ luồng cho hàm xử lý đặt vé (`bookTickets`) chuẩn quy cách 5 hình khối:
    *   Terminator: `([Bắt đầu])` / `([Kết thúc])`
    *   Input/Output: `[/Nhận thông tin đặt vé/]`
    *   Decision: `Kiểm tra số lượng hợp lệ (1-4 vé)?`
    *   Process: `["Tính tổng tiền sau chiết khấu Early Bird"]`
    *   Flowline: Mũi tên kết nối luồng xử lý.

#### **Phần 2 - Triển khai Mã nguồn & Kiểm chuẩn Bẫy lỗi (Implementation & Edge Cases)**
*   Viết chương trình hoàn chỉnh bằng JavaScript Vanilla (ES6+) thực thi toàn bộ logic nghiệp vụ trên.
*   Ném ra ngoại lệ (`throw new Error(...)`) đối với tất cả trường hợp vi phạm quy tắc nghiệp vụ (vé mua không hợp lệ, hết vé, mã check-in không tồn tại hoặc đã bị dùng).
*   Tạo các trường hợp kiểm thử (test cases) minh họa:
    *   Khởi tạo 2 khu vực vé riêng biệt (`VIP` và `ZONE_A`).
    *   Thực thi đặt vé thành công với giá trị chiết khấu mặc định và giá trị tùy chỉnh.
    *   Thử nghiệm bẫy lỗi: Đặt quá 4 vé, đặt khi hết hạn ngạch khu vực.
    *   Thực thi quét mã check-in lần thứ nhất (thành công) và quét lại lần thứ hai (thất bại).

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSession 14_Ex8`.
    Ví dụ: `HNKS25CNTT1_Core_Session_Session 14_Ex8`
