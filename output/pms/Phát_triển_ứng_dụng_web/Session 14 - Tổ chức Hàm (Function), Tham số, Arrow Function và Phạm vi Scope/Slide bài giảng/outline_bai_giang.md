# Outline Bài Giảng: Session 14 - Tổ chức Hàm (Function), Tham số, Arrow Function và Phạm vi Scope

**Tổng số slide:** 18

---

### Slide 1: [cover] Session 14 - Tổ chức Hàm (Function), Tham số, Arrow Function và Phạm vi Scope


> 🎙️ **Speaker Notes:** Chào mừng các học viên đến với Session 14. Hôm nay chúng ta sẽ tìm hiểu về cách tổ chức hàm, tham số, Arrow Function và cơ chế phạm vi biến trong JavaScript. [~1 phut]

---

### Slide 2: [agenda] 

- 1. Khai báo Hàm: Function Declaration & Function Expression
- 2. ES6 Arrow Function và Cơ chế Tham số Mặc định (Default Parameters)
- 3. Phạm vi Biến (Scope), Cơ chế Hoisting và Kỹ thuật Closure

> 🎙️ **Speaker Notes:** Nội dung bài học gồm 3 phần chính đi từ nền tảng định nghĩa hàm đến các cú pháp hiện đại ES6 và kỹ thuật quản lý bộ nhớ nâng cao như Closure. [~2 phut]

---

### Slide 3: [objectives] Mục tiêu bài học

- [Mục tiêu] Phân biệt cú pháp, cơ chế Hoisting và ngữ cảnh áp dụng giữa Function Declaration và Function Expression.
- [Mục tiêu] Sử dụng thành thạo cú pháp ES6 Arrow Function ngắn gọn kết hợp cơ chế Implicit Return và Tham số mặc định (Default Parameters).
- [Mục tiêu] Xác định đúng phạm vi biến (Global, Function, Block Scope) và tránh các lỗi liên quan đến Temporal Dead Zone (TDZ).
- [Mục tiêu] Giải thích nguyên lý Lexical Scoping và vận dụng Closure để đóng gói trạng thái dữ liệu riêng tư (Private State).

> 🎙️ **Speaker Notes:** Sau buổi học này, các bạn cần nắm vững cách định nghĩa hàm tối ưu, tránh rò rỉ biến toàn cục và biết cách đóng gói dữ liệu an toàn với Closure. [~2 phut]

---

### Slide 4: [comparison_2col] Khai báo Hàm — 1/3
*Function Declaration được Hoisting hoàn toàn còn Function Expression chỉ khả dụng sau phép gán.*

**Function Declaration**
- Cú pháp truyền thống với từ khóa function và tên hàm định danh.
- Được tự động đưa lên đầu phạm vi (Hoisting), cho phép gọi trước khi khai báo.
- Thích hợp cho các hàm dùng chung toàn hệ thống.
```
function calculateSubtotal(price, quantity) {
  return price * quantity;
}
```
**Function Expression**
- Định nghĩa hàm ẩn danh và gán trực tiếp vào một biến.
- Không được hoisted; gọi trước dòng phép gán sẽ ném lỗi ReferenceError.
- Phù hợp để hạn chế ô nhiễm phạm vi và định nghĩa hàm nội bộ.
```
const calculateDiscount = function(subtotal, discountRate) {
  return subtotal * discountRate;
};
```

> 🎙️ **Speaker Notes:** So sánh hai cách khai báo hàm cơ bản. Lưu ý tính chất Hoisting khác nhau giữa Function Declaration và Function Expression để tránh lỗi sập chương trình. [~4 phut]

---

### Slide 5: [code_trace_table] Khai báo Hàm — 2/3
*Luồng thực thi hàm tạo vùng nhớ riêng biệt và trả về kết quả thông qua câu lệnh return.*

