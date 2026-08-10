# Bộ câu hỏi tự luận kiểm tra bài đọc (Reading Comprehension Essay Questions)

### Câu 1: Dựa trên bài đọc về hệ thống xử lý hóa đơn bán hàng trực tuyến, hãy phân tích từng bước cập nhật giá trị của biến total với các dữ liệu đầu vào cụ thể: unit_price = 250000, quantity = 4, discount_amount = 50000, và vat_rate = 0.1.
1. Hãy tính toán chi tiết giá trị của subtotal và giá trị biến total lần lượt qua từng dòng lệnh: total = subtotal, total -= discount_amount, và total += total * vat_rate.
2. Giải thích tại sao việc áp dụng toán tử gán phím tắt += ở bước tính thuế VAT lại căn cứ trên tổng tiền đã khấu trừ chiết khấu thay vì giá trị tiền hàng gốc subtotal?
> **Gợi ý trả lời & Định hướng đáp án:** Gợi ý trả lời:
1. Tiến trình tính toán từng dòng lệnh:
- subtotal = unit_price * quantity = 250000 * 4 = 1000000.
- Dòng 1: total = subtotal => total nhận giá trị 1000000.
- Dòng 2: total -= discount_amount tương đương total = 1000000 - 50000 = 950000.
- Dòng 3: total += total * vat_rate tương đương total = 950000 + (950000 * 0.1) = 950000 + 95000.0 = 1045000.0.
2. Cơ chế của toán tử gán phím tắt +=: Biểu thức vế phải (total * vat_rate) được lấy giá trị tại thời điểm thực thi, lúc này total đã là 950000 (sau khi trừ discount_amount). Điều này giúp doanh nghiệp tính chính xác thuế VAT 10% trên số tiền thực thu của khách hàng (950,000 VNĐ), tránh tính dư thuế trên tiền hàng gốc trước giảm giá.

---

### Câu 2: Trong phần đóng gói vận chuyển ở bài đọc, mã nguồn sử dụng hai toán tử số học chia nguyên (//) và chia dư (%) với các biến total_items = 14 và box_capacity = 4.
1. Hãy cho biết giá trị kết quả và ý nghĩa nghiệp vụ của hai biến full_boxes và remaining_items thu được.
2. Nếu một lập trình viên thay đổi câu lệnh thành full_boxes = total_items / box_capacity (dùng toán tử chia thực /), kết quả nhận được sẽ mang giá trị bao nhiêu và thuộc kiểu dữ liệu nào? Phân tích sai sót vận hành khi đưa kết quả này vào quy trình đóng thùng hàng.
> **Gợi ý trả lời & Định hướng đáp án:** Gợi ý trả lời:
1. Kết quả thực thi:
- full_boxes = 14 // 4 = 3. Ý nghĩa: Đóng vừa đủ 3 thùng hàng đầy.
- remaining_items = 14 % 4 = 2. Ý nghĩa: Còn dư 2 sản phẩm lẻ không đủ đóng thành 1 thùng đầy.
2. Trường hợp dùng toán tử chia thực /:
- full_boxes = 14 / 4 = 3.5 với kiểu dữ liệu số thực (float).
- Phân tích sai sót: Trong thực tế đóng gói kho vận, số thùng hàng bắt buộc phải là số nguyên (kiểu int). Việc trả về giá trị float 3.5 sẽ gây lỗi logic hoặc lỗi kiểu dữ liệu khi truyền vào các mô-đun xử lý tiếp theo (như in nhãn thùng hàng, phân công công nhân), vì không thể xuất ra 0.5 thùng hàng vật lý.

---

### Câu 3: Dựa vào bảng tra cứu toán tử và đoạn mã nguồn thực thi tính hóa đơn chi tiết trong bài đọc:
1. Sau khi thực thi biểu thức total += total * vat_rate với total = 950000 và vat_rate = 0.1, hãy xác định kiểu dữ liệu chính xác của biến total (int hay float) và giải thích nguyên do dựa trên quy tắc ép kiểu số học của Python.
2. Viết lại hai câu lệnh total -= discount_amount và total += total * vat_rate dưới dạng cú pháp biểu thức gán đầy đủ (không dùng toán tử phím tắt shortcut).
> **Gợi ý trả lời & Định hướng đáp án:** Gợi ý trả lời:
1. Kiểu dữ liệu của biến total sau câu lệnh là float (giá trị 1045000.0). Nguyên nhân: vat_rate có giá trị 0.1 là kiểu float. Khi thực hiện phép nhân total * vat_rate (950000 * 0.1), Python tự động ép kiểu phép nhân giữa int và float thành float (95000.0). Tiếp đó, phép cộng total + 95000.0 giữa int và float tiếp tục trả về kiểu float.
2. Cú pháp gán đầy đủ tương đương:
- total -= discount_amount tương đương với: total = total - discount_amount
- total += total * vat_rate tương đương với: total = total + (total * vat_rate)

---

### Câu 4: Bài đọc đưa ra cảnh báo về việc tính sai thứ tự ưu tiên của các phép toán làm ảnh hưởng đến tính đúng đắn của hóa đơn.
Dựa trên bảng độ ưu tiên toán tử và luồng xử lý trong bài đọc:
1. Phân tích thứ tự thực thi chi tiết của các toán tử trong biểu thức: test_val = 100 + 50 * 2 ** 3 // 4 - 10.
2. Xác định giá trị cuối cùng của biến test_val. Nếu muốn phép cộng 100 + 50 được thực hiện đầu tiên, lập trình viên phải thay đổi biểu thức như thế nào?
> **Gợi ý trả lời & Định hướng đáp án:** Gợi ý trả lời:
1. Phân tích thứ tự ưu tiên toán tử theo bài đọc:
- Bước 1 (Lũy thừa **): Tính 2 ** 3 = 8.
- Bước 2 (Nhân * và Chia nguyên // có độ ưu tiên ngang nhau, tính từ trái qua phải): Tính phép nhân 50 * 8 = 400 trước, sau đó tính phép chia nguyên 400 // 4 = 100.
- Bước 3 (Cộng + và Trừ - có độ ưu tiên thấp nhất, tính từ trái qua phải): Tính phép cộng 100 + 100 = 200 trước, sau đó tính phép trừ 200 - 10 = 190.
2. Giá trị cuối cùng của test_val là 190.
Để phép cộng 100 + 50 được ưu tiên thực hiện đầu tiên, lập trình viên bắt buộc phải đặt phép cộng vào trong cặp dấu ngoặc đơn: test_val = (100 + 50) * 2 ** 3 // 4 - 10, vì phép tính trong ngoặc () luôn có độ ưu tiên cao nhất.

---