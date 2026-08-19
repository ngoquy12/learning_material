# <center>[Sáng tạo 1] Thiết kế Module Đóng gói Quản lý Vé và Check-in Sự kiện Concert</center>

### **1. Mục tiêu**
*   **Về kiến thức:** Vận dụng linh hoạt các phương thức khai báo hàm (Function Declaration, Function Expression), cú pháp rút gọn Arrow Function, cơ chế Tham số mặc định (Default Parameters) và kỹ thuật đóng gói scope bằng Closure.
*   **Về kỹ năng:** Tự phân tích bài toán thực tế, thiết kế cấu trúc I/O Schema, xây dựng sơ đồ luồng dữ liệu (Data Flow Diagram) và triển khai giải pháp lập trình JavaScript nâng cao cho hệ thống quản lý bán vé sự kiện.
*   **Về tư duy:** Xây dựng tư duy thiết kế phần mềm bảo mật thông tin (Data Encapsulation), ngăn chặn ô nhiễm phạm vi toàn cục (Global Scope Contamination) và tự phát hiện các góc khuất dữ liệu (Edge Cases) trong môi trường sản xuất.

### **2. Bối cảnh & Vấn đề**
Trong hệ thống Ticketbox, việc quản lý hạn ngạch vé theo từng khu vực (VIP, Zone A, Standard), tính toán giá tiền sau chiết khấu và kiểm soát lượt quét mã QR check-in tại cổng ra vào gặp phải nhiều sự cố nghiêm trọng do mã nguồn cũ lạm dụng biến toàn cục (`var` global). 

Một số sự cố thực tế ghi nhận được:
1.  **Đè dữ liệu biến toàn cục:** Số lượng vé đã bán của khu vực VIP bị ghi đè khi khu vực Standard tiến hành thanh toán, do dùng chung biến đếm ở Global Scope.
2.  **Sai lệch chiết khấu do toán tử `||`:** Khi chương trình khuyến mãi Early Bird thiết lập mức giảm giá `0%` (không giảm), hàm tính tiền cũ dùng toán tử `discountRate || 0.15` đã tự động biến `0%` thành `15%`, gây thất thoát doanh thu cho ban tổ chức.
3.  **Lộ dữ liệu nhạy cảm:** Trạng thái mã QR check-in của khách hàng bị thay đổi trực tiếp từ bên ngoài console trình duyệt, dẫn đến tình trạng gian lận vé vào cửa.

Bạn được giao nhiệm vụ tái thiết kế lại module quản lý vé sự kiện này bằng cách đóng gói toàn bộ trạng thái vào các hàm khép kín (Closure), sử dụng Arrow Function và Tham số mặc định để đảm bảo hệ thống hoạt động chính xác, an toàn và dễ mở rộng.

### **3. Quy tắc nghiệp vụ**
Hệ thống quản lý vé cho một đêm diễn nhạc hội cần tuân thủ các quy tắc cốt lõi sau:
*   **Giới hạn số lượng mua:** Mỗi giao dịch của một tài khoản chỉ được phép đặt tối đa 4 vé.
*   **Chiết khấu & Thuế:** Giá vé mặc định phải tính toán kèm thuế VAT (mặc định `8%` nếu không truyền) và mức chiết khấu Early Bird (mặc định `15%` cho vé mở bán sớm, hoặc `0%` nếu là vé thường).
*   **Bảo mật trạng thái check-in:** Mỗi khu vực vé phải có một bộ quản lý độc lập (Ticket Zone Manager) được tạo ra từ một Closure. Bộ quản lý này giữ private danh sách mã vé/QR đã phát hành và lượt check-in. Bên ngoài không thể can thiệp trực tiếp biến đếm hay mảng lưu mã vé ngoài việc thông qua các phương thức do Closure trả về.
*   **Kiểm tra check-in 1 lần:** Mã QR chỉ có hiệu lực quét đúng 1 lần duy nhất. Nếu quét lại mã đã dùng, hệ thống phải từ chối và cảnh báo lỗi.