**Code Demo:** Luồng thực thi calculateSubtotal
```JS
const totalAmount = calculateSubtotal(50000, 3);
console.log("Tổng tiền hàng:", totalAmount);

function calculateSubtotal(price, quantity) {
  return price * quantity;
}
```
| Bước | Dòng mã thực thi | Biến / Tham số | Giá trị (RAM) | Ghi chú cơ chế |
|---|---|---|---|---|
| 1 | function calculateSubtotal(...) | calculateSubtotal | Function Object | Trình biên dịch hoist hàm calculateSubtotal lên đầu phạm vi |
| 2 | const total = calculateSubtotal(25000, 4); | price, quantity | price = 25000, quantity = 4 | Khởi tạo không gian thực thi hàm, gán đối số 25000 và 4 |
| 3 | const subtotal = price * quantity; | subtotal | 100000 | Thực hiện phép tính 25000 * 4 và lưu vào biến local subtotal |
| 4 | return subtotal; | kết quả trả về | 100000 | Trả về 100000 cho nơi gọi hàm và giải phóng bộ nhớ hàm |
| 5 | console.log(total); | total | 100000 | Biến total nhận giá trị 100000 và in ra terminal console |

> 🎙️ **Speaker Notes:** Bảng từng bước theo dõi bộ nhớ khi thực thi một hàm. Chú ý bước 1 khi trình biên dịch hoist hàm lên trước khi dòng lệnh đầu tiên chạy. [~5 phut]

---

### Slide 6: [code_right_card] Khai báo Hàm — 3/3
*Quên câu lệnh return hoặc gọi sai thời điểm Function Expression sẽ dẫn tới lỗi nghiêm trọng.*

**Code Demo:** Bẫy lập trình trong khai báo hàm
```JS
// 1. Lỗi gọi trước khi khai báo Expression
const discount = calculateDiscount(100000, 0.1);
// ReferenceError: Cannot access 'calculateDiscount' before initialization

const calculateDiscount = function(subtotal, rate) {
  return subtotal * rate;
};

// 2. Lỗi thiếu từ khóa return trong thân hàm
function calculateTax(subtotal) {
  const tax = subtotal * 0.1;
  // Quên từ khóa return tax!
}
console.log(calculateTax(100000)); // Kết quả: undefined
```
**Các điểm cẩn trọng chính**
- Gây lỗi ReferenceError khi cố gắng gọi Function Expression nằm trong Temporal Dead Zone.
- Thân hàm không có từ khóa return mặc định sẽ trả về undefined cho nơi gọi.
- Phân biệt rõ: Parameters là biến giữ chỗ khi định nghĩa, Arguments là giá trị thực tế truyền vào.

> 🎙️ **Speaker Notes:** Nhấn mạnh hai lỗi phổ biến: gọi Function Expression trước khi khởi tạo và quên trả về dữ liệu bằng câu lệnh return. [~4 phut]

---

### Slide 7: [interactive] Hoạt động: Dự đoán kết quả

**Kiểu:** predict_outcome
**Câu hỏi:** Đoạn mã JavaScript sau đây sẽ cho kết quả thực thi như thế nào trên Console?
```JS
console.log(getMessage("Rikkei"));

function getMessage(name) {
  return "Xin chào " + name;
}

console.log(getRole());

var getRole = function() {
  return "Admin";
};
```
- A. In ra "Xin chào Rikkei" sau đó ném lỗi TypeError: getRole is not a function
- B. In ra "Xin chào Rikkei" và "Admin"
- C. Ném lỗi ReferenceError ngay tại dòng 1
- D. In ra undefined cho cả hai dòng console.log
> 🔑 **Đáp án (giảng viên):** Đáp án đúng là A. getMessage là Function Declaration nên được hoisted hoàn toàn và chạy bình thường. Biến getRole khai báo bằng var chỉ được hoisted tên biến với giá trị undefined, nên khi gọi getRole() như một hàm sẽ báo lỗi TypeError: getRole is not a function.

> 🎙️ **Speaker Notes:** Yêu cầu học viên phân tích cơ chế Hoisting khác biệt giữa Function Declaration và biến var chứa Function Expression. [~3 phut]

---

### Slide 8: [comparison_2col] Arrow Function ES6 — 1/3
*Arrow Function giúp cô đọng cú pháp và hỗ trợ ngầm định trả về kết quả đối với thân hàm đơn dòng.*

