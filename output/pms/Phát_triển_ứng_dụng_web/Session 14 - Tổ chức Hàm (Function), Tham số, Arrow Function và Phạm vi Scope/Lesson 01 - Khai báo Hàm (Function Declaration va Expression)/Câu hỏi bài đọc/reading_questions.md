# Bộ câu hỏi kiểm tra bài đọc (Reading Comprehension Questions)

## Tình huống & Mã nguồn kiểm tra
Dựa trên mã nguồn nghiệp vụ được trích dẫn từ bài đọc:

```javascript vanilla (es6+), html5
function calculateInvoiceTotal(subtotalAmount, shippingFee = 30000, vatRate = 0.1) {
  if (typeof subtotalAmount !== 'number' || subtotalAmount <= 0) {
    return 'Số tiền không hợp lệ';
  }

  let vatAmount = subtotalAmount * vatRate;

  if (subtotalAmount >= 500000) {
    shippingFee = 0; // Miễn phí vận chuyển cho đơn hàng từ 500.000 VNĐ
  }

  let totalValue = subtotalAmount + vatAmount + shippingFee;
  return totalValue;
}
```

---

### Câu 1 (Xung hướng - Tính toán kết quả với dữ liệu X1): Khi thực thi câu lệnh calling `calculateInvoiceTotal(200000)`, hãy truy vết từng bước chạy của chương trình và xác định giá trị trả về cuối cùng của hàm.
> **Gợi ý trả lời & Định hướng đáp án:**
> - Bước 1: Giá trị đối số 200000 được gán cho tham số `subtotalAmount`. Hai tham số còn lại không được truyền nên lấy giá trị mặc định: `shippingFee = 30000` và `vatRate = 0.1`.
> - Bước 2: Kiểm tra điều kiện đầu `(typeof 200000 !== 'number' || 200000 <= 0)` -> Kết quả `false`, bỏ qua khối `if` đầu tiên.
> - Bước 3: Tính tiền thuế VAT: `vatAmount = 200000 * 0.1 = 20000`.
> - Bước 4: Kiểm tra điều kiện freeship `(200000 >= 500000)` -> Kết quả `false`, giữ nguyên `shippingFee = 30000`.
> - Bước 5: Tính tổng hóa đơn: `totalValue = 200000 + 20000 + 30000 = 250000`.
> - Bước 6: Lệnh `return` trả về giá trị số `250000` và kết thúc hàm.

---

### Câu 2 (Xung hướng - Thử nghiệm với mốc dữ liệu X2): Nếu gọi hàm với đầy đủ đối số là `calculateInvoiceTotal(600000, 40000, 0.08)`, luồng thực thi thay đổi thế nào và kết quả trả về là bao nhiêu?
> **Gợi ý trả lời & Định hướng đáp án:**
> - Bước 1: Khởi tạo các tham số với giá trị được truyền vào: `subtotalAmount = 600000`, `shippingFee = 40000` (ghi đè 30000 mặc định), `vatRate = 0.08` (ghi đè 0.1 mặc định).
> - Bước 2: Kiểm tra điều kiện hợp lệ -> `false`, chuyển xuống tính VAT.
> - Bước 3: Tính tiền thuế VAT: `vatAmount = 600000 * 0.08 = 48000`.
> - Bước 4: Kiểm tra điều kiện freeship `(600000 >= 500000)` -> Kết quả `true`, biến `shippingFee` bị cập nhật đè từ 40000 về `0`.
> - Bước 5: Tính tổng hóa đơn: `totalValue = 600000 + 48000 + 0 = 648000`.
> - Bước 6: Kết quả hàm trả về là số `648000`.

---

### Câu 3 (Nghịch hướng - Suy luận dữ liệu đầu vào từ kết quả Y3): Giả sử người dùng chỉ truyền vào 1 đối số `subtotalAmount` (sử dụng `shippingFee` và `vatRate` mặc định). Để hàm trả về tổng hóa đơn `totalValue` đúng bằng 140,000 VNĐ, giá trị `subtotalAmount` truyền vào phải là bao nhiêu?
> **Gợi ý trả lời & Định hướng đáp án:**
> - Giả định 1: `subtotalAmount < 500000` (chưa đạt mốc freeship), do đó `shippingFee = 30000` và `vatRate = 0.1`.
> - Công thức tổng tiền: `totalValue = subtotalAmount + (subtotalAmount * 0.1) + 30000 = 1.1 * subtotalAmount + 30000`.
> - Thiết lập phương trình: `1.1 * subtotalAmount + 30000 = 140000`.
> - Giải phương trình: `1.1 * subtotalAmount = 110000` => `subtotalAmount = 110000 / 1.1 = 100000`.
> - Kiểm tra lại điều kiện: `100000 < 500000` (thỏa mãn giả định không được freeship).
> - Kết luận: Giá trị đầu vào `subtotalAmount` cần truyền là `100000`.

---

### Câu 4 (Phân tích bẫy lỗi & Trường hợp biên): Phân tích kết quả thực thi khi truyền giá trị dạng chuỗi `calculateInvoiceTotal('200000')` hoặc số âm `calculateInvoiceTotal(-50000)`. Nếu bỏ qua dòng kiểm tra `typeof subtotalAmount !== 'number'`, sự cố bẫy kiểu dữ liệu (Type Coercion) nào sẽ xảy ra?
> **Gợi ý trả lời & Định hướng đáp án:**
> - Với đoạn mã hiện tại: Cả hai trường hợp `'200000'` (kiểu string) và `-50000` (số <= 0) đều kích hoạt điều kiện guard clause `(typeof subtotalAmount !== 'number' || subtotalAmount <= 0)`. Hàm dừng ngay lập tức và trả về chuỗi thông báo `'Số tiền không hợp lệ'`.
> - Nếu loại bỏ câu lệnh kiểm tra (bẫy bẫy lỗi): Khi truyền `'200000'`, toán tử `+` trong JavaScript sẽ thực hiện nối chuỗi thay vì cộng số (`'200000' + 20000 + 30000`), dẫn đến kết quả sai lệch nghiêm trọng là chuỗi `'2000002000030000'`.
> - Giải pháp khắc phục chuẩn hóa: Giữ nguyên guard clause kiểm tra kiểu dữ liệu chặt chẽ bằng `typeof` và kiểm tra giá trị số hợp lệ trước khi tính toán.

---