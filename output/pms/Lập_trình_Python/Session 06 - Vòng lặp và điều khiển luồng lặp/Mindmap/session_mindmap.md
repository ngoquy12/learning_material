```markmap
# Vòng lặp và điều khiển luồng lặp

## Mục tiêu bài học
- Làm chủ câu lệnh for và hàm range để duyệt dãy số xác định
- Xây dựng vòng lặp while kiểm soát luồng theo điều kiện linh hoạt
- Phối hợp break, continue và else để tối ưu luồng thực thi
- Phòng tránh các bẫy hiệu năng như off-by-one và vòng lặp vô hạn

## Đặt tình huống
- Hệ thống tài chính cần tự động hóa các tác vụ lặp đi lặp lại
- Gửi thông báo định kỳ, tính lãi tích lũy, thử lại kết nối thanh toán
- Cần cơ chế kiểm soát lượt lặp chính xác và tối ưu tài nguyên

## Vòng lặp for và hàm range
### Khái niệm
- Duyệt qua chuỗi số hoặc tập hợp với số lần biết trước
### Cú pháp
```python
for index in range(start, stop):
    # Khối lệnh thực thi thụt lề 4 khoảng trắng
```
### Ứng dụng thực tế
- Tính tiền lãi tiết kiệm hàng tháng hoặc gửi thông báo nhắc nợ
### Cơ chế range
![](../images/mindmap_img_1.png)
### Lỗi off-by-one
- Giá trị stop trong range không bao gồm chính nó
- Dùng range(1, 5) chỉ lặp 4 lần, gây thiếu lượt xử lý

## Vòng lặp while và điều kiện dừng
### Cơ chế while
- Lặp lại khối lệnh khi biểu thức điều kiện còn True
### Cú pháp
```python
while condition:
    # Khối lệnh lặp
    # Cập nhật biến điều kiện
```
### Ứng dụng thực tế
- Tích lũy số dư tài khoản đến khi đủ điều kiện thanh toán
### Vòng lặp vô hạn
- Quên cập nhật biến điều kiện làm cho biểu thức luôn True
- Gây treo chương trình và chiếm dụng 100% tài nguyên CPU

## Điều khiển luồng lặp với break, continue và else
### Cơ chế break và continue
- break dừng và thoát khỏi vòng lặp ngay lập tức
- continue bỏ qua phần còn lại và sang lượt lặp tiếp theo
### Khối lệnh else
- Khối else chạy khi vòng lặp kết thúc bình thường mà không bị break
### Luồng điều khiển
![](../images/mindmap_img_2.png)
### Quy tắc tối ưu
- Thay thế cờ hiệu rườm rà bằng câu lệnh break và continue
- Phẳng hóa cấu trúc mã nguồn giúp tăng tốc độ đọc và bảo trì
```