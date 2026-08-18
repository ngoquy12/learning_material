## <center>BÀI KIỂM TRA ĐẦU GIỜ: QUẢN LÝ VÀ ĐIỀU HƯỚNG QUY TRÌNH TRẠNG THÁI ĐƠN HÀNG CONSOLE (CONSOLE ORDER WORKFLOW NAVIGATOR)</center>

### **1. Mục tiêu**
- Đánh giá khả năng vận dụng cấu trúc dữ liệu Mảng (Array) và Đối tượng (Object Literal) để lưu trữ và quản lý trạng thái đơn hàng.
- Thực hành xây dựng menu điều hướng quy trình bằng câu lệnh rẽ nhánh `switch-case` và vòng lặp `while` trên nền tảng Console.
- Kiểm tra kỹ năng xử lý điều kiện rẽ nhánh `if-else`, toán tử logic `&&`, `||` để kiểm soát sự chuyển đổi trạng thái tác vụ hợp lệ.
- Thao tác duyệt mảng bằng vòng lặp `for...of`, tính toán số liệu thống kê tiến độ và xuất báo cáo chuẩn định dạng Template Literals.

### **2. Yêu cầu**

Hệ thống bán hàng yêu cầu xây dựng một chương trình Console CLI để điều hướng và quản lý trạng thái xử lý của các đơn hàng trong danh mục. Hãy thực hiện các yêu cầu theo bảng chi tiết chức năng bên dưới:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellPadding="8">
  <thead>
    <tr style="background-color: #f2f2f2; text-align: left;">
      <th style="width: 25%;">Tên Chức năng / Thao tác</th>
      <th style="width: 20%;">Đầu vào (Input)</th>
      <th style="width: 35%;">Logic Xử lý & Quy tắc</th>
      <th style="width: 20%;">Đầu ra (Output)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Khởi tạo & Điều hướng Menu Quy trình</b><br><code>navigateWorkflowMenu()</code></td>
      <td>
        - Mảng <code>orders</code> chứa các object đơn hàng.<br>
        - Biến <code>userChoice</code> (nhập từ prompt hoặc console).
      </td>
      <td>
        - Mảng <code>orders</code> khởi tạo sẵn 3 đơn hàng mẫu có cấu trúc: <code>{ orderId, customerName, totalAmount, status }</code> (trạng thái gồm: <code>"Pending"</code>, <code>"Processing"</code>, <code>"Completed"</code>, <code>"Cancelled"</code>).<br>
        - Sử dụng vòng lặp và câu lệnh <code>switch-case</code> để hiển thị menu các thao tác:<br>
          + 1: Xem danh sách đơn hàng<br>
          + 2: Cập nhật trạng thái đơn hàng<br>
          + 3: Thống kê báo cáo tiến độ quy trình<br>
          + 0: Thoát chương trình<br>
        - Xử lý nhánh <code>default</code> khi nhập lựa chọn không hợp lệ.
      </td>
      <td>
        Menu lựa chọn hiển thị rõ ràng trên màn hình Console CLI.
      </td>
    </tr>
    <tr>
      <td><b>Cập nhật Trạng thái Tiến trình Đơn hàng</b><br><code>updateOrderStatus()</code></td>
      <td>
        - <code>targetOrderId</code> (String): Mã đơn hàng cần cập nhật.<br>
        - <code>nextStatusChoice</code> (Number): Lựa chọn trạng thái mới (1: Processing, 2: Completed, 3: Cancelled).
      </td>
      <td>
        - Tìm đơn hàng có <code>orderId === targetOrderId</code> trong mảng <code>orders</code>.<br>
        - Nếu không tìm thấy: Báo lỗi đơn hàng không tồn tại.<br>
        - Kiểm tra logic chuyển đổi trạng thái bằng `if-else`:<br>
          + Không được chuyển đơn hàng đã <code>"Completed"</code> hoặc <code>"Cancelled"</code> sang trạng thái khác.<br>
          + Cập nhật thuộc tính <code>status</code> của đối tượng nếu điều kiện hợp lệ.
      </td>
      <td>
        Thông báo kết quả cập nhật trạng thái thành công/thất bại kèm thông tin đơn hàng sau cập nhật qua Console.
      </td>
    </tr>
    <tr>
      <td><b>Thống kê & Báo cáo Tiến độ Quy trình</b><br><code>reportProcessStatus()</code></td>
      <td>
        - Mảng <code>orders</code> hiện tại.
      </td>
      <td>
        - Duyệt mảng bằng vòng lặp <code>for...of</code>.<br>
        - Khởi tạo các biến đếm số lượng cho từng trạng thái: <code>pendingCount</code>, <code>processingCount</code>, <code>completedCount</code>, <code>cancelledCount</code>.<br>
        - Tính tỷ lệ hoàn thành đơn hàng: <code>completionRate = (completedCount / totalOrders) * 100</code>.<br>
        - Xuất báo cáo tổng quan sử dụng Template Literals.
      </td>
      <td>
        Bảng thống kê số lượng đơn hàng theo từng trạng thái và tỷ lệ hoàn thành (%) hiển thị trên Console.
      </td>
    </tr>
  </tbody>
</table>

---

### **3. Tiêu chí đánh giá**

- **Khởi tạo dữ liệu & Điều hướng Menu (3.0 điểm):**
  - Khai báo đúng cấu trúc mảng đối tượng `orders` với đầy đủ các thuộc tính tiếng Anh chuẩn camelCase. (1.5 điểm)
  - Xây dựng luồng menu tương tác điều hướng bằng `switch-case` chính xác, xử lý trường hợp nhập sai lựa chọn. (1.5 điểm)

- **Xử lý Điều kiện Cập nhật Trạng thái (3.5 điểm):**
  - Đọc và tìm kiếm thành công phần tử đối tượng theo `orderId`. (1.5 điểm)
  - Rẽ nhánh điều kiện `if-else` kiểm tra chính xác các quy tắc chuyển đổi trạng thái đơn hàng (không sửa đơn đã hoàn thành/hủy). (2.0 điểm)

- **Thống kê Tiến độ & Báo cáo Console (2.5 điểm):**
  - Duyệt mảng `orders` đúng cú pháp, đếm chính xác số lượng đơn theo 4 trạng thái. (1.5 điểm)
  - Tính toán tỷ lệ % hoàn thành chính xác và in định dạng báo cáo đẹp mắt với Template Literals. (1.0 điểm)

- **Quy chuẩn Mã nguồn & Đặt tên (1.0 điểm):**
  - Tất cả biến, thuộc tính object, chỉ số đếm đặt tên 100% bằng tiếng Anh có nghĩa (`orderId`, `customerName`, `totalAmount`, `status`, `pendingCount`, v.v.). (1.0 điểm)

---

### **4. Yêu cầu nộp bài**

1. Tạo thư mục bài làm theo cấu trúc: `bai_kiem_tra_01_[ho_va_ten]`.
2. Tạo file mã nguồn JavaScript: `index.js` (hoặc `script.js`).
3. Chạy và kiểm tra kết quả hiển thị trên Console Terminal bằng Node.js Runtime hoặc Browser Console.
4. Đẩy (Push) toàn bộ mã nguồn lên kho lưu trữ GitHub cá nhân và nộp liên kết Repository lên hệ thống quản lý học tập.