```markmap
# Session 08: Phạm vi biến và scope

## Local Scope (Phạm vi cục bộ)
- Bản chất: Biến khai báo bên trong một khối hàm.
- Vòng đời: Khởi tạo khi hàm bắt đầu thực thi và bị hủy khi hàm kết thúc (`return`).
- Phạm vi truy cập: Chỉ hiển thị bên trong hàm chứa nó, cố gắng gọi từ bên ngoài sẽ gây lỗi `NameError`.
- ![](../images/mindmap_img_1.png)

## Global Scope (Phạm vi toàn cục)
- Bản chất: Biến khai báo ở tầng cao nhất của chương trình (ngoài tất cả các hàm).
- Phạm vi truy cập: Có thể đọc trực tiếp từ bất kỳ vị trí nào trong tệp mã nguồn.
- Code ví dụ:
  ```python
  tax_rate = 0.08
  def calculate_tax(price):
      # Đọc trực tiếp biến global tax_rate
      return price * tax_rate
  ```

## Variable Shadowing (Che khuất biến)
- Nguyên lý LEGB: Thứ tự phân giải scope trong Python là Local -> Enclosing -> Global -> Built-in.
- Khái niệm: Xảy ra khi một biến khai báo trong phạm vi hẹp hơn (Local) trùng tên với biến ở phạm vi rộng hơn (Global).
- Hệ quả: Biến toàn cục tạm thời bị ẩn đi và không bị thay đổi giá trị gốc sau khi hàm thực thi xong.
- Code ví dụ:
  ```python
  x = 10
  def shadow():
      x = 5 # Che khuất global x
      print(f"Local: {x}") # In ra 5
  shadow()
  print(f"Global: {x}") # Vẫn in ra 10
  ```

## Nested Functions (Hàm lồng nhau)
- Cấu trúc: Định nghĩa một hàm (inner function) nằm hoàn toàn bên trong một hàm khác (outer function).
- Enclosing Scope: Phạm vi của hàm cha đối với hàm con (nằm giữa phạm vi cục bộ của hàm con và phạm vi toàn cục).
- Cơ chế truy cập: Hàm con có quyền đọc trực tiếp các biến được khai báo ở hàm cha.
- ![](../images/mindmap_img_2.png)

## global Keyword
- Mục đích: Khai báo với Python rằng một biến trong hàm chính là biến toàn cục (Global).
- Ứng dụng: Dùng khi cần ghi đè hoặc thay đổi giá trị của biến toàn cục ngay bên trong hàm cục bộ.
- Code ví dụ:
  ```python
  global_tax_rate = 0.08
  def update_global_tax(new_rate):
      global global_tax_rate
      global_tax_rate = new_rate
  ```
- Gotcha: Lạm dụng `global` làm mã nguồn khó bảo trì, phá vỡ tính đóng gói của hàm.

## nonlocal Keyword
- Mục đích: Khai báo với Python rằng một biến thuộc phạm vi bao quanh (Enclosing - hàm cha).
- Ứng dụng: Sử dụng trong hàm lồng nhau để sửa đổi biến của hàm cha mà không tạo biến cục bộ mới.
- Code ví dụ:
  ```python
  def outer_fee_calculator(base_price):
      service_charge = 15.0
      def apply_service_fee(price):
          nonlocal service_charge
          service_charge = 20.0
          return price + service_charge
      return apply_service_fee(base_price)
  ```
- Lưu ý: Biến được khai báo nonlocal bắt buộc phải tồn tại trong hàm cha trước đó.

## UnboundLocalError
- Bản chất: Lỗi runtime xảy ra khi truy cập và tính toán với một biến cục bộ trước khi định nghĩa nó.
- Nguyên nhân: Python thấy có câu lệnh gán biến đó trong hàm nên đánh dấu nó là biến Local, nhưng câu lệnh tính toán lại chạy trước câu lệnh gán.
- Code ví dụ gây lỗi:
  ```python
  x = 10
  def increment():
      x = x + 1 # Gây UnboundLocalError: local variable 'x' referenced before assignment
  ```
- Cách khắc phục: Khai báo explicitly bằng từ khóa `global x` nếu muốn thay đổi biến ngoài.

## PEP 8 Scope Variable Convention
- Hằng số toàn cục (Global Constants): Khai báo bằng chữ IN HOA phân cách bằng dấu gạch dưới. Do không đổi giá trị nên không cần dùng từ khóa `global`.
  ```python
  DATABASE_TIMEOUT = 30
  PI = 3.14159
  ```
- Định mức thiết kế: Tránh lạm dụng thay đổi trạng thái toàn cục, ưu tiên truyền tham số đầu vào và nhận giá trị đầu ra qua lệnh `return`.
```
```
```