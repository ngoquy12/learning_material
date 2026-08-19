# BẢNG TIÊU CHÍ ĐÁNH GIÁ TỔNG HỢP (100đ) - Tương tác DOM API (Document Object Model)- Truy xuất và Thay đổi Nội dung

## Bài tập 1: E-Commerce (Mức độ 1: Cơ bản - Debug lỗi)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Debug Code** | 20đ | - Tìm đủ và giải thích đúng nguyên nhân gây ra 5 lỗi trong code ban đầu.<br>- Mã nguồn sạch đẹp, tuân thủ chuẩn đặt tên biến CamelCase. |
| **Truy xuất DOM API chuẩn xác** | 25đ | - Sử dụng đúng `document.getElementById()` hoặc `document.querySelector()` đúng cú pháp selector (`#` cho ID, `.` cho Class).<br>- Phân biệt rõ đối tượng đơn lẻ và HTMLCollection/NodeList. |
| **Thao tác Thay đổi Nội dung DOM** | 25đ | - Dùng đúng `textContent` cho văn bản thuần (Text node).<br>- Dùng đúng `innerHTML` khi cần chèn chuỗi HTML có chứa các thẻ element (`<span>`, `<ul>`, `<li>`).<br>- Không dùng thuộc tính `.value` cho các thẻ không phải Form Input (`<h2>`, `<p>`). |
| **Xử lý Logic Nghiệp vụ SaaS** | 20đ | - Cập nhật chính xác các thông tin: Tên gói, Trạng thái quá hạn, Giới hạn thiết bị, Giới hạn tài khoản con.<br>- Render danh sách tính năng dạng danh sách HTML đầy đủ. |
| **Xử lý Biên & Mã an toàn** | 10đ | - Đảm bảo script thực thi không bắn lỗi Uncaught TypeError trên Console trình duyệt.<br>- Kiểm tra trường hợp dữ liệu danh sách `features` bị rỗng. |

---

## Bài tập 2: Logistics (Mức độ 1: Cơ bản - Debug lỗi)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Phát hiện & Fix lỗi Selector** | 20đ | - Sửa đúng `getElementById("pnr-code")` (bỏ `#`) (10đ).<br>- Sử dụng đúng `getElementsByClassName("passenger-name")[0]` hoặc đổi sang `querySelector` (10đ). |
| **Phát hiện & Fix lỗi Nội dung DOM** | 20đ | - Sửa thuộc tính `.value` thành `textContent` / `innerText` cho thẻ `span#ticket-class` (10đ).<br>- Sửa lỗi gọi hàm `innerHTML(...)` thành gán giá trị `innerHTML = ...` hoặc `textContent = ...` (10đ). |
| **Xử lý Logic Nghiệp vụ & Class** | 40đ | - Tính toán đúng phí hành lý theo hạng vé `Business` (0 VNĐ) và `Eco` (40đ).<br>- Thao tác class đúng kỹ thuật với `classList.remove()` và `classList.add()` (hoặc `className`) thay vì gán vào `.style`.<br>- Cập nhật đúng nội dung văn bản cho `#status-badge`. |
| **Thao tác Attribute & Trạng thái Nút** | 20đ | - Kiểm tra điều kiện phí quá cước để gỡ bỏ thuộc tính `disabled` bằng `removeAttribute("disabled")` hoặc `.disabled = false` khi hợp lệ.<br>- Mã nguồn sạch đẹp, có comment giải thích rõ ràng các điểm lỗi đã sửa. |
| **Tổng điểm** | **100đ** | **Đạt từ 80đ trở lên là ĐẠT (PASS)** |

---

