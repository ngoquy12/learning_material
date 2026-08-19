# Bài tập tổng hợp trên lớp: Cập nhật giao diện thẻ sản phẩm E-Commerce


## 1. Mục tiêu bài tập
- Nắm vững kỹ thuật truy xuất các phần tử trong cây DOM Tree bằng các phương thức chuẩn (`getElementById`, `querySelector`, `querySelectorAll`).
- Thực hành thao tác cập nhật linh hoạt nội dung văn bản, cấu trúc HTML (`textContent`, `innerHTML`) và các thuộc tính của phần tử (`src`, `alt`, `disabled`, `classList`, `style`).
- Áp dụng tư duy xử lý logic nghiệp vụ bán hàng (tính toán giá sau giảm, định dạng tiền tệ, cập nhật trạng thái tồn kho và hiển thị nhãn khuyến mãi) trực tiếp lên giao diện trình duyệt.


## 2. Mô tả bối cảnh & Yêu cầu bài toán (Input / Output)
- **Bối cảnh doanh nghiệp**: Trên trang danh mục sản phẩm của hệ thống bán hàng trực tuyến, thông tin sản phẩm từ hệ thống quản trị cần được đổ dữ liệu và hiển thị tự động lên thẻ sản phẩm (Product Card). Chương trình cần xử lý việc cập nhật tên, hình ảnh, tính toán giá bán thực tế sau khi áp dụng mã giảm giá, đổi trạng thái nút mua hàng dựa trên lượng hàng tồn kho và điều khiển ẩn/hiện các nhãn ưu đãi theo đúng dữ liệu đầu vào.
- **Dữ liệu đầu vào (Input)**: Một đối tượng JavaScript `product` đại diện cho dữ liệu sản phẩm có cấu trúc như sau:
  - `id` (string): Mã định danh sản phẩm.
  - `name` (string): Tên sản phẩm.
  - `originalPrice` (number): Giá gốc sản phẩm (đơn vị: VNĐ).
  - `discountPercent` (number): Phần trăm giảm giá (từ 0 đến 100).
  - `stockQuantity` (number): Số lượng tồn kho.
  - `imageUrl` (string): Đường dẫn hình ảnh sản phẩm.
  - `isFeatured` (boolean): Trạng thái sản phẩm nổi bật.

- **Kết quả đầu ra (Output)**: Các phần tử DOM tương ứng trên trang web được cập nhật hiển thị chính xác:
  - Phần tử tiêu đề (`#product-title`): Cập nhật văn bản hiển thị tên sản phẩm.
  - Phần tử giá gốc (`#product-price-original`): Hiển thị giá gốc định dạng `XXX.XXX VNĐ`. Nếu `discountPercent > 0`, áp dụng kiểu chữ gạch ngang (`text-decoration: line-through`), ngược lại bỏ gạch ngang.
  - Phần tử giá bán (`#product-price-final`): Hiển thị giá bán thực tế `XXX.XXX VNĐ` sau khi đã trừ phần trăm giảm giá (`Giá bán = Giá gốc * (100 - discountPercent) / 100`).
  - Phần tử nhãn tồn kho (`#product-stock-badge`):
    - Nếu `stockQuantity > 0`: Cập nhật text `Còn hàng (${stockQuantity})`, thêm class `badge-success`, xóa class `badge-danger`.
    - Nếu `stockQuantity <= 0`: Cập nhật text `Hết hàng`, thêm class `badge-danger`, xóa class `badge-success`.
  - Nút bấm mua hàng (`#btn-add-to-cart`): Cập nhật thuộc tính `disabled = true` nếu `stockQuantity <= 0`; cập nhật `disabled = false` nếu `stockQuantity > 0`.
  - Ảnh sản phẩm (`#product-image`): Cập nhật thuộc tính `src` bằng `imageUrl` và thuộc tính `alt` bằng `name`.
  - Nhãn nổi bật (`#featured-tag`): Thiết lập kiểu hiển thị `display: inline-block` nếu `isFeatured === true`, ngược lại thiết lập `display: none`.


