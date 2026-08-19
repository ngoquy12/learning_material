# Bài thực hành: Xây dựng Module Tính toán và Xử lý Đơn hàng E-commerce với Biến ES6

## 1. Mục tiêu bài học
- Vận dụng kiến thức JavaScript Vanilla (ES6+), HTML5/CSS3, DOM API và Cursor AI IDE để khai báo, phân biệt và quản lý chính xác phạm vi của let, const và var.
- Thực hành áp dụng chuẩn đặt tên Naming Convention (camelCase cho biến, UPPER_SNAKE_CASE cho hằng số cố định) và phân biệt đúng các kiểu dữ liệu nguyên thủy (number, string, boolean, null, undefined).
- Thành thạo thao tác tính toán dòng tiền đơn hàng và render thông tin kết quả lên giao diện HTML bằng DOM API.

## 2. Yêu cầu bài toán
Trong hệ thống thương mại điện tử, việc tính toán giá trị đơn hàng yêu cầu độ chính xác tuyệt đối và mã nguồn phải tuân thủ nghiêm ngặt chuẩn đặt tên để dễ bảo trì. Bạn được giao nhiệm vụ khởi tạo một module quản lý đơn hàng. Module này cần lưu trữ cấu hình hằng số hệ thống (tỷ lệ thuế VAT, mã cửa hàng), các thông tin đơn hàng biến đổi (số lượng, phí vận chuyển, chiết khấu), xử lý các trạng thái dữ liệu nguyên thủy (bao gồm trạng thái chưa nhập địa chỉ undefined và trạng thái không dùng mã giảm giá null), sau đó tính toán tổng chi phí và hiển thị kết quả chi tiết lên giao diện người dùng thông qua DOM API.

## 3. Các bước thực hiện
- **Tài nguyên đầu vào**: Môi trường phát triển Cursor AI IDE, trình duyệt web modern (Chrome/Firefox/Edge), tệp cấu trúc HTML5 cơ bản và tệp mã nguồn JavaScript ES6+.

### Các bước thực hiện:
1. Bước 1: Khởi tạo thư mục dự án trong Cursor AI IDE, tạo hai tệp `index.html` và `app.js`. Liên kết tệp `app.js` vào tệp HTML.
2. Bước 2: Trong tệp `app.js`, khai báo các hằng số hệ thống cố định (VAT_RATE, STORE_ID) bằng từ khóa `const` theo chuẩn UPPER_SNAKE_CASE.
3. Bước 3: Khai báo các thông tin giỏ hàng (tên sản phẩm, đơn giá, số lượng, phí vận chuyển, mã chiết khấu) bằng `const` hoặc `let` theo chuẩn camelCase. Đảm bảo phân biệt rõ biến có thể thay đổi và biến hằng số.
4. Bước 4: Khởi tạo biến `customerAddress` không gán giá trị (để mang giá trị `undefined`) và biến `couponCode` gán giá trị `null` để biểu thị việc khách hàng không áp dụng mã giảm giá.
5. Bước 5: Thực hiện các phép tính toán tài chính: Tạm tính (subtotal), Tổng tiền sau chiết khấu (totalAfterDiscount), Tiền thuế VAT (taxAmount) và Tổng tiền thanh toán cuối cùng (finalAmount).
6. Bước 6: Sử dụng DOM API (`document.getElementById` và `innerHTML`) để truy xuất phần tử trên trang HTML và hiển thị toàn bộ hóa đơn đơn hàng cùng trạng thái xử lý.
7. Bước 7: Kiểm tra Console log để xác nhận kiểu dữ liệu (`typeof`) của các biến `customerAddress` và `couponCode`, đảm bảo mã chạy không có lỗi runtime.

## 4. Mã nguồn tham khảo (Code Demo)

```text
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hệ thống Quản lý Giỏ hàng E-commerce</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f6f9;
            margin: 20px;
            line-height: 1.6;
        }
        .order-card {
            background-color: #ffffff;
            border: 1px solid #dddddd;
            border-radius: 8px;
            padding: 20px;
            max-width: 480px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .order-card h2 {
            margin-top: 0;
            color: #333333;
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
        }
        .detail-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
        }
        .total-price {
            font-size: 1.2em;
            font-weight: bold;
            color: #d9534f;
            border-top: 1px solid #eee;
            padding-top: 10px;
        }
        .badge {
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.85em;
            font-weight: bold;
        }
        .badge-success {
            background-color: #d4edda;
            color: #155724;
        }
    </style>
</head>
<body>
    <div class="order-card">
        <h2>Chi Tiết Đơn Hàng</h2>
        <div id="order-content">Đang tải dữ liệu đơn hàng...</div>
    </div>

    <script>
        // 1. Hằng số cấu hình hệ thống cố định (UPPER_SNAKE_CASE)
        const VAT_RATE = 0.1;
        const STORE_ID = "STORE-VN-01";

        // 2. Thông tin sản phẩm và giỏ hàng (camelCase, let/const phù hợp)
        const productName = "Laptop Gaming X Pro";
        const unitPrice = 25000000;
        let quantity = 2;

        // 3. Phí vận chuyển và chiết khấu (let vì giá trị có thể cập nhật sau)
        let shippingFee = 50000;
        let discountAmount = 1000000;
        let isVipCustomer = true;

        // 4. Quản lý trạng thái dữ liệu nguyên thủy: undefined và null
        let customerAddress; // Chưa gán giá trị -> undefined
        let couponCode = null; // Chủ động gán null -> không áp dụng mã giảm giá

        // 5. Tính toán các giá trị tài chính của đơn hàng
        let subtotal = unitPrice * quantity;
        let totalAfterDiscount = subtotal - discountAmount;
        let taxAmount = totalAfterDiscount * VAT_RATE;
        let finalAmount = totalAfterDiscount + taxAmount + shippingFee;

        // 6. Trạng thái xử lý đơn hàng (boolean)
        let isOrderConfirmed = true;
        let isOrderShipped = false;

        // 7. Hiển thị dữ liệu lên giao diện HTML bằng DOM API
        const orderContentEl = document.getElementById("order-content");

        orderContentEl.innerHTML = `
            <div class="detail-row"><span>Mã cửa hàng:</span> <strong>${STORE_ID}</strong></div>
            <div class="detail-row"><span>Sản phẩm:</span> <strong>${productName}</strong></div>
            <div class="detail-row"><span>Đơn giá:</span> <span>${unitPrice.toLocaleString('vi-VN')} VNĐ</span></div>
            <div class="detail-row"><span>Số lượng:</span> <span>${quantity}</span></div>
            <div class="detail-row"><span>Tạm tính:</span> <span>${subtotal.toLocaleString('vi-VN')} VNĐ</span></div>
            <div class="detail-row"><span>Giảm giá:</span> <span>-${discountAmount.toLocaleString('vi-VN')} VNĐ</span></div>
            <div class="detail-row"><span>Thuế VAT (${VAT_RATE * 100}%):</span> <span>+${taxAmount.toLocaleString('vi-VN')} VNĐ</span></div>
            <div class="detail-row"><span>Phí vận chuyển:</span> <span>+${shippingFee.toLocaleString('vi-VN')} VNĐ</span></div>
            <div class="detail-row total-price"><span>Tổng thanh toán:</span> <span>${finalAmount.toLocaleString('vi-VN')} VNĐ</span></div>
            <hr>
            <div class="detail-row"><span>Địa chỉ giao hàng:</span> <i>${customerAddress === undefined ? "Chưa nhập địa chỉ (undefined)" : customerAddress}</i></div>
            <div class="detail-row"><span>Mã giảm giá:</span> <i>${couponCode === null ? "Không áp dụng (null)" : couponCode}</i></div>
            <div class="detail-row"><span>Trạng thái:</span> <span class="badge badge-success">${isOrderConfirmed ? "Đã xác nhận" : "Đang chờ"}</span></div>
        `;

        // Kiểm tra log ra DevTools Console
        console.log("=== ĐƠN HÀNG ĐÃ ĐƯỢC TÍNH TOÁN ===");
        console.log("Kiểu dữ liệu của customerAddress:", typeof customerAddress);
        console.log("Kiểu dữ liệu của couponCode:", typeof couponCode);
        console.log("Kiểu dữ liệu của isOrderConfirmed:", typeof isOrderConfirmed);
    </script>
</body>
</html>
```

# 5. Checklist đánh giá kết quả
- [ ] Khai báo chính xác từ khóa `const` cho các hằng số không đổi và `let` cho các biến có thay đổi giá trị; tuyệt đối không gán lại giá trị cho biến `const`.
- [ ] Đặt tên biến tuân thủ đúng quy tắc Naming Convention (camelCase cho tên biến thường, UPPER_SNAKE_CASE cho hằng số cấu hình hệ thống), không sử dụng Tiếng Việt có dấu hay ký tự đặc biệt.
- [ ] Phân biệt đúng cách sử dụng và hiển thị của kiểu dữ liệu nguyên thủy `undefined` (biến chưa gán giá trị) và `null` (chủ động rỗng).
- [ ] Tính toán chính xác tổng chi phí đơn hàng (gồm tạm tính, giảm giá, thuế VAT và phí giao hàng).
- [ ] Thao tác thành công với DOM API (`getElementById`, `innerHTML`) để render giao diện đẹp mắt và chính xác.
