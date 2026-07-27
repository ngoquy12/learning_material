```markmap
# Session 05 - Lesson 03: String methods

## String Immutability
- Bản chất: Chuỗi trong Python là bất biến, không thể sửa đổi giá trị vùng nhớ tại chỗ
  - ![](../images/mindmap_img_1.png)
- Gotcha: Gọi phương thức nhưng không gán lại giá trị sẽ mất kết quả biến đổi
  - Minh họa lập trình:
    ```python
    # Sai: Giá trị không thay đổi
    user_address = "  hanoi  "
    user_address.strip()

    # Đúng: Gán lại hoặc lưu vào biến mới
    user_address = user_address.strip()
    ```

## Input Normalization
- Phương thức: upper(), lower(), strip()
  - upper(): Chuyển đổi toàn bộ ký tự sang dạng viết hoa
  - lower(): Chuyển đổi toàn bộ ký tự sang dạng viết thường
  - strip(): Loại bỏ tất cả khoảng trắng dư thừa ở hai đầu chuỗi
- Gotcha: AttributeError xảy ra khi gọi các phương thức này trên kiểu dữ liệu không phải chuỗi như NoneType hoặc int
  - Minh họa lập trình:
    ```python
    raw_input = "  Rikkei_EDU  "
    clean_lower = raw_input.strip().lower()
    ```

## Text Division and Assembly
- split(separator): Chia chuỗi thành một danh sách các chuỗi con dựa vào ký tự phân tách
  - Gotcha: Nếu separator không tồn tại trong chuỗi gốc, trả về list chứa duy nhất một phần tử là chuỗi ban đầu
  - Ví dụ: `"abc-def".split(",")` trả về `["abc-def"]`
- join(iterable): Liên kết danh sách các chuỗi thành một chuỗi duy nhất bằng ký tự nối
  - Gotcha: TypeError xảy ra nếu danh sách liên kết chứa bất kỳ phần tử nào khác kiểu chuỗi
  - Minh họa lập trình:
    ```python
    # Gây ra lỗi TypeError tại runtime
    invalid_list = ["phone", 908, 112]
    joined_data = "-".join(invalid_list)
    ```

## Substring Replacement
- replace(old, new): Tìm kiếm và thay thế tất cả chuỗi con cũ bằng chuỗi con mới
- Cơ chế: Tạo ra một chuỗi mới chứa giá trị được thay thế, không tác động lên chuỗi gốc
- Gotcha: Nếu không tìm thấy chuỗi cần thay thế, Python trả về bản sao chuỗi gốc mà không báo lỗi
  - Minh họa lập trình:
    ```python
    domain = "rikkei.vn"
    normalized = domain.replace(".vn", ".edu.vn")
    ```

## Sanitization Pipeline
- Nguyên lý: Ghép chuỗi lệnh (Method Chaining) để tối ưu và tinh gọn luồng làm sạch dữ liệu đầu vào
  - ![](../images/mindmap_img_2.png)
- Minh họa lập trình:
  ```python
  raw_data = "  john_doe_RIKKEI@Rikkei.VN  "
  cleaned = raw_data.strip().lower()
  parts = cleaned.split("@")
  normalized_domain = parts[1].replace(".vn", ".edu.vn")
  final_email = "@".join([parts[0], normalized_domain])
  ```
```
```
```