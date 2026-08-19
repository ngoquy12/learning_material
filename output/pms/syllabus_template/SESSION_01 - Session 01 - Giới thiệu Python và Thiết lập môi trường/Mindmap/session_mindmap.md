```markmap

# Giới thiệu Python và Thiết lập môi trường

## Lesson 01 — Tổng quan Python và Thiết lập môi trường

### Khái niệm & Vai trò
- Định nghĩa ngắn gọn: Ngôn ngữ lập trình bậc cao, thông dịch, cú pháp tối giản.
- Vai trò: Phát triển phần mềm, xử lý dữ liệu và tự động hóa quy trình.

### Cú pháp & Giải nghĩa
- Cú pháp kiểm tra môi trường:
```

bash
  python --version

```- Giải thích thành phần:
  - `python`: Trình thông dịch Python được cài đặt trong hệ thống.
  - `--version`: Cờ lệnh truy vấn thông tin phiên bản môi trường.

### Ví dụ thực hành
- Kịch bản áp dụng: Khởi chạy chương trình và kiểm tra thông số hệ thống.
```

python
  system_name = "Rikkei POS System"
  system_version = "1.0.0"
  print(f"Khởi động {system_name} - Phiên bản {system_version}")

```- Giải thích ví dụ: Trình thông dịch thực thi từ trên xuống, gán chuỗi và xuất thông báo.

### Lưu ý triển khai
- **Lỗi đường dẫn biến môi trường**: Trình thông dịch không thể gọi từ Terminal nếu chưa thêm vào PATH.
- **Lưu ý định dạng**: Tuân thủ quy chuẩn PEP 8 về đặt tên tệp mã nguồn bằng `snake_case`.

## Lesson 02 — Khai báo biến và Nhập xuất dữ liệu

### Khái niệm & Vai trò
- Định nghĩa ngắn gọn: Vùng lưu trữ dữ liệu và các hàm tương tác đầu vào/đầu ra.
- Vai trò: Thu thập dữ liệu người dùng, tính toán nghiệp vụ và hiển thị kết quả.

### Cú pháp & Giải nghĩa
- Khai báo cú pháp chuẩn:
```

python
  variable_name = input("Prompt string")
  formatted_output = f"Text {variable_name}"

```- Giải thích thành phần:
  - `variable_name`: Tên biến lưu giữ dữ liệu nhập từ bàn phím.
  - `input()`: Hàm tạm dừng chương trình để nhận dữ liệu chuỗi.
  - `f"..."`: Cú pháp f-string nhúng biến trực tiếp vào chuỗi.

### Ví dụ thực hành
- Kịch bản áp dụng: Nhập thông tin bán hàng, chuyển đổi kiểu dữ liệu và tính tiền.
```

python
  item_name = input("Nhập tên sản phẩm: ")
  unit_price = float(input("Nhập đơn giá: "))
  quantity = int(input("Nhập số lượng: "))
  total_payment = unit_price * quantity
  print(f"Sản phẩm: {item_name} | Tổng tiền: {total_payment:,.0f} VNĐ")

```- Giải thích ví dụ: Chuyển chuỗi từ `input()` sang `float`/`int` để thực hiện phép tính nhân.
- Minh họa luồng dữ liệu xử lý hóa đơn:
  -

### Lưu ý triển khai
- **Lỗi ép kiểu dữ liệu**: Chương trình phát sinh lỗi `ValueError` nếu ép chuỗi văn bản sang số.
- **Lưu ý định dạng**: Đặt tên biến dạng `snake_case` thể hiện rõ bản chất danh từ nghiệp vụ.

## Liên kết hệ thống
- Mối quan hệ logic: Lesson 01 cung cấp môi trường thực thi để Lesson 02 khai báo biến và xử lý logic.
- Luồng dữ liệu xuyên suốt: Môi trường Runtime (L01) -> Nhận chuỗi `input()` (L02) -> Ép kiểu và tính toán (L02) -> Xuất kết quả `print()` (L02).
- Ứng dụng tổng hợp: Xây dựng ứng dụng dòng lệnh tương tác hoàn chỉnh trên môi trường Python chuẩn hóa.
```