## Bài tập 3: FinTech (Mức độ 1: Cơ bản - Debug lỗi)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Báo cáo Debug** | 20đ | - Thư mục bài nộp đúng chuẩn quy định.<br>- Viết comment mô tả chính xác 4 lỗi kỹ thuật trong đoạn mã ban đầu, nêu rõ nguyên nhân gây ra lỗi. |
| **Xử lý Logic & Sửa Lỗi DOM** | 40đ | - Sửa đúng lỗi lấy phần tử từ `getElementsByClassName` hoặc dùng `querySelector` hợp lý (10đ).<br>- Ép kiểu dữ liệu `Number` chính xác trước khi tính toán tài chính (10đ).<br>- Phân biệt và dùng đúng `innerHTML` thay cho `textContent` khi chèn đoạn mã chứa thẻ HTML (10đ).<br>- Đổi thuộc tính `.value` thành `.textContent` hoặc `.innerText` cho thẻ `span` (10đ). |
| **Tính toán Nghiệp vụ FinTech** | 20đ | - Tính chính xác Lương 1 giờ tiêu chuẩn, Lương OT (150%) và Tiền phạt đi muộn theo đúng quy tắc nghiệp vụ (10đ).<br>- Định dạng số tiền chính xác theo chuẩn tiền tệ Việt Nam (`VNĐ`) (10đ). |
| **Thao tác Style & Hiệu năng** | 20đ | - Thao tác thêm class CSS (`classList.add('text-danger')`) hoạt động đúng (10đ).<br>- Mã nguồn sạch đẹp, biến đặt tên theo chuẩn camelCase, không có đoạn code thừa hoặc câu lệnh thừa gây ảnh hưởng hiệu năng DOM (10đ). |

---

## Bài tập 4: Healthcare (Mức độ 2: Cơ bản - Kiểm thử I/O)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | 20đ | - Đặt tên biến, tên hàm rõ nghĩa theo chuẩn camelCase.<br>- Sử dụng đúng phương thức truy xuất DOM (`getElementById`, `querySelector`).<br>- Thụt lề chuẩn xác, mã nguồn sạch sẽ, có comment giải thích logic. |
| **Xử lý Logic đúng nghiệp vụ** | 40đ | - Tính chính xác phụ thu VIP (15.000 VNĐ) và ưu đãi HSSV ngày thường (20%).<br>- Cập nhật chuẩn xác nội dung text và HTML tương ứng vào DOM (`textContent`, `innerHTML`).<br>- Định dạng chuẩn chuỗi hiển thị giá tiền (có dấu chấm phân cách hàng nghìn và đơn vị `VNĐ`). |
| **Xử lý Biên & Ngoại lệ** | 20đ | - Kiểm tra điều kiện giới hạn tuổi (dưới 18 tuổi đăng ký dịch vụ `isRestricted18Plus = true`).<br>- Reset đầy đủ trạng thái các phần tử DOM về giá trị mặc định `"--"` khi vi phạm điều kiện.<br>- Cập nhật chính xác danh sách lớp CSS (`status-success`, `status-error`). |
| **Tối ưu hiệu năng & Phạm vi cho phép** | 20đ | - Tuyệt đối không dùng Event Listener hay Form Submit (đúng yêu cầu Session 17).<br>- Tránh truy xuất lặp đi lặp lại cùng một phần tử DOM nhiều lần (nên lưu vào biến tạm).<br>- Không làm thừa/dư thuộc tính trên cây DOM. |

---

## Bài tập 5: CRM (Mức độ 2: Cơ bản - Kiểm thử I/O)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Đặt tên biến/hàm đúng chuẩn camelCase, có ý nghĩa nghiệp vụ CRM (`planType`, `overdueDays`, `accountItems`).<br>- Thụt lề chuẩn (2 hoặc 4 spaces), mã nguồn sạch sẻ, có comment giải thích từng bước xử lý DOM.<br>- Không thừa code rác hoặc console.log dư thừa. |
| **Xử lý Logic đúng nghiệp vụ** | **40đ** | - Truy xuất chính xác thông tin từ `data-* attributes` (10đ).<br>- Xử lý đúng logic hạ cấp gói xuống "Free" khi trễ hạn > 3 ngày, hiển thị thông báo warning chính xác (15đ).<br>- Render chính xác HTML tính năng (`#feature-list`) dựa trên loại gói sau cùng (15đ). |
| **Xử lý Biên & Ngoại lệ** | **20đ** | - Đánh dấu đúng các phần tử tài khoản dư thừa bằng `classList.add('account-error')` theo từng loại gói (`family`: >5, `individual`/`free`: >1) (15đ).<br>- Cập nhật chính xác tổng số tài khoản lên `#account-count` (5đ). |
| **Tối ưu hiệu năng & DOM Manipulation** | **20đ** | - Chọn đúng phương thức truy xuất DOM (`getElementById` cho ID đơn lẻ, `querySelectorAll` cho danh sách phần tử) (10đ).<br>- Thao tác với class thông qua `classList` thay vì nối chuỗi `className` thủ công; hiển thị/ẩn element bằng thuộc tính `hidden` hoặc `classList` hợp lý (10đ). |

