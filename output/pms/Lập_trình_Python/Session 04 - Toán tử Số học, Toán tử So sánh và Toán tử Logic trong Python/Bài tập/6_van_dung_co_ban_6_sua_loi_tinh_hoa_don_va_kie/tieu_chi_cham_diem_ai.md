### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 6] Sửa lỗi tính hóa đơn và kiểm tra ưu đãi thẻ thành viên POS — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra được chính xác dòng tính toán `final_amount` bị sai thứ tự ưu tiên do thiếu ngoặc đơn và dòng kiểm tra `eligible_voucher` bị dùng sai toán tử logic.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Điền đầy đủ và chính xác dữ liệu cho Row 2 và Row 3 trong bảng Test Case (chỉ ra đúng kết quả thực tế bị lỗi và kết quả kỳ vọng chuẩn nghiệp vụ).

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Viết lại đúng công thức tính tổng tiền `final_amount = (base_price + num_toppings * 8000) * (1 - discount_rate)` hoặc biểu thức tương đương hợp lệ.
*   **[20 điểm] Xử lý điều kiện logic chuẩn:** Sửa thành công biểu thức điều kiện Voucher `eligible_voucher = (final_amount >= 100000) and (num_toppings >= 2)` sử dụng đúng toán tử `and`.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Ép kiểu thành công `int()` cho số tiền và số lượng topping, ép kiểu `bool` chuẩn qua biểu thức so sánh chuỗi.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Đảm bảo chương trình không bị lỗi runtime khi thực hiện các phép tính số thực với boolean.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích được tại sao trong Python toán tử `*` có độ ưu tiên cao hơn `+` và `-`, dẫn đến việc biểu thức không có ngoặc đơn bị tính toán sai thứ tự mong muốn.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Tên biến đặt chuẩn `snake_case`, thụt lề rõ ràng, comment giải thích bằng tiếng Việt có dấu.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Tối ưu hóa biểu thức toán tử:** Triển khai ngắn gọn biểu thức tính toán mà không cần tạo nhiều biến trung gian nhưng vẫn giữ nguyên độ đọc hiểu của mã nguồn.