```markmap
# Cấu trúc dữ liệu List và Tuple

## Mục tiêu bài học
- Thao tác thành thạo truy cập Index, Cắt lát Slicing và Cập nhật List
- Nắm vững tính bất biến Immutability của Tuple trong Python
- Ứng dụng kỹ thuật Tuple Unpacking và Swap hoán đổi giá trị
- Phân biệt bản chất List và Tuple để lựa chọn cấu trúc dữ liệu tối ưu

## Đặt tình huống
- Quản lý nhật ký phiên làm việc và tọa độ GPS cố định hệ thống
- Rủi ro ghi đè nhầm cấu hình hệ thống gây lỗi dừng đột ngột
- Đặt ra nhu cầu kết hợp danh sách động linh hoạt và bộ dữ liệu cố định

## Thao tác cơ bản trên List
### Khởi tạo và Truy cập Index
- Tạo danh sách chứa nhiều dữ liệu và lấy phần tử theo Index
  ```python
  session_log = [5001, 5002, 5003, 5004]
  first_session = session_log[0]
  ```
### Cập nhật giá trị List
- Thay đổi trực tiếp nội dung phần tử thông qua vị trí Index
  ```python
  session_log[0] = 9999
  ```
### Kỹ thuật Cắt lát Slicing
- Trích xuất phân đoạn danh sách mới theo chỉ số `[start:end]`
  ```python
  sub_log = session_log[1:3]
  ```

## Cấu trúc Tuple và Tính bất biến
### Khởi tạo và Bảo vệ dữ liệu
- Tuple lưu trữ tập hợp dữ liệu cố định không thể sửa đổi
  ```python
  geo_location = (10.76262, 106.66017)
  ```
### Giải nén dữ liệu Unpacking
- Trích xuất trực tiếp các phần tử Tuple vào từng biến riêng lẻ
  ```python
  latitude, longitude = geo_location
  ```
### Kỹ thuật Swap biến trực tiếp
- Tráo đổi giá trị hai biến tối ưu không dùng biến trung gian
  ```python
  latitude, longitude = longitude, latitude
  ```
### Luồng hoạt động cơ chế


## So sánh và Lưu ý vận hành
### So sánh List vs Tuple
- List dùng cho dữ liệu động, hỗ trợ thêm xóa sửa
- Tuple dùng cho cấu hình cố định, tối ưu tốc độ và bộ nhớ
### Sự cố TypeError
- Cố tình sửa phần tử Tuple khiến chương trình dừng đột ngột
  ```python
  # Lỗi TypeError: 'tuple' object does not support item assignment
  geo_location[0] = 10.80000
  ```
### Kỹ thuật nên tránh
- Không sử dụng biến trung gian `temp` khi thực hiện tráo đổi biến
### Kỹ thuật đề xuất
- Kết hợp Unpacking và Slicing để khởi tạo lại dữ liệu mới
  ```python
  updated_geo = (lat, lng)
  ```
```