## <center>[Vận dụng chuyên sâu] Thiết kế hệ thống quản lý danh mục và xử lý đơn hàng E-Commerce CLI</center>

### **1. Mục tiêu**
*   **Tư duy kiến trúc hệ thống:** Phân tích và thiết kế luồng xử lý dữ liệu đơn hàng trong hệ thống quản trị Thương mại Điện tử (E-Commerce Subsystem) sử dụng mô hình lập trình hướng hàm chuẩn hóa.
*   **Kỹ năng xử lý cấu trúc lặp nâng cao:** Vận dụng linh hoạt các cấu trúc vòng lặp `for` để duyệt danh mục sản phẩm, tính toán giá trị giỏ hàng và cập nhật tồn kho (tuân thủ tuyệt đối giới hạn không sử dụng vòng lặp `while`, từ khóa `break` và `continue`).
*   **Xử lý ràng buộc và Ngoại lệ:** Thực thi kiểm chuẩn dữ liệu (Validation), xử lý các ngoại lệ nghiệp vụ (`ValueError`, `KeyError`) và bảo đảm tính toàn vẹn dữ liệu tồn kho.
*   **Tuân thủ chuẩn công nghiệp Python (PEP 8):** Áp dụng Type Hints (Python 3.10+ syntax `int | float | str`), đặt tên biến/hàm theo chuẩn `snake_case` bằng tiếng Anh và ghi chú thích logic bằng tiếng Việt có dấu.

### **2. Vấn đề**

Trong một hệ thống Thương mại Điện tử, bộ phận vận hành kho và đơn hàng cần một công cụ xử lý danh sách đơn hàng theo lô (Batch Processing CLI) trong ca làm việc. Mỗi đơn hàng chứa thông tin khách hàng, hạng hội viên (VIP hoặc Regular), danh sách các sản phẩm và số lượng tương ứng.

Hệ thống cần tự động duyệt qua danh sách đơn hàng chờ xử lý, kiểm tra tính hợp lệ của tồn kho cho từng sản phẩm, áp dụng chính sách chiết khấu tương ứng với hạng hội viên, tính toán tổng doanh thu và cập nhật lại số lượng tồn kho theo thời gian thực trong bộ nhớ (In-Memory Data Store).



### **3. Quy tắc nghiệp vụ**

Hệ thống quản lý dữ liệu sản phẩm và đơn hàng được mô hình hóa trong bộ nhớ dưới dạng các cấu trúc dữ liệu dictionary/list. Các quy tắc nghiệp vụ cốt lõi bao gồm:

#### **A. Quy tắc tính chiết khấu (Discount Policy)**
*   **Hạng VIP:**
    *   Tổng giá trị đơn hàng trước chiết khấu $\ge 1,000,000$ VND: Giảm **15%** trên tổng giá trị đơn hàng.
    *   Tổng giá trị đơn hàng trước chiết khấu $< 1,000,000$ VND: Giảm **10%** trên tổng giá trị đơn hàng.
*   **Hạng Regular:**
    *   Tổng giá trị đơn hàng trước chiết khấu $\ge 2,000,000$ VND: Giảm **5%** trên tổng giá trị đơn hàng.
    *   Tổng giá trị đơn hàng trước chiết khấu $< 2,000,000$ VND: Giảm **0%** (không giảm giá).

#### **B. Quy tắc kiểm tra tồn kho và Cập nhật trạng thái (Inventory Check & Processing)**
1.  **Mặt hàng hợp lệ:** Mỗi sản phẩm trong đơn hàng phải tồn tại trong danh mục tồn kho (`catalog`). Nếu mã sản phẩm không tồn tại, đơn hàng bị đánh dấu thất bại với lý do: `"Mã sản phẩm không tồn tại trong danh mục"`.
2.  **Số lượng tồn kho:** Số lượng yêu cầu của mỗi mặt hàng không được vượt quá số lượng tồn kho hiện có (`stock`). Nếu số lượng đặt mua vượt quá tồn kho, đơn hàng bị đánh dấu thất bại với lý do: `"Số lượng tồn kho không đủ"`.
3.  **Trừ tồn kho:** Nếu tất cả mặt hàng trong đơn hàng đều hợp lệ, hệ thống tiến hành trừ số lượng tồn kho tương ứng của từng sản phẩm trong `catalog`, tính tổng thanh toán sau chiết khấu và đổi trạng thái đơn hàng thành `"PROCESSED"`.
4.  **Hủy thao tác đơn lỗi:** Nếu đơn hàng có bất kỳ mặt hàng nào không hợp lệ, tuyệt đối **KHÔNG** trừ tồn kho của bất kỳ sản phẩm nào trong đơn hàng đó và đổi trạng thái thành `"FAILED"`.

