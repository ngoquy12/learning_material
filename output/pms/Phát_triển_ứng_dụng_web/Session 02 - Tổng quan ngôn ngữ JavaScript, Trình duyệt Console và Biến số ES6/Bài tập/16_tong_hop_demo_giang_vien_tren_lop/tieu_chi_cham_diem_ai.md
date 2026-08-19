# **Tiêu chí chấm điểm (AI / Mentor)**

**[Tổng hợp Demo] Bài tập Tổng hợp Kiến thức Session — Tổng điểm: 100 điểm**

#### **1. Phân tích luồng & Sơ đồ thuật toán — 20 điểm**
- **Sơ đồ tiến trình thực thi (10 điểm)**: Vẽ/mô tả đầy đủ luồng tải tệp của trình duyệt và V8 Engine (Tải HTML -> Đọc thẻ script -> Nạp vào RAM -> Parser -> Ignition Bytecode).
- **Phân tích biến số & Scope (10 điểm)**: Bảng liệt kê chính xác các biến cần dùng, phân định rõ ràng biến nào dùng `const` (hằng số hệ thống), biến nào dùng `let` (dữ liệu nhập/thay đổi) và lý do không dùng `var`.

#### **2. Hiện thực hóa mã nguồn tích hợp — 40 điểm**
- **Cấu trúc tệp & Tách biệt Logic (10 điểm)**: Tạo tệp `index.html` và `app.js` riêng biệt; nhúng script chính xác ngay trước thẻ đóng `</body>`; khởi chạy thành công qua Live Server HTTP (không chạy bằng protocol `file:///`).
- **Khai báo biến ES6 & Naming Convention (10 điểm)**: Đặt tên biến đúng chuẩn `camelCase` (ví dụ: `clinicName`, `patientName`, `consultationFee`), khai báo đúng `const`/`let`, không xảy ra lỗi Re-assignment hay Ô nhiễm Scope.
- **Xử lý Nhập/Xuất Dữ liệu (10 điểm)**: Nhận dữ liệu thành công qua `prompt()`, bật thông báo hoàn tất qua `alert()` đúng quy trình nghiệp vụ.
- **Định dạng Template Literals (10 điểm)**: Sử dụng chính xác cặp dấu backticks (`` ` ``) và cú pháp `${variable}` để đóng gói chuỗi kết quả rõ ràng, chuyên nghiệp.

#### **3. Xử lý bẫy dữ liệu & Ngoại lệ — 20 điểm**
- **Ép kiểu dữ liệu minh bạch (10 điểm)**: Bắt buộc dùng `Number()` để chuyển đổi chuỗi số từ `prompt()` trước khi thực hiện phép tính toán học; giải thích và chứng minh được hậu quả nếu quên ép kiểu (lỗi cộng chuỗi).
- **Kiểm tra kiểu dữ liệu (10 điểm)**: Thực hiện in kết quả kiểm tra `typeof` của các biến số quan trọng ra Console để xác minh dữ liệu đã ở đúng dạng Số (`number`).

#### **4. Clean Code & Quy chuẩn nộp bài — 20 điểm**
- **Chú thích mã nguồn (10 điểm)**: Có comment ghi chú rõ ràng các bước thực hiện trong tệp `app.js`, giải thích logic xử lý cho từng phân đoạn nghiệp vụ.
- **Quy chuẩn cấu trúc thư mục (10 điểm)**: Đặt tên thư mục dự án đúng theo mẫu quy định `[Tên Lớp]_[Môn Học]_Session02_Demo`, mã nguồn không chứa câu lệnh thừa hoặc biến không sử dụng.
