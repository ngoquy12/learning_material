# BẢNG TIÊU CHÍ ĐÁNH GIÁ TỔNG HỢP (100đ) - Tương tác DOM API (Document Object Model)- Truy xuất và Thay đổi Nội dung

## Bài tập 1: GRAB_RIDE (Mức độ 1: Cơ bản - Debug lỗi)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Báo cáo Debug** | **20đ** | - Chỉ ra đầy đủ và giải thích đúng nguyên nhân của 5 lỗi trong starter code (10đ).<br>- Thụt lề chuẩn, đặt tên biến rõ ràng, code sạch sẽ (10đ). |
| **Xử lý Logic đúng nghiệp vụ** | **40đ** | - Tính đúng `baseFare` cho trường hợp $\le 2\text{ km}$ (12.000 VNĐ) và $> 2\text{ km}$ (12.000 + (km - 2) * 4500) (20đ).<br>- Tính đúng phụ phí `isSurge` (x1.2) và làm tròn kết quả chuẩn xác (20đ). |
| **Thao tác DOM API chính xác** | **20đ** | - Truy xuất đúng ID các phần tử (không thừa `#`, đúng tên `distance-display`) (10đ).<br>- Cập nhật nội dung text (`textContent`/`innerText`) và thuộc tính (`src`, `className`) đúng cú pháp JavaScript DOM (10đ). |
| **Xử lý Giao diện & Biên** | **20đ** | - Cập nhật đúng trạng thái và class hiển thị của Surge badge (`surge-active` / `surge-normal`) (10đ).<br>- Định dạng chuẩn chuỗi tổng tiền (vd: `30.600 VNĐ` hoặc `30600 VNĐ`) trên thẻ `<span>` (10đ). |

---

## Bài tập 2: GRAB_RIDE (Mức độ 1: Cơ bản - Debug lỗi)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Báo cáo Debug & Nhận diện lỗi** | **20đ** | - Phát hiện đủ 5 lỗi bug trong mã nguồn cho trước (10đ).<br>- Giải thích đúng nguyên nhân kỹ thuật và nghiệp vụ của từng lỗi (10đ). |
| **Sửa lỗi DOM Selection API** | **25đ** | - Sửa đúng `getElementById` (không chứa dấu `#`) (10đ).<br>- Sửa đúng `querySelector` (phải chứa dấu `.` đại diện class `.fare-amount`) (15đ). |
| **Sửa lỗi DOM Manipulation & Styling** | **25đ** | - Phân biệt và dùng đúng `innerHTML` thay vì `textContent` khi chèn thẻ HTML highlight tổng tiền (15đ).<br>- Sử dụng đúng `classList.add("status-error")` thay vì gán trực tiếp `.class` (10đ). |
| **Xử lý Logic Nghiệp vụ (Business Rules)** | **20đ** | - Tính đúng công thức cước phí lũy tiến: `12000 + (distance - 2) * 4500` (10đ).<br>- Tính đúng hệ số phụ phí `1.2x` và format đúng chuỗi tiền tệ `30.600 VNĐ` (10đ). |
| **Cấu trúc Code & Quy chuẩn nộp bài** | **10đ** | - Đặt tên file, cấu trúc thư mục đúng quy định (5đ).<br>- Mã nguồn trình bày sạch sẻ, có comment đầy đủ, không thừa code rác (5đ). |

---

