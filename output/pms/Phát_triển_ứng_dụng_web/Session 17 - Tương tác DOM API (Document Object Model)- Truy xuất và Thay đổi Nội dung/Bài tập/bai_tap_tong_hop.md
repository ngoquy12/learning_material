# Bài tập tổng hợp trên lớp: Cập nhật Trạng thái và Thẻ Thông tin Chuyến xe GrabRide


## 1. Mục tiêu bài tập
- **Truy xuất phần tử DOM Tree**: Sử dụng thành thạo các phương thức tìm kiếm phần tử HTML (`getElementById`, `querySelector`, `querySelectorAll`) để định vị các thành phần hiển thị trên giao diện chuyến xe.
- **Thao tác nội dung và thuộc tính DOM**: Thực hành thay đổi nội dung văn bản (`innerText`, `textContent`), cấu trúc HTML nội hàm (`innerHTML`), và các thuộc tính phần tử (`setAttribute`, `src`, `alt`, `classList`) một cách linh hoạt.
- **Xử lý logic nghiệp vụ Front-end**: Tính toán giá tiền chuyến xe dựa trên phụ phí giờ cao điểm, định dạng tiền tệ và cập nhật giao diện trực quan theo trạng thái thực tế mà không cần dùng sự kiện (Event Listeners).


## 2. Mô tả bối cảnh & Yêu cầu bài toán (Input / Output)
- **Bối cảnh doanh nghiệp**: Trong ứng dụng gọi xe Grab, sau khi hệ thống tìm được tài xế phù hợp cho hành khách, màn hình sẽ chuyển sang trạng thái "Đang di chuyển" hoặc "Đã điều phối". Bạn cần viết đoạn mã JavaScript để nhận dữ liệu thông tin chuyến đi và tiến hành cập nhật trực tiếp lên các thẻ HTML đã dựng sẵn (Avatar tài xế, Tên tài xế, Cước phí đã tính phụ phí giờ cao điểm, Trạng thái chuyến đi và Thẻ ưu đãi đi kèm).
- **Dữ liệu đầu vào (Input)**:
  - Khung giao diện HTML cố định chứa các phần tử có ID: `#driver-name`, `#driver-avatar`, `#ride-distance`, `#ride-fare`, `#ride-status`, `#promo-badge`.
  - Một đối tượng dữ liệu thông tin chuyến xe (`rideData`) gồm các thuộc tính:
    - `driverName` (string): Tên tài xế.
    - `avatarUrl` (string): Đường dẫn ảnh chân dung tài xế.
    - `distanceKm` (number): Quãng đường di chuyển (tính theo km).
    - `isPeakHour` (boolean): Trạng thái giờ cao điểm (`true` nếu rơi vào giờ cao điểm, `false` nếu giờ bình thường).
    - `status` (string): Trạng thái chuyến xe nhận các giá trị: `"ARRIVING"`, `"COMPLETED"`, `"CANCELLED"`.

- **Kết quả đầu ra (Output)**:
  - Cập nhật tên tài xế vào phần tử `#driver-name`.
  - Đổi thuộc tính `src` và `alt` của phần tử ảnh `#driver-avatar` tương ứng với `avatarUrl` và `driverName`.
  - Tính toán tổng cước phí và cập nhật vào `#ride-fare`:
    - Đơn giá cố định: 10.000 VNĐ/km.
    - Nếu `isPeakHour = true`: Tổng tiền = Quãng đường x Đơn giá x 1.2 (phụ thu 20%).
    - Nếu `isPeakHour = false`: Tổng tiền = Quãng đường x Đơn giá.
    - Định dạng hiển thị chuỗi tiền tệ (Ví dụ: `120.000 VNĐ`).
  - Cập nhật trạng thái chuyến xe vào phần tử `#ride-status`:
    - Giá trị `"ARRIVING"`: Hiển thị chữ "Tài xế đang đến", gắn class CSS `status-arriving`.
    - Giá trị `"COMPLETED"`: Hiển thị chữ "Chuyến đi hoàn thành", gắn class CSS `status-completed`.
    - Giá trị `"CANCELLED"`: Hiển thị chữ "Chuyến đi đã hủy", gắn class CSS `status-cancelled`.
  - Cập nhật nhãn ưu đãi vào phần tử `#promo-badge`:
    - Nếu Tổng cước phí ≥ 100.000 VNĐ: Thêm cấu trúc HTML `<span class="badge-discount">Tặng Voucher 10% chuyến sau</span>`.
    - Ngược lại: Xóa rỗng nội dung bên trong `#promo-badge`.