### Bảng ví dụ minh họa Input/Output:

| Trường hợp (Case) | Dữ liệu đầu vào (Input) | Kết quả kỳ vọng (Expected Output) | Ghi chú nghiệp vụ |
| :--- | :--- | :--- | :--- |
| **Trường hợp 1 (Chuẩn)** | `{ id: "P01", name: "Laptop Gaming", originalPrice: 20000000, discountPercent: 10, stockQuantity: 5, imageUrl: "laptop.jpg", isFeatured: true }` | - `#product-title`: "Laptop Gaming"<br>- `#product-price-original`: "20.000.000 VNĐ" (có gạch ngang)<br>- `#product-price-final`: "18.000.000 VNĐ"<br>- `#product-stock-badge`: "Còn hàng (5)", chứa class `badge-success`<br>- `#btn-add-to-cart`: `disabled` = `false`<br>- `#product-image`: `src`="laptop.jpg", `alt`="Laptop Gaming"<br>- `#featured-tag`: `style.display` = "inline-block" | Sản phẩm còn hàng, có giảm giá và là sản phẩm nổi bật. |
| **Trường hợp 2 (Ngoại lệ)** | `{ id: "P02", name: "Chuột Không Dây", originalPrice: 500000, discountPercent: 0, stockQuantity: 0, imageUrl: "mouse.jpg", isFeatured: false }` | - `#product-title`: "Chuột Không Dây"<br>- `#product-price-original`: "500.000 VNĐ" (không gạch ngang)<br>- `#product-price-final`: "500.000 VNĐ"<br>- `#product-stock-badge`: "Hết hàng", chứa class `badge-danger`<br>- `#btn-add-to-cart`: `disabled` = `true`<br>- `#product-image`: `src`="mouse.jpg", `alt`="Chuột Không Dây"<br>- `#featured-tag`: `style.display` = "none" | Sản phẩm hết hàng, không có giảm giá, không nổi bật. Nút mua bị khóa. |


## 3. Các bước thực hiện & Quy định kỹ thuật
- **Tài nguyên & Môi trường**: Thực thi trên môi trường trình duyệt Web chuẩn (HTML5 & JavaScript ES6+).
- **Yêu cầu kỹ thuật**:
  - Học viên tự thiết kế cấu trúc HTML ban đầu chứa đầy đủ các selector định danh (`id`, `class`) như mô tả và tự xây dựng hàm xử lý JavaScript để thao tác với DOM Tree.
  - Sử dụng các phương thức truy xuất DOM phù hợp (`document.getElementById`, `document.querySelector`).
  - Xử lý các giá trị biên an toàn: Nếu đối tượng sản phẩm bị `null`, `undefined` hoặc thiếu trường dữ liệu, chương trình cần hiển thị một thông báo lỗi trên khung sản phẩm thay vì làm treo hoặc dừng chương trình.
  - Xây dựng hàm bổ trợ để định dạng giá tiền (thêm dấu chấm phân cách hàng nghìn và đuôi `VNĐ`).
  - Tuân thủ quy chuẩn Clean Code: Đặt tên biến và tên hàm theo chuẩn camelCase (ví dụ: `renderProductCard`, `formatCurrency`), mã nguồn có ghi chú giải thích logic rõ ràng.


## 4. Checklist đánh giá kết quả (Nghiệm thu)
- [ ] Xây dựng hoàn chỉnh chương trình đáp ứng đúng bối cảnh nghiệp vụ doanh nghiệp.
- [ ] Trả về kết quả Output chính xác theo đúng bảng ví dụ minh họa.
- [ ] Bắt lỗi ngoại lệ và xử lý dữ liệu biên an toàn không gây crash chương trình.
- [ ] Mã nguồn đạt chuẩn Clean Code, đặt tên biến/hàm đúng quy chuẩn và có chú thích rõ ràng.