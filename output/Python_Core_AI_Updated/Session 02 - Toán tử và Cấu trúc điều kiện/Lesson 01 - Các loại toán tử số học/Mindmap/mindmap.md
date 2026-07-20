```markmap
# Session 02: Các loại toán tử số học

## Mục tiêu bài học
- Hiểu và áp dụng thành thạo các toán tử số học cơ bản và nâng cao trong Python.
- Thực hiện đúng thứ tự ưu tiên của các phép toán để tránh sai sót logic.
- Nhận biết và xử lý các lỗi thường gặp như chia cho 0 hoặc lỗi kiểu dữ liệu từ input.

## Toán tử số học cơ bản
### Khái niệm cốt lõi
- Các phép tính cơ bản bao gồm cộng (+), trừ (-), nhân (*) và lũy thừa (**), được sử dụng để thực hiện tính toán trên các kiểu dữ liệu số.
### Cú pháp & Cách khai báo
- Ví dụ:
  ```python
  a = 17
  b = 5
  tong = a + b
  hieu = a - b
  tich = a * b
  luy_thua = b ** 2
  ```
### Lưu ý thực chiến
- Toán tử lũy thừa (**) có độ ưu tiên cao hơn các toán tử nhân và chia thông thường.

## Phép chia thông thường (/)
### Khái niệm cốt lõi
- Phép chia thông thường (/) thực hiện chia hai số và luôn trả về kết quả dưới dạng số thực (float), ngay cả khi hai số chia hết cho nhau.
### Cú pháp & Cách khai báo
- Ví dụ:
  ```python
  thuong_thuc = 17 / 5
  ```
### Lưu ý thực chiến
- Kết quả nhận được luôn có kiểu dữ liệu là float. Gây ra lỗi ZeroDivisionError nếu chia cho số 0.

## Phép chia lấy nguyên (//)
### Khái niệm cốt lõi
- Phép chia lấy nguyên (//) chia phần trị số và làm tròn xuống số nguyên lớn nhất nhỏ hơn hoặc bằng kết quả thực tế.
### Cú pháp & Cách khai báo
- Ví dụ:
  ```python
  thuong_nguyen = 17 // 5
  ```
### Lưu ý thực chiến
- Nếu một trong hai toán hạng là kiểu số thực (float), kết quả trả về sẽ là một số thực làm tròn (ví dụ: 17.0 // 5 cho ra 3.0). Tránh chia cho 0 để ngăn ZeroDivisionError.

## Phép chia lấy dư (%)
### Khái niệm cốt lõi
- Phép chia lấy dư (%) thực hiện phép chia và trả về phần dư còn lại của phép chia đó.
### Cú pháp & Cách khai báo
- Ví dụ:
  ```python
  so_du = 17 % 5
  ```
### Lưu ý thực chiến
- Thường dùng để kiểm tra tính chẵn lẻ của một số (chia dư cho 2) hoặc tính chia hết. Gây lỗi chia cho 0 nếu số chia là 0.

## Thứ tự ưu tiên toán tử
### Khái niệm cốt lõi
- Độ ưu tiên sắp xếp từ cao xuống thấp: Ngoặc đơn () -> Lũy thừa (**) -> Nhân, chia, chia nguyên, chia dư (*, /, //, %) -> Cộng, trừ (+, -).
- ![](../images/mindmap_img_1.png)
### Cú pháp & Cách khai báo
- Ví dụ:
  ```python
  ket_qua = (17 + 5) * 2 ** 3
  ```
### Lưu ý thực chiến
- Luôn sử dụng dấu ngoặc đơn () để chỉ định rõ ràng thứ tự tính toán mong muốn, giúp tránh lỗi logic và làm mã nguồn dễ đọc hơn.

## Hàm input và chuyển đổi dữ liệu
### Khái niệm cốt lõi
- Hàm input() nhận dữ liệu từ bàn phím dưới dạng chuỗi (str). Cần ép kiểu dữ liệu sang int hoặc float trước khi thực hiện các phép toán số học.
### Cú pháp & Cách khai báo
- Ví dụ:
  ```python
  a = int(input())
  b = float(input())
  ```
### Lưu ý thực chiến
- Quên ép kiểu sẽ gây ra lỗi TypeError vì không thể thực hiện phép toán số học giữa chuỗi và số.
```
```
```