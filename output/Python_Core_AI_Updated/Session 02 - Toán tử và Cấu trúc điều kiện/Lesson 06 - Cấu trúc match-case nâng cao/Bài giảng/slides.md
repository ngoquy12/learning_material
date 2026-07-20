---
marp: true
theme: gaia
_class: lead
paginate: true
---

# Session 02 - Lesson 06
## Cấu trúc match-case nâng cao

---

# Vấn đề
* **Xử lý dữ liệu phức tạp**: Khi nhận dữ liệu từ API hoặc hệ thống khác dưới dạng Dictionary và List lồng nhau.
* **Hạn chế của `if-elif-else`**:
    * Phải lặp đi lặp lại việc kiểm tra sự tồn tại của khóa (`in`, `get()`).
    * Phải ép kiểu hoặc kiểm tra kiểu dữ liệu thủ công.
    * Mã nguồn trở nên cồng kềnh, dễ lỗi logic và rất khó bảo trì.

---

# Phân tích: Giải pháp từ Python 3.10+

* **Structural Pattern Matching**: Cho phép so khớp trực tiếp cấu trúc của dữ liệu (kiểu dữ liệu, giá trị, hình dạng) thay vì chỉ so sánh giá trị đơn thuần.
* **Mapping Pattern**: So khớp Dictionary dựa trên sự hiện diện của các khóa mà không cần kiểm tra thủ công.
* **Capture Pattern (`as`)**: Vừa kiểm tra cấu trúc, vừa trích xuất và gán dữ liệu khớp vào một biến để sử dụng ngay lập tức.
* **Guard Clause (`if`)**: Thêm điều kiện lọc bổ sung trực tiếp vào case.

---

# So khớp cơ bản vs `if-elif-else`

```python
def process_status(status_code):
    # Sử dụng structural pattern matching thay vì if-elif-else truyền thống
    match status_code:
        case 200:
            return "OK"
        case 400:
            return "Bad Request"
        case 404:
            return "Not Found"
        case 500:
            return "Internal Server Error"
        case _:
            return "Unknown Status Code"
```

* **`case _` (Wildcard Pattern)**: Đóng vai trò là pattern mặc định, khớp với bất kỳ giá trị nào còn lại.

---

# So khớp cấu trúc phức tạp (Composite)

```python
def handle_command(command):
    # So khớp cấu trúc List/Tuple (Sequence Pattern) và Dict (Mapping Pattern)
    match command:
        # Khớp với list/tuple có 3 phần tử bắt đầu bằng "move"
        case ["move", int(x), int(y)]:
            return f"Di chuyển đến tọa độ x={x}, y={y}"
        # Khớp với list/tuple có 2 phần tử bắt đầu bằng "say"
        case ["say", str(message)]:
            return f"Phát thông điệp: {message}"
        # Khớp với dictionary có key "action" là "delete" và có key "id"
        case {"action": "delete", "id": user_id}:
            return f"Xóa người dùng có ID={user_id}"
        case _:
            return "Lệnh không hợp lệ"
```

---

# Sử dụng Guard Clause để lọc điều kiện

```python
def process_coordinate(coordinate):
    # Sử dụng Guard Clause (từ khóa 'if') để kiểm tra điều kiện bổ sung trong case
    match coordinate:
        case (x, y) if x == 0 and y == 0:
            return "Gốc tọa độ"
        case (x, y) if x > 0 and y > 0:
            return f"Điểm ({x}, {y}) nằm ở góc phần tư thứ I"
        case (x, y) if x < 0 or y < 0:
            return f"Điểm ({x}, {y}) có ít nhất một tọa độ âm"
        case (x, y):
            return f"Điểm ở tọa độ ({x}, {y})"
        case _:
            return "Định dạng tọa độ không hợp lệ"
```

---

# Trích xuất dữ liệu API với Capture Pattern (`as`)

```python
def parse_api_response(response):
    # Tái cấu trúc bộ xử lý API phản hồi phức tạp bằng match-case và capture pattern 'as'
    match response:
        case {"status": "success", "data": {"user": str(name), "role": role}}:
            return f"Đăng nhập thành công! Người dùng: {name} (Vai trò: {role})"
        case {"status": "error", "error": {"code": int(code), "message": msg}}:
            return f"Lỗi hệ thống [{code}]: {msg}"
        case {"status": _} as raw_response:
            return f"Phản hồi không xác định nhưng có thuộc tính status: {raw_response['status']}"
        case _:
            return "Định dạng phản hồi API không hợp lệ"
```

---

# Sơ đồ luồng hoạt động của match-case

```text
Input 
  │
  ├──► [Match Pattern?] ──(False)──► (Xét Pattern tiếp theo...)
  │          │
  │        (True)
  │          │
  │          ▼
  ├──► [Guard Constraint?] ──(False)──► (Xét Pattern tiếp theo...)
  │          │
  │        (True)
  │          │
  ▼          ▼
[Thực thi mã trong Case]
  │
  ▼
(Không khớp bất kỳ case nào) ──► Wildcard (case _) ──► Thực thi mặc định
```

---

# Tổng kết & 3 Lỗi thường gặp cần tránh

* **Lỗi 1: Đặt wildcard `case _` sai vị trí**
    * *Sai*: Đặt `case _` trước các case cụ thể khác. Việc này khiến các case phía sau bị che khuất và không bao giờ được kiểm tra.
* **Lỗi 2: Hiểu lầm về tính chính xác của Mapping Pattern**
    * *Thực tế*: Mapping Pattern không yêu cầu khớp chính xác tuyệt đối tất cả các key của từ điển gốc, nó chỉ cần khớp tối thiểu các key được khai báo trong pattern.
* **Lỗi 3: Sai cú pháp gán biến trong Capture Pattern**
    * *Sai*: Sử dụng dấu gán `=` (ví dụ: `case pattern = variable`).
    * *Đúng*: Sử dụng từ khóa `as` (ví dụ: `case pattern as variable`).