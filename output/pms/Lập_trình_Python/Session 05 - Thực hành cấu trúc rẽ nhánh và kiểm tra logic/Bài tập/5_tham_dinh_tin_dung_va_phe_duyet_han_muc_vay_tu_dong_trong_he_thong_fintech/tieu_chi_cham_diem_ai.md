### **Tiêu chí chấm điểm (AI)**
**Thẩm Định Tín Dụng và Phê Duyệt Hạn Mức Vay Tự Động Trong Hệ Thống Fintech — Tổng điểm: 100 điểm**

#### **1. Thiết lập & Khởi tạo (10 điểm)**
- **[10 điểm]**: Khai báo và ép kiểu toàn bộ 9 biến đầu vào đúng yêu cầu (`str`, `int`, `float`). Cấu trúc file `.py` chuẩn xác, chạy trực tiếp từ Terminal không gặp lỗi cú pháp. Khoảng trắng và ghi chú code (comments) tuân thủ PEP 8.

#### **2. Logic nghiệp vụ (30 điểm)**
- **[10 điểm]**: Tính toán chính xác các chỉ số tài chính trung gian: Nghĩa vụ trả nợ hàng tháng cho nợ hiện tại (`current_debt * 0.05`), Nghĩa vụ nợ mới (`requested_loan * (1 + base_annual_rate) / loan_term_months`), và tỷ lệ DTI.
- **[15 điểm]**: Hiện thực hóa đúng cây quyết định (Decision Tree) phân loại 4 trạng thái (`REJECTED`, `APPROVED_VIP`, `APPROVED_STANDARD`, `APPROVED_CONDITIONAL`) với thứ tự rẽ nhánh chính xác, không bỏ sót trường hợp hoặc sai sót logic điều kiện.
- **[5 điểm]**: Tính toán chính xác `max_approved_loan`, `applied_annual_rate` và so sánh tìm `actual_approved_loan` hợp lý.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ (30 điểm)**
- **[15 điểm]**: Kiểm tra đầy đủ điều kiện hợp lệ của 9 tham số đầu vào (miền giá trị tuổi, thu nhập, CIC, dư nợ, nhóm nợ xấu, kỳ hạn, thế chấp).
- **[15 điểm]**: Thực hiện rẽ nhánh chặn ngay lập tức (Early Return/Exit logic) khi phát hiện dữ liệu vi phạm, in thông báo lỗi chính xác và dừng quy trình thẩm định mà không gây crash chương trình.

#### **4. Tối ưu hoá hiệu suất (20 điểm)**
- **[10 điểm]**: Sử dụng kết hợp tối ưu các toán tử logic `and`, `or`, `not` để gộp điều kiện rẽ nhánh, tránh việc lặp lại câu lệnh `if` dư thừa.
- **[10 điểm]**: Tận dụng cơ chế Short-circuit Evaluation (ví dụ: đưa điều kiện dễ vi phạm hoặc điều kiện từ chối rủi ro cao lên đầu tiên) để ngắt luồng xử lý sớm nhất có thể.

#### **5. Chất lượng mã nguồn (10 điểm)**
- **[5 điểm]**: Đặt tên biến hoàn toàn theo chuẩn `snake_case` ngắn gọn, mang ý nghĩa nghiệp vụ tài chính rõ ràng.
- **[5 điểm]**: Định dạng báo cáo Console sạch đẹp, rõ ràng, căn lề thẳng hàng, in đúng định dạng số thực/phần trăm.

#### **Điểm cộng (5-10 điểm)**
- **[+5 điểm]**: Sử dụng chuỗi định dạng F-string nâng cao để căn chỉnh độ rộng cột và phân cách phần ngàn hiển thị tiền tệ (ví dụ: `{monthly_income:,.1f}`).
- **[+5 điểm]**: Mã nguồn sạch hoàn toàn không sử dụng các cấu trúc nâng cao chưa học (vòng lặp, hàm, mảng) mà vẫn đạt được sự gọn gàng và tường minh cao nhất.