---

## Bài tập 6: EdTech (Mức độ 2: Cơ bản - Kiểm thử I/O)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Đặt tên biến rõ nghĩa theo danh từ tiếng Anh (VD: `portType`, `kwhConsumed`, `totalAmount`).<br>- Thụt lề chuẩn 2 hoặc 4 spaces, mã nguồn sạch sẽ.<br>- Có comment giải thích chi tiết logic nghiệp vụ và từng bước thao tác DOM. |
| **Xử lý Logic đúng nghiệp vụ** | **40đ** | - **10đ**: Truy xuất đúng toàn bộ phần tử DOM đầu vào và đầu ra.<br>- **10đ**: Kiểm tra chính xác trạng thái ngắt sạc an toàn (Quá nhiệt > 70°C và Đầy pin >= 100%) và cập nhật đúng class/text.<br>- **10đ**: Tính đúng Tiền điện theo đơn giá `REGULAR` (3.850) và `SUPER` (4.500).<br>- **10đ**: Tính đúng Phí phạt đỗ xe quá 30 phút (1.000 VNĐ/phút vượt quá). |
| **Xử lý Biên & Ngoại lệ** | **20đ** | - Ép kiểu số an toàn, kiểm soát trường hợp `isNaN`, số âm (`< 0`), hoặc loại cổng sạc không hợp lệ.<br>- Hiển thị đúng thông báo lỗi `"DỮ LIỆU KHÔNG HỢP LỆ"` tại thẻ `#total-amount` và gắn class `text-error` khi dữ liệu đầu vào vi phạm quy tắc. |
| **Tối ưu hiệu năng & Thao tác DOM** | **20đ** | - Sử dụng đúng các thuộc tính/phương thức DOM cơ bản (`innerText`/`textContent`, `classList.add`, `classList.remove`).<br>- Không truy xuất trùng lặp cùng 1 DOM element nhiều lần (nên lưu vào biến hằng số `const`).<br>- Tuân thủ tuyệt đối quy định không dùng Event Listener, Fetch, hay LocalStorage. |

---

## Bài tập 7: E-Commerce (Mức độ 3: Nâng cao - Xây dựng tính năng mới)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Đặt tên biến/hàm theo chuẩn `camelCase`, đúng ngữ nghĩa nghiệp vụ HRM.<br>- Code định dạng sạch sẽ, thụt lề chuẩn xác, có comment giải thích các khối xử lý DOM.<br>- Sử dụng ES6 (Template Literals, Arrow Functions, Destructuring). |
| **Xử lý Logic đúng nghiệp vụ** | **40đ** | - Tính chính xác lương giờ cơ bản, tiền phạt đi muộn (chỉ phạt khi `lateMinutes > 15`).<br>- Tính chuẩn hệ số OT 150% và ngày lễ 300%.<br>- Tính đúng tổng lương thực nhận `netSalary` theo từng nhân viên.<br>- Tính chính xác các chỉ số tổng quan: Tổng quỹ lương, Tổng tiền phạt, Nhân viên lương cao nhất. |
| **Thao tác DOM & Dynamic Styling** | **20đ** | - Truy xuất chính xác các phần tử bằng `getElementById`, `querySelector`.<br>- Thay đổi nội dung thẻ bằng `textContent` và `innerHTML` hợp lý.<br>- Dynamic Styling đúng điều kiện: Thêm class `row-warning`, `row-highlight`, thuộc tính `data-salary-level` và render đúng badge trạng thái. |
| **Xử lý Biên & Ràng buộc Kỹ thuật** | **20đ** | - Định dạng tiền tệ chính xác (`x.xxx.xxx VNĐ`).<br>- Kiểm soát trường hợp mảng dữ liệu rỗng (không bị lỗi runtime JS).<br>- Tuân thủ 100% ràng buộc: Không dùng `addEventListener`, `fetch`, `localStorage`, `form submit`. |

