# ĐỀ CƯƠNG BÀI GIẢNG SLIDE (OUTLINE & SPEAKER NOTES)
**Khóa học:** Phát triển ứng dụng web  
**Chủ đề Session:** Session 14 - Tổ chức Hàm (Function), Tham số, Arrow Function và Phạm vi Scope  
**Ngữ cảnh Domain thống nhất:** Hệ thống Quản lý Lưu kho Kiện hàng Warehouse  
**Công nghệ:** JavaScript  
**Tổng số slide:** 14 slides  

---

## Slide 01: Tổ chức Hàm, Arrow Function & Scope [COVER]
*Phụ đề:* Quản lý mã nguồn sạch và đóng gói logic nghiệp vụ trong Hệ thống Quản lý Lưu kho Kiện hàng Warehouse


> 🎙️ **Speaker Notes (Lời giảng E-learning):**
> Chào mừng các bạn sinh viên đến với Session 14. Trong bài học hôm nay, chúng ta sẽ làm chủ cách đóng gói mã nguồn JavaScript thông qua Hàm (Function), cú pháp hiện đại Arrow Function ES6, các cơ chế xử lý tham số và đặc biệt là quản lý phạm vi truy cập biến Scope cùng cơ chế Closures thông qua bài toán thực tế của Hệ thống Quản lý Lưu kho Kiện hàng Warehouse.

---

## Slide 02: Nội Dung Bài Giảng [AGENDA]
**Nội dung Agenda:**
- 1. Khai báo Hàm (Declaration & Expression) & Cơ chế Hoisting
- 2. Arrow Function ES6, Tham số Mặc định & Rest Parameters
- 3. Phạm vi Biến Scope (Global, Function, Block Scope)
- 4. Cơ chế Closures & Đóng gói Dữ liệu Kho hàng
- 5. Tổng kết, Lỗi Kỹ thuật Thường gặp & Bài tập Thực hành

> 🎙️ **Speaker Notes (Lời giảng E-learning):**
> Lộ trình bài học của chúng ta được chia thành 5 phần rõ ràng. Đầu tiên là nền tảng khai báo hàm và hoisting. Tiếp theo là các tính năng modern ES6 như Arrow Function và Rest Parameters. Sau đó chúng ta đi sâu vào bản chất kiến trúc biến qua Scope, nâng cao với Closures, và cuối cùng là tổng kết các lỗi hay gặp khi đi làm.

---

## Slide 03: Mục Tiêu Bài Học [OBJECTIVES]
**Chuẩn đầu ra bài học:**
1. Phân biệt chính xác Function Declaration và Expression theo cơ chế Hoisting.
2. Vận dụng thành thạo cú pháp Arrow Function ES6 và Tham số mặc định.
3. Làm chủ quy tắc hoạt động của Global Scope, Block Scope và Scope Chain.
4. Ứng dụng Closures để tạo các hàm bảo mật trạng thái kiện hàng trong Warehouse.

> 🎙️ **Speaker Notes (Lời giảng E-learning):**
> Sau khi hoàn thành bài học này, các bạn cần đạt được 4 chuẩn đầu ra cốt lõi: phân biệt được cách khai báo hàm, sử dụng thành thạo Arrow Function ES6, kiểm soát chặt chẽ phạm vi biến để tránh rò rỉ bộ nhớ, và ứng dụng thành công Closures vào hệ thống lưu kho thực tế.

---

## Slide 04: 1. Khai báo Hàm — 1/2 [COMPARISON]
*Phụ đề:* Tái sử dụng công thức tính phí lưu kho thay vì viết lặp code thủ công

### [Trái] Cách viết lặp code thủ công
```javascript
// Kiện hàng PKG-01
let fee1 = 15 * 5000 + 3 * 2000;
// Kiện hàng PKG-02
let fee2 = 40 * 5000 + 7 * 2000;
// Kiện hàng PKG-03
let fee3 = 8 * 5000 + 1 * 2000;
```
- Tốn thời gian lặp lại công thức tính phí kho.
- Dễ sai sót khi thay đổi đơn giá lưu kho.
- Khó bảo trì khi số lượng kiện hàng lên tới hàng nghìn.

### [Phải] Đóng gói thành Hàm (Function)
```javascript
function calcStorageFee(weight, days) {
  const basePricePerKg = 5000;
  const dayFeePerDay = 2000;
  return weight * basePricePerKg + days * dayFeePerDay;
}
let fee1 = calcStorageFee(15, 3);
```
- Định nghĩa công thức 1 lần duy nhất.
- Gọi lại linh hoạt cho mọi kiện hàng.
- Dễ dàng cập nhật bảng giá lưu kho đồng bộ.

