# Bộ câu hỏi Khảo thí & Đánh giá năng lực: Cấu trúc match-case nâng cao

### Câu 1: Khi sử dụng Mapping Pattern như case {'status': _}, nếu từ điển đầu vào có thêm các khóa khác không được khai báo trong case thì case đó có khớp không?

**Gợi ý trả lời & Hướng dẫn tự học:**
Có khớp. Khác với Sequence Pattern yêu cầu khớp toàn bộ số phần tử (hoặc phải dùng cấu trúc gom nhóm), Mapping Pattern trong match-case chỉ yêu cầu từ điển đầu vào chứa đầy đủ các khóa được khai báo trong pattern. Các khóa dư thừa khác của từ điển đầu vào sẽ được bỏ qua và không ảnh hưởng đến kết quả khớp.

---

