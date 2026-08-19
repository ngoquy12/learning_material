# BẢNG TIÊU CHÍ ĐÁNH GIÁ TỔNG HỢP (100đ) - Tương tác DOM API (Document Object Model)- Truy xuất và Thay đổi Nội dung

## Bài tập 1: E-Commerce (Cơ bản 1 - Debug lỗi)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Phân tích & Phát hiện Lỗi (Debug Report)** | **20đ** | - Phát hiện đầy đủ và chính xác ít nhất 5 lỗi trong file `script.js`.<br>- Giải thích rõ ràng bản chất kỹ thuật của lỗi (VD: `getElementById` truyền dư `#`, `getElementsByClassName` trả về `HTMLCollection` chứ không phải 1 element, thẻ `span`/`strong` không có thuộc tính `.value`...). |
| **Xử lý Logic đúng Nghiệp vụ GrabRide** | **40đ** | - Tính chuẩn cước phí gốc cho 2km đầu ($12.000$ VNĐ) và các km tiếp theo ($4.500$ VNĐ/km).<br>- Áp dụng đúng công thức nhân hệ số $1.2$ khi `isSurge = true`.<br>- Kết quả tính toán chính xác tuyệt đối với các bộ test cases (ví dụ 1.5km, 5.5km, 10km). |
| **Thao tác DOM API & Chuẩn hóa UI** | **20đ** | - Truy xuất đúng DOM element mà không gây lỗi `null` hoặc `undefined`.<br>- Sử dụng đúng `innerText`/`textContent` để cập nhật văn bản.<br>- Đặt thuộc tính `src` cho ảnh thành công.<br>- Thay đổi style/class hiển thị đúng bằng `classList.add()` mà không làm phá vỡ CSS nền. |
| **Cấu trúc Mã nguồn & Quy chuẩn Nộp bài** | **20đ** | - Mã nguồn viết sạch sẻ, có comment giải thích rõ ràng.<br>- Đặt tên biến/hàm theo chuẩn camelCase (`calculateTripFare`, `totalFareEl`).<br>- Tuân thủ đúng cấu trúc thư mục nộp bài và các ràng buộc phạm vi kỹ thuật (không dùng event/fetch). |

---

## Bài tập 2: Logistics (Cơ bản 2 - Kiểm thử I/O)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Đặt tên biến/hàm theo chuẩn `camelCase`, rõ nghĩa.<br>- Thụt lề đồng nhất (2 hoặc 4 spaces).<br>- Có comment giải thích các đoạn xử lý DOM quan trọng. |
| **Xử lý Logic đúng nghiệp vụ** | **40đ** | - Xử lý hạ cấp gói cước chính xác khi `paymentOverdueDays > 3` (15đ).<br>- Cập nhật đúng thông tin gói cước, số thiết bị & danh sách tính năng tương ứng với `PERSONAL`, `FAMILY`, `FREE` (15đ).<br>- Hiển thị/Ẩn cảnh báo tài khoản con (`#warning-badge`) chính xác theo điều kiện số lượng (10đ). |
| **Thao tác DOM API & Chuẩn I/O** | **20đ** | - Sử dụng đúng `document.getElementById` hoặc `document.querySelector` (5đ).<br>- Cập nhật nội dung bằng `textContent` và danh sách bằng `innerHTML` hợp lý (10đ).<br>- Thao tác class (`classList.add`, `classList.remove`) và ẩn/hiện element (`style.display`) đúng quy định (5đ). |
| **Kiểm thử Biên & Ngoại lệ** | **20đ** | - Xử lý đúng khi `activeSubAccounts` chạm mốc biên (= 5 thì ẩn warning, > 5 mới hiện).<br>- Xử lý đúng khi `paymentOverdueDays` chạm mốc 3 (chưa phạt) và 4 (bắt đầu phạt hạ cấp).<br>- Không để phát sinh lỗi JavaScript Runtime khi gọi hàm với dữ liệu hợp lệ. |

---

