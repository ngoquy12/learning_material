```markmap
# Môi trường Python 3.12 và Cú pháp cơ bản

## Mục tiêu bài học
- Cài đặt thành công Python 3.12 và cấu hình môi trường làm việc.
- Nắm vững cú pháp khai báo biến và quy tắc đặt tên snake_case.
- Thành thạo nhập xuất dữ liệu console với input() và print().
- Thực hiện ép kiểu dữ liệu an toàn phục vụ tính toán tài chính.

## Đặt tình huống
- Xây dựng module phần mềm thu ngân tính hóa đơn bán hàng.
- Dữ liệu nhập từ bàn phím mặc định là chuỗi văn bản.
- Phép cộng chuỗi gây sai số tài chính nghiêm trọng ("20000" + "3" = "200003").
- Yêu cầu ép kiểu số chính xác và định dạng hiển thị hóa đơn chuẩn.

## Cài đặt và Môi trường Python 3.12
### Cấu hình môi trường
- Tải bản Python 3.12 chính thức từ python.org
- Tích chọn Add python.exe to PATH khi cài đặt
### Chế độ thực thi
- Chế độ REPL: Chạy trực tiếp từng dòng lệnh trên terminal
- Chế độ Script: Lưu file .py và thực thi bằng Python Runner
### Minh họa luồng biên dịch
![](../images/mindmap_img_1.png)

## Cú pháp cơ bản và Biến
### Quy tắc định danh
- Phân biệt chữ hoa chữ thường
- Sử dụng chuẩn đặt tên snake_case cho biến
- Không bắt đầu bằng số hoặc chứa từ khóa hệ thống
### Cú pháp khai báo
```python
unit_price = 15000.5
quantity = 4
```
### Kiểu dữ liệu cơ sở
- int: Kiểu số nguyên (ví dụ: 4, 100)
- float: Kiểu số thực (ví dụ: 15000.5, 3.14)
- str: Kiểu chuỗi văn bản (ví dụ: "Hóa đơn")
- bool: Kiểu logic (True hoặc False)

## Nhập xuất console và Ép kiểu dữ liệu
### Hàm nhập input()
- Nhận dữ liệu nhập từ bàn phím của người dùng
- Dữ liệu trả về luôn ở dạng chuỗi str
### Ép kiểu dữ liệu
- Chuyển chuỗi sang số thực với float()
- Chuyển chuỗi sang số nguyên với int()
```python
price = float(input("Nhập đơn giá: "))
quantity = int(input("Nhập số lượng: "))
total = price * quantity
```
### Minh họa luồng Ép kiểu vs Ghép chuỗi
*Prompt tạo ảnh: A clean 2D flat vector technical illustration comparing raw string output bug vs explicit type casting logic. Left side titled 'Sai lầm: Phép cộng chuỗi' showing input string '20000' + '3' resulting in string '200003'. Right side titled 'Đúng chuẩn: Ép kiểu float và int' showing float('20000') * int('3') resulting in numerical result 60000.0. Main title in meaningful concise Accented Vietnamese 'So sánh Ép kiểu số học vs Cộng chuỗi văn bản'. Strictly NO text emojis (never use emoji characters like ❌, ✅, ⚠️, 🔴, 🟢, ▶). Only use clean 2D flat vector icons, symbols, and Phosphor-style vector graphics. 16:9 aspect ratio, spacious layout with at least 32px safe outer margin on all sides. Code snippets enclosed inside clean IDE editor window cards with 3 window dots at top left, using crisp monospace font. Sequential numbers in code examples follow strict logical sequence (1, 2, 3). Each status badge appears EXACTLY ONCE at the bottom of its panel (never duplicate badges). Rich in technical detail: concrete numeric values, color-coded red for warning string concatenation and emerald green for math casting, inline annotations on arrows. Standard diagram geometry: diamond for condition check, rectangles for calculations. Solid lines for control flow. Minimalist infographics style, clean white background, muted corporate color palette (navy blue, slate gray, soft emerald for correct path, subtle rose red for bug path). Clean sans-serif font, no 3D elements, no glowing neon effects. All labels in Sentence Case or Title Case (NEVER ALL CAPS).*
### Định dạng xuất print()
- Tham số sep: Quy định ký tự phân cách các giá trị
- Tham số end: Quy định ký tự kết thúc chuỗi xuất
```python
print("HÓA ĐƠN", "SIÊU THỊ", sep=" - ")
print("Tổng chi phí:", total, end=" VNĐ\n")
```
### Cảnh báo thực chiến
- Ép chuỗi chữ không hợp lệ sang số gây ValueError
- Không thực hiện nhân/cộng trực tiếp chuỗi chứa dữ liệu số
```