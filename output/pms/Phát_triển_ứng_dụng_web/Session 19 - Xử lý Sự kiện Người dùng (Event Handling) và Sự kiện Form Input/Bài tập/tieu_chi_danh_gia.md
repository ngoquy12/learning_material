# BẢNG TIÊU CHÍ ĐÁNH GIÁ TỔNG HỢP (100đ) - Xử lý Sự kiện Người dùng (Event Handling) và Sự kiện Form Input

## Bài tập 1: E-Commerce (Mức độ 1: Cơ bản - Debug lỗi)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Debug Report** | **20đ** | - Tổ chức thư mục chuẩn theo yêu cầu.<br>- Viết file `debug_report.md` liệt kê chính xác nguyên nhân và giải pháp sửa ít nhất 4 lỗi trong bài gốc. |
| **Sự kiện DOM & Prevent Default** | **25đ** | - Sử dụng `addEventListener('submit', ...)` chuẩn xác.<br>- Gọi `e.preventDefault()` để chặn hành vi reload trang.<br>- Đăng ký đúng sự kiện `input` và `change` trên các phần tử DOM. |
| **Xử lý Logic Nghiệp vụ** | **25đ** | - Ép kiểu số chuẩn xác cho `kwh` và `minutes`.<br>- Tính đúng phí đỗ quá giờ (Miễn phí 30p đầu, không bị âm tiền).<br>- Tính đúng tiền điện theo cổng sạc `STANDARD` (3.850đ) và `FAST` (4.500đ). |
| **Xử lý Biên & Validation** | **15đ** | - Catch lỗi đầu vào: số kWh $\le 0$, số phút $< 0$ hoặc để trống.<br>- Hiển thị/Ẩn thông báo lỗi trên UI phù hợp với trạng thái người dùng nhập. |
| **Trải nghiệm người dùng (UX) & Format** | **15đ** | - Tính toán real-time mượt mà khi gõ phím/thay đổi option.<br>- Định dạng số tiền có dấu phân cách hàng nghìn (ví dụ: `150,000 VNĐ` hoặc `150.000 VNĐ`). |

---

## Bài tập 2: Logistics (Mức độ 1: Cơ bản - Debug lỗi)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Báo cáo Debug & Giải thích lỗi (Debug Report)** | 20đ | Xác định đúng và giải thích chính xác nguyên nhân của 5 lỗi trong code mẫu (Form reload, String type casting, Checkbox property, Loose equality check, String concatenation). |
| **Xử lý Sự kiện Form & Ngăn ngừa mặc định** | 20đ | Sử dụng đúng `e.preventDefault()`, lắng nghe đúng sự kiện `submit` trên Form và đọc dữ liệu chính xác từ các phần tử DOM. |
| **Xử lý Logic Nghiệp vụ & Ép kiểu** | 30đ | Ép kiểu dữ liệu chuẩn xác (`parseInt`/`Number`). Tính đúng giá vé cơ bản, phụ thu ghế VIP (15.000đ), giảm giá 20% cho sinh viên ngày thường, và chặn phim 18+ chính xác. |
| **Xử lý Biên & Validation Đầu vào** | 15đ | Kiểm tra tuổi hợp lệ (`> 0`), không để trống. Hiển thị thông báo lỗi với CSS class `error` đúng theo yêu cầu khi có sự cố. |
| **Cấu trúc Mã nguồn & Phong cách viết Code** | 15đ | Mã nguồn sạch sẻ, thụt lề chuẩn, đặt tên biến rõ ràng theo chuẩn camelCase, comment giải thích code đầy đủ, tuân thủ đúng cấu trúc thư mục nộp bài. |

---