## Bài tập 3: FinTech (Nâng cao 1 - Tính năng mới)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết đánh giá |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Cấu trúc thư mục và đặt tên file chuẩn quy định (5đ).<br>- Đặt tên biến/hàm ngữ nghĩa (`camelCase`), chuẩn sạch đẹp (5đ).<br>- Thụt lề chuẩn, định dạng code nhất quán (5đ).<br>- Viết comment giải thích logic thao tác DOM rõ ràng (5đ). |
| **Xử lý Logic đúng nghiệp vụ** | **40đ** | - Tính toán chính xác chiết khấu 15% cho Early Bird và định dạng tiền tệ `VND` (10đ).<br>- Kiểm soát chính xác hạn ngạch tối đa 4 vé/tài khoản (10đ).<br>- Render chính xác danh sách vé động từ dữ liệu mảng vào DOM tree (10đ).<br>- Cập nhật chuẩn xác 100% các trạng thái QR check-in (Valid vs Expired) (10đ). |
| **Thao tác DOM API & Xử lý Biên** | **20đ** | - Sử dụng đúng các phương thức `getElementById`, `querySelector`, `classList`, `dataset`, `setAttribute` (10đ).<br>- Xóa sạch nội dung cũ (`innerHTML = ''`) trước khi render lại danh sách tránh nhân bản phần tử (5đ).<br>- Kiểm soát biên lỗi: Mảng vé rỗng, vé bằng 0, dữ liệu null/undefined (5đ). |
| **Tối ưu hiệu năng & Cấu trúc DOM** | **20đ** | - Không lặp lại việc query DOM cùng 1 element nhiều lần (lưu node vào biến) (10đ).<br>- Tạo DOM Node tối ưu, không thừa các thẻ HTML trung gian (5đ).<br>- Tuân thủ nghiêm ngặt ràng buộc: Không sử dụng Event Listeners, Fetch API hay LocalStorage (5đ). |

---

## Bài tập 4: Healthcare (Nâng cao 2 - Nghiệp vụ phức tạp)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Cấu trúc HTML/CSS sạch sẽ, đúng semantic.<br>- Mã nguồn JS tuân thủ quy tắc đặt tên `camelCase`, comment giải thích logic nghiệp vụ rõ ràng.<br>- Sử dụng chính xác APIs của Session 17 (`querySelector`, `getElementById`, `innerHTML`, `textContent`, `classList`). |
| **Xử lý Logic đúng Nghiệp vụ Fitness** | **40đ** | - Tính đúng logic tặng 2 tháng cho gói 12 tháng (tổng 14 tháng) (10đ).<br>- So sánh ngày hiện tại với ngày hết hạn chính xác để gắn nhãn `HẾT HẠN` / `HỢP LỆ` (10đ).<br>- Cảnh báo đúng trường hợp vượt quá lượt check-in trong ngày (10đ).<br>- Render đúng đặc quyền VIP (Tủ đồ & Khăn tắm) cho gói VIP (10đ). |
| **Xử lý Biên & Ngoại lệ (Edge Cases)** | **20đ** | - Xử lý an toàn dữ liệu `trainerAssigned` bị `null`/`undefined` (5đ).<br>- Kiểm soát dữ liệu số tháng tập không hợp lệ (5đ).<br>- Xử lý trường hợp mảng hội viên rỗng, hiển thị UI thay thế phù hợp (10đ). |
| **Tối ưu Hiệu năng & Cập nhật Summary DOM** | **20đ** | - Tính toán và cập nhật chính xác các chỉ số thống kê trên Summary Bar (`#total-checkins`, `#total-warnings`, `#total-vip`) (10đ).<br>- Tối ưu hóa các thao tác DOM, tránh việc truy xuất DOM lặp đi lặp lại không cần thiết trong vòng lặp (10đ). |

---

