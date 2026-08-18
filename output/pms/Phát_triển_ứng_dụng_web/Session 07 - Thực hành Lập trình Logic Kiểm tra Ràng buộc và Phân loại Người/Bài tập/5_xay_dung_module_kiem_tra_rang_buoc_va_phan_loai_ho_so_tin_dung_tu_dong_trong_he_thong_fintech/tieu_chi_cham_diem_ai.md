### **Tiêu chí chấm điểm (AI)**
**Xây dựng Module Kiểm Tra Ràng Buộc Và Phân Loại Hồ Sơ Tín Dụng Tự Động Trong Hệ Thống Fintech — Tổng điểm: 100 điểm**

#### **1. Thiết lập & Khởi tạo (10 điểm)**
- **Khai báo biến đầy đủ (5 điểm):** Khai báo chính xác các biến đầu vào (`fullName`, `creditScore`, `monthlyIncome`, `existingDebt`, `accountType`, `isBlacklisted`, `employmentYears`) sử dụng đúng từ khóa `const`/`let` ES6, áp dụng chuẩn đặt tên `camelCase`.
- **Cấu trúc tập tin & Môi trường (5 điểm):** Tổ chức mã nguồn sạch sẽ, lưu dưới dạng tệp `.js` hoặc nhúng script đúng chuẩn HTML5, thực thi thành công không phát sinh lỗi cú pháp (SyntaxError).

#### **2. Logic nghiệp vụ (30 điểm)**
- **Phân hạng tín dụng với if-else (10 điểm):** Sử dụng cấu trúc `if - else if - else` phân loại chuẩn xác 4 hạng tín dụng (`Platinum`, `Gold`, `Silver`, `Standard`) theo đúng dải điểm `creditScore`.
- **Xử lý nhóm tài khoản với switch-case (10 điểm):** Sử dụng đúng cấu trúc `switch-case` có từ khóa `break` và khối `default` để xác định `baseMultiplier` và `baseRate` tương ứng với `accountType`.
- **Áp dụng toán tử ba ngôi (10 điểm):** Sử dụng chính xác toán tử điều kiện `Ternary Operator` để tính toán `bonusMultiplier` dựa trên `employmentYears` và mức giảm `discountRate` dựa trên phân hạng tín dụng.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ (30 điểm)**
- **Kiểm tra tính hợp lệ dữ liệu đầu vào (15 điểm):** Tích hợp thành công kết hợp toán tử logic (`&&`, `||`, `!`) để chặn các trường hợp dữ liệu âm, điểm tín dụng ngoài miền `[300, 850]`, hoặc `accountType` không hợp lệ.
- **Thẩm định quy tắc từ chối vay (15 điểm):** Tính chính xác chỉ số DTI và thiết lập điều kiện chặn hồ sơ nợ xấu (`isBlacklisted === 1`), điểm tín dụng quá thấp (`creditScore < 550`), hoặc DTI vượt ngưỡng (`> 0.6`).

#### **4. Tối ưu hoá hiệu suất (20 điểm)**
- **Áp dụng cơ chế ngắn mạch Short-Circuit Evaluation (10 điểm):** Sắp xếp thứ tự các biểu thức điều kiện hợp lý trong mệnh đề `if` để dừng đánh giá ngay khi gặp điều kiện sai/đúng sớm nhất.
- **Biểu thức toán học & Xử lý số âm (10 điểm):** Công thức tính toán hạn mức và lãi suất chính xác. Đảm bảo `maxLoanLimit` không bị âm (gán bằng 0 nếu kết quả tính ra giá trị âm).

#### **5. Chất lượng mã nguồn (10 điểm)**
- **Template Literals & Định dạng Console (5 điểm):** Xuất báo cáo kết quả thẩm định rõ ràng, đẹp mắt bằng Template Literals backticks (`` `...` ``), hiển thị đầy đủ tiêu đề, phân hạng, hạn mức và lãi suất.
- **Quy chuẩn lập trình Clean Code (5 điểm):** Thụt lề chuẩn xác 2 hoặc 4 khoảng trắng, không chứa mã thừa, đặt tên biến có ý nghĩa bằng tiếng Anh.

#### **Điểm cộng (5-10 điểm)**
- **Thưởng tính năng nâng cao (5-10 điểm):** Tự động định dạng số tiền VND theo chuẩn phân cách hàng nghìn (ví dụ: `279,750,000 VNĐ`) hoặc sử dụng hàm `prompt()` tương tác trực tiếp với người dùng và ép kiểu dữ liệu an toàn bằng `Number()` / `parseFloat()`.