> 🎙️ **Speaker Notes (Lời giảng E-learning):**
> Hãy nhìn vào bức tranh so sánh này. Ở bên trái, khi tính phí lưu kho cho từng kiện hàng theo khối lượng và số ngày, việc nhân chia trực tiếp làm code bị lặp lại và cực kỳ nguy hiểm nếu bảng giá đổi. Bên phải, khi ta đóng gói vào hàm `calcStorageFee`, code gọn gàng, rõ nghĩa và dễ duy trì hơn rất nhiều.

---

## Slide 05: 1. Khai báo Hàm — 2/2 [CODE]
*Phụ đề:* Phân biệt Function Declaration và Function Expression qua cơ chế Hoisting

**Các ý chính:**
- Function Declaration được hoist toàn bộ lên đầu scope, cho phép gọi hàm trước dòng định nghĩa.
- Function Expression gán hàm vào biến (const/let), chỉ sử dụng được sau khi dòng code thực thi tới.
- Khuyên dùng: Dùng Expression để ngăn chặn gọi hàm lộn xộn, tăng tính dự đoán cho chương trình.

**Code (Hoisting trong Hàm Warehouse):**
```javascript
// 1. Function Declaration (Được Hoisting)
const feeA = calculateFee(25, 4); // OK! Gọi trước khai báo

function calculateFee(weight, days) {
  return weight * 5000 + days * 2000;
}

// 2. Function Expression (KHÔNG được Hoisting)
// getZone() -> Error: Cannot access before initialization
const getZone = function(packageId) {
  return packageId.startsWith('K-') ? 'Khu A' : 'Khu B';
};
const zone = getZone('K-102'); // Đúng: Gọi sau khai báo
```

> 🎙️ **Speaker Notes (Lời giảng E-learning):**
> Điểm khác biệt quan trọng nhất giữa Function Declaration và Function Expression chính là Hoisting. Với Function Declaration, JavaScript Engine nâng toàn bộ định nghĩa hàm lên đầu scope, cho nên các bạn gọi hàm trước dòng khai báo vẫn chạy bình thường. Ngược lại, Function Expression gán hàm vào biến const, giúp mã nguồn tuân thủ thứ tự đọc từ trên xuống dưới.

---

## Slide 06: 2. Arrow Function ES6 — 1/2 [CODE]
*Phụ đề:* Tối ưu cú pháp ngắn gọn và viết hàm xử lý kiện hàng trên 1 dòng

**Các ý chính:**
- Bỏ từ khóa `function`, dùng mũi tên `=>` giúp cú pháp cực kỳ súc tích.
- Nếu chỉ có 1 tham số: Có thể bỏ cặp ngoặc tròn `()`.
- Nếu thân hàm chỉ có 1 biểu thức: Có thể bỏ `{}` và từ khóa `return` (tự động trả về).
- Lưu ý: Arrow Function không có từ khóa `this` riêng.

**Code (Cú pháp Arrow Function trong Warehouse):**
```javascript
// Regular Function Expression
const checkOverweightOld = function(weight) {
  return weight > 30;
};

// Arrow Function đầy đủ
const checkOverweight = (weight) => {
  return weight > 30;
};

// Arrow Function rút gọn (Implicit Return)
const isExpressPackage = pkg => pkg.isPriority && pkg.weight < 10;

// Gọi hàm kiểm tra kiện hàng
console.log(checkOverweight(45)); // true
console.log(isExpressPackage({ isPriority: true, weight: 5 })); // true
```

> 🎙️ **Speaker Notes (Lời giảng E-learning):**
> Arrow Function ra đời từ ES6 mang đến cú pháp ngắn gọn tuyệt vời. Đối với các logic kiểm tra kiện hàng quá tải hay kiện hàng hỏa tốc ngắn gọn, chúng ta có thể viết trên một dòng duy nhất bằng cơ chế Implicit Return. Điều này giúp mã nguồn khi làm việc với array helper cực kỳ sạch đẹp.

---

## Slide 07: 2. Tham số Mặc định & Rest Parameters — 2/2 [COMPARISON]
*Phụ đề:* Xử lý tham số linh hoạt khi nhập danh sách kiện hàng vào kho

### [Trái] Tham số Mặc định (Default Params)
```javascript
// Gán giá trị mặc định cho storageDays và zone
const createPackage = (
  id,
  weight,
  days = 1,
  zone = 'Khu Chờ'
) => ({
  id,
  weight,
  fee: weight * 5000 + days * 2000,
  zone
});

const p1 = createPackage('PKG-99', 10);
// zone sẽ tự nhận 'Khu Chờ', days = 1
```
- Tránh lỗi `undefined` khi truyền thiếu arguments.
- Tự động áp dụng cấu hình lưu kho mặc định.
- Code rõ ràng, không cần kiểm tra `if (!days)`.

