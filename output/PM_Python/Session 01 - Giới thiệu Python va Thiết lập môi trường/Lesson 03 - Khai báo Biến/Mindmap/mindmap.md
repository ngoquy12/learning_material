```markmap
# Session 01 - Lesson 03: Khai báo Biến

## Biến (Variable)
- Bản chất kỹ thuật
  - Là nhãn tham chiếu (Reference label) liên kết với một đối tượng (Object) trong bộ nhớ RAM
  - Không phải vùng chứa tĩnh, chỉ lưu trữ địa chỉ của đối tượng đang trỏ tới
  - ![](../images/mindmap_img_1.png)
- Hành vi xử lý
  - Có thể thay đổi đối tượng tham chiếu linh hoạt nhờ cơ chế Dynamic Typing của Python

## Phép gán (=)
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

## Quy tắc đặt tên biến
- Ký tự hợp lệ
  - Chỉ gồm chữ cái (a-z, A-Z), chữ số (0-9) và dấu gạch dưới (_)
- Quy tắc bắt đầu
  - Phải bắt đầu bằng chữ cái hoặc dấu gạch dưới (_), cấm bắt đầu bằng chữ số
- Nhạy cảm hoa thường
  - Phân biệt chữ hoa và chữ thường (Case-sensitive)
- Từ khóa hệ thống (Keywords)
  - Không được trùng với các từ khóa dành riêng của Python như `if`, `class`, `import`

## Chuẩn PEP 8 (snake_case)
- Quy chuẩn định dạng
  - Viết thường toàn bộ ký tự tên biến
  - Ngăn cách các từ bằng dấu gạch dưới (_) để dễ đọc
  - Ví dụ chuẩn: `original_price`, `total_price`
- Trực quan nghiệp vụ
  - Đặt tên mang ý nghĩa mô tả rõ ràng dữ liệu thực tế thay vì ký tự vô nghĩa như `x`, `y`, `z`

## Lỗi Cú pháp (SyntaxError)
- Cơ chế kích hoạt
  - Xảy ra khi trình biên dịch/thông dịch quét mã nguồn và phát hiện tên biến vi phạm quy tắc đặt tên
  - Ngăn chương trình khởi chạy ngay lập tức
- Các trường hợp vi phạm điển hình
  - Bắt đầu bằng chữ số: `1st_place = 10`
  - Chứa ký tự cấm: `user-name = "Admin"` hoặc `user$email = "admin@rikkei.edu.vn"`

## Lỗi Định danh (NameError)
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
```
```
```