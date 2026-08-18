### **Tiêu chí chấm điểm (AI)**
**Mô phỏng Điểm An toàn Hệ thống và Kích hoạt Cảnh báo — Tổng điểm: 100 điểm**

#### **1. Thiết lập & Khởi tạo (10 điểm)**
- **10 điểm:** Tạo đúng file `system_guard.py`, sử dụng đầy đủ Type Hints (`cpu_usage: float`, `ram_usage: float`, `request_count: int`, `is_admin_ip: int`) tuân thủ chuẩn PEP 8.
- **0 điểm:** Không làm bài hoặc sai cấu trúc tên file.

#### **2. Chỉ số sức khỏe & Cảnh báo tài nguyên (35 điểm)**
- **35 điểm:** Tính đúng chỉ số sức khỏe `health_index` bằng công thức trọng số, tính đúng các cờ logic `cpu_alert` và `ram_alert`.
- **15 điểm:** Tính sai công thức hoặc sai mức cảnh báo.
- **0 điểm:** Tính sai hoàn toàn chỉ số sức khỏe máy chủ.

#### **3. Nghi ngờ DDoS & Cờ an toàn tổng thể (35 điểm)**
- **35 điểm:** Đánh giá đúng logic cờ nghi ngờ DDoS `ddos_alert` (kết hợp `is_admin_ip == 0`) và cờ an toàn hệ thống `is_system_safe`.
- **0 điểm:** Viết sai logic đánh giá rủi ro an ninh mạng.

#### **4. Ràng buộc Phạm vi kiến thức (10 điểm)**
- **10 điểm:** Hoàn toàn không sử dụng câu lệnh rẽ nhánh điều kiện `if`, `else`, `elif` trong mã nguồn.
- **0 điểm:** Sử dụng các câu lệnh `if-else` để rẽ nhánh.

#### **5. Chất lượng trình bày (10 điểm)**
- **10 điểm:** Mã nguồn trình bày sạch đẹp, đặt tên biến snake_case chuẩn xác, sử dụng f-string định dạng hiển thị kết quả.
