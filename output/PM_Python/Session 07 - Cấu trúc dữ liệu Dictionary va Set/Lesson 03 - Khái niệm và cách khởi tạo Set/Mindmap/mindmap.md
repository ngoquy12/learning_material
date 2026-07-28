```markmap
# Session 07: Khái niệm và cách khởi tạo Set
## Set (Tập hợp)
- Định nghĩa: Cấu trúc dữ liệu đại diện cho tập hợp chứa các phần tử không trùng lặp.
- Cơ chế hoạt động: Sử dụng bảng băm (Hash Table) để lưu trữ, giúp tối ưu hóa hiệu năng kiểm tra phần tử (membership testing) với độ phức tạp O(1).
- ![](../images/mindmap_img_1.png)
## Tính độc bản (Unique) và Không thứ tự (Unordered)
- Tính độc bản: Tự động loại bỏ hoàn toàn các giá trị trùng lặp khi nạp vào Set.
- Tính không thứ tự: Các phần tử không được gán chỉ mục (Index), không lưu vết vị trí xuất hiện ban đầu.
## Khởi tạo Set rỗng
- Lưu ý quan trọng: Tuyệt đối không sử dụng cặp ngoặc nhọn rỗng vì Python sẽ định nghĩa đó là một Dictionary rỗng.
- Cú pháp chuẩn xác:
  ```python
  # Đúng: Khởi tạo Set rỗng bằng constructor
  my_set = set()

  # Sai: Khởi tạo dictionary rỗng
  my_dict = {}
  ```
## Ép kiểu dữ liệu (Type Casting)
- Cơ chế: Chuyển đổi các cấu trúc dữ liệu dạng chuỗi (Sequence) sang Set để loại bỏ các phần tử trùng lặp.
- Cú pháp ứng dụng thực tế:
  ```python
  raw_user_ids = [1001, 1002, 1001, 1003, 1002, 1004]
  unique_user_ids = set(raw_user_ids)
  # unique_user_ids chứa: {1001, 1002, 1003, 1004}
  ```
## Lỗi phần tử Mutable (Unhashable Class)
- Nguyên lý: Tất cả phần tử trong Set phải là Immutable (bất biến) và Hashable (có thể băm). Các đối tượng khả biến (Mutable) như List hay Dict không được phép làm phần tử của Set.
- Lỗi Runtime thường gặp (TypeError):
  ```python
  # Ném lỗi: TypeError: unhashable type: 'list'
  invalid_set = {[1, 2], 3}
  ```
- Giải pháp khắc phục: Chuyển đổi cấu trúc Mutable (List) thành Immutable (Tuple) trước khi đưa vào Set.
  ```python
  # Chương trình hoạt động chính xác
  valid_set = {(1, 2), 3}
  ```
```
```
```