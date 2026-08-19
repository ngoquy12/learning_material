# Bộ câu hỏi kiểm tra bài đọc (Reading Comprehension Questions)

## Tình huống & Mã nguồn kiểm tra
Dựa trên mã nguồn nghiệp vụ được trích dẫn từ bài đọc:

```javascript vanilla (es6+), html5
function createCartTracker(initialQty) {
    let itemCount = typeof initialQty === "number" && initialQty >= 0 ? initialQty : 0;

    return function processCart(action, value) {
        if (action === "ADD") {
            if (typeof value === "number" && value > 0) {
                itemCount += value;
                return `Đã thêm ${value}. Tổng: ${itemCount}`;
            }
            return "Số lượng thêm không hợp lệ";
        }
        if (action === "APPLY_COUPON") {
            if (value === "SALE50" && itemCount >= 5) {
                return `Áp dụng thành công cho ${itemCount} sản phẩm`;
            }
            return "Không đủ điều kiện nhận ưu đãi";
        }
        if (action === "REMOVE") {
            if (typeof value === "number" && value > 0 && value <= itemCount) {
                itemCount -= value;
                return `Đã giảm ${value}. Còn lại: ${itemCount}`;
            }
            return "Số lượng giảm không hợp lệ";
        }
        return "Hành động không hợp lệ";
    };
}
```

---

### Câu 1 (Xung hướng - Tính toán kết quả với dữ liệu X1): Nếu khởi tạo `const myCart = createCartTracker(3);` và lần lượt gọi `myCart("ADD", 4)` rồi `myCart("APPLY_COUPON", "SALE50")`, hãy chỉ ra các nhánh điều kiện được thực thi và giá trị chuỗi trả về ở từng bước.
> **Gợi ý trả lời & Định hướng đáp án:**
> - Bước 1: Khởi tạo `createCartTracker(3)` gán biến `itemCount = 3` nằm trong Lexical Scope của hàm `createCartTracker` và được ghi nhớ bởi Closure.
> - Bước 2: Gọi `myCart("ADD", 4)`:
>   + Mã nguồn khớp với nhánh `action === "ADD"`.
>   + Kiểm tra điều kiện `typeof 4 === "number" && 4 > 0` trả về `true`.
>   + Biến closure `itemCount` được cập nhật: `3 + 4 = 7`.
>   + Kết quả trả về: `"Đã thêm 4. Tổng: 7"`.
> - Bước 3: Gọi `myCart("APPLY_COUPON", "SALE50")`:
>   + Mã nguồn khớp với nhánh `action === "APPLY_COUPON"`.
>   + Kiểm tra điều kiện `value === "SALE50"` (true) và `itemCount >= 5` (7 >= 5 là true).
>   + Cả hai điều kiện đều thỏa mãn nên nhánh `if` chính được kích hoạt.
>   + Kết quả trả về: `"Áp dụng thành công cho 7 sản phẩm"`.

---

### Câu 2 (Xung hướng - Thử nghiệm với mốc dữ liệu X2): Nếu thay đổi dữ liệu khởi tạo thành `const myCart = createCartTracker(2);` sau đó gọi `myCart("ADD", 1)` và `myCart("APPLY_COUPON", "SALE50")`, luồng thực thi và kết quả trả về ở bước gọi coupon thay đổi như thế nào?
> **Gợi ý trả lời & Định hướng đáp án:**
> - Bước 1: Khởi tạo `createCartTracker(2)` gán `itemCount = 2`.
> - Bước 2: Gọi `myCart("ADD", 1)`:
>   + Đi vào nhánh `action === "ADD"`, kiểm tra `1 > 0` thỏa mãn.
>   + Cập nhật `itemCount = 2 + 1 = 3`.
>   + Kết quả trả về: `"Đã thêm 1. Tổng: 3"`.
> - Bước 3: Gọi `myCart("APPLY_COUPON", "SALE50")`:
>   + Đi vào nhánh `action === "APPLY_COUPON"`.
>   + Kiểm tra biểu thức điều kiện: `value === "SALE50"` trả về `true`, tuy nhiên `itemCount >= 5` (3 >= 5) trả về `false`.
>   + Do sử dụng toán tử logic `&&`, biểu thức tổng chuyển thành `false` và bỏ qua khối `if` nội bộ.
>   + Luồng thực thi chuyển xuống dòng trả về mặc định của nhánh coupon.
>   + Kết quả trả về: `"Không đủ điều kiện nhận ưu đãi"`.