### Bảng ví dụ minh họa Input/Output:

| Trường hợp (Case) | Dữ liệu đầu vào (Input) | Kết quả kỳ vọng (Expected Output) | Ghi chú nghiệp vụ |
| :--- | :--- | :--- | :--- |
| **Trường hợp 1 (Chuẩn)** | `rideData = {`<br>`  driverName: "Nguyễn Văn An",`<br>`  avatarUrl: "https://example.com/avatar1.jpg",`<br>`  distanceKm: 10,`<br>`  isPeakHour: true,`<br>`  status: "ARRIVING"`<br>`}` | - `#driver-name`: "Nguyễn Văn An"<br>- `#driver-avatar`: `src="https://example.com/avatar1.jpg"`, `alt="Nguyễn Văn An"`<br>- `#ride-fare`: "120.000 VNĐ"<br>- `#ride-status`: "Tài xế đang đến" (Class: `status-arriving`)<br>- `#promo-badge`: `<span class="badge-discount">Tặng Voucher 10% chuyến sau</span>` | Tính phụ phí 20% giờ cao điểm: 10 * 10.000 * 1.2 = 120.000 VNĐ. Giá trị ≥ 100.000 VNĐ nên hiện badge. |
| **Trường hợp 2 (Ngoại lệ)** | `rideData = {`<br>`  driverName: "",`<br>`  avatarUrl: "",`<br>`  distanceKm: -5,`<br>`  isPeakHour: false,`<br>`  status: "UNKNOWN"`<br>`}` | - `#driver-name`: "Chưa xác định"<br>- `#driver-avatar`: `src="default-avatar.png"`, `alt="Chưa xác định"`<br>- `#ride-fare`: "Khoảng cách không hợp lệ"<br>- `#ride-status`: "Trạng thái không xác định" (Class: `status-default`)<br>- `#promo-badge`: "" (Rỗng) | Bắt lỗi dữ liệu biên: Khoảng cách âm, tên rỗng, trạng thái không hợp lệ. |


## 3. Các bước thực hiện & Quy định kỹ thuật
- **Tài nguyên & Môi trường**: 
  - Thực thi trên môi trường trình duyệt Web (HTML5, ES6 JavaScript).
  - Làm việc trên file HTML tĩnh chứa sẵn cấu trúc giao diện thẻ GrabRide và file JavaScript kết nối.
- **Yêu cầu kỹ thuật**:
  - Học viên tự chủ động thiết kế thuật toán xử lý dữ liệu và cấu trúc các câu lệnh DOM API phù hợp (Closed How).
  - **Phạm vi nghiêm cấm**: Không sử dụng Lắng nghe sự kiện (Event Listeners / `addEventListener`), không sử dụng các sự kiện inline (`onclick`, `onchange`), không dùng `fetch`/`axios`, không dùng `localStorage`.
  - Truy xuất chính xác các phần tử DOM qua ID hoặc Class selector.
  - Xử lý thay đổi nội dung linh hoạt giữa `innerText`/`textContent` (cho văn bản thuần) và `innerHTML` (cho đoạn thẻ HTML badge).
  - Xử lý thuộc tính thẻ `<img>` thông qua thuộc tính trực tiếp hoặc phương thức `setAttribute()`.
  - Cập nhật CSS Class động cho trạng thái thông qua `classList.add()`, `classList.remove()` hoặc `className`.
  - Bắt lỗi dữ liệu đầu vào: Trường hợp khoảng cách ≤ 0, chuỗi tên rỗng, hoặc giá trị trạng thái không nằm trong danh sách nghiệp vụ.


## 4. Checklist đánh giá kết quả (Nghiệm thu)
- [ ] Xây dựng hoàn chỉnh chương trình đáp ứng đúng bối cảnh nghiệp vụ doanh nghiệp.
- [ ] Trả về kết quả Output chính xác theo đúng bảng ví dụ minh họa.
- [ ] Bắt lỗi ngoại lệ và xử lý dữ liệu biên an toàn không gây crash chương trình.
- [ ] Mã nguồn đạt chuẩn Clean Code, đặt tên biến/hàm đúng quy chuẩn và có chú thích rõ ràng.