# Bộ câu hỏi tự luận kiểm tra bài đọc (Reading Comprehension Essay Questions)

### Câu 1: Dựa vào bối cảnh hệ thống tự động hóa thẩm định hồ sơ vay tại RikkeiBank, hãy phân tích nguyên nhân tạo ra hiện tượng "Arrow Anti-pattern" trong mã nguồn ban đầu. Việc lồng liên tiếp các câu lệnh kiểm tra biến `age`, `income` và `credit_score` gây ra những khó khăn và nguy cơ gì cho hệ thống vận hành?
> **Gợi ý trả lời & Định hướng đáp án:** Đánh giá khả năng hiểu bối cảnh doanh nghiệp và điểm nghẽn vận hành (Operational Pain Point):
- Nguyên nhân: Đội ngũ phát triển lồng nhiều câu lệnh rẽ nhánh liên tiếp (`if age >= 18:` -> `if income >= 15:` -> `if credit_score >= 650:`), khiến mã nguồn bị thụt lùi sâu vào bên trong theo dạng hình mũi tên.
- Tác hại/Rủi ro: Làm mã nguồn trở nên cực kỳ phức tạp và khó đọc, gia tăng rủi ro bỏ sót logic kiểm định trong quá trình bảo trì, đồng thời vi phạm nghiêm trọng chuẩn định dạng PEP 8 của Python.

---

### Câu 2: Để khắc phục mã nguồn cũ của RikkeiBank, phương pháp "Phẳng hóa điều kiện" (Condition Flattening) đã được áp dụng như thế nào? Trình bày đoạn mã điều kiện tối ưu kiểm tra đồng thời ba biến `age`, `income`, `credit_score` và phân tích quy chuẩn khoảng trắng toán tử, thụt lề theo tiêu chuẩn PEP 8.
> **Gợi ý trả lời & Định hướng đáp án:** Đánh giá kiến thức tái cấu trúc mã nguồn (Refactoring) và chuẩn PEP 8:
- Giải pháp: Kết hợp cả 3 điều kiện thẩm định độc lập trên cùng một cấp độ bằng cách sử dụng toán tử logic `and`.
- Đoạn mã tối ưu:
  `if age >= 18 and income >= 15 and credit_score >= 650:`
      `# Phê duyệt hồ sơ`
- Phân tích chuẩn PEP 8:
  + Thụt lề (Indentation): Sử dụng đúng 4 khoảng trắng (spaces) cho khối lệnh xử lý bên trong `if`, loại bỏ các cấp thụt lề thừa.
  + Khoảng trắng toán tử: Đặt đúng 1 khoảng trắng đơn trước và sau các toán tử so sánh (`>=`) và toán tử logic (`and`) để tăng tính dễ đọc.

---

### Câu 3: Dựa vào sơ đồ quy trình xét duyệt tín dụng (Mermaid Diagram) trong bài đọc, hãy phân tích luồng thực thi và xác định thông báo phản hồi chính xác của hệ thống RikkeiBank cho 2 trường hợp hồ sơ sau:
- Hồ sơ A: `age` = 17, `income` = 25 (triệu VNĐ), `credit_score` = 720.
- Hồ sơ B: `age` = 30, `income` = 12 (triệu VNĐ), `credit_score` = 690.
> **Gợi ý trả lời & Định hướng đáp án:** Đánh giá khả năng đọc hiểu sơ đồ luồng điều khiển và logic rẽ nhánh:
- Hồ sơ A:
  + Kiểm tra điều kiện 1: `18 <= age <= 65`. Vì `age` = 17 (< 18), luồng điều khiển rẽ sang nhánh 'Không'.
  + Kết quả phản hồi: Hệ thống trả về thông báo "Từ chối: Không đủ tuổi".
- Hồ sơ B:
  + Kiểm tra điều kiện 1: `18 <= age <= 65` (`age` = 30) -> Thỏa mãn, rẽ sang nhánh 'Có'.
  + Kiểm tra điều kiện 2: `income >= 15` VÀ `credit_score >= 650`. Mặc dù `credit_score` = 690 (>= 650) nhưng `income` = 12 (< 15 triệu), khiến điều kiện kết hợp toán tử VÀ bị sai.
  + Kết quả phản hồi: Hệ thống trả về thông báo "Từ chối: Tiêu chí tài chính không đạt".

---

### Câu 4: Trích dẫn bảng quy chuẩn định dạng PEP 8 trong bài đọc, hãy cho biết quy định kỹ thuật cụ thể đối với việc dùng phím Tab, khoảng trắng và độ sâu rẽ nhánh lồng nhau tối đa. Việc trộn lẫn Tab và Space hoặc lồng vượt quá 2 cấp rẽ nhánh sẽ gây ra hậu quả gì?
> **Gợi ý trả lời & Định hướng đáp án:** Đánh giá khả năng ghi nhớ bẫy lỗi (Gotcha) và quy chuẩn kỹ thuật PEP 8:
- Quy định kỹ thuật PEP 8 trong bài:
  + Thụt lề: Bắt buộc dùng 4 khoảng trắng (Spaces) cho mỗi cấp. Tuyệt đối không dùng phím Tab hoặc trộn lẫn Tab và Space.
  + Độ sâu rẽ nhánh: Khuyên dùng tối đa 1 - 2 cấp lồng nhau.
- Hậu quả vi phạm:
  + Việc trộn lẫn Tab và Space sẽ làm mất tính nhất quán của mã nguồn trên các trình biên dịch/hệ điều hành khác nhau, dễ phát sinh lỗi cú pháp (IndentationError).
  + Việc lồng quá 2 cấp rẽ nhánh làm tái diễn lỗi Arrow Anti-pattern, khiến mã bị thụt lùi sâu, rất khó đọc và khó bảo trì.

---