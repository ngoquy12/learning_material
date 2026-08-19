# Bài tập tổng hợp trên lớp: Cập nhật Trạng thái và Hiển thị Thẻ Sản phẩm Flash Sale (E-Commerce)


## 1. Mục tiêu bài tập
- Thành thạo kỹ năng truy xuất các phần tử trên cây DOM (DOM Tree) bằng các phương thức chuẩn như `getElementById`, `querySelector`, `querySelectorAll`.
- Thực hành thay đổi linh hoạt nội dung văn bản (`textContent`) và cấu trúc HTML nội bộ (`innerHTML`) của các phần tử DOM để hiển thị dữ liệu sản phẩm động.
- Vận dụng kỹ thuật thao tác với thuộc tính phần tử (`src`, `alt`, `classList`, `style`) để thay đổi trạng thái giao diện sản phẩm (còn hàng/hết hàng, ẩn/hiện mức giảm giá, áp dụng khung nhãn khuyến mãi) theo đúng quy tắc nghiệp vụ.


## 2. Mô tả bối cảnh & Yêu cầu bài toán (Input / Output)
- **Bối cảnh doanh nghiệp**: Trang thương mại điện tử RikkeiShop đang chuẩn bị cho sự kiện Flash Sale. Hệ thống giao diện cần hiển thị thẻ thông tin chi tiết của sản phẩm dựa trên dữ liệu đối tượng nhận được từ hệ thống backend. Nhiệm vụ của lập trình viên là viết đoạn mã thao tác DOM API để render (hiển thị) chính xác các thông tin: tên sản phẩm, hình ảnh, giá gốc, giá khuyến mãi, trạng thái tồn kho và các nhãn đánh dấu (badges/tags) lên khung HTML có sẵn mà không làm phá vỡ bố cục giao diện.
- **Dữ liệu đầu vào (Input)**: Một đối tượng JavaScript `product` chứa thông tin chi tiết sản phẩm với cấu trúc:
  - `id` (chuỗi): Mã sản phẩm.
  - `name` (chuỗi): Tên sản phẩm.
  - `price` (số): Giá niêm yết gốc (đơn vị: VNĐ).
  - `discountPercent` (số): Phần trăm giảm giá (giá trị từ `0` đến `100`).
  - `inStock` (boolean): Trạng thái còn hàng (`true`: còn hàng, `false`: hết hàng).
  - `imageUrl` (chuỗi): Đường dẫn liên kết ảnh sản phẩm.
  - `tags` (mảng chuỗi): Danh sách các nhãn phân loại sản phẩm (ví dụ: `["Flash Sale", "Free Ship"]`).
- **Kết quả đầu ra (Output)**: Cây DOM HTML trên trang web được cập nhật hiển thị đồng bộ với dữ liệu `product`:
  - Thẻ ảnh (`<img>`): Thao tác gán thuộc tính `src` bằng `imageUrl` và `alt` bằng `name`. Nếu `imageUrl` rỗng, gán đường dẫn ảnh mặc định.
  - Thẻ tiêu đề: Thay đổi nội dung chữ thành `name`.
  - Khung hiển thị giá: 
    - Nếu `discountPercent > 0`: Hiển thị giá gốc bị gạch ngang và tính toán giá thực tế sau giảm = `price * (1 - discountPercent / 100)` để hiển thị màu nổi bật.
    - Nếu `discountPercent === 0`: Chỉ hiển thị giá gốc, ẩn phần thông tin giảm giá.
  - Khung trạng thái kho hàng:
    - Nếu `inStock === true`: Cập nhật chữ "Còn hàng", thêm class hiển thị màu xanh.
    - Nếu `inStock === false`: Cập nhật chữ "Hết hàng", thêm class hiển thị màu đỏ và áp dụng mờ thẻ sản phẩm (giảm opacity hoặc thêm class disabled).
  - Khung danh sách nhãn (`tags`): Cập nhật `innerHTML` chứa danh sách các phần tử HTML nhãn tương ứng.


### Bảng ví dụ minh họa Input/Output:

