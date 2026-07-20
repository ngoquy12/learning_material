---
marp: true
theme: gaia
_class: lead
paginate: true
---

# Session 02 - Lesson 05: Điều kiện lồng nhau và toán tử ba ngôi

Giảng viên: [Tên Giảng Viên]
Bộ môn: Lập trình Python

---

# Vấn đề: Cấu trúc Rẽ nhánh Phức tạp

- **Deep Nesting (Lồng nhau sâu)**: Khi giải quyết các bài toán phân nhánh phức tạp, lập trình viên thường viết nhiều cấu trúc `if-else` lồng nhau.
- **Hệ quả**: 
  - Tạo ra cấu trúc mã nguồn dạng mũi tên (**Arrow Anti-Pattern** hoặc **Pyramid of Doom**).
  - Làm code cực kỳ rối mắt, khó đọc.
  - Tăng nguy cơ phát sinh lỗi tiềm ẩn khi bảo trì hoặc mở rộng hệ thống.

---

# Minh họa: Lồng điều kiện gây khó đọc

```python
def calculate_shipping_cost(price, location):
    # Ví dụ về lồng điều kiện gây khó đọc và bảo trì
    if price > 0:
        if location == "internal":
            if price >= 100:
                return 0
            else:
                return 5
        else:
            return 15
    else:
        return -1
```

- Nhận xét: Luồng xử lý bị đẩy sâu sang bên phải, khó theo dõi điều kiện logic cùng lúc.

---

# Phân tích Giải pháp

- **Toán tử ba ngôi (Ternary Operator)**:
  - Rút gọn logic đơn giản thành dạng biểu thức trực quan:
    `giá_trị_đúng if điều_kiện else giá_trị_sai`
  - Giúp gán giá trị hoặc trả về kết quả trực tiếp mà không cần viết khối `if-else` dài dòng.
- **Mệnh đề bảo vệ (Guard Clauses)**:
  - Xử lý sớm các trường hợp ngoại lệ, điều kiện biên hoặc lỗi ở đầu hàm bằng từ khóa `return`.
  - Giữ luồng xử lý chính chạy thẳng theo lề trái của mã nguồn.

---

# Sử dụng Toán tử ba ngôi

Dưới đây là cách sử dụng toán tử ba ngôi để gán trạng thái ngắn gọn:

```python
def classify_score(score):
    # Sử dụng toán tử ba ngôi để gán trạng thái ngắn gọn
    result = "Đạt" if score >= 5.0 else "Không đạt"
    return result
```

- Ưu điểm: Mã nguồn súc tích, dễ hiểu ngay lập tức.

---

# Tái cấu trúc với Guard Clauses và Toán tử ba ngôi

Kết hợp cả hai kỹ thuật để làm sạch mã nguồn:

```python
def check_payment_status(amount, is_verified):
    # Phiên bản tối ưu sử dụng Guard Clauses
    if amount <= 0:
        return "Invalid amount"
        
    if not is_verified:
        return "Unverified account"
        
    # Dòng xử lý chính sử dụng toán tử ba ngôi
    return "Require approval" if amount > 1000 else "Approved"
```

---

# Ưu điểm của mã nguồn đã tối ưu

- Các điều kiện lỗi (`amount <= 0`, `not is_verified`) được loại bỏ ngay từ đầu bằng **Guard Clauses**.
- Tránh được việc lồng các khối `if` vào nhau một cách không cần thiết.
- Luồng xử lý chính được viết thẳng ở lề trái màn hình, kết hợp **Toán tử ba ngôi** ở dòng cuối cùng để trả về kết quả đơn giản.

---

# 3 Lỗi thường gặp cần tránh

1. **Deep Nesting (Pyramid of Doom)**: Lồng quá 3 tầng `if-else` khiến code bị thụt lề quá nhiều về phía bên phải.
2. **Lạm dụng toán tử ba ngôi**: Viết các biểu thức ba ngôi lồng nhau phức tạp (ví dụ: `a if cond1 else b if cond2 else c`) gây rất khó đọc.
3. **Quên return trong Guard Clauses**: Không dùng hoặc quên `return` khiến chương trình kiểm tra sai điều kiện và tiếp tục thực thi các dòng bên dưới bất hợp lệ.

---

# Tổng kết

- Tối ưu hóa cấu trúc rẽ nhánh giúp mã nguồn sáng sủa, nâng cao khả năng bảo trì.
- Hãy luôn ưu tiên xử lý các trường hợp biên/lỗi trước bằng **Guard Clauses**.
- Sử dụng **Toán tử ba ngôi** đúng nơi, đúng chỗ cho các quyết định logic đơn giản.