## Bài tập 3: FinTech (Mức độ 1: Cơ bản - Debug lỗi)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **1. Đã sửa xong lỗi Reload Trang & Sự kiện Form** | 20đ | - Sử dụng chính xác `event.preventDefault()` trong callback sự kiện `submit`.<br>- Lắng nghe đúng sự kiện `submit` trên thẻ `<form>`. |
| **2. Đã sửa lỗi Phản hồi Thời gian thực (Real-time Input)** | 20đ | - Đổi sự kiện trên `portTemp` từ `change` sang `input`.<br>- Cảnh báo ẩn/hiện tức thì theo giá trị nhiệt độ nhập vào.<br>- Chặn không cho phép tính toán hóa đơn nếu nhiệt độ > 70°C. |
| **3. Xử lý Đúng Logic Nghiệp vụ & Ép kiểu** | 40đ | - Ép kiểu số (`parseFloat`/`Number`) chính xác cho các giá trị từ input.<br>- Tính đúng tiền điện theo từng loại cổng sạc (3.850đ hoặc 4.500đ).<br>- Tính đúng phí đỗ xe theo quy tắc miễn phí 30 phút đầu.<br>- Hiển thị đúng tổng tiền hóa đơn (`ChargingInvoice`). |
| **4. Xử lý Biên & Validation dữ liệu đầu vào** | 10đ | - Kiểm tra số kWh phải là số dương lớn hơn 0.<br>- Xử lý trường hợp người dùng nhập chữ hoặc để trống thông tin. |
| **5. Cấu trúc mã nguồn & Comment Debug** | 10đ | - Mã nguồn trình bày sạch sẻ, thụt lề chuẩn.<br>- Đặt tên biến rõ ràng, có ghi chú (comment) giải thích những điểm bị lỗi và cách khắc phục. |

---

## Bài tập 4: Healthcare (Mức độ 2: Cơ bản - Kiểm thử I/O)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Đặt tên biến/hàm theo chuẩn `camelCase`, phân tách file HTML/CSS/JS rõ ràng (5đ).<br>- Comment mã nguồn đầy đủ, giải thích rõ các sự kiện DOM (5đ).<br>- Thụt lề chuẩn xác, mã nguồn sạch sẽ, không dư thừa code rác (10đ). |
| **Xử lý Logic nghiệp vụ & DOM Event** | **40đ** | - Sử dụng đúng `e.preventDefault()` trong sự kiện `submit` (10đ).<br>- Xử lý đúng sự kiện `change` bật/tắt ô nhập thành viên theo gói dịch vụ (10đ).<br>- Tính toán chính xác tổng chi phí (áp dụng giảm 20% cho năm) và hiển thị định dạng tiền tệ (10đ).<br>- Render chính xác Thẻ Xác Nhận thông tin khi tất cả dữ liệu hợp lệ (10đ). |
| **Xử lý Biên & Validation Input** | **20đ** | - Validate đúng tất cả các trường: Họ tên, Email (regex), Số điện thoại Việt Nam, Số lượng thành viên (1-5) (15đ).<br>- Hiển thị/xóa thông báo lỗi trực quan đúng vị trí bên dưới ô input khi dữ liệu không hợp lệ (5đ). |
| **Trải nghiệm người dùng (UX) & Tối ưu** | **20đ** | - Cập nhật tạm tính tổng tiền Real-time khi người dùng thay đổi Lựa chọn (10đ).<br>- Đơn giản, giao diện trực quan, không gặp lỗi console khi thao tác liên tục (10đ). |

---

## Bài tập 5: CRM (Mức độ 2: Cơ bản - Kiểm thử I/O)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Cấu trúc HTML/CSS/JS tách biệt rõ ràng.<br>- Đặt tên biến, hàm theo chuẩn `camelCase` (ví dụ: `calculateTripFare`, `distanceInput`).<br>- Sử dụng `const`/`let` đúng phạm vi, không dùng `var`.<br>- Code được comment đầy đủ, thụt lề chuẩn. |
| **Xử lý Logic đúng nghiệp vụ** | **40đ** | - Sử dụng đúng `event.preventDefault()` khi submit form (10đ).<br>- Tính toán chính xác Base Fare theo khoảng cách lũy tiến (10đ).<br>- Áp dụng chính xác hệ số phụ phí cao điểm / mưa (10đ).<br>- Xử lý chuẩn xác các trường hợp mã giảm giá `GRABNEW`, `TIETKIEM` và đưa tiền về tối thiểu 0 VNĐ (10đ). |
| **Xử lý Biên & Ngoại lệ** | **20đ** | - Bắt chính xác lỗi khi khoảng cách trống, bằng 0 hoặc số âm (10đ).<br>- Hiển thị thông báo lỗi rõ ràng trên UI và ẩn khối kết quả khi gặp lỗi (10đ). |
| **Tối ưu hiệu năng & Thao tác DOM** | **20đ** | - Truy xuất phần tử DOM chính xác thông qua ID/Class.<br>- Render kết quả hiển thị mượt mà, định dạng tiền tệ Việt Nam (`VNĐ`) trực quan.<br>- Xử lý chuỗi mã giảm giá linh hoạt (loại bỏ khoảng trắng `trim()`, chuyển thành chữ hoa `toUpperCase()`). |

