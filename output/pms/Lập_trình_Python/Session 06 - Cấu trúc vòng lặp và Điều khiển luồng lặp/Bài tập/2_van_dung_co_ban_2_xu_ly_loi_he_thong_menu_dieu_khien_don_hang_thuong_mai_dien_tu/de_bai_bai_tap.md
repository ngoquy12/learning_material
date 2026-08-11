## <center>[Vận dụng cơ bản 2] Xử lý lỗi hệ thống Menu điều khiển đơn hàng thương mại điện tử</center>

### **1. Mục tiêu**
*   **Phát hiện và phân tích lỗi logic**: Nhận diện các điểm sai sót trong chức năng xử lý lệnh thao tác từ menu tính toán đơn hàng thương mại điện tử (E-Commerce CLI).
*   **Lập báo cáo kiểm thử (Test Case Report)**: Xây dựng bảng kịch bản kiểm thử mô tả chi tiết giá trị đầu vào (Input), kết quả sai hiện tại (Buggy Output) và kết quả đúng chuẩn nghiệp vụ (Expected Output).
*   **Tối ưu hóa mã nguồn & Kiểm chuẩn dữ liệu**: Cập nhật hàm xử lý theo quy chuẩn Python PEP 8, ném ngoại lệ `ValueError` khi dữ liệu không hợp lệ, tuyệt đối không sử dụng các cấu trúc bị cấm (`while`, `break`, `continue`).

### **2. Bối cảnh & Vấn đề**
Trong hệ thống quản lý đơn hàng e-commerce, nhân viên vận hành sử dụng bộ điều hướng lệnh theo dạng danh sách thao tác console (1: Xem tổng tiền đơn hàng, 2: Áp dụng mã giảm giá %, 3: Cộng phí giao hàng cố định, 0: Hoàn tất phiên giao dịch). 

Tuy nhiên, đoạn mã legacy hiện tại đang bị lỗi nghiêm trọng: không kiểm tra phạm vi của mã lệnh thao tác menu, không xác thực phần trăm giảm giá (cho phép giảm vượt quá 100% hoặc giảm số âm), và làm cho giá trị đơn hàng có thể bị âm mà không đưa ra bất kỳ cảnh báo nào.



### **3. Mã nguồn hiện tại**
Dưới đây là mã nguồn legacy chứa các lỗi logic nghiệp vụ và thiếu kiểm chuẩn dữ liệu:

```python
def process_cart_action(action: int, order_total: float, discount_percent: float) -> float:
    """Hàm xử lý thao tác menu đơn hàng e-commerce (Đoạn mã legacy có lỗi)."""
    # Thao tác 1: Xem số tiền hiện tại
    if action == 1:
        return order_total
    
    # Thao tác 2: Áp dụng giảm giá (%)
    elif action == 2:
        # LỖI: Không kiểm tra discount_percent có hợp lệ không (ví dụ < 0 hoặc > 100)
        # LỖI: Không kiểm tra order_total có > 0 không
        discount_amount = order_total * (discount_percent / 100)
        order_total = order_total - discount_amount
        return order_total
    
    # Thao tác 3: Cộng phí vận chuyển cố định 30,000 VND
    elif action == 3:
        return order_total + 30000.0
    
    # LỖI: Không có xử lý cho các lựa chọn khác ngoài 1, 2, 3 (ví dụ action = 99 hoặc action < 0)
    # LỖI: Trả về kết quả mặc định không cảnh báo
    return order_total


def batch_process_menu(actions: list[int], initial_total: float, discount_rate: float) -> None:
    """Duyệt qua danh sách thao tác menu được truyền vào."""
    current_total = initial_total
    print("=== BẮT ĐẦU XỬ LÝ MENU ĐƠN HÀNG ===")
    for act in actions:
        current_total = process_cart_action(act, current_total, discount_rate)
        print(f"[THÔNG TIN] Thao tác {act} - Tổng tiền hiện tại: {current_total:,.0f} VND")


# Chạy thử nghiệm với dữ liệu gây lỗi
test_actions = [1, 2, 99]
batch_process_menu(test_actions, 500000.0, 150.0)
```

