### **Tiêu chí chấm điểm (AI)**
**[Khắc phục lỗi tính phí vận chuyển đơn hàng] — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra các dòng code gây lỗi ép kiểu (dòng 11), lỗi thứ tự logic câu điều kiện (dòng 19 - 22), và thiếu validate (dòng 8-9).
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Thiếu lập đúng bảng HTML/Markdown 3 test cases chỉ ra chính xác Input đầu vào (không hợp lệ, nặng trên 30kg, quãng đường âm) và lỗi thực tế (Crash chương trình hoặc ra sai số tiền).

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** 
    *   Sắp xếp lại cấu trúc điều kiện `if-elif` hợp lý (kiểm tra điều kiện `trong_luong > 30` trước `trong_luong > 10`).
    *   Tính chính xác công thức phụ thu cho các phân khúc trọng lượng.
*   **[20 điểm] Giả lập mã phản hồi lỗi nghiệp vụ:**
    *   Khi dữ liệu sai quy định, in ra đúng thông điệp lỗi dạng từ điển/JSON giả lập có chứa `"status_code": 400` và thông điệp cảnh báo thích hợp.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:**
    *   Kiểm tra thành công tiền tố `"LGT-"` bằng phương thức `.startswith()` hoặc cắt chuỗi.
    *   Kiểm tra độ dài mã đơn hàng tối thiểu 8 ký tự.
*   **[10 điểm] Bắt lỗi nhập liệu không phải số:**
    *   Có giải pháp kiểm tra chuỗi nhập vào có phải số thực dương hay không bằng kỹ thuật xử lý chuỗi đơn giản trước khi ép kiểu để tránh lỗi runtime ValueError.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** 
    *   Giải thích rõ cơ chế hoạt động của hàm `input()` luôn trả về kiểu `str`.
    *   Trình bày phương pháp kiểm tra số thực bằng cách xử lý dấu chấm thập phân `.replace('.', '', 1).isdigit()` hoặc cách thức tương đương phù hợp với kiến thức cơ bản.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Định dạng biến rõ ràng (snake_case), sử dụng f-string chuyên nghiệp để hiển thị kết quả, thụt lề chuẩn PEP 8.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub Repo đúng cấu trúc thư mục quy định (`[Tên Lớp]_PythonCore_Session01_Ex01`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Tối ưu hóa giao diện hiển thị:** Trang trí định dạng hóa đơn console bắt mắt, chuyên nghiệp và có phân tách dấu phẩy hàng nghìn cho tiền tệ (VND) (ví dụ: `150,000` thay vì `150000`).