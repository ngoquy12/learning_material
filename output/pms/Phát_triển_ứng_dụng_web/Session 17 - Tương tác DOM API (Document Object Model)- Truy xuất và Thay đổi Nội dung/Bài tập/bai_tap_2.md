# Bài tập 2: Logistics (Mức độ 1: Cơ bản - Debug lỗi)

### 1. Mục tiêu bài tập
- **Phát hiện và sửa lỗi DOM Selection**: Nhận biết và khắc phục các lỗi cú pháp khi truy xuất phần tử DOM bằng `document.getElementById()`, `document.querySelector()`.
- **Thao tác chính xác với thuộc tính phần tử DOM**: Đọc và ghi đúng các thuộc tính nội dung (`innerText`, `textContent`, `innerHTML`) và attribute (`data-*`, `class`, `style`) thay vì nhầm lẫn với `value` trên các thẻ không phải `input`.
- **Cập nhật giao diện theo Logic Nghiệp vụ Chấm công**: Hiểu và sửa lại logic tính lương ca làm việc, tiền phạt đi muộn và tiền làm thêm giờ (OT) cho nhân viên vận tải/logistics.
- **Rèn luyện tư duy Debugging**: Phát hiện nguyên nhân làm đoạn mã bị dừng đột ngột hoặc tính toán ra kết quả `NaN` (Not a Number).

---


### 2. Bối cảnh & Mô tả bài toán
Doanh nghiệp vận tải và kho bãi **Rikkei Logistics** đang sử dụng ứng dụng web để hiển thị **Phiếu Tạm tính Lương Ca làm việc (Shift Payroll Summary)** dành cho nhân viên điều vận và tài xế. Sau khi kết thúc ca, dữ liệu thô được render ra HTML, và một đoạn mã JavaScript sẽ chịu trách nhiệm bóc tách dữ liệu từ các thẻ HTML, tính toán tiền phạt đi muộn, tiền OT, sau đó cập nhật lại kết quả lên màn hình.

Tuy nhiên, lập trình viên Junior vừa giao nộp đoạn mã JavaScript bị lỗi. Khi chạy trên trình duyệt, trang web không hiển thị đúng tổng tiền (ra kết quả `NaN`), trạng thái chuyên cần không đổi màu CSS, và một số thông tin bị mất hoàn toàn do chọn sai phần tử HTML.

Dưới đây là sơ đồ xử lý dữ liệu của trang web:

```mermaid
graph TD
    A[Đọc dữ liệu thô từ thẻ HTML<br/>Phút đi muộn, Giờ OT, Loại ca] --> B{Đi muộn > 15 phút?}
    B -- Có --|Trừ 50.000 VNĐ| C[Tính tiền phạt]
    B -- Không --|Phạt = 0 VNĐ| C
    C --> D{Loại ca làm việc?}
    D -- WEEKDAY --|OT = 150% Lương giờ| E[Tính tiền OT]
    D -- HOLIDAY --|OT = 300% Lương giờ| E
    E --> F[Tổng lương ca = Lương cơ bản 300k + Tiền OT - Tiền phạt]
    F --> G[Ghi dữ liệu mới vào DOM<br/>innerText / innerHTML / classList]
```

---


### 3. Quy tắc nghiệp vụ (Business Rules)
1. **Lương ca cơ bản (Base Shift Pay)**: `300.000 VNĐ` / ca 8 giờ (Tương đương `37.500 VNĐ/giờ`).
2. **Phạt đi muộn (Late Penalty)**:
   - Nếu số phút đi muộn (`lateMinutes`) **lớn hơn 15 phút**: Bị trừ `50.000 VNĐ`.
   - Nếu số phút đi muộn **$\le$ 15 phút**: Không bị trừ tiền phạt (`0 VNĐ`).
3. **Tiền làm thêm giờ (Overtime - OT)**:
   - Làm ngày thường (`WEEKDAY`): Lương 1 giờ OT = `37.500 * 150%` (`56.250 VNĐ/giờ`).
   - Làm ngày lễ (`HOLIDAY`): Lương 1 giờ OT = `37.500 * 300%` (`112.500 VNĐ/giờ`).
   - `Tiền OT = Số giờ OT * Lương 1 giờ OT`.