#### **C. Ràng buộc kỹ thuật nghiêm ngặt**
*   **Giới hạn kiến thức:** Tuyệt đối **KHÔNG** sử dụng vòng lặp `while`, các lệnh điều khiển `break` và `continue`. Sinh viên phải giải quyết bài toán lặp bằng vòng lặp `for` với các biến cờ hiệu (boolean flags) hoặc logic điều kiện thích hợp.
*   **Kiến trúc:** Phải tách biệt logic thành các hàm riêng biệt (ví dụ: hàm tính chiết khấu, hàm kiểm tra đơn hàng, hàm cập nhật tồn kho, hàm hiển thị báo cáo console).

### **4. Yêu cầu bài toán**

#### **Mẫu dữ liệu tham khảo (Visual Payload Sample)**
Dưới đây là cấu trúc dữ liệu đầu vào ví dụ mà hệ thống của bạn cần xử lý:

```python
# Danh mục sản phẩm trong kho (Inventory Catalog)
catalog_data = {
    "PROD01": {"name": "Áo sơ mi Nam Premium", "price": 450000, "stock": 20},
    "PROD02": {"name": "Quần Jean Nữ Slimfit", "price": 650000, "stock": 15},
    "PROD03": {"name": "Giày Sneaker Unisex", "price": 1200000, "stock": 3},
    "PROD04": {"name": "Balo Máy tính bảng", "price": 300000, "stock": 0}
}

# Danh sách đơn hàng chờ xử lý (Pending Order Batch)
order_batch = [
    {
        "order_id": "ORD-8801",
        "customer_name": "Nguyễn Văn A",
        "customer_type": "VIP",
        "items": [
            {"product_id": "PROD01", "quantity": 2},
            {"product_id": "PROD03", "quantity": 1}
        ]
    },
    {
        "order_id": "ORD-8802",
        "customer_name": "Trần Thị B",
        "customer_type": "Regular",
        "items": [
            {"product_id": "PROD02", "quantity": 20}  # Vượt quá số lượng tồn kho (15)
        ]
    },
    {
        "order_id": "ORD-8803",
        "customer_name": "Lê Hoàng C",
        "customer_type": "VIP",
        "items": [
            {"product_id": "PROD99", "quantity": 1}  # Mã sản phẩm không tồn tại
        ]
    }
]
```

#### **Phần 1: Phân tích và Thiết kế giải pháp (Báo cáo)**
1.  **Xác định I/O Schema:** Mô tả kiểu dữ liệu chi tiết cho tham số đầu vào và kết quả đầu ra của từng hàm xử lý.
2.  **Mô tả thuật toán xử lý:** Biểu diễn thuật toán duyệt batch đơn hàng và thuật toán validation (không dùng `break`/`continue`/`while`) bằng Mã giả (Pseudocode) hoặc Sơ đồ khối (Flowchart).

#### **Phần 2: Triển khai mã nguồn từ đầu (Source Code Implementation)**
Sinh viên tự viết toàn bộ mã nguồn chương trình từ đầu trên file Python với các chức năng:
1.  Định nghĩa danh mục kho hàng và danh sách đơn hàng ban đầu.
2.  Viết hàm tính toán giá trị đơn hàng và số tiền giảm giá dựa trên hạng khách hàng.
3.  Viết hàm duyệt qua từng đơn hàng, kiểm tra tính hợp lệ của toàn bộ mặt hàng trong đơn mà không làm rò rỉ dữ liệu tồn kho khi có lỗi.
4.  Viết hàm cập nhật tồn kho và lưu vết trạng thái đơn hàng.
5.  In giao diện báo cáo tổng hợp kết quả ra màn hình Console với định dạng phân tách rõ ràng (Tổng đơn xử lý thành công, tổng đơn thất bại, tổng doanh thu thực tế thu về, và bảng kho hàng sau khi cập nhật).

### **5. Yêu cầu nộp bài**

Học viên cần nộp:
*   Phần phân tích/báo cáo thiết kế giải pháp và mã nguồn triển khai hoàn chỉnh.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session06_Ex03`.
    Ví dụ: `HNKS25CNTT1_Core_Session06_Ex03`