## Bài tập 3: GRAB_RIDE (Mức độ 1: Cơ bản - Debug lỗi)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Phát hiện & Báo cáo lỗi (Debug Log)** | **20đ** | Liệt kê đầy đủ và chính xác ít nhất 4 lỗi có trong đoạn mã mẫu. Giải thích rõ nguyên nhân dẫn tới lỗi runtime hoặc lỗi hiển thị. |
| **Sửa lỗi DOM Selector & Thao tác thuộc tính** | **20đ** | - Sửa đúng `getElementById` không dùng dấu `#`.<br>- Dùng đúng `innerText` / `textContent` thay cho `.value` trên thẻ `<span>`.<br>- Gọi đúng phương thức `classList.add(...)`. |
| **Xử lý Ép kiểu & Logic Nghiệp vụ** | **30đ** | - Chuyển đổi đúng `data-distance` thành kiểu `Number` (`parseFloat`).<br>- Chuyển đổi/So sánh đúng `data-is-surge` (so sánh chuỗi `"true"` hoặc ép kiểu `Boolean`).<br>- Tính đúng công thức cước cơ bản: $12.000 + (5.5 - 2) \times 4.500 = 27.750$ VNĐ.<br>- Tính đúng phụ phí 1.2x: $27.750 \times 1.2 = 33.300$ VNĐ. |
| **Xử lý Biên & Chống lỗi Runtime (Null Check)** | **15đ** | - Kiểm tra null/undefined đối với phần tử DOM trước khi gán dữ liệu.<br>- Xử lý trường hợp `data-distance` bị rỗng hoặc không phải là số hợp lệ. |
| **Phong cách mã nguồn & Định dạng** | **15đ** | - Đặt tên biến rõ ràng, tuân thủ `camelCase`.<br>- Code trình bày sạch sẽ, có comment giải thích các bước fix lỗi.<br>- Định dạng tiền cước hiển thị đẹp mắt (VD: `33,300 VNĐ` hoặc `33.300 VNĐ`). |

---

## Bài tập 4: GRAB_RIDE (Mức độ 2: Cơ bản - Kiểm thử I/O)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Sử dụng đúng cú pháp DOM API (`getElementById`, `querySelector`).<br>- Đặt tên biến/hàm theo chuẩn `camelCase` (ví dụ: `calculateGrabFare`, `tripCard`).<br>- Định dạng code rõ ràng, có comment giải thích các bước thực hiện. |
| **Xử lý Logic đúng nghiệp vụ** | **40đ** | - Tính chuẩn cước phí 2 km đầu (12.000 VNĐ) và các km tiếp theo (4.500 VNĐ/km) (20đ).<br>- Áp dụng chính xác hệ số 1.2x khi `data-is-surge="true"` (10đ).<br>- Làm tròn số tiền chính xác và định dạng chuỗi VNĐ đúng quy định (10đ). |
| **Xử lý Biên & Ngoại lệ (I/O Validation)** | **20đ** | - Bắt lỗi thành công trường hợp `distance <= 0`, `NaN`, hoặc chuỗi không hợp lệ (10đ).<br>- Cập nhật đúng thông điệp lỗi và thay đổi style/class tương ứng trên DOM khi gặp dữ liệu lỗi (10đ). |
| **Tác động & Cập nhật DOM** | **20đ** | - Đọc dữ liệu đúng từ `dataset` của DOM (5đ).<br>- Cập nhật chính xác `textContent` / `innerHTML` cho thẻ `#total-fare` và `#fare-detail` (10đ).<br>- Thay đổi `style.color` hoặc `classList` đúng mô tả cho thẻ `#status-badge` (5đ). |

---

## Bài tập 5: GRAB_RIDE (Mức độ 2: Cơ bản - Kiểm thử I/O)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Sử dụng đúng các phương thức DOM API (`getElementById`, `querySelector`).<br>- Đặt tên biến rõ ràng, đúng chuẩn `camelCase`.<br>- Code sạch sẻ, có comment giải thích các bước truy xuất và cập nhật DOM. |
| **Xử lý Logic đúng nghiệp vụ** | **40đ** | - Đọc chính xác thuộc tính `data-distance` và `data-weather` từ DOM.<br>- Tính chính xác cước gốc cho $d \le 2$ km (12.000 VNĐ) và $d > 2$ km.<br>- Áp dụng chuẩn hệ số phụ phí thời tiết (1.2x cho `rain`, 1.0x cho `clear`).<br>- Tính đúng tổng cước cuối cùng và làm tròn hợp lý. |
| **Xử lý Biên & Ngoại lệ** | **20đ** | - Kiểm tra và xử lý thỏa đáng trường hợp $d \le 0$ hoặc `NaN`.<br>- Cập nhật giao diện cảnh báo lỗi đúng yêu cầu (class `text-danger`, thông báo lỗi). |
| **Thao tác DOM & Định dạng Output** | **20đ** | - Đổi class giao diện linh hoạt (`classList.add`/`classList.remove` hoặc `className`).<br>- Định dạng số tiền chính xác chuẩn Việt Nam (có hậu tố `VNĐ`).<br>- Không dùng các kỹ thuật cấm (Event Listener, Form Submit, LocalStorage). |

