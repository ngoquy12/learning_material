```markmap
# Session 09 - Lesson 01: Các hàm xử lý chuỗi nâng cao

## regex_tong_quan
- Định nghĩa: Biểu thức chính quy (Regular Expression) xác định mẫu tìm kiếm (Search Pattern) cho chuỗi văn bản.
- Tiền tố Raw String `r`:
  - Bắt buộc dùng `r"pattern"` để ngăn Python xử lý ký tự thoát (escape character).
  - Tránh lỗi hiểu nhầm các chuỗi điều khiển như `\n`, `\t`, `\d`.
- Phòng ngừa lỗi runtime:
  - **TypeError**: Tránh truyền biến kiểu số (`int`) hoặc `None` vào hàm kiểm tra Regex (chỉ nhận String).
  - **re.error**: Xảy ra khi biểu thức sai cú pháp (thiếu ngoặc đóng `[]`, `()`).
- ![](../images/mindmap_img_1.png)

## ky_tu_neo_dau_cuoi
- Ký tự neo đầu `^`: Bắt buộc chuỗi cần so khớp phải bắt đầu bằng mẫu định nghĩa sau dấu `^`.
- Ký tự neo cuối `$`: Bắt buộc chuỗi cần so khớp phải kết thúc bằng mẫu định nghĩa trước dấu `$`.
- Tầm quan trọng:
  - Đảm bảo kiểm tra toàn bộ chuỗi (không cho phép khớp một phần nhỏ ở giữa).
  - Nếu thiếu ký tự neo, các chuỗi chứa mã độc hoặc dữ liệu rác ở hai đầu vẫn có thể được xác định là khớp.

## ky_tu_luong_hoa
- Ký tự chỉ số lượng xuất hiện (Quantifiers):
  - `*`: Xuất hiện từ 0 hoặc nhiều lần.
  - `+`: Xuất hiện từ 1 hoặc nhiều lần.
  - `?`: Xuất hiện 0 hoặc 1 lần (optional).
  - `{n}`: Xuất hiện chính xác n lần.
  - `{n, m}`: Xuất hiện từ n đến m lần.
- Lớp ký tự (Character Classes) thông dụng:
  - `\d`: Chữ số tương đương `[0-9]`.
  - `\w`: Ký tự chữ, số và dấu gạch dưới `[a-zA-Z0-9_]`.
  - `.`: Đại diện cho bất kỳ ký tự nào ngoại trừ ký tự xuống dòng.

## re_match_vs_re_search
- So sánh cơ chế hoạt động:
  - `re.match()`: Chỉ tìm kiếm từ ký tự đầu tiên của chuỗi target. Trả về `None` nếu ký tự đầu không khớp.
  - `re.search()`: Quét qua toàn bộ chuỗi target, trả về kết quả khớp đầu tiên tìm thấy.
  - `re.fullmatch()`: Yêu cầu toàn bộ chuỗi phải khớp chính xác 100% với biểu thức mẫu.
- Phòng ngừa lỗi AttributeError:
  - Kết quả trả về của hàm tìm kiếm có thể là `None` nếu không khớp.
  - Luôn kiểm tra điều kiện trước khi gọi phương thức `.group()` thu thập kết quả.
  - Ví dụ:
    ```python
    match = re.search(r"\d+", "Class 20")
    if match:
        print(match.group())
    ```

## regex_email_phone_pattern
- Mã nguồn kiểm định chuẩn:
  ```python
  import re

  def validate_user_email(email_address):
      email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
      return bool(re.fullmatch(email_pattern, email_address))

  def validate_vietnamese_phone(phone_number):
      phone_pattern = r"^0(3|5|7|8|9)\d{8}$"
      return bool(re.fullmatch(phone_pattern, phone_number))
  ```
- Giải cấu trúc Email Pattern:
  - `^[a-zA-Z0-9._%+-]+`: Bắt đầu với tên hộp thư dạng chữ, số hoặc ký tự cho phép.
  - `@[a-zA-Z0-9.-]+\.`: Phải chứa ký tự `@` và tên miền máy chủ kết thúc bằng dấu chấm `.`.
  - `[a-zA-Z]{2,}$`: Tên miền cấp cao nhất (TLD) có tối thiểu 2 ký tự chữ cái.
- Giải cấu trúc Phone Pattern:
  - `^0(3|5|7|8|9)`: Bắt đầu bằng số 0 và tiếp theo là đầu số nhà mạng chuẩn Việt Nam.
  - `\d{8}$`: Phần đuôi phải gồm đúng 8 chữ số, đảm bảo tổng chiều dài là 10 ký tự số.

## chuan_hoa_map_filter
- Chuỗi xử lý dữ liệu với map và filter:
  - `map()`: Thực hiện tiền xử lý, chuẩn hóa định dạng (loại bỏ khoảng trắng hai đầu bằng `.strip()`).
  - `filter()`: Sử dụng hàm lọc dựa trên Regex để giữ lại các bản ghi hợp lệ.
- Minh họa luồng Code:
  ```python
  import re
  raw_list = ["  user1@domain.com ", "invalid_email@", "0987654321"]
  # Lam sach ky tu trang o hai dau
  stripped = list(map(lambda s: s.strip(), raw_list))
  # Loc de lay danh sach email hop le
  email_pat = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
  valid_emails = list(filter(lambda s: re.fullmatch(email_pat, s), stripped))
  ```
- ![](../images/mindmap_img_2.png)
```
```
```