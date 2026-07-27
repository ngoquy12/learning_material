```markmap
# Session 02 - Lesson 05: Điều kiện lồng nhau và toán tử ba ngôi

## Mục tiêu bài học
- Nắm vững cú pháp điều kiện lồng nhau và tối ưu hóa cấu trúc rẽ nhánh bằng Guard Clauses
- Hiểu rõ bản chất, cú pháp và phạm vi áp dụng toán tử ba ngôi
- Áp dụng các tiêu chuẩn PEP 8 để định dạng câu lệnh điều kiện rõ ràng, sạch sẽ
- Làm chủ cơ chế Đánh giá ngắn mạch để tối ưu hóa hiệu năng và phòng tránh lỗi runtime

## Nested If-Else (Cấu trúc điều kiện lồng nhau)
### Khái niệm cốt lõi
- Xảy ra khi một khối lệnh rẽ nhánh chứa một cấu trúc rẽ nhánh khác bên trong để kiểm tra điều kiện phụ thuộc
- Lạm dụng lồng nhau quá sâu tạo ra mô hình Arrow Pattern gây khó đọc và bảo trì
- ![](../images/mindmap_img_1.png)
### Cú pháp & Cách khai báo
- Code mẫu:
  ```python
  # Cach tiep can phang hoa ma nguon dung Guard Clause
  def get_rate(vip, amount):
      if amount <= 0:
          return 0.0
      if not vip:
          return 0.05
      return 0.2 if amount > 200 else 0.1
  ```
### Lưu ý thực chiến
- Ưu tiên sử dụng Guard Clauses để thoát hàm sớm giúp giảm cấp thụt lề
- Chú ý căn lề đồng nhất để tránh lỗi IndentationError khi lồng các khối mã

## Ternary Operator (Toán tử ba ngôi)
### Khái niệm cốt lõi
- Là biểu thức điều kiện (Conditional Expression) viết trên một dòng nhằm gán giá trị trực tiếp dựa trên điều kiện đúng hoặc sai
- Giúp rút gọn các khối if-else gán giá trị đơn giản thành biểu thức ngắn gọn
### Cú pháp & Cách khai báo
- Code mẫu:
  ```python
  # value_if_true if condition else value_if_false
  discount = 0.2 if is_vip else 0.05
  ```
### Lưu ý thực chiến
- Tuyệt đối không lồng nhiều toán tử ba ngôi trên cùng một dòng vì dễ gây SyntaxError hoặc mã nguồn cực kỳ khó hiểu
- Không lạm dụng cho các logic xử lý phức tạp, chỉ dùng cho thao tác gán trị đơn giản

## Tiêu chuẩn PEP 8 cho câu lệnh điều kiện
### Khái niệm cốt lõi
- Quy chuẩn định dạng mã nguồn Python giúp thống nhất cách viết các biểu thức điều kiện, tăng tính tường minh
### Cú pháp & Cách khai báo
- Code mẫu:
  ```python
  # Kiem tra gia tri logic dung chuan PEP 8
  if is_active:
      process()
  # Kiem tra None dung chuan
  if target is None:
      exit()
  ```
### Lưu ý thực chiến
- Tránh các so sánh dư thừa dạng `if is_vip == True:`, nên viết gọn là `if is_vip:`
- Giới hạn độ dài dòng biểu thức dưới 79 ký tự để đảm bảo tính mỹ quan của mã nguồn

## Đánh giá ngắn mạch (Short-circuit Evaluation)
### Khái niệm cốt lõi
- Cơ chế tối ưu của Python dừng đánh giá các toán hạng tiếp theo trong biểu thức logic ngay khi kết quả cuối cùng được xác định
- Toán tử `and` dừng ngay khi gặp toán hạng False; toán tử `or` dừng ngay khi gặp toán hạng True
- ![](../images/mindmap_img_2.png)
### Cú pháp & Cách khai báo
- Code mẫu:
  ```python
  # Tranh chia cho 0 nho ngan mach kiem tra x != 0 truoc
  if x != 0 and (y / x) > 1.5:
      print("Valid calculation")
  ```
### Lưu ý thực chiến
- Đặt điều kiện tối giản hoặc cần kiểm tra an toàn lên trước để lọc dữ liệu sớm
- Phải khai báo đầy đủ các biến liên quan để tránh phát sinh lỗi NameError hoặc TypeError khi ngắn mạch không được kích hoạt
```
```
```