---

## Bài tập 6: GRAB_RIDE (Mức độ 2: Cơ bản - Kiểm thử I/O)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Đặt tên biến rõ ràng, tuân thủ camelCase (`baseFare`, `totalFare`, `isSurge`).<br>- Thụt lề chuẩn, comment giải thích logic ngắn gọn.<br>- Truy xuất DOM đúng phương thức (`getElementById` / `querySelector`). |
| **Xử lý Logic đúng nghiệp vụ** | **40đ** | - **Test Case 1 (15đ)**: $S = 1.5$ km, `surge = false` $\rightarrow$ Base: `12.000 VNĐ`, Surge: `0 VNĐ`, Total: `12.000 VNĐ`.<br>- **Test Case 2 (15đ)**: $S = 5$ km, `surge = true` $\rightarrow$ Base: `25.500 VNĐ`, Surge: `5.100 VNĐ`, Total: `30.600 VNĐ`.<br>- **Test Case 3 (10đ)**: $S = 20$ km, `surge = true` $\rightarrow$ Total: `111.600 VNĐ` (Tính đúng cước lũy tiến). |
| **Xử lý Biên & Ngoại lệ** | **20đ** | - **Test Case 4 (10đ)**: $S = 0$ hoặc $S = -3$ hoặc $S = "abc"$ $\rightarrow$ Hiển thị `"Dữ liệu khoảng cách không hợp lệ"` tại `#total-fare` và gắn class `error`.<br>- **Test Case 5 (10đ)**: Khi Tổng tiền $> 100.000$ VNĐ $\rightarrow$ Thêm class `high-fare` vào phần tử `#total-fare`. |
| **Thao tác DOM & Định dạng** | **20đ** | - Sử dụng đúng `innerText`/`textContent` để cập nhật nội dung.<br>- Thao tác class chuẩn xác bằng `classList.add()`.<br>- Định dạng đơn vị tiền tệ rõ ràng, không làm biến đổi cấu trúc HTML ban đầu.<br>- Tuyệt đối không dùng Event Listener hay Form Submit. |

---

## Bài tập 7: GRAB_RIDE (Mức độ 3: Nâng cao - Xây dựng tính năng mới)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Truy xuất DOM API** | **20 điểm** | - Sử dụng đúng các phương thức `document.getElementById`, `querySelector`, `querySelectorAll`.<br>- Cập nhật chính xác `dataset`, `setAttribute`, `classList` (thêm/xóa lớp `d-none`, `badge-surge`).<br>- Thụt lề chuẩn, comment giải thích code rõ ràng. |
| **Logic Nghiệp vụ & Công thức Cước phí** | **40 điểm** | - Tính đúng cước khoảng cách lũy tiến ($2\text{ km}$ đầu $12.000\text{đ}$, từ $\text{km}$ 3 tính $4.500\text{đ/km}$).<br>- Tính chính xác hệ số phụ phí khi mưa/giờ cao điểm ($1.2\text{x}$ hoặc $1.3\text{x}$).<br>- Tính chính xác giảm giá theo mã `GRABNEW` (tối đa $15.000\text{đ}$) hoặc `TIETKIEM` ($\ge 30.000\text{đ}$).<br>- Định dạng chuẩn tiền tệ VNĐ trên giao diện. |
| **Render Giao diện & Đổ Dữ liệu Động** | **20 điểm** | - Đổ đầy đủ thông tin chuyến đi vào các thẻ HTML tương ứng.<br>- Sử dụng `innerHTML` để render dynamic HTML cho thông tin tài xế đúng thiết kế.<br>- Cập nhật đúng các thuộc tính `data-*` trên container node. |
| **Xử lý Ngoại lệ & Kiểm soát Phạm vi** | **20 điểm** | - Hiển thị đúng thông báo lỗi trên DOM khi `distanceKm` không hợp lệ ($< 0.1\text{ km}$ hoặc sai kiểu dữ liệu).<br>- Không vi phạm vùng cấm: Không sử dụng `addEventListener`, không `fetch`, không `localStorage`. |

