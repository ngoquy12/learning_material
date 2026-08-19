# **Tiêu chí chấm điểm (AI)**
**Tính toán Chỉ số và Đánh giá Hạn mức Thẻ Tín dụng — Tổng điểm: 100 điểm**

#### **1. Thiết lập & Khởi tạo (10 điểm)**
- **10 điểm:** Tạo đúng file `credit_evaluator.py`, sử dụng đầy đủ Type Hints (`monthly_income: float`, `monthly_debt: float`, `has_bad_debt: int`, `requested_limit: float`) tuân thủ chuẩn PEP 8.
- **0 điểm:** Không làm bài hoặc sai cấu trúc tên file.

#### **2. Logic nghiệp vụ & Tính toán (40 điểm)**
- **40 điểm:** Tính toán chính xác tỷ lệ DTI, hạn mức thẻ tối đa `max_allowed_limit` theo đúng công thức.
- **20 điểm:** Tính toán đúng chỉ số nhưng sai tỉ lệ hoặc đơn vị làm tròn.
- **0 điểm:** Tính sai hoàn toàn các chỉ số cơ bản.

#### **3. Đánh giá kiểm chuẩn & Trạng thái phê duyệt (30 điểm)**
- **30 điểm:** Đánh giá đúng logic kết hợp toán tử Boolean để sinh ra cờ `is_input_valid` và cờ phê duyệt `is_approved` theo đúng quy tắc kinh doanh.
- **15 điểm:** Thiếu một trong các điều kiện logic (ví dụ: quên kiểm tra `has_bad_debt` hoặc kiểm tra sai ngưỡng DTI).
- **0 điểm:** Sử dụng sai logic đánh giá phê duyệt.

#### **4. Ràng buộc Phạm vi kiến thức & Tối ưu hóa (10 điểm)**
- **10 điểm:** Đáp ứng tuyệt đối yêu cầu **không sử dụng cấu trúc rẽ nhánh `if-else`**. Mọi tính toán và gán giá trị được giải quyết hoàn toàn bằng biểu thức Boolean và số học.
- **0 điểm:** Sử dụng câu lệnh `if`, `elif` hoặc `else` trong bài làm, vi phạm phạm vi kiến thức giới hạn của buổi học.

#### **5. Chất lượng trình bày (10 điểm)**
- **10 điểm:** Định dạng hiển thị kết quả rõ ràng, sử dụng f-string chuyên nghiệp, đặt tên biến chuẩn `snake_case`, thụt lề chuẩn.
- **5 điểm:** Trình bày mã nguồn cẩu thả, đặt tên biến kiểu CamelCase.