---

## Bài tập 6: EdTech (Mức độ 2: Cơ bản - Kiểm thử I/O)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Đặt đúng các ID HTML theo yêu cầu bài toán (5đ).<br>- Đặt tên biến, hàm theo chuẩn `camelCase`, mã nguồn sạch sẻ, thụt lề chuẩn (10đ).<br>- Có ghi chú (comments) giải thích các đoạn xử lý logic (5đ). |
| **Xử lý Logic đúng nghiệp vụ** | **40đ** | - Sử dụng đúng `addEventListener` và `e.preventDefault()` để chặn submit form (10đ).<br>- Tính toán chính xác ưu đãi tặng 2 tháng cho gói 12 tháng (10đ).<br>- Tính đúng tổng chi phí khi có/không có phụ phí VIP (10đ).<br>- Đạt 100% kết quả từ bảng Kịch bản kiểm thử Test Cases (10đ). |
| **Xử lý Biên & Ngoại lệ (Validation)** | **20đ** | - Kiểm tra lỗi chuỗi rỗng/khoảng trắng đối với Họ và tên (10đ).<br>- Kiểm tra chính xác định dạng số điện thoại (10 chữ số, bắt đầu bằng số 0) (10đ). |
| **Tối ưu & Tương tác DOM** | **20đ** | - Hiển thị/ẩn chính xác các thẻ thông báo lỗi (`#error-message`) và kết quả (`#result-container`) tương ứng với từng trạng thái (10đ).<br>- Định dạng số tiền hiển thị rõ ràng, dễ đọc (VD: `5,300,000 VNĐ` hoặc `5.300.000 VNĐ`) (10đ). |

---

## Bài tập 7: E-Commerce (Mức độ 3: Nâng cao - Xây dựng tính năng mới)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết đánh giá |
| :--- | :--- | :--- |
| **1. Cấu trúc HTML/CSS & Phong cách mã nguồn** | **20đ** | - Đầy đủ thẻ HTML, đúng `id` theo yêu cầu bài toán.<br>- Code JS được tổ chức sạch sẽ, áp dụng chuẩn CamelCase, phân chia hàm rõ ràng (`renderTable`, `validateForm`, `updateGauge`).<br>- Thêm comment giải thích chi tiết logic xử lý sự kiện. |
| **2. Xử lý Sự kiện Form & Real-time Input** | **40đ** | - Sử dụng đúng `e.preventDefault()` để chặn reload trang.<br>- Sự kiện `input` trên ô cân nặng phản hồi tức thì lên thanh tải trọng `#shelfUsageBar` mà không làm giật Lag UI.<br>- Sự kiện `change` trên `#shelfType` thay đổi động luật kiểm tra nhiệt độ.<br>- Sự kiện `blur` kiểm tra đúng lỗi và hiển thị thông báo lỗi từng trường. |
| **3. Kiểm soát Quy tắc Nghiệp vụ Logistics & Biên** | **20đ** | - Chặn chính xác khi tổng tải trọng kệ vượt quá **500 kg**.<br>- Kiểm tra chính xác dải nhiệt độ Kệ Kho Lạnh (-18°C đến 5°C) và Kệ Thường (15°C đến 40°C).<br>- Validate định dạng mã Pallet (`PL-XXXX`) và chặn trùng lặp mã.<br>- Tính đúng phụ phí 25% cho Kệ Kho Lạnh và hiển thị tổng chi phí chính xác. |
| **4. Ủy quyền Sự kiện & Thao tác DOM** | **20đ** | - Áp dụng đúng kỹ thuật **Event Delegation** trên `tbody` để xử lý nút Xóa Pallet.<br>- Cập nhật trạng thái bộ nhớ (Mảng JS) đồng bộ 100% với hiển thị trên DOM sau khi thêm/xóa.<br>- Không sử dụng các công nghệ bị cấm (`fetch`, `async/await`, `localStorage`). |