---

## Bài tập 8: Logistics (Mức độ 3: Nâng cao - Xây dựng tính năng mới)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Cấu trúc thư mục và đặt tên file chính xác theo quy định.<br>- Mã nguồn rõ ràng, đặt tên biến/hàm theo chuẩn `camelCase`. Có comment giải thích logic thao tác DOM trực quan. |
| **Thao tác DOM & Thay đổi Nội dung/Style** | **20đ** | - Sử dụng đúng các phương thức DOM API: `getElementById`, `querySelector`, `querySelectorAll`, `children`, `appendChild`.<br>- Thay đổi chính xác thuộc tính `textContent`, `innerHTML`, `dataset`, `classList` (add/remove) và inline `style.width` cho thanh progress bar. |
| **Xử lý Logic Nghiệp vụ (Business Rules)** | **40đ** | - Ràng buộc nhiệt độ kho lạnh ($-18^\circ\text{C}$ đến $5^\circ\text{C}$) đạt chuẩn 100%.<br>- Tính toán chính sở tỷ lệ lấp đầy %, chuyển đổi trạng thái CSS class (`status-normal`, `status-warning`, `status-full`) chính xác.<br>- Tính chính xác tổng tải trọng và tổng phí lưu kho toàn hệ thống theo loại kệ (`DRY`: 10.000, `COLD`: 25.000 VNĐ/kg/ngày). |
| **Xử lý Biên, Cảnh báo & Ngoại lệ** | **20đ** | - Chặn chính xác các trường hợp nhập pallet vượt mức $500\text{ kg}$.<br>- Render thông báo lỗi/thành công chuyên nghiệp lên `#alert-box` trên giao diện DOM.<br>- Xử lý an toàn khi truy xuất các thuộc tính dữ liệu `dataset` hoặc parse dữ liệu kiểu số từ DOM text. |

---

## Bài tập 9: FinTech (Mức độ 3: Nâng cao - Xây dựng tính năng mới)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết đánh giá |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Đặt tên biến/hàm theo chuẩn `camelCase`, thể hiện rõ ngữ cảnh domain HRM/FinTech (`baseSalary`, `latePenalty`, `netSalary`).<br>- Thụt lề chuẩn 2 hoặc 4 spaces, có comment giải thích rõ ràng từng đoạn logic xử lý DOM API.<br>- Tổ chức code sạch đẹp, tách hàm xử lý hợp lý (Ví dụ: `calculateHourlyRate()`, `formatCurrency()`, `renderPayroll()`). |
| **Xử lý Logic đúng nghiệp vụ** | **40đ** | - **Trích xuất dataset chính xác (10đ)**: Đọc đúng toàn bộ `data-*` từ profile và danh sách hàng `.shift-row`.<br>- **Tính toán chuẩn nghiệp vụ (20đ)**:<br>  + Tính đúng phạt đi muộn (chỉ phạt khi $>15$ phút, đúng 50.000 VNĐ/lần).<br>  + Tính đúng hệ số OT (ngày thường 1.5x, ngày lễ 3.0x).<br>  + Tính đúng 10.5% BHXH.<br>  + Tính đúng công thức Net Salary.<br>- **Render danh sách hàng (10đ)**: Điền đúng dữ liệu vào từng ô `<td>` trong bảng nhật ký ca làm việc bằng DOM manipulation. |
| **Xử lý Biên & Ngoại lệ (Edge Cases)** | **20đ** | - **Kiểm soát NaN/Null (10đ)**: Ép kiểu dữ liệu an toàn (`parseInt`/`parseFloat`), xử lý trường hợp `data-` bị thiếu, rỗng hoặc chứa chuỗi không hợp lệ.<br>- **Lương âm / Đi muộn 0 phút (10đ)**: Xử lý đúng khi nhân viên không đi muộn ca nào, hoặc khi tổng khấu trừ lớn hơn tổng lương khiến Net Salary $<0$. |
| **Tối ưu hiệu năng & DOM Manipulation** | **20đ** | - **Tối ưu truy xuất DOM (10đ)**: Không lặp lại các câu lệnh `document.querySelector` trùng lặp trong vòng lặp. Lưu truy xuất vào biến cached DOM.<br>- **Định dạng & Dynamic Styling (10đ)**: Định dạng chuẩn tiền tệ `Intl.NumberFormat('vi-VN')`, cập nhật class CSS (`classList.add/remove`) và dynamic inline style mượt mà. |

