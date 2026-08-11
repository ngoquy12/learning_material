### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 1] Sửa lỗi menu điều hướng đơn hàng thương mại điện tử — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ rõ dòng mã nguồn so sánh `choice == 1` trong khi `choice` là kiểu `str` còn `1` là kiểu `int`, dẫn đến phép so sánh luôn trả về `False`.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Cung cấp đủ 3 test case theo chuẩn bảng HTML (Input, Buggy Output, Expected Output), mô tả chính xác phản ứng của chương trình trước và sau khi sửa lỗi.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Ép kiểu thành công `choice_int = int(choice_raw)` hoặc thực hiện so sánh chuỗi `choice_raw == "1"` giúp các phím menu `1`, `2`, `3`, `0` hoạt động chính xác.
*   **[20 điểm] Xử lý ngoại lệ chuẩn ngôn ngữ:** Sử dụng khối `try-except ValueError` bọc việc ép kiểu số nguyên để trả về thông báo lỗi an toàn khi người dùng nhập dữ liệu không hợp lệ.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Xử lý các khoảng trắng thừa bằng `.strip()` và kiểm tra trường hợp đầu vào rỗng.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Đảm bảo toàn bộ luồng chương trình xử lý mượt mà, trả về thông báo chuẩn `[LỖI] ...` mà không để phát sinh ngoại lệ không được kiểm soát out out khỏi Terminal.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích được vì sao hàm `input()` trong Python luôn trả về kiểu `str` và sự nguy hiểm khi so sánh trực tiếp kiểu chuỗi với kiểu số nguyên trong hệ thống giao dịch E-Commerce.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến/hàm theo chuẩn `snake_case`, sử dụng đầy đủ Type Hints (`str`, `float`, `None`, `int | str`), mã nguồn thụt lề 4 khoảng trắng đúng PEP 8.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định (`[Tên Lớp]_[Môn Học]_Session06_Ex01`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Viết thêm các câu lệnh `assert` hoặc file kiểm thử tự động xác nhận hàm `process_order_menu` hoạt động đúng cho tất cả các trường hợp đầu vào (`"1"`, `"0"`, `"abc"`, `""`).