```markmap
---
markmap:
  colorFreezeLevel: 3
---
# Session 01 - Giới thiệu Python va Thiết lập môi trường

## 



### Python_Core_Characteristics

- Lịch sử phát triển
  - Guido van Rossum sáng lập năm 1991
  - Tập trung tối đa vào tốc độ viết mã nguồn và sự trong sáng của cú pháp
- Đặc tính chuyên môn
  - Ngôn ngữ thông dịch (Interpreted Language) chuyển mã nguồn thành Bytecode và thực thi bằng Python Virtual Machine (PVM)
  - Quy tắc đặt tên biến: Tiếng Anh dạng snake_case
  - Thư viện mặc định đa dạng, hạn chế phụ thuộc bên thứ ba
  - ![](../images/mindmap_img_1.png)

### Virtual_Environment

- Bản chất
  - Môi trường ảo cô lập tài nguyên cho từng dự án độc lập, tránh xung đột phiên bản thư viện
- Công cụ sử dụng
  - Thư viện tích hợp sẵn `venv` để khởi tạo không gian làm việc sạch
- Lệnh thực thi cơ bản
  - Khởi tạo môi trường ảo: `python -m venv .venv`
  - Kích hoạt (Windows): `.venv\Scripts\activate`
  - Kích hoạt (macOS/Linux): `source .venv/bin/activate`

### Terminal_and_CLI_Execution

- Cơ chế vận hành
  - Sử dụng Terminal/Command Line Interface (CLI) để gọi trình thông dịch Python chạy file mã nguồn
- Mã nguồn mẫu: `first_python_program`
  
  ```python
  course_name = "Python Core Essentials"
  total_lessons = 12
  print(course_name)
  print(total_lessons)
  ```
- Lệnh thực thi
  - Thực thi chương trình từ Terminal: `python program_greeting.py`

### Syntax_Error

- Phân loại lỗi thường gặp
  - IndentationError: Lỗi thụt dòng sai nguyên tắc (Python dùng thụt dòng thay cho cặp ngoặc nhọn để phân cấp khối lệnh)
  - SyntaxError: Lỗi cấu trúc cú pháp cơ bản (thiếu dấu ngoặc, thiếu nháy bao chuỗi, sai từ khóa)
  - NameError: Gọi biến hoặc hàm chưa được định nghĩa trước đó
- Ví dụ và cách khắc phục: `fix_syntax_errors`
  
  ```python
  # Loi SyntaxError do thieu dau nhay dong
  # message = "Chao ban
  message = "Chao ban" # Sua dung
  
  # Loi IndentationError do thut le sai cap
  #  print(message)
  print(message) # Sua dung
  ```

## 



### Python Interpreter

* Bản chất: Trình thông dịch dịch mã nguồn Python từng dòng thành Bytecode và thực thi trên Python Virtual Machine (PVM)
* ![](../images/mindmap_img_1.png)
* Sự cố thường gặp: Lỗi CommandNotFoundException (hoặc python is not recognized)
  * Nguyên nhân: Chưa cấu hình biến môi trường PATH khi cài đặt Python gốc
  * Giải pháp: Tích chọn "Add Python to PATH" trong quá trình cài đặt (Setup Wizard)

### VS Code (Visual Studio Code)

* Bản chất: Trình soạn thảo mã nguồn gọn nhẹ (Source Code Editor) hỗ trợ lập trình đa ngôn ngữ qua hệ thống Extensions
* Thiết lập cốt lõi: Cài đặt Extension Python phát triển bởi Microsoft để kích hoạt IntelliSense, Linting và kiểm thử
* Cơ chế vận hành: Yêu cầu định cấu hình chỉ định chính xác đường dẫn trình thông dịch (Select Interpreter Path)
* Sự cố thường gặp: Lỗi InterpreterMismatchError
  * Biểu hiện: VS Code tự động chọn sai bộ dịch mặc định làm phát sinh lỗi môi trường hoặc thư viện
  * Giải pháp: Sử dụng tổ hợp phím Ctrl + Shift + P (hoặc Cmd + Shift + P) gõ "Python: Select Interpreter" để chọn đúng môi trường ảo

### Global Environment

* Khái niệm: Môi trường hệ thống dùng chung mặc định được thiết lập ngay sau khi cài đặt Python vào hệ điều hành
* Hạn chế: Xảy ra xung đột phụ thuộc (Dependency Conflict) khi các dự án độc lập đòi hỏi các phiên bản thư viện khác nhau chạy song song
* Cơ chế phân bổ: Thư viện cài đặt ngoài thông qua câu lệnh pip sẽ lưu trữ trực tiếp vào thư mục dùng chung site-packages của hệ thống

### Virtual Environment

* Phân loại giải pháp chính cô lập môi trường
  * venv: Công cụ tích hợp sẵn trong thư viện tiêu chuẩn của Python, nhẹ và tối ưu cho từng dự án riêng lẻ
  * Anaconda: Nền tảng quản lý gói phân phối lớn phù hợp cho Khoa học dữ liệu, quản lý đa phiên bản Python độc lập qua Conda
* ![](../images/mindmap_img_2.png)
* Cú pháp thiết lập nhanh (venv)
  * Khởi tạo: `python -m venv venv_name`
  * Kích hoạt trên Windows: `.\venv_name\Scripts\activate`
  * Kích hoạt trên macOS/Linux: `source venv_name/bin/activate`
* Sự cố thường gặp: Lỗi ModuleNotFoundError
  * Nguyên nhân: Thư viện được cài đặt ở môi trường Global nhưng file code được thực thi bằng Python Interpreter của Virtual Environment hoặc ngược lại

### Terminal/Command Line Interface (CLI)

* Khái niệm: Giao diện dòng lệnh giúp tương tác trực tiếp với hệ điều hành, quản lý gói phụ thuộc và thực thi mã nguồn
* Mã nguồn kiểm thử môi trường (PEP 8 Standard)
  
  ```python
  import sys
  
  def print_greeting():
      """Return a simple greeting string."""
      return "Xin chao Python!"
  
  def calculate_sum(first_number, second_number):
      """Return the sum of two integer arguments."""
      return first_number + second_number
  
  if __name__ == "__main__":
      print(print_greeting())
      print("Result:", calculate_sum(5, 10))
      print("Interpreter Path:", sys.executable)
  ```
* Thử nghiệm thực thi qua CLI
  * Điều hướng thư mục hiện hành: `cd path/to/project_folder`
  * Chạy kiểm thử: `python main.py`

## 



### Biến (Variable)

- Bản chất kỹ thuật
  - Là nhãn tham chiếu (Reference label) liên kết với một đối tượng (Object) trong bộ nhớ RAM
  - Không phải vùng chứa tĩnh, chỉ lưu trữ địa chỉ của đối tượng đang trỏ tới
  - ![](../images/mindmap_img_1.png)
- Hành vi xử lý
  - Có thể thay đổi đối tượng tham chiếu linh hoạt nhờ cơ chế Dynamic Typing của Python

### Phép gán (=)

- Cơ chế hoạt động
  - Đánh giá biểu thức ở vế phải (Right-hand side) trước, sau đó gán tham chiếu cho biến ở vế trái (Left-hand side)
- Cú pháp thực thi
  - Gán giá trị đơn: `variable_name = value`
  - Giải nén Tuple (tuple unpacking): `var1, var2 = val1, val2`
  - Ví dụ thực tế:
    
    ```python
    product_price = 25000
    shop_name, rating = "TechStore", 4.8
    total_price = product_price * 4
    ```

### Quy tắc đặt tên biến

- Ký tự hợp lệ
  - Chỉ gồm chữ cái (a-z, A-Z), chữ số (0-9) và dấu gạch dưới (_)
- Quy tắc bắt đầu
  - Phải bắt đầu bằng chữ cái hoặc dấu gạch dưới (_), cấm bắt đầu bằng chữ số
- Nhạy cảm hoa thường
  - Phân biệt chữ hoa và chữ thường (Case-sensitive)
- Từ khóa hệ thống (Keywords)
  - Không được trùng với các từ khóa dành riêng của Python như `if`, `class`, `import`

### Chuẩn PEP 8 (snake_case)

- Quy chuẩn định dạng
  - Viết thường toàn bộ ký tự tên biến
  - Ngăn cách các từ bằng dấu gạch dưới (_) để dễ đọc
  - Ví dụ chuẩn: `original_price`, `total_price`
- Trực quan nghiệp vụ
  - Đặt tên mang ý nghĩa mô tả rõ ràng dữ liệu thực tế thay vì ký tự vô nghĩa như `x`, `y`, `z`

### Lỗi Cú pháp (SyntaxError)

- Cơ chế kích hoạt
  - Xảy ra khi trình biên dịch/thông dịch quét mã nguồn và phát hiện tên biến vi phạm quy tắc đặt tên
  - Ngăn chương trình khởi chạy ngay lập tức
- Các trường hợp vi phạm điển hình
  - Bắt đầu bằng chữ số: `1st_place = 10`
  - Chứa ký tự cấm: `user-name = "Admin"` hoặc `user$email = "admin@rikkei.edu.vn"`

### Lỗi Định danh (NameError)

- Cơ chế kích hoạt
  - Xảy ra tại thời điểm chạy (Runtime) khi chương trình gọi một định danh chưa được gán giá trị hoặc giải phóng bộ nhớ
- Các nguyên nhân phổ biến
  - Sử dụng biến trước khi khai báo và khởi tạo
  - Sai chính tả ký tự hoa/thường của biến đã khai báo trước đó
  - Ví dụ thực tế:
    
    ```python
    # Gọi print biến khi chưa khai báo
    print(customer_name) # Kích hoạt NameError: name 'customer_name' is not defined
    ```

## 



### Biến (Variable)

- Bản chất & Quy định đặt tên
  - Là nhãn đại diện cho phân vùng bộ nhớ lưu trữ giá trị
  - Đặt tên theo chuẩn CamelCase hoặc Snake Case (Khuyên dùng `snake_case` trong Python)
  - CẤM: Bắt đầu bằng số, chứa ký tự đặc biệt (trừ `_`), trùng từ khóa hệ thống (`int`, `str`, `import`...)
- Khai báo & Gán giá trị
  
  ```python
  product_name = "Mechanical Keyboard"
  quantity = 3
  ```
- Cấu trúc bộ nhớ của biến
  - ![](../images/mindmap_img_1.png)

### Kiểu dữ liệu Số (int, float)

- Số nguyên (int)
  - Lưu các số nguyên dương, âm hoặc bằng không (Ví dụ: -5, 0, 100)
  - Không giới hạn độ lớn lưu trữ trong Python 3
- Số thực (float)
  - Lưu số có phần thập phân hoặc biểu diễn dưới dạng số mũ khoa học (Ví dụ: 3.14, -0.05, 1e-3)
- Kiểm tra kiểu dữ liệu
  - Sử dụng hàm `type()` để xác định kiểu của đối tượng dữ liệu tại runtime
  ```python
  quantity = 3
  unit_price = 45.5
  print(type(quantity))  # <class 'int'>
  print(type(unit_price)) # <class 'float'>
  ```

### Phép toán số học cơ bản

- Toán tử toán học
  - Cộng `+`, Trừ `-`, Nhân `*`
  - Chia lấy giá trị thực `/` (Kết quả luôn là float)
  - Chia lấy nguyên `//`, Chia lấy dư `%`, Lũy thừa `**`
