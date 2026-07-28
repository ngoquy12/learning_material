```markmap
# Session 07 - Lesson 05: Khi nào nên dùng List, Dictionary hay Set
## List (Danh sách)
### Bản chất
- Cấu trúc tuyến tính có thứ tự (ordered sequence)
- Cho phép trùng lặp dữ liệu (duplicates)
### Khi nào dùng
- Bảo toàn thứ tự chèn (insertion order)
- Truy cập phần tử qua chỉ mục (index index-based access)
- Làm hàng đợi (queue) hoặc ngăn xếp (stack)
### Mã nguồn mẫu
- ```python
  request_history = ["10:00:01", "10:00:05"]
  request_history.append("10:01:23")
  ```

## Set (Tập hợp)
### Bản chất
- Tập hợp không có thứ tự (unordered sequence)
- Các phần tử phải duy nhất (unique) và không thể thay đổi trực tiếp (immutable)
### Khi nào dùng
- Loại bỏ trùng lặp dữ liệu (deduplication)
- Kiểm tra sự tồn tại (membership testing) cực nhanh
### Mã nguồn mẫu
- ```python
  access_logs = ["192.168.1.1", "10.0.0.5", "192.168.1.1"]
  unique_blocked_ips = set(access_logs)
  is_blocked = "192.168.1.1" in unique_blocked_ips
  ```

## Dictionary (Từ điển)
### Bản chất
- Cấu trúc bản đồ khóa - giá trị (key-value mapping)
- Tránh trùng lặp đối với Key
### Khi nào dùng
- Tạo mối liên kết logic giữa Key và Value
- Tra cứu dữ liệu nhanh chóng dựa trên định danh (Key)
### Mã nguồn mẫu
- ```python
  role_clearances = {"admin": "level_3", "guest": "level_1"}
  # Dùng get() để tránh KeyError khi Key không tồn tại
  role_level = role_clearances.get("guest", "level_0")
  ```

## Độ phức tạp thời gian tìm kiếm
### Cơ chế tìm kiếm
- List: O(n) - Duyệt tuần tự từ đầu đến cuối danh sách (Linear Search)
- Set và Dictionary: O(1) - Sử dụng hàm băm tự động tìm vị trí vùng nhớ (Hash Table)
- ![](../images/mindmap_img_1.png)

## Khả năng băm (Hashability)
### Nguyên lý
- Chỉ các đối tượng immutable (str, int, float, tuple) mới có thể băm (hashable)
- Đối tượng mutable (list, set, dict) không thể tạo hash value để làm Key cho Dict hoặc làm phần tử cho Set
### Các lỗi Runtime thường gặp
- KeyError: Truy cập trực tiếp key không tồn tại qua cú pháp dict[key]
- TypeError: Đưa kiểu mutable vào làm phần tử của Set hoặc Key của Dict
- ```python
  # Gây lỗi TypeError: unhashable type: 'list'
  invalid_set = {[1, 2], 3} 
  ```
- ![](../images/mindmap_img_2.png)

## Chuẩn PEP 8 cho cấu trúc dữ liệu cơ bản
### Trình bày mã nguồn chuẩn hóa
- Đặt khoảng trắng sau các dấu phẩy `,`
- Đặt khoảng trắng sau dấu hai chấm `:` phân tách key-value
- Thụt lề nhất quán cho các danh sách hoặc từ điển nhiều dòng
### Ví dụ chuẩn PEP 8
- ```python
  # Khai báo chuẩn khoảng trắng
  correct_list = [1, 2, 3]
  correct_dict = {"admin": "level_3", "guest": "level_1"}
  ```
```
```