---

## Bài tập 10: Healthcare (Mức độ 4: Phân tích & Tối ưu - Tái cấu trúc)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Mã nguồn được tổ chức sạch sẽ, đặt tên biến/hàm theo chuẩn `camelCase`.<br>- Có comment giải thích chi tiết các điểm đã được tối ưu so với đoạn code legacy cũ.<br>- Cấu trúc HTML/CSS phân tách rõ ràng, không dùng inline style. |
| **Phân tích & Tối ưu DOM (Bloom Level 4)** | **20đ** | - Loại bỏ hoàn toàn việc lạm dụng `innerHTML +=` trong vòng lặp.<br>- Sử dụng thành thạo `DocumentFragment` để gom nhóm các thao tác chèn node.<br>- Cache các truy vấn selector ra ngoài vòng lặp.<br>- Sử dụng `textContent` thay cho `innerHTML` đối với dữ liệu văn bản tĩnh/động. |
| **Xử lý Logic đúng Nghiệp vụ** | **40đ** | - **Hạn ngạch vé (10đ):** Phát hiện chính xác đơn hàng `ticketQuantity > 4`, gán CSS `.order-error` và không tính cộng dồn vào `soldSeats`.<br>- **Chính sách Early Bird (10đ):** Tính chính xác mức giảm 15% cho các đơn hàng mở bán sớm.<br>- **Trạng thái Zone (10đ):** Phân loại đúng 3 cấp độ (`sold-out`, `warning`, `available`) dựa trên sức chứa còn lại.<br>- **Trạng thái QR (10đ):** Đánh dấu đúng trạng thái `qr-disabled` hoặc `qr-active`. |
| **Xử lý Biên & Chuẩn hóa Dữ liệu** | **20đ** | - Kiểm tra null/undefined cho dữ liệu đầu vào trước khi render.<br>- Định dạng tiền tệ hiển thị rõ ràng (VD: `1,700,000 VNĐ` hoặc sử dụng `toLocaleString('vi-VN')`).<br>- Giao diện tự động dọn dẹp nội dung cũ (`innerHTML = ''`) trước khi nạp dữ liệu mới. |

---

## Bài tập 11: CRM (Mức độ 4: Phân tích & Tối ưu - Tái cấu trúc)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Phân tích & Tái cấu trúc (Clean Code)** | **20đ** | - Tách biệt rõ ràng hàm `calculateTripFare`, `formatCurrencyVND` và `renderTripTable`.<br>- Đặt tên biến/hàm theo chuẩn CamelCase, có comment giải thích rõ ràng các bước xử lý. |
| **Xử lý Logic Nghiệp vụ Cước phí** | **40đ** | - Tính đúng giá $2\text{ km}$ đầu ($12.000\text{ VNĐ}$) và các km tiếp theo ($4.500\text{ VNĐ/km}$).<br>- Nhân đúng hệ số $1.2x$ khi `isSurge === true` và làm tròn số (`Math.round`).<br>- Định dạng chuẩn tiền tệ VNĐ (ví dụ `30.600 VNĐ`). |
| **Xử lý Biên & Dữ liệu Ngoại lệ** | **20đ** | - Bắt lỗi `distanceKm <= 0` hoặc không phải số: Không sập chương trình, hiển thị cước `$0\text{ VNĐ}$` và cảnh báo giao diện.<br>- Xử lý tên hành khách rỗng/null thành `"Khách ẩn danh"`. |
| **Tối ưu Hiệu năng DOM API** | **20đ** | - Tuyệt đối **không** dùng `innerHTML` trong vòng lặp.<br>- Sử dụng `DocumentFragment` để gom thao tác DOM và chỉ append vào tbody 1 lần duy nhất.<br>- Dùng `createElement`, `textContent`, và `classList.add` đúng tiêu chuẩn bảo mật & hiệu năng. |

