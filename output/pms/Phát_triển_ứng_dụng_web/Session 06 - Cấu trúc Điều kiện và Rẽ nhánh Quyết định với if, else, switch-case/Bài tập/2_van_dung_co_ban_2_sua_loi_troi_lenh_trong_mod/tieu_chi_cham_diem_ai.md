# **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 2] Sửa lỗi trôi lệnh trong module tính phí hành lý ký gửi — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
* **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ rõ vị trí dòng code thiếu câu lệnh `break;` trong trường hợp `case "Business"`.
* **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thiện 2 dòng còn lại trong bảng Test Case với đầy đủ thông tin Input, Buggy Output, Expected Output và giải thích nguyên nhân.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
* **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Khắc phục hoàn toàn lỗi trôi lệnh (fall-through), bổ sung đầy đủ lệnh `break;` cho tất cả các nhánh trong `switch-case`.
* **[20 điểm] Tính toán chính xác cước phí quá cước:** Áp dụng đúng biểu thức toán tử ba ngôi để tính `excessWeight` và `excessFee` đúng quy định (50.000 VNĐ/kg quá cước).

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
* **[10 điểm] Validate định dạng đầu vào cơ bản:** Kiểm tra thành công điều kiện trọng lượng `actualWeight` phải là kiểu số (`typeof actualWeight === "number"`) và lớn hơn hoặc bằng 0. Trả về đúng thông báo `"Trọng lượng hành lý không hợp lệ"`.
* **[10 điểm] Bắt lỗi an toàn hệ thống:** Xử lý nhánh `default` chính xác khi gặp hạng vé nằm ngoài danh mục `Business`, `Deluxe`, `Eco`.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
* **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích được cơ chế hoạt động của hành vi fall-through trong `switch-case` của JavaScript và lý do tại sao thiếu `break;` lại tạo ra sai sót nghiệp vụ nghiêm trọng.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
* **[5 điểm] Định dạng mã nguồn sạch:** Mã nguồn viết bằng ES6+, sử dụng `const`/`let` đúng mục đích, tên biến tiếng Anh chuẩn Clean Code, thụt lề 2 spaces rõ ràng.
* **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên repository tuân thủ chính xác cấu trúc thư mục `[Tên Lớp]_[Môn Học]_SessionSession 06_Ex2`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
* **[10 điểm] Viết bộ kiểm thử tự động (Test Runner):** Tạo hàm chạy thử tự động gọi `calculateBaggageFee` với nhiều bộ dữ liệu biên và in ra nhãn PASS/FAIL trực quan trên console.
