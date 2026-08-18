### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 1] Sửa lỗi tính phụ thu check-in sớm hệ thống đặt phòng — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra chính xác dòng code chứa biểu thức tính `total_payment` bị sai thứ tự đóng mở ngoặc làm sai lệch giá trị.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thành đầy đủ các ô còn trống (`...`) trong bảng Test Case với các giá trị Buggy Output, Expected Output và Logic Note chính xác 100%.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sửa biểu thức tính toán phụ thu và tổng tiền thanh toán cho ra kết quả chính xác trong mọi trường hợp (`has_early_checkin` là 0 hoặc 1).
*   **[20 điểm] Xử lý ngoại lệ chuẩn ngôn ngữ:** Sử dụng đúng các kiểu dữ liệu `float` và `int`, thực hiện phép tính số học chính xác không làm mất phần thập phân của tiền tệ.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Kiểm tra và đảm bảo các biến đầu vào không bị âm (giá phòng > 0, số đêm > 0).
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Đảm bảo biến cờ `has_early_checkin` chỉ nhận giá trị nhị phân `0` hoặc `1` để tránh làm sai lệch phép nhân số học.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích được vì sao thứ tự ưu tiên toán tử trong Python (ngoặc `()` -> nhân/chia `* /` -> cộng/trừ `+ -`) lại gây ra lỗi nghiêm trọng trong các hệ thống tính toán tài chính nếu lập trình viên không bao ngoặc rõ ràng.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến chuẩn `snake_case`, sử dụng Type Hints đầy đủ (`room_price_per_night: float`, `nights_count: int`), chú thích bằng tiếng Việt có dấu trung thực.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục yêu cầu `[Tên Lớp]_[Môn Học]_SessionSession 04_Ex1`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Viết thêm đoạn mã kiểm thử độc lập tính toán lại 3 kịch bản kiểm thử trong bảng báo cáo mà không dùng câu lệnh rẽ nhánh.