### [Phải] Gộp tham số (Rest Parameters)
```javascript
// Gom tất cả trọng lượng các kiện vào 1 mảng
const totalWeight = (...weights) => {
  return weights.reduce(
    (sum, w) => sum + w,
    0
  );
};

const total = totalWeight(12, 5, 30, 8);
// total = 55kg
```
- Dùng cú pháp `...` gom nhiều tham số thành mảng.
- Thay thế hoàn toàn đối tượng `arguments` cũ.
- Linh hoạt tiếp nhận số lượng kiện hàng bất kỳ.

> 🎙️ **Speaker Notes (Lời giảng E-learning):**
> Trong thực tế quản lý kho, khi tạo mới kiện hàng có những thông số cố định như số ngày lưu mặc định là 1 ngày, khu vực mặc định là Khu Chờ. Tham số mặc định giúp chúng ta xử lý việc này gọn gàng. Còn với Rest Parameters `...weights`, hàm có thể tiếp nhận 5, 10 hay 100 kiện hàng cùng lúc mà vẫn gom vào mảng xử lý mượt mà.

---

## Slide 08: So Sánh Các Cú Pháp Khai Báo Hàm [TABLE]
*Phụ đề:* Bảng tổng hợp đặc tính kỹ thuật quan trọng phục vụ chọn lựa thiết kế mã nguồn


> 🎙️ **Speaker Notes (Lời giảng E-learning):**
> Bảng so sánh này là kim chỉ nam quan trọng giúp các bạn lựa chọn đúng loại hàm. Hãy nhớ: Function Declaration có Hoisting, Arrow Function không có 'this' riêng và cực hợp cho các callback. Trong dự án Warehouse, chúng ta kết hợp linh hoạt cả 3 loại tùy theo mục đích.

---

## Slide 09: 3. Phạm vi Biến (Scope) — 1/2 [COMPARISON]
*Phụ đề:* Phân biệt Global Scope và Block Scope để tránh rò rỉ dữ liệu kho

### [Trái] Nguy cơ với Global Scope (var)
```javascript
var warehouseName = 'Kho Tổng Hanoi';

for (var i = 0; i < 3; i++) {
  var warehouseName = 'Kho Chi Nhánh ' + i;
}

console.log(warehouseName);
// 'Kho Chi Nhánh 2' (Bị ghi đè dữ liệu!)
```
- Biến khai báo bằng `var` bị rò rỉ ra ngoài khối lệnh `{}`.
- Dễ gây ra sự cố ghi đè biến nguy hiểm.
- Khó kiểm soát trạng thái dữ liệu ứng dụng.

### [Phải] An toàn với Block Scope (let/const)
```javascript
const warehouseName = 'Kho Tổng Hanoi';

for (let i = 0; i < 3; i++) {
  const currentArea = 'Khu ' + i;
  console.log(currentArea); // Hợp lệ
}

// console.log(currentArea); // Error: Not defined!
```
- Biến `let`/`const` chỉ tồn tại trong cặp ngoặc `{}`.
- Bảo vệ dữ liệu không bị biến ngoài can thiệp.
- Giúp bộ nhớ giải phóng biến ngay sau khi thoát block.

> 🎙️ **Speaker Notes (Lời giảng E-learning):**
> Phạm vi biến Scope quyết định nơi nào trong mã nguồn được phép truy cập vào biến. Nếu dùng `var`, biến có phạm vi Global hoặc Function Scope, dễ bị lỡ tay ghi đè dữ liệu như ví dụ bên trái. Với `let` và `const` giới hạn trong Block Scope `{}`, chúng ta giữ cho dữ liệu từng khu vực kho hoàn toàn cô lập và an toàn.

---

## Slide 10: 3. Cơ chế Closures — 2/2 [CODE]
*Phụ đề:* Đóng gói dữ liệu và tạo trình tự sinh mã kiện hàng tự động an toàn

**Các ý chính:**
- Hàm con `generateId` ghi nhớ phạm vi chứa nó ngay cả khi `createPackageTracker` đã thực thi xong.
- Biến `count` không thể bị truy cập trực tiếp hay sửa đổi từ bên ngoài (Private Data).
- Mỗi instance (`ZoneA`, `ZoneB`) sở hữu một bộ nhớ trạng thái độc lập hoàn toàn.

