# <center>BÀI KIỂM TRA ĐẦU GIỜ: QUẢN LÝ TRẠNG THÁI VÀ ĐIỀU HƯỚNG PHIÊN BÁN HÀNG CONSOLE</center>

## <center>(CLI SALES SESSION NAVIGATION & STATE CONTROL)</center>

### **1. Mục tiêu**
- **Kiến thức:** Đánh giá khả năng vận dụng các kiểu dữ liệu cơ bản (`dict`, `str`, `list`), các cấu trúc điều khiển rẽ nhánh (`if-elif-else`), và việc gán nhãn kiểu dữ liệu (`type hints`) trong Python 3.12.
- **Kỹ năng:** Xây dựng luồng điều hướng quy trình và kiểm soát chuyển đổi trạng thái (State Transition Logic) cho ứng dụng bán hàng dạng Console/CLI không sử dụng lập trình hướng đối tượng (OOP).
- **Chuẩn hóa code:** Thực thi viết mã chuẩn PEP 8, xử lý ngoại lệ theo cơ chế native (`ValueError`), đặt tên định danh hoàn toàn bằng Tiếng Anh chuẩn (`camelCase`).

---

### **2. Yêu cầu**

Thực hiện viết một chương trình Python 3.12 để quản lý phiên bán hàng và điều hướng trạng thái đơn hàng trên giao diện Console. 

Chi tiết 3 chức năng core được mô tả trong bảng quy chuẩn dưới đây:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellPadding="8" cellSpacing="0">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="width: 25%; text-align: left;">Tên chức năng / Hàm</th>
      <th style="width: 20%; text-align: left;">Đầu vào / Tham số</th>
      <th style="width: 35%; text-align: left;">Lô-gíc xử lý & Quy tắc</th>
      <th style="width: 20%; text-align: left;">Đầu ra / Giá trị trả về</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>[Khởi tạo phiên bán hàng]</b><br><code>createSalesSession()</code></td>
      <td><code>cashierId: str</code><br><code>sessionCode: str</code></td>
      <td>
        - Kiểm tra nếu <code>cashierId</code> hoặc <code>sessionCode</code> bị rỗng (sau khi cắt khoảng trắng) thì ném ngoại lệ <code>ValueError</code>.<br>
        - Khởi tạo Dictionary đại diện cho phiên làm việc với trạng thái ban đầu là <code>"DRAFT"</code> (Đơn nháp).
      </td>
      <td><code>dict[str, Any]</code> chứa các khóa:<br><code>sessionCode</code>, <code>cashierId</code>, <code>currentState</code>.</td>
    </tr>
    <tr>
      <td><b>[Cập nhật trạng thái đơn hàng]</b><br><code>updateOrderState()</code></td>
      <td><code>sessionData: dict[str, Any]</code><br><code>nextState: str</code></td>
      <td>
        - Kiểm tra quy tắc chuyển dịch trạng thái hợp lệ:<br>
        &nbsp;&nbsp;+ Từ <code>"DRAFT"</code> chỉ được chuyển sang <code>"PENDING_PAYMENT"</code> hoặc <code>"CANCELLED"</code>.<br>
        &nbsp;&nbsp;+ Từ <code>"PENDING_PAYMENT"</code> chỉ được chuyển sang <code>"COMPLETED"</code> hoặc <code>"CANCELLED"</code>.<br>
        &nbsp;&nbsp;+ Nếu trạng thái hiện tại là <code>"COMPLETED"</code> hoặc <code>"CANCELLED"</code>, đây là trạng thái kết thúc (Terminal State), không thể chuyển đi đâu thêm.<br>
        - Nếu chuyển đổi không hợp lệ, ném ngoại lệ <code>ValueError</code> kèm thông báo lỗi cụ thể.<br>
        - Nếu hợp lệ, cập nhật lại <code>currentState</code> trong <code>sessionData</code>.
      </td>
      <td><code>bool</code> (Trả về <code>True</code> nếu chuyển trạng thái thành công).</td>
    </tr>
    <tr>
      <td><b>[Hiển thị menu điều hướng tác vụ]</b><br><code>displaySessionNavigation()</code></td>
      <td><code>sessionData: dict[str, Any]</code></td>
      <td>
        - Dựa vào <code>currentState</code> trong <code>sessionData</code>, in ra màn hình Console danh sách các thao tác hợp lệ tiếp theo mà thu ngân có thể chọn.<br>
        - Ví dụ:<br>
        &nbsp;&nbsp;+ Nếu là <code>"DRAFT"</code>: In ra gợi ý chuyển sang <code>PENDING_PAYMENT</code> hoặc <code>CANCELLED</code>.<br>
        &nbsp;&nbsp;+ Nếu là <code>"COMPLETED"</code>/<code>"CANCELLED"</code>: In thông báo <i>"Phiên giao dịch đã kết thúc"</i>.
      </td>
      <td><code>None</code> (In trực tiếp ra màn hình Console).</td>
    </tr>
  </tbody>
</table>

---

### **3. Tiêu chí đánh giá**

- **Khởi tạo và Type Hints (2.5 điểm):** Hàm `createSalesSession()` khởi tạo đúng Dictionary, kiểm tra hợp lệ dữ liệu vào và gán đầy đủ Type Hints cho tham số và kiểu trả về.
- **Lô-gíc chuyển đổi trạng thái (3.5 điểm):** Hàm `updateOrderState()` kiểm soát chính xác các điều kiện chuyển trạng thái, bắt được các trường hợp vi phạm và ném `ValueError` phù hợp.
- **Điều hướng giao diện Console (2.0 điểm):** Hàm `displaySessionNavigation()` hiển thị đúng lựa chọn thao tác tương ứng với từng trạng thái của hệ thống.
- **Chuẩn mã nguồn PEP 8 & Naming (2.0 điểm):** Đặt tên hàm/biến bằng Tiếng Anh chuẩn `camelCase` (VD: `sessionData`, `nextState`), không sử dụng OOP/Class, mã nguồn rõ ràng, dễ đọc.

---

### **4. Yêu cầu nộp bài**

1. Tạo tập tin mã nguồn Python có tên: `sales_navigation.py`.
2. Kiểm thử trực tiếp 3 hàm đã viết bằng cách mô phỏng 1 luồng giao dịch hoàn chỉnh từ khởi tạo `DRAFT` -> `PENDING_PAYMENT` -> `COMPLETED`.
3. Lưu tập tin vào thư mục bài tập của buổi học và tiến hành `commit`, `push` mã nguồn lên repository GitHub cá nhân trước thời gian hết giờ quy định.
