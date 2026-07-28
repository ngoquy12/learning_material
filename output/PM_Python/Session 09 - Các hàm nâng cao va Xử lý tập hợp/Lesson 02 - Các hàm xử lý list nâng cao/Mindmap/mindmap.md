```markmap
# Session 09: Các hàm xử lý list nâng cao

## list_comprehension_co_ban
### Bản chất và Nguyên lý
- Khởi tạo danh sách mới cực ngắn từ một iterable có sẵn
- Cú pháp cơ bản: `[expression for item in iterable if condition]`
- ![](../images/mindmap_img_1.png)
### Mã nguồn minh họa
- Lọc phần tử chẵn từ danh sách số
  ```python
  numbers = [1, 2, 3, 4, 5]
  evens = [x for x in numbers if x % 2 == 0]
  ```

## list_comprehension_nang_cao
### Cú pháp điều kiện phức hợp
- Dùng cấu trúc rẽ nhánh `if-else` trực tiếp đứng trước vòng lặp
- Cú pháp biến đổi: `[expr_t if cond else expr_f for item in iterable]`
- Quy tắc thực tế: Sử dụng tối đa một toán tử ba ngôi để tránh làm giảm độ đọc hiểu
### Vòng lặp lồng nhau (Nested loops)
- Cho phép lặp qua nhiều danh sách tuần tự để làm phẳng (Flatten) ma trận
  ```python
  matrix = [[1, 2], [3, 4]]
  flat = [val for row in matrix for val in row]
  ```

## list_sort_vs_sorted
### Phương thức list.sort() (In-place)
- Tác động trực tiếp lên danh sách gốc, thay đổi thứ tự phần tử tại chỗ
- Trả về giá trị `None`, giúp tối ưu hóa bộ nhớ thực thi
### Hàm built-in sorted()
- Tạo và trả về danh sách mới đã được sắp xếp, giữ nguyên danh sách gốc ban đầu
- Thích hợp khi cần giữ lại trạng thái ban đầu của dữ liệu để đối chiếu
### Mã nguồn so sánh
- Phân biệt cơ chế tác động trực tiếp và tạo mới
  ```python
  data = [3, 1, 2]
  new_data = sorted(data)  # new_data=[1,2,3], data=[3,1,2]
  data.sort()              # data=[1,2,3]
  ```

## sap_xep_da_tieu_chi_lambda
### Cơ chế lọc bằng key=lambda
- Trích xuất tiêu chí so sánh cho từng phần tử thông qua hàm ẩn danh (Anonymous Function)
- Kết hợp tuple trong giá trị trả về của lambda để thực hiện sắp xếp qua nhiều thứ tự ưu tiên khác nhau
### Mã nguồn nâng cao
- Trình bày thuật toán sắp xếp danh sách đối tượng lồng nhau
  ```python
  products = [
      {"name": "Laptop", "price": 1200, "active": True},
      {"name": "Mouse", "price": 25, "active": True},
      {"name": "Monitor", "price": 300, "active": False}
  ]
  # Sắp xếp active giảm dần (True trước), sau đó giá giảm dần
  products.sort(key=lambda x: (not x["active"], -x["price"]))
  ```
### Các lỗi phổ biến khi thực thi (Runtime Gotchas)
- KeyError: Truy cập vào khóa định danh không tồn tại trong từ điển
- TypeError: So sánh các kiểu dữ liệu không tương thích như int và str
- AttributeError: Dùng sai ký pháp dấu chấm `.key` trên kiểu dữ liệu dict thay vì `["key"]`

## list_comprehension_vs_map_filter
### Khác biệt về cơ chế và hiệu năng
- List Comprehension: Trực quan, dễ đọc, cấu trúc tường minh và được khuyên dùng trong Python
- Map và Filter: Trả về generator/iterator giúp tiết kiệm bộ nhớ tức thời (Lazy Evaluation)
### Sự tương đương trong cú pháp
- So sánh cách cài đặt cùng một bài toán xử lý chuỗi dữ liệu
  ```python
  # Cách 1: List Comprehension
  r1 = [x * 2 for x in range(5) if x > 2]
  # Cách 2: Phối hợp map & filter
  r2 = list(map(lambda x: x * 2, filter(lambda x: x > 2, range(5))))
  ```

## pep_8_clean_code
### Quy tắc thẩm mỹ và độ dài
- Hạn chế viết list comprehension quá dài vượt quá 79 ký tự trên một dòng đơn
- Tách dòng rõ ràng và thụt lề chuẩn khi xử lý cấu trúc điều kiện phức tạp
### Tối ưu hóa Readable Code
- Tránh lạm dụng List Comprehension cho các tác vụ biến đổi dữ liệu có logic quá phức tạp
- Ưu tiên viết tường minh bằng vòng lặp `for` truyền thống nếu logic phân nhánh vượt quá 2 tầng
```
```
```