## <center>[Vận dụng cơ bản 1] Sửa lỗi menu điều hướng đơn hàng thương mại điện tử</center>

### **1. Mục tiêu**
*   Nhận diện lỗi lệch kiểu dữ liệu (data type mismatch) giữa chuỗi ký tự nhận từ giao diện CLI và các giá trị số nguyên trong câu lệnh điều kiện `if/elif/else`.
*   Áp dụng kỹ thuật chuyển đổi kiểu dữ liệu an toàn và bọc xử lý ngoại lệ `ValueError` đối với dữ liệu người dùng nhập từ bàn phím.
*   Củng cố nguyên lý xây dựng menu điều hướng đơn hàng trong hệ thống Thương mại điện tử (E-commerce) theo chuẩn mã nguồn Python hiện đại.

### **2. Bối cảnh & Vấn đề**
Bộ phận Vận hành của công ty Thương mại điện tử TechCart đang sử dụng một công cụ giao diện dòng lệnh (CLI Console Menu) để hỗ trợ nhân viên tư vấn nhanh đơn hàng cho khách hàng. Hệ thống cho phép người dùng nhập các phím số tương ứng từ menu để thực hiện các chức năng: xem tổng tiền tạm tính, áp dụng mã giảm giá, hoặc cộng phí vận chuyển.

Tuy nhiên, mã nguồn hiện tại đang gặp sự cố nghiêm trọng: Khi nhân viên nhập bất kỳ phím lựa chọn nào từ menu (ví dụ nhập `1`, `2`, `3` hoặc `0`), hệ thống luôn báo lỗi `[LỖI] Lựa chọn không hợp lệ! Vui lòng chỉ chọn các phím từ 0 đến 3.` và không thực hiện chức năng tương ứng. Ngoài ra, nếu người dùng nhập ký tự không phải là số (như chữ cái `abc`), hệ thống xử lý chưa an toàn.



### **3. Mã nguồn hiện tại**

```python
def display_ecommerce_menu() -> None:
    """Hiển thị bảng menu chức năng điều hành đơn hàng."""
    print("=================================")
    print("   HỆ THỐNG ĐƠN HÀNG E-COMMERCE  ")
    print("=================================")
    print("1. Xem tổng tiền đơn hàng tạm tính")
    print("2. Áp dụng mã giảm giá")
    print("3. Chọn phương thức vận chuyển")
    print("0. Hủy đơn hàng và thoát")
    print("=================================")


def process_order_menu(choice_raw: str, cart_total: float) -> str:
    """Xử lý lựa chọn chức năng menu từ người dùng.

    Lỗi nghiệp vụ hiện tại: So sánh sai kiểu dữ liệu giữa chuỗi nhập vào
    và số nguyên định sẵn trong nhánh kiểm tra.
    """
    # Gán trực tiếp dữ liệu chuỗi nhập vào
    choice = choice_raw

    # Logic so sánh gặp lỗi kiểu dữ liệu
    if choice == 1:
        return f"[THÔNG TIN] Giá trị giỏ hàng hiện tại: {cart_total:,.0f} VND"
    elif choice == 2:
        promo_code: str = input("Nhập mã giảm giá (SUMMER10 / WELCOME): ")
        if promo_code == "SUMMER10":
            discount: float = cart_total * 0.10
            new_total: float = cart_total - discount
            return f"[THÀNH CÔNG] Đã áp dụng mã SUMMER10 (-10%). Tổng tiền mới: {new_total:,.0f} VND"
        else:
            return "[LỖI] Mã giảm giá không hợp lệ!"
    elif choice == 3:
        shipping_type: str = input("Chọn phương thức vận chuyển (1: Giao thường - 30k, 2: Giao hỏa tốc - 50k): ")
        if shipping_type == "1":
            shipping_fee: float = 30000.0
        elif shipping_type == "2":
            shipping_fee = 50000.0
        else:
            shipping_fee = 0.0
        
        total_with_ship: float = cart_total + shipping_fee
        return f"[THÀNH CÔNG] Tổng thanh toán bao gồm phí vận chuyển: {total_with_ship:,.0f} VND"
    elif choice == 0:
        return "[HỆ THỐNG] Đã hủy thao tác đơn hàng. Tạm biệt!"
    else:
        return "[LỖI] Lựa chọn không hợp lệ! Vui lòng chỉ chọn các phím từ 0 đến 3."


if __name__ == "__main__":
    display_ecommerce_menu()
    user_input: str = input("Vui lòng chọn chức năng (0-3): ")
    current_cart_total: float = 500000.0
    result_message: str = process_order_menu(user_input, current_cart_total)
    print(result_message)
```

### **4. Yêu cầu bài toán**

#### **Phần 1: Báo cáo phân tích & Kiểm thử (30 điểm)**
1.  Phân tích mã nguồn và chỉ rõ nguyên nhân chính xác (dòng code số mấy, cơ chế so sánh nào) khiến cho chương trình luôn chuyển đến nhánh `else` khi người dùng nhập `1`, `2`, `3` hoặc `0`.
2.  Lập bảng báo cáo Test Case gồm tối thiểu **3 trường hợp kiểm thử** theo bảng chuẩn HTML dưới đây:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="padding: 8px; text-align: left;">STT</th>
      <th style="padding: 8px; text-align: left;">Mô tả kịch bản test</th>
      <th style="padding: 8px; text-align: left;">Dữ liệu đầu vào (Input)</th>
      <th style="padding: 8px; text-align: left;">Kết quả thực tế bị lỗi (Buggy Output)</th>
      <th style="padding: 8px; text-align: left;">Kết quả kỳ vọng đúng (Expected Output)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px;">1</td>
      <td style="padding: 8px;">Chọn xem tổng tiền tạm tính</td>
      <td style="padding: 8px;">user_input = "1"</td>
      <td style="padding: 8px;">[LỖI] Lựa chọn không hợp lệ!...</td>
      <td style="padding: 8px;">[THÔNG TIN] Giá trị giỏ hàng hiện tại: 500,000 VND</td>
    </tr>
    <tr>
      <td style="padding: 8px;">2</td>
      <td style="padding: 8px;">Nhập lựa chọn thoát hệ thống</td>
      <td style="padding: 8px;">user_input = "0"</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="padding: 8px;">3</td>
      <td style="padding: 8px;">Nhập ký tự chuỗi không phải số</td>
      <td style="padding: 8px;">user_input = "abc"</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Hiệu chỉnh mã nguồn (40 điểm)**
1.  Chỉnh sửa hàm `process_order_menu` để khắc phục hoàn toàn lỗi lệch kiểu dữ liệu giữa `str` và `int`.
2.  Bổ sung khối xử lý ngoại lệ `try-except ValueError` để khi người dùng nhập chuỗi ký tự không chuyển đổi thành số nguyên được, hệ thống sẽ bắt lỗi an toàn và hiển thị thông báo lỗi chuẩn thay vì làm dừng chương trình đột ngột.
3.  Đảm bảo mã nguồn đạt tiêu chuẩn PEP 8, có đầy đủ Type Hints (`int | str`, `float`, `str`, `None`).
4.  **LƯU Ý QUAN TRỌNG:** Tuyệt đối không sử dụng các từ khóa chưa học hoặc bị cấm như `while`, `break`, `continue`.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session06_Ex01`.
    Ví dụ: `HNKS25CNTT1_Core_Session06_Ex01`