- Độ ưu tiên thực thi
  - Thứ tự: Ngoặc đơn `()` -> Lũy thừa `**` -> Nhân/Chia `*`, `/`, `//`, `%` -> Cộng/Trừ `+`, `-`
  ```python
  result = (10 + 5) * 2 / 2**2
  print(result) # 7.5 (float)
  ```

### Kiểu dữ liệu Chuỗi (str)

- Bản chất
  - Biểu diễn một chuỗi ký tự Unicode
  - Đặt trong cặp dấu nháy đơn `'...'` hoặc nháy kép `"..."`
- Hàm đo độ dài chuỗi
  - Sử dụng hàm `len()` để đếm số lượng ký tự trong chuỗi (gồm cả khoảng trắng)
  ```python
  brand = "Rikkei Education"
  print(len(brand)) # 16
  ```

### Ghép chuỗi và xử lý cơ bản

- Phép ghép chuỗi
  - Sử dụng toán tử `+` để nối hai hoặc nhiều chuỗi lại với nhau
- Lỗi phân giải kiểu (TypeError)
  - Cố gắng thực hiện phép toán cộng giữa `str` và `int`/`float` trực tiếp sẽ gây lỗi hệ thống
- Khắc phục lỗi TypeError
  
  ```python
  price = 45.5
  # Lỗi: message = "Price: " + price
  message = "Price: " + str(price) # Giải pháp ép kiểu trước khi cộng
  print(message)
  ```