---

## Bài tập 8: Logistics (Mức độ 3: Nâng cao - Xây dựng tính năng mới)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Cấu trúc HTML5 semantic, CSS sắp xếp khoa học.<br>- Mã JS sạch sẽ, chia hàm nhỏ gọn theo đúng nguyên tắc Single Responsibility.<br>- Đặt tên biến/hàm gợi nhớ, có comment giải thích các đoạn xử lý logic phức tạp. |
| **Xử lý Logic & Nghiệp vụ Gói Dịch vụ** | **40đ** | - Tính toán chính xác giá tiền theo từng Gói (Personal, Business, Enterprise) và Chu kỳ thanh toán (Monthly/Yearly - giảm 15%).<br>- Xử lý đúng hạn ngạch số lượng tài khoản con theo từng gói (Personal = 1, Business <= 5, Enterprise > 20 tính phụ trội $15/tài khoản).<br>- Render chính xác thẻ đăng ký thành công lên DOM bằng JS. |
| **Xử lý Sự kiện & Real-time Validation** | **20đ** | - Sử dụng thành thạo `addEventListener` cho các sự kiện `submit`, `input`, `blur`, `change`.<br>- Sử dụng `preventDefault()` để ngăn reload trang.<br>- Áp dụng **Event Delegation** chuẩn xác cho thao tác Xóa tài khoản con dynamic.<br>- Báo lỗi thời gian thực chi tiết (Email sai định dạng, trùng mã GPS ID, thiếu thông tin). |
| **Tối ưu Hiệu năng & Trải nghiệm Người dùng** | **20đ** | - Cập nhật giá Real-time không giật lag.<br>- Disable/Enable thông minh các nút bấm (Ví dụ: vô hiệu hóa nút thêm tài khoản khi đạt giới hạn gói).<br>- Xử lý trạng thái thông báo rõ ràng, trực quan cho người dùng. |

---

## Bài tập 9: FinTech (Mức độ 3: Nâng cao - Xây dựng tính năng mới)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết đánh giá |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20 điểm** | - Đặt tên biến, hàm theo chuẩn `camelCase`, thể hiện rõ ngữ nghĩa.<br>- Tổ chức code sạch sẻ, tách biệt giữa phần xử lý Logic (State) và Render UI.<br>- Có comment giải thích chi tiết logic nghiệp vụ phức tạp (Công thức tính phí ship, giờ cao điểm). |
| **Xử lý Sự kiện & Form (DOM Events)** | **20 điểm** | - Lắng nghe đúng và đủ các sự kiện `input`, `change`, `click`, `submit` bằng `addEventListener`.<br>- Sử dụng `e.preventDefault()` chuẩn xác khi submit Form.<br>- Truy xuất và cập nhật các phần tử DOM mượt mà, đúng kỹ thuật. |
| **Tính đúng đắn Logic Nghiệp vụ** | **40 điểm** | - Tính đúng phí giao hàng theo khoảng cách làm tròn ($15k$ cho $2km$ đầu, $+5k/km$ tiếp theo).<br>- Cộng đúng phụ phí $10k$ khi chọn khung giờ cao điểm.<br>- Giảm đúng $15k$ phí ship cho đơn từ $100k$ (không âm phí ship).<br>- Áp dụng chính xác voucher `SHOPEEFOOD50` (tối đa $30k$) và `FREESHIP`.<br>- Khóa nút/chặn đặt hàng chuẩn xác khi cửa hàng đóng cửa (`isOpen = false`). |
| **Xử lý Biên & Ngoại lệ (Edge Cases)** | **10 điểm** | - Giới hạn số lượng món theo tồn kho (`stock`), không cho chọn quá stock hoặc âm số lượng.<br>- Báo lỗi rõ ràng khi khoảng cách nhập vào $\le 0$ hoặc giỏ hàng $0$ món.<br>- Xử lý đúng khi nhập mã voucher sai/không tồn tại. |
| **Giao diện & Tương tác UX** | **10 điểm** | - Hiển thị giá tiền dạng định dạng chuẩn VND (VD: `45,000 VNĐ`).<br>- Vô hiệu hóa (disabled) trực quan các nút tăng/giảm số lượng hoặc nút Submit khi không đủ điều kiện. |
| **TỔNG ĐIỂM** | **100 điểm** | **Đạt yêu cầu khi tổng điểm $\ge 70$ điểm.** |

