### **Tiêu chí chấm điểm (AI)**
**BÀI TẬP THỰC HÀNH: XÂY DỰNG MODULE PHÂN LOẠI VÀ TÍNH PHÍ LƯU KHO TỰ ĐỘNG — Tổng điểm: 100 điểm**

#### **1. Thiết lập & Khởi tạo (10 điểm)**
- **10 điểm**: Nhận đầy đủ 7 tham số đầu vào từ console qua hàm `input()`, xử lý chuỗi bằng `.strip()`, `.upper()` và ép kiểu dữ liệu (`float()`, `int()`) chính xác, không gây ra lỗi dừng chương trình đột ngột khi nhập đúng định dạng.
- **5 điểm**: Nhận thiếu tham số hoặc không thực hiện chuẩn hóa chuỗi đầu vào (thiếu `.strip()` hoặc `.upper()`).
- **0 điểm**: Không khởi tạo đúng các tham số đầu vào hoặc ghi sai cú pháp ép kiểu.

#### **2. Logic nghiệp vụ (30 điểm)**
- **30 điểm**:
  - Xác định chính xác khu vực lưu trữ (`HAZMAT_ZONE`, `COLD_ZONE`, `HEAVY_ZONE`, `STANDARD_ZONE`) theo đúng thứ tự ưu tiên nghiệp vụ và toán tử logic (`and`, `or`).
  - Tính toán chính xác hệ số phụ phí thời gian (`time_factor`), phụ phí dễ vỡ (`fragility_factor`) và tổng chi phí lưu kho (`total_fee`).
  - Phân loại đúng mức độ ưu tiên vận chuyển (`HIGH_PRIORITY` / `NORMAL_PRIORITY`).
- **20 điểm**: Phân loại khu vực lưu trữ đúng nhưng tính sai hệ số phụ phí hoặc sai thứ tự ưu tiên rẽ nhánh.
- **10 điểm**: Logic rẽ nhánh sai nhiều hơn 2 trường hợp khu vực kho.
- **0 điểm**: Viết sai toàn bộ câu lệnh điều kiện `if-elif-else`.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ (30 điểm)**
- **30 điểm**: 
  - Kiểm tra đầy đủ 6 điều kiện hợp lệ dữ liệu (SKU rỗng, loại hàng, trọng lượng <= 0, thể tích <= 0, số ngày < 1, xác nhận dễ vỡ).
  - Sử dụng cấu trúc rẽ nhánh để chặn luồng xử lý ngay khi phát hiện dữ liệu lỗi (Short-circuit / Early Exit), in thông báo lỗi chính xác theo yêu cầu và không thực hiện tính toán tiếp.
- **15 điểm**: Kiểm tra thiếu 2-3 điều kiện hợp lệ hoặc vẫn tiếp tục tính toán chi phí khi dữ liệu đầu vào bị lỗi.
- **0 điểm**: Không thực hiện bất kỳ thao tác kiểm chuẩn dữ liệu nào.

#### **4. Tối ưu hoá hiệu suất (20 điểm)**
- **20 điểm**: 
  - Tận dụng tối đa nguyên lý Short-circuit evaluation trong biểu thức điều kiện `if` (đặt điều kiện dễ vi phạm hoặc quan trọng lên trước).
  - Cấu trúc các nhóm rẽ nhánh `if-elif-else` phẳng, tránh việc lồng ghép quá 3 cấp `if` không cần thiết.
- **10 điểm**: Rẽ nhánh lồng nhau quá sâu (Nested if >= 4 cấp) gây khó đọc hoặc lặp lại các phép so sánh trùng lặp.
- **0 điểm**: Sử dụng nhiều câu lệnh `if` độc lập không hợp lý dẫn đến đánh giá dư thừa tất cả điều kiện.

#### **5. Chất lượng mã nguồn (10 điểm)**
- **10 điểm**: Đặt tên biến chuẩn `snake_case` theo PEP 8, mã nguồn trình bày sạch sẽ, có comment giải thích rõ ràng các bước xử lý logic, định dạng output rõ ràng và chuyên nghiệp.
- **5 điểm**: Đặt tên biến chưa chuẩn (dùng camelCase hoặc tên viết tắt 1 ký tự khó hiểu), thiếu comment.
- **0 điểm**: Viết code lộn xộn, vi phạm nghiêm trọng quy tắc thụt lề (IndentationError) của Python.

#### **Điểm cộng (5-10 điểm)**
- **+5 điểm**: Định dạng số tiền VNĐ đầu ra có dấu phân cách hàng nghìn (ví dụ: `4,140,000 VNĐ`) bằng format string.
- **+5 điểm**: Xử lý ngoại lệ người dùng nhập sai kiểu dữ liệu (ví dụ nhập chữ vào trường số) một cách an toàn bằng câu lệnh kiểm tra logic trước khi ép kiểu.