**Thân hàm 1 dòng (Implicit Return)**
- Loại bỏ cặp ngoặc nhọn {} và từ khóa return đối với các biểu thức 1 dòng.
- Giá trị của biểu thức tự động được trả về cho nơi gọi hàm.
- Tối ưu độ ngắn gọn cho các hàm tính toán biến đổi dữ liệu đơn giản.
```
// Concise Body: Bỏ {} và return
const calculateSubtotal = (price, quantity) => price * quantity;

console.log(calculateSubtotal(50000, 3));
// Kết quả: 150000
```
**Thân hàm nhiều dòng (Block Body)**
- Bắt buộc dùng cặp ngoặc nhọn {} khi thân hàm có từ 2 câu lệnh trở lên.
- Bắt buộc viết từ khóa return rõ ràng để trả về kết quả.
- Nếu dùng cặp ngoặc {} mà quên từ khóa return, hàm sẽ trả về undefined.
```
// Block Body: Bắt buộc {} và return
const calculateSubtotal = (price, quantity) => {
  const netTotal = price * quantity;
  return netTotal;
};
```

> 🎙️ **Speaker Notes:** Phân biệt cú pháp Concise Body (Implicit Return) và Block Body (Explicit Return) của Arrow Function. [~4 phut]

---

### Slide 9: [code_right_card] Arrow Function ES6 — 2/3
*Tham số mặc định thiết lập giá trị phòng thủ khi đối số bị thiếu hoặc mang giá trị undefined.*

**Code Demo:** Default Parameters trong tính phí lưu kho
```JS
const calculateStorageFee = (subtotal, shippingFee = 30000, discount = 0) => {
  const netTotal = subtotal + shippingFee - discount;
  return netTotal;
};

// 1. Thiếu đối số -> Tự nhận 30000 và 0
console.log(calculateStorageFee(150000)); 
// Kết quả: 180000

// 2. Truyền đầy đủ đối số -> Ghi đè giá trị mặc định
console.log(calculateStorageFee(150000, 15000, 20000)); 
// Kết quả: 145000
```
**Quy tắc Default Parameters**
- Giá trị mặc định chỉ kích hoạt khi đối số bị thiếu hoặc có giá trị chính xác là undefined.
- Các giá trị falsy như 0, chuỗi rỗng "", false hoặc null vẫn sẽ ghi đè giá trị mặc định.
- Thứ tự tham số chuẩn: Đặt tất cả tham số bắt buộc ở đầu và tham số tùy chọn ở cuối danh sách.

> 🎙️ **Speaker Notes:** Giải thích cách Default Parameters phòng vệ cho ứng dụng tránh nhận kết quả NaN khi tính toán hóa đơn. [~4 phut]

---

### Slide 10: [flowchart] Arrow Function ES6 — 3/3
*Quy trình giải quyết đối số truyền vào tham số có thiết lập giá trị mặc định.*

- [start] Gọi hàm với danh sách đối số truyền vào
- [decision] Đối số === undefined hoặc bị thiếu?
- [process] Gán giá trị mặc định (Default Parameter)
- [process] Sử dụng giá trị đối số thực tế được truyền
- [process] Thực thi tính toán logic trong thân hàm
- [end] Trả về kết quả (Implicit hoặc Explicit Return)

> 🎙️ **Speaker Notes:** Sơ đồ tiến trình kiểm tra đối số trong JavaScript engine khi gặp cấu hình tham số mặc định. [~4 phut]

---

### Slide 11: [interactive] Hoạt động: Kiểm tra nhanh

**Kiểu:** quick_quiz
**Câu hỏi:** Cho hàm `calculateFee(amount, discount = 10, tax = 0)` và lời gọi `calculateFee(100, 0, undefined)`. Giá trị nhận được của discount và tax lần lượt là bao nhiêu?
```JS
const calculateFee = (amount, discount = 10, tax = 0) => {
  return amount - discount + tax;
};

console.log(calculateFee(100, 0, undefined));
```
- A. discount nhận 0, tax nhận 0 (kết quả trả về: 100)
- B. discount nhận 10, tax nhận 0 (kết quả trả về: 90)
- C. discount nhận 0, tax nhận undefined (kết quả trả về: NaN)
- D. discount nhận 10, tax nhận undefined (kết quả trả về: NaN)
> 🔑 **Đáp án (giảng viên):** Đáp án đúng là A. discount nhận 0 vì 0 là giá trị hợp lệ ghi đè 10. tax nhận 0 vì giá trị undefined truyền vào kích hoạt giá trị mặc định 0. Phép tính: 100 - 0 + 0 = 100.

> 🎙️ **Speaker Notes:** Nhấn mạnh bẫy phân biệt giữa 0 (falsy nhưng vẫn ghi đè) và undefined (kích hoạt default parameter). [~3 phut]

