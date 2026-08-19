# BẢNG TIÊU CHÍ ĐÁNH GIÁ TỔNG HỢP (100đ) - Tương tác DOM API (Document Object Model)- Truy xuất và Thay đổi Nội dung

## Bài tập 1: E-Commerce (Mức độ 1: Cơ bản - Debug lỗi)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Cấu trúc thư mục và đặt tên file đúng quy chuẩn (5đ).<br>- Trình bày code sạch sẽ, thụt lề chuẩn, khai báo biến rõ ràng (`const`/`let`) (5đ).<br>- Viết comment giải thích đầy đủ 6 điểm lỗi đã sửa đúng định dạng `FIX-BUG` (10đ). |
| **Xử lý Debug & DOM Selection** | **30đ** | - Truy xuất chính xác các phần tử DOM bằng `querySelector` / `getElementById` (10đ).<br>- Trích xuất chuỗi nội dung văn bản từ thẻ `<span>` đúng cách (`textContent` hoặc `innerText`) thay vì dùng `.value` (10đ).<br>- Phân biệt và áp dụng đúng giữa `.innerHTML` và `.textContent` khi chèn thẻ `<strong>` (10đ). |
| **Logic Nghiệp vụ Smart Home** | **30đ** | - Bóc tách chuỗi (phần tích hợp `parseInt`/`parseFloat` hoặc `replace('W', '')`) và tính toán đúng tổng Watt ($7500\text{W}$) (10đ).<br>- Tính toán chính xác Ampe ($34.09\text{A}$) có làm tròn 2 chữ số thập phân (10đ).<br>- Đánh giá đúng điều kiện quá tải ($> 6600\text{W}$) để kích hoạt hiển thị cảnh báo (10đ). |
| **Thao tác ClassList & Inline Style** | **20đ** | - Sử dụng đúng các phương thức `classList` (`add`, `remove`, `replace`) mà không ghi đè làm mất class gốc `status-badge` (10đ).<br>- Thao tác ẩn/hiện element thông qua class `hidden` hoặc thuộc tính `.style.display` đúng cú pháp chuỗi (10đ). |

---

## Bài tập 2: Logistics (Mức độ 1: Cơ bản - Debug lỗi)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết đánh giá |
| :--- | :--- | :--- |
| **Phân tích & Liệt kê lỗi (Debug Report)** | **20đ** | - Chỉ ra chính xác 7/7 lỗi trong đoạn mã ban đầu (14đ).<br/>- Giải thích đúng nguyên nhân kỹ thuật (ví dụ: `span` không có thuộc tính `.value`, `getElementById` không nhận tiền tố `#`) (6đ). |
| **Thao tác DOM API đúng cú pháp** | **30đ** | - Sử dụng đúng `document.getElementById("late-minutes")` (không dấu `#`).<br/>- Sử dụng đúng `document.querySelector(".emp-name")` (có dấu `.`).<br/>- Sử dụng `.innerText` / `.textContent` thay cho `.value` đối với các thẻ non-input.<br/>- Đọc đúng attribute `data-type` qua `.dataset.type` hoặc `.getAttribute("data-type")`.<br/>- Gán CSS class đúng qua `.className` hoặc `.classList.add()`. |
| **Xử lý Logic Chấm công & Tính lương** | **30đ** | - Áp dụng đúng điều kiện phạt đi muộn: `lateMinutes > 15`.<br/>- Tính đúng tiền OT theo hệ số ca `WEEKDAY` (1.5) hoặc `HOLIDAY` (3.0).<br/>- Tính đúng Tổng lương thực nhận = `Lương ca + OT - Phạt`.<br/>- Hiển thị đúng kết quả `390.625` VNĐ cho bộ test case mặc định. |
| **Trình bày Code & Chuẩn mực** | **20đ** | - Tuân thủ cấu trúc thư mục quy định (5đ).<br/>- Code trình bày sạch đẹp, không dư thừa console.log lỗi (5đ).<br/>- Tuân thủ phạm vi kiến thức (Không sử dụng Event Listener, Fetch, LocalStorage) (10đ). |

---