---

## Bài tập 8: GRAB_RIDE (Mức độ 3: Nâng cao - Xây dựng tính năng mới)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Tổ chức mã nguồn sạch sẽ, tách hàm rõ ràng theo đúng yêu cầu.<br>- Đặt tên biến/hàm chuẩn camelCase, theo ngữ cảnh GrabRide (`calculateTripFare`, `renderDriverCard`).<br>- Thụt lề chuẩn 2 spaces, có comment giải thích cho từng đoạn xử lý DOM. |
| **Xử lý Logic đúng nghiệp vụ** | **40đ** | - **Cước cơ bản (15đ)**: Tính đúng $2\text{ km}$ đầu 12k, các km sau 4.5k/km.<br>- **Phụ phí Surge (15đ)**: Đúng hệ số $1.2\text{x}$ (mưa hoặc cao điểm) và $1.4\text{x}$ (cả hai).<br>- **Mã giảm giá (10đ)**: Tính đúng giảm $20\%$ max 15k cho `GRABDIWUI` và giảm 10k cho `CHAOXINCHAO`. |
| **Thao tác DOM API & Xử lý Biên** | **20đ** | - Sử dụng chính xác `getElementById`, `querySelector`, `classList`, `setAttribute`.<br>- Định dạng số tiền chính xác (thêm chấm phân cách hàng nghìn và đuôi `"VNĐ"`).<br>- Kiểm soát biên: Khoảng cách âm hoặc $= 0$, mã giảm giá không hợp lệ không làm crash script. |
| **Tối ưu UI & Ẩn/Hiện trạng thái** | **20đ** | - Hiển thị đúng Badge trạng thái tài xế theo từng màu tương ứng.<br>- Thao tác class `d-none` thành công để bật/tắt `#surge-alert`.<br>- Thay đổi màu sắc đánh giá sao (`#driver-rating`) linh hoạt theo điều kiện điểm số. |

---

## Bài tập 9: GRAB_RIDE (Mức độ 3: Nâng cao - Xây dựng tính năng mới)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Tổ chức mã nguồn sạch sẻ, chia nhỏ hàm xử lý rõ ràng (`calculateTripFare`, `updateSurgeUI`, `updateDriverUI`, `renderTripSummary`).<br>- Đặt tên biến và hàm chuẩn camelCase, có comment giải thích rõ các bước truy xuất DOM. |
| **Xử lý Logic nghiệp vụ (Business Logic)** | **40đ** | - Tính đúng cước cơ bản (2km đầu 12k, km sau 4.5k/km) (15đ).<br>- Tính chính xác phụ phí Surge x1.2 khi `isSurge = true` (10đ).<br>- Áp dụng đúng công thức giảm giá cho mã `GRABNEW` (-20%) và `SAIGONXANH` (-10k) (15đ). |
| **Thao tác DOM API & Định dạng** | **20đ** | - Sử dụng thành thạo `getElementById` / `querySelector` để đọc và ghi nội dung (8đ).<br>- Sử dụng đúng `textContent` / `innerHTML` cho thẻ text và badge (6đ).<br>- Cập nhật linh hoạt `classList` (`surge-active`, `vip-driver`) và thuộc tính CSS `style` (6đ). |
| **Xử lý Biên & Ngoại lệ (Edge Cases)** | **20đ** | - Xử lý trường hợp quãng đường $d \le 0$ hoặc không phải số hợp lệ (5đ).<br>- Xử lý trường hợp số tiền giảm giá lớn hơn tổng tiền sau surge (không để tổng tiền bị âm) (5đ).<br>- Xử lý mã giảm giá không tồn tại/rỗng (5đ).<br>- Định dạng tiền tệ VNĐ chính xác với dấu phân cách hàng nghìn (5đ). |

---

