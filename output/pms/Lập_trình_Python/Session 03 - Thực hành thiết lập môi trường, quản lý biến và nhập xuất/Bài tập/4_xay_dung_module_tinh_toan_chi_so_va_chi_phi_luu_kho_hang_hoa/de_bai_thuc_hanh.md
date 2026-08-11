## <center>Xây dựng Module Tính toán Chỉ số và Chi phí Lưu kho Hàng hóa</center>

### **1. Mục tiêu**
- Khởi tạo môi trường ảo Python 3.12 (`venv`) và cấu hình cấu trúc mã nguồn theo chuẩn PEP 8.
- Áp dụng thành thạo các kiểu dữ liệu cơ sở (`int`, `float`, `str`, `bool`) để quản lý thông tin kiện hàng trong phân hệ kho.
- Thực hiện chuyển đổi kiểu dữ liệu bắt buộc (Explicit Type Casting) từ dữ liệu nhập vào CLI của người dùng (`input()`).
- Sử dụng các phép toán số học (`+`, `-`, `*`, `/`, `//`, `%`) và biểu thức logic để giải quyết các chỉ số logistics nâng cao (thể tích quy đổi, phân bổ Pallet, phụ phí và thuế).
- Định dạng và hiển thị kết quả báo cáo chuyên nghiệp trên Terminal bằng hàm `print()` kết hợp tham số `sep`, `end` và kỹ thuật f-string formatting.

### **2. Vấn đề**
Trong phân hệ Quản lý Kho hàng (Warehouse Management Subsystem - WMS), bộ phận vận hành cần một công cụ dòng lệnh (CLI) để nhanh chóng tính toán các chỉ số lưu kho cho từng lô hàng mới nhập. Việc xác định trọng lượng quy đổi theo thể tích (Volumetric Weight) và chi phí lưu kho dự kiến giúp doanh nghiệp tối ưu hóa diện tích sàn kho và dự trù ngân sách chính xác.

Chương trình cần tiếp nhận các thông số kích thước 3 chiều của thùng hàng, trọng lượng thực tế, số lượng thùng, đơn giá lưu kho và số ngày lưu trữ. Sau đó, hệ thống thực hiện chuyển đổi kiểu dữ liệu, tính toán toàn bộ chỉ số vận hành và in ra phiếu báo cáo tổng hợp chuẩn hóa.

Dưới đây là sơ đồ luồng dữ liệu xử lý của bài toán:

```mermaid

flowchart TD
    A[/ "Nhập thông tin kiện hàng: SKU, kích thước, trọng lượng, số lượng" /] --> B[/"Thực hiện ép kiểu dữ liệu: str, float, int"/]
    B --> C[/"Tính thể tích 1 thùng (volume_per_box) và tổng thể tích (total_volume)"/]
    C --> D[/"Tính trọng lượng quy đổi (volumetric_weight) và trọng lượng tính phí"/]
    D --> E[/"Tính số lượng Pallet cần sử dụng (pallets_needed)"/]
    E --> F[/"Tính chi phí lưu kho gốc, phụ phí kho 10% và thuế VAT 8%"/]
    F --> G[/ "Xuất phiếu báo cáo chi phí lưu kho định dạng bảng (CLI)" /]

```

### **3. Yêu cầu bài toán**
Viết một script Python hoàn chỉnh có tên file `warehouse_calculator.py` để xử lý bài toán trên.

Dưới đây là bảng chi tiết các biến và thông số cần quản lý trong chương trình:

<table border="1" style="width:100%; border-collapse: collapse; text-align: left;">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="padding: 8px;">Tên biến (PEP 8)</th>
      <th style="padding: 8px;">Kiểu dữ liệu</th>
      <th style="padding: 8px;">Mô tả nghiệp vụ</th>
      <th style="padding: 8px;">Công thức / Ràng buộc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px;"><code>sku_code</code></td>
      <td style="padding: 8px;"><code>str</code></td>
      <td style="padding: 8px;">Mã định danh lô/kiện hàng</td>
      <td style="padding: 8px;">Chuỗi ký tự in hoa, không chứa khoảng trắng thừa</td>
    </tr>
    <tr>
      <td style="padding: 8px;"><code>box_length</code>, <code>box_width</code>, <code>box_height</code></td>
      <td style="padding: 8px;"><code>float</code></td>
      <td style="padding: 8px;">Chiều dài, rộng, cao của 1 thùng (cm)</td>
      <td style="padding: 8px;">Số thực dương</td>
    </tr>
    <tr>
      <td style="padding: 8px;"><code>unit_weight</code></td>
      <td style="padding: 8px;"><code>float</code></td>
      <td style="padding: 8px;">Trọng lượng thực tế của 1 thùng (kg)</td>
      <td style="padding: 8px;">Số thực dương</td>
    </tr>
    <tr>
      <td style="padding: 8px;"><code>box_quantity</code></td>
      <td style="padding: 8px;"><code>int</code></td>
      <td style="padding: 8px;">Tổng số lượng thùng trong lô hàng</td>
      <td style="padding: 8px;">Số nguyên dương</td>
    </tr>
    <tr>
      <td style="padding: 8px;"><code>daily_rate_per_m3</code></td>
      <td style="padding: 8px;"><code>float</code></td>
      <td style="padding: 8px;">Đơn giá lưu kho (VND / m3 / ngày)</td>
      <td style="padding: 8px;">Số thực positive</td>
    </tr>
    <tr>
      <td style="padding: 8px;"><code>storage_days</code></td>
      <td style="padding: 8px;"><code>int</code></td>
      <td style="padding: 8px;">Số ngày dự kiến lưu kho</td>
      <td style="padding: 8px;">Số nguyên dương</td>
    </tr>
  </tbody>