### Kiểu dữ liệu Luận lý (bool)

- Giá trị định nghĩa
  - Có đúng hai giá trị luận lý: `True` và `False`
- Gotchas (Lỗi thường gặp)
  - Viết thường chữ cái đầu `true` hoặc `false` sẽ kích hoạt lỗi `NameError` (do hệ thống hiểu lầm là biến chưa khai báo)
  ```python
  is_available = True
  # is_completed = false -> Lỗi NameError
  ```

### Phép toán so sánh

- Các toán tử so sánh
  - So sánh bằng `==`, So sánh khác `!=`
  - So sánh lớn hơn `>`, nhỏ hơn `<`, lớn hơn hoặc bằng `>=`, nhỏ hơn hoặc bằng `<=`
- Cơ chế trả về
  - Kết quả của mọi phép so sánh luôn là một giá trị kiểu `bool` (`True` hoặc `False`)
  ```python
  stock = 10
  order = 12
  is_valid = stock >= order
  print(is_valid) # False
  ```

### Biểu thức logic

- Các toán tử logic
  - Phép và `and`: Chỉ trả về `True` nếu cả hai vế đều `True`
  - Phép hoặc `or`: Trả về `True` nếu ít nhất một vế mang giá trị `True`
  - Phép phủ định `not`: Nghịch đảo giá trị logic hiện tại
  - ![](../images/mindmap_img_2.png)