## Bài tập 3: FinTech (Mức độ 1: Cơ bản - Debug lỗi)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Phát hiện & Giải thích Lỗi (Debug Report)** | 20đ | Giải thích đúng nguyên nhân gây lỗi của cả 5 vị trí: Thứ tự load Script, HTMLCollection vs Element, `.value` trên Div, ép kiểu Attribute dữ liệu, ghi đè Class Attribute. |
| **Sửa lỗi Nhúng Script & Truy xuất DOM** | 20đ | Sử dụng đúng thuộc tính `defer` trên thẻ `<script>`. Truy xuất chính xác Element bằng `querySelector` hoặc truy cập đúng chỉ số `[0]` của `HTMLCollection`. |
| **Tính toán Nghiệp vụ BHYT & Chuyển đổi Dữ liệu** | 30đ | Ép kiểu dữ liệu `dataset` từ chuỗi sang số/boolean đúng chuẩn. Tính chính xác 80% giảm trừ BHYT (500,000 VNĐ -> 100,000 VNĐ). Cập nhật chuỗi kết quả có đơn vị "VNĐ". |
| **Thao tác Class & Cập nhật DOM Content** | 20đ | Dùng `classList.add("priority-badge")` giữ nguyên class `.badge`. Cập nhật đúng textContent cho nhãn ưu tiên và số thứ tự (`Q-008`). |
| **Cấu trúc Mã nguồn & Phong cách (Clean Code)** | 10đ | Code sạch vẽ đúng thụt lề, tên biến rõ nghĩa theo chuẩn camelCase, comment đầy đủ các bước xử lý. |

---

## Bài tập 4: Healthcare (Mức độ 2: Cơ bản - Kiểm thử I/O)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Đặt tên biến/hàm đúng chuẩn camelCase (`memberData`, `renderMemberDashboard`).<br>- Thụt lề chuẩn (2 hoặc 4 spaces), code sạch chắt lọc, có comment giải thích các bước tương tác DOM.<br>- Tổ chức file HTML/JS tách biệt đúng cấu trúc quy định. |
| **Xử lý Logic đúng nghiệp vụ** | **40đ** | - Tính toán đúng ưu đãi 12 tháng + 2 tháng (=14 tháng) (10đ).<br>- Phân loại đúng quyền lợi gói VIP vs STANDARD (10đ).<br>- Hiển thị đúng chuỗi định dạng lượt check-in (10đ).<br>- Logic phân nhánh đúng 3 trường hợp trạng thái thẻ (Đã hết hạn > Vượt quá lượt > Hợp lệ) (10đ). |
| **Thao tác DOM API & Ngoại lệ** | **20đ** | - Truy xuất chính xác các phần tử HTML thông qua `getElementById` hoặc `querySelector` (5đ).<br>- Thay đổi đúng nội dung bằng `textContent` / `innerHTML` (5đ).<br>- Thay đổi class chuẩn xác bằng `classList` (`add`, `remove`, `toggle`) hoặc `className` mà không làm mất style mặc định (5đ).<br>- Gán đúng thuộc tính `data-status` bằng `setAttribute` (5đ). |
| **Kiểm thử I/O & Xử lý dữ liệu đầu vào** | **20đ** | - Chạy đúng 100% kết quả đầu ra trực quan với ít nhất 3 Test Cases đầu vào khác nhau (Thẻ VIP hết hạn, Thẻ Standard vượt lượt check-in, Thẻ VIP hợp lệ).<br>- Không phát sinh lỗi runtime JavaScript trong Console. |

---

