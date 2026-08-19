# Bài tập 3: FinTech (Mức độ 1: Cơ bản - Debug lỗi)

### 1. Mục tiêu bài tập
Sau khi hoàn thành bài tập này, học viên sẽ có khả năng:
- **Phát hiện và sửa lỗi (Debug)** các sự kiện lắng nghe người dùng trên Web Form (`submit`, `input`, `change`).
- Khắc phục sự cố trang bị nạp lại (reload) bằng việc sử dụng chính xác phương thức `event.preventDefault()`.
- Xử lý và ép kiểu dữ liệu từ form input (`DOM element.value`) đúng định dạng số để tính toán tài chính xác thực, tránh lỗi nối chuỗi.
- Áp dụng các quy tắc kiểm tra an toàn (Validation) và hiển thị phản hồi thời gian thực (Real-time Feedback) cho ứng dụng quản lý trạm sạc xe điện VinFast.

---


### 2. Bối cảnh & Mô tả bài toán
Hệ thống trạm sạc xe điện thông minh **VinFast EV Charging Station** đang triển khai giao diện màn hình sạc nhanh tại các trạm dừng nghỉ. Nhóm phát triển Junior đã viết bản phác thảo code HTML/JavaScript cho tính năng **"Tính toán Hóa đơn & Kiểm tra An toàn Phiên sạc"** (`VehicleSession` & `ChargingInvoice`). 

Tuy nhiên, phiên bản này đang gặp nhiều lỗi nghiêm trọng:
1. Khi nhấn nút "Xác nhận & Tính hóa đơn", trang web lập tức bị tải lại làm mất hết dữ liệu đã nhập.
2. Tổng tiền thanh toán bị tính sai do lỗi nối chuỗi thay vì phép cộng số.
3. Phí đỗ xe quá giờ không tính chính xác thời gian miễn phí.
4. Cảnh báo nhiệt độ quá tải của cổng sạc không hoạt động khi người dùng đang nhập dữ liệu.

Nhiệm vụ của bạn là kiểm tra, phát hiện các lỗi trong mã nguồn ban đầu, sau đó sửa lại để hệ thống hoạt động chính xác theo quy trình nghiệp vụ.

```mermaid
graph TD
    A[Người dùng chọn Cổng sạc & Nhập số kWh] --> B[Nhập Thời gian đỗ & Nhiệt độ Cổng sạc]
    B --> C{Kiểm tra Nhiệt độ thời gian thực}
    C -- Nhiệt độ > 70°C -- > D[Hiển thị Cảnh báo Nguy hiểm & Khóa Form]
    C -- Nhiệt độ <= 70°C -- > E[Cho phép nhấn Xác nhận]
    E --> F[Sự kiện Submit Form]
    F --> G[Chặn Reload Trang: preventDefault]
    G --> H[Tính Tiền điện + Phí phạt quá giờ]
    H --> I[Hiển thị Hóa đơn ChargingInvoice]
```

---


### 3. Quy tắc nghiệp vụ (Business Rules)

1. **Đơn giá điện sạc năng lượng (`ChargingPort`):**
   - Cổng sạc Thường (`STANDARD`): **3.850 VNĐ / kWh**
   - Cổng sạc Siêu nhanh (`FAST`): **4.500 VNĐ / kWh**

2. **Quy tắc Phí đỗ xe sau khi sạc xong (`VehicleSession`):**
   - Tối đa **30 phút đầu** sau khi sạc đầy được **miễn phí đỗ**.
   - Từ phút thứ **31** trở đi, tính phí phạt đỗ xe là **1.000 VNĐ / phút**.
   - *Công thức tính phí phạt*: `Phí phạt = max(0, Tổng_số_phút_đỗ - 30) * 1000`

3. **Quy tắc Cảnh báo An toàn Trạm sạc (`KwhMeter`):**
   - Nếu nhiệt độ cổng sạc (`portTemp`) **vượt quá 70°C**:
     - Hiển thị ngay cảnh báo lỗi thời gian thực: `"CẢNH BÁO: Nhiệt độ cổng sạc quá cao (>70°C). Tự động ngắt kết nối!"`.
     - Vùng hiển thị hóa đơn bị ẩn hoặc xóa kết quả tính.
   - Nếu nhiệt độ **<= 70°C**: Ẩn thông báo cảnh báo và cho phép tính hóa đơn bình thường.

4. **Ràng buộc Dữ liệu Đầu vào (Validation):**
   - Điện lượng tiêu thụ (`kwh`) phải là số dương lớn hơn 0.
   - Thời gian đỗ xe (`parkingMinutes`) và Nhiệt độ (`portTemp`) không được để trống hoặc mang giá trị âm.

---


