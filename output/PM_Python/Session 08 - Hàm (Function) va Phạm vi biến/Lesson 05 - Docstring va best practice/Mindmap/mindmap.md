```markmap
# Session 08: Docstring & Best Practice (PEP 257)

## docstring_definition
- Bản chất: Chuỗi ký tự đặt ngay sau định nghĩa module, class, function để tài liệu hóa mã nguồn
- Cơ chế Runtime: Python tự biên dịch thành thuộc tính __doc__ của đối tượng
- Đoạn mã mẫu:
  ```python
  def greet():
      """Greet the user."""
      pass
  print(greet.__doc__)
  ```
- Cách truy cập: Sử dụng hàm help(object) hoặc truy xuất trực tiếp thuộc tính object.__doc__
- Cảnh báo lỗi: Lỗi AttributeError xảy ra nếu cố truy cập __doc__ trên instance không hỗ trợ hoặc biến không định nghĩa tài liệu
- ![](../images/mindmap_img_1.png)

## docstring_vs_comment
- Comment (#):
  - Mục đích: Giải thích thuật toán phức tạp hoặc luồng code cho lập trình viên bảo trì
  - Runtime: Bị trình thông dịch bỏ qua hoàn toàn khi chạy chương trình
- Docstring ("""..."""):
  - Mục đích: Giải thích giao diện sử dụng (API) phục vụ cho người dùng hàm/thư viện
  - Runtime: Tồn tại trong RAM dưới dạng đối tượng chuỗi để công cụ tạo tài liệu tự động trích xuất

## pep_257
- Định nghĩa: Quy chuẩn hướng dẫn chuẩn hóa cấu trúc và ngữ nghĩa của Python Docstrings
- Quy tắc bắt buộc: Luôn sử dụng cặp ba dấu nháy kép """ ngay cả với chuỗi một dòng, không dùng ''' hay #
- Quản lý đồng bộ: Cập nhật nội dung Docstring ngay khi sửa đổi cấu trúc đầu vào hoặc đầu ra của hàm

## one_line_docstrings
- Cấu trúc: Mô tả ngắn gọn viết trên một dòng duy nhất, kết thúc bằng dấu chấm và ngoặc kép đóng/mở cùng hàng
- Nội dung: Dùng câu mệnh lệnh với động từ nguyên mẫu mô tả đích danh hành động của hàm
- Đoạn mã mẫu:
  ```python
  def square(number):
      """Return the square of a number."""
      return number ** 2
  ```

## multi_line_docstrings
- Cấu trúc: Dòng tóm tắt ngắn (one-line summary) -> Dòng trống -> Mô tả các tham số, giá trị trả về và ngoại lệ phát sinh
- Ràng buộc căn lề: Khối Docstring nhiều dòng phải thụt lề (Indentation) đồng nhất với các câu lệnh bên dưới hàm
- Đoạn mã mẫu:
  ```python
  def divide(a, b):
      """Divide two numbers and return the float result.

      Parameters:
      a (float): The numerator.
      b (float): The denominator (must not be zero).

      Returns:
      float: The quotient result.
      """
      return a / b
  ```
- Cảnh báo lỗi: Lỗi IndentationError xảy ra khi dòng đóng nháy kép hoặc các dòng mô tả lệch hàng so với cấu trúc hàm

## pep_8_and_pep_257_alignment
- Mục tiêu: Đảm bảo cú pháp định dạng mã nguồn (PEP 8) nhất quán với tài liệu hướng dẫn (PEP 257)
- Vị trí ở cấp Module: Docstring của Module phải đặt đầu tệp nguồn, trước mọi import và các khai báo biến toàn cục
- Quy tắc mô tả tối giản: Không lặp lại thông tin khai báo hàm ở dòng tóm tắt nhằm tránh dư thừa thông tin
```
```
```