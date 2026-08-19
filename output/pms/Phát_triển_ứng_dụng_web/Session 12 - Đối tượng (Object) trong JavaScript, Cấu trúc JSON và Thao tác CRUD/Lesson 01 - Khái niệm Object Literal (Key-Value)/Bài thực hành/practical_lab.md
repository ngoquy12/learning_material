# Bài thực hành: Xây dựng Module Quản lý Thuộc tính Sản phẩm E-commerce với Object Literal

## 1. Mục tiêu bài học
- Vận dụng kiến thức JavaScript Vanilla (ES6+), HTML5/CSS3, DOM API và Cursor AI IDE để khởi tạo và thao tác với cấu trúc dữ liệu Object Literal trong ứng dụng E-commerce.
- Thành thạo kỹ thuật truy cập thuộc tính qua Dot Notation và Bracket Notation, phân biệt trường hợp sử dụng tên khóa chuẩn và tên khóa chứa ký tự đặc biệt.
- Xây dựng cơ chế truy cập thuộc tính an toàn, xử lý triệt để các tình huống thuộc tính chưa định nghĩa (undefined) nhằm tránh bẫy lỗi ReferenceError, SyntaxError và TypeError.
- Thực hành hiển thị thông tin sản phẩm và nhật ký cảnh báo hệ thống lên giao diện Web thông qua DOM API.

## 2. Yêu cầu bài toán
Trong hệ thống Quản lý Sản phẩm E-commerce, dữ liệu chi tiết của một sản phẩm thường chứa nhiều loại thuộc tính khác nhau: thuộc tính định danh cơ bản (id, name, price), thuộc tính cấu hình mở rộng chứa ký tự đặc biệt (warranty-period, inventory-count, warehouse-location), và các thông số kỹ thuật lồng nhau (specs: screen, ram, storage).

Bạn hãy xây dựng một ứng dụng nhỏ bằng JavaScript Vanilla và DOM API với các yêu cầu sau:
1. Định nghĩa đối tượng `detailProduct` sử dụng cú pháp Object Literal chứa đầy đủ thông tin sản phẩm như mô tả.
2. Viết hàm `getSafeAttribute(productObj, attributeKey)` nhận vào đối tượng sản phẩm và tên thuộc tính cần đọc:
   - Sử dụng Bracket Notation để đọc giá trị động.
   - Nếu thuộc tính tồn tại và khác `undefined`, trả về giá trị của thuộc tính đó.
   - Nếu thuộc tính không tồn tại (`undefined`), trả về chuỗi cảnh báo an toàn: `[CẢNH BÁO] Thuộc tính '[attributeKey]' không tồn tại trên sản phẩm.`
3. Viết hàm `getNestedAttribute(productObj, parentKey, childKey)` để đọc thuộc tính đối tượng con (ví dụ: specs.ram):
   - Kiểm tra xem đối tượng cha `productObj[parentKey]` có tồn tại trước khi đọc `childKey` để phòng tránh bẫy lỗi `TypeError` (reading property of undefined).
   - Trả về giá trị hoặc thông báo cảnh báo an toàn tương ứng nếu đối tượng cha hoặc khóa con không tồn tại.
4. Sử dụng DOM API để render thông tin sản phẩm hợp lệ lên thẻ HTML `#product-card`, đồng thời render danh sách thông báo nhật ký khi kiểm thử các thuộc tính không tồn tại lên thẻ HTML `#log-output`.

## 3. Các bước thực hiện
- **Tài nguyên đầu vào**: Môi trường phát triển bao gồm trình soạn thảo Cursor AI IDE, trình duyệt Web (Chrome/Firefox/Edge), cấu trúc tệp mã nguồn gồm index.html, style.css, app.js và bộ dữ liệu sản phẩm mẫu.

### Các bước thực hiện:
1. Bước 1: Khởi tạo thư mục dự án trong Cursor AI IDE, tạo các tệp index.html, style.css và app.js. Nhúng tệp app.js và style.css vào index.html.
2. Bước 2: Trong tệp app.js, định nghĩa đối tượng `detailProduct` bằng cú pháp Object Literal chứa đầy đủ các thuộc tính khóa chuẩn, thuộc tính khóa chứa dấu gạch ngang và đối tượng con `specs`.
3. Bước 3: Xây dựng các hàm `getSafeAttribute` và `getNestedAttribute` xử lý logic truy cập dữ liệu an toàn bằng Bracket Notation và kiểm tra điều kiện undefined.
4. Bước 4: Sử dụng DOM API (document.getElementById, innerHTML) để lấy dữ liệu từ đối tượng sản phẩm, hiển thị thông tin lên màn hình và kiểm tra bẫy lỗi với các thuộc tính không hợp lệ.
5. Bước 5: Kiểm tra kết quả chạy trên trình duyệt web, mở Trình duyệt Console để xác nhận không phát sinh SyntaxError, ReferenceError hay TypeError.

## 4. Mã nguồn tham khảo (Code Demo)

```text
// --- TỆP INDEX.HTML ---
/*
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Hệ thống Quản lý Sản phẩm E-commerce</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="container">
    <h1>Quản lý Thông tin Sản phẩm</h1>
    <div id="product-card" class="card"></div>
    <div id="log-output" class="log-panel"></div>
  </div>
  <script src="app.js"></script>
</body>
</html>
*/

// --- TỆP APP.JS ---
// 1. Khai báo đối tượng sản phẩm bằng Object Literal
const detailProduct = {
  id: "PHONE-FLAGSHIP-01",
  name: "Điện thoại Flagship Ultra",
  price: 29990000,
  brand: "Rikkei Tech",
  "warranty-period": "24 tháng",
  "inventory-count": 45,
  "warehouse-location": "Kho A - Tầng 2",
  specs: {
    screen: "6.7 inch OLED",
    ram: "12GB",
    storage: "256GB"
  }
};

// 2. Hàm truy cập thuộc tính an toàn cấp 1 dùng Bracket Notation
function getSafeAttribute(productObj, attributeKey) {
  // BẪY LỖI 1: Luôn truyền tên khóa dưới dạng chuỗi hoặc biến chứa chuỗi vào ngoặc vuông [].
  // BẪY LỖI 2: Dùng Bracket Notation cho tên khóa có dấu gạch ngang (không dùng Dot Notation).
  const attributeValue = productObj[attributeKey];

  if (attributeValue === undefined) {
    return `[CẢNH BÁO] Thuộc tính '${attributeKey}' không tồn tại trên sản phẩm.`;
  }

  return attributeValue;
}

// 3. Hàm truy cập thuộc tính lồng nhau an toàn (Ngăn ngừa TypeError)
function getNestedAttribute(productObj, parentKey, childKey) {
  // Kiểm tra đối tượng cha trước khi truy cập thuộc tính con
  const parentObj = productObj[parentKey];
  
  if (parentObj === undefined || typeof parentObj !== "object" || parentObj === null) {
    return `[CẢNH BÁO] Thuộc tính cha '${parentKey}' không tồn tại hoặc không phải là một đối tượng.`;
  }

  const childValue = parentObj[childKey];
  if (childValue === undefined) {
    return `[CẢNH BÁO] Thuộc tính con '${childKey}' không tồn tại trong '${parentKey}'.`;
  }

  return childValue;
}

// 4. Hàm hiển thị dữ liệu lên giao diện HTML bằng DOM API
function renderApp() {
  const productCardEl = document.getElementById("product-card");
  const logOutputEl = document.getElementById("log-output");

  // Truy xuất dữ liệu hợp lệ
  const productId = detailProduct.id; // Dot Notation cho khóa chuẩn
  const productName = detailProduct.name;
  const formattedPrice = detailProduct.price.toLocaleString("vi-VN");
  const warranty = getSafeAttribute(detailProduct, "warranty-period"); // Bracket Notation cho khóa đặc biệt
  const location = getSafeAttribute(detailProduct, "warehouse-location");
  const ramSpec = getNestedAttribute(detailProduct, "specs", "ram");

  // Thử nghiệm các trường hợp thuộc tính không tồn tại để kiểm chứng bẫy lỗi
  const invalidAttrTest = getSafeAttribute(detailProduct, "description");
  const invalidNestedTest = getNestedAttribute(detailProduct, "category", "name");

  // Render thông tin sản phẩm
  productCardEl.innerHTML = `
    <h2>${productName}</h2>
    <p><strong>Mã sản phẩm:</strong> ${productId}</p>
    <p><strong>Giá bán:</strong> ${formattedPrice} VNĐ</p>
    <p><strong>Bảo hành:</strong> ${warranty}</p>
    <p><strong>Vị trí kho:</strong> ${location}</p>
    <p><strong>Dung lượng RAM:</strong> ${ramSpec}</p>
  `;

  // Render nhật ký cảnh báo lỗi an toàn
  logOutputEl.innerHTML = `
    <h3>Nhật ký Kiểm tra Truy xuất Hệ thống</h3>
    <ul>
      <li class="log-item warning">${invalidAttrTest}</li>
      <li class="log-item warning">${invalidNestedTest}</li>
    </ul>
  `;
}

// Chạy hàm khi trang web tải xong nội dung DOM
document.addEventListener("DOMContentLoaded", renderApp);
```

# 5. Checklist đánh giá kết quả
- [ ] Khai báo chính xác đối tượng Object Literal chứa đầy đủ thông tin thuộc tính khóa chuẩn, thuộc tính đặc biệt có dấu gạch ngang và thuộc tính lồng nhau.
- [ ] Phân biệt và sử dụng đúng Dot Notation cho thuộc tính chuẩn và Bracket Notation cho thuộc tính đặc biệt hoặc tên thuộc tính dạng biến.
- [ ] Xây dựng thành công hàm `getSafeAttribute` và `getNestedAttribute` xử lý giá trị undefined, ngăn ngừa các lỗi ReferenceError, SyntaxError và TypeError.
- [ ] Sử dụng DOM API để render dữ liệu sản phẩm và danh sách cảnh báo kiểm thử thành công trên giao diện Web mà không phát sinh lỗi ở trình duyệt Console.
- [ ] Mã nguồn ngắn gọn, tuân thủ tiêu chuẩn JavaScript ES6+, trình bày sạch sẻ và có chú thích rõ ràng trong môi trường Cursor AI IDE.