---

## Bài tập 12: EdTech (Mức độ 4: Phân tích & Tối ưu - Tái cấu trúc)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **1. Phân tích điểm yếu (Code Review & Analysis)** | **20đ** | - Phát hiện và giải thích chính xác 4 điểm yếu về hiệu năng DOM Reflow/Repaint, lặp Query DOM, inline style và spaghetti code.<br>- Nêu rõ lý do tại sao mã cũ gây chậm hệ thống. |
| **2. Tối ưu hóa hiệu năng DOM (DOM Optimization)** | **25đ** | - Sử dụng `DocumentFragment` để thực hiện thao tác batch update DOM 1 lần duy nhất.<br>- Triển khai hàm `cacheDOMElements()` truy xuất DOM tối ưu, không gọi `querySelector` trong vòng lặp.<br>- Sử dụng `createElement` và `textContent` thay cho `innerHTML`. |
| **3. Xử lý Logic Nghiệp vụ (Business Rules)** | **25đ** | - Tính toán chính xác định mức miễn phí và phí phạt cước 50.000 VNĐ/kg cho cả 3 hạng vé (Eco, Deluxe, Business).<br>- Phân loại đúng CSS class và Badge nhãn theo từng hạng vé.<br>- Thống kê chính xác: Tổng số khách, Tổng doanh thu cước, Số khách Business. |
| **4. Xử lý Biên & Dữ liệu Ngoại lệ (Edge Cases)** | **15đ** | - Xử lý đúng khi danh sách mảng rỗng (`[]` hoặc `null`): Hiển thị Empty State trên DOM.<br>- Kiểm tra PNR đúng 6 ký tự alphanumeric, gắn class `.card-invalid` cho PNR lỗi.<br>- Chuẩn hóa khối lượng hành lý âm (`< 0`) hoặc không phải số về `0`. |
| **5. Cấu trúc mã nguồn & Phong cách (Code Style)** | **15đ** | - Tách biệt rõ ràng Pure Functions (tính toán) và DOM Manipulation Functions.<br>- Không vi phạm danh mục Forbidden Scope (Không dùng Event listeners, Form submit, Fetch, LocalStorage).<br>- Code có comment giải thích rõ ràng bằng Tiếng Việt có dấu, đặt tên hàm/biến chuẩn `camelCase`. |

---

## Bài tập 13: E-Commerce (Mức độ 5: Sáng tạo - Thiết kế Mini Module)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc Module & DOM Selection** | **20đ** | - Sử dụng đúng các phương thức DOM API (`getElementById`, `querySelector`, `querySelectorAll`).<br>- Tổ chức mã nguồn thành Module/Object rõ ràng (`SaaSSubscriptionManager`).<br>- Không vi phạm phạm vi cấm (Không dùng Event Listener, Fetch, LocalStorage). |
| **Logic Nghiệp vụ SaaS & Định giá** | **40đ** | - Tính toán chính xác giá chu kỳ Năm (giảm 20% trên 12 tháng) và render thẻ `<del>`, `.discount-tag` đúng DOM.<br>- Xử lý đúng quy tắc hạ cấp về gói `FREE` khi `paymentStatus === 'FAILED_OVER_3_DAYS'`.<br>- Render đúng số lượng tối đa 5 sub-profiles cho gói `FAMILY` và ẩn phần này khi ở gói `INDIVIDUAL`/`FREE`. |
| **Feature Gate & Biến đổi Giao diện** | **20đ** | - Duyệt qua tất cả `.feature-item` bằng `querySelectorAll`.<br>- Thêm/xóa class `.feature-active` / `.feature-disabled` chính xác theo `allowedFeatures`.<br>- Cập nhật nội dung text và icon (`✔️` / `❌`) khớp với từng quyền. |
| **Xử lý Biên & Phòng vệ Mã nguồn** | **20đ** | - Kiểm tra null/undefined trước khi thao tác với DOM element.<br>- Sử dụng `textContent` thay cho `innerHTML` đối với dữ liệu từ người dùng (tránh lỗi bảo mật XSS).<br>- Cắt mảng sub-profiles an toàn khi dữ liệu lớn hơn 5 và ghi log cảnh báo (`console.warn`). |

