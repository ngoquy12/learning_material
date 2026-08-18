### **Tiêu chí chấm điểm (AI)**
**Báo cáo Kiểm định Logic Phân loại Kho bãi — Tổng điểm: 100 điểm**

#### **1. Thiết lập & Khởi tạo (10 điểm)**
- **5 điểm:** Khai báo đúng và đầy đủ 7 biến đầu vào kiểu nguyên thủy (`userRole`, `itemCategory`, `packageWeightKg`, `storageTemperatureC`, `stockQuantity`, `minThreshold`, `isHazardous`) đúng kiểu dữ liệu yêu cầu.
- **5 điểm:** Khởi tạo tập tin `warehouse_logic.js` sạch sẽ, cấu trúc file rõ ràng, chạy trực tiếp trên Node.js hoặc Cursor IDE không phát sinh lỗi cú pháp.

#### **2. Logic nghiệp vụ (30 điểm)**
- **10 điểm:** Áp dụng đúng cấu trúc `switch-case` cho `userRole`, gán chính xác `roleTitle`, `canApprove` và có nhánh `default` xử lý các vai trò không hợp lệ.
- **10 điểm:** Sử dụng cấu trúc điều kiện `if / else if / else` kết hợp toán tử logic (`&&`, `||`, `!`) chính xác để phân bổ lô hàng vào đúng khu vực (`ZONE_HAZMAT`, `ZONE_COLD_STORAGE`, `ZONE_HEAVY_CARGO`, `ZONE_GENERAL_STORAGE`) và gán đúng `safetyMultiplier`.
- **10 điểm:** Áp dụng đúng toán tử ba ngôi (Ternary Operator) cho 3 quyết định: tính `heavySurcharge`, xác định `stockStatus` và gán cờ `approvalTag`.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ (30 điểm)**
- **15 điểm:** Kiểm tra toàn diện dữ liệu đầu vào (Validation): phát hiện chính xác trọng lượng `<= 0` hoặc `NaN`, số lượng tồn kho `< 0` hoặc `NaN`, ngưỡng tối thiểu `< 0` hoặc `NaN`.
- **15 điểm:** Xử lý ngắt luồng điều khiển chuẩn xác khi gặp dữ liệu lỗi (in thông báo cảnh báo rõ ràng và không tính toán các bước phía sau).

#### **4. Tối ưu hoá hiệu suất (20 điểm)**
- **10 điểm:** Áp dụng nguyên lý ngắn mạch (Short-circuit evaluation) hợp lý trong điều kiện kiểm tra, tránh các phép so sánh dư thừa.
- **10 điểm:** Thực hiện tính toán chi phí chính xác theo công thức quy định, gán giá trị biến hợp lý mà không tạo ra các biến trung gian dư thừa.

#### **5. Chất lượng mã nguồn (10 điểm)**
- **5 điểm:** Đặt tên biến theo quy tắc `camelCase` chuẩn JavaScript, rõ nghĩa (ví dụ: `packageWeightKg`, `safetyMultiplier`, `heavySurcharge`).
- **5 điểm:** Định dạng đầu ra Console chuyên nghiệp, sử dụng Template Literals đầy đủ, dễ đọc và định dạng dấu phân cách phần ngàn cho tiền tệ (hoặc trình bày chỉn chu).

#### **Điểm cộng (5-10 điểm)**
- **+5 điểm:** Áp dụng `toLocaleString('vi-VN')` để định dạng tiền tệ VNĐ chuyên nghiệp trong Template Literals (ví dụ: `1,482,500 VNĐ`).
- **+5 điểm:** Mã nguồn có ghi chú (comments) giải thích rõ ràng luồng tư duy logic và các ràng buộc nghiệp vụ ở từng khối lệnh.