### **4. Yêu cầu bài toán**

#### **Phần 1: Báo cáo phân tích lỗi & Lập bảng Test Case (30 điểm)**
1. Chỉ ra cụ thể ít nhất 3 vị trí dòng mã nguồn legacy gặp lỗi logic hoặc thiếu kiểm tra ràng buộc nghiệp vụ.
2. Xây dựng bảng danh sách kịch bản kiểm thử (tối thiểu 3 Test Cases) theo định dạng HTML sau:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="padding: 8px; text-align: left;">STT</th>
      <th style="padding: 8px; text-align: left;">Mô tả kịch bản kiểm thử</th>
      <th style="padding: 8px; text-align: left;">Dữ liệu đầu vào (Input)</th>
      <th style="padding: 8px; text-align: left;">Kết quả thực tế bị lỗi (Buggy Output)</th>
      <th style="padding: 8px; text-align: left;">Kết quả kỳ vọng đúng (Expected Output)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px;">1</td>
      <td style="padding: 8px;">Áp dụng tỷ lệ giảm giá > 100%</td>
      <td style="padding: 8px;">action=2, total=500000, discount=150.0</td>
      <td style="padding: 8px;">Tổng tiền = -250,000 VND (Âm tiền)</td>
      <td style="padding: 8px;">Ném ngoại lệ ValueError báo lỗi phần trăm không hợp lệ</td>
    </tr>
    <tr>
      <td style="padding: 8px;">2</td>
      <td style="padding: 8px;">Nhập mã thao tác menu không tồn tại</td>
      <td style="padding: 8px;">action=99, total=500000, discount=10.0</td>
      <td style="padding: 8px;">Chương trình bỏ qua âm thầm, trả về tổng tiền cũ</td>
      <td style="padding: 8px;">Ném ngoại lệ ValueError báo lựa chọn không hợp lệ</td>
    </tr>
    <tr>
      <td style="padding: 8px;">3</td>
      <td style="padding: 8px;">Áp dụng giảm giá khi tổng tiền đơn hàng <= 0</td>
      <td style="padding: 8px;">action=2, total=-100000, discount=10.0</td>
      <td style="padding: 8px;">Tiếp tục tính toán sai trên số tiền âm</td>
      <td style="padding: 8px;">Ném ngoại lệ ValueError báo tổng tiền phải lớn hơn 0</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Sửa mã nguồn nghiệp vụ (50 điểm)**
Học viên tiến hành viết lại hàm `process_cart_action` và `batch_process_menu` thỏa mãn các quy tắc nghiệp vụ sau:
1. **Kiểm tra phạm vi thao tác `action`**: Các thao tác hợp lệ gồm `0, 1, 2, 3`. Nếu `action` không thuộc danh sách này, ném lỗi: `raise ValueError("[LỖI] Lựa chọn menu không hợp lệ! Chỉ chấp nhận 0, 1, 2, 3.")`.
2. **Kiểm tra tổng tiền `order_total`**: Phải là số dương (`order_total > 0`). Nếu `order_total <= 0`, ném lỗi: `raise ValueError("[LỖI] Giá trị đơn hàng phải lớn hơn 0!")`.
3. **Kiểm tra tỷ lệ giảm giá `discount_percent`**: Khi `action == 2`, `discount_percent` phải nằm trong khoảng từ `0.0` đến `100.0`. Nếu nằm ngoài khoảng, ném lỗi: `raise ValueError("[LỖI] Tỷ lệ giảm giá phải từ 0% đến 100%!")`.
4. **Xử lý `action == 0`**: Trả về đúng `order_total` và in thông báo `"[HỆ THỐNG] Đã hoàn tất xử lý đơn hàng an toàn."`.
5. **Ràng buộc kĩ thuật**:
   * Chuẩn PEP 8: Đặt tên biến/hàm kiểu `snake_case`, bổ sung Type Hints chuẩn Python 3.10+ (`int | float`).
   * **Tuyệt đối CẤM**: Không sử dụng vòng lặp `while`, không sử dụng các lệnh `break`, `continue`.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session06_Ex02`.
    Ví dụ: `HNKS25CNTT1_Core_Session06_Ex02`