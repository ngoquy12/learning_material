# Bộ câu hỏi kiểm tra bài đọc (Reading Comprehension Questions)

## Tình huống & Mã nguồn kiểm tra
Dựa trên mã nguồn nghiệp vụ được trích dẫn từ bài đọc:

```javascript vanilla (es6+), html5
// Rikkei Store - Module tính tổng giá trị hóa đơn đơn hàng
const calculateInvoice = (
  basePrice,
  taxRate = 0.1,
  shippingFee = 30000
) => {
  // Kiểm tra tính hợp lệ của giá gốc sản phẩm
  if (typeof basePrice !== "number" || basePrice <= 0) {
    return "Đầu vào không hợp lệ";
  }

  // Tính tiền thuế và tổng số tiền thanh toán
  const tax = basePrice * taxRate;
  const total = basePrice + tax + shippingFee;
  return total;
};
```

---

### Câu 1 (Xung hướng - Tính toán kết quả với dữ liệu X1): Nếu hệ thống gọi hàm với câu lệnh calculateInvoice(200000, undefined, undefined), mã nguồn sẽ thực thi qua các bước nào và trả về kết quả cuối cùng là bao nhiêu?
> **Gợi ý trả lời & Định hướng đáp án:**
> - Bước 1: Khởi tạo tham số và kiểm tra điều kiện đầu vào. Biến basePrice nhận giá trị 200000. Biểu thức (typeof basePrice !== "number" || basePrice <= 0) trả về false vì typeof 200000 là "number" và 200000 > 0. Khối lệnh if bị bỏ qua.
> - Bước 2: Kích hoạt cơ chế Tham số Mặc định (Default Parameters). Vì hai đối số tiếp theo được truyền vào là undefined, trình dịch tự động gán giá trị mặc định: taxRate = 0.1 và shippingFee = 30000.
> - Bước 3: Tính số tiền thuế tax = 200000 * 0.1 = 20000.
> - Bước 4: Tính tổng số tiền total = 200000 + 20000 + 30000 = 250000.
> - Kết quả trả về: 250000.

---

### Câu 2 (Xung hướng - Thử nghiệm với mốc dữ liệu X2): Nếu người dùng thay đổi dữ liệu đầu vào thành lời gọi calculateInvoice(500000, 0.05, 15000), luồng điều kiện thực thi như thế nào và kết quả thu được là bao nhiêu?
> **Gợi ý trả lời & Định hướng đáp án:**
> - Bước 1: Giá trị basePrice = 500000 hợp lệ, biểu thức trong câu lệnh if trả về false, luồng thực thi chuyển xuống tính toán.
> - Bước 2: Vì đối số taxRate được truyền giá trị cụ thể là 0.05 (khác undefined), hệ thống KHÔNG sử dụng giá trị mặc định 0.1 mà nhận taxRate = 0.05.
> - Bước 3: Tương tự, đối số shippingFee nhận giá trị 15000 (khác undefined), hệ thống bỏ qua giá trị mặc định 30000 và nhận shippingFee = 15000.
> - Bước 4: Tính số tiền thuế tax = 500000 * 0.05 = 25000.
> - Bước 5: Tính tổng số tiền total = 500000 + 25000 + 15000 = 540000.
> - Kết quả trả về: 540000.

---

### Câu 3 (Nghịch hướng - Suy luận dữ liệu đầu vào từ kết quả Y3): Giả sử đơn hàng được áp dụng chính sách miễn phí vận chuyển bằng cách truyền shippingFee = 0 và không truyền đối số taxRate (để sử dụng mức thuế mặc định). Để hàm calculateInvoice trả về tổng tiền chính xác là 132000 VNĐ, giá gốc sản phẩm basePrice cần phải bằng bao nhiêu?
> **Gợi ý trả lời & Định hướng đáp án:**
> - Bước 1: Lời gọi hàm có dạng calculateInvoice(basePrice, undefined, 0).
> - Bước 2: Xác định giá trị các tham số khi thực thi: taxRate nhận giá trị mặc định 0.1; shippingFee nhận giá trị truyền vào là 0.
> - Bước 3: Thiết lập công thức toán học tính total theo basePrice:
>   total = basePrice + (basePrice * 0.1) + 0 = basePrice * 1.1.
> - Bước 4: Giải phương trình tìm basePrice với mục tiêu total = 132000:
>   basePrice * 1.1 = 132000 => basePrice = 132000 / 1.1 = 120000.
> - Kết luận: Giá gốc sản phẩm basePrice phải đúng bằng 120000 VNĐ.

---

### Câu 4 (Phân tích bẫy lỗi & Trường hợp biên): Phân tích sự cố logic xảy ra khi gọi hàm calculateInvoice(200000, null, 20000). Giá trị trả về là bao nhiêu, tại sao cơ chế Default Parameter không hoạt động như kỳ vọng và cách khắc phục là gì?
> **Gợi ý trả lời & Định hướng đáp án:**
> - Nguyên nhân bẫy lỗi: Trong Javascript ES6, cơ chế Tham số Mặc định CHỈ được kích hoạt khi đối số bị khuyết hoặc truyền giá trị chính xác là undefined. Khi truyền giá trị null, trình biên dịch ghi nhận null là một giá trị xác định được gán chủ động.
> - Trạng thái biến khi thực thi: basePrice = 200000, taxRate = null, shippingFee = 20000.
> - Hậu quả tính toán: Trong biểu thức toán học (basePrice * taxRate), Javascript tự động ép kiểu dữ liệu (implicit coercion) biến null thành số 0. Do đó tax = 200000 * 0 = 0.
> - Kết quả trả về: total = 200000 + 0 + 20000 = 220000 VNĐ (Sai logic nghiệp vụ vì đơn hàng bị mất 10% tiền thuế mặc định).
> - Cách khắc phục: Khi gọi hàm, nếu muốn sử dụng giá trị mặc định của tham số, bắt buộc phải truyền undefined thay vì null (ví dụ: calculateInvoice(200000, undefined, 20000)). Hoặc bổ sung kiểm tra kiểm soát giá trị null bên trong thân hàm: taxRate = (taxRate === null) ? 0.1 : taxRate.

---