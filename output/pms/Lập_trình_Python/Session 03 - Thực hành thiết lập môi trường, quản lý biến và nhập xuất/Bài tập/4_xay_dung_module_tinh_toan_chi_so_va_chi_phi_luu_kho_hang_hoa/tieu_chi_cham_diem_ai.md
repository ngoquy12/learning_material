### **Tiêu chí chấm điểm (AI)**
**Bài tập: Xây dựng Module Tính toán Chỉ số và Chi phí Lưu kho Hàng hóa — Tổng điểm: 100 điểm**

#### **1. Thiết lập & Khởi tạo (10 điểm)**
- **10 điểm:** Tạo môi trường ảo `venv` đúng chuẩn; file `.py` có đầy đủ header docstring/comment theo quy tắc PEP 8; khai báo mã nguồn rõ ràng.
- **5 điểm:** Tạo file mã nguồn nhưng thiếu comment header hoặc không thiết lập môi trường `venv`.
- **0 điểm:** Không khởi tạo file mã nguồn đúng yêu cầu.

#### **2. Logic nghiệp vụ (30 điểm)**
- **30 điểm:** Thực hiện chính xác 100% các công thức toán học tính thể tích, trọng lượng quy đổi, trọng lượng tính phí, số lượng Pallet (sử dụng đúng chia lấy phần nguyên `//` và phép so sánh dư `%`), phụ phí 10% và thuế VAT 8%.
- **20 điểm:** Tính đúng thể tích và chi phí cơ bản nhưng sai công thức tính trọng lượng quy đổi hoặc tính sai số Pallet.
- **10 điểm:** Chỉ tính được thể tích cơ bản, sai toàn bộ logic phụ phí và thuế.
- **0 điểm:** Tính toán sai toàn bộ logic nghiệp vụ.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ (30 điểm)**
- **30 điểm:** Đọc dữ liệu từ `input()` chính xác; xử lý chuỗi nhập bằng `.strip()`; ép kiểu dữ liệu tường minh (Explicit Type Casting) đúng 100% cho toàn bộ các biến `float` và `int`.
- **20 điểm:** Ép kiểu đúng nhưng quên làm sạch dữ liệu đầu vào bằng `.strip()` cho chuỗi ký tự.
- **10 điểm:** Ép kiểu sai loại dữ liệu (ví dụ: số lượng thùng ép thành `float` hoặc đơn giá ép thành `int`).
- **0 điểm:** Không thực hiện ép kiểu dữ liệu, gây lỗi chương trình khi thực hiện phép toán.

#### **4. Tối ưu hoá hiệu suất (20 điểm)**
- **20 điểm:** Định dạng báo cáo dòng lệnh CLI căn chỉnh lề hoàn hảo bằng f-string (`:.4f`, `:.2f`); áp dụng thành thạo và hợp lý tham số `sep` và `end` trong hàm `print()`.
- **10 điểm:** Có định dạng dữ liệu đầu ra nhưng chưa tròn chữ số thập phân hoặc không sử dụng tham số `sep`/`end`.
- **0 điểm:** In kết quả thô, không định dạng bảng, không căn chỉnh.

#### **5. Chất lượng mã nguồn (10 điểm)**
- **10 điểm:** Đặt tên biến hoàn toàn theo chuẩn `snake_case` (PEP 8); code sáng rực, phân chia khối logic rõ ràng.
- **5 điểm:** Đặt tên biến vi phạm PEP 8 (ví dụ: `camelCase` hoặc đặt tên biến 1 ký tự không rõ nghĩa `a`, `b`, `c`).
- **0 điểm:** Mã nguồn lộn xộn, không tuân thủ bất kỳ quy chuẩn nào.

#### **Điểm cộng (5-10 điểm)**
- **+5 điểm:** Áp dụng định dạng dấu phân cách hàng nghìn cho số tiền (ví dụ: `2,700,000.00 VND`) bằng f-string specifier `:,2f`.
- **+5 điểm:** Xây dựng phần hiển thị giao diện CLI đẹp mắt, sáng tạo bằng các đường viền ký tự chuẩn hóa.