# Bài thực hành: Phát triển Hệ thống Thẻ Sản phẩm Tương tác E-commerce với addEventListener và removeEventListener

## 1. Mục tiêu bài học
- [Cài đặt và cấu hình] Khởi tạo cấu trúc DOM cho thẻ sản phẩm E-commerce và liên kết script xử lý JavaScript.
- [Triển khai logic cốt lõi] Xử lý các sự kiện click (thêm giỏ hàng), dblclick (yêu thích) và mouseover (xem trước trạng thái) sử dụng addEventListener.
- [Kiểm thử và hoàn thiện] Triển khai logic kiểm soát kho, hủy sự kiện bằng removeEventListener và ngăn ngừa các lỗi truyền tham chiếu callback.

## 2. Yêu cầu bài toán
Trong các hệ thống thương mại điện tử hiện đại, trải nghiệm tương tác trực quan trên thẻ sản phẩm đóng vai trò quyết định đến tỷ lệ chuyển đổi đơn hàng. Người dùng cần di chuột để xem nhanh thông tin, nhấp đơn để thêm sản phẩm vào giỏ và nhấp đôi để lưu vào danh sách yêu thích một cách mượt mà mà không cần tải lại trang.

Tuy nhiên, khi số lượng hàng tồn kho chạm mốc giới hạn, hệ thống cần vô hiệu hóa chức năng thêm giỏ hàng ngay lập tức trên giao diện người dùng và gỡ bỏ sự kiện tương tác để tránh việc gửi thừa yêu cầu. Việc này đòi hỏi kỹ thuật quản lý sự kiện chặt chẽ bằng cách đăng ký và hủy đăng ký bộ nghe sự kiện trên trình duyệt.

Với tư cách là Lập trình viên Frontend tại Rikkei Education, bạn được giao nhiệm vụ xây dựng mô-đun tương tác cho thẻ sản phẩm E-commerce. Bạn sẽ áp dụng phương thức addEventListener để lắng nghe đa sự kiện và removeEventListener để gỡ bỏ sự kiện khi hết hàng, đồng thời đảm bảo mã nguồn chuẩn hóa không mắc các lỗi phổ biến khi làm việc với hàm callback.

