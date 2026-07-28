```markmap
# S06-L04: Khái niệm Tuple và cách khởi tạo

## Tuple
- Bản chất: Cấu trúc dữ liệu dạng chuỗi (Sequence Type) sắp thứ tự (Ordered) và cho phép chứa các phần tử trùng lặp
- Phân bổ vùng nhớ: Lưu trữ trực tiếp dữ liệu dạng mảng cố định, tối ưu hóa tốc độ truy cập hơn List
- Cách khởi tạo cơ bản:
  ```python
  server_coordinate = (10.762622, 106.660172)
  connection_ports = (8000, 8080, 9000)
  ```
- ![](../images/mindmap_img_1.png)

## Đặc tính Bất biến (Immutability)
- Định nghĩa: Giá trị của các phần tử bên trong Tuple không thể bị sửa đổi, thêm mới hoặc xóa bỏ sau khi đã khởi tạo thành công
- Lợi ích thiết kế: Đảm bảo tính toàn vẹn dữ liệu (Data integrity) và an toàn luồng trong suốt vòng đời ứng dụng

## Lỗi TypeError với Tuple
- Mô tả: Phát sinh khi cố ý gán lại giá trị cho một phần tử qua chỉ mục
- Lỗi gán chỉ mục trực tiếp:
  ```python
  ports = (80, 443)
  ports[0] = 8080 # Gây ra lỗi TypeError: 'tuple' object does not support item assignment
  ```
- Lỗi phương thức thay đổi cấu trúc: Phát sinh lỗi `AttributeError` khi cố tình gọi `.append()`, `.pop()`, `.remove()`, hoặc `.insert()`

## Tuple đơn phần tử
- Quy tắc cú pháp: Bắt buộc phải có dấu phẩy `,` ngay sau phần tử duy nhất để Python nhận diện là kiểu Tuple
- Nhận diện cú pháp:
  ```python
  valid_tuple = (100,)   # Điểm dừng cuối là dấu phẩy -> Hợp lệ (Kiểu tuple)
  invalid_tuple = (100)  # Thiếu dấu phẩy -> Lỗi logic (Kiểu int)
  ```

## Tuple Indexing
- Nguyên lý: Truy cập phần tử thông qua chỉ mục số nguyên đặt trong cặp ngoặc vuông `[]`
- Phân loại chỉ mục:
  - Chỉ mục dương (Positive indexing): Bắt đầu từ 0 (phần tử đầu tiên) tiến dần về bên phải
  - Chỉ mục âm (Negative indexing): Bắt đầu từ -1 (phần tử cuối cùng) lùi dần về bên trái
- Code mẫu truy cập:
  ```python
  network_protocols = ('TCP', 'UDP', 'HTTP')
  first_protocol = network_protocols[0]   # 'TCP'
  last_protocol = network_protocols[-1]   # 'HTTP'
  ```

## Tuple Slicing
- Cú pháp: `tuple_obj[start:stop:step]` trích xuất một Tuple mới từ Tuple gốc từ chỉ mục `start` đến sát chỉ mục `stop`
- Code mẫu cắt lát:
  ```python
  data_stream = (10, 20, 30, 40, 50)
  subset = data_stream[1:4] # Kết quả: (20, 30, 40)
  ```

## Ứng dụng Bản ghi tĩnh
- Dữ liệu cấu hình: Lưu trữ hằng số ứng dụng, cấu hình server tĩnh
- Tọa độ bản đồ: Lưu trữ tọa độ GPS (Latitude, Longitude) không thay đổi
- Thông tin định danh: Lưu trữ cặp kết nối đặc thù như Host và Port
```
```
```