| Trường hợp (Case) | Dữ liệu đầu vào (Input) | Kết quả kỳ vọng (Expected Output) | Ghi chú nghiệp vụ |
| :--- | :--- | :--- | :--- |
| **Trường hợp 1 (Chuẩn)** | `product = {`<br>`  id: "SP01",`<br>`  name: "Tai nghe Bluetooth",`<br>`  price: 1000000,`<br>`  discountPercent: 20,`<br>`  inStock: true,`<br>`  imageUrl: "https://picsum.photos/200",`<br>`  tags: ["Flash Sale", "Free Ship"]`<br>`}` | - `img.src` = `"https://picsum.photos/200"`, `img.alt` = `"Tai nghe Bluetooth"`<br>- Tiêu đề = `"Tai nghe Bluetooth"`<br>- Giá gốc = `"1.000.000 đ"` (gạch ngang), Giá KM = `"800.000 đ"`<br>- Trạng thái = `"Còn hàng"` (chữ xanh)<br>- Khung tags = `<span>Flash Sale</span><span>Free Ship</span>` | Luồng thành công bình thường. Hiển thị đầy đủ thông tin tính toán giảm giá và nhãn khuyến mãi cho sản phẩm còn hàng. |
| **Trường hợp 2 (Ngoại lệ)** | `product = {`<br>`  id: "SP02",`<br>`  name: "Bàn phím Cơ Wireless",`<br>`  price: 1500000,`<br>`  discountPercent: 0,`<br>`  inStock: false,`<br>`  imageUrl: "",`<br>`  tags: []`<br>`}` | - `img.src` = `"https://via.placeholder.com/200"` (ảnh mặc định)<br>- Tiêu đề = `"Bàn phím Cơ Wireless"`<br>- Giá hiển thị = `"1.500.000 đ"` (ẩn phần giá KM)<br>- Trạng thái = `"Hết hàng"` (chữ đỏ, làm mờ thẻ card sản phẩm)<br>- Khung tags = *(Trống)* | Xử lý dữ liệu thiếu (ảnh rỗng), sản phẩm không giảm giá và hết hàng trong kho. |


## 3. Các bước thực hiện & Quy định kỹ thuật
- **Tài nguyên & Môi trường**: 
  - Thực thi trên môi trường Trình duyệt Web (JavaScript Standard ES6+).
  - Tạo cấu trúc khung HTML cố định chứa các thẻ có định danh ID/Class rõ ràng (ví dụ: `#product-card`, `#product-img`, `#product-title`, `#original-price`, `#sale-price`, `#stock-status`, `#tag-container`).
- **Yêu cầu kỹ thuật**:
  - Học viên tự chủ động thiết kế thuật toán định dạng tiền tệ (VNĐ), tính toán giá sau giảm và truy xuất cấu trúc mã nguồn (Closed How).
  - **Không viết sẵn Code Skeleton**: Học viên tự khai báo các biến lưu trữ phần tử DOM và tự chọn phương thức truy xuất phù hợp (`getElementById`, `querySelector`, `querySelectorAll`).
  - **Xử lý dữ liệu biên & ngoại lệ**: 
    - Kiểm tra `imageUrl`: Nếu là chuỗi rỗng hoặc `undefined`, tự động thế bằng một URL ảnh placeholder mặc định.
    - Kiểm tra `discountPercent`: Nếu nằm ngoài khoảng từ `0` đến `100` hoặc không hợp lệ, mặc định coi như không giảm giá (`0%`).
    - Định dạng tiền tệ chính xác kèm đơn vị `"đ"` hoặc `"VNĐ"`.
  - **Quy chuẩn đặt tên & Clean Code**: 
    - Đặt tên biến đại diện phần tử DOM với tiền tố/hậu tố rõ ràng (ví dụ: `titleNode`, `productImgEl`, `priceContainer`).
    - Tách biệt logic xử lý dữ liệu (tính giá, format tiền) và logic cập nhật giao diện DOM.
  - **Phạm vi kiến thức giới hạn nghiêm ngặt**:
    - KHÔNG sử dụng Bắt sự kiện (`addEventListener`, `onclick`...).
    - KHÔNG sử dụng Xử lý Form Submit.
    - KHÔNG sử dụng Fetch API / Axios hay Lưu trữ dữ liệu (`LocalStorage`, `SessionStorage`).
    - Mã chương trình sẽ được thực thi trực tiếp bằng cách gọi hàm render với dữ liệu đối tượng `product` mẫu khi trang web vừa tải xong.


## 4. Checklist đánh giá kết quả (Nghiệm thu)
- [ ] Xây dựng hoàn chỉnh chương trình đáp ứng đúng bối cảnh nghiệp vụ doanh nghiệp.
- [ ] Trả về kết quả Output chính xác theo đúng bảng ví dụ minh họa.
- [ ] Bắt lỗi ngoại lệ và xử lý dữ liệu biên an toàn không gây crash chương trình.
- [ ] Mã nguồn đạt chuẩn Clean Code, đặt tên biến/hàm đúng quy chuẩn và có chú thích rõ ràng.