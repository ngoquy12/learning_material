# Bộ câu hỏi Khảo thí & Đánh giá năng lực: Toán tử logic

### Câu 1: Cơ chế đánh giá ngắn mạch (Short-circuit) hoạt động thế nào với toán tử and?

**Gợi ý trả lời & Hướng dẫn tự học:**
Với toán tử and, nếu vế bên trái trả về False, Python lập tức kết luận toàn bộ biểu thức là False và không thực thi vế bên phải nữa. Điều này giúp ngăn ngừa các lỗi runtime như chia cho 0 hoặc truy cập thuộc tính của đối tượng None ở vế phải.

---

### Câu 2: Mô tả thứ tự thực thi của biểu thức logic: not A or B and C.

**Gợi ý trả lời & Hướng dẫn tự học:**
Thứ tự thực thi như sau: Phép phủ định `not A` chạy đầu tiên. Tiếp theo, phép hội `B and C` được thực hiện do `and` có độ ưu tiên cao hơn `or`. Cuối cùng, kết quả của hai vế mới được kết hợp qua toán tử `or`.

---

