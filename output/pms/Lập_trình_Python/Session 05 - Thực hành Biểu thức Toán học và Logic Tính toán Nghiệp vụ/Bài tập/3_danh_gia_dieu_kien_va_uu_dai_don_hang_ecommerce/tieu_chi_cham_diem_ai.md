# **Tiêu chí chấm điểm (AI)**
**Đánh giá Điều kiện và Ưu đãi Đơn hàng E-Commerce — Tổng điểm: 100 điểm**

#### **1. Thiết lập & Khởi tạo (10 điểm)**
- **10 điểm:** Tạo đúng file `order_reward.py`, sử dụng đầy đủ Type Hints (`cart_value: float`, `is_vip: int`, `distance_km: float`) tuân thủ chuẩn PEP 8.
- **0 điểm:** Không làm bài hoặc sai cấu trúc tên file.

#### **2. Logic nghiệp vụ & Đánh giá Boolean (40 điểm)**
- **40 điểm:** Tính đúng các cờ Boolean `is_free_shipping` và `is_gift_approved` theo đúng quy tắc nghiệp vụ.
- **20 điểm:** Viết sai logic tính toán hoặc thiếu tham số của cờ.
- **0 điểm:** Sai hoàn toàn logic đánh giá.

#### **3. Tính toán phí vận chuyển thực tế phi rẽ nhánh (30 điểm)**
- **30 điểm:** Triển khai thành công công thức tính phí vận chuyển sau giảm trừ sử dụng toán tử Boolean nhân trực tiếp với giá trị float mà **không sử dụng câu lệnh điều kiện `if-else`**.
- **0 điểm:** Viết sai công thức tính hoặc sử dụng `if-else`.

#### **4. Ràng buộc Phạm vi kiến thức (10 điểm)**
- **10 điểm:** Hoàn toàn không sử dụng câu lệnh điều kiện rẽ nhánh `if`, `else`, `elif` trong toàn bộ file.
- **0 điểm:** Sử dụng câu lệnh điều kiện rẽ nhánh trong mã nguồn.

#### **5. Chất lượng trình bày (10 điểm)**
- **10 điểm:** Đặt tên biến snake_case chuẩn xác, định dạng f-string cho tiền tệ rõ ràng, có chú thích code.