## Bài tập 10: GRAB_RIDE (Mức độ 4: Phân tích & Tối ưu - Tái cấu trúc)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Phân tích & Nhận diện Code Smell** | 15đ | - Trích xuất đúng 4 điểm yếu chính của đoạn mã Legacy (Hiệu năng DOM query, Reflow do `innerHTML`, tính toán sai nghiệp vụ km, thiếu validation). |
| **Cấu trúc & Phong cách mã nguồn** | 15đ | - Áp dụng mô hình thiết kế rõ ràng (Object Literal / Class / Module Pattern).<br>- Đặt tên hàm/biến chuẩn Clean Code (camelCase), comment giải thích logic đầy đủ. |
| **Xử lý Logic Nghiệp vụ (GrabRide Rules)** | 35đ | - Tính chính xác cước 2km đầu ($12.000\text{đ}$) và km thứ 3 trở đi ($4.500\text{đ/km}$).<br>- Áp dụng chính xác phụ phí $1.2\text{x}$ khi mưa/giờ cao điểm.<br>- Tính chính xác giảm giá cho mã `"GRAB20"` và `"GRAB50"` đúng trần max discount.<br>- Trả về kết quả tính toán chính xác với dữ liệu mẫu. |
| **Tối ưu DOM API & An toàn** | 20đ | - Thực hiện Cache DOM Node thành công (không gọi lại `querySelector`/`getElementById` trong hàm render).<br>- Tuyệt đối sử dụng `textContent` thay cho `innerHTML` khi hiển thị chuỗi văn bản.<br>- Sử dụng thành thạo `classList.add/remove/toggle` và `dataset`. |
| **Xử lý Biên & Ngoại lệ (Edge Cases)** | 15đ | - Kiểm soát tốt dữ liệu đầu vào bị âm, `NaN`, hoặc `null/undefined`.<br>- Hiển thị trạng thái lỗi trực quan lên UI khi dữ liệu không hợp lệ.<br>- Không làm sập chương trình khi thiếu tham số mã giảm giá. |

---

## Bài tập 11: GRAB_RIDE (Mức độ 4: Phân tích & Tối ưu - Tái cấu trúc)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Phân tích & Tái cấu trúc Kiến trúc** | **20đ** | - File `README.md` chỉ ra chính xác 4 lỗi code smell của mã nguồn cũ.<br>- Mã nguồn mới được chia nhỏ thành các hàm có trách nhiệm riêng biệt (Pure Function tính cước, Function tạo Node, Function render, Function update summary). |
| **Thao tác DOM API & Tối ưu hiệu năng** | **20đ** | - Cache thành công các element DOM cố định.<br>- Sử dụng `DocumentFragment` để batching DOM node.<br>- Không gọi `document.getElementById/querySelector` bên trong vòng lặp.<br>- Sử dụng `textContent` thay cho `innerHTML` để chống XSS. |
| **Logic Nghiệp vụ & Chính xác dữ liệu** | **40đ** | - Tính đúng cước phí 2km đầu ($12.000$) và từ km thứ 3 ($4.500$/km).<br>- Tính đúng hệ số phụ phí `isSurge` ($1.2x$).<br>- Định dạng chuẩn tiền tệ VNĐ.<br>- Tính chính xác tổng doanh thu và tổng số chuyến VIP trên Dashboard. |
| **Xử lý Biên & Ngoại lệ** | **10đ** | - Xử lý an toàn khi mảng chuyến đi rỗng.<br>- Xử lý đúng dữ liệu `distance` không hợp lệ ($\le 0$, `null`, `undefined`, chuỗi không phải số).<br>- Xử lý dữ liệu chuỗi nguy hiểm (HTML injection) không bị thực thi script. |
| **Phong cách Mã nguồn & Quy chuẩn UI** | **10đ** | - Đặt tên biến/hàm theo chuẩn CamelCase rõ nghĩa (`calculateTripFare`, `createTripCardNode`).<br>- CSS phân định rõ các class (`trip-card`, `trip-card--vip`, `trip-card--standard`).<br>- Thụt lề chuẩn, comment giải thích logic rõ ràng. |

---