## Bài tập 5: CRM (Mức độ 2: Cơ bản - Kiểm thử I/O)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Đặt tên biến/hàm theo chuẩn `camelCase` có nghĩa (`distance`, `isSurge`, `totalFare`).<br>- Định dạng code thụt lề chuẩn 2/4 spaces.<br>- Thêm comment giải thích rõ ràng từng bước đọc DOM, tính toán và ghi DOM. |
| **Xử lý Logic đúng nghiệp vụ** | **40đ** | - Tính đúng giá sàn 12.000 VNĐ cho $\le 2$ km (10đ).<br>- Tính đúng giá lũy tiến 4.500 VNĐ/km cho $> 2$ km (15đ).<br>- Nhàn chính xác hệ số 1.2x khi `isSurge` là `true` và làm tròn số tiền (15đ). |
| **Xử lý Biên & Ngoại lệ** | **20đ** | - Bắt lỗi khi khoảng cách $\le 0$ hoặc `NaN` (10đ).<br>- Đổi màu chữ thông báo lỗi thành màu đỏ (`red` / `#dc3545`) và thông báo hợp lệ thành màu xanh (`green` / `#28a745`) (10đ). |
| **Thao tác DOM & Kiểm thử I/O** | **20đ** | - Đọc dữ liệu chính xác từ DOM elements/attributes (`data-distance`, `data-surge`) (10đ).<br>- Cập nhật nội dung hiển thị chính xác vào `#fare-amount` và `#trip-status` với định dạng tiền tệ Việt Nam (`VNĐ`) (10đ).<br>- Tuyệt đối không vi phạm danh sách Forbidden Scope (Event Listeners, Fetch, LocalStorage). |

---

## Bài tập 6: EdTech (Mức độ 2: Cơ bản - Kiểm thử I/O)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Đặt tên biến/hàm theo chuẩn camelCase, thể hiện rõ ngữ nghĩa domain VinFast EV Charging.<br>- Tách bạch rõ ràng giữa bước: Read Input -> Process Logic -> Write Output (DOM UI).<br>- Có comment giải thích các bước tính toán theo Business Rules. |
| **Xử lý Logic đúng nghiệp vụ** | **40đ** | - Đọc chính xác 5 tham số đầu vào từ `data-*` attributes (`data-kwh`, `data-charging-type`, `data-idle-minutes`, `data-battery`, `data-temp`).<br>- Tính chuẩn đơn giá Sạc thường / Sạc siêu nhanh.<br>- Tính chính xác phí phạt đỗ xe quá 30 phút.<br>- Tính đúng tổng hóa đơn và hiển thị định dạng chuẩn tiền tệ VNĐ (`toLocaleString('vi-VN')`). |
| **Xử lý Biên & Ngoại lệ** | **20đ** | - Xử lý trường hợp `idle-minutes` $\le 30$ (Phí phạt bằng 0 VNĐ).<br>- Chuyển đổi dữ liệu từ String sang Number an toàn (dùng `parseFloat`, `parseInt` kết hợp `isNaN` check).<br>- Xử lý trường hợp nhiệt độ vượt ngưỡng ($> 70^\circ\text{C}$) hoặc pin đầy ($\ge 100\%$) để kích hoạt chế độ tự động ngắt sạc. |
| **Thao tác DOM API & Chuẩn I/O** | **20đ** | - Thao tác DOM chuẩn xác bằng `getElementById` / `querySelector`.<br>- Thay đổi style/cảnh báo bằng `classList.add()` / `classList.remove()` hoặc `innerHTML`.<br>- Không vi phạm phạm vi cấm (Không dùng Event Listeners, Fetch API, LocalStorage). |

---

## Bài tập 7: E-Commerce (Mức độ 3: Nâng cao - Xây dựng tính năng mới)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Đặt tên biến/hàm chuẩn `camelCase`, mang ý nghĩa nghiệp vụ (5đ).<br>- Tổ chức mã nguồn sạch sẽ, tách biệt logic tính toán và logic thao tác DOM (10đ).<br>- Có comment giải thích các bước xử lý dữ liệu và DOM API (5đ). |
| **Thao tác DOM API & Dataset** | **30đ** | - Truy xuất chính xác phần tử bằng `getElementById`, `querySelector` (10đ).<br>- Trích xuất và ép kiểu đúng dữ liệu từ `dataset` ( distance, boolean flags) (10đ).<br>- Cập nhật chuẩn xác `textContent`, `innerHTML`, thao tác class qua `classList` (`add`, `remove`, `toggle`) (10đ). |
| **Xử lý Logic nghiệp vụ (Business Logic)** | **30đ** | - Tính Cước phí nền chuẩn xác theo quy tắc 2km đầu và các km tiếp theo (10đ).<br>- Tính đúng hệ số nhân phụ phí khi xảy ra đồng thời hoặc đơn lẻ (trời mưa / giờ cao điểm) (10đ).<br>- Tính chính xác mức giảm giá của các mã `GRAB20` (có giới hạn max 20k) và `TIETKIEM` (10đ). |
| **Xử lý Biên & Ngoại lệ (Edge Cases)** | **20đ** | - Kiểm soát khoảng cách không hợp lệ ($0$, số âm, `NaN`): hiển thị trạng thái lỗi trên DOM (10đ).<br>- Xử lý trường hợp không có mã giảm giá hoặc mã giảm giá không tồn tại trong hệ thống (5đ).<br>- Đảm bảo cước thanh toán không bao giờ bị âm ($Total \ge 0$) (5đ). |