---

### Câu 3 (Nghịch hướng - Suy luận dữ liệu đầu vào từ kết quả Z): Giả sử hệ thống khởi tạo `const myCart = createCartTracker(10);` và thực hiện `myCart("ADD", 5)`. Để câu lệnh tiếp theo `myCart("REMOVE", X)` trả về chính xác chuỗi kết quả "Đã giảm 13. Còn lại: 2", tham số X truyền vào phải có giá trị là bao nhiêu và thỏa mãn điều kiện logic nào?
> **Gợi ý trả lời & Định hướng đáp án:**
> - Trạng thái ban đầu: `createCartTracker(10)` khởi tạo `itemCount = 10`.
> - Sau lệnh `myCart("ADD", 5)`: `itemCount` tăng lên thành `10 + 5 = 15`.
> - Phân tích mẫu chuỗi kết quả mong muốn: `"Đã giảm ${value}. Còn lại: ${itemCount}"`.
>   + Vị trí `${value}` tương ứng với số `13`, suy ra `X = 13`.
>   + Vị trí `${itemCount}` sau khi trừ tương ứng với số `2` (phép tính `15 - 13 = 2` hoàn toàn chính xác).
> - Kiểm tra điều kiện ràng buộc của nhánh `REMOVE` với `X = 13` và `itemCount = 15`:
>   + `typeof 13 === "number"` -> `true`.
>   + `13 > 0` -> `true`.
>   + `13 <= 15` (`value <= itemCount`) -> `true`.
> - Kết luận: Tham số `X` cần truyền vào chính xác là số `13`.

---

### Câu 4 (Phân tích bẫy lỗi & Trường hợp biên): Nếu một lập trình viên vô tình thêm dòng lệnh `var itemCount = 0;` vào bên trong nhánh `APPLY_COUPON`, hiện tượng Hoisting và Scope Shadowing sẽ gây ra lỗi gì cho hàm `processCart`? Nêu nguyên nhân và giải pháp khắc phục.
> **Gợi ý trả lời & Định hướng đáp án:**
> - Phân tích lỗi (Bug & Gotcha):
>   + Trong JavaScript, từ khóa `var` có cơ chế Hoisting (nâng khai báo) lên đầu phạm vi hàm chứa nó là `processCart`.
>   + Việc khai báo `var itemCount` ở bất kỳ đâu trong `processCart` sẽ tạo ra một biến cục bộ trùng tên, che khuất hoàn toàn (Scope Shadowing) biến `itemCount` ở phạm vi Lexical Scope bên ngoài của `createCartTracker`.
>   + Khi hàm `processCart` bắt đầu chạy, biến `itemCount` cục bộ này được khởi tạo là `undefined` trước khi dòng `var itemCount = 0` được thực thi tới.
>   + Hệ quả: Khi gọi bất kỳ lệnh nào như `myCart("ADD", 4)`, phép toán `itemCount += value` sẽ thực hiện `undefined + 4` dẫn tới kết quả `NaN` (Not a Number), làm hỏng toàn bộ trạng thái dữ liệu giỏ hàng.
> - Giải pháp khắc phục:
>   + Xóa bỏ khai báo `var itemCount` trùng tên bên trong hàm con `processCart` để hàm giữ nguyên liên kết Closure tới biến cha.
>   + Nếu cần lưu trữ số lượng tạm thời cho coupon, phải đặt tên biến khác hoàn toàn (ví dụ: `let discountApplied = 0;`) để tránh xung đột phạm vi biến.

---