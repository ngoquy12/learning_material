```markmap
# Session 08 - Lesson 01: Giới thiệu hàm và cách định nghĩa

## Định nghĩa hàm với từ khóa def
- Cú pháp cơ bản
  - Khai báo bằng từ khóa def, tên hàm, cặp ngoặc đơn chứa tham số và dấu hai chấm
  - Khối lệnh bên trong bắt buộc phải lùi đầu dòng (Indentation)
  - ```python
    def greet_user(username):
        """Docstring: Hien thi loi chao."""
        print("Xin chao " + username)
    ```
- Quy tắc đặt tên hàm
  - Sử dụng cú pháp snake_case (chữ thường, phân tách bằng dấu gạch dưới)
  - Nên bắt đầu bằng động từ thể hiện hành động thực thi
- Khái niệm Docstring
  - Chuỗi văn bản đặt ngay dưới def để giải thích chức năng, được bọc trong bộ ba dấu nháy kép

## Tham số và đối số (Parameters vs Arguments)
- Phân biệt khái niệm
  - Tham số (Parameters): Các biến được khai báo trong cặp ngoặc đơn của định nghĩa hàm
  - Đối số (Arguments): Các giá trị thực tế truyền vào hàm khi gọi thực thi
- Trình tự truyền đối số
  - Truyền theo vị trí mặc định (Positional arguments) từ trái qua phải
- ![](../images/mindmap_img_1.png)
- Lỗi thời gian chạy (Runtime error)
  - `TypeError`: Xảy ra khi số lượng đối số truyền vào không khớp với số lượng tham số khai báo

## Từ khóa return và giá trị trả về
- Chức năng của return
  - Dừng thực thi hàm ngay lập tức và chuyển quyền điều khiển kèm dữ liệu về nơi gọi hàm
- Trường hợp không khai báo return
  - Python tự động trả về giá trị None
- ```python
  def calculate_sum(a, b):
      return a + b
  result = calculate_sum(5, 10)
  ```

## Tái sử dụng mã nguồn và Nguyên lý DRY
- Nguyên lý DRY (Don't Repeat Yourself)
  - Đóng gói các đoạn mã lặp lại nhiều lần vào một hàm duy nhất để giảm thiểu trùng lặp logic
- Lợi ích thực tiễn
  - Rút ngắn số lượng dòng mã nguồn
  - Cho phép cập nhật và bảo trì logic nghiệp vụ tại một nơi duy nhất
  - Dễ dàng Debug lỗi phát sinh

## Xử lý cấu trúc dữ liệu trong hàm
- Truyền nhận đối tượng phức tạp
  - Hàm có thể nhận đầu vào là List, Tuple, Dictionary và trả về cấu trúc dữ liệu tương ứng
- Minh họa xử lý danh sách và từ điển
  - ```python
    def filter_employees_by_skill(employees_list, target_skill):
        filtered_result = []
        for employee in employees_list:
            if target_skill in employee["skills"]:
                filtered_result.append(employee["name"])
        return filtered_result
    ```
- ![](../images/mindmap_img_2.png)

## Phạm vi của biến (Variable Scope)
- Biến cục bộ (Local Scope)
  - Khai báo bên trong hàm, chỉ có hiệu lực và truy cập được bên trong hàm đó
  - Tự động giải phóng khỏi bộ nhớ khi hàm kết thúc thực thi
  - Lỗi `NameError`: Xảy ra khi cố gắng gọi biến cục bộ từ bên ngoài hàm
- Biến toàn cục (Global Scope)
  - Khai báo ngoài hàm, có thể đọc dữ liệu ở mọi nơi trong chương trình
  - Lỗi `UnboundLocalError`: Xảy ra khi cố gắng thay đổi giá trị biến global trong hàm mà không dùng từ khóa global

## Phối hợp các hàm (Modular Programming)
- Nguyên tắc đơn nhiệm (Single Responsibility Principle)
  - Mỗi hàm được thiết kế để chỉ thực hiện một tác vụ nghiệp vụ duy nhất
- Kỹ thuật khớp nối (Chaining functions)
  - Kết quả trả về của hàm này được sử dụng làm đối số đầu vào cho hàm khác
  - ```python
    def get_raw_input():
        return "  Python Developer  "
    def clean_data(text):
        return text.strip()
    clean_text = clean_data(get_raw_input())
    ```
```
```
```