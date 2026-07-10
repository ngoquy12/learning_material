```markmap
# Session 01: Nhập, xuất dữ liệu trong python
## Mục tiêu bài học
- Hiểu rõ khái niệm cốt lõi và kiến trúc của Nhập, xuất dữ liệu trong python.
- Áp dụng các quy tắc triển khai thực tiễn để giải quyết bài toán: Chương trình I/O cơ bản.
- Vận hành và kiểm tra đầu ra hoạt động ổn định.
## Nhập, xuất dữ liệu trong python
### Khái niệm cốt lõi
- Giải pháp kỹ thuật giúp tối ưu hóa hiệu năng, giảm thiểu blocking I/O và tự động hóa validation.
### Cú pháp & Cách khai báo
- Ví dụ triển khai:
      # 1. Khai báo biến và các kiểu dữ liệu cơ bản
      student_name = "Nguyễn Văn A"  # Kiểu chuỗi (str)
      student_age = 20               # Kiểu số nguyên (int)
      student_gpa = 3.8              # Kiểu số thực (float)
      is_active = True               # Kiểu luận lý (bool)
      
      # 2. Nhập xuất dữ liệu cơ bản từ bàn phím
      print("--- THÔNG TIN SINH VIÊN ---")
      print(f"Họ tên: {student_name}")
      print(f"Tuổi: {student_age}")
      print(f"GPA: {student_gpa}")
      
      # Nhận input và thực hiện ép kiểu (Casting) từ str sang int
      extra_years = input("Nhập số năm cộng thêm: ")
      future_age = student_age + int(extra_years)
      print(f"Tuổi của sinh viên sau {extra_years} năm nữa là: {future_age}")
### Lưu ý thực chiến
- Tránh bỏ sót các tham số bắt buộc.
- Cấu hình môi trường ảo venv chính xác và không đặt trùng tên file hệ thống.
[Prompt: Generate a flowchart diagram showing standard input processed by control flow logic and printing the formatted output.]
```