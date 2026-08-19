# Bộ câu hỏi kiểm tra bài đọc (Reading Comprehension Questions)

## Tình huống & Mã nguồn kiểm tra
Dựa trên mã nguồn nghiệp vụ được trích dẫn từ bài đọc:

```javascript
vanilla (es6+), html5

# Mã nguồn minh họa nghiệp vụ cho bài học: Tổng quan JavaScript và Cơ chế V8 Engine
score = 8.5

if score >= 9.0:
    rank = "Xuất sắc"
elif score >= 8.0:
    rank = "Giỏi"
elif score >= 6.5:
    rank = "Khá"
else:
    rank = "Trung bình"

print(f"Học lực: {rank}")
```

---

### Câu 1 (Xung hướng - Tính toán kết quả với dữ liệu X): Nếu giá trị đầu vào là `score = 8.5`, chương trình sẽ thực thi qua những câu lệnh rẽ nhánh nào và in kết quả `rank` ra màn hình là gì?
> **Gợi ý trả lời & Định hướng đáp án:**
> - Điều kiện `score >= 9.0` (8.5 >= 9.0) trả về `False`.
> - Điều kiện `score >= 8.0` (8.5 >= 8.0) trả về `True`.
> - Gán `rank = 'Giỏi'` và kết quả in ra màn hình là `Học lực: Giỏi`.

---

### Câu 2 (Xung hướng - Thử nghiệm với mốc dữ liệu Y): Nếu sửa giá trị thành `score = 7.0`, nhánh rẽ nào sẽ được kích hoạt và kết quả `rank` thay đổi ra sao?
> **Gợi ý trả lời & Định hướng đáp án:**
> - Các điều kiện `>= 9.0` và `>= 8.0` đều `False`.
> - Điều kiện `score >= 6.5` (7.0 >= 6.5) trả về `True`.
> - Gán `rank = 'Khá'` và in ra màn hình `Học lực: Khá`.

---

### Câu 3 (Nghịch hướng - Suy luận dữ liệu đầu vào từ kết quả Z): Để hệ thống xếp loại `rank = 'Giỏi'`, giá trị biến `score` phải thỏa mãn khoảng giá trị toán học nào?
> **Gợi ý trả lời & Định hướng đáp án:**
> - Biến `score` phải thỏa mãn điều kiện `8.0 <= score < 9.0` (từ 8.0 đến dưới 9.0).

---

### Câu 4 (Phân tích bẫy lỗi & Trường hợp biên): Nếu nhập `score = -1.0` hoặc `score = 11.0`, hãy chỉ ra điểm bất hợp lý của mã nguồn hiện tại và đề xuất cách cải tiến.
> **Gợi ý trả lời & Định hướng đáp án:**
> - Mã nguồn chưa có nhánh kiểm tra tính hợp lệ dữ liệu (0 <= score <= 10).
> - Khi `score = 11.0`, hệ thống vẫn xếp loại 'Xuất sắc', khi `score = -1.0` xếp loại 'Trung bình'.
> - Cần bổ sung câu lệnh `if score < 0 or score > 10:` ở đầu để báo lỗi dữ liệu không hợp lệ.

---
