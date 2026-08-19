# **Tiêu chí chấm điểm (AI)**
**Hệ thống Đánh giá Điều kiện Học bổng Sinh viên — Tổng điểm: 100 điểm**

#### **1. Thiết lập & Khởi tạo (10 điểm)**
- **10 điểm:** Khởi tạo đúng file `scholarship_checker.py`, sử dụng đầy đủ Type Hints (`gpa: float`, `social_hours: int`, `is_poor: int`, `violations: int`) tuân thủ chuẩn PEP 8.
- **0 điểm:** Không làm bài hoặc sai cấu trúc tên file.

#### **2. Logic nghiệp vụ & Quy đổi điểm (35 điểm)**
- **35 điểm:** Thực hiện đúng công thức quy đổi điểm học thuật hệ 100 và tính toán các cờ Boolean riêng biệt cho học bổng học thuật và học bổng hỗ trợ.
- **15 điểm:** Tính sai công thức quy đổi hoặc đánh giá thiếu các tham số.
- **0 điểm:** Viết sai toàn bộ logic nghiệp vụ học bổng.

#### **3. Kiểm chuẩn dữ liệu & Quyết định học bổng (35 điểm)**
- **35 điểm:** Kiểm tra hợp lệ dữ liệu GPA, số giờ hoạt động, số lỗi kỷ luật và tích hợp chuẩn xác thành cờ quyết định học bổng cuối cùng `is_scholarship_approved` bằng toán tử `and`/`or`/`not`.
- **0 điểm:** Tính sai logic phê duyệt học bổng chung.

#### **4. Quy tắc Không dùng cấu trúc rẽ nhánh (10 điểm)**
- **10 điểm:** Đáp ứng tuyệt đối yêu cầu **không sử dụng câu lệnh rẽ nhánh `if-else`**. Giải quyết hoàn toàn bằng biểu thức Boolean và số học.
- **0 điểm:** Sử dụng từ khóa `if`, `else`, `elif` trong bài làm.

#### **5. Chất lượng trình bày (10 điểm)**
- **10 điểm:** Trình bày code khoa học, đặt tên biến chuẩn `snake_case`, sử dụng f-string định dạng hiển thị kết quả.