**Code (Bộ tạo mã kiện hàng tự tăng (Package ID Tracker)):**
```javascript
function createPackageTracker(prefix) {
  let count = 0; // Biến tư nhân (Private State)
  
  return function generateId() {
    count++; // Closure ghi nhớ và tăng biến count của hàm cha
    return `${prefix}-${String(count).padStart(4, '0')}`;
  };
}

const generateZoneAId = createPackageTracker('ZONE-A');
console.log(generateZoneAId()); // 'ZONE-A-0001'
console.log(generateZoneAId()); // 'ZONE-A-0002'

const generateZoneBId = createPackageTracker('ZONE-B');
console.log(generateZoneBId()); // 'ZONE-B-0001'
```

> 🎙️ **Speaker Notes (Lời giảng E-learning):**
> Closures là một trong những tính năng mạnh mẽ nhất của JavaScript. Khi hàm `createPackageTracker` chạy xong và trả về hàm con, biến `count` không bị hủy đi mà được hàm con 'đóng gói' mang theo. Bên ngoài không thể can thiệp sửa trực tiếp `count = 999`, đảm bảo mã kiện hàng tăng đúng trình tự.

---

## Slide 11: Bảng Trace Luồng Thực Thi Scope & Closures [TABLE]
*Phụ đề:* Từng bước phân tích trạng thái bộ nhớ khi gọi bộ tạo mã kiện hàng


> 🎙️ **Speaker Notes (Lời giảng E-learning):**
> Hãy cùng trace bảng bộ nhớ này. Mỗi khi gọi `createPackageTracker`, một không gian lưu trữ Scope hoàn toàn riêng biệt được tạo ra. Việc gọi `genA()` không làm ảnh hưởng tới biến `count` của `genB()`. Đây chính là nền tảng của lập trình hướng đối tượng và module pattern trong JavaScript.

---

## Slide 12: Thuật Ngữ Cần Nhớ [GRID4]
*Phụ đề:* 4 khái niệm cốt lõi bắt buộc nắm vững để làm chủ Hàm và Scope

### 1. Function Declaration
- **Định nghĩa:** Khai báo hàm truyền thống với từ khóa function, được hoisting hoàn toàn lên đầu phạm vi.
- **Ví dụ:** `function calcFee(w) { return w * 5000; }`
### 2. Arrow Function
- **Định nghĩa:** Cú pháp hàm mũi tên rút gọn ES6, không có binding riêng cho từ khóa this và arguments.
- **Ví dụ:** `const calcFee = w => w * 5000;`
### 3. Block Scope
- **Định nghĩa:** Phạm vi giới hạn bên trong cặp ngoặc nhọn {} khi khai báo bằng let hoặc const.
- **Ví dụ:** `{ const zone = 'A1'; }`
### 4. Closures
- **Định nghĩa:** Hàm con ghi nhớ và duy trì truy cập vào các biến thuộc phạm vi của hàm cha outer chứa nó.
- **Ví dụ:** `const tracker = createPackageTracker();`

> 🎙️ **Speaker Notes (Lời giảng E-learning):**
> Vui lòng ghi nhớ 4 thuật ngữ quan trọng nhất của Session 14 trên đây. Đây là các câu hỏi phỏng vấn tuyển dụng cực kỳ phổ biến đối với vị trí Lập trình viên JavaScript / Front-End Web.

---

## Slide 13: Tổng Kết & Cảnh Báo Lỗi Thường Gặp [CARDS]
*Phụ đề:* Những bài học xương máu giúp viết code chuẩn sạch trong dự án thực tế

### Lỗi 1: Tái rò rỉ biến Global
### Lỗi 2: Lầm tưởng Arrow Function có 'this'
### Lỗi 3: Gọi Function Expression trước khai báo
### Lỗi 4: Lạm dụng Closures gây tràn RAM

> 🎙️ **Speaker Notes (Lời giảng E-learning):**
> Chúng ta cùng điểm lại 4 sai lầm kỹ thuật phổ biến nhất. Nhớ luôn dùng const/let để giới hạn scope, không dùng Arrow Function làm method cho Object nếu cần truy cập `this`, và lưu ý gọi hàm expression đúng thứ tự.

---

## Slide 14: Chúc Các Bạn Học Tốt! [CLOSING]

> 🎙️ **Speaker Notes (Lời giảng E-learning):**
> Cảm ơn các bạn đã theo dõi trọn vẹn bài giảng Session 14. Các bạn hãy mở ngay hệ thống LMS để hoàn thành bài tập thực hành viết hàm xử lý xuất nhập kho. Hẹn gặp lại các bạn ở session tiếp theo!

---