---

## Bài tập 10: Healthcare (Mức độ 4: Phân tích & Tối ưu - Tái cấu trúc)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết đánh giá |
| :--- | :--- | :--- |
| **Phân tích Legacy & Cấu trúc Mã nguồn** | **20đ** | - Phân tích chính xác các điểm yếu của code cũ (Memory leak, tight coupling).<br>- Tổ chức mã nguồn sạch đẹp, đặt tên biến/hàm rõ nghĩa theo quy chuẩn Clean Code.<br>- Tách biệt rõ ràng Logic nghiệp vụ, Event Handlers và DOM Rendering. |
| **Kỹ thuật Event Handling & Delegation** | **30đ** | - Sử dụng **Event Delegation** chính xác trên Container chung, không gán event listener trong hàm loop/render.<br>- Xử lý sự kiện Form submit chuẩn mực với `preventDefault()`.<br>- Lắng nghe sự kiện `input`/`blur` để phản hồi validation real-time chuyên nghiệp. |
| **Xử lý Logic Nghiệp vụ Trạm sạc** | **30đ** | - Tính chính xác phí điện sạc theo loại cổng (Regular: 3.850đ, Super Fast: 4.500đ).<br>- Áp dụng đúng quy tắc ngắt sạc an toàn (Pin = 100% hoặc Nhiệt độ > 70°C).<br>- Tính chính xác phí phạt quá giờ (Miễn phí 30p đầu khi pin 100%, từ phút 31 phạt 1.000đ/phút; Không phạt nếu ngắt do quá nhiệt). |
| **Xử lý Biên, Ngoại lệ & Tối ưu Giao diện** | **20đ** | - Validate chặt chẽ dữ liệu đầu vào (kWh, nhiệt độ, thời gian đỗ xe).<br>- Giao diện cập nhật mượt mà, không bị giật lag, hiển thị hóa đơn chi tiết, rõ ràng.<br>- Không vi phạm các phạm vi cấm (Không Async/Fetch/LocalStorage). |

---

## Bài tập 11: CRM (Mức độ 4: Phân tích & Tối ưu - Tái cấu trúc)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn (Clean Code & Structure)** | **20đ** | - Áp dụng đúng kỹ thuật Tái cấu trúc (Refactoring): Loại bỏ hoàn toàn inline HTML events và vòng lặp gán `addEventListener` trên từng item.<br>- Đặt tên biến/hàm ngữ nghĩa (`camelCase`), thụt lề chuẩn 2 spaces.<br>- Tách biệt rõ ràng giữa logic tính toán (Business Logic) và logic tương tác DOM (Event Handlers). |
| **Xử lý Logic Nghiệp vụ & Event Delegation** | **40đ** | - **Event Delegation (15đ):** Đăng ký đúng 1 listener duy nhất tại container cha, dùng `event.target.closest()` xử lý chuẩn xác hành động `toggle` và `delete`.<br>- **Cảnh báo quá tải dòng điện 30A (15đ):** Tính chính xác $I = \frac{\sum P}{220}$, chặn đúng hành vi bật thiết bị làm $I > 30\text{A}$ và render banner cảnh báo.<br>- **Tính tiền điện EVN 6 bậc (10đ):** Tính đúng chính xác theo 6 bậc thang lũy tiến của EVN. |
| **Xử lý Sự kiện Form & Input (Debounce/Validation)** | **20đ** | - **Form Validation (10đ):** Sử dụng `preventDefault()` chuẩn xác, kiểm tra đủ 3 điều kiện validation, hiển thị/ẩn error message trực quan trên UI.<br>- **Tối ưu Input với Debounce (10đ):** Triển khai cơ chế hoãn xử lý ($300\text{ms}$) cho sự kiện `input` ô tính tiền điện, không bị giật lag giao diện. |
| **Xử lý Biên & Ngoại lệ (Edge Cases)** | **20đ** | - Xử lý trường hợp nhập số kWh là âm, chữ cái, hoặc để trống.<br>- Xử lý trường hợp danh sách thiết bị rỗng hoặc khi xóa toàn bộ thiết bị.<br>- Xử lý làm tròn số Amperes chính xác 2 chữ số thập phân (`toFixed(2)`). |

