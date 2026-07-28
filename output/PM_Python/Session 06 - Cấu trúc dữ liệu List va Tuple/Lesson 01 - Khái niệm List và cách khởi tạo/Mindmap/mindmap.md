```markmap
# Session 06: Khái niệm List và cách khởi tạo

## dynamic_array_nature
- Bản chất mảng động (Dynamic Array)
  - Quản lý bộ nhớ: Tự động thay đổi kích thước cơ cấu (Dynamic Resizing) khi thêm hoặc xóa phần tử
  - Cơ chế lưu trữ: Con trỏ tham chiếu (Pointer Array) trỏ tới các đối tượng lưu trữ tại vùng nhớ Heap
  - Cơ chế vận hành bộ nhớ
    - ![](../images/mindmap_img_1.png)

## list_initialization
- Cách khởi tạo Danh sách
  - Cú pháp cơ bản: Sử dụng cặp ngoặc vuông `[]` hoặc hàm dựng `list()`
  - Mã nguồn thực thi:
    ```python
    empty_list_1 = []
    empty_list_2 = list()
    scores = [8.5, 9.0, 7.5]
    ```

## heterogeneous_data_pep8
- Đặc tính đa kiểu dữ liệu (Heterogeneous)
  - Lưu trữ đa dạng: Cho phép chứa đồng thời `str`, `int`, `float`, `bool`
  - Quy chuẩn PEP 8: Sử dụng dấu phẩy kèm một khoảng trắng sau mỗi phần tử để tăng cấu trúc trực quan
  - Mã nguồn thực thi:
    ```python
    student_profile = ["Alice", 18, 8.5, 9.0, 7.5, True]
    ```

## list_indexing
- Đánh chỉ mục (Indexing) & Xử lý tuần tự
  - Cơ chế chỉ mục: Chỉ mục dương chạy từ trái sang (0 đến n-1), Chỉ mục âm chạy từ phải sang (-1 đến -n)
  - Xử lý tuần tự (Tính toán): Truy xuất phần tử qua index để tính tổng và điểm trung bình
  - Mã nguồn thực thi:
    ```python
    math_score = student_profile[2]       # Lay 8.5 (chi muc duong)
    physics_score = student_profile[3]    # Lay 9.0 (chi muc duong)
    chemistry_score = student_profile[-2] # Lay 7.5 (chi muc am)
    total_score = math_score + physics_score + chemistry_score
    average_score = total_score / 3
    ```

## syntax_troubleshooting
- Nhận diện & Khắc phục lỗi cú pháp
  - Lỗi IndexError: Truy cập chỉ mục nằm ngoài phạm vi độ dài của List
  - Lỗi SyntaxError do thiếu dấu phẩy: Thiếu dấu phẩy phân tách các phần tử
  - Lỗi TypeError do sai cặp ngoặc: Nhầm lẫn dùng ngoặc tròn `()` tạo thành Tuple không thể chỉnh sửa dữ liệu
  - Mã nguồn lỗi thường gặp:
    ```python
    # Han che 1: IndexError
    # student_profile[10] -> Loi vuot qua khoang chi muc ban dau

    # Han che 2: SyntaxError
    # bad_list = [8.5  9.0  7.5] -> Thieu dau phay thong bao loi

    # Han che 3: TypeError
    # read_only_tuple = ("Alice", 18) -> Khong phai List
    ```
```
```
```