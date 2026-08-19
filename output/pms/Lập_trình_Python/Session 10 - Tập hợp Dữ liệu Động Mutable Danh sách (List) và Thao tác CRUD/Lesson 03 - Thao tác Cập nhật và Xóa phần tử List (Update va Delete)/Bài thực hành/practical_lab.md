# Bài thực hành: Cập nhật và Xóa phần tử trong Giỏ hàng E-commerce

## 1. Mục tiêu bài học
- Vận dụng môi trường Python 3.12, virtualenv và trình soạn thảo Cursor/Windsurf AI IDE tuân thủ quy chuẩn PEP 8 và Type Hints để xử lý dữ liệu kiểu List.
- Thành thạo các thao tác cập nhật giá trị phần tử qua chỉ số và xóa phần tử an toàn sử dụng pop(), remove(), del, clear().
- Áp dụng các phương thức biến đổi danh sách in-place như sort(), reverse(), hàm len() và xử lý triệt để các lỗi thường gặp như ValueError, IndexError.

## 2. Yêu cầu bài toán
Trong hệ thống thương mại điện tử, việc quản lý giỏ hàng đòi hỏi xử lý linh hoạt danh sách sản phẩm và giá cả tương ứng. Hãy viết chương trình Python 3.12 để quản lý giỏ hàng với các yêu cầu logic cụ thể như sau:
1. Khởi tạo danh sách sản phẩm cart_items (list[str]) và danh sách giá tương ứng cart_prices (list[int]). Khai báo Type Hints đầy đủ.
2. Cập nhật thông tin tên và giá của sản phẩm tại một chỉ số vị trí chỉ định (kiểm tra ranh giới danh sách trước khi gán để tránh IndexError).
3. Lọc bỏ các sản phẩm không hợp lệ (có giá bằng 0) bằng cách duyệt ngược danh sách từ cuối về đầu và sử dụng phương thức pop() để đảm bảo tính an toàn cho chỉ số danh sách.
4. Thực hiện xóa một sản phẩm cụ thể dựa theo tên sản phẩm bằng phương thức remove(), có sử dụng toán tử 'in' để kiểm tra trước nhằm tránh lỗi thường gặp ValueError.
5. Đảo ngược danh sách (reverse()) để ưu tiên sản phẩm mới thêm và dọn sạch hoàn toàn giỏ hàng sau khi hoàn tất thanh toán (clear()).

## 3. Các bước thực hiện
- **Tài nguyên đầu vào**: Môi trường phát triển Python 3.12, môi trường ảo virtualenv, công cụ Cursor/Windsurf AI IDE và tệp mã nguồn cart_manager.py tuân thủ chuẩn PEP 8 và Type Hints.

### Các bước thực hiện:
1. Bước 1: Khởi tạo môi trường ảo virtualenv, kích hoạt môi trường và tạo tệp mã nguồn cart_manager.py trên Cursor/Windsurf AI IDE.
2. Bước 2: Khai báo danh sách sản phẩm và giá tiền sử dụng Type Hints. Thực hiện thao tác cập nhật phần tử qua chỉ số an toàn.
3. Bước 3: Cài đặt vòng lặp duyệt ngược để lọc loại bỏ các mặt hàng giá 0 với pop(), sau đó thực hiện xóa theo tên bằng remove() kết hợp kiểm tra điều kiện tồn tại.
4. Bước 4: Sử dụng phương thức reverse() và clear() đúng quy cách in-place, chạy chương trình kiểm thử kết quả trên terminal.

## 4. Mã nguồn tham khảo (Code Demo)

```text
def process_cart() -> None:

# Khởi tạo danh sách sản phẩm và giá tương ứng với Type Hints (Python 3.12)
    cart_items: list[str] = [
        "Laptop Pro",
        "Tai nghe hỏng",
        "Bàn phím cơ",
        "Quà tặng hết hàng",
        "Màn hình 4K",
    ]
    cart_prices: list[int] = [1500, 0, 85, 0, 400]

    print(f"Tổng số sản phẩm ban đầu: {len(cart_items)}")

# 1. Cập nhật sản phẩm tại chỉ số 0 (Đổi phiên bản sản phẩm và điều chỉnh giá)
    update_index: int = 0
    if update_index < len(cart_items):
        cart_items[update_index] = "Laptop Pro M2"
        cart_prices[update_index] = 1600
        print(f"Đã cập nhật sản phẩm tại chỉ số {update_index}: {cart_items[update_index]}")
    else:
        print(f"Lỗi: Chỉ số {update_index} vượt quá phạm vi danh sách.")

# 2. Duyệt ngược danh sách từ cuối về đầu để xóa an toàn sản phẩm có giá bằng 0
    i: int = len(cart_prices) - 1
    while i >= 0:
        if cart_prices[i] == 0:
            removed_item: str = cart_items.pop(i)
            cart_prices.pop(i)
            print(f"[CẢNH BÁO] Đã loại bỏ sản phẩm không hợp lệ: {removed_item}")
        i -= 1

# 3. Xóa an toàn một sản phẩm chỉ định bằng remove() có kiểm tra tồn tại bằng 'in'
    target_item: str = "Bàn phím cơ"
    if target_item in cart_items:
        target_index: int = cart_items.index(target_item)
        cart_items.remove(target_item)
        cart_prices.pop(target_index)
        print(f"Đã xóa thành công sản phẩm: {target_item}")
    else:
        print(f"Không tìm thấy {target_item} để xóa.")

# 4. Đảo ngược danh sách hiển thị (thao tác in-place)
    cart_items.reverse()
    cart_prices.reverse()

    print("\n--- THÔNG TIN GIỎ HÀNG XÁC NHẬN ---")
    print("Sản phẩm:", cart_items)
    print("Đơn giá tương ứng:", cart_prices)
    print("Số lượng mặt hàng thanh toán:", len(cart_items))

# 5. Dọn dẹp giỏ hàng sau khi hoàn tất thanh toán thành công
    cart_items.clear()
    cart_prices.clear()

    print("\nTrạng thái giỏ hàng sau thanh toán:")
    print("Mặt hàng:", cart_items)
    print("Đơn giá:", cart_prices)


if __name__ == "__main__":
    process_cart()
```

# 5. Checklist đánh giá kết quả
- [ ] Khởi tạo thành công môi trường ảo virtualenv và quản lý tệp trên Cursor/Windsurf AI IDE.
- [ ] Khai báo chuẩn xác Type Hints (list[str], list[int]) và tuân thủ quy tắc định dạng mã nguồn PEP 8.
- [ ] Thực hiện cập nhật giá trị phần tử qua chỉ số có kiểm tra phạm vi để phòng tránh IndexError.
- [ ] Áp dụng thành công thuật toán duyệt ngược để loại bỏ phần tử bằng pop() mà không làm lệch chỉ số.
- [ ] Sử dụng toán tử 'in' trước khi gọi phương thức remove() để xử lý lỗi thường gặp ValueError.
- [ ] Sử dụng đúng các phương thức biến đổi in-place như reverse() và clear() mà không mắc lỗi gán biến nhận giá trị None.
