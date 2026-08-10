# Bộ câu hỏi tự luận kiểm tra bài đọc (Reading Comprehension Essay Questions)

### Câu 1: Dựa vào sơ đồ luồng xác thực điều kiện tín dụng tự động trong bài đọc, hệ thống tiếp nhận hồ sơ đầu vào với các biến: `age = 25`, `income = 15,000,000 VNĐ` và `has_bad_debt = False`. Hãy phân tích giá trị chân lý của từng biểu thức thành phần trong Bộ đánh giá Logic (`age >= 18`, `income >= 10M`, `not has_bad_debt`) và giải thích vì sao kết quả Cờ hiệu cuối cùng lại trả về trạng thái True (ĐỦ ĐIỀU KIỆN).
> **Gợi ý trả lời & Định hướng đáp án:** Lời giải cần thể hiện chi tiết 3 bước đánh giá logic:
1. Biểu thức `age >= 18`: Thay giá trị `age = 25`, ta có `25 >= 18` mang giá trị `True`.
2. Biểu thức `income >= 10M`: Thu nhập 15,000,000 VNĐ lớn hơn ngưỡng 10,000,000 VNĐ nên `15,000,000 >= 10,000,000` mang giá trị `True`.
3. Biểu thức `not has_bad_debt`: Với `has_bad_debt = False`, phép phủ định `not False` trả về giá trị `True`.
Kết hợp cả 3 vế bằng toán tử `AND`: `True and True and True` cho kết quả cuối cùng là `True`. Do đó, cờ hiệu trạng thái trả về `True` tương ứng với kết luận hồ sơ ĐỦ ĐIỀU KIỆN.

---

### Câu 2: Bài đọc có đề cập đến cơ chế đánh giá ngắn mạch (Short-circuit Evaluation) của Python đối với các toán tử logic `and` và `or`. Hãy giải thích quy tắc dừng đánh giá của cơ chế này. Áp dụng vào thách thức của hệ thống ngân hàng số cần xử lý hàng triệu hồ sơ mỗi ngày, việc chủ động sắp xếp biểu thức kiểm tra nguy cơ nợ xấu (`has_bad_debt`) lên đầu chuỗi toán tử `and` mang lại lợi ích gì về mặt hiệu năng?
> **Gợi ý trả lời & Định hướng đáp án:** Lời giải cần làm rõ các ý chính:
1. Quy tắc cơ chế Short-circuit Evaluation:
- Đối với toán tử `and`: Nếu vế trái đánh giá ra `False`, toàn bộ biểu thức chắc chắn là `False`, Python sẽ dừng ngay lập tức và không tính toán tiếp vế phải.
- Đối với toán tử `or`: Nếu vế trái đánh giá ra `True`, toàn bộ biểu thức chắc chắn là `True`, Python sẽ dừng ngay và không tính toán vế phải.
2. Lợi ích vận hành cho hệ thống ngân hàng:
- Khi sắp xếp điều kiện kiểm tra nợ xấu (`has_bad_debt`) lên trước, nếu khách hàng có nợ xấu (`has_bad_debt = True` làm cho biểu thức `not has_bad_debt` thành `False`), toán tử `and` sẽ kích hoạt ngắn mạch ngay ở bước đầu tiên.
- Hệ thống lập tức loại hồ sơ mà không cần tốn tài nguyên CPU để tính toán các biểu thức so sánh thu nhập hay điểm tín dụng phía sau, giúp tối ưu hóa tốc độ xử lý Boolean khi duyệt hàng triệu hồ sơ/ngày.

---

### Câu 3: Trong phần giải pháp của bài đọc, đoạn mã mẫu khởi tạo các biến dữ liệu gồm: `customer_age = 24`, `monthly_income = 18000000`, `credit_score = 710` và `has_bad_debt = False`. Dựa theo Lộ trình 4 bước thiết lập cờ hiệu, hãy viết câu lệnh Python hợp nhất các tiêu chí (tuổi tối thiểu 18, thu nhập tối thiểu 10 triệu, điểm tín dụng từ 700 trở lên và không nợ xấu) vào một biến cờ hiệu tên là `is_approved`. Sau đó, diễn giải từng bước tính toán giá trị của biến này.
> **Gợi ý trả lời & Định hướng đáp án:** Lời giải cần bao gồm 2 phần chính:
1. Câu lệnh Python hợp nhất biểu thức logic:
`is_approved = (customer_age >= 18) and (monthly_income >= 10000000) and (credit_score >= 700) and (not has_bad_debt)`

2. Diễn giải chi tiết từng bước tính toán:
- Vế 1: `customer_age >= 18` -> `24 >= 18` -> `True`.
- Vế 2: `monthly_income >= 10000000` -> `18000000 >= 10000000` -> `True`.
- Vế 3: `credit_score >= 700` -> `710 >= 700` -> `True`.
- Vế 4: `not has_bad_debt` -> `not False` -> `True`.
Tổng hợp biểu thức: `True and True and True and True` => Biến cờ hiệu `is_approved` nhận giá trị cuối cùng là `True`.

---