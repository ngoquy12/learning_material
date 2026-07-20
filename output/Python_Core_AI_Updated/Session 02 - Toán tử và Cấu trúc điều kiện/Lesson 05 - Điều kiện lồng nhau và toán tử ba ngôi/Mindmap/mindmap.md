```markmap
# Session 02: Điều kiện lồng nhau và toán tử ba ngôi
## Mục tiêu bài học
- Hiểu và tối ưu hóa cấu trúc rẽ nhánh phức tạp trong Python
- Áp dụng toán tử ba ngôi và mệnh đề bảo vệ để làm sạch mã nguồn
## Nested if-else (Cấu trúc điều kiện lồng nhau)
### Khái niệm cốt lõi
- Việc đặt câu lệnh điều kiện if-else này bên trong một câu lệnh if-else khác để kiểm tra các điều kiện phụ thuộc lẫn nhau.
- ![](../images/mindmap_img_1.png)
### Cú pháp & Cách khai báo
- Cú pháp lồng nhau:
  ```python
  if condition_1:
      if condition_2:
          result = "Both true"
      else:
          result = "Only first true"
  ```
### Lưu ý thực chiến
- Tránh lỗi Deep Nesting (Pyramid of Doom) khi lồng quá 3 tầng if-else, gây khó đọc và bảo trì mã nguồn.
## Ternary Operator (Toán tử ba ngôi trong Python)
### Khái niệm cốt lõi
- Cú pháp viết tắt if-else trên một dòng để gán giá trị hoặc trả về kết quả nhanh chóng dựa theo điều kiện logic.
### Cú pháp & Cách khai báo
- Cú pháp toán tử ba ngôi:
  ```python
  result = "Approved" if amount > 1000 else "Pending"
  ```
### Lưu ý thực chiến
- Không lồng biểu thức ba ngôi trong biểu thức ba ngôi khác vì sẽ gây khó hiểu và giảm khả năng đọc code.
## Guard Clauses (Mệnh đề bảo vệ)
### Khái niệm cốt lõi
- Kỹ thuật kiểm tra điều kiện biên hoặc lỗi ở đầu hàm và thoát sớm bằng return, loại bỏ cấu trúc if-else lồng nhau phức tạp.
- ![](../images/mindmap_img_2.png)
### Cú pháp & Cách khai báo
- Cú pháp sử dụng Guard Clauses:
  ```python
  def check_payment(amount, is_verified):
      if amount <= 0:
          return "Invalid amount"
      if not is_verified:
          return "Unverified account"
      return "Require approval" if amount > 1000 else "Approved"
  ```
### Lưu ý thực chiến
- Bắt buộc phải có lệnh return hoặc raise tương ứng trong các nhánh bảo vệ để chấm dứt hàm ngay lập tức, tránh để logic chạy tiếp xuống dưới.
```
```
```