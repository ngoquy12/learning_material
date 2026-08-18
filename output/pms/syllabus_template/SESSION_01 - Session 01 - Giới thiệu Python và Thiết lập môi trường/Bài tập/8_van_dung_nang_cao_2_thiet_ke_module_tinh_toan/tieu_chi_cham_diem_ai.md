### **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 2] Thiết kế Module Tính toán và Xuất Hóa đơn POS Phức hợp tại Highlands Coffee — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:** X định chính xác toàn bộ danh sách biến Input (tối thiểu 9 thông số: tên món, giá gốc, phụ thu size, số lượng topping, giá topping, số lượng ly, tỷ lệ giảm giá, tỷ lệ VAT, tiền khách đưa) và biến Output (đơn giá ly, subtotal, tiền giảm, VAT, tổng thanh toán, tiền thừa) kèm kiểu dữ liệu (`str`, `int`, `float`) tương ứng.
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:** Trình bày rõ ràng các bước tính toán logic theo đúng thứ tự tài chính. Vẽ sơ đồ Mermaid Flowchart hợp lệ, tuân thủ đúng 5 dạng hình chuẩn kỹ thuật (đặc biệt: dùng hình chữ nhật cho bước tính toán, hình bình hành cho thao tác `input`/`print`).

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Schema:** Khai báo biến minh bạch, sử dụng tên tiếng Anh theo chuẩn CamelCase hoặc snake_case (`item_name`, `base_price`, `size_surcharge`, `topping_count`, ...). Thực hiện ép kiểu dữ liệu `int()` và `float()` chính xác từ kết quả hàm `input()`.
*   **[15 điểm] Hàm/Module xử lý nghiệp vụ tích hợp:** Tính toán chính xác tuyệt đối 7 chỉ số tài chính nghiệp vụ (đơn giá ly, subtotal, tiền giảm giá, tiền sau giảm, tiền VAT, tổng hóa đơn, tiền thừa) theo đúng công thức đã quy định.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy dữ liệu vượt ngưỡng / Tiền thiếu:** Đảm bảo thứ tự trừ tiền chính xác (Tiền thừa = Tiền khách đưa - Tổng chi trả). Phân tích trường hợp biên nếu tiền khách đưa nhỏ hơn tổng chi trả (kết quả ra số âm thể hiện số tiền khách còn thiếu).
*   **[15 điểm] Validate dữ liệu đầu vào nâng cao:** Chuyển đổi dữ liệu chuỗi nhập từ CLI sang đúng kiểu số (`int` cho số lượng ly/topping, `float` cho giá tiền và tỷ lệ phần trăm) mà không bị lỗi xung đột kiểu dữ liệu (`TypeError`).

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Định dạng đầu ra Hóa đơn chuyên nghiệp:** Sử dụng f-string để thiết kế giao diện hóa đơn CLI đẹp mắt, có tiêu đề cửa hàng, các đường viền phân cách (`=`, `-`), hiển thị từng mục tiền minh bạch, rõ ràng và căn lề ngay ngắn.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Mã nguồn sạch sẽ, không dùng từ khóa bị cấm, tên biến 100% bằng Tiếng Anh, có chú thích giải thích logic bằng Tiếng Việt có dấu đầy đủ.
*   **[5 điểm] Nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định `[Tên Lớp]_[Môn Học]_SessionSESSION_01_Ex8`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ & Căn chỉnh lề nâng cao:** Tối ưu hóa chuỗi tính toán không dùng biến trung gian dư thừa và áp dụng ký tự căn lề f-string nâng cao (như `{var:>15}` hoặc `{var:<20}`) để tạo bảng hóa đơn đẹp như máy in nhiệt thực tế.