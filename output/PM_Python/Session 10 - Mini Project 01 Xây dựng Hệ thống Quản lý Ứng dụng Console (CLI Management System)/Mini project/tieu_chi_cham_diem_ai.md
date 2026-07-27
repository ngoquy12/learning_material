### **Tiêu chí chấm điểm (AI)**
**Warehouse and Order Management CLI — Tổng điểm: 100 điểm**

#### **1. Thiết lập cấu trúc và Khởi tạo — 20 điểm**
- **10 điểm**: Khởi tạo thành công cấu trúc ứng dụng dưới dạng các hàm Python rõ ràng. Không sử dụng lập trình hướng đối tượng (Class) và thư viện ngoài theo đúng yêu cầu cài đặt của học phần.
- **10 điểm**: Triển khai hàm `initialize_system()` nạp đủ dữ liệu ban đầu cho kho hàng với cấu trúc kiểu dữ liệu phù hợp (List, Dict) đúng thỏa ước thiết kế.

#### **2. Logic nghiệp vụ cốt lõi — 30 điểm**
- **10 điểm**: Hàm `add_inventory_item` thực hiện thêm mới sản phẩm hoạt động chính xác, phát hiện trùng lặp mã sản phẩm và đưa ra cảnh báo chuẩn xác.
- **10 điểm**: Hàm `update_inventory_stock` điều chỉnh tăng hoặc giảm tồn kho chuẩn xác và an toàn (không cho phép giảm quá số lượng hàng đang có).
- **10 điểm**: Logic tạo và xử lý đơn hàng `process_new_order` hoạt động ổn định. Thực hiện trừ kho đúng mã hàng và tính tổng trị giá đơn hàng chính xác. Đảm bảo tính toàn vẹn dữ liệu (không trừ kho bất kỳ mặt hàng nào nếu có một mặt hàng bị thiếu).

#### **3. Kiểm chuẩn dữ liệu và Xử lý ngoại lệ — 30 điểm**
- **15 điểm**: Xử lý ngoại lệ thông minh bằng `try-except` trên đầu vào người dùng thông qua giao diện dòng lệnh. Ngăn chặn hệ thống bị tắt khi người dùng nhập sai kiểu dữ liệu chữ thay vì số.
- **15 điểm**: Kiểm chứng nghiệp vụ hợp lệ (Validation): từ chối nhập số lượng hoặc giá mang giá trị âm hoặc bằng không và phản hồi bằng thông báo lỗi cụ thể ra console.

#### **4. Chức năng nâng cao hoặc Kiểm thử tự động — 10 điểm**
- **10 điểm**: Xây dựng báo cáo tồn kho định dạng ASCII căn chỉnh cột trực quan, tính toán tổng số lượng sản phẩm, hoặc thực hiện bổ sung bộ lọc sản phẩm theo danh mục (`category`) tích hợp sẵn trên CLI giúp trải nghiệm người dùng tối ưu hơn.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
- **5 điểm**: Quy chuẩn đặt tên biến, tên hàm 100% bằng Tiếng Anh có ý nghĩa, tuân thủ nghiêm ngặt chuẩn cú pháp viết thường ngăn cách bằng dấu gạch dưới `snake_case`. Có ghi chú giải thích hoạt động các luồng xử lý phức tạp.
- **5 điểm**: Tổ chức Repository Github đúng cấu trúc yêu cầu, có tài liệu hướng dẫn vận hành chi tiết trong tệp README.md kèm hình ảnh minh họa cho các trường hợp kiểm thử thực tế.

#### **Điểm cộng khuyến khích (Bonus) — 5 đến 10 điểm**
- **5 điểm**: Triển khai tính năng lưu vết lịch sử giao dịch kho hoặc tích hợp cơ chế phân quyền tài khoản đơn giản (Admin / Staff) trực tiếp bằng cấu trúc dữ liệu mô phỏng trong bộ nhớ.