---

## Bài tập 12: EdTech (Mức độ 4: Phân tích & Tối ưu - Tái cấu trúc)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc Code & Refactoring (Phân tích & Tối ưu)** | **20đ** | - Chỉ ra chính xác lỗi Memory Leak & Code duplication của legacy code.<br>- Áp dụng triệt để **Event Delegation** (không gán listener trực tiếp lên thẻ dynamic).<br>- Tách biệt hàm logic nghiệp vụ (pure function) và hàm thao tác DOM rõ ràng. |
| **Xử lý Logic Nghiệp vụ & Live Preview** | **40đ** | - Tính toán đúng 100% tổng tiền cho tất cả kết hợp (Gói x Chu kỳ x Giảm giá 20% cho Yearly).<br>- Toggle ẩn/hiện danh sách tài khoản con chính xác khi chọn Gói (Family vs Personal/Free).<br>- Quản lý chuẩn số lượng Sub-accounts (tối thiểu 1, tối đa 5 đối với gói Family). |
| **Xử lý Sự kiện Form & Realtime Validation** | **20đ** | - Sử dụng chuẩn xác các event `input`, `change`, `blur`, `submit`.<br>- Validate chính xác định dạng Email, lỗi bỏ trống.<br>- Validate lỗi trùng lặp Email (Email con trùng nhau hoặc trùng với Email chính).<br>- Sử dụng `preventDefault()` chuẩn xác khi Submit. |
| **Xử lý Biên & Trải nghiệm Người dùng (UX)** | **20đ** | - Vô hiệu hóa (Disable) nút "Thêm" khi đạt tối đa 5 tài khoản con.<br>- Hiển thị thông báo lỗi chi tiết bên dưới từng ô input lỗi.<br>- Tự động Focus vào ô input vi phạm đầu tiên khi submit không thành công.<br>- Định dạng tiền tệ đẹp mắt (`2.400.000 VNĐ`). |

---

## Bài tập 13: E-Commerce (Mức độ 5: Sáng tạo - Thiết kế Mini Module)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết đánh giá |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Cấu trúc HTML semantics, CSS sạch sẽ dễ nhìn (5đ).<br>- Code JS đặt tên rõ nghĩa (`camelCase`), có comment giải thích luồng xử lý sự kiện (5đ).<br>- Phân chia hàm hợp lý (Modular pattern/Clean Code), không viết toàn bộ logic trong event handler (10đ). |
| **Xử lý Logic & Đăng ký Sự kiện (Event Handling)** | **40đ** | - Sử dụng đúng `preventDefault()` ngăn reload trang khi submit (5đ).<br>- Lắng nghe và xử lý chuẩn xác các sự kiện `input`, `change`, `blur` để tính toán real-time preview (10đ).<br>- Thực hiện đúng kỹ thuật Event Delegation (`click`) trên container cha cho các nút động (15đ).<br>- Tính toán chính xác đơn giá điện (AC/DC) và công thức phí phạt đỗ quá giờ (10đ). |
| **Xử lý Biên & Ngoại lệ (Edge Cases & Validation)** | **20đ** | - Validate đúng định dạng biển số xe và các khoảng giá trị % pin (5đ).<br>- Ngăn chặn submit khi Pin mục tiêu <= Pin hiện tại (5đ).<br>- Xử lý chuẩn an toàn quá nhiệt (> 70°C): vô hiệu hóa nút submit và hiển thị cảnh báo trực quan (5đ).<br>- Kiểm soát số phút quá giờ (nhập số âm, nhập chữ, hoặc chưa ngắt sạc đã bấm xuất hóa đơn) (5đ). |
| **Tối ưu Hiệu năng & Trải nghiệm Người dùng (UX)** | **20đ** | - Áp dụng Event Delegation tối ưu tài nguyên bộ nhớ thay vì gán nhiều listeners (10đ).<br>- Trải nghiệm UI/UX mượt mà: Thông báo lỗi hiển thị rõ ràng bên dưới input, tự động cập nhật preview không trễ (10đ). |