---

## Bài tập 8: Logistics (Mức độ 3: Nâng cao - Xây dựng tính năng mới)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Cấu trúc HTML hợp lệ, ngữ nghĩa tốt.<br>- Đặt tên hàm/biến rõ ràng theo chuẩn `camelCase`.<br>- Tổ chức thư mục đúng yêu cầu, code sạch sẽ và có comment giải thích logic thao tác DOM. |
| **Xử lý Logic nghiệp vụ** | **40đ** | - Tính đúng 100% chi phí khám ban đầu có/không có BHYT (khám gốc 200k, BHYT giảm 80%).<br>- Phân loại chính xác bệnh nhân Ưu tiên (Tuổi $\ge 70$ hoặc Phụ nữ mang thai) và Thường.<br>- Đánh số thứ tự đúng định dạng `PRI-xxx` và `NOR-xxx`.<br>- Áp dụng đúng thuật toán sắp xếp hiển thị ưu tiên lên trước.<br>- Kiểm soát chính xác ngưỡng 5 bệnh nhân/bác sĩ/khung giờ. |
| **Thao tác DOM API & Giao diện** | **20đ** | - Truy xuất chính xác các phần tử DOM bằng `getElementById` / `querySelector`.<br>- Render bảng hàng đợi động, áp dụng đúng class CSS (`row-priority`, `row-overload`) và hiển thị badge nhãn.<br>- Hiển thị đúng các con số thống kê và tạo động thẻ alert thông báo cảnh báo bác sĩ quá tải.<br>- Không vi phạm vùng kiến thức cấm (Không dùng Event Listener). |
| **Xử lý Biên & Tối ưu performance** | **20đ** | - Báo lỗi/xử lý an toàn khi danh sách đầu vào rỗng.<br>- Tối ưu hóa số lần truy cập và thay đổi DOM (tránh render lặp không cần thiết).<br>- Định dạng tiền tệ đẹp mắt và chính xác (`40,000 VNĐ`). |

---

## Bài tập 9: FinTech (Mức độ 3: Nâng cao - Xây dựng tính năng mới)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết đánh giá |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Tổ chức mã sạch sẻ, thụt lề đúng chuẩn (2 hoặc 4 spaces).<br>- Đặt tên biến, hàm theo chuẩn `camelCase` có nghĩa (VD: `calculateEVNBill`, `totalAmperes`).<br>- Viết comment tiếng Việt đầy đủ giải thích các khối logic chính.<br>- Không thừa mã nguồn hoặc console.log dư thừa. |
| **Xử lý Logic đúng nghiệp vụ (IoT & FinTech)** | **40đ** | - **IoT Automation (15đ)**: Nhận diện chính xác điều kiện phòng trống >= 15 phút, cập nhật đúng trạng thái Điều hòa về OFF và đổi thông số Watt/Ampere về 0.<br>- **Kiểm tra Tải điện (10đ)**: Tính đúng tổng Amperes thiết bị đang ON, bật/tắt class cảnh báo `alert-danger`/`alert-success` chính xác theo mốc 30A.<br>- **Tính Tiền Điện EVN (15đ)**: Áp chuẩn công thức lũy tiến 6 bậc của EVN, tính đúng 8% VAT và làm tròn chính xác. |
| **Thao tác DOM API & Rendering** | **20đ** | - Sử dụng đúng các DOM API được phép (`getElementById`, `querySelector`, `querySelectorAll`, `dataset`, `textContent`, `innerHTML`, `classList`).<br>- Hiển thị bảng chi tiết hóa đơn EVN đẹp mắt, khớp dữ liệu.<br>- Định dạng chuẩn tiền tệ Việt Nam (`VNĐ`) với phân cách hàng nghìn.<br>- Tuân thủ quy định **KHÔNG** dùng Event Listener / Fetch / LocalStorage. |
| **Xử lý Biên & Ngoại lệ (Edge Cases)** | **20đ** | - Kiểm soát trường hợp `data-kwh` không hợp lệ (`NaN`, chuỗi rỗng, số âm): Hiển thị thông báo lỗi `#billing-error` và ẩn bảng hóa đơn.<br>- Xử lý chuẩn xác trường hợp dòng điện đúng bằng mốc ranh giới 30.0A (vẫn thuộc ngưỡng an toàn).<br>- Xử lý mượt mà khi danh sách thiết bị không có Điều hòa hoặc tất cả thiết bị đều đang OFF. |

