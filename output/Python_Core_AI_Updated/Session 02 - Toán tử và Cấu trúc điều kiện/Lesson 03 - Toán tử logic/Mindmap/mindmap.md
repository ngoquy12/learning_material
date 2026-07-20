```markmap
# Session 02: Lesson 03 - Toán tử logic

## Mục tiêu bài học
- Hiểu rõ cách hoạt động của các toán tử logic and, or, not trong Python.
- Nắm vững thứ tự ưu tiên của toán tử và cơ chế đánh giá ngắn mạch.
- Biết cách tạo bảng chân trị tự động để kiểm tra logic code thực tế.

## Toán tử logic cơ bản
### Khái niệm cốt lõi
- Toán tử logic kết hợp nhiều điều kiện so sánh để đưa ra quyết định rẽ nhánh chương trình.
### Cú pháp & Cách khai báo
- Ví dụ cơ bản:
  ```python
  a = True
  b = False
  print(a and b)  # Kết quả: False
  print(a or b)   # Kết quả: True
  print(not a)    # Kết quả: False
  ```
### Lưu ý thực chiến
- Tránh nhầm lẫn giữa toán tử logic (and, or) với toán tử bitwise (&, |) khi xử lý các giá trị Boolean.

## Thứ tự ưu tiên logic
### Khái niệm cốt lõi
- Thứ tự ưu tiên thực thi từ cao xuống thấp khi không có dấu ngoặc là: not, tiếp đến is/in/so sánh, and, và cuối cùng là or.
### Cú pháp & Cách khai báo
- Phân biệt thứ tự mặc định và sử dụng dấu ngoặc đơn:
  ```python
  # Mặc định: and chạy trước or
  res1 = True or False and False  # Tương đương: True or (False and False) -> True
  
  # Thay đổi thứ tự bằng dấu ngoặc
  res2 = (True or False) and False  # Kết quả: False
  ```
### Lưu ý thực chiến
- Luôn sử dụng cặp ngoặc đơn để tường minh hóa các biểu thức phức tạp, tránh lỗi logic do quên thứ tự ưu tiên.

## Kiểm tra đầu vào
### Khái niệm cốt lõi
- Sử dụng các toán tử logic để kiểm tra đồng thời nhiều ràng buộc dữ liệu đầu vào trước khi xử lý tiếp.
### Cú pháp & Cách khai báo
- Xác thực dữ liệu hợp lệ:
  ```python
  tuoi = 20
  chieu_cao = 165
  # Kiểm tra nhiều điều kiện đồng thời
  is_valid = (tuoi >= 18) and (chieu_cao >= 150)
  ```
### Lưu ý thực chiến
- Cảnh giác với giá trị rỗng (chuỗi rỗng "", số 0, None) vì Python coi chúng là Falsy trong các biểu thức điều kiện.

## Đánh giá ngắn mạch
### Khái niệm cốt lõi
- Khi kết quả của biểu thức đã được xác định chắc chắn ở vế trước, Python sẽ dừng và không đánh giá vế sau.
### Cú pháp & Cách khai báo
- Ngăn ngừa lỗi runtime chia cho 0 hoặc lỗi giá trị None:
  ```python
  mau_so = 0
  # Vế trái False giúp bỏ qua vế phải, tránh lỗi ZeroDivisionError
  hop_le = (mau_so != 0) and (10 / mau_so > 1)
  ```
### Lưu ý thực chiến
- Đặt điều kiện kiểm tra an toàn (như khác None hoặc khác 0) ở vế bên trái của toán tử logic để tránh lỗi hệ thống.
- ![](../images/mindmap_img_1.png)

## Bảng chân trị tự động
### Khái niệm cốt lõi
- Sử dụng vòng lặp lồng nhau duyệt qua các cặp giá trị True/False để kết xuất ra toàn bộ kết quả của biểu thức logic.
### Cú pháp & Cách khai báo
- Tạo bảng chân trị tự động cho biểu thức logic:
  ```python
  print("A     | B     | A and (not B)")
  print("-" * 30)
  for A in [True, False]:
      for B in [True, False]:
          ket_qua = A and (not B)
          print(f"{str(A):<5} | {str(B):<5} | {str(ket_qua)}")
  ```
### Lưu ý thực chiến
- Tự động hóa bảng chân trị giúp kiểm thử và phát hiện sai sót logic trong các điều kiện nghiệp vụ phức tạp.
```
```
```