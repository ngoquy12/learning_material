# **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 3] Sửa lỗi cập nhật và xóa cước phí chuyến đi GrabRide — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra đúng dòng mã nguồn thực hiện sai thứ tự thao tác dẫn đến việc dồn chỉ số (index shift).
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Điền hoàn chỉnh 2 dòng test case còn thiếu (STT 2 và STT 3) trong bảng báo cáo kiểm thử với đầy đủ kết quả thực tế, kết quả kỳ vọng và giải thích nguyên nhân.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sửa đổi mã nguồn đảm bảo chuyến đi tại chỉ số 2 được cập nhật đúng thành `50000` VNĐ và chuyến đi tại chỉ số 1 bị xóa thành công.
*   **[20 điểm] Thứ tự thao tác tối ưu:** Thay đổi thứ tự thực hiện (Cập nhật trước khi Xóa, hoặc tính toán lại chỉ số sau khi Xóa) để danh sách đầu ra đạt kết quả chuẩn xác.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Kiểm tra độ dài danh sách trước khi truy cập index:** Đảm bảo danh sách có đủ số lượng phần tử trước khi thực hiện cập nhật hoặc xóa để tránh lỗi `IndexError`.
*   **[10 điểm] Sử dụng đúng cú pháp được phép:** Tuân thủ đúng các thao tác đã học (`list[index] = value`, `del list[index]`, `len()`), không sử dụng các phương thức cấm (`append`, `pop`, `dict`, `set`, `tuple`, `def`, `class`).

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích ngắn gọn tại sao thao tác `del` trên danh sách động (`list`) lại làm thay đổi vị trí chỉ số của các phần tử đứng đằng sau nó.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Tuân thủ chuẩn PEP 8, 4 khoảng trắng thụt lề, đặt tên biến rõ ràng theo `snake_case`, có đầy đủ Type Hints (`list[int]`).
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định (`[Tên Lớp]_[Môn Học]_Session10_Ex3`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] In thông điệp trực quan:** Bổ sung các câu lệnh `print` chi tiết mô tả rõ trạng thái của danh sách qua từng bước xử lý (trước khi điều chỉnh, sau khi cập nhật, và sau khi xóa).