### 4. Yêu cầu kỹ thuật & Mã nguồn bị lỗi (Broken Starter Code)


#### 4.1. Mã nguồn hiện tại bị lỗi

Dưới đây là mã nguồn HTML và JavaScript hiện tại do lập trình viên thử việc bàn giao. Hãy đưa đoạn mã này vào dự án của bạn và tiến hành debug.

**File `index.html`:**
```html
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>VinFast EV Charging Station - Debug Form</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }
        .form-group { margin-bottom: 15px; }
        label { display: block; font-weight: bold; }
        input, select { padding: 8px; width: 300px; margin-top: 5px; }
        button { padding: 10px 20px; background-color: #0066cc; color: white; border: none; cursor: pointer; }
        .error { color: red; font-weight: bold; margin-top: 10px; display: none; }
        .invoice-card { margin-top: 20px; padding: 15px; border: 2px solid #0066cc; background-color: #f4f8fc; display: none; }
    </style>
</head>
<body>
    <h2>Hệ thống Trạm sạc Xe điện VinFast - Tính Hóa đơn</h2>
    
    <div id="dangerAlert" class="error"></div>

    <form id="chargingForm">
        <div class="form-group">
            <label for="portType">Loại cổng sạc:</label>
            <select id="portType">
                <option value="3850">Sạc Thường (STANDARD) - 3.850đ/kWh</option>
                <option value="4500">Sạc Siêu nhanh (FAST) - 4.500đ/kWh</option>
            </select>
        </div>

        <div class="form-group">
            <label for="kwhInput">Điện lượng sạc (kWh):</label>
            <input type="number" id="kwhInput" placeholder="Nhập số kWh ví dụ: 25.5">
        </div>

        <div class="form-group">
            <label for="parkingMinutes">Thời gian đỗ thêm sau khi sạc (Phút):</label>
            <input type="number" id="parkingMinutes" placeholder="Nhập số phút đỗ xe">
        </div>

        <div class="form-group">
            <label for="portTemp">Nhiệt độ Cổng sạc (°C):</label>
            <input type="number" id="portTemp" placeholder="Nhập nhiệt độ hiện tại">
        </div>

        <button type="submit" id="btnCalculate">Xác nhận & Tính hóa đơn</button>
    </form>

    <div id="invoiceResult" class="invoice-card">
        <h3>HÓA ĐƠN DỊCH VỤ SẠC XE (ChargingInvoice)</h3>
        <p>Tiền điện tiêu thụ: <span id="kwhCostText">0</span> VNĐ</p>
        <p>Phí phạt đỗ quá giờ: <span id="penaltyCostText">0</span> VNĐ</p>
        <hr>
        <p><strong>TỔNG THỦ TIỀN: <span id="totalCostText">0</span> VNĐ</strong></p>
    </div>

    <script src="script.js"></script>
</body>
</html>
```

**File `script.js` (Mã nguồn chứa lỗi):**
```javascript
// Mã nguồn bị lỗi do lập trình viên thử việc bàn giao
const chargingForm = document.getElementById('chargingForm');
const portType = document.getElementById('portType');
const kwhInput = document.getElementById('kwhInput');
const parkingMinutes = document.getElementById('parkingMinutes');
const portTemp = document.getElementById('portTemp');

const dangerAlert = document.getElementById('dangerAlert');
const invoiceResult = document.getElementById('invoiceResult');
const kwhCostText = document.getElementById('kwhCostText');
const penaltyCostText = document.getElementById('penaltyCostText');
const totalCostText = document.getElementById('totalCostText');

// LỖI 1: Lắng nghe sự kiện change thay vì input trên ô nhiệt độ
portTemp.addEventListener('change', function() {
    if (portTemp.value > 70) {
        dangerAlert.innerText = "CẢNH BÁO: Nhiệt độ cổng sạc quá cao (>70°C). Tự động ngắt kết nối!";
        dangerAlert.style.display = "block";
    } else {
        dangerAlert.style.display = "none";
    }
});

// LỖI 2: Sự kiện submit form bị reload trang và xử lý tính toán dữ liệu sai kiểu
chargingForm.addEventListener('submit', function(e) {
    // Quên ngăn chặn hành vi mặc định của form

    let pricePerKwh = portType.value;
    let kwhAmount = kwhInput.value;
    let extraMinutes = parkingMinutes.value;

    // LỖI 3: Tính toán phí phạt đỗ xe bị sai công thức (Chưa trừ 30 phút miễn phí)
    let penaltyFee = extraMinutes * 1000;

    // LỖI 4: Phép tính tiền bị lỗi cộng chuỗi thay vì phép cộng số
    let kwhTotalCost = kwhAmount * pricePerKwh;
    let finalTotal = kwhTotalCost + penaltyFee; // Xảy ra lỗi nếu penaltyFee bị hiểu sai kiểu dữ liệu

    // Hiển thị kết quả
    kwhCostText.innerText = kwhTotalCost.toLocaleString('vi-VN');
    penaltyCostText.innerText = penaltyFee.toLocaleString('vi-VN');
    totalCostText.innerText = finalTotal.toLocaleString('vi-VN');

    invoiceResult.style.display = "block";
});
```

