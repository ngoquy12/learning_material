### **Tiêu chí chấm điểm (AI)**
**Xây Dựng Engine Thẩm Định Hạn Mức Tín Dụng Và Phê Duyệt Khoản Vay Tự Động Fintech — Tổng điểm: 100 điểm**

#### **1. Thiết lập & Khởi tạo (10 điểm)**
- **[10 điểm]:** Khởi tạo thành công Virtual Environment (`venv`), tạo file `fintech_credit_risk_engine.py` có khối Docstring mô tả tiêu chuẩn ở đầu file, khai báo mã nguồn chạy tương thích hoàn toàn trên Python 3.12.
- **[05 điểm]:** Tạo file script nhưng thiếu `venv` hoặc không có khối chú thích Docstring tiêu chuẩn.
- **[0 điểm]:** Không tạo môi trường ảo và file script bị lỗi khởi chạy ban đầu.

#### **2. Logic nghiệp vụ (30 điểm)**
- **[30 điểm]:** Thực hiện chính xác tất cả các công thức tài chính: `net_monthly_income`, `dti_ratio`, `credit_score_factor`, `approved_credit_limit`, `monthly_interest_rate`, `monthly_installment` (PMT), `total_payment`, `total_interest` và kết quả luận lý `is_eligible`.
- **[20 điểm]:** Tính đúng trên 80% công thức, sai sót nhỏ ở công thức lũy thừa PMT hoặc quy đổi lãi suất tháng.
- **[10 điểm]:** Chỉ tính được các phép cộng trừ thu nhập ròng và DTI đơn giản, chưa tính được PMT và tổng lãi.
- **[0 điểm]:** Thất bại trong việc triển khai logic tính toán tài chính.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ (30 điểm)**
- **[30 điểm]:** Sử dụng `input()` đúng cú pháp cho 7 tham số, thực hiện ép kiểu explicit bắt buộc (`str`, `float`, `int`) chính xác cho từng biến. Xử lý đúng kiểu trả về `bool` cho biến trạng thái phê duyệt.
- **[20 điểm]:** Ép kiểu đúng đa số các trường dữ liệu nhưng quên ép kiểu số nguyên cho `credit_score` hoặc `tenure_months` (để mặc định chuỗi/float).
- **[10 điểm]:** Quên ép kiểu dữ liệu từ `input()`, gây ra lỗi `TypeError` khi thực hiện phép toán số học.
- **[0 điểm]:** Không thu thập dữ liệu qua `input()`, gán cứng giá trị trong code.

#### **4. Tối ưu hoá hiệu suất (20 điểm)**
- **[20 điểm]:** Trình bày báo cáo CLI chuyên nghiệp, căn lề sạch đẹp, định dạng số thực 2 chữ số thập phân (`:.2f`), sử dụng thành thục tham số `sep` và `end` trong hàm `print()` theo đúng yêu cầu bài toán.
- **[10 điểm]:** In được kết quả ra màn hình nhưng không định dạng số thập phân, không tuân thủ cấu trúc khung báo cáo hoặc không sử dụng `sep`/`end`.
- **[0 điểm]:** Màn hình console xuất dữ liệu hỗn loạn, không đọc được kết quả.

#### **5. Chất lượng mã nguồn (10 điểm)**
- **[10 điểm]:** Mã nguồn tuân thủ nghiêm ngặt chuẩn PEP 8 (đặt tên biến `snake_case`, khoảng cách toán tử, dòng trống phân chia logic), biến được đặt tên rõ nghĩa bằng tiếng Anh.
- **[05 điểm]:** Đặt tên biến chưa chuẩn PEP 8 (ví dụ: dùng camelCase hoặc viết tắt khó hiểu như `a`, `b`, `c`).
- **[0 điểm]:** Code vi phạm nghiêm trọng các quy chuẩn lập trình Python cơ bản.

#### **Điểm cộng (5-10 điểm)**
- **[+5 điểm]:** Áp dụng kỹ thuật f-string kết hợp với tính năng căn lề chuỗi (string alignment `:<25`, `:>15`) giúp báo cáo CLI căn chỉnh cột hoàn hảo trên nhiều thiết bị hiển thị khác nhau.
- **[+5 điểm]:** Bổ sung thêm biến tính toán chỉ số khả năng chi trả nợ hàng tháng (`installment_to_income_ratio`) để hiển thị mức độ an toàn tài chính nâng cao.