- Ví dụ biểu thức
  
  ```python
  is_valid = True
  is_empty = False
  check_status = is_valid and (not is_empty)
  print(check_status) # True
  ```

### Chuyển đổi kiểu dữ liệu (Type Casting)

- Mục đích
  - Chuyển đổi dữ liệu từ kiểu này sang kiểu khác để thực hiện tính toán hoặc xử lý logic
- Các hàm ép kiểu chính
  - `int()`: Chuyển sang số nguyên (Cắt bỏ phần thập phân nếu từ float)
  - `float()`: Chuyển dữ liệu sang số thực
  - `str()`: Biến đổi giá trị bất kỳ sang chuỗi ký tự tương ứng
  - ![](../images/mindmap_img_3.png)
- Minh họa
  
  ```python
  str_value = "100"
  int_value = int(str_value)
  print(int_value + 5) # 105
  ```

### Chương trình tuần tự và xuất dữ liệu

- Cơ chế tuần tự
  - Trình thông dịch Python thực thi từng dòng lệnh từ trên xuống dưới một cách tuần tự cấu trúc
- Xuất dữ liệu ra terminal
  - Sử dụng hàm `print()` để đưa giá trị ra màn hình hiển thị standard output
  ```python
  item_name = "Mechanical Keyboard"
  quantity = 3
  unit_price = 45.5
  total_price = quantity * unit_price
  print("Product:", item_name)
  print("Total Price:", total_price)
  ```

## 



### ham_print

- Cú pháp và tham số hệ thống
  
  ```python
  print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)
  ```
- Tham số định dạng đầu ra
  - sep: Thay đổi ký tự phân tách giữa các phần tử truyền vào
  - end: Xác định ký tự kết thúc dòng lệnh xuất dữ liệu
- Code minh họa cấu hình tham số
  
  ```python
  print("Python", "Basic", sep=" - ", end="!\n")
  ```

### f_string

- Khái niệm Formatted String Literals
  - Tiền tố f hoặc F đặt trước chuỗi nháy kép hoặc đơn
  - Các biến hoặc biểu thức được nhúng trong dấu ngoặc nhọn {}
- Định dạng dữ liệu số trực quan
  - Định dạng số thực làm tròn chữ số thập phân: `{value:.2f}`
  - Ví dụ:
    
    ```python
    score = 9.5678
    print(f"Final Score: {score:.2f}")
    ```
- Cơ chế nội bộ
  - ![](../images/mindmap_img_1.png)

### ham_input

- Đặc tính kiểu dữ liệu mặc định
  - Mọi giá trị người dùng nhập từ bàn phím đều được trả về dưới dạng chuỗi str
  - Không thể thực hiện trực tiếp phép toán số học khi chưa ép kiểu
- Nguyên lý hoạt động
  - Dừng tiến trình hiện tại -> Đợi phản hồi bàn phím -> Kết thúc bằng phím Enter
- Cú pháp cơ bản
  
  ```python
  user_name = input("Enter customer name: ")
  ```

### ep_kieu_du_lieu_co_ban

