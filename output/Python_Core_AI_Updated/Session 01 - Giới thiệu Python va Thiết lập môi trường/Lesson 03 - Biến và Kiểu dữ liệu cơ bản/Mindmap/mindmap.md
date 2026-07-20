```markmap
# Session 01: Biến và Kiểu dữ liệu cơ bản

## Mục tiêu bài học
- Khai báo và sử dụng thành thạo biến với các kiểu dữ liệu cơ bản int, float, str, bool.
- Hiểu rõ quy tắc đặt tên biến và cách kiểm tra kiểu dữ liệu bằng hàm type.
- Nhận diện và tránh các lỗi cú pháp cơ bản liên quan đến biến.

## Biến (Variable)
### Khái niệm cốt lõi
- Biến là nhãn hoặc tên tham chiếu đến một vùng nhớ chứa dữ liệu trong bộ nhớ máy tính.
- ![](../images/mindmap_img_1.png)
### Cú pháp & Cách khai báo
- Khai báo tên biến và gán giá trị trực tiếp:
  ```python
  age = 25
  product_name = "Smart Device"
  ```
### Lưu ý thực chiến
- Python là ngôn ngữ kiểu động (dynamic typing), không cần khai báo kiểu dữ liệu trước khi tạo biến.

## Phép gán (Assignment)
### Khái niệm cốt lõi
- Phép gán sử dụng toán tử bằng (=) để liên kết một tên biến với một giá trị hoặc một đối tượng trong bộ nhớ.
### Cú pháp & Cách khai báo
- Sử dụng toán tử `=` để gán:
  ```python
  x = 10
  y = x + 5
  ```
### Lưu ý thực chiến
- Toán tử `=` biểu thị phép gán giá trị từ vế phải sang vế trái, không phải là phép so sánh bằng.

## Quy tắc đặt tên biến (Variable Naming Rules)
### Khái niệm cốt lõi
- Tên biến chỉ được chứa chữ cái, chữ số và dấu gạch dưới, bắt đầu bằng chữ cái hoặc dấu gạch dưới, phân biệt chữ hoa và chữ thường.
### Cú pháp & Cách khai báo
- Tên biến hợp lệ theo quy tắc đặt tên:
  ```python
  student_age = 20
  _value = 5.5
  ```
### Lưu ý thực chiến
- Tránh sử dụng các từ khóa hệ thống, không bắt đầu bằng chữ số và nên tuân thủ định dạng snake_case.

## Kiểu dữ liệu int (Integer)
### Khái niệm cốt lõi
- Kiểu dữ liệu số nguyên, đại diện cho các số nguyên dương, âm hoặc số 0 mà không có phần thập phân.
### Cú pháp & Cách khai báo
- Khai báo biến kiểu số nguyên:
  ```python
  quantity = 100
  negative_number = -50
  ```
### Lưu ý thực chiến
- Số nguyên trong Python có độ dài vô hạn, chỉ bị giới hạn bởi dung lượng bộ nhớ khả dụng của hệ thống.

## Kiểu dữ liệu float (Floating-point)
### Khái niệm cốt lõi
- Kiểu dữ liệu số thực, đại diện cho các số có phần thập phân hoặc các số được biểu diễn ở dạng số mũ.
### Cú pháp & Cách khai báo
- Khai báo biến kiểu số thực:
  ```python
  price = 9.99
  pi = 3.14159
  ```
### Lưu ý thực chiến
- Cần cẩn trọng khi thực hiện phép toán so sánh trực tiếp float do sai số làm tròn số phân số trong hệ nhị phân.

## Kiểu dữ liệu str (String)
### Khái niệm cốt lõi
- Kiểu dữ liệu chuỗi ký tự, dùng để lưu trữ văn bản và được đặt trong cặp dấu nháy đơn hoặc nháy kép.
### Cú pháp & Cách khai báo
- Khai báo biến kiểu chuỗi:
  ```python
  greeting = "Hello"
  address = '123 Street'
  ```
### Lưu ý thực chiến
- Chuỗi ký tự trong Python là đối tượng không thể thay đổi giá trị tại chỗ (immutable) sau khi được tạo.

## Kiểu dữ liệu bool (Boolean)
### Khái niệm cốt lõi
- Kiểu dữ liệu luận lý chỉ nhận một trong hai trạng thái giá trị logic là True hoặc False.
### Cú pháp & Cách khai báo
- Khai báo biến kiểu luận lý:
  ```python
  is_active = True
  is_completed = False
  ```
### Lưu ý thực chiến
- Từ khóa True và False bắt buộc phải viết hoa chữ cái đầu tiên, viết thường hoàn toàn sẽ gây ra lỗi định nghĩa.

## Hàm type()
### Khái niệm cốt lõi
- Hàm tích hợp sẵn dùng để kiểm tra và trả về kiểu dữ liệu thực tế của một đối tượng hoặc một biến.
### Cú pháp & Cách khai báo
- Sử dụng hàm type để xác định kiểu dữ liệu:
  ```python
  x = 10
  print(type(x))
  ```
### Lưu ý thực chiến
- Hàm trả về một đối tượng kiểu dữ liệu, thường được kết hợp với hàm print để hiển thị thông tin trực quan.

## Hàm print()
### Khái niệm cốt lõi
- Hàm tích hợp sẵn dùng để hiển thị dữ liệu hoặc kết quả của các biến và biểu thức ra màn hình.
### Cú pháp & Cách khai báo
- Sử dụng hàm print để xuất nhiều giá trị:
  ```python
  message = "Rikkei"
  print("Welcome to", message)
  ```
### Lưu ý thực chiến
- Hàm print tự động thêm ký tự xuống dòng ở cuối đầu ra, có thể cấu hình lại bằng tham số end.

## Lỗi cú pháp (Syntax Error)
### Khái niệm cốt lõi
- Lỗi xảy ra do viết mã nguồn vi phạm các quy tắc cú pháp và cấu trúc câu lệnh của ngôn ngữ Python.
### Cú pháp & Cách khai báo
- Ví dụ về mã nguồn gây lỗi cú pháp:
  ```python
  # 1st_value = 10  # Lỗi do tên biến bắt đầu bằng số
  # class = 5       # Lỗi do trùng từ khóa hệ thống
  ```
### Lưu ý thực chiến
- Khi gặp lỗi cú pháp, trình thông dịch Python sẽ thông báo lỗi và dừng chương trình ngay lập tức trước khi chạy.
```
```
```