4. **Tổng lương thực nhận ca**:
   - `Tổng lương = Lương ca cơ bản + Tiền OT - Tiền phạt đi muộn`.
5. **Cập nhật trạng thái chuyên cần trên DOM**:
   - Nếu bị phạt đi muộn (> 15 phút): Đổi nội dung thẻ trạng thái thành `"Vi phạm đi muộn"` và gán class CSS `status-warning`.
   - Nếu không bị phạt ($\le$ 15 phút): Đổi nội dung thẻ trạng thái thành `"Đúng giờ"` và gán class CSS `status-success`.

---


### 4. Yêu cầu kỹ thuật & Triển khai


#### A. Cấu trúc Mã nguồn hiện tại (Bị lỗi)

**File `index.html`:**
```html
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Phiếu Tạm tính Lương Ca - Rikkei Logistics</title>
  <style>
    .card { border: 1px solid #ccc; padding: 16px; width: 350px; font-family: sans-serif; }
    .status-success { color: green; font-weight: bold; }
    .status-warning { color: red; font-weight: bold; }
  </style>
</head>
<body>
  <div class="card" id="payroll-card">
    <h2>PHIẾU TẠM TÍNH LƯƠNG</h2>
    <p>Mã nhân viên: <span id="emp-code">EMP-8821</span></p>
    <p>Tên nhân viên: <span class="emp-name">Nguyễn Văn Lái</span></p>
    <p>Số phút đi muộn: <span id="late-minutes">20</span> phút</p>
    <p>Số giờ OT: <span id="ot-hours">2.5</span> giờ</p>
    <p>Loại ca: <span id="shift-type" data-type="WEEKDAY">Ngày thường</span></p>

    <hr>
    <p>Trạng thái: <span id="attendance-status"></span></p>
    <p>Tiền phạt đi muộn: <span id="penalty-amount">0</span> VNĐ</p>
    <p>Tiền OT: <span id="ot-amount">0</span> VNĐ</p>
    <p><strong>Thực nhận ca này: <span id="total-salary">0</span> VNĐ</strong></p>
  </div>

  <script src="script.js"></script>
</body>
</html>
```

**File `script.js` (Chứa 7 lỗi sai cần debug):**
```javascript
// --- BẮT ĐẦU ĐOẠN MÃ LỖI CẦN DEBUG ---

// Lỗi 1: Truy xuất sai selector getElementById
const lateInput = document.getElementById("#late-minutes");

// Lỗi 2: Đọc dữ liệu từ thẻ <span> dùng sai thuộc tính
const lateMinutes = Number(lateInput.value);

// Lỗi 3: Dùng querySelector sai cú pháp selector cho class
const empNameEl = document.querySelector("emp-name");
console.log("Nhân viên:", empNameEl.textContent);

// Lỗi 4: Đọc custom attribute data-type bị sai cú pháp
const shiftTypeEl = document.getElementById("shift-type");
const shiftType = shiftTypeEl.getAttribute("dataset-type");

const otHours = Number(document.getElementById("ot-hours").innerText);
const baseHourlyRate = 37500;
const baseShiftPay = 300000;

// Lỗi 5: Logic so sánh phạt đi muộn bị ngược
let penalty = 0;
if (lateMinutes < 15) {
    penalty = 50000;
}

// Lỗi 6: Cập nhật nội dung thẻ span dùng sai thuộc tính .value
document.getElementById("penalty-amount").value = penalty;

// Tính tiền OT
let otRate = 1.0;
if (shiftType === "WEEKDAY") {
    otRate = 1.5;
} else if (shiftType === "HOLIDAY") {
    otRate = 3.0;
}

const otPay = otHours * baseHourlyRate * otRate;
document.getElementById("ot-amount").innerText = otPay;

// Tính tổng lương
const totalSalary = baseShiftPay + otPay - penalty;
document.getElementById("total-salary").innerText = totalSalary;

// Lỗi 7: Thay đổi Class CSS của phần tử DOM sai cú pháp
const statusEl = document.getElementById("attendance-status");
if (penalty > 0) {
    statusEl.class = "status-warning";
    statusEl.innerHTML = "Vi phạm đi muộn";
} else {
    statusEl.class = "status-success";
    statusEl.innerHTML = "Đúng giờ";
}
```

