### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 2] Sửa lỗi logic tính hóa đơn giảm giá thẻ thành viên Highlands POS — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra đúng dòng mã lệnh tính toán `final_price` trong mã nguồn legacy bị sai phạm vi nhân tỷ lệ giảm giá (dùng `base_price` thay vì `subtotal`).
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Điền chính xác và đầy đủ các giá trị Buggy Output, Expected Output và Ghi chú cho cả 2 test case còn lại trong bảng báo cáo kiểm thử.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sửa biểu thức tính `final_price` thành công, kết quả trả về chính xác số tiền cần thanh toán sau khi trừ 10% `subtotal` nếu là thành viên Vàng (ví dụ: `final_price = subtotal - subtotal * 0.1 * is_gold_member` hoặc `subtotal * (1 - 0.1 * is_gold_member)`).
*   **[20 điểm] Tuân thủ phạm vi kiến thức cho phép:** Tuyệt đối không dùng câu lệnh rẽ nhánh `if/else/elif`, không dùng hàm `def`, vòng lặp hay thư viện ngoài. Sử dụng thuần thục toán tử số học và ép kiểu/ép giá trị logic.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Ép kiểu chính xác dữ liệu nhập từ bàn phím (`float` cho số tiền, `int` cho số lượng topping, `bool` qua so sánh chuỗi `== "True"`).
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Đảm bảo khi người dùng nhập `is_gold_input` khác `"True"` (ví dụ: `"False"`, `"no"`), chương trình vẫn chạy an toàn và hiểu là không giảm giá mà không gây crash ứng dụng.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích được cơ chế ép kiểu ẩn (implicit type conversion) của Python khi sử dụng biến `bool` (`True` tương đương 1, `False` tương đương 0) trong biểu thức số học.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Tuân thủ chuẩn PEP 8 (thụt lề 4 dấu cách, tên biến dạng `snake_case` bằng tiếng Anh, chú thích mã nguồn bằng tiếng Việt rõ ràng).
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub repository đúng cấu trúc thư mục quy định: `[Tên Lớp]_[Môn Học]_Session 04_Ex2`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Hiển thị số tiền giảm giá chi tiết:** Viết thêm biểu thức tính toán độc lập số tiền khách được giảm `discount_amount = subtotal * 0.1 * is_gold_member` và in ra màn hình mà không dùng câu lệnh `if/else`.