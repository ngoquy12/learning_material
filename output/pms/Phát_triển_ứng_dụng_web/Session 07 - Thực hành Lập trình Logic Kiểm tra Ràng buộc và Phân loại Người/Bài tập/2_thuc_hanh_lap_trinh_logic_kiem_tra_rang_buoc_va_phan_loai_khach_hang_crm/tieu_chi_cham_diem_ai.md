### **Tiêu chí chấm điểm (AI)**
**CRM Customer Classifier — Tổng điểm: 100 điểm**

#### **1. Thiết lập & Khởi tạo (10 điểm)**
- **10 điểm:** Khai báo đầy đủ 6 biến nguyên thủy (`customerName`, `customerAge`, `annualRevenue`, `creditScore`, `tierCode`, `hasOverdueDebt`) đúng chuẩn ES6 (`const`/`let`), áp dụng chính xác quy tắc đặt tên `camelCase`, dữ liệu khởi tạo phù hợp theo đúng tả nghiệp vụ.
- **5 điểm:** Khai báo đủ biến nhưng đặt tên sai quy tắc camelCase hoặc dùng từ khóa `var` không phù hợp.
- **0 điểm:** Thiếu biến đầu vào hoặc không khởi tạo file mã nguồn theo yêu cầu.

#### **2. Logic nghiệp vụ (30 điểm)**
- **10 điểm (Yêu cầu 2 - Switch-case):** Sử dụng cấu trúc `switch(tierCode)` đúng cú pháp, có đầy đủ từ khóa `break` cho mỗi case (1, 2, 3, 4) và xử lý trường hợp `default`. Gán chính xác `tierName` và `discountPercent`.
- **10 điểm (Yêu cầu 3 - If/Else):** Sử dụng các câu lệnh `if / else-if / else` kết hợp toán tử logic (`&&`, `||`) phân loại chính xác 4 cấp độ ưu tiên chăm sóc (`priorityLevel`) theo đúng điều kiện kinh doanh.
- **10 điểm (Yêu cầu 4 - Ternary Operator):** Viết đúng biểu thức điều kiện ba ngôi `condition ? val1 : val2` ngắn gọn, không lạm dụng `if/else` cho yêu cầu này để xác định `creditApproval`.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ (30 điểm)**
- **30 điểm:** Viết logic kiểm tra ràng buộc dữ liệu đầu vào đầy đủ cho các trường (Tên không rỗng, Tuổi 18-100, Doanh thu >= 0, Điểm tín nhiệm 300-850). Chương trình dừng xử lý các bước sau ngay lập tức khi phát hiện dữ liệu vi phạm và in báo cáo lỗi rõ ràng.
- **15 điểm:** Có kiểm tra ràng buộc nhưng thiếu trường dữ liệu hoặc vẫn để chương trình tiếp tục thực thi logic phía sau khi đã có lỗi xảy ra.
- **0 điểm:** Không thực hiện kiểm chuẩn dữ liệu đầu vào.

#### **4. Tối ưu hoá hiệu suất (20 điểm)**
- **20 điểm:** Sử dụng so sánh bằng nghiêm ngặt (`===`, `!==`), áp dụng cơ chế ngắn mạch (short-circuit evaluation) hợp lý trong biểu thức logic, không dư thừa lệnh rẽ nhánh.
- **10 điểm:** Sử dụng so sánh lỏng lẻo (`==`, `!=`) hoặc viết lặp lại các câu lệnh điều kiện bị trùng lặp logic.
- **0 điểm:** Logic rẽ nhánh sai dẫn đến kết quả phân loại bị lặp hoặc không chính xác.

#### **5. Chất lượng mã nguồn (10 điểm)**
- **10 điểm:** Mã nguồn thụt lề (indentation) chuẩn xác 2 hoặc 4 khoảng trắng, có ghi chú (comments) giải thích rõ ràng từng khối logic (Validation, Switch-case, If-else, Ternary), định dạng đầu ra console đẹp mắt bằng Template Literals đúng mẫu.
- **5 điểm:** Đầu ra in ra console đúng nhưng mã nguồn chưa thụt lề sạch đẹp, thiếu ghi chú giải thích.
- **0 điểm:** Mã nguồn rối rắm, không theo định dạng chuẩn.

#### **Điểm cộng (5-10 điểm)**
- **+5 điểm:** Định dạng số tiền doanh thu theo định dạng tiền tệ VNĐ có phân cách hàng nghìn rõ ràng trước khi in ra báo cáo.
- **+5 điểm:** Tạo thêm kịch bản kiểm thử bao quát được tất cả các nhánh điều kiện biên (Boundary Edge Cases).