## Bài tập 5: CRM (Tối ưu hóa - Tái cấu trúc)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Tối ưu hóa DOM (DOM Refactoring)** | **20đ** | - Áp dụng thành công caching cho các phần tử DOM, không để lặp lại việc truy xuất phần tử DOM.<br>- Sử dụng `DocumentFragment` hoặc gom chuỗi HTML để thao tác `innerHTML` đúng 1 lần.<br>- Sử dụng `textContent` hợp lý thay cho `innerHTML` cho các đoạn text tĩnh/tiền tệ. |
| **Xử lý Logic đúng Nghiệp vụ ShopeeFood** | **40đ** | - Tính đúng Subtotal (bỏ qua sản phẩm `stock === 0`).<br>- Áp dụng đúng quy tắc giảm 15k phí ship cho đơn $\ge 100\text{k}$ (phí ship không âm).<br>- Tính chuẩn phụ phí giờ cao điểm $10\text{k}$ (11h-13h, 18h-20h).<br>- Tính chính xác tổng thanh toán cuối cùng. |
| **Xử lý Trạng thái & Trường hợp Biên** | **20đ** | - Xử lý chuẩn xác khi quán đóng cửa (`isStoreOpen = false`): Hiển thị banner lỗi, ẩn khu vực checkout.<br>- Phân biệt rõ món còn hàng/hết hàng trên giao diện bằng class CSS và nhãn tương ứng.<br>- Xử lý an toàn trường hợp giỏ hàng rỗng (`cartItems = []`). |
| **Tái cấu trúc Mã nguồn & Clean Code** | **20đ** | - Tách biệt logic nghiệp vụ tính toán (Pure Functions) và logic thao tác DOM (Impure Functions).<br>- Đặt tên hàm, biến chuẩn CamelCase, tự giải thích (self-documenting).<br>- Định dạng tiền tệ chính xác (`xxx.xxxđ`). Mã nguồn không chứa Event Listeners hay API cấm. |

---

## Bài tập 6: EdTech (Sáng tạo - Thiết kế Mini Module)

### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Mô đun hóa Mã nguồn** | **20đ** | - Mã nguồn JS được thiết kế dạng Module/Class sạch sẻ, phân tách rõ ràng trách nhiệm từng hàm (`renderUserProfile`, `renderBilling`,...<br>- Đặt tên biến, hàm theo chuẩn Camel-case, comment giải thích logic nghiệp vụ đầy đủ.<br>- Khung HTML ngữ nghĩa, CSS định hình giao diện rõ ràng. |
| **Thao tác DOM API & Rendering** | **20đ** | - Sử dụng đúng và tối ưu các truy xuất DOM (`getElementById`, `querySelector`, `querySelectorAll`).<br>- Cập nhật chính xác `textContent`, `innerHTML`, `classList` và thuộc tính DOM theo trạng thái dữ liệu.<br>- Không để lọt các lỗi đè dữ liệu hoặc render sót node. |
| **Xử lý Logic Nghiệp vụ & Grace Period** | **30đ** | - Tính toán chính xác giá tiền gói năm (chiết khấu 20%) và định dạng tiền tệ `VNĐ`.<br>- Thực hiện chuẩn xác logic Grace Period: `daysOverdue > 3` phải ép downgrade giao diện về `FREE` và đổi trạng thái Alert sang màu đỏ.<br>- Nếu `daysOverdue <= 3` hiển thị thông báo màu vàng cảnh báo số ngày còn lại. |
| **Quản lý Hạn ngạch & Feature Matrix** | **20đ** | - Render chính xác ma trận đặc quyền (locked/unlocked) cho cả 4 hạng gói.<br>- Xử lý đúng hạn ngạch tài khoản con: Ẩn/Vô hiệu hóa với gói Free/Individual; Đánh dấu nhãn vượt hạn ngạch (`.exceeded-limit`) từ tài khoản thứ 6 trở đi với gói Family. |
| **Kiểm soát Ngoại lệ & Dữ liệu Biên** | **10đ** | - Xử lý an toàn khi mảng tài khoản con bị rỗng (`[]` hoặc `null`).<br>- Xử lý khi dữ liệu gói nhập vào không hợp lệ (mặc định trả về gói `FREE`).<br>- Không vi phạm danh mục cấm (Không dùng Event Listener, Fetch, LocalStorage). |

---

