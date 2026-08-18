### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 6] Sửa lỗi tính tổng thanh toán hóa đơn đặt phòng — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra đúng dòng code trong hàm thực hiện nhân giảm giá lên toàn bộ tổng tiền thay vì chỉ áp dụng cho tiền phòng cơ bản.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thiện 2 dòng còn thiếu (STT 2 và STT 3) trong bảng Test Case với đầy đủ thông tin: Input, Buggy Output, Expected Output, Failing Line và Logic Note.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sửa lại công thức tính tổng thanh toán theo đúng chính sách: `total_payment = base_cost - (base_cost * 0.10 * is_member) + early_surcharge + cleaning_fee`.
*   **[20 điểm] Tuân thủ phạm vi kiến thức:** Không sử dụng các từ khóa bị cấm (`if`, `else`, `and`, `or`, `not`, `for`, `while`, `list`, `dict`), xử lý tính toán dựa trên toán tử số học và tính chất tính toán của kiểu Boolean trong Python.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Chuẩn hóa kiểu dữ liệu:** Đảm bảo tất cả các tham số truyền vào và giá trị trả về tuân thủ đúng Type Hints (`float`, `int`, `bool`).
*   **[10 điểm] Xử lý số thực chính xác:** Kết quả trả về là kiểu `float` chính xác, không bị lỗi làm tròn hoặc tràn số.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Phân tích tác động nghiệp vụ:** Giải thích được hậu quả thực tế của lỗi logic này trong hệ thống tài chính/đặt phòng (gây thất thoát doanh thu khi khách đặt nhiều dịch vụ kèm theo).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến rõ ràng theo quy chuẩn `snake_case`, chú thích code bằng tiếng Việt có dấu chuẩn sản xuất, tuân thủ PEP 8.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub theo đúng cấu trúc thư mục quy định.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết kiểm thử tự động (Assertion):** Tự bổ sung các câu lệnh `assert` kiểm tra kết quả trả về của hàm với các bộ dữ liệu thử nghiệm khác nhau.