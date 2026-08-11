### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 2] Xử lý lỗi hệ thống Menu điều khiển đơn hàng thương mại điện tử — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ rõ vị trí mã legacy thiếu kiểm tra `action` ngoài phạm vi (0-3), thiếu validation `discount_percent` (0-100%), và thiếu kiểm tra `order_total > 0`.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Bảng báo cáo kiểm thử trình bày tối thiểu 3 kịch bản đầy đủ 5 cột (STT, Mô tả kịch bản, Input, Buggy Output, Expected Output) đúng định dạng HTML quy định.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sửa triệt để lỗi làm âm giá trị đơn hàng, tính đúng phí giao hàng và giảm giá theo phần trăm hợp lệ.
*   **[20 điểm] Xử lý ngoại lệ chuẩn ngôn ngữ:** Sử dụng câu lệnh `raise ValueError` với thông báo lỗi tiếng Việt rõ ràng cho từng trường hợp vi phạm quy tắc.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Kiểm tra loại thao tác menu `action` phải thuộc tập hợp `{0, 1, 2, 3}`.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Hàm `batch_process_menu` xử lý ngoại lệ an toàn bằng khối `try...except ValueError`, in ra thông báo lỗi chi tiết mà không làm sập chương trình.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích được vì sao việc cho phép dữ liệu giảm giá âm hoặc vượt 100% lại gây thiệt hại tài chính nặng nề trong hệ thống e-commerce thực tế và đề xuất hướng phòng ngừa tại layer Input Validation.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Mã nguồn viết đúng chuẩn PEP 8, khai báo Type Hints chuẩn Python 3.10+ (`int | float`), tuyệt đối không chứa các từ khóa/vòng lặp bị cấm (`while`, `break`, `continue`).
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub repository đúng cấu trúc tên thư mục quy định `[Tên Lớp]_[Môn Học]_Session06_Ex02`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Viết thêm các hàm kiểm thử tự động (sử dụng `pytest` hoặc `unittest`) để tự động kiểm tra các trường hợp `ValueError` khi truyền dữ liệu sai.