## Bài tập 12: GRAB_RIDE (Mức độ 4: Phân tích & Tối ưu - Tái cấu trúc)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Phân tích & Kiến trúc Mã nguồn** | 20đ | - Chỉ ra chính xác ít nhất 4 lỗi trong đoạn mã legacy (Reflow/Repaint, DOM Query in Loop, Coupling Logic & UI, Lack of Validation).<br>- Tách biệt hoàn toàn hàm pure logic (`calculateTripFare`) và hàm thao tác DOM (`renderTripDashboard`). |
| **Xử lý Logic đúng nghiệp vụ** | 40đ | - Tính chính xác cước 2km đầu (12.000đ) và từ km thứ 3 (4.500đ/km).<br>- Tính chính xác hệ số phụ phí 1.2x khi `isSurge = true` và làm tròn số (`Math.round`).<br>- Thống kê chính xác tổng doanh thu và đếm đúng số chuyến đường dài ($\ge 10\text{ km}$). |
| **Xử lý Biên & Ngoại lệ** | 20đ | - Xử lý an toàn các trường hợp `distance <= 0`, dữ liệu rỗng hoặc không phải dạng số.<br>- Đánh dấu giao diện trực quan cho chuyến đi không hợp lệ (class `.trip-invalid`).<br>- Định dạng số tiền hiển thị chuẩn tiếng Việt (dùng `toLocaleString('vi-VN')` hoặc hàm tự viết). |
| **Tối ưu Hiệu năng DOM API** | 20đ | - **Bắt buộc:** Cache các DOM element references bên ngoài vòng lặp.<br>- **Bắt buộc:** Gom nhóm thao tác DOM (chèn danh sách chuyến đi bằng 1 lệnh DOM update duy nhất).<br>- Sử dụng `textContent` thay cho `innerHTML` tại các vị trí hiển thị text thuần túy. Không sử dụng các Event Listeners hay API bị cấm. |

---

## Bài tập 13: GRAB_RIDE (Mức độ 5: Sáng tạo - Thiết kế Mini Module)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết đánh giá |
| :--- | :--- | :--- |
| **1. Cấu trúc Module & Phong cách mã nguồn** | **20 điểm** | - Đóng gói logic sạch sẻ trong Mini Module `GrabFareModule` (10đ).<br>- Đặt tên biến/hàm theo chuẩn camelCase, rõ nghĩa, comment mã nguồn đầy đủ (5đ).<br>- Định dạng mã nguồn chuẩn ES6, thụt lề nhất quán (5đ). |
| **2. Xử lý Logic Nghiệp vụ (Business Rules)** | **40 điểm** | - Tính đúng Cước cơ bản ($12k$ cho 2km đầu, $4.5k$ cho các km tiếp theo) (10đ).<br>- Tính chính xác hệ số Surge Pricing khi mưa / giờ cao điểm và trường hợp kết hợp (1.2x * 1.2x = 1.44x) (10đ).<br>- Xử lý chuẩn xác 2 mã Promo `GRAB20`, `GRABNEW` và các trường hợp mã sai/rỗng (10đ).<br>- Tổng tiền thanh toán không âm và định dạng VNĐ chính xác (10đ). |
| **3. Thao tác DOM API & Rendering UI** | **20 điểm** | - Truy xuất chính xác các DOM Element thông qua `getElementById` / `querySelector` (5đ).<br>- Sử dụng thành thạo `textContent` / `innerText` cho văn bản và `innerHTML` cho HTML động (5đ).<br>- Cập nhật thuộc tính đúng chuẩn (`setAttribute` cho `src`, `alt` của ảnh) (5đ).<br>- Thao tác class động (`classList.add`, `classList.remove`, `toggle`) để thay đổi trạng thái UI/Badge (5đ). |
| **4. Xử lý Biên & Ngoại lệ (Edge Cases)** | **20 điểm** | - Kiểm soát khoảng cách âm hoặc bằng 0 ($d \le 0$), chuyển đổi trạng thái hiển thị giao diện báo lỗi (10đ).<br>- Xử lý an toàn khi thiếu thông tin tài xế hoặc promo code bị sai định dạng (chữ hoa/chữ thường) (5đ).<br>- Tuân thủ 100% phạm vi kỹ thuật (Không sử dụng Event Listener, Fetch, LocalStorage) (5đ). |

---

