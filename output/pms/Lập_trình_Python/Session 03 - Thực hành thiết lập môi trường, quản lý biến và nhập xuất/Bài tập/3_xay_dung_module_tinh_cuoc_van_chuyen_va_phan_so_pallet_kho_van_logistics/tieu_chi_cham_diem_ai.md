### **Tiêu chí chấm điểm (AI)**
**Bài tập: Xây dựng Module Tính Cước Vận Chuyển và Phân Sổ Pallet Kho Vận Logistics — Tổng điểm: 100 điểm**

#### **1. Thiết lập & Khởi tạo (10 điểm)**
- **Khởi tạo file & PEP 8 (5 điểm)**: Khởi tạo đúng tên file `logistics_calc.py`. Đặt tên tất cả các biến theo quy tắc `snake_case` (ví dụ: `tracking_code`, `weight_kg`, `chargeable_weight`).
- **Ghi chú & Docstring (5 điểm)**: Khai báo Docstring đầu file giải thích mục đích chương trình và ghi chú (`# comment`) giải thích các đoạn xử lý logic chính.

#### **2. Logic nghiệp vụ (30 điểm)**
- **Tính toán thể tích & Trọng lượng quy đổi (10 điểm)**: Thực hiện đúng công thức quy đổi cm³ sang m³ (`/ 1000000`) và trọng lượng quy đổi (`* 250`).
- **Xác định Trọng lượng tính cước (5 điểm)**: Sử dụng hàm `max()` chính xác để chọn trọng lượng lớn hơn giữa thực tế và quy đổi.
- **Phân bổ Pallet lưu kho (10 điểm)**: Sử dụng chính xác toán tử chia lấy nguyên `//` để tính số Pallet và toán tử chia lấy dư `%` để tính số kg còn lẻ.
- **Tính Cước thô & Thuế VAT & Tổng thanh toán (5 điểm)**: Áp dụng đúng công thức cước thô, tính chính xác 8% thuế VAT và tổng tiền phải trả.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ (30 điểm)**
- **Chuẩn hóa dữ liệu chuỗi (10 điểm)**: Áp dụng thành thạo các phương thức `.strip()`, `.upper()`, `.title()` để làm sạch dữ liệu đầu vào của `tracking_code` và `customer_name`.
- **Ép kiểu dữ liệu ép buộc (Explicit Casting) (10 điểm)**: Ép kiểu dữ liệu đầu vào từ `input()` thành `float` hoặc `int` chính xác trước khi đưa vào tính toán số học, không gây lỗi `TypeError`.
- **Định dạng số thập phân & Tiền tệ (10 điểm)**: Định dạng hiển thị đúng thể tích (`.3f`), trọng lượng (`.2f`) và dấu phân cách hàng nghìn (`,`) cho các giá trị tiền tệ trong f-string.

#### **4. Tối ưu hoá hiệu suất (20 điểm)**
- **Điều khiển luồng xuất Console (10 điểm)**: Sử dụng hợp lý các tham số `sep` và `end` trong hàm `print()` để tạo giao diện dòng lệnh ngăn nắp, dễ đọc.
- **Quản lý biến hiệu quả (10 điểm)**: Không sử dụng biến trung gian dư thừa, không trùng lặp các phép tính toán giống nhau.

#### **5. Chất lượng mã nguồn (10 điểm)**
- **Cấu trúc mã sạch (5 điểm)**: Mã nguồn viết mạch lạc, thụt lề chuẩn 4 spaces theo PEP 8, không có dòng trống thừa hoặc mã rác không sử dụng.
- **Đầu ra chính xác theo mẫu (5 điểm)**: Đảm bảo format Phiếu Cước Vận Tải hiển thị trên Terminal trùng khớp với cấu trúc mẫu yêu cầu.

#### **Điểm cộng (5-10 điểm)**
- **Căn chỉnh lề nâng cao (5 điểm)**: Sử dụng cú pháp căn lề f-string padding (ví dụ: `{label:<25}`) giúp các đường biên của bảng báo cáo thẳng hàng tuyệt đối.
- **Bắt lỗi nhập liệu cơ bản (5 điểm)**: Thêm giải pháp kiểm tra dữ liệu chuỗi rỗng bằng phương thức `str.strip()` trước khi ép kiểu.