- Ép kiểu dữ liệu tường minh (Explicit Type Conversion)
  - int(): Chuyển đổi chuỗi chữ số hoặc số thực thành số nguyên
  - float(): Chuyển đổi chuỗi số hoặc số nguyên thành số thực
- Lỗi runtime thường gặp (Gotchas)
  - TypeError: Phát sinh khi thực hiện tính toán số học trên chuỗi chưa ép kiểu
  - ValueError: Phát sinh khi ép kiểu một chuỗi chứa chữ hoặc ký tự đặc biệt sang số
  - Ví dụ lỗi:
    
    ```python
    # Gây ra lỗi ValueError
    number = int("123a")
    ```

### chuong_trinh_cli_tuong_tac

- Quy trình xử lý luồng dữ liệu CLI
  - ![](../images/mindmap_img_2.png)
- Mã nguồn thực hành chuẩn PEP 8
  
  ```python
  user_name = input("Enter customer name: ")
  price_input = input("Enter item unit price: ")
  quantity_input = input("Enter purchase quantity: ")
  
  # Ép kiểu dữ liệu để tính toán
  unit_price = float(price_input)
  purchase_quantity = int(quantity_input)
  actual_total = unit_price * purchase_quantity
  
  # Xuất kết quả định dạng CLI
  print("Processing order data:")
  print("Customer", user_name, sep=" -> ")
  print("Price", unit_price, "Quantity", purchase_quantity, sep=" | ")
  print(f"Final amount to be paid: {actual_total:.2f}")
  ```

## 



### Nhập dữ liệu với hàm input()

- Cơ chế hoạt động
  - Dừng chương trình chờ người dùng nhập dữ liệu từ bàn phím.
  - Giá trị trả về luôn là kiểu chuỗi (str), kể cả khi nhập số.
  - Ví dụ: Nhập `10` -> Kết quả nhận được là `"10"` (str).
- Hệ quả logic
  - Thực hiện phép toán không số học (nhân chuỗi): `"10" * 3` ra kết quả `"101010"`.
  - ![](../images/mindmap_img_1.png)

### Ép kiểu dữ liệu (Type Casting)

- Ép kiểu tường minh (Explicit Type Casting)
  - Sử dụng các hàm dựng sẵn: `int()` để chuyển sang số nguyên, `float()` để chuyển sang số thực.
  - Chuyển đổi dữ liệu thô từ `input()` thành kiểu số để tính toán.
- Mã nguồn mẫu thực chiến
  - Đoạn mã thực thi:
    
    ```python
    price_raw = input("Nhập đơn giá: ")
    qty_raw = input("Nhập số lượng: ")
    price = float(price_raw)
    qty = int(qty_raw)
    total = price * qty
    ```
- Cơ chế quản lý bộ nhớ
  - ![](../images/mindmap_img_2.png)

### Định dạng chuỗi nâng cao với f-string

- Cú pháp cơ bản
  - Khai báo bằng tiền tố `f` hoặc `F` trước cặp nháy: `f"Chuỗi {bien}"`.
  - Python tự động tính toán biểu thức hoặc hiển thị giá trị của biến bên trong ngoặc nhọn `{}`.
- Định dạng nâng cao `{gia_tri:dinh_dang}`
  - Làm tròn số thập phân: Sử dụng `:.2f` để lấy 2 chữ số sau dấu phẩy.
  - Phân tách phần nghìn: Sử dụng `,` để tự động thêm dấu phẩy ngăn cách.
- Mã nguồn định dạng hỗn hợp
  - Đoạn mã thực thi:
    
    ```python
    total = 1250.756
    print(f"Tổng thanh toán: ${total:,.2f}")
    # Kết quả: Tổng thanh toán: $1,250.76
    ```

### Lỗi ngoại lệ thường gặp (Exceptions)

- Lỗi ValueError
  - Nguyên nhân: Ép kiểu chuỗi ký tự không đúng định dạng số.
  - Ví dụ: `int("abc")` hoặc `float("12.3a")`.
- Lỗi TypeError
  - Nguyên nhân: Thực hiện phép toán không hợp lệ giữa các kiểu dữ liệu không tương thích.
  - Ví dụ: Nhân hai chuỗi với nhau `"10" * "5"`.
- Lỗi SyntaxError
  - Nguyên nhân: Viết thiếu tiền tố `f` khi định dạng chuỗi hoặc quên đóng dấu ngoặc nhọn `{}`.
```