---

### Slide 12: [grid2x2] Scope & Closure — 1/2
*Phạm vi biến (Scope) xác định ranh giới truy cập dữ liệu và ngăn chặn hiện tượng rò rỉ biến.*

- **Global Scope:** Biến khai báo ngoài cùng, truy cập được từ mọi nơi. Dễ gây ô nhiễm phạm vi (Global Scope Pollution) nếu không kiểm soát.
- **Function Scope:** Biến khai báo bên trong hàm chỉ tồn tại và được truy cập nội bộ trong thân hàm đó.
- **Block Scope:** Biến let/const khai báo trong cặp ngoặc {} (if, for) chỉ hoạt động bên trong khối đó.
- **Temporal Dead Zone (TDZ):** Vùng chết thời gian ngăn chặn việc truy cập các biến let/const trước dòng khai báo chính thức.

> 🎙️ **Speaker Notes:** Tổng quan 4 khái niệm cốt lõi về phạm vi Scope trong JavaScript: Global, Function, Block và hiện tượng TDZ của let/const. [~5 phut]

---

### Slide 13: [code_right_card] Scope & Closure — 2/2
*Closure cho phép hàm con duy trì quyền truy cập biến của hàm ngoài để đóng gói trạng thái (Private State).*

**Code Demo:** Bảo vệ bộ đếm Pallet nhập kho bằng Closure
```JS
function createPalletTracker() {
  // Biến nội bộ được đóng gói an toàn (Private State)
  let itemCounter = 0;
  
  return function() {
    itemCounter += 1;
    return itemCounter;
  };
}

// Tạo vùng không gian Closure độc lập
const addPallet = createPalletTracker();
console.log(addPallet()); // Kết quả: 1
console.log(addPallet()); // Kết quả: 2
console.log(addPallet()); // Kết quả: 3
```
**Ứng dụng Kỹ thuật Closure**
- Hàm con ghi nhớ môi trường Lexical Scope nơi nó được sinh ra.
- Bảo mật dữ liệu nội bộ `itemCounter`, ngăn chặn mã bên ngoài chỉnh sửa trực tiếp.
- Mỗi lần gọi `createPalletTracker()` tạo ra một vùng lưu trữ độc lập hoàn toàn.

> 🎙️ **Speaker Notes:** Phân tích cơ chế Closure ghi nhớ biến nội bộ của hàm ngoài ngay cả khi hàm ngoài đã kết thúc thực thi. [~5 phut]

---

### Slide 14: [interactive] Hoạt động: Thử thách Closure

**Kiểu:** predict_outcome
**Câu hỏi:** Xét đoạn mã bên dưới, khi thực thi dòng lệnh cuối cùng `console.log(counterB())`, kết quả thu được là bao nhiêu?
```JS
function createPalletTracker() {
  let itemCounter = 0;
  return function() {
    itemCounter += 1;
    return itemCounter;
  };
}

const counterA = createPalletTracker();
const counterB = createPalletTracker();

counterA();
counterA();
console.log(counterB());
```
- A. In ra 1 — counterA và counterB có không gian Closure độc lập
- B. In ra 3 — counterA và counterB dùng chung biến itemCounter
- C. In ra undefined
- D. Ném lỗi ReferenceError
> 🔑 **Đáp án (giảng viên):** Đáp án đúng là A. Mỗi lần hàm createPalletTracker() được gọi, một phạm vi thực thi và không gian Closure hoàn toàn mới được tạo ra. Do đó counterA và counterB quản lý 2 bộ đếm độc lập.

> 🎙️ **Speaker Notes:** Làm rõ hiểu lầm phổ biến của học viên về việc các instance của Closure dùng chung bộ nhớ. [~3 phut]

---

### Slide 15: [glossary_table] Thuật ngữ cần nhớ
*Bảng tổng hợp các thuật ngữ kỹ thuật cốt lõi trong bài học.*

