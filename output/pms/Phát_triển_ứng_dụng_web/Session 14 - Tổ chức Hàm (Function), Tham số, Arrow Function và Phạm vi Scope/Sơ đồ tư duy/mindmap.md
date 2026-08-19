# Tổ chức Hàm, Tham số, Arrow Function và Phạm vi Scope

## Lesson 01 — Khai báo Hàm (Function Declaration & Expression)
### Khái niệm & Vai trò
- Định nghĩa ngắn gọn: Khối lệnh có tên để thực thi tác vụ và tái sử dụng.
- Vai trò: Tránh trùng lặp mã nguồn và đóng gói logic tính toán nghiệp vụ.
### Cú pháp & Giải nghĩa
- Khai báo cú pháp chuẩn:
  ```javascript
  // Function Declaration (Có hỗ trợ Hoisting)
  function calculateInvoiceTotal(subtotalAmount, shippingFee) {
    return subtotalAmount + shippingFee;
  }

  // Function Expression (Không hỗ trợ Hoisting)
  const calculateDiscountAmount = function(totalPrice, discountPercent) {
    return (totalPrice * discountPercent) / 100;
  };
  ```
- Giải thích thành phần:
  - calculateInvoiceTotal: Tên hàm theo quy tắc camelCase thể hiện hành động.
  - subtotalAmount: Tham số đầu vào nhận dữ liệu khi hàm được gọi.
  - return: Trả kết quả về nơi gọi và chấm dứt thực thi hàm.
### Ví dụ thực hành
- Kịch bản áp dụng: Tính tổng chi trả hóa đơn gồm tiền hàng và phí vận chuyển.
  ```javascript
  function calculateInvoiceTotal(subtotalAmount, shippingFee) {
    const vatTaxRate = 0.1;
    const vatAmount = subtotalAmount * vatTaxRate;
    return subtotalAmount + vatAmount + shippingFee;
  }

  const cartSubtotal = 1000000;
  const cartShipping = 30000;
  const finalPayment = calculateInvoiceTotal(cartSubtotal, cartShipping);
  console.log(finalPayment); // Output: 1130000
  ```
- Giải thích ví dụ: Hàm nhận tiền hàng và phí ship, tự động tính VAT rồi trả kết quả.
- 
### Lưu ý triển khai
- **Khác biệt Hoisting**: Function Declaration được đẩy lên đầu scope, Function Expression thì không.
- **Lưu ý định dạng**: Đặt tên hàm bằng động từ tiếng Anh theo chuẩn camelCase.

## Lesson 02 — Cú pháp Arrow Function ES6 và Tham số Mặc định
### Khái niệm & Vai trò
- Định nghĩa ngắn gọn: Cú pháp viết hàm thu gọn ES6 và thiết lập tham số dự phòng.
- Vai trò: Tối ưu cú pháp ngắn gọn và ngăn ngừa lỗi khi thiếu đối số.
### Cú pháp & Giải nghĩa
- Khai báo cú pháp chuẩn:
  ```javascript
  // Arrow Function kết hợp Tham số mặc định
  const calculateOrderTotal = (basePrice, taxRate = 0.08, shippingFee = 30000) => {
    return basePrice + (basePrice * taxRate) + shippingFee;
  };

  // Cú pháp thu gọn với implicit return
  const applyDiscount = (totalAmount, discountRate = 0.05) => totalAmount * (1 - discountRate);
  ```
- Giải thích thành phần:
  - =>: Mũi tên béo định nghĩa Arrow Function thay cho từ khóa function.
  - taxRate = 0.08: Tham số mặc định tự động dùng khi đối số bị khuyết.
  - () => expression: Implicit return tự động trả kết quả biểu thức không cần return.
### Ví dụ thực hành
- Kịch bản áp dụng: Tính tổng tiền đơn hàng với thuế và phí giao hàng mặc định.
  ```javascript
  const calculateOrderTotal = (basePrice, taxRate = 0.08, shippingFee = 30000) => {
    const taxAmount = basePrice * taxRate;
    return basePrice + taxAmount + shippingFee;
  };

  const totalOrder1 = calculateOrderTotal(500000, 0.1, 15000);
  const totalOrder2 = calculateOrderTotal(500000);
  console.log(totalOrder1, totalOrder2); // Output: 565000 570000
  ```
- Giải thích ví dụ: Đơn thứ hai khuyết thuế và phí ship nên tự động lấy giá trị mặc định.
### Lưu ý triển khai
- **Trả về Object trong Implicit Return**: Bắt buộc bọc ngoặc tròn xung quanh Object Literal `({ id, name })`.
- **Lưu ý định dạng**: Khai báo các tham số mặc định ở cuối danh sách tham số.

## Lesson 03 — Phạm vi Biến Global, Local Scope và Closures cơ bản
### Khái niệm & Vai trò
- Định nghĩa ngắn gọn: Quy tắc truy cập biến theo phạm vi và khả năng ghi nhớ scope cha.
- Vai trò: Bảo mật dữ liệu, đóng gói biến riêng tư và tránh ô nhiễm toàn cục.
### Cú pháp & Giải nghĩa
- Khai báo cú pháp chuẩn:
  ```javascript
  const createCounter = (initialValue = 0) => {
    let count = initialValue; // Biến cục bộ trong Lexical Scope
    return {
      increment: () => ++count, // Closure duy trì quyền truy cập count
      getValue: () => count
    };
  };
  ```
- Giải thích thành phần:
  - Global Scope: Phạm vi toàn cục, mọi nơi trong script đều truy cập được.
  - Local Scope: Phạm vi cục bộ bên trong hàm hoặc khối ngoặc nhọn.
  - Closure: Hàm con nhớ và truy cập được biến của hàm cha khi cha hoàn tất.
### Ví dụ thực hành
- Kịch bản áp dụng: Tạo quản lý giỏ hàng đóng gói danh sách sản phẩm bằng Closure.
  ```javascript
  const createCartManager = (defaultItems = []) => {
    const items = [...defaultItems];
    return {
      addItem: (product) => {
        items.push(product);
        return `Đã thêm: ${product}`;
      },
      getTotal: () => items.length
    };
  };

  const myCart = createCartManager(['Áo sơ mi']);
  console.log(myCart.addItem('Quần jeans')); // Output: Đã thêm: Quần jeans
  console.log(myCart.getTotal()); // Output: 2
  ```
- Giải thích ví dụ: Mảng items được bảo mật trong Closure, không thể sửa từ bên ngoài.
### Lưu ý triển khai
- **Ô nhiễm phạm vi toàn cục**: Không tạo biến thiếu từ khóa khai báo làm lây lan Global.
- **Lưu ý định dạng**: Dùng const cho phương thức Closure và let cho biến trạng thái nội bộ.

## Liên kết hệ thống
- Mối quan hệ logic: Lesson 01 tạo nền tảng định nghĩa hàm, Lesson 02 tối ưu cú pháp bằng Arrow Function và tham số mặc định, Lesson 03 mở rộng phạm vi biến và đóng gói trạng thái bằng Closure.
- Luồng dữ liệu xuyên suốt: Tham số đầu vào (Lesson 01/02) -> Xử lý trong Local Scope -> Trả kết quả trực tiếp hoặc lưu giữ trạng thái trong Closure (Lesson 03).
- Ứng dụng tổng hợp: Kết hợp Arrow Function, Tham số mặc định và Closure để xây dựng các mô-đun quản lý dữ liệu (Giỏ hàng, Bộ đếm) an toàn và tối ưu bộ nhớ.