## Bài tập 14: GRAB_RIDE (Mức độ 5: Sáng tạo - Thiết kế Mini Module)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **1. Cấu trúc & Thao tác DOM API** | **20đ** | - Sử dụng chính xác các hàm truy xuất DOM (`getElementById`, `querySelector`).<br>- Thao tác đúng thuộc tính DOM (`textContent` cho văn bản thuần, `innerHTML` cho thẻ danh sách `<li>`).<br>- Sử dụng đúng `classList` (`add`/`remove`) và `style.display` để ẩn/hiện element theo trạng thái nghiệp vụ. |
| **2. Logic Nghiệp vụ & Khái toán Cước phí** | **40đ** | - Tính đúng Base Fare theo mốc 2 km đầu (12.000 VNĐ) và các km tiếp theo (4.500 VNĐ/km).<br>- Tính đúng Surge Multiplier khi mưa (`1.2`), giờ cao điểm (`1.2`) hoặc cả 2 (`1.44`).<br>- Áp dụng đúng quy tắc tính mã giảm giá (`GRABXANH`, `TEACHERCHILL` max 15.000 VNĐ).<br>- Định dạng chuẩn tiền tệ VNĐ trên giao diện. |
| **3. Xử lý Trạng thái & Fallback UI (Biên/Ngoại lệ)** | **20đ** | - Ẩn/Hiện đúng giữa `#error-banner` và `#trip-card` khi `distanceKm` không hợp lệ ($\le 0$ hoặc không phải số).<br>- Hiển thị đúng trạng thái tài xế: Khi có tên -> đổi class thành màu xanh `text-success`; Khi thiếu tên tài xế -> hiển thị `"Đang tìm tài xế..."` kèm class cảnh báo `text-warning`. |
| **4. Tối ưu mã nguồn & Kiến trúc Module** | **20đ** | - Code sạch sẽ, chia nhỏ logic xử lý tính toán và logic DOM thành các hàm helper (ví dụ: `calculateFare`, `formatVND`).<br>- Tuân thủ 100% phạm vi kiến thức (Không vi phạm các kiến thức cấm như Event Listener hay LocalStorage).<br>- Comment code rõ ràng, chuyên nghiệp. |

---

## Bài tập 15: GRAB_RIDE (Mức độ 5: Sáng tạo - Thiết kế Mini Module)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **1. Cấu trúc Module & Phong cách mã nguồn** | **20đ** | - Thiết kế module `GrabFareApp` rõ ràng, tách biệt logic tính toán và logic thao tác DOM (10đ).<br>- Định dạng code chuẩn JavaScript (CamelCase, thụt lề, comment giải thích đầy đủ) (10đ). |
| **2. Logic Nghiệp vụ Tính toán Cước phí** | **30đ** | - Tính đúng Cước cơ bản (2km đầu 12k, km tiếp theo 4.5k/km) (10đ).<br>- Tính đúng Phụ phí thời tiết/cao điểm (hệ số 1.2x) (10đ).<br>- Áp dụng chính xác quy tắc của các mã giảm giá `GRABNEW`, `XEMAY10` (10đ). |
| **3. Thao tác DOM API & Cập nhật Giao diện** | **30đ** | - Truy xuất chính xác các phần tử DOM qua ID/Class theo yêu cầu (10đ).<br>- Cập nhật nội dung văn bản (`textContent`) và định dạng tiền tệ Việt Nam (`toLocaleString`) chuẩn xác (10đ).<br>- Thao tác thuộc tính linh hoạt (`setAttribute` cho ảnh đại diện, `classList` cho Badge trạng thái) (10đ). |
| **4. Xử lý Biên & Ngoại lệ (Edge Cases)** | **20đ** | - Hiển thị lỗi rõ ràng khi dữ liệu khoảng cách không hợp lệ ($D \le 0$) qua `#alert-box` và ẩn bảng tính tiền (10đ).<br>- Xử lý an toàn khi mã giảm giá không tồn tại hoặc giảm giá vượt quá tổng tiền (10đ). |
| **Tổng điểm** | **100đ** | **Đạt yêu cầu tối thiểu: 70/100 điểm.** |

---