</table>

#### **Ví dụ dữ liệu đầu vào (Input):**
```text
=== NHẬP THÔNG TIN LÔ HÀNG NỘP KHO ===
Nhập mã kiện hàng (SKU): WMS-2024-8899
Nhập chiều dài thùng hàng (cm): 60.0
Nhập chiều rộng thùng hàng (cm): 40.0
Nhập chiều cao thùng hàng (cm): 50.0
Nhập trọng lượng 1 thùng (kg): 12.5
Nhập số lượng thùng hàng: 50
Nhập đơn giá lưu kho (VND/m3/ngày): 15000
Nhập số ngày lưu kho dự kiến: 30
```

#### **Ví dụ dữ liệu đầu ra (Output):**
```text
======================================================================
                 PHIẾU KÊ KHAI CHI PHÍ LƯU KHO HÀNG HÓA
======================================================================
Mã lô hàng (SKU)               : WMS-2024-8899
Tổng số lượng thùng            : 50 thùng
----------------------------------------------------------------------
[1] CHỈ SỐ KÍCH THƯỚC VÀ THỂ TÍCH:
- Thể tích 1 thùng (m3)       : 0.1200 m3
- Tổng thể tích lô hàng (m3)   : 6.0000 m3
- Số Pallet tiêu chuẩn cần dùng: 5 Pallet

[2] CHỈ SỐ TRỌNG LƯỢNG:
- Tổng trọng lượng thực tế     : 625.00 kg
- Tổng trọng lượng quy đổi     : 1200.00 kg
- Trọng lượng tính phí kho     : 1200.00 kg

[3] DỰ TOÁN CHI PHÍ LƯU KHO (30 NGÀY):
- Chi phí lưu kho cơ bản       : 2,700,000.00 VND
- Phụ phí quản lý kho (10%)    : 270,000.00 VND
- Thuế giá trị gia tăng (VAT 8%): 237,600.00 VND
----------------------------------------------------------------------
TỔNG CHI PHÍ LƯU KHO THANH TOÁN: 3,207,600.00 VND
======================================================================
```

### **4. Quy tắc xử lý**
- **Yêu cầu 1:** Tạo môi trường ảo `venv` cho bài tập, đảm bảo script thực thi tương thích hoàn toàn trên Python 3.12. Đặt comment mô tả file ở đầu chương trình bao gồm: tên tác giả, ngày tạo và mục đích mã nguồn.
- **Yêu cầu 2:** Nhận dữ liệu đầu vào từ bàn phím bằng hàm `input()`. Sử dụng phương thức `.strip()` để làm sạch chuỗi nhập vào cho mã SKU.
- **Yêu cầu 3:** Thực hiện ép kiểu tường minh (Explicit Type Casting):
  - Chuyển `box_length`, `box_width`, `box_height`, `unit_weight`, `daily_rate_per_m3` sang kiểu `float`.
  - Chuyển `box_quantity`, `storage_days` sang kiểu `int`.
- **Yêu cầu 4:** Áp dụng các công thức tính toán chỉ số kho bằng mã lệnh Python:
  - Thể tích 1 thùng (m3): `volume_per_box = (box_length * box_width * box_height) / 1000000.0`
  - Tổng thể tích lô hàng (m3): `total_volume = volume_per_box * box_quantity`
  - Trọng lượng quy đổi thể tích (kg): `volumetric_weight = (box_length * box_width * box_height) / 5000.0 * box_quantity` (Quy chuẩn Hàng không/Kho vận: 1 m3 = 200 kg tương đương chia 5000 cm3/kg).
  - Tổng trọng lượng thực tế (kg): `total_actual_weight = unit_weight * box_quantity`
  - Trọng lượng tính phí (kg): `chargeable_weight = max(total_actual_weight, volumetric_weight)`
  - Số lượng Pallet tiêu chuẩn cần dùng (Giả định 1 Pallet chứa tối đa 1.2 m3 hàng): `pallets_needed = int(total_volume // 1.2) + int((total_volume % 1.2) > 0)` (Áp dụng toán tử chia lấy phần nguyên `//`, chia lấy dư `%` và ép kiểu luận lý `bool` sang `int`).
  - Chi phí lưu kho cơ bản: `raw_storage_fee = total_volume * daily_rate_per_m3 * storage_days`
  - Phụ phí quản lý kho (10%): `surcharge = raw_storage_fee * 0.10`
  - Thuế VAT (8% trên tổng chi phí bao gồm phụ phí): `vat_amount = (raw_storage_fee + surcharge) * 0.08`
  - Tổng chi phí thanh toán: `total_payable = raw_storage_fee + surcharge + vat_amount`
- **Yêu cầu 5:** Định dạng dữ liệu đầu ra chuyên nghiệp bằng f-string specifiers:
  - Thể tích làm tròn 4 chữ số thập phân (`:.4f`).
  - Các chỉ số trọng lượng và chi phí làm tròn 2 chữ số thập phân (`:.2f`).
  - Phải dùng tham số `sep` và `end` của hàm `print()` ít nhất 2 lần trong mã nguồn để tạo các đường phân cách và cấu trúc báo cáo.

### **5. Yêu cầu nộp bài**
- Mã nguồn được lưu trong file `warehouse_calculator.py`.
- Tạo file `README.md` mô tả hướng dẫn kích hoạt môi trường `venv` và lệnh chạy chương trình từ Terminal/CLI.
- Đẩy mã nguồn lên repository GitHub cá nhân theo cấu trúc:
  ```text
  repository-name/
  ├── .gitignore
  ├── README.md
  └── warehouse_calculator.py
  ```
- Dán liên kết GitHub repository vào hệ thống nộp bài.