| Thuật ngữ | Tiếng Anh | Định nghĩa |
|---|---|---|
| Khai báo hàm định danh | Function Declaration | Cú pháp khai báo hàm truyền thống với từ khóa function và tên định danh, có hỗ trợ cơ chế Hoisting hoàn toàn. |
| Khai báo hàm dạng biểu thức | Function Expression | Kỹ thuật định nghĩa hàm và gán vào một biến, chỉ được thực thi khi luồng chương trình chạy tới đúng câu lệnh gán. |
| Cơ chế đưa lên đầu | Hoisting | Cơ chế của trình biên dịch JavaScript tự động di chuyển phần khai báo hàm và biến lên đầu phạm vi chứa nó trước khi mã chạy. |
| Hàm mũi tên | Arrow Function | Cú pháp khai báo hàm cô đọng ra đời trong ES6 sử dụng ký hiệu =>. |
| Trả về ngầm định | Implicit Return | Tính năng của Arrow Function 1 dòng cho phép tự động trả về kết quả biểu thức mà không cần cặp ngoặc {} và từ khóa return. |
| Tham số mặc định | Default Parameter | Giá trị an toàn được gán sẵn cho tham số khi đối số truyền vào bị thiếu hoặc mang giá trị undefined. |
| Phạm vi biến | Scope | Vùng mã nguồn mà trong đó một biến có thể được truy cập và sử dụng (Global, Function, Block Scope). |
| Vùng chết thời gian | Temporal Dead Zone (TDZ) | Khoảng thời gian từ khi phạm vi được khởi tạo đến khi dòng khai báo biến let/const được chạy, truy cập biến trong vùng này sẽ gây lỗi. |
| Bao đóng | Closure | Tính năng cho phép hàm con truy cập và ghi nhớ các biến thuộc phạm vi hàm bao ngoài ngay cả khi hàm ngoài đã thực thi xong. |

> 🎙️ **Speaker Notes:** Điểm lại danh sách thuật ngữ kỹ thuật cốt lõi. Học viên tra cứu bảng này khi làm bài tập thực hành. [~2 phut]

---

### Slide 16: [exercises] Bài tập & Tài liệu tham khảo
*Vận dụng kiến thức về Arrow Function và Closure vào giải quyết bài toán thực tế.*

**Bài tập thực hành:**
- Viết hàm Arrow Function calculateStorageCost nhận tham số days (số ngày) và rate (đơn giá/ngày, mặc định 50000 VNĐ) để tính tổng tiền lưu kho.
- Xây dựng hàm Closure createWarehouseShelf quản lý số lượng kiện hàng trên kệ, hỗ trợ tăng số lượng kiện và trả về tổng số kiện hiện tại mà không làm rò rỉ biến đếm ra ngoài.
**Tài liệu tham khảo:**
- MDN Web Docs — Functions & Scope: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Functions
- JavaScript.info — Closure & Lexical Environment: https://javascript.info/closure
- ES6 Specification — Arrow Functions & Default Parameters: https://es6-features.org

> 🎙️ **Speaker Notes:** Giao bài tập vận dụng về nhà cho học viên. Khuyến khích đọc tài liệu tham khảo MDN và JavaScript.info để hiểu sâu về Lexical Scope. [~2 phut]

---

### Slide 17: [summary_2col] Tổng kết
*4 nguyên tắc cốt lõi cần ghi nhớ khi tổ chức hàm và quản lý phạm vi biến trong JavaScript.*

**Khai báo & Cú pháp Hàm**
- Dùng Function Declaration cho các hàm dùng chung toàn hệ thống cần Hoisting; dùng Function Expression hoặc Arrow Function cho hàm nội bộ.
- Ưu tiên sử dụng Arrow Function ngắn gọn (Implicit Return) cho các phép tính toán biến đổi dữ liệu đơn dòng.
**Tham số & Quản lý Phạm vi Biến**
- Luôn đặt các tham số bắt buộc ở đầu danh sách tham số và tham số mặc định ở cuối danh sách.
- Hạn chế khai báo biến toàn cục (Global Scope); tận dụng Block Scope (let/const) và Closure để bảo vệ trạng thái riêng tư.

> 🎙️ **Speaker Notes:** Tóm tắt các quy tắc viết code sạch và bảo mật dữ liệu. Học viên cần áp dụng chuẩn mực này vào dự án thực tế. [~2 phut]

---

### Slide 18: [closing] Cảm ơn các bạn!
*Bài học tiếp theo: Session 15 - Xử lý Mảng (Array) và các Phương thức Biến đổi Dữ liệu ES6*


> 🎙️ **Speaker Notes:** Cảm ơn các bạn đã lắng nghe và tham gia tích cực. Hẹn gặp lại cả lớp trong Session 15! [~1 phut]

---