---

## Bài tập 14: FinTech (Mức độ 5: Sáng tạo - Thiết kế Mini Module)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **1. Cấu trúc Architecture & Phong cách Code** | **20 điểm** | - Đóng gói đúng mô hình Mini-Module/Class sạch sẽ.<br>- Đặt tên biến, hàm theo chuẩn `camelCase`, hằng số `UPPER_SNAKE_CASE`.<br>- Comment mã nguồn rõ ràng, cấu trúc HTML/CSS mạch lạc. |
| **2. Xử lý Logic Nghiệp vụ FinTech** | **40 điểm** | - Tính chính xác đơn giá sạc theo loại `STANDARD` (3.850đ) và `SUPER_FAST` (4.500đ).<br>- Tính chính xác phí phạt đỗ xe (Miễn phí 30 phút đầu, từ phút 31 tính 1.000đ/phút).<br>- Kiểm soát chính xác logic ngắt sạc khi `Pin = 100%` hoặc `Nhiệt độ > 70°C`.<br>- Format đúng định dạng tiền tệ Việt Nam (`VNĐ`). |
| **3. Thao tác DOM API (Phạm vi Session 17)** | **20 điểm** | - Truy xuất phần tử DOM chính xác bằng `querySelector`/`getElementById`.<br>- Sử dụng thành thạo `createElement`, `appendChild`, `textContent`, `classList`.<br>- Tuân thủ quy định: Không dùng Event Listener, Form submit, Fetch API hay LocalStorage. |
| **4. Xử lý Biên & Ngoại lệ DOM** | **20 điểm** | - Kiểm tra và xử lý khi `portId` không tồn tại trên DOM.<br>- Tránh nhân bản (duplicate) phần tử Hóa đơn nếu hóa đơn đó đã tồn tại.<br>- Xử lý an toàn dữ liệu đầu vào bị thiếu hoặc bị sai kiểu dữ liệu (vd: `temperature` bị âm, `currentKwh` không phải là số). |

---

## Bài tập 15: EdTech (Mức độ 5: Sáng tạo - Thiết kế Mini Module)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Mã nguồn được tổ chức sạch sẽ theo dạng Module Object (`POSReceiptEngine`).<br>- Đặt tên biến, hàm theo chuẩn CamelCase (rõ nghĩa, đúng tiếng Anh chuyên ngành).<br>- Có comment giải thích logic rõ ràng cho từng phương thức DOM. |
| **Xử lý Logic đúng nghiệp vụ** | **40đ** | - Tính đúng phụ thu Size món: M (+6.000đ), L (+10.000đ), S (+0đ).<br>- Tính đúng phụ thu Topping (8.000đ / phần).<br>- Tính đúng 10% giảm giá cho Gold Member.<br>- Định dạng chuẩn tiền tệ VNĐ (có phân cách hàng nghìn). |
| **Thao tác DOM API & Rendering** | **20đ** | - Truy xuất chính xác các phần tử bằng `getElementById` hoặc `querySelector`.<br>- Sử dụng linh hoạt `textContent`, `innerHTML` để chèn nội dung.<br>- Thao tác class thành thạo với `classList.add()` / `classList.remove()`.<br>- Cập nhật thuộc tính thành công qua `setAttribute()`. |
| **Xử lý Biên & Tối ưu hiệu năng** | **20đ** | - Kiểm soát trường hợp mảng `drinks` hoặc `toppings` rỗng (hiển thị thông báo phù hợp thay vì để trắng hoặc lỗi JS).<br>- Kiểm tra sự tồn tại của phần tử DOM trước khi thao tác để tránh lỗi Null Reference.<br>- Thuật toán duyệt mảng và tạo chuỗi DOM tối ưu, không gọi DOM API lặp đi lặp lại trong vòng lặp lớn. |

---

