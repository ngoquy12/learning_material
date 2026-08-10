# Bộ câu hỏi tự luận kiểm tra bài đọc (Reading Comprehension Essay Questions)

### Câu 1: Giả sử một doanh nghiệp muốn triển khai hệ thống tự động hóa xử lý dữ liệu và xuất báo cáo định kỳ bằng Python 3.12. Dựa trên nội dung bài học về định hướng lập trình và kỳ vọng đầu ra sản phẩm thực tế, anh/chị hãy phân tích các lý do cốt lõi khiến Python được lựa chọn phổ biến cho các bài toán doanh nghiệp. Đồng thời, lập trình viên cần chuẩn bị tư duy lập trình và các chuẩn mực mã nguồn (như chuẩn PEP 8) như thế nào để một sản phẩm từ giai đoạn Demo có thể sẵn sàng đưa vào vận hành thực tế (Production-ready)?
> **Gợi ý trả lời & Định hướng đáp án:** Lời giải cần thể hiện được các điểm chính sau:
1. Lý do Python được ưu tiên lựa chọn: Cú pháp rõ ràng, đa năng, hệ sinh thái thư viện phong phú, tốc độ phát triển ứng dụng nhanh và khả năng tích hợp hệ thống cao.
2. Tư duy lập trình cần chuẩn bị: Tư duy phân tích bài toán thành các module độc lập, tư duy xử lý ngoại lệ (Exception Handling) để tránh sập hệ thống, và tư duy tối ưu hiệu năng.
3. Chuẩn mực mã nguồn để sẵn sàng Production: Tuân thủ chuẩn PEP 8 (đặt tên biến/hàm dạng snake_case, thụt lề 4 khoảng trắng, giới hạn độ dài dòng code), viết Docstring/comment giải thích logic nghiệp vụ phức tạp, và đảm bảo mã nguồn dễ đọc, dễ bảo trì và dễ mở rộng khi làm việc nhóm.

---

### Câu 2: Trong phiên bản Python 3.12, cơ chế thông báo lỗi (Enhanced Error Messages) đã được cải tiến đáng kể để hỗ trợ lập trình viên. Anh/chị hãy phân tích lợi ích của cải tiến này trong quá trình phát triển sản phẩm thực tế. Khi gặp sự cố chương trình bị dừng đột ngột do lỗi thực thi (Runtime Error) trong một ứng dụng Demo, anh/chị hãy trình bày quy trình các bước phân tích thông điệp Traceback để khoanh vùng và xử lý lỗi một cách bài bản.
> **Gợi ý trả lời & Định hướng đáp án:** Lời giải cần bao gồm các nội dung chính:
1. Lợi ích của Enhanced Error Messages trong Python 3.12: Chỉ rõ chính xác vị trí dòng lệnh xảy ra lỗi, đưa ra các gợi ý sửa lỗi thông minh (như gợi ý tên biến hoặc tên hàm bị gõ sai chính tả), giúp giảm thời gian debug và tăng tốc độ phát triển.
2. Quy trình phân tích Traceback bài bản:
- Bước 1: Đọc từ dưới lên trên để xác định loại lỗi (Exception Type) và thông điệp chi tiết (Error Message).
- Bước 2: Xác định vị trí tệp tin (File) và số dòng lệnh (Line number) phát sinh sự cố.
- Bước 3: Kiểm tra ngữ cảnh thực thi, giá trị và kiểu dữ liệu của các biến liên quan tại thời điểm xảy ra lỗi.
- Bước 4: Đưa ra giải pháp sửa đổi, tái cấu trúc mã nguồn hoặc thêm các khối try-except để bắt ngoại lệ dự phòng.

---

### Câu 3: Một học viên viết đoạn mã Python 3.12 để quản lý sản phẩm và tính tổng giá trị đơn hàng cho bài tập Demo như sau:

product_Name = "Laptop Dell"
price = "15000000"
quantity = 2
total = price * quantity
print("Tong gia tri don hang la: " + total)

Anh/chị hãy phân tích các lỗi về cú pháp (Syntax Error), lỗi kiểu dữ liệu/logic (TypeError/Logic Error) và các vị phạm quy chuẩn PEP 8 trong đoạn mã trên. Sau đó, hãy viết lại đoạn mã hoàn chỉnh đạt chuẩn Python 3.12 (sử dụng f-string) và giải thích chi tiết các điểm đã sửa đổi.
> **Gợi ý trả lời & Định hướng đáp án:** Lời giải chi tiết bao gồm:
1. Phân tích lỗi:
- Lỗi vi phạm PEP 8: Biến `product_Name` sử dụng kiểu CamelCase/mixedCase thay vì chuẩn snake_case (`product_name`).
- Lỗi kiểu dữ liệu / Logic: `price` đang mang kiểu chuỗi (str) `"15000000"`. Khi thực hiện phép nhân với số nguyên `quantity` (2), kết quả thu được là chuỗi lặp lại `"1500000015000000"` chứ không phải phép tính số học.
- Lỗi thực thi (TypeError): Lệnh `print` thực hiện nối chuỗi (`+`) giữa một string và biến `total` (khi đó là string hoặc int) có thể gây lỗi hoặc không đạt chuẩn định dạng đầu ra chuẩn.

2. Đoạn mã sửa lại chuẩn Python 3.12:
product_name = "Laptop Dell"
price = 15000000
quantity = 2
total = price * quantity
print(f"Tổng giá trị đơn hàng là: {total:,} VNĐ")

3. Giải thích sửa đổi: Chuyển `price` về kiểu số nguyên (int) để thực hiện đúng phép tính số học; đổi tên biến thành `product_name` theo chuẩn PEP 8; sử dụng f-string kết hợp định dạng số `{total:,}` giúp mã nguồn ngắn gọn, tối ưu hiệu năng và hiển thị kết quả trực quan.

---

### Câu 4: Trong định hướng phát triển phần mềm chuyên nghiệp bằng Python, việc quản lý phạm vi biến (Variable Scope) và thiết kế cấu trúc hàm đóng vai trò quyết định đến chất lượng sản phẩm. Anh/chị hãy phân tích tác hại của việc lạm dụng biến toàn cục (Global Variable) trong các bài toán thực tế. Để đạt được kỳ vọng đầu ra của khóa học, lập trình viên cần áp dụng nguyên lý thiết kế nào để truyền nhận dữ liệu giữa các thành phần một cách an toàn và minh bạch?
> **Gợi ý trả lời & Định hướng đáp án:** Lời giải cần làm rõ các luận điểm:
1. Tác hại của việc lạm dụng biến toàn cục (Global Variable):
- Làm mất tính đóng gói (Encapsulation) của ứng dụng.
- Gây khó khăn trong việc theo dõi luồng dữ liệu khi dự án phát triển lớn hơn, dễ dẫn đến lỗi hiệu ứng lề (Side-effects) do biến bị thay đổi ngoài kiểm soát ở nhiều nơi khác nhau.
- Gây cực kỳ khó khăn cho việc viết kiểm thử tự động (Unit Test) và tái sử dụng mã nguồn.

2. Nguyên lý thiết kế mã nguồn chuẩn mực:
- Áp dụng nguyên tắc đóng gói: Giới hạn phạm vi biến trong tầm cục bộ (Local Scope) của hàm hoặc lớp.
- Truyền dữ liệu minh bạch qua tham số đầu vào (Arguments/Parameters) của hàm.
- Trả về kết quả đầu ra rõ ràng thông qua từ khóa `return` thay vì thay đổi trực tiếp biến bên ngoài.
- Tổ chức mã nguồn thành các module/hàm đơn chức năng (Single Responsibility Principle) giúp mã nguồn đạt chuẩn công nghiệp.

---