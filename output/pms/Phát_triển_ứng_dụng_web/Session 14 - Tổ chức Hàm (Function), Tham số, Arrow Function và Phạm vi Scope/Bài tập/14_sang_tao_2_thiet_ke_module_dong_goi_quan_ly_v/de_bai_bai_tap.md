# <center>[Sáng tạo 2] Thiết kế Module Đóng gói Quản lý Vé & Đặt chỗ Concert bằng Closure</center>

### **1. Mục tiêu**
*   **Vận dụng sáng tạo cú pháp ES6+:** Thành thạo việc tổ chức hàm thông qua Arrow Function, Tham số mặc định (Default Parameters), Hàm ẩn danh (Function Expression) và cú pháp trả về đối tượng thu gọn `() => ({ ... })`.
*   **Kỹ thuật đóng gói (Encapsulation) với Closure:** Áp dụng khái niệm Lexical Scope và Closure để cô lập hoàn toàn trạng thái private của hệ thống bán vé (số lượng vé kho, danh sách vé đã cấp, trạng thái check-in) mà không lạm dụng biến toàn cục (Global Variable) hay cú pháp Lớp (Class).
*   **Tư duy thiết kế hệ thống:** Tự phân tích, định nghĩa cấu trúc dữ liệu I/O, chủ động phát hiện các bẫy bối cảnh (Edge Cases) nghiệp vụ bán vé sự kiện và vẽ sơ đồ luồng dữ liệu (Mermaid Flowchart) chuẩn hóa.

### **2. Bối cảnh & Vấn đề**
Trong các đợt mở bán vé concert âm nhạc quy mô lớn trên nền tảng Ticketbox, hệ thống thường gặp phải rủi ro nghiêm trọng liên quan đến việc ghi đè biến toàn cục (Global Scope Pollution) hoặc người dùng can thiệp trực tiếp vào mã nguồn JavaScript trên Console trình duyệt để sửa đổi số lượng vé khả dụng và hạn ngạch mua vé.

Đội ngũ kỹ thuật yêu cầu xây dựng một **Module Quản lý Đặt chỗ & Check-in Vé Concert** độc lập. Module này phải đóng gói toàn bộ dữ liệu nhạy cảm bên trong Lexical Scope của một hàm khởi tạo (Factory Function sử dụng Closure). Dữ liệu này chỉ có thể được truy xuất và cập nhật thông qua các hàm con (Arrow Functions) do Closure cung cấp, đảm bảo tính an toàn dữ liệu tuyệt đối trước khi gửi thông tin lên hệ thống.

### **3. Quy tắc nghiệp vụ**
Hệ thống xử lý vé cần đáp ứng các quy tắc nghiệp vụ thực tế sau:
1.  **Kiểm soát hạn ngạch mua vé (Account Quota):** Mỗi tài khoản khách hàng chỉ được phép đặt mua tối đa **4 vé** cho một sự kiện (nếu cố tình đặt thêm sẽ bị từ chối).
2.  **Tính giá vé & Chiết khấu Early Bird:**
    *   Giá vé phụ thuộc vào từng khu vực (ví dụ: Zone A, VIP, GA).
    *   Vé đặt mua trong đợt **Early Bird** được tự động chiết khấu **15%** trên tổng giá trị tiền vé gốc.
    *   Hệ thống có phí dịch vụ xuất vé mặc định là **20.000 VNĐ / đơn hàng** (sử dụng Tham số mặc định trong hàm, cho phép ghi đè nếu có chương trình ưu đãi phí).
3.  **Quản lý mã QR & Check-in 1 lần:** Mỗi vé bán ra thành công sẽ tạo ra một mã QR check-in duy nhất. Mỗi mã QR chỉ có hiệu lực quét check-in **1 lần duy nhất** vào cổng sự kiện; lần quét thứ 2 trở đi phải trả về cảnh báo mã vé đã được sử dụng.
4.  **Bảo mật dữ liệu (Scope Isolation):** Biến lưu trữ tổng số vé còn lại trong kho và mảng chứa danh sách vé đã phát hành phải nằm trong phạm vi cục bộ (Local Scope) của Closure, tuyệt đối không được lộ ra ngoài phạm vi toàn cục.

### **4. Yêu cầu bài toán**
Bài tập này được thiết kế theo mô hình mở (**Closed How - Open What & Why**). Học viên không được cung cấp mã nguồn mẫu (skeleton code) hay dữ liệu sẵn có, mà phải tự chủ động triển khai toàn bộ giải pháp thông qua 4 phần sản phẩm chi tiết:

#### **Phần 1: Tự thiết kế I/O Schema**
Định nghĩa chi tiết cấu trúc dữ liệu đầu vào (Input) và đầu ra (Output) cho hàm tạo bộ quản lý bán vé và các phương thức con (đặt vé, tính tiền đơn hàng, quét mã QR check-in).

#### **Phần 2: Chủ động phát hiện Bẫy dữ liệu (Edge Cases)**
Liệt kê ít nhất 3 kịch bản bẫy lỗi hoặc xung đột trạng thái nghiệp vụ có thể xảy ra (ví dụ: đặt vé khi kho hết vé, đặt quá hạn ngạch 4 vé/tài khoản, quét QR không tồn tại hoặc quét trùng) và đề xuất phương án xử lý logic cho từng trường hợp.

#### **Phần 3: Sơ đồ luồng dữ liệu (Data Flow Diagram)**
Vẽ sơ đồ Mermaid thể hiện toàn bộ vòng đời của dữ liệu từ khi khởi tạo Closure bộ quản lý, thực thi giao dịch mua vé, tính tiền chiết khấu Early Bird cho đến khi thực hiện quét check-in mã QR tại cổng.
*Lưu ý về quy chuẩn Mermaid:* Tuân thủ nghiêm ngặt 5 dạng hình khối (Terminator `([ ])`, Input/Output `[/ /]`, Decision diamond `?`, Process rectangle `[" "]`, Flowline `-->`).

#### **Phần 4: Triển khai Mã nguồn JavaScript (ES6+)**
Viết chương trình JavaScript hoàn chỉnh đáp ứng:
*   Sử dụng Arrow Function và Tham số mặc định (Default Parameters).
*   Đóng gói biến trạng thái private bằng Closure.
*   Cung cấp các hàm con trả về kết quả (tính tiền, xuất vé, check-in QR, báo cáo doanh thu).
*   Mã nguồn sạch, các biến/hàm đặt tên bằng tiếng Anh chuẩn camelCase, chú thích logic bằng tiếng Việt có dấu.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo (Phần 1, 2, 3) và mã nguồn triển khai (Phần 4).
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session14_Ex14`.
    Ví dụ: `HNKS25CNTT1_Core_Session14_Ex14`