---

## Bài tập 14: FinTech (Mức độ 5: Sáng tạo - Thiết kế Mini Module)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Đặt tên biến, hàm theo chuẩn CamelCase (e.g., `calculateFee`, `renderQueueTable`).<br>- Cấu trúc HTML/CSS chuẩn hóa, giao diện sạch sẽ, thân thiện.<br>- Phân chia rõ ràng giữa dữ liệu (State), xử lý sự kiện (Events) và thao tác DOM (Render). |
| **Xử lý Logic đúng nghiệp vụ** | **40đ** | - **Tính toán BHYT (10đ):** Giảm đúng 80% khi tích chọn BHYT.<br>- **Phân loại ưu tiên (10đ):** Cấp mã `PRIO-xxx` chuẩn xác cho người $\ge 70$ tuổi hoặc phụ nữ mang thai.<br>- **Quản lý Slot Capacity (10đ):** Tính chính xác số lượng lịch đặt theo Bác sĩ + Khung giờ, chặn thành công khi đạt giới hạn 5/5.<br>- **Quản lý Hàng chờ (10đ):** Render danh sách cuộc hẹn chính xác sau mỗi lần đăng ký thành công. |
| **Xử lý Tương tác Sự kiện & Validation** | **20đ** | - Sử dụng đúng `preventDefault()` để ngăn reload trang.<br>- Xử lý chuẩn xác các sự kiện `input`, `change` cho preview chi phí và hiển thị/ẩn ô Checkbox mang thai.<br>- Thống kê slot khả dụng cập nhật linh hoạt thời gian thực.<br>- Báo lỗi rõ ràng khi input không hợp lệ hoặc slot đã đầy. |
| **Tối ưu hiệu năng & Trải nghiệm (UX)** | **20đ** | - Tổ chức mã nguồn thành các hàm nhỏ có tính tái sử dụng (Clean code, No duplicate code).<br>- Không lạm dụng truy vấn DOM nhiều lần (Lưu trữ DOM Element vào biến/const).<br>- Reset Form đúng cách và cập nhật lại toàn bộ chỉ số Real-time sau khi đặt lịch thành công. |

---

## Bài tập 15: EdTech (Mức độ 5: Sáng tạo - Thiết kế Mini Module)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Áp dụng đúng mô hình Class/Module tách biệt logic DOM và Business.<br>- Đặt tên biến/hàm theo chuẩn `camelCase`, mã nguồn sạch sẽ, có comment giải thích rõ ràng. |
| **Xử lý Sự kiện & Real-time Calculation** | **40đ** | - Sử dụng chính xác các sự kiện `input`, `change`, `submit`.<br>- Tính toán chính xác 100% các công thức phụ phí (check-in sớm, trẻ em, người lớn thứ 3, dịch vụ đi kèm).<br>- Giao diện cập nhật tiền tức thì ngay khi đổi input. |
| **Form Validation & Ngoại lệ** | **20đ** | - Sử dụng `event.preventDefault()` chính xác.<br>- Validate đầy đủ logic ngày tháng (check-out > check-in), định dạng SĐT, Email, Họ tên.<br>- Hiển thị/ẩn các thông báo lỗi chi tiết ngay bên dưới các ô input (không dùng `alert`). |
| **Trải nghiệm UI & Hiển thị Hóa đơn** | **20đ** | - Render hóa đơn (`ServiceInvoice`) đẹp mắt, rõ ràng từng khoản mục tiền sau khi submit thành công.<br>- Reset form và dữ liệu hóa đơn đúng chuẩn khi đặt lại. |

---

