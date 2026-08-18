### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 1] Sửa lỗi tính phí hành lý quá cước tại quầy check-in — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra đúng dòng lệnh kiểm tra điều kiện `else if (baggageWeight > 7)` đặt sai thứ tự ưu tiên logic.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Điền hoàn chỉnh bảng Test Case với ít nhất 3 kịch bản kiểm thử (bao gồm các mốc 5kg, 25kg, 40kg) phản ánh chính xác sự khác biệt giữa Buggy Output và Expected Output.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Điều chỉnh lại chuỗi điều kiện `if / else if` theo đúng thứ tự (kiểm tra từ mốc cao nhất xuống mốc thấp nhất hoặc sử dụng điều kiện khoảng cách hợp lý `> 7 && <= 20`).
*   **[20 điểm] Tính toán chính xác công thức quá cước:** Áp dụng đúng công thức tính phí phát sinh cho hành lý trên 35 kg ($500.000 + (baggageWeight - 35) \times 50.000$).

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Kiểm tra và loại bỏ các giá trị trọng lượng âm (`baggageWeight < 0`).
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Xử lý trường hợp dữ liệu đầu vào bị rỗng, `null`, `undefined` hoặc không phải kiểu số (`isNaN`).

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích ngắn gọn tại sao việc sắp xếp thứ tự biểu thức điều kiện trong cấu trúc `if - else if` lại quan trọng và nêu bẫy lập trình "điều kiện bao quát đặt lên trước điều kiện chi tiết".

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Mã nguồn viết bằng JavaScript ES6+ chuẩn mực, căn lề 2 spaces, khai báo hằng số `const`/`let` phù hợp, tên biến chuẩn tiếng Anh (`baggageWeight`, `excessFee`).
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Nộp bài đúng cấu trúc thư mục quy định `[Tên Lớp]_[Môn Học]_SessionSession 06_Ex1` trên GitHub.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động đơn giản:** Viết một hàm JavaScript hỗ trợ tự động chạy kiểm thử danh sách mốc hành lý đầu vào và in kết quả PASSED/FAILED ra terminal console.