### **Tiêu chí chấm điểm (AI)**
**Xây dựng Module Logic Phân loại Hội viên và Tính Phí Vận chuyển Đơn hàng E-commerce — Tổng điểm: 100 điểm**

#### **1. Thiết lập & Khởi tạo (10 điểm)**
- **Khởi tạo đúng các biến primitive:** Khai báo chính xác 3 biến `userTotalSpent`, `shippingZoneCode`, `isVipMember` đúng kiểu dữ liệu (number, string, boolean) theo đúng chuẩn JavaScript ES6 (`let`/`const`) (5 điểm).
- **Cấu trúc tập tin:** Đặt tên file chính xác `script.js`, mã nguồn không chứa lỗi cú pháp cơ bản khi thực thi (5 điểm).

#### **2. Logic nghiệp vụ (30 điểm)**
- **Phân loại thứ hạng hội viên bằng `if-else if-else`:** Xác định chính xác các cấp bậc "ĐỒNG", "BẠC", "VÀNG" và phần trăm giảm giá theo đúng các mốc điều kiện tổng chi tiêu (10 điểm).
- **Tra cứu phí vận chuyển bằng `switch-case`:** Sử dụng đúng cấu trúc `switch-case` cho `shippingZoneCode`, có đầy đủ lệnh `break` ở mỗi nhánh và xử lý đúng trường hợp `default` (10 điểm).
- **Vận dụng toán tử ba ngôi (Ternary Operator):** Áp dụng đúng toán tử 3 ngôi để tính phí vận chuyển ưu đãi 50% khi `isVipMember === true` (10 điểm).

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ (30 điểm)**
- **Kiểm tra dữ liệu đầu vào:** Kiểm tra chính xác điều kiện `userTotalSpent < 0`, dừng chương trình hợp lý và xuất câu thông báo lỗi chi tiết (15 điểm).
- **Tích hợp logic điều kiện kết hợp:** Sử dụng đúng toán tử logic `&&` và `||` để miễn phí vận chuyển 0 VNĐ cho hội viên VÀNG thuộc vùng 'INNER' hoặc có thẻ VIP (15 điểm).

#### **4. Tối ưu hoá hiệu suất (20 điểm)**
- **Kiểm tra so sánh nghiêm ngặt:** Sử dụng nhất quán toán tử so sánh bằng nghiêm ngặt `===` và khác nghiêm ngặt `!==` khi kiểm tra chuỗi và giá trị boolean (10 điểm).
- **Cấu trúc luồng rẽ nhánh ngắn gọn:** Luồng xử lý logic gọn gàng, tránh các câu lệnh rẽ nhánh thừa thãi hoặc kiểm tra điều kiện trùng lặp (10 điểm).

#### **5. Chất lượng mã nguồn (10 điểm)**
- **Đặt tên biến & Định dạng code:** Tên biến tuân thủ quy tắc `camelCase` mang ý nghĩa rõ ràng, thụt lề chuẩn xác, code sạch sẽ chuyên nghiệp (5 điểm).
- **Xuất kết quả đúng định dạng:** Sử dụng Template Literals (`...`) để hiển thị báo cáo ra màn hình Console khớp với cấu trúc ví dụ mẫu (5 điểm).

#### **Điểm cộng (5-10 điểm)**
- **Tính linh hoạt:** Xử lý chuẩn xác trường hợp `shippingZoneCode` nhập vào dạng chữ thường/chữ hoa (ví dụ sử dụng `.toUpperCase()` nếu học viên tự tìm hiểu thêm) (+5 điểm).
- **Chú thích mã nguồn rõ ràng:** Viết comment ngắn gọn giải thích logic xử lý ở từng khối lệnh quan trọng (+5 điểm).