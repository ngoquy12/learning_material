```markmap
# Session 01: Lesson 05 - Nhập, xuất dữ liệu trong Python

## ham_print
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

## f_string
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

## ham_input
- Đặc tính kiểu dữ liệu mặc định
  - Mọi giá trị người dùng nhập từ bàn phím đều được trả về dưới dạng chuỗi str
  - Không thể thực hiện trực tiếp phép toán số học khi chưa ép kiểu
- Nguyên lý hoạt động
  - Dừng tiến trình hiện tại -> Đợi phản hồi bàn phím -> Kết thúc bằng phím Enter
- Cú pháp cơ bản
  ```python
  user_name = input("Enter customer name: ")
  ```

## ep_kieu_du_lieu_co_ban
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

## chuong_trinh_cli_tuong_tac
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
```
```
```