## 3. Các bước thực hiện
- **Tài nguyên đầu vào**: Môi trường phát triển: Trình duyệt web (Chrome/Edge/Firefox), trình soạn thảo VS Code. Dữ liệu gồm: Nút thêm giỏ hàng (#add-to-cart-btn), nút yêu thích (#wishlist-btn), hình ảnh sản phẩm (.product-image), thẻ hiển thị số lượng giỏ hàng (#cart-badge) và thẻ trạng thái tồn kho (#stock-status).

### Các bước thực hiện:
1. Bước 1: Khởi tạo cấu trúc giao diện HTML/CSS và truy xuất các phần tử DOM cần thiết trong script JavaScript.
2. Bước 2: Định nghĩa các hàm callback có tên (Named Functions) cho các sự kiện: handleAddToCart (click), handleAddToWishlist (dblclick), và handleImageHover (mouseover).
3. Bước 3: Đăng ký các sự kiện tương ứng vào phần tử DOM bằng addEventListener, đảm bảo truyền đúng tham chiếu tên hàm mà không kèm dấu ngoặc đơn () hoặc tiền tố 'on'.
4. Bước 4: Thêm logic kiểm tra giới hạn tồn kho trong handleAddToCart; khi đạt hạn mức tối đa, gỡ bỏ sự kiện click bằng removeEventListener và cập nhật trạng thái giao diện.

## 4. Mã nguồn tham khảo (Code Demo)

```text
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Thẻ Sản Phẩm Tương Tác E-commerce</title>
  <style>
    .product-card {
      width: 320px;
      border: 1px solid #e0e0e0;
      padding: 16px;
      border-radius: 8px;
      text-align: center;
      font-family: Arial, sans-serif;
    }
    .product-image {
      width: 100%;
      height: 200px;
      object-fit: cover;
      border-radius: 4px;
      cursor: pointer;
    }
    .badge {
      background: #007bff;
      color: white;
      padding: 4px 8px;
      border-radius: 12px;
      font-weight: bold;
    }
    .stock-info {
      margin: 10px 0;
      color: #28a745;
      font-weight: bold;
    }
    .btn {
      margin: 5px;
      padding: 8px 16px;
      cursor: pointer;
      border: none;
      border-radius: 4px;
      font-weight: bold;
    }
    .btn-cart {
      background-color: #28a745;
      color: white;
    }
    .btn-wishlist {
      background-color: #ffc107;
      color: black;
    }
    .disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
  </style>
</head>
<body>
  <div class="product-card">
    <img class="product-image" src="https://via.placeholder.com/300x200" alt="Sản phẩm mẫu">
    <h3>Tai nghe Bluetooth Pro</h3>
    <p class="stock-info" id="stock-status">Trạng thái: Sẵn sàng phục vụ</p>
    <p>Giỏ hàng: <span class="badge" id="cart-badge">0</span></p>
    <p id="wishlist-status"></p>
    
    <button class="btn btn-cart" id="add-to-cart-btn">Thêm vào giỏ hàng</button>
    <button class="btn btn-wishlist" id="wishlist-btn">Nhấp đôi để yêu thích</button>
  </div>

  <script>
    // 1. Truy xuất các phần tử DOM
    const addToCartBtn = document.querySelector('#add-to-cart-btn');
    const wishlistBtn = document.querySelector('#wishlist-btn');
    const cartBadge = document.querySelector('#cart-badge');
    const stockStatus = document.querySelector('#stock-status');
    const wishlistStatus = document.querySelector('#wishlist-status');
    const productImage = document.querySelector('.product-image');

    let cartCount = 0;
    const maxStock = 3;

    // 2. Định nghĩa các hàm callback có tên rõ ràng (Named Callback Functions)
    function handleAddToCart() {
      if (cartCount < maxStock) {
        cartCount++;
        cartBadge.textContent = cartCount;
        console.log('Đã thêm sản phẩm vào giỏ. Số lượng:', cartCount);
      }

      // Kiểm tra chạm trần số lượng tồn kho
      if (cartCount >= maxStock) {
        stockStatus.textContent = 'Trạng thái: Đã hết hàng tồn kho!';
        stockStatus.style.color = 'red';
        addToCartBtn.classList.add('disabled');
        
        // Hủy đăng ký sự kiện click bằng đúng tham chiếu hàm đã khai báo
        addToCartBtn.removeEventListener('click', handleAddToCart);
        console.log('Hệ thống: Đã gỡ bỏ sự kiện click do sản phẩm vượt quá tồn kho.');
      }
    }

    function handleAddToWishlist() {
      wishlistStatus.textContent = 'Đã thêm vào danh sách yêu thích!';
      wishlistStatus.style.color = '#d9534f';
      console.log('Sự kiện dblclick kích hoạt: Đã lưu vào yêu thích.');
    }

    function handleImageHover() {
      if (cartCount < maxStock) {
        const remaining = maxStock - cartCount;
        stockStatus.textContent = 'Trạng thái: Còn lại ' + remaining + ' sản phẩm trong kho';
      }
    }

    // 3. Đăng ký sự kiện với addEventListener
    // ĐÚNG: Chỉ truyền tham chiếu tên hàm, không có dấu () và không dùng tiền tố 'on'
    addToCartBtn.addEventListener('click', handleAddToCart);
    wishlistBtn.addEventListener('dblclick', handleAddToWishlist);
    productImage.addEventListener('mouseover', handleImageHover);
  </script>
</body>
</html>
```

## 5. Checklist đánh giá kết quả
- [ ] Khởi tạo đúng cấu trúc giao diện HTML và liên kết chính xác các phần tử DOM trong JavaScript
- [ ] Đăng ký thành công các sự kiện click, dblclick, mouseover bằng phương thức addEventListener
- [ ] Truyền đúng tham chiếu hàm callback (không dùng tiền tố 'on' như 'onclick' và không chứa dấu () gây thực thi ngay)
- [ ] Triển khai gỡ bỏ bộ nghe sự kiện thành công bằng removeEventListener khi số lượng đạt hạn mức kho
- [ ] Mã nguồn hoạt động chuẩn xác trên trình duyệt, xử lý các trạng thái giao diện đúng yêu cầu và không phát sinh lỗi console