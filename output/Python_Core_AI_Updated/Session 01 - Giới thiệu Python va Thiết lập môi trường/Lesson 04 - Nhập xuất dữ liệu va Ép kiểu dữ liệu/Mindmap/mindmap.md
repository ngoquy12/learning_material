```markmap
# Session 01: Lesson 04 - Nhập xuất dữ liệu & Ép kiểu dữ liệu

## Mục tiêu bài học
- Sử dụng thành thạo hàm input để nhận dữ liệu và hàm print để hiển thị kết quả
- Thực hiện ép kiểu dữ liệu linh hoạt bằng int, float, str phục vụ tính toán số học
- Nhận diện và phòng tránh lỗi ValueError cùng các lỗi logic phổ biến khi xử lý dữ liệu đầu vào

## Hàm input()
### Khái niệm cốt lõi
- Hàm dùng để tạm dừng chương trình và nhận dữ liệu nhập vào từ bàn phím dưới dạng một chuỗi ký tự (string).
### Cú pháp & Cách khai báo
- Nhận dữ liệu chuỗi từ người dùng:
  ```python
  ten_nguoi_dung = input("Nhap ten cua ban: ")
  ```
### Lưu ý thực chiến
- Dữ liệu thu hồi từ input luôn có kiểu str. Nếu cần tính toán số học, bắt buộc phải thực hiện chuyển đổi kiểu dữ liệu.
- ![](../images/mindmap_img_1.png)

## Hàm print()
### Khái niệm cốt lõi
- Hàm xuất dữ liệu ra màn hình console, hỗ trợ in nhiều giá trị cùng lúc và tự động chuyển đổi các đối tượng sang chuỗi để hiển thị.
### Cú pháp & Cách khai báo
- Xuất nhiều giá trị đồng thời:
  ```python
  print("Kien thuc", "Python", 101)
  ```
### Lưu ý thực chiến
- Mặc định hàm tự động thêm ký tự xuống dòng ở cuối đầu ra, có thể tùy chỉnh thông qua tham số end để thay đổi hành vi mặc định.

## Ép kiểu dữ liệu (Type Casting)
### Khái niệm cốt lõi
- Quá trình chuyển đổi giá trị từ kiểu dữ liệu gốc sang kiểu dữ liệu đích như int, float, str để phục vụ các mục đích xử lý logic thích hợp.
### Cú pháp & Cách khai báo
- Chuyển đổi chuỗi chữ số thành số để thực hiện phép toán:
  ```python
  so_nguyen = int("25")
  so_thuc = float("10.5")
  tong = so_nguyen + so_thuc
  print("Tong gia tri:", tong)
  ```
### Lưu ý thực chiến
- Cảnh giác với lỗi logic nối chuỗi ngoài ý muốn khi thực hiện phép cộng (+) giữa hai giá trị nhận trực tiếp từ hàm input mà quên ép kiểu số.
- ![](../images/mindmap_img_2.png)

## Lỗi giá trị (ValueError) trong ép kiểu
### Khái niệm cốt lõi
- Lỗi phát sinh trong thời gian chạy (runtime) khi hàm ép kiểu nhận vào giá trị có định dạng không phù hợp để chuyển đổi sang kiểu dữ liệu đích.
### Cú pháp & Cách khai báo
- Các trường hợp điển hình gây ra lỗi ValueError:
  ```python
  # Loi do chuoi chua ky tu khong phai so
  so_nguyen_loi_1 = int("25a")

  # Loi do ep chuoi so thap phan truc tiep sang so nguyen
  so_nguyen_loi_2 = int("10.5")
  ```
### Lưu ý thực chiến
- Chỉ ép kiểu chuỗi sang int khi chuỗi đó chỉ chứa các chữ số nguyên. Đối với chuỗi chứa số thập phân, bắt buộc phải ép kiểu sang float trước.
```
```
```