---


#### B. Yêu cầu Nhiệm vụ của Học viên

1. **Báo cáo Debug (Bắt buộc)**:
   - Tạo file `DEBUG_REPORT.md` (hoặc ghi chú trong comment mã nguồn), liệt kê rõ **7 lỗi** có trong file `script.js` ban đầu.
   - Với mỗi lỗi, giải thích rõ: *Dòng bị lỗi*, *Nguyên nhân gây ra lỗi* và *Cách khắc phục*.

2. **Sửa mã nguồn (`script.js`)**:
   - Sửa toàn bộ mã JavaScript để trang web chạy không phát sinh lỗi trong Console.
   - Tính toán chính xác theo các thông số trong HTML gốc:
     - Số phút đi muộn = `20` -> Bị phạt `50.000 VNĐ`.
     - Số giờ OT = `2.5` giờ ngày thường (`WEEKDAY`) -> Tiền OT = `2.5 * 37.500 * 1.5 = 140.625 VNĐ`.
     - Tổng thực nhận = `300.000 + 140.625 - 50.000 = 390.625 VNĐ`.
     - Trạng thái hiển thị: `"Vi phạm đi muộn"` có màu chữ đỏ (class `status-warning`).
   - Cập nhật đúng các giá trị tính toán được lên các phần tử HTML tương ứng (`#penalty-amount`, `#ot-amount`, `#total-salary`, `#attendance-status`).

3. **Phạm vi Cấm (Forbidden Scope)**:
   - Không dùng `addEventListener`, `onclick` hay các sự kiện tương tác (Session 19).
   - Không dùng `fetch`, `axios`, `LocalStorage`, `jQuery`.
   - Không sửa đổi cấu trúc HTML gốc.

---


### 5. Quy chuẩn nộp bài
- Cấu trúc thư mục dự án:
  ```text
  HRM_DOM_Debug/
  ├── index.html
  ├── script.js
  └── DEBUG_REPORT.md
  ```
- File `script.js` phải được comment rõ ràng tại các vị trí đã được debug.
- Mã nguồn chạy trực tiếp bằng cách mở file `index.html` trên trình duyệt Google Chrome/Edge.

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết đánh giá |
| :--- | :--- | :--- |
| **Phân tích & Liệt kê lỗi (Debug Report)** | **20đ** | - Chỉ ra chính xác 7/7 lỗi trong đoạn mã ban đầu (14đ).<br/>- Giải thích đúng nguyên nhân kỹ thuật (ví dụ: `span` không có thuộc tính `.value`, `getElementById` không nhận tiền tố `#`) (6đ). |
| **Thao tác DOM API đúng cú pháp** | **30đ** | - Sử dụng đúng `document.getElementById("late-minutes")` (không dấu `#`).<br/>- Sử dụng đúng `document.querySelector(".emp-name")` (có dấu `.`).<br/>- Sử dụng `.innerText` / `.textContent` thay cho `.value` đối với các thẻ non-input.<br/>- Đọc đúng attribute `data-type` qua `.dataset.type` hoặc `.getAttribute("data-type")`.<br/>- Gán CSS class đúng qua `.className` hoặc `.classList.add()`. |
| **Xử lý Logic Chấm công & Tính lương** | **30đ** | - Áp dụng đúng điều kiện phạt đi muộn: `lateMinutes > 15`.<br/>- Tính đúng tiền OT theo hệ số ca `WEEKDAY` (1.5) hoặc `HOLIDAY` (3.0).<br/>- Tính đúng Tổng lương thực nhận = `Lương ca + OT - Phạt`.<br/>- Hiển thị đúng kết quả `390.625` VNĐ cho bộ test case mặc định. |
| **Trình bày Code & Chuẩn mực** | **20đ** | - Tuân thủ cấu trúc thư mục quy định (5đ).<br/>- Code trình bày sạch đẹp, không dư thừa console.log lỗi (5đ).<br/>- Tuân thủ phạm vi kiến thức (Không sử dụng Event Listener, Fetch, LocalStorage) (10đ). |