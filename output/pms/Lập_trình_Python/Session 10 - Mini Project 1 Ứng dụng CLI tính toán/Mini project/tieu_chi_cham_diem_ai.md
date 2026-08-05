### **Tiêu chí chấm điểm (AI)**
**[Mini Project 1: Ứng dụng Máy tính Cá nhân CLI] — Tổng điểm: 100 điểm**

---

#### **1. Thiết lập cấu trúc và Khởi tạo — 20 điểm**
* **Khởi tạo và Duy trì vòng lặp CLI (10 điểm):**
  * Khởi tạo thành công vòng lặp chính `while` để giữ chương trình chạy liên tục cho đến khi người chọn dừng (`0`).
  * In giao diện Menu chọn chức năng đầy đủ các mục (1-7 và 0).
* **Tuân thủ giới hạn kiến thức (10 điểm):**
  * Mã nguồn viết dạng chương trình phẳng (flat code logic).
  * TUYỆT ĐỐI KHÔNG sử dụng `def` (hàm), không tạo `class`, không khai báo `list`/`dict`/`tuple`/`set`, không đọc/ghi tập tin `open()`.

---

#### **2. Logic nghiệp vụ cốt lõi — 30 điểm**
* **Thực hiện phép tính cơ bản (15 điểm):**
  * Tính đúng kết quả các phép tính: Cộng (`+`), Trừ (`-`), Nhân (`*`), Chia (`/`), Chia lấy dư (`%`), Lũy thừa (`**`).
* **Quản lý biến bộ nhớ (15 điểm):**
  * Khai báo biến `previous_result` để lưu trữ kết quả tính toán gần nhất.
  * Xử lý đúng logic hỏi người dùng có tiếp tục lấy kết quả cũ làm số hạng đầu tiên ($a$) hay nhập số mới.
  * Chức năng Reset bộ nhớ đưa `previous_result` về lại `None` hoạt động chuẩn xác.

---

#### **3. Kiểm chuẩn dữ liệu và Xử lý ngoại lệ — 30 điểm**
* **Xử lý lỗi ép kiểu dữ liệu (15 điểm):**
  * Bắt thành công ngoại lệ `ValueError` khi người dùng nhập chuỗi ký tự thay vì số vào `input()`. In thông báo lỗi rõ ràng và yêu cầu nhập lại.
* **Xử lý lỗi tính toán số học (10 điểm):**
  * Bắt thành công ngoại lệ `ZeroDivisionError` khi người dùng thực hiện phép chia hoặc chia lấy dư với số chia bằng `0`.
* **Kiểm soát lựa chọn menu (5 điểm):**
  * Xử lý chính xác trường hợp người dùng nhập lựa chọn chức năng không nằm trong danh mục (ví dụ: nhập số `-1`, `99` hoặc ký tự chữ).

---

#### **4. Chức năng nâng cao hoặc Kiểm thử tự động — 10 điểm**
* **Trải nghiệm người dùng tương tác CLI (10 điểm):**
  * Phân biệt rõ ràng giữa phép chia số thực (trả về kết quả `float`) và phép chia lấy dư (yêu cầu số nguyên `int`).
  * Trình bày biểu thức tính toán hoàn chỉnh ra Console sau khi thực hiện xong (ví dụ: `Đã tính: 15.0 + 5.0 = 20.0`).

---

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
* **Đặt tên biến Tiếng Anh chuẩn `snake_case` (5 điểm):**
  * Tất cả các biến số (`first_number`, `second_number`, `user_choice`, `previous_result`, `is_running`...) đều tuân thủ 100% Tiếng Anh chuẩn `snake_case`, không dùng tiếng Việt không dấu hoặc từ viết tắt khó hiểu.
* **Quy chuẩn Repository GitHub (5 điểm):**
  * Nộp đúng định dạng đường dẫn GitHub repository.
  * Có đầy đủ file `main.py` hoạt động ổn định và file `README.md` mô tả dự án.

---

#### **Điểm cộng khuyến khích (Bonus) — 5 đến 10 điểm**
* **Đếm số lượng phép tính (5 điểm):**
  * Khởi tạo biến `calculation_count` đếm và hiển thị tổng số phép tính đã thực hiện thành công trong suốt phiên làm việc của người dùng.
* **Định dạng kết quả đẹp mắt (5 điểm):**
  * Làm tròn số thực hợp lý (dùng `round(result, 4)`) đối với các kết quả phép chia bị lẻ thập phân kéo dài.