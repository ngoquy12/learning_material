# <center>[Tổng hợp Demo] Phân hệ Tổng hợp Nghiệp vụ Tích hợp (EVENT_TICKETING)</center>

### **1. Mục tiêu**
- **Kiến thức**: Tích hợp toàn bộ kiến thức cốt lõi của Session 14 bao gồm Khai báo hàm (Function Declaration/Expression), cú pháp Arrow Function ES6, Tham số mặc định (Default Parameters), quản lý phạm vi biến (Global Scope, Local Scope) và cơ chế đóng gói dữ liệu Closure.
- **Kỹ năng**: Phân tích luồng thực thi của hàm (Call Stack), truy vết phạm vi biến, thiết kế các hàm xử lý tính toán nghiệp vụ độc lập, sử dụng Closure để bảo mật dữ liệu trạng thái và hạn chế tối đa việc ô nhiễm phạm vi toàn cục (Global Scope Pollution).
- **Vai trò**: Hướng dẫn Giảng viên thực hiện Live Coding trực quan hóa luồng chạy thực tế để học viên dễ tiếp thu.

### **2. Bối cảnh & Vấn đề (Dành cho Demo trên lớp)**
Trong phân hệ bán vé của hệ thống quản lý sự kiện trực tuyến **EVENT_TICKETING**, nền tảng cần xử lý các giao dịch đặt vé cho một đêm nhạc. Hệ thống cũ gặp vấn đề nghiêm trọng khi lạm dụng biến toàn cục làm xung đột dữ liệu số lượng vé tồn kho giữa các sự kiện khác nhau, đồng thời logic tính toán tổng chi phí và chiết khấu bị lặp lại nhiều nơi do thiếu tính tái sử dụng của hàm.

Giảng viên sẽ thực hiện Demo Live Coding xây dựng phân hệ quản lý vé đơn giản: chuẩn hóa các hàm tính toán tổng tiền vé, áp dụng mã ưu đãi bằng Arrow Function với tham số mặc định, và bảo vệ số lượng vé tồn kho riêng biệt cho từng sự kiện bằng cơ chế Closure.

### **3. Quy tắc nghiệp vụ & 3 Chức năng cốt lõi cần làm**

- **Hàm 1: Tính toán tổng tiền hóa đơn vé gốc (Function Declaration hoặc Function Expression)**
  - **Nghiệp vụ**: Tính tổng số tiền hóa đơn vé dựa trên giá vé niêm yết, số lượng vé đăng ký, phí dịch vụ hệ thống cố định và tỷ lệ thuế VAT.
  - **Đầu vào (Input)**: Đơn giá vé gốc (`baseTicketPrice`), số lượng vé mua (`ticketQuantity`), phí dịch vụ cố định (`serviceFee`), tỷ lệ thuế VAT (`vatRate`).
  - **Đầu ra (Output)**: Trả về giá trị số tương ứng với tổng tiền hóa đơn trước chiết khấu (đã bao gồm VAT và phí dịch vụ).

- **Hàm 2: Tính số tiền thực trả sau chiết khấu và phụ phí VIP (Arrow Function & Default Parameters)**
  - **Nghiệp vụ**: Sử dụng Arrow Function kết hợp tham số mặc định để tính số tiền vé cuối cùng thanh toán sau khi trừ tỷ lệ chiết khấu (mặc định là 5%) và cộng phụ phí hạng vé VIP (mặc định là 0 VNĐ nếu là vé thường).
  - **Đầu vào (Input)**: Tổng tiền hóa đơn vé gốc (`totalOrderAmount`), tỷ lệ chiết khấu (`discountRate`, mặc định = 0.05), phụ phí hạng vé (`vipSurcharge`, mặc định = 0).
  - **Đầu ra (Output)**: Trả về giá trị số tương ứng với tổng số tiền thanh toán thực tế cuối cùng của đơn hàng.

- **Hàm 3: Khởi tạo bộ quản lý tồn kho vé đóng gói (Scope & Closure)**
  - **Nghiệp vụ**: Tạo một hàm quản lý kho vé riêng biệt, lưu trữ số lượng vé trong Lexical Scope (biến riêng tư) và trả về đối tượng chứa các phương thức thực thi (đặt vé và kiểm tra vé). Điều này ngăn chặn việc sửa đổi biến số lượng vé trực tiếp từ phạm vi toàn cục (Global Scope).
  - **Đầu vào (Input)**: Số lượng vé mở bán ban đầu của sự kiện (`initialTicketStock`, mặc định = 50).
  - **Đầu ra (Output)**: Trả về một đối tượng (Closure) gồm 2 phương thức: phương thức trừ số lượng vé khi đặt thành công (`bookTicket`) và phương thức tra cứu số lượng vé còn lại (`getRemainingTickets`).

### **4. Yêu cầu nộp bài**
Bài tập này là phần thực hành Live Coding trên lớp. Học viên lưu mã nguồn và sơ đồ phân tích vào thư mục: `[Tên Lớp]_[Môn Học]_Session14_Demo`.
Ví dụ: `HNKS25CNTT1_Core_Session14_Demo`