---


#### 4.2. Danh mục Bug cần sửa (Debug Checklist)

Bạn hãy phân tích mã nguồn trên, tìm và khắc phục triệt để các lỗi sau:

1. **Lỗi Reload Trang (Form Submission Bug):**
   - Khi bấm submit, trang web nạp lại và xóa sạch kết quả. Cần bổ sung `event.preventDefault()` đúng vị trí trong callback của sự kiện `submit`.

2. **Lỗi Cập nhật Cảnh báo Nhiệt độ (Real-time Input Bug):**
   - Sự kiện `change` chỉ kích hoạt khi blur (rời khỏi ô input). Hãy đổi sang lắng nghe sự kiện `input` để cảnh báo hiển thị ngay lập tức khi người dùng nhập số > 70.
   - Thêm xử lý: Nếu nhiệt độ > 70°C, không được cho phép tính và hiển thị hóa đơn khi submit form.

3. **Lỗi Tính Phí đỗ xe quá giờ (Business Logic Bug):**
   - Mã nguồn cũ đang tính `extraMinutes * 1000` mà không trừ đi 30 phút miễn phí. Hãy cập nhật công thức: nếu phút đỗ <= 30 thì phí phạt = 0; nếu > 30 thì tính `(extraMinutes - 30) * 1000`.

4. **Lỗi Nối chuỗi & Ép kiểu dữ liệu (Data Type Bug):**
   - Giá trị lấy từ `input.value` luôn là chuỗi (`string`). Cần ép kiểu dữ liệu sang dạng số (`parseFloat` hoặc `Number`) trước khi thực hiện các phép tính toán tài chính.

5. **Lỗi Xử lý Dữ liệu Rống / Không hợp lệ (Validation Exception):**
   - Nếu số kWh <= 0 hoặc để trống, hiển thị thông báo lỗi bằng `alert()` hoặc hiển thị thẻ `dangerAlert` báo người dùng nhập lại, không xuất hóa đơn rác.

---


### 5. Quy chuẩn nộp bài

- **Cấu trúc thư mục dự án:**
  ```text
  ev-charging-debug/
  ├── index.html
  └── script.js
  ```
- **Quy định nộp bài:**
  - File HTML và JS phải được liên kết đúng chuẩn.
  - Trong file `script.js`, học viên cần viết comment rõ ràng các vị trí đã tiến hành Debug (ví dụ: `// FIX BUG 1: Ngăn chặn reload trang bằng event.preventDefault()`).
  - Không sử dụng Fetch API, Async/Await hay LocalStorage.

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **1. Đã sửa xong lỗi Reload Trang & Sự kiện Form** | 20đ | - Sử dụng chính xác `event.preventDefault()` trong callback sự kiện `submit`.<br>- Lắng nghe đúng sự kiện `submit` trên thẻ `<form>`. |
| **2. Đã sửa lỗi Phản hồi Thời gian thực (Real-time Input)** | 20đ | - Đổi sự kiện trên `portTemp` từ `change` sang `input`.<br>- Cảnh báo ẩn/hiện tức thì theo giá trị nhiệt độ nhập vào.<br>- Chặn không cho phép tính toán hóa đơn nếu nhiệt độ > 70°C. |
| **3. Xử lý Đúng Logic Nghiệp vụ & Ép kiểu** | 40đ | - Ép kiểu số (`parseFloat`/`Number`) chính xác cho các giá trị từ input.<br>- Tính đúng tiền điện theo từng loại cổng sạc (3.850đ hoặc 4.500đ).<br>- Tính đúng phí đỗ xe theo quy tắc miễn phí 30 phút đầu.<br>- Hiển thị đúng tổng tiền hóa đơn (`ChargingInvoice`). |
| **4. Xử lý Biên & Validation dữ liệu đầu vào** | 10đ | - Kiểm tra số kWh phải là số dương lớn hơn 0.<br>- Xử lý trường hợp người dùng nhập chữ hoặc để trống thông tin. |
| **5. Cấu trúc mã nguồn & Comment Debug** | 10đ | - Mã nguồn trình bày sạch sẻ, thụt lề chuẩn.<br>- Đặt tên biến rõ ràng, có ghi chú (comment) giải thích những điểm bị lỗi và cách khắc phục. |