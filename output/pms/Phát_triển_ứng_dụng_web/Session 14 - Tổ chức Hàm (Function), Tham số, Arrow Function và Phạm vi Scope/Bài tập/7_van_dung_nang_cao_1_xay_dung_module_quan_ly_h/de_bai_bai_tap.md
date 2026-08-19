# <center>[Vận dụng nâng cao 1] Xây dựng Module Quản lý Hạn ngạch và Chiết khấu Vé Concert</center>

### **1. Mục tiêu**
*   **Ứng dụng Kỹ thuật Closure:** Đóng gói trạng thái hạn ngạch vé mua của từng tài khoản khách hàng một cách độc lập trong bộ nhớ RAM (Lexical Scope), ngăn chặn việc truy cập hoặc sửa đổi trái phép từ môi trường Global Scope.
*   **Thành thạo Arrow Function & Tham số mặc định (Default Parameters):** Xây dựng các hàm tính toán giá vé theo khu vực (Zone) và áp dụng chính sách ưu đãi đặt sớm (Early Bird) với cú pháp ES6+ tối ưu.
*   **Tư duy Xử lý Biên & Ràng buộc Nghiệp vụ:** Triển khai cơ chế kiểm tra điều kiện biên khắt khe, chủ động ngăn chặn các giao dịch vi phạm quy định mua vé của hệ thống.

### **2. Bối cảnh & Vấn đề**
Trong các sự kiện âm nhạc quy mô lớn trên hệ thống Ticketbox, ban tổ chức luôn đặt ra quy định khắt khe về hạn ngạch mua vé đối với mỗi tài khoản để tránh hiện tượng đầu cơ (phe vé). Mỗi khách hàng chỉ được phép mua tối đa một số lượng vé nhất định cho toàn bộ đợt mở bán.

Tuy nhiên, ở phiên bản thử nghiệm ban đầu, đội ngũ phát triển đã sử dụng các biến toàn cục (Global Variable) để theo dõi số vé khách hàng đã mua. Điều này dẫn đến sự cố nghiêm trọng: dữ liệu giữa các khách hàng bị ghi đè lên nhau, và khách hàng có thể dùng Console trình duyệt để sửa biến toàn cục nhằm mua vượt hạn ngạch.

Hệ thống Ticketbox cần bạn nâng cấp module quản lý mua vé. Yêu cầu đặt ra là phải cô lập dữ liệu mua vé của từng khách hàng vào một phạm vi an toàn (Scope Isolation), đồng thời hỗ trợ linh hoạt việc tính toán tổng tiền vé dựa trên từng khu vực khán đài và chương trình giảm giá Early Bird.

### **3. Quy tắc nghiệp vụ**
Hệ thống tính toán vé và quản lý hạn ngạch vận hành dựa trên các quy tắc sau:

1.  **Bảng quy đổi giá vé theo Khu vực (Zone):**

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellpadding="8">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th>Mã Khu vực (Zone Type)</th>
      <th>Hệ số Giá (Zone Multiplier)</th>
      <th>Mô tả Chi tiết</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>VIP</code></td>
      <td>1.8</td>
      <td>Khu vực sát sân khấu, bao gồm quà tặng kèm</td>
    </tr>
    <tr>
      <td><code>ZONE_A</code></td>
      <td>1.4</td>
      <td>Khu vực khán đài chính, tầm nhìn trực diện</td>
    </tr>
    <tr>
      <td><code>GA</code></td>
      <td>1.0</td>
      <td>Khu vực đứng phổ thông (Giá trị mặc định)</td>
    </tr>
  </tbody>
</table>

2.  **Công thức Tính tiền vé:**
    *   Giá vé gốc một vé sau khi nhân hệ số Zone: `pricePerTicket = basePrice * zoneMultiplier`.
    *   Tổng tiền chưa giảm giá: `subtotal = pricePerTicket * ticketQuantity`.
    *   Ưu đãi Early Bird: Nếu khách hàng mua trong đợt Early Bird (`isEarlyBird = true`), tổng tiền được giảm 15% (tương đương thanh toán 85% của `subtotal`). Nếu `isEarlyBird = false`, không áp dụng giảm giá.

3.  **Quy định Hạn ngạch & Ràng buộc Mua vé (Quota Enforcement):**
    *   Hạn ngạch mua vé mặc định cho mỗi tài khoản là 4 vé (tham số mặc định `maxQuota = 4`).
    *   Số lượng vé mua trong mỗi đơn hàng (`ticketQuantity`) phải là số nguyên hợp lệ lớn hơn 0 và không quá 4.
    *   Hệ thống phải lưu vết số vé tích lũy đã mua thành công của tài khoản (`accumulatedTickets`).
    *   Nếu đơn hàng mới khiến tổng số vé tích lũy vượt quá hạn ngạch cho phép (`accumulatedTickets + ticketQuantity > maxQuota`), hệ thống phải từ chối giao dịch, giữ nguyên số vé tích lũy cũ và báo lỗi rõ ràng.

### **4. Yêu cầu bài toán**

#### **Phần 1: Báo cáo Phân tích & Thiết kế (Bắt buộc)**
Trước khi viết mã nguồn, học viên phải hoàn thành báo cáo phân tích gồm:
1.  **Phân tích Đầu vào / Đầu ra (I/O Analysis):** Liệt kê danh sách các hàm, các tham số đầu vào (kèm kiểu dữ liệu, giá trị mặc định), và kết quả trả về (Output format/Object) của từng hàm.
2.  **Đề xuất Giải pháp Kỹ thuật:** Giải thích chi tiết cơ chế Closure sẽ giúp bảo vệ biến `accumulatedTickets` như thế nào để môi trường bên ngoài không thể can thiệp trực tiếp.
3.  **Lập Sơ đồ luồng (Flowchart / Pseudocode):** Mô tả trình tự kiểm tra điều kiện (từ validate đầu vào, kiểm tra hạn ngạch closure, tính toán chiết khấu, đến cập nhật state và trả kết quả).

#### **Phần 2: Triển khai Mã nguồn JavaScript (Implementation)**
1.  Viết hàm khởi tạo bộ quản lý bán vé sử dụng Closure (ví dụ tên hàm: `createTicketManager`). Hàm này nhận vào tên khách hàng và hạn ngạch tối đa (mặc định là 4).
2.  Bên trong Closure, trả về một đối tượng chứa các phương thức thực thi (được viết bằng Arrow Function):
    *   Phương thức mua vé nhận các tham số: `ticketQuantity`, `basePrice`, `zoneType` (mặc định `'GA'`), `isEarlyBird` (mặc định `false`).
    *   Phương thức lấy thông tin trạng thái hạn ngạch hiện tại của tài khoản.
3.  Xử lý triệt để các trường hợp vi phạm dữ liệu: truyền số lượng vé âm, sai kiểu dữ liệu, vượt hạn ngạch, hoặc truyền mã Zone không tồn tại (nếu mã Zone không hợp lệ, mặc định dùng hệ số 1.0).
4.  Tạo ít nhất 2 đối tượng quản lý tài khoản khách hàng khác nhau để chứng minh tính độc lập về bộ nhớ RAM (Lexical Scope) của từng Closure. Thực thi các kịch bản: mua vé thành công với tham số mặc định, mua vé Early Bird hạng VIP, và mua vượt quá hạn ngạch.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session14_Ex7`.
    Ví dụ: `HNKS25CNTT1_Core_Session14_Ex7`
