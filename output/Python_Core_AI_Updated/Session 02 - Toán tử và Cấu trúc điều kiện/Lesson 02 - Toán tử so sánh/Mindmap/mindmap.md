```markmap
# Session 02: Toán tử so sánh

## Mục tiêu bài học
- Hiểu rõ chức năng của 6 toán tử so sánh cơ bản trong ngôn ngữ Python.
- Phân biệt chính xác bản chất của phép gán và phép so sánh bằng.
- Tạo lập các biểu thức logic thực tế và kiểm soát lỗi không tương thích kiểu dữ liệu.

## Phân biệt gán và so sánh bằng
### Khái niệm cốt lõi
- Toán tử gán (=) để lưu trữ giá trị vào vùng nhớ của biến. Toán tử so sánh bằng (==) để kiểm tra tính tương đương và trả về kết quả True hoặc False.
- ![](../images/mindmap_img_1.png)
### Cú pháp & Cách khai báo
- 
  ```python
  # Gán giá trị 20 cho biến age
  age = 20
  # So sánh giá trị của age với 18
  is_equal = age == 18
  ```
### Lưu ý thực chiến
- Nhầm lẫn sử dụng '=' thay cho '==' trong cấu trúc điều kiện là lỗi cú pháp phổ biến dẫn đến SyntaxError.

## Sáu toán tử so sánh cơ bản
### Khái niệm cốt lõi
- Các toán tử so sánh bao gồm: lớn hơn (>), bé hơn (<), lớn hơn hoặc bằng (>=), bé hơn hoặc bằng (<=), bằng (==), khác (!=). Bản chất là đánh giá quan hệ giữa hai toán hạng.
### Cú pháp & Cách khai báo
- 
  ```python
  x = 15
  y = 10
  print(x > y)   # True
  print(x <= y)  # False
  print(x != y)  # True
  ```
### Lưu ý thực chiến
- Không viết sai thứ tự của các toán tử ghép, ví dụ viết nhầm thành '=>' hoặc '=<' sẽ gây lỗi cú pháp.

## Kiểu dữ liệu Boolean và biểu thức
### Khái niệm cốt lõi
- Kết quả trả về của bất kỳ biểu thức so sánh nào đều thuộc kiểu dữ liệu boolean (chỉ gồm hai giá trị: True hoặc False).
### Cú pháp & Cách khai báo
- 
  ```python
  score = 8.5
  has_passed = score >= 5.0
  print(has_passed)       # True
  print(type(has_passed)) # <class 'bool'>
  ```
### Lưu ý thực chiến
- Biến kiểu Boolean nên được đặt tên có tiền tố chỉ trạng thái như 'is_', 'has_', 'can_' để mã nguồn tự tường minh.

## So sánh chuỗi và số
### Khái niệm cốt lõi
- Việc so sánh chuỗi với số qua toán tử so sánh thứ tự (>, <, >=, <=) sẽ sinh lỗi. Phép so sánh quan hệ chuỗi được thực hiện theo thứ tự mã Unicode (lexicographical order).
- ![](../images/mindmap_img_2.png)
### Cú pháp & Cách khai báo
- 
  ```python
  compare_str = 'apple' < 'banana' # True
  # So sánh bằng khác kiểu dữ liệu
  is_equal = '20' == 20            # False
  ```
### Lưu ý thực chiến
- So sánh lớn bé khác kiểu dữ liệu sinh ra lỗi TypeError. Phải ép kiểu dữ liệu về cùng một dạng trước khi so sánh.

## Biểu thức logic thực tế
### Khái niệm cốt lõi
- Biểu thức so sánh lưu kết quả boolean của các điều kiện trong thực tế để phục vụ cho các logic rẽ nhánh chương trình.
### Cú pháp & Cách khai báo
- 
  ```python
  age = 20
  # Đánh giá tính hợp lệ của tuổi tham gia
  is_eligible = age >= 18
  print('Eligible:', is_eligible)
  ```
### Lưu ý thực chiến
- Nên phân tách các biểu thức logic phức tạp thành các biến bool trung gian thay vì viết chuỗi so sánh quá dài trên một dòng code.
```
```
```