### **4. Yêu cầu bài toán**

[REQUIREMENT] Học viên không được nhận sẵn khung mã nguồn hay dữ liệu mẫu. Học viên phải tự chủ động thực hiện 4 phần nhiệm vụ sau:

#### **Phần 1: Tự thiết kế I/O Schema & Kịch bản bẫy lỗi (Edge Cases)**
*   Định nghĩa chi tiết cấu trúc dữ liệu đầu vào (Input) và đầu ra (Output) cho các hàm quản lý vé và check-in dưới dạng JSON hoặc Object Schema.
*   Liệt kê tối thiểu 3 kịch bản bẫy lỗi biên nghiệp vụ (Ví dụ: Đặt quá 4 vé trong 1 giao dịch, truyền thuế VAT = 0%, quét check-in mã không tồn tại hoặc quét trùng 2 lần) và nêu giải pháp xử lý.

#### **Phần 2: Thiết kế Sơ đồ luồng dữ liệu (Mermaid Data Flow)**
Vẽ sơ đồ quy trình xử lý đặt vé và quét check-in bằng cú pháp Mermaid. Sơ đồ phải tuân thủ nghiêm ngặt chuẩn hình dạng:
*   Bắt đầu/Kết thúc: Hình Oval `([ ... ])`
*   Đầu vào/Đầu ra dữ liệu: Hình Song song `[/ ... /]`
*   Xử lý/Tính toán: Hình Chữ nhật `[" ... "]`
*   Kiểm tra điều kiện: Hình Thoi `Kiểm tra điều kiện?`

#### **Phần 3: Triển khai Mã nguồn JavaScript (ES6+)**
Viết một script hoàn chỉnh chạy trên môi trường Node.js hoặc Browser Console đáp ứng:
1.  **Hàm tính toán tổng tiền đơn hàng:** Sử dụng Arrow Function kết hợp Tham số mặc định (`taxRate = 0.08`, `discountRate = 0.15`) để tính toán tiền vé. Lưu ý xử lý đúng trường hợp `discountRate = 0`.
2.  **Hàm tạo bộ quản lý khu vực vé (`createTicketZoneManager`):** Sử dụng Closure để đóng gói:
    *   Biến cục bộ private: `zoneName`, `basePrice`, `totalQuota`, `soldTickets` (mảng chứa dữ liệu vé đã bán), `checkedInTickets` (danh sách vé đã quét).
    *   Trả về một đối tượng chứa các phương thức (Arrow Functions):
        *   `issueTicket(customerName, quantity, discountRate)`: Đặt vé, kiểm tra hạn ngạch và giới hạn 4 vé/lần.
        *   `checkIn(ticketCode)`: Thực hiện check-in cho mã vé, đánh dấu đã sử dụng và chặn quét trùng.
        *   `getZoneStats()`: Trả về báo cáo tổng quan về số vé còn lại, tổng doanh thu đã thu về mà không làm rò rỉ biến private ra ngoài.
3.  Tạo ít nhất 2 khu vực vé độc lập (ví dụ: `VIP Zone` và `GA Zone`) để chứng minh tính đóng gói và không đè dữ liệu giữa các scope.

#### **Phần 4: Chạy thử nghiệm Kịch bản (Test Cases)**
*   Thực hiện các câu lệnh gọi hàm để minh chứng giải pháp xử lý thành công tất cả các kịch bản thành công và các kịch bản bẫy lỗi đã đề xuất ở Phần 1.
*   Sử dụng `console.log` hiển thị rõ ràng thông báo kết quả thực thi theo định dạng chuẩn sản xuất.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo (I/O Schema, Bẫy lỗi, Sơ đồ Mermaid) và mã nguồn triển khai trong file bài làm.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session14_Ex13`.
    Ví dụ: `HNKS25CNTT1_Core_Session14_Ex13`
