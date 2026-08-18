### **Tiêu chí chấm điểm (AI)**
**Thẩm định Hợp lệ và Đánh giá Rủi ro Vận chuyển Logistics — Tổng điểm: 100 điểm**

#### **1. Thiết lập & Khởi tạo (10 điểm)**
- **10 điểm:** Tạo đúng file `cargo_evaluator.py`, sử dụng đầy đủ Type Hints (`cargo_weight: float`, `is_dangerous: int`, `declared_value: float`, `has_license: int`) tuân thủ chuẩn PEP 8.
- **0 điểm:** Không làm bài hoặc sai cấu trúc tên file.

#### **2. Logic tính cước phí (35 điểm)**
- **35 điểm:** Tính đúng cước cơ bản, phụ phí trọng lượng lớn sử dụng nhân Boolean, phụ phí hàng nguy hiểm và tổng chi phí vận chuyển.
- **15 điểm:** Tính sai một trong các phụ phí hoặc tính sai tổng cước phí.
- **0 điểm:** Tính sai hoàn toàn cước phí.

#### **3. Thẩm định Boolean & Phê duyệt đơn (35 điểm)**
- **35 điểm:** Thiết lập đúng biểu thức logic Boolean cho yêu cầu bảo hiểm `is_insurance_required` và điều kiện phê duyệt đơn vận chuyển `is_approved`.
- **0 điểm:** Viết sai logic phê duyệt vận chuyển.

#### **4. Ràng buộc Phạm vi kiến thức (10 điểm)**
- **10 điểm:** Đáp ứng tuyệt đối yêu cầu **không sử dụng câu lệnh rẽ nhánh `if-else`** trong mã nguồn.
- **0 điểm:** Sử dụng các câu lệnh `if-else` trong bài làm.

#### **5. Chất lượng trình bày (10 điểm)**
- **10 điểm:** Mã nguồn viết sạch sẽ, tuân thủ thụt lề chuẩn, đặt tên biến snake_case chuẩn, định dạng số liệu đẹp.
