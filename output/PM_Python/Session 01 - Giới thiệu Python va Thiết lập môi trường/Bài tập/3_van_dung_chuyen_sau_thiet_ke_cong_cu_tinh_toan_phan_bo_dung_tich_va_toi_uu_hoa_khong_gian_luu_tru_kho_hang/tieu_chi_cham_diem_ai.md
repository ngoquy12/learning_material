### **Tiêu chí chấm điểm (AI)**
**[Vận dụng chuyên sâu] Thiết kế công cụ tính toán phân bổ dung tích và tối ưu hóa không gian lưu trữ kho hàng — Tổng điểm: 100 điểm**

#### **1. Báo cáo phân tích và Thiết kế giải pháp — 20 điểm**
*   **[10 điểm] Xác định cấu trúc I/O:** Xác định rõ ràng danh sách 6 biến số đầu vào (tên biến tiếng Anh khoa học, kiểu dữ liệu sau khi ép kiểu là `float`) và danh sách các biến đầu ra cùng đơn vị đo lường tương ứng.
*   **[10 điểm] Mô tả giải thuật xử lý nghiệp vụ:** Viết mã giả (Pseudocode) thể hiện rõ ràng luồng xử lý tuần tự từ trên xuống dưới, thể hiện đầy đủ các bước tính toán hệ số hao hụt không gian và chuyển đổi kiểu dữ liệu trước khi xuất báo cáo.

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM:** Thực hiện khai báo đầy đủ các biến lưu trữ giá trị nhập từ bàn phím bằng hàm `input()`. Khai báo chính xác các biến hằng số nghiệp vụ (tỷ lệ không gian khả dụng, đơn giá thuê, tỷ lệ chi phí vận hành).
*   **[15 điểm] Logic tính toán tích hợp:** Hiện thực hóa chính xác toàn bộ các công thức tính toán thể tích kho thô, thể tích hữu dụng, thể tích pallet, số lượng pallet tối đa (phải dùng chia lấy nguyên `//` hoặc ép kiểu `int`) và ước tính tài chính (doanh thu, chi phí, lợi nhuận) chạy trơn tru không có lỗi logic.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Thực thi chia lấy nguyên:** Tránh trường hợp phân bổ tràn không gian bằng việc xử lý cắt bỏ phần dư lẻ của pallet (ví dụ: kho chứa tối đa 2904.16 pallet thì kết quả đầu ra phải là số nguyên 2904).
*   **[15 điểm] Định dạng dữ liệu đầu ra chuyên nghiệp:** Sử dụng triệt để f-string với các cú pháp định dạng chuỗi để ép hiển thị đúng 2 chữ số thập phân cho kích thước/thể tích (`:.2f`) và ép số nguyên cho doanh số/số lượng pallet (`:.0f` hoặc `int()`).

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Gợi ý nhập liệu trực quan:** Viết câu lệnh `input()` chứa thông điệp hướng dẫn rõ ràng kèm theo đơn vị đo (ví dụ: "Nhập chiều dài kho hàng (m): ") để giảm thiểu lỗi nhập sai kiểu dữ liệu của người dùng.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Các biến được đặt tên hoàn toàn bằng tiếng Anh chuẩn ngành WMS (như `warehouse_length`, `usable_volume`, `pallet_capacity`...), không viết tắt tùy tiện hoặc dùng ngôn ngữ pha trộn.
*   **[5 điểm] Nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy chuẩn: `[Tên Lớp]_[Môn Học]_Session01_Ex03`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Kỹ năng tự học nâng cao:** Sử dụng thành công định dạng f-string hiển thị dấu phân cách hàng nghìn (ví dụ: `3,920,625,000 VND`) đối với các trường tài chính để tăng tính trực quan của báo cáo doanh nghiệp.