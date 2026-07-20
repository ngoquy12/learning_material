```markmap
# Session 02: Cấu trúc điều kiện rẽ nhánh if-elif-else

## Mục tiêu bài học
- Sử dụng cấu trúc rẽ nhánh điều kiện logic cơ bản với if, elif và else.
- Viết biểu thức so sánh và kết hợp chúng bằng toán tử logic để kiểm soát chương trình.
- Phát hiện và khắc phục các lỗi cú pháp về thụt lề và lỗi dòng điều khiển không thể thực thi.

## Khối lệnh điều kiện if-else
### Khái niệm cốt lõi
- Cho phép chương trình lựa chọn thực thi hoặc bỏ qua một khối lệnh dựa trên tính đúng/sai (True/False) của một điều kiện.
### Cú pháp & Cách khai báo
- Ví dụ cú pháp:
  ```python
  x = 10
  if x > 5:
      print("Lớn hơn 5")
  else:
      print("Nhỏ hơn hoặc bằng 5")
  ```
### Lưu ý thực chiến
- Cần có dấu hai chấm ở cuối điều kiện và bắt buộc các dòng lệnh phía dưới phải thụt lề đồng nhất để tránh lỗi SyntaxError hoặc IndentationError.

## Biểu thức điều kiện
### Khái niệm cốt lõi
- Biểu thức trả về giá trị Boolean (True hoặc False) qua việc so sánh các giá trị hoặc biến số.
### Cú pháp & Cách khai báo
- Ví dụ cú pháp:
  ```python
  a = 15
  b = 20
  ket_qua = a < b
  ```
### Lưu ý thực chiến
- Tránh nhầm lẫn giữa toán tử gán '=' và toán tử so sánh bằng '=='.

## Cấu trúc rẽ nhánh nhiều trường hợp if-elif-else
### Khái niệm cốt lõi
- Chuỗi các nhánh điều kiện chạy liên tiếp, chương trình sẽ đi vào khối lệnh đầu tiên thoả mãn True và bỏ qua các nhánh còn lại.
### Cú pháp & Cách khai báo
- Ví dụ cú pháp:
  ```python
  bmi = 22.5
  if bmi < 18.5:
      print("Thiếu cân")
  elif bmi < 25.0:
      print("Bình thường")
  else:
      print("Béo phì")
  ```
### Lưu ý thực chiến
- Nhánh else là tuỳ chọn và chỉ chạy khi toàn bộ các điều kiện if và elif phía trước đều sai (False).
- ![](../images/mindmap_img_1.png)

## Toán tử logic
### Khái niệm cốt lõi
- Các từ khoá and, or, not dùng để liên kết nhiều biểu thức so sánh đơn lẻ thành một điều kiện phức tạp.
### Cú pháp & Cách khai báo
- Ví dụ sử dụng:
  ```python
  tuoi = 20
  co_bang_lai = True
  if tuoi >= 18 and co_bang_lai:
      print("Được phép lái xe")
  ```
### Lưu ý thực chiến
- Toán tử and yêu cầu tất cả các vế đúng, toán tử or chỉ cần một vế đúng, toán tử not phủ định giá trị Boolean gốc.

## Dòng điều khiển (Control Flow)
### Khái niệm cốt lõi
- Trình tự thực thi các câu lệnh của chương trình, bị rẽ sang các hướng khác nhau khi gặp cấu trúc điều kiện.
### Cú pháp & Cách khai báo
- Ví dụ dòng chạy:
  ```python
  print("Bắt đầu")
  if False:
      print("Bỏ qua dòng này")
  print("Kết thúc")
  ```
### Lưu ý thực chiến
- Dòng điều khiển sẽ đi từ trên xuống dưới, việc kiểm soát thứ tự nhánh quyết định hiệu năng và logic của chương trình.
- ![](../images/mindmap_img_2.png)

## Lỗi logic điều kiện không thể thực thi (Unreachable Code)
### Khái niệm cốt lõi
- Hiện tượng một khối lệnh không bao giờ được thực hiện do logic điều kiện bao trùm của nhánh trước đó đã chặn hết các dữ liệu đầu vào có thể xảy ra.
### Cú pháp & Cách khai báo
- Ví dụ lỗi:
  ```python
  x = 15
  if x > 10:
      print("Lớn hơn 10")
  elif x > 20: 
      print("Không thể chạm tới")
  ```
### Lưu ý thực chiến
- Luôn kiểm tra xem miền giá trị của các điều kiện đằng sau có bị trùng khít hay nằm hoàn toàn trong miền của các điều kiện đằng trước hay không.

## Tối ưu hóa thứ tự nhánh điều kiện
### Khái niệm cốt lõi
- Sắp xếp các điều kiện theo mức độ ưu tiên hoặc phạm vi từ hẹp đến rộng để tránh bỏ sót trường hợp và tối ưu số lần so khớp biểu thức.
### Cú pháp & Cách khai báo
- Sắp xếp hợp lý:
  ```python
  score = 85
  if score >= 90:
      print("Xuất sắc")
  elif score >= 80:
      print("Khá")
  ```
### Lưu ý thực chiến
- Đặt điều kiện có điều kiện biên chặt chẽ hơn hoặc có tần suất xảy ra cao hơn lên trước nhằm giảm thiểu công sức tính toán của máy tính.
```
```
```