---

## Bài tập 10: Healthcare (Mức độ 4: Phân tích & Tối ưu - Tái cấu trúc)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Phân tích & Tái cấu trúc Mã nguồn** | **20đ** | - Tách biệt hoàn toàn Business Logic (hàm thuần khiết) và DOM Rendering Logic.<br>- Mã nguồn sạch, chuẩn ES6+, đặt tên biến/hàm thể hiện đúng ngữ nghĩa nghiệp vụ ShopeeFood. |
| **Xử lý Đúng Logic Nghiệp vụ** | **40đ** | - Tính chính xác subtotal các món.<br>- Tính đúng phí giao hàng cơ bản (20k), cộng phụ phí cao điểm 10k (khung 11h-13h, 18h-20h).<br>- Áp dụng chính xác giảm 15k phí ship cho đơn > 100k (không âm phí ship).<br>- Tính chính xác tổng thanh toán cuối cùng. |
| **Tối ưu hóa Hiệu năng DOM** | **20đ** | - Thực hiện DOM Caching hiệu quả, không gọi `querySelector`/`getElementById` dư thừa.<br>- Sử dụng `DocumentFragment` để gộp việc chèn phần tử vào DOM (tránh Layout Thrashing).<br>- Sử dụng `textContent` và `classList` đúng chuẩn thay cho `innerHTML` và direct `style`. |
| **Xử lý Biên & Ngoại lệ** | **20đ** | - Phát hiện chính xác trạng thái quán đóng cửa hoặc hết hàng (`stockQuantity <= 0` hoặc `isAvailable === false`).<br>- Khóa nút thanh toán đúng chuẩn (`disabled`, `aria-disabled`), hiển thị banner lỗi đúng định dạng CSS.<br>- Xử lý an toàn dữ liệu đầu vào rỗng hoặc không hợp lệ. |

---

## Bài tập 11: CRM (Mức độ 4: Phân tích & Tối ưu - Tái cấu trúc)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Phân tích & Tái cấu trúc Mã nguồn (Refactoring Quality)** | **20đ** | - Tách biệt hoàn toàn logic đọc DOM, tính toán và ghi DOM.<br>- Loại bỏ triệt để đoạn mã lặp lại (Spaghetti/Duplicate DOM queries).<br>- Tổ chức hàm mô đun hóa (Clean Code, DRY principle). |
| **Xử lý Logic Nghiệp vụ Tính Cước** | **40đ** | - Tính đúng cước cơ bản (2km đầu 12k, từ km thứ 3 là 4.5k/km) (15đ).<br>- Tính đúng hệ số Surge 1.2x khi `data-surge="true"` (10đ).<br>- Tính đúng KM (`GRABNEW` giảm 20% max 20k, `VIPRIDE` giảm 10% max 50k) (10đ).<br>- Làm tròn tiền và không âm (5đ). |
| **Thao tác DOM API & An toàn** | **20đ** | - Sử dụng `dataset` đúng chuẩn để đọc dữ liệu thuộc tính `data-*` (5đ).<br>- Sử dụng `textContent` để cập nhật văn bản thay cho `innerHTML` (5đ).<br>- Thao tác với `classList` (`add`, `remove`, `toggle`) và thuộc tính `setAttribute`/`title` chính xác (10đ). |
| **Xử lý Biên & Dữ liệu Ngoại lệ (Edge Cases)** | **20đ** | - Khoảng cách âm ($\le 0$) hoặc không phải là số (`NaN`): Đánh dấu card lỗi `.card-error`, hiển thị `-- VNĐ` (10đ).<br>- Thuộc tính `data-surge` bị thiếu hoặc mang giá trị bất thường (5đ).<br>- Mã giảm giá không hợp lệ/đã hết hạn (5đ). |

---

## Bài tập 12: EdTech (Mức độ 4: Phân tích & Tối ưu - Tái cấu trúc)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc Code & Refactoring (Phân tích & Tối ưu)** | **20đ** | - Tổ chức mã nguồn theo đối tượng `SmartHomeManager` đúng chuẩn.<br>- Cache toàn bộ DOM selector trong `cacheDOM()`, không gọi `querySelector`/`getElementById` lặp lại trong vòng lặp.<br>- Sử dụng JSDoc và đặt tên biến theo chuẩn Clean Code. |
| **Xử lý Logic Nghiệp vụ IoT & Automation** | **40đ** | - **Rule 1 (10đ):** Cảnh báo đúng ngưỡng dòng điện 30A ($I = P / 220$), toggle class UI cảnh báo an toàn/vượt ngưỡng chuẩn xác.<br>- **Rule 2 (15đ):** Tự động lọc các thiết bị phòng trống (`vacant`) có `idle-time >= 15`, đổi `data-status="inactive"`, gán `power-watt="0"`, thêm class `.device-auto-off` và cập nhật text UI tương ứng.<br>- **Rule 3 (15đ):** Tính chính xác tiền điện EVN 6 bậc thang kèm 8% VAT, định dạng `Intl.NumberFormat` chuẩn `vi-VN`. |
| **Xử lý Biên & Dữ liệu Lỗi (Edge Cases)** | **20đ** | - Ép kiểu dữ liệu an toàn (`parseInt`, `parseFloat`), phòng ngừa `isNaN` khi thuộc tính DOM thiếu hoặc chứa ký tự lạ.<br>- Xử lý đúng trường hợp tổng kWh = 0 hoặc tổng dòng điện bằng 0.<br>- Không bị lỗi vỡ giao diện khi danh sách thiết bị rỗng. |
| **Tối ưu Hiệu năng DOM (Batch Update)** | **20đ** | - Không lạm dụng `innerHTML += ...` gây ra Reflow/Repaint liên tục.<br>- Cập nhật nội dung trực tiếp qua `.textContent` hoặc `.innerText` cho từng element nhỏ.<br>- Tốc độ xử lý tức thì, tối thiểu hóa độ phức tạp thuật toán $O(N)$. |

---

## Bài tập 13: E-Commerce (Mức độ 5: Sáng tạo - Thiết kế Mini Module)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Mô đun hóa Mã nguồn** | **20đ** | - Tổ chức mã nguồn chuẩn dạng Module/Object `ShopeeFoodEngine`.<br>- Phân chia hàm rõ ràng, nguyên tắc Single Responsibility (Mỗi hàm thực hiện đúng 1 việc).<br>- Đặt tên biến/hàm theo chuẩn camelCase, comment đầy đủ, đúng ngữ nghĩa tiếng Anh hoặc tiếng Việt technical. |
| **Thao tác DOM API & Dataset** | **20đ** | - Truy xuất chính xác các element bằng `querySelector`, `querySelectorAll`, `getElementById`.<br>- Đọc và ép kiểu dữ liệu từ `dataset` (`data-*`) chính xác.<br>- Sử dụng thành thạo `textContent`, `innerHTML`, `setAttribute`, `removeAttribute`, và API `classList` (`add`, `remove`, `contains`). |
| **Xử lý Logic Nghiệp vụ ShopeeFood** | **40đ** | - **Trạng thái Cửa hàng (10đ)**: Xử lý đúng khi đóng cửa (hiển thị banner, disable nút đặt hàng, đưa tổng tiền về 0).<br>- **Tồn kho Món ăn (10đ)**: Đánh dấu món hết hàng trên DOM, loại bỏ món 0-stock khỏi tổng tiền.<br>- **Phí Ship & Cao điểm (10đ)**: Tính đúng phí ship theo km (làm tròn lên), phụ phí khung giờ (11-13h, 18-20h), và miễn phí ship cho đơn trên 100k.<br>- **Voucher & Tổng thanh toán (10đ)**: Áp dụng voucher đúng điều kiện tối thiểu, tính tổng tiền cuối chính xác. |
| **Xử lý Biên & Ngoại lệ DOM** | **10đ** | - Xử lý an toàn khi DOM Element không tồn tại (null check trước khi truy cập).<br>- Xử lý khi danh sách món ăn rỗng hoặc tất cả các món đều hết hàng.<br>- Phí giao hàng sau khi giảm không bị âm (min = 0). |
| **Định dạng & Hiển thị UI** | **10đ** | - Định dạng tiền tệ VND chuẩn (VD: `100.000 đ`).<br>- Dynamic render danh sách tóm tắt hóa đơn chi tiết vào `#order-breakdown`.<br>- Giao diện thay đổi trực quan, đúng CSS class theo từng trạng thái nghiệp vụ. |

---

## Bài tập 14: FinTech (Mức độ 5: Sáng tạo - Thiết kế Mini Module)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | 20đ | - Thư mục và file đặt đúng quy chuẩn bài nộp.<br>- Mã nguồn JS tuân thủ mô hình Module (`CoffeePosEngine`), khai báo biến rõ ràng (`const`/`let`).<br>- Thụt lề chuẩn, comment giải thích đầy đủ các bước thao tác DOM API. |
| **Xử lý Logic đúng nghiệp vụ** | 40đ | - Tính chính xác giá từng món (Base price + Size Fee + Toppings Fee).<br>- Tính đúng Subtotal, Chiết khấu hội viên (0%, 5%, 10%) và Thuế VAT (8%).<br>- Cập nhật đầy đủ và chính xác tất cả thông tin Header, Table Rows và Summary lên DOM.<br>- Định dạng chuẩn tiền tệ VNĐ cho tất cả hiển thị số tiền. |
| **Xử lý Biên & Ngoại lệ** | 20đ | - Xử lý mảng order rỗng/null: Ẩn receipt card, hiển thị error banner đúng yêu cầu.<br>- Xử lý đúng món có giá âm hoặc size không hợp lệ (gán giá 0 và thêm suffix danh xưng lỗi). |
| **Tối ưu DOM & Thuộc tính động** | 20đ | - Sử dụng hiệu quả các API DOM (`querySelector`, `getElementById`, `classList`, `setAttribute`, `style`).<br>- Gán đúng class badge hội viên (`badge-gold`, `badge-silver`, ...).<br>- Thêm thuộc tính `data-vip-order="true"` và đổi style nền `#final-total-box` khi tổng hóa đơn > 200.000 VNĐ. |

---

## Bài tập 15: EdTech (Mức độ 5: Sáng tạo - Thiết kế Mini Module)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Architecture Module** | 20đ | - Thiết kế Module/Class rõ ràng, encapsulated tốt.<br>- Sử dụng DOM Caching (truy xuất DOM 1 lần trong `init`, lưu biến references).<br>- Không vi phạm scope cấm (Không dùng Event Listeners, Fetch API, LocalStorage). |
| **Xử lý Logic Nghiệp vụ & Giá vé** | 40đ | - Tính chính xác giá ghế VIP (+15k), Ghế Đôi (x2 + 30k).<br>- Tính chuẩn 20% giảm giá cho HS/SV trong ngày thường.<br>- Định dạng tiền tệ VND chuẩn xác (ví dụ: `150.000 VNĐ`). |
| **Thao tác DOM & Kiểm soát T18** | 20đ | - Render đúng cấu trúc sơ đồ ghế kèm theo `dataset` (`data-seat-id`, `data-seat-type`, `data-price`).<br>- Xử lý kiểm soát tuổi T18 đúng yêu cầu (thêm class `restricted-mode`, cập nhật banner cảnh báo, đặt thuộc tính `aria-disabled`). |
| **Xử lý Biên & Mã nguồn Clean Code** | 20đ | - Đọc/ghi thuộc tính DOM an toàn, xử lý danh sách ghế trống hoặc ID không tồn tại.<br>- Đặt tên biến/hàm chuẩn CamelCase, mã nguồn viết bằng tiếng Anh/Việt sạch đẹp, comment giải thích logic đầy đủ. |

---

