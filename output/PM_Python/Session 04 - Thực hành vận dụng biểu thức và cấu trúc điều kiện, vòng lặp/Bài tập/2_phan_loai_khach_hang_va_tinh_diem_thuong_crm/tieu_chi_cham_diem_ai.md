### **Tiêu chí chấm điểm (AI)**
**Phân Loại Khách Hàng và Tính Điểm Thưởng CRM — Tổng điểm: 100 điểm**

#### **1. Thiết lập cấu trúc và Khởi tạo — 20 điểm**
* **10 điểm**: Thiết lập thành công vòng lặp chính `while` để chương trình chạy liên tục và chỉ dừng lại (sử dụng lệnh `break`) khi người dùng nhập chuỗi "STOP" (không phân biệt chữ hoa, chữ thường bằng phương thức như `.upper()` hoặc `.lower()`).
* **10 điểm**: Khởi tạo chính xác biến đếm số lượng khách hàng đã xử lý thành công ngoài vòng lặp và tăng giá trị biến đếm này sau mỗi lượt xử lý thành công.

#### **2. Logic nghiệp vụ cốt lõi — 30 điểm**
* **15 điểm**: Viết chính xác cấu trúc logic `if-elif-else` lồng nhau để phân chia 4 hạng khách hàng (Kim Cương, Vàng, Bạc, Đồng) theo đúng hai điều kiện ràng buộc đồng thời (Tổng chi tiêu và Số tháng hoạt động tích cực như mô tả ở Mục 4). 
* **15 điểm**: Tính toán chuẩn xác điểm thưởng:
  * Điểm cơ bản tính đúng theo từng nhóm hạng (nhân số hóa đơn với hệ số tương ứng).
  * Điểm thưởng thêm (Bonus) tính đúng bằng cách kiểm tra điều kiện số hóa đơn > 5 và áp dụng phép nhân tỉ lệ 10%.

#### **3. Kiểm chuẩn dữ liệu và Xử lý ngoại lệ — 30 điểm**
* **15 điểm**: Thực hiện xác thực các biểu thức đầu vào. Kiểm tra các giá trị chi tiêu, số tháng hoạt động, số hóa đơn không được âm. Nếu có giá trị âm, chặn lại và thông báo lỗi.
* **15 điểm**: Sử dụng câu lệnh điều khiển vòng lặp `continue` một cách chính xác để quay lại đầu vòng lặp yêu cầu nhập mới sau khi phát hiện lỗi dữ liệu đầu vào mà không làm tăng biến đếm số khách hàng và không làm crash chương trình.

#### **4. Kiểm thử hoặc câu hỏi lý thuyết bổ sung — 10 điểm**
* **10 điểm**: Chương trình in ra định dạng rõ ràng các thông tin kết quả tính toán của từng khách hàng và hiển thị tổng số khách hàng đã phân hạng thành công khi kết thúc chương trình giống như mô tả trong các testcase ở mục Yêu cầu bài toán.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
* **5 điểm**: Đặt tên biến rõ ràng, theo định dạng snake_case của Python (ví dụ: `total_spend`, `active_months`, `bill_count`), phản ánh đúng ý nghĩa nghiệp vụ. Mã nguồn được viết thụt dòng căn chỉnh chuẩn quy ước PEP 8. Có bình luận (comment) ngắn gọn giải thích logic tại các khối xử lý chính.
* **5 điểm**: Nộp bài đúng hạn thông qua đường dẫn GitHub repository hợp lệ chứa tập tin mã nguồn.

#### **Điểm cộng khuyến khích (Bonus) — 5 điểm**
* **5 điểm**: Xử lý thêm ngoại lệ dữ liệu đầu vào không phải là số khi ép kiểu (sử dụng cấu trúc `try-except` cơ bản để bắt lỗi `ValueError` khi người dùng nhập chữ vào các ô thông tin chi tiêu hay số hóa đơn).