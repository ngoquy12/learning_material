### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 4] Sửa lỗi tính tổng chi phí đăng ký khám bệnh tự động — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra đúng vị trí dòng khai báo/gán biến `specialistSurcharge` chưa được chuyển đổi kiểu dữ liệu từ Chuỗi sang Số.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thiện chính xác 100% các ô thông tin còn thiếu (`...`) trong dòng STT 2 và STT 3 của bảng báo cáo kiểm thử.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sửa thành công phép cộng số học, đảm bảo tổng chi phí khám bệnh tính toán chính xác tuyệt đối.
*   **[20 điểm] Ép kiểu dữ liệu minh bạch:** Áp dụng đúng hàm `Number()` cho toàn bộ dữ liệu số nhập từ `prompt()`.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Định dạng chuỗi kết quả chuẩn xác:** Sử dụng cú pháp Template Literals `${...}` để ghép chuỗi hóa đơn đầy đủ thông tin bệnh nhân, tiền khám, phụ phí và tổng tiền.
*   **[10 điểm] Xuất dữ liệu đa kênh:** Thực thi đúng việc xuất dữ liệu đồng thời ra cả `console.log()` và `alert()`.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích được cơ chế ép kiểu ngầm định (implicit type coercion) của toán tử `+` trong JavaScript khi có ít nhất một toán hạng là kiểu `String`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến chuẩn camelCase (`patientName`, `baseFee`, `specialistSurcharge`, `totalFee`), sử dụng `const`/`let` đúng phạm vi và đúng mục đích.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc tên thư mục quy định `[Tên Lớp]_[Môn Học]_Session02_Ex4`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý dữ liệu không hợp lệ:** Thêm đoạn mã kiểm tra nếu giá trị chuyển đổi bằng `NaN` (ví dụ bệnh nhân nhập chữ thay vì số) thì thông báo cảnh báo nhập sai dữ liệu.