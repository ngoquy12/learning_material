# Bài thực hành: Xây dựng Trình Quản lý Giỏ hàng và Áp dụng Mã Giảm giá E-commerce với Closure và Scope

## 1. Mục tiêu bài học
- Vận dụng kiến thức JavaScript ES6+ bao gồm Phạm vi biến (Global/Local Scope) và Closure để xây dựng mô-đun quản lý giỏ hàng độc lập.
- Bảo vệ dữ liệu giao dịch tư nhân (private state) tránh tình trạng ô nhiễm Global Scope hoặc can thiệp dữ liệu trái phép từ Console.
- Kết nối logic tính toán với DOM API để cập nhật giao diện người dùng và tự động xử lý tính toán thuế, giảm giá.
- Sử dụng Cursor AI IDE để rà soát lỗi Temporal Dead Zone (TDZ) và tối ưu hóa mã nguồn theo tiêu chuẩn ES6+.

## 2. Yêu cầu bài toán
Doanh nghiệp E-commerce Rikkei Store cần xây dựng mô-đun quản lý giỏ hàng trực tuyến. Mô-đun cần thỏa mãn các quy tắc nghiệp vụ sau:
1. Khai báo các cấu hình toàn cục (Global Scope) dùng chung như tỷ lệ thuế GTGT (GLOBAL_TAX_RATE = 0.1) và đơn vị tiền tệ (GLOBAL_CURRENCY = 'VND').
2. Xây dựng hàm `createCartManager(customerName)` ứng dụng Closure để trả về một đối tượng quản lý giỏ hàng riêng cho từng khách hàng. Dữ liệu mảng mặt hàng `cartItems` và tỷ lệ giảm giá `discountPercent` phải là private state, không thể truy cập trực tiếp từ môi trường toàn cục.
3. Đối tượng giỏ hàng cung cấp các phương thức công khai (public API): `addItem(name, price, quantity)`, `applyVoucher(code)`, `calculateTotal()`, và `getCartSummary()`.
4. Mã giảm giá quy định: 'RIKKEI10' giảm 10%, 'VIP20' giảm 20%. Mọi mã khác báo lỗi không hợp lệ.
5. Tích hợp DOM API để hiển thị danh sách giỏ hàng, thông tin hóa đơn và các thao tác thêm sản phẩm/áp mã voucher trên giao diện người dùng.

## 3. Các bước thực hiện
- **Tài nguyên đầu vào**: Môi trường phát triển Cursor AI IDE cùng với cấu trúc tệp chuẩn bị gồm index.html, style.css và app.js.

### Các bước thực hiện:
1. Bước 1: Khởi tạo dự án trên Cursor AI IDE với tệp index.html tạo giao diện giỏ hàng và tệp app.js để viết mã logic JavaScript.
2. Bước 2: Khai báo các hằng số toàn cục (Global Scope) quản lý thuế GTGT và đơn vị tiền tệ ở đầu tệp app.js.
3. Bước 3: Định nghĩa hàm factory function `createCartManager(customerName)` ứng dụng kỹ thuật Closure để đóng gói mảng danh sách sản phẩm và phần trăm giảm giá.
4. Bước 4: Cài đặt các hàm xử lý sự kiện với DOM API để lắng nghe hành động nhập sản phẩm, bấm nút thêm vào giỏ và nút áp dụng mã giảm giá.
5. Bước 5: Thực hiện kiểm thử tính đóng gói dữ liệu: xác nhận không thể truy cập trực tiếp mảng giỏ hàng qua console, đồng thời rà soát lỗi TDZ khi khai báo biến/hàm.

## 4. Mã nguồn tham khảo (Code Demo)

```text
// 1. GLOBAL SCOPE: Cấu hình chung cho toàn hệ thống
const GLOBAL_TAX_RATE = 0.1; // Thuế GTGT 10%
const GLOBAL_CURRENCY = "VND";

// 2. CLOSURE FACTORY: Tạo trình quản lý giỏ hàng với Private State
function createCartManager(customerName) {
  // Private state: Bảo vệ tuyệt đối bên trong đóng phạm vi của hàm
  const cartItems = [];
  let discountPercent = 0;

  return {
    addItem: (name, price, quantity = 1) => {
      if (!name || price <= 0 || quantity <= 0) {
        return { success: false, message: "Thông tin sản phẩm không hợp lệ" };
      }
      const newItem = {
        id: "SKU-" + Date.now().toString().slice(-4),
        name,
        price: Number(price),
        quantity: Number(quantity)
      };
      cartItems.push(newItem);
      return { success: true, item: newItem };
    },

    applyVoucher: (voucherCode) => {
      // Local scope variable
      const cleanCode = voucherCode.trim().toUpperCase();
      if (cleanCode === "RIKKEI10") {
        discountPercent = 0.1;
        return { success: true, message: "Áp dụng mã RIKKEI10 thành công (Giảm 10%)" };
      } else if (cleanCode === "VIP20") {
        discountPercent = 0.2;
        return { success: true, message: "Áp dụng mã VIP20 thành công (Giảm 20%)" };
      }
      return { success: false, message: "Mã giảm giá không hợp lệ hoặc đã hết hạn" };
    },

    calculateTotal: () => {
      // Local scope variables phục vụ tính toán tạm thời
      let subtotal = 0;
      for (const item of cartItems) {
        subtotal += item.price * item.quantity;
      }

      const discountAmount = subtotal * discountPercent;
      const amountAfterDiscount = subtotal - discountAmount;
      const taxAmount = amountAfterDiscount * GLOBAL_TAX_RATE;
      const finalTotal = amountAfterDiscount + taxAmount;

      return {
        subtotal,
        discountAmount,
        taxAmount,
        finalTotal
      };
    },

    getCartSummary: () => {
      return {
        customer: customerName,
        totalQuantity: cartItems.reduce((sum, item) => sum + item.quantity, 0),
        items: [...cartItems] // Trả về bản sao shallow copy để tránh đột biến trực tiếp từ ngoài
      };
    }
  };
}

// 3. MINH HỌA TƯƠNG TÁC VỚI DOM API VÀ XỬ LÝ GIAO DIỆN
document.addEventListener("DOMContentLoaded", () => {
  // Khởi tạo phiên giỏ hàng cho khách hàng Nguyen Van A
  const userCart = createCartManager("Nguyen Van A");

  const btnAdd = document.getElementById("btn-add");
  const btnVoucher = document.getElementById("btn-voucher");
  const cartListContainer = document.getElementById("cart-list");
  const invoiceSummaryContainer = document.getElementById("invoice-summary");

  const renderCartUI = () => {
    const summary = userCart.getCartSummary();
    const totals = userCart.calculateTotal();

    // Render danh sách sản phẩm
    cartListContainer.innerHTML = summary.items.map(item => `
      <div class="cart-item">
        <span>${item.name} x ${item.quantity}</span>
        <span>${(item.price * item.quantity).toLocaleString()} ${GLOBAL_CURRENCY}</span>
      </div>
    `).join("");

    // Render tổng hóa đơn
    invoiceSummaryContainer.innerHTML = `
      <p>Khách hàng: <strong>${summary.customer}</strong></p>
      <p>Tạm tính: ${totals.subtotal.toLocaleString()} ${GLOBAL_CURRENCY}</p>
      <p>Giảm giá: -${totals.discountAmount.toLocaleString()} ${GLOBAL_CURRENCY}</p>
      <p>Thuế GTGT (${GLOBAL_TAX_RATE * 100}%): +${totals.taxAmount.toLocaleString()} ${GLOBAL_CURRENCY}</p>
      <h3>Tổng thanh toán: ${totals.finalTotal.toLocaleString()} ${GLOBAL_CURRENCY}</h3>
    `;
  };

  if (btnAdd) {
    btnAdd.addEventListener("click", () => {
      const nameInput = document.getElementById("product-name").value;
      const priceInput = document.getElementById("product-price").value;
      const quantityInput = document.getElementById("product-qty").value;

      const result = userCart.addItem(nameInput, priceInput, quantityInput);
      if (result.success) {
        renderCartUI();
      } else {
        alert(result.message);
      }
    });
  }

  if (btnVoucher) {
    btnVoucher.addEventListener("click", () => {
      const codeInput = document.getElementById("voucher-code").value;
      const result = userCart.applyVoucher(codeInput);
      alert(result.message);
      if (result.success) {
        renderCartUI();
      }
    });
  }
});
```

## 5. Checklist đánh giá kết quả
- [ ] Thao tác khởi tạo và quản lý biến đúng phạm vi Global Scope và Local Scope, không tạo biến toàn cục ngoài ý muốn.
- [ ] Sử dụng Closure đóng gói thành công private state (danh sách mặt hàng và mã giảm giá), đảm bảo dữ liệu không bị ghi đè chéo giữa các instance giỏ hàng.
- [ ] Định nghĩa hàm và biến đúng thứ tự, không vi phạm lỗi Temporal Dead Zone (TDZ).
- [ ] Sử dụng thành thạo Cursor AI IDE để phát hiện lỗi phạm vi biến và tối ưu hóa mã nguồn ES6+.
- [ ] Kết nối thành công logic Closure với DOM API để hiển thị dữ liệu giỏ hàng và hóa đơn thanh toán lên giao diện HTML/CSS.