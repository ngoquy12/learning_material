```markmap
# Session 02: Cấu trúc match-case nâng cao

## Mục tiêu bài học
- Hiểu và áp dụng cơ chế so khớp mẫu (Pattern Matching) để thay thế cấu trúc if-elif-else phức tạp.
- Sử dụng thành thạo cấu trúc match-case với Sequence, Mapping, Guard Clause và Capture Pattern.
- Kiểm soát và xử lý an toàn các nhánh rẽ nhánh đa trường hợp trong Python 3.10+.

## Structural Pattern Matching
### Khái niệm cốt lõi
- Cơ chế so khớp cấu trúc dữ liệu theo mẫu (shape/structure) và giá trị của dữ liệu.
### Cú pháp & Cách khai báo
- Cú pháp cơ bản:
  ```python
  match status_code:
      case 200:
          print("OK")
      case 404:
          print("Not Found")
  ```
### Lưu ý thực chiến
- Chỉ hỗ trợ từ Python 3.10 trở lên. Không hoạt động trên các phiên bản cũ hơn.
- ![](../images/mindmap_img_1.png)

## Wildcard Pattern (case _)
### Khái niệm cốt lõi
- Mẫu đại diện khớp với bất kỳ giá trị nào, đóng vai trò như nhánh mặc định (default/else) khi không có trường hợp nào khác khớp.
### Cú pháp & Cách khai báo
- Sử dụng ký tự gạch dưới:
  ```python
  match value:
      case 1:
          print("One")
      case _:
          print("Default case")
  ```
### Lưu ý thực chiến
- Bắt buộc phải đặt ở vị trí cuối cùng trong danh sách các match case để tránh gây lỗi SyntaxError.

## Sequence Pattern
### Khái niệm cốt lõi
- So khớp dữ liệu dạng chuỗi tuần tự như danh sách (list) hoặc bộ dữ liệu (tuple) dựa trên số lượng và cấu trúc phần tử.
### Cú pháp & Cách khai báo
- Ví dụ so khớp list/tuple:
  ```python
  match point:
      case (0, 0):
          print("Origin")
      case (x, y):
          print(f"Point {x}, {y}")
      case (x, y, *rest):
          print(f"3D+ Point, remaining: {rest}")
  ```
### Lưu ý thực chiến
- Sử dụng dấu sao (*) để gom phần còn lại của sequence vào một biến, tránh lỗi lệch số lượng phần tử.

## Mapping Pattern
### Khái niệm cốt lõi
- So khớp dữ liệu kiểu ánh xạ hoặc từ điển (dictionary) dựa trên sự hiện diện của các khóa (keys) và giá trị tương ứng.
### Cú pháp & Cách khai báo
- Ví dụ so khớp dictionary:
  ```python
  match user_data:
      case {"role": "admin", "id": user_id}:
          print(f"Admin ID: {user_id}")
      case {"role": _}:
          print("Standard user")
  ```
### Lưu ý thực chiến
- Chỉ kiểm tra sự trùng khớp của các cặp key-value được khai bảo, các key dư thừa khác trong object thực tế sẽ được bỏ qua.

## Guard Clause (if trong match-case)
### Khái niệm cốt lõi
- Điều kiện bổ sung (guard) đi kèm sau biểu thức so khớp mẫu giúp bộ lọc hoạt động chặt chẽ hơn.
### Cú pháp & Cách khai báo
- Thêm từ khóa if phía sau case pattern:
  ```python
  match number:
      case val if val > 0:
          print("Positive")
      case val if val < 0:
          print("Negative")
  ```
### Lưu ý thực chiến
- Biến trong pattern sẽ được gán giá trị trước khi biểu thức điều kiện của mệnh đề if được đánh giá.

## Capture Pattern (Từ khóa as)
### Khái niệm cốt lõi
- Trích xuất và ràng buộc một phần hoặc toàn bộ mẫu đã khớp vào một biến để tái sử dụng trong khối mã thực thi.
### Cú pháp & Cách khai báo
- Sử dụng từ khóa as để gán biến:
  ```python
  match response:
      case {"status": 200, "data": x} as result:
          print(f"Full response: {result}, data: {x}")
  ```
### Lưu ý thực chiến
- Rất hữu dụng khi cần vừa xác thực cấu trúc logic của mẫu vừa lưu lại toàn bộ dữ liệu gốc để xử lý.
```
```
```