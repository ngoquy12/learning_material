---
markmap:
  colorFreezeLevel: 2
---
# Toán tử và Cấu trúc điều kiện

## Session 02: Các loại toán tử số học
  ```markmap
  - Hiểu rõ khái niệm cốt lõi và kiến trúc của Các loại toán tử số học.
  - Áp dụng các quy tắc triển khai thực tiễn để giải quyết bài toán: Bài tập tính toán số học.
  - Vận hành và kiểm tra đầu ra hoạt động ổn định.
  - Giải pháp kỹ thuật giúp tối ưu hóa hiệu năng, giảm thiểu blocking I/O và tự động hóa validation.
  - Ví dụ triển khai:
        math_score = 8.5
        english_score = 7.0
        average_score = (math_score + english_score) / 2
        has_scholarship = average_score >= 8.0 and math_score >= 6.5 and english_score >= 6.5
        status = "Đạt học bổng" if has_scholarship else "Không đạt học bổng"
        print(f"Điểm TB: {average_score} -> Trạng thái: {status}")
        rank_level = "A" if average_score >= 8.5 else "B" if average_score >= 7.0 else "C"
        match rank_level:
            case "A":
                print("Xếp loại xuất sắc, được nhận học bổng loại I.")
            case "B":
                print("Xếp loại khá giỏi, được nhận học bổng loại II.")
            case _:
                print("Cần cố gắng thêm trong các kỳ học sau.")
  - Tránh bỏ sót các tham số bắt buộc.
  - Cấu hình môi trường ảo venv chính xác và không đặt trùng tên file hệ thống.
  [Prompt: Generate a flowchart diagram showing standard input processed by control flow logic and printing the formatted output.]
  ```

## Session 02: Toán tử so sánh
  ```markmap
  - Hiểu rõ khái niệm cốt lõi và kiến trúc của Toán tử so sánh.
  - Áp dụng các quy tắc triển khai thực tiễn để giải quyết bài toán: Biểu thức so sánh logic.
  - Vận hành và kiểm tra đầu ra hoạt động ổn định.
  - Giải pháp kỹ thuật giúp tối ưu hóa hiệu năng, giảm thiểu blocking I/O và tự động hóa validation.
  - Ví dụ triển khai:
        math_score = 8.5
        english_score = 7.0
        average_score = (math_score + english_score) / 2
        has_scholarship = average_score >= 8.0 and math_score >= 6.5 and english_score >= 6.5
        status = "Đạt học bổng" if has_scholarship else "Không đạt học bổng"
        print(f"Điểm TB: {average_score} -> Trạng thái: {status}")
        rank_level = "A" if average_score >= 8.5 else "B" if average_score >= 7.0 else "C"
        match rank_level:
            case "A":
                print("Xếp loại xuất sắc, được nhận học bổng loại I.")
            case "B":
                print("Xếp loại khá giỏi, được nhận học bổng loại II.")
            case _:
                print("Cần cố gắng thêm trong các kỳ học sau.")
  - Tránh bỏ sót các tham số bắt buộc.
  - Cấu hình môi trường ảo venv chính xác và không đặt trùng tên file hệ thống.
  [Prompt: Generate a flowchart diagram showing standard input processed by control flow logic and printing the formatted output.]
  ```

## Session 02: Toán tử logic
  ```markmap
  - Hiểu rõ khái niệm cốt lõi và kiến trúc của Toán tử logic.
  - Áp dụng các quy tắc triển khai thực tiễn để giải quyết bài toán: Bảng chân trị logic áp dụng vào code.
  - Vận hành và kiểm tra đầu ra hoạt động ổn định.
  - Giải pháp kỹ thuật giúp tối ưu hóa hiệu năng, giảm thiểu blocking I/O và tự động hóa validation.
  - Ví dụ triển khai:
        math_score = 8.5
        english_score = 7.0
        average_score = (math_score + english_score) / 2
        has_scholarship = average_score >= 8.0 and math_score >= 6.5 and english_score >= 6.5
        status = "Đạt học bổng" if has_scholarship else "Không đạt học bổng"
        print(f"Điểm TB: {average_score} -> Trạng thái: {status}")
        rank_level = "A" if average_score >= 8.5 else "B" if average_score >= 7.0 else "C"
        match rank_level:
            case "A":
                print("Xếp loại xuất sắc, được nhận học bổng loại I.")
            case "B":
                print("Xếp loại khá giỏi, được nhận học bổng loại II.")
            case _:
                print("Cần cố gắng thêm trong các kỳ học sau.")
  - Tránh bỏ sót các tham số bắt buộc.
  - Cấu hình môi trường ảo venv chính xác và không đặt trùng tên file hệ thống.
  [Prompt: Generate a flowchart diagram showing standard input processed by control flow logic and printing the formatted output.]
  ```

## Session 02: Cấu trúc điều kiện đa nhánh if-else-match-case
  ```markmap
  - Hiểu rõ khái niệm cốt lõi và kiến trúc của Cấu trúc điều kiện đa nhánh if-else-match-case.
  - Áp dụng các quy tắc triển khai thực tiễn để giải quyết bài toán: Chương trình phân loại điều kiện.
  - Vận hành và kiểm tra đầu ra hoạt động ổn định.
  - Giải pháp kỹ thuật giúp tối ưu hóa hiệu năng, giảm thiểu blocking I/O và tự động hóa validation.
  - Ví dụ triển khai:
        math_score = 8.5
        english_score = 7.0
        average_score = (math_score + english_score) / 2
        has_scholarship = average_score >= 8.0 and math_score >= 6.5 and english_score >= 6.5
        status = "Đạt học bổng" if has_scholarship else "Không đạt học bổng"
        print(f"Điểm TB: {average_score} -> Trạng thái: {status}")
        rank_level = "A" if average_score >= 8.5 else "B" if average_score >= 7.0 else "C"
        match rank_level:
            case "A":
                print("Xếp loại xuất sắc, được nhận học bổng loại I.")
            case "B":
                print("Xếp loại khá giỏi, được nhận học bổng loại II.")
            case _:
                print("Cần cố gắng thêm trong các kỳ học sau.")
  - Tránh bỏ sót các tham số bắt buộc.
  - Cấu hình môi trường ảo venv chính xác và không đặt trùng tên file hệ thống.
  [Prompt: Generate a flowchart diagram showing standard input processed by control flow logic and printing the formatted output.]
  ```

## Session 02: Điều kiện lồng nhau và toán tử ba ngôi
  ```markmap
  - Hiểu rõ khái niệm cốt lõi và kiến trúc của Điều kiện lồng nhau và toán tử ba ngôi.
  - Áp dụng các quy tắc triển khai thực tiễn để giải quyết bài toán: Mã nguồn rẽ nhánh sạch và gọn.
  - Vận hành và kiểm tra đầu ra hoạt động ổn định.
  - Giải pháp kỹ thuật giúp tối ưu hóa hiệu năng, giảm thiểu blocking I/O và tự động hóa validation.
  - Ví dụ triển khai:
        math_score = 8.5
        english_score = 7.0
        average_score = (math_score + english_score) / 2
        has_scholarship = average_score >= 8.0 and math_score >= 6.5 and english_score >= 6.5
        status = "Đạt học bổng" if has_scholarship else "Không đạt học bổng"
        print(f"Điểm TB: {average_score} -> Trạng thái: {status}")
        rank_level = "A" if average_score >= 8.5 else "B" if average_score >= 7.0 else "C"
        match rank_level:
            case "A":
                print("Xếp loại xuất sắc, được nhận học bổng loại I.")
            case "B":
                print("Xếp loại khá giỏi, được nhận học bổng loại II.")
            case _:
                print("Cần cố gắng thêm trong các kỳ học sau.")
  - Tránh bỏ sót các tham số bắt buộc.
  - Cấu hình môi trường ảo venv chính xác và không đặt trùng tên file hệ thống.
  [Prompt: Generate a flowchart diagram showing standard input processed by control flow logic and printing the formatted output.]
  ```
