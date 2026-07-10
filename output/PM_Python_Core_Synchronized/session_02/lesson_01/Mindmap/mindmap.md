```markmap
# Session 02: Các loại toán tử số học
## Mục tiêu bài học
- Hiểu rõ khái niệm cốt lõi và kiến trúc của Các loại toán tử số học.
- Áp dụng các quy tắc triển khai thực tiễn để giải quyết bài toán: Bài tập tính toán số học.
- Vận hành và kiểm tra đầu ra hoạt động ổn định.
## Các loại toán tử số học
### Khái niệm cốt lõi
- Giải pháp kỹ thuật giúp tối ưu hóa hiệu năng, giảm thiểu blocking I/O và tự động hóa validation.
### Cú pháp & Cách khai báo
- Ví dụ triển khai:
      # 1. Sử dụng toán tử số học và logic
      math_score = 8.5
      english_score = 7.0
      
      # Điều kiện đạt học bổng: Điểm trung bình >= 8.0 VÀ không môn nào dưới 6.5
      average_score = (math_score + english_score) / 2
      has_scholarship = average_score >= 8.0 and math_score >= 6.5 and english_score >= 6.5
      
      # 2. Sử dụng cấu trúc rẽ nhánh khoa học và toán tử ba ngôi
      status = "Đạt học bổng" if has_scholarship else "Không đạt học bổng"
      print(f"Điểm TB: {average_score} -> Trạng thái: {status}")
      
      # 3. Sử dụng cấu trúc match-case mới (Python 3.10+)
      rank_level = "A" if average_score >= 8.5 else "B" if average_score >= 7.0 else "C"
      match rank_level:
          case "A":
              print("Xếp loại xuất sắc, được nhận học bổng loại I.")
          case "B":
              print("Xếp loại khá giỏi, được nhận học bổng loại II.")
          case _:
              print("Cần cố gắng thêm trong các kỳ học sau.")
### Lưu ý thực chiến
- Tránh bỏ sót các tham số bắt buộc.
- Cấu hình môi trường ảo venv chính xác và không đặt trùng tên file hệ thống.
[Prompt: Generate a flowchart diagram showing standard input processed by control flow logic and printing the formatted output.]
```