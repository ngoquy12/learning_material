## <center>BÀI KIỂM TRA ĐẦU GIỜ: XỬ LÝ GIAO DỊCH VÀ TÍNH TOÁN HÓA ĐƠN BÁN HÀNG (TRANSACTION & BILLING PROCESSING)</center>

### **1. Mục tiêu**
- Đánh giá khả năng thao tác dữ liệu cấu trúc phức hợp (`list`, `dict`) trong Python 3.12 để xử lý luồng giao dịch bán lẻ.
- Kiểm tra việc áp dụng Type Hints chuẩn xác và tuân thủ quy chuẩn PEP 8.
- Xử lý các ràng buộc nghiệp vụ (kiểm tra tồn kho, áp dụng mã giảm giá, tính tổng tiền hóa đơn và cập nhật kho) trong ứng dụng Console mà không sử dụng Lập trình hướng đối tượng (OOP) hay Cơ sở dữ liệu SQL.

### **2. Yêu cầu**

Hệ thống quản lý bán hàng lưu trữ thông tin sản phẩm và giỏ hàng dưới dạng các cấu trúc dữ liệu nguyên bản (Dictionary và List):
- Cấu trúc kho hàng `inventory`: `dict[str, dict[str, Any]]` (Ví dụ: `{"PROD01": {"itemName": "Tai nghe Bluetooth", "price": 500000.0, "stock": 15}}`).
- Cấu trúc giỏ hàng `cart`: `list[dict[str, Any]]` (Ví dụ: `[{"productId": "PROD01", "quantity": 2}]`).

Thực hiện xây dựng các hàm chức năng xử lý giao dịch theo bảng mô tả chi tiết dưới đây:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellSpacing="0" cellPadding="8">
  <thead>
    <tr style="background-color: #f2f2f2; text-align: left;">
      <th style="width: 25%;">Tên chức năng / Hàm</th>
      <th style="width: 25%;">Đầu vào (Parameters)</th>
      <th style="width: 30%;">Logic xử lý & Quy tắc nghiệp vụ</th>
      <th style="width: 20%;">Đầu ra (Output)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Thêm sản phẩm vào giỏ hàng</b><br><code>addItemToCart()</code></td>
      <td>
        - <code>inventory</code>: <code>dict[str, dict[str, Any]]</code><br>
        - <code>cart</code>: <code>list[dict[str, Any]]</code><br>
        - <code>productId</code>: <code>str</code><br>
        - <code>quantity</code>: <code>int</code>
      </td>
      <td>
        1. Kiểm tra <code>productId</code> có tồn tại trong <code>inventory</code> hay không.<br>
        2. Kiểm tra <code>quantity</code> phải > 0 và nhỏ hơn hoặc bằng số lượng tồn kho (<code>stock</code>).<br>
        3. Nếu sản phẩm đã có trong <code>cart</code>, cộng dồn <code>quantity</code>. Nếu chưa có, thêm phần tử mới vào <code>cart</code>.<br>
        4. Trả về <code>False</code> nếu thông tin không hợp lệ hoặc thiếu hàng trong kho.
      </td>
      <td><code>bool</code> (Trả về <code>True</code> nếu thêm thành công, ngược lại <code>False</code>)</td>
    </tr>
    <tr>
      <td><b>Xử lý thanh toán giao dịch</b><br><code>processTransaction()</code></td>
      <td>
        - <code>inventory</code>: <code>dict[str, dict[str, Any]]</code><br>
        - <code>cart</code>: <code>list[dict[str, Any]]</code><br>
        - <code>discountCode</code>: <code>str</code>
      </td>
      <td>
        1. Nếu <code>cart</code> rỗng, nảy ra ngoại lệ <code>ValueError("Giỏ hàng đang rỗng")</code>.<br>
        2. Tính tổng tiền hàng chưa giảm giá (<code>subtotal</code>).<br>
        3. Tính số tiền giảm (<code>discountAmount</code>) dựa trên <code>discountCode</code>:<br>
           - <code>"VIP10"</code>: Giảm 10% tổng tiền.<br>
           - <code>"SALE5"</code>: Giảm 5% tổng tiền.<br>
           - Mã khác hoặc rỗng: Giảm 0%.<br>
        4. Cập nhật trừ số lượng tồn kho (<code>stock</code>) tương ứng trong <code>inventory</code>.<br>
        5. Trả về tổng quan hóa đơn và xóa sạch sản phẩm trong <code>cart</code>.
      </td>
      <td>
        <code>dict[str, float]</code><br>
        Ví dụ dạng:<br>
        <code>{"subtotal": 1000000.0, "discountAmount": 100000.0, "finalTotal": 900000.0}</code>
      </td>
    </tr>
  </tbody>
</table>

### **3. Tiêu chí đánh giá**

- **Logic nghiệp vụ & Tính đúng đắn (4.0 điểm):**
  - Xử lý chính xác việc kiểm tra tồn kho và cộng dồn sản phẩm trùng trong giỏ hàng.
  - Tính toán đúng tổng tiền, tiền giảm giá và trừ tồn kho chính xác sau khi hoàn tất giao dịch.
- **Áp dụng Type Hints & Chuẩn PEP 8 (3.0 điểm):**
  - Khai báo đầy đủ Type Hints cho toàn bộ hàm và biến theo chuẩn Python 3.12.
  - Đặt tên hàm và biến đúng quy chuẩn camelCase, mã hóa bằng Tiếng Anh 100%.
- **Bắt lỗi & Quản lý ngoại lệ (2.0 điểm):**
  - Xử lý các trường hợp giỏ hàng rỗng, mã giảm giá không hợp lệ, hoặc số lượng mua vượt quá số lượng kho bán.
- **Cấu trúc mã nguồn & Đúng hạn (1.0 điểm):**
  - Mã nguồn trình bày sạch sẽ, mô-đun hóa tốt và hoàn thành trong thời gian 15-20 phút.

### **4. Yêu cầu nộp bài**

- Học viên khởi tạo file `main.py` trong môi trường ảo `virtualenv` trên IDE (Cursor / Windsurf).
- Tiến hành thực thi các hàm trên dữ liệu thử nghiệm và in kết quả ra màn hình Console.
- Thực hiện commit và push mã nguồn lên Git repository theo quy định.