# 📋 Kịch Bản Video — Session 08 Lesson 03
## Phạm vi biến và scope (Variable Scope & LEGB Rule)

> **Trạng thái:** ⏸️ CHỜ DUYỆT (Human-in-the-Loop Script Review Gate)  
> **Tech stack:** Python/Core  
> **Lesson slug:** `session_08_lesson_03`  
> **Thư mục bài học:** `Session 08 - Hàm (Function) va Phạm vi biến/Lesson 03 - Phạm vi biến và scope`  
> **Tổng scene:** 10 scenes + Intro (9.24s) + Outro (12.15s)  
> **Thời lượng dự kiến:** ~5 phút 00 giây

---

## 🎯 Nguyên tắc Voice-UI Tách Biệt & Chuẩn Thiết Kế

| Thành phần | Tiêu chuẩn áp dụng |
|---|---|
| **TTS Narration (Giọng đọc)** | Câu văn hoàn chỉnh, tự nhiên. BẮT BUỘC dẫn dắt bằng bối cảnh thực tế/câu hỏi gợi mở trước khi phân tích kỹ thuật, kết thúc bằng câu chốt. |
| **UI Displays (Màn hình)** | Từ khóa ngắn 3-6 từ, code snippet chuẩn IDE tối, sơ đồ flow. KHÔNG chép nguyên câu đọc lên card. |
| **Giao diện UI (Dark Theme)** | Nền đen `#09090b` / `#0a0a0f`, tiêu đề góc trên trái Trắng thuần `#ffffff`, viền card mỏng `rgba(255,255,255,0.08)`. |
| **Bảo lưu mã nguồn** | 100% TÊN HÀM, TÊN BIẾN giữ nguyên chữ thường đúng cú pháp (`tax_rate`, `update_tax()`). CẤM tự động viết hoa. |
| **Loại bỏ rác layout** | **TUYỆT ĐỐI CẤM `border-left` màu accent** sặc sỡ bên hông card. **TUYỆT ĐỐI CẤM `card-badge` / `card-badge-lg`** gây rối màn hình. |

---

## Scene 01 — Tổng quan bài học & Bối cảnh thực tế
**Loại layout:** `split-3col` (3 thẻ cấu trúc song song)  
**Thời lượng ước tính:** ~28s

### Giọng đọc (TTS Narration):
> "Chào mừng bạn đến với bài học thứ ba trong Session 8. Trong phát triển phần mềm doanh nghiệp, đã bao giờ bạn gặp tình huống một hàm vô tình sửa đổi dữ liệu của hàm khác khiến toàn bộ hệ thống gặp lỗi khó hiểu chưa? Đây là bài toán về kiểm soát xung đột dữ liệu. Hôm nay chúng ta sẽ cùng tìm hiểu về Phạm vi biến và Scope — cơ chế nền tảng giúp Python phân định rõ ranh giới hoạt động và bảo vệ an toàn cho dữ liệu trong chương trình."

### Nội dung UI hiển thị:
- **Tiêu đề scene:** Tổng quan bài học & Bối cảnh thực tế
- 3 thẻ cấu trúc (`#13131f`, border `rgba(255,255,255,0.08)`):
  - Card 1 (`#a5b4fc`): **Phạm vi biến (Scope)** / Ranh giới truy cập dữ liệu
  - Card 2 (`#6ee7b7`): **Quy tắc LEGB** / Thứ tự ưu tiên tìm kiếm biến
  - Card 3 (`#fdba74`): **Từ khóa global & nonlocal** / Quản lý vùng nhớ nâng cao

---

## Scene 02 — Local Scope (Phạm vi cục bộ)
**Loại layout:** `split-container` (trái: bullet-list + alert-info, phải: code-panel)  
**Thời lượng ước tính:** ~30s

### Giọng đọc (TTS Narration):
> "Hãy cùng khám phá cấp độ phạm vi đầu tiên và phổ biến nhất — đó là Local Scope, hay phạm vi cục bộ. Mỗi khi bạn tạo một biến bên trong một hàm, biến đó sẽ sinh ra và chỉ sống nội bộ trong hàm đó mà thôi. Khi hàm thực thi xong và trả về kết quả, toàn bộ vùng nhớ Local Scope sẽ bị giải phóng tự động. Điều này giúp code độc lập và không sợ làm ảnh hưởng đến các biến ở bên ngoài."

### Nội dung UI hiển thị:
- **Tiêu đề scene:** Local Scope — Phạm vi cục bộ
- Trái — bullet-list & alert:
  - Biến khai báo bên trong hàm
  - Chỉ truy cập được trong nội bộ hàm
  - Tự động giải phóng bộ nhớ khi hàm kết thúc
  - Alert-info: Đảm bảo tính đóng gói (encapsulation)
- Phải — code panel (`local_scope.py`):
```python
def calculate_discount(price):
    discount_rate = 0.15  # Local variable
    return price * (1 - discount_rate)

result = calculate_discount(100)
print(result)  # 85.0
```

---

## Scene 03 — Global Scope (Phạm vi toàn cục)
**Loại layout:** `split-container` (trái: bullet-list + alert-warning, phải: code-panel)  
**Thời lượng ước tính:** ~29s

### Giọng đọc (TTS Narration):
> "Trái ngược với phạm vi cục bộ, Global Scope đại diện cho các biến được khai báo ở cấp cao nhất của file mã nguồn. Một biến toàn cục tồn tại suốt vòng đời của chương trình và có thể được đọc từ bất kỳ hàm nào. Tuy nhiên, mặc định các hàm con chỉ được phép đọc giá trị chứ không thể tự ý sửa đổi biến toàn cục. Quy tắc này giúp ngăn chặn các tác dụng phụ không mong muốn trong ứng dụng."

### Nội dung UI hiển thị:
- **Tiêu đề scene:** Global Scope — Phạm vi toàn cục
- Trái — bullet-list & alert:
  - Khai báo ở cấp cao nhất của file code
  - Tồn tại suốt vòng đời chương trình
  - Các hàm được phép đọc nhưng CẤM tự ý ghi đè
  - Alert-warning: Đọc tự do, muốn ghi đè cần từ khóa `global`
- Phải — code panel (`global_scope.py`):
```python
tax_rate = 0.08  # Global variable

def print_invoice(amount):
    # Đọc biến toàn cục tax_rate
    total = amount * (1 + tax_rate)
    print(f"Tổng hóa đơn: {total}")

print_invoice(100)  # 108.0
```

---

## Scene 04 — Quy tắc tìm kiếm LEGB
**Loại layout:** `step-list` (danh sách thứ tự 4 cấp độ LEGB)  
**Thời lượng ước tính:** ~31s

### Giọng đọc (TTS Narration):
> "Khi một biến được gọi trong code, làm thế nào Python biết phải lấy giá trị từ đâu? Bộ thông dịch Python áp dụng một quy tắc tìm kiếm tuần tự từ trong ra ngoài gọi là LEGB. Viết tắt của bốn cấp độ: L là Local, E là Enclosing, G là Global, và B là Built-in. Python sẽ kiểm tra từng phân vùng theo đúng thứ tự này và dừng lại ngay khi tìm thấy biến đầu tiên khớp tên."

### Nội dung UI hiển thị:
- **Tiêu đề scene:** Quy tắc tìm kiếm LEGB
- Step-list:
  1. `L — Local`: Kiểm tra trong nội bộ hàm hiện tại
  2. `E — Enclosing`: Kiểm tra ở hàm bao ngoài (nested function)
  3. `G — Global`: Kiểm tra ở phạm vi toàn file
  4. `B — Built-in`: Kiểm tra các hàm tích hợp sẵn của Python (`len`, `print`, `sum`)
- Alert-info: Python tìm từ L ➔ E ➔ G ➔ B và dừng ở vị trí đầu tiên khớp tên.

---

## Scene 05 — Từ khóa global
**Loại layout:** `split-container` (trái: bullet-list + alert-warning, phải: code-panel)  
**Thời lượng ước tính:** ~30s

### Giọng đọc (TTS Narration):
> "Giả sử bạn thực sự cần thay đổi một giá trị cấu hình toàn cục từ bên trong một hàm thì phải làm thế nào? Đây là lúc từ khóa global phát huy tác dụng. Khai báo global cùng tên biến ở đầu hàm là cách bạn thông báo cho Python biết: hãy thao tác trực tiếp lên ô nhớ toàn cục thay vì tạo một biến cục bộ mới. Xem ví dụ hàm update_tax bên phải để thấy cách biến tax_rate bị thay đổi."

### Nội dung UI hiển thị:
- **Tiêu đề scene:** Từ khóa `global`
- Trái — bullet-list & alert:
  - Cho phép hàm ghi đè trực tiếp biến toàn cục
  - Khai báo ở dòng đầu tiên bên trong hàm
  - Tránh tự động tạo biến Local trùng tên
  - Alert-warning: `global tax_rate` liên kết trực tiếp vùng nhớ Global
- Phải — code panel (`global_keyword.py`):
```python
tax_rate = 0.08  # Global

def update_tax(new_rate):
    global tax_rate  # Báo cho Python dùng biến Global
    tax_rate = new_rate

print(tax_rate)  # 0.08
update_tax(0.10)
print(tax_rate)  # 0.1
```

---

## Scene 06 — Cảnh báo lạm dụng global (Anti-pattern)
**Loại layout:** `split-equal` (đối sánh 2 cách viết code song song)  
**Thời lượng ước tính:** ~28s

### Giọng đọc (TTS Narration):
> "Mặc dù từ khóa global rất tiện lợi, nhưng lạm dụng nó lại là một anti-pattern bị nghiêm cấm trong các dự án doanh nghiệp. Khi quá nhiều hàm cùng sửa chung biến toàn cục, chương trình sẽ rơi vào trạng thái khó kiểm soát và cực kỳ dễ sinh bug. Giải pháp chuẩn mực hơn là truyền dữ liệu qua tham số và nhận kết quả trả về thông qua câu lệnh return."

### Nội dung UI hiển thị:
- **Tiêu đề scene:** Cảnh báo lạm dụng `global` — Anti-pattern
- Trái — Code không nên dùng (Lạm dụng `global` ❌):
```python
# BAD: Phụ thuộc biến Global
count = 0
def increment():
    global count
    count += 1
```
- Phải — Code chuẩn mực (Dùng Tham số & Return ✅):
```python
# GOOD: Hàm thuần khiết (Pure function)
def increment(current_count):
    return current_count + 1

count = increment(count)
```

---

## Scene 07 — Enclosing Scope & Từ khóa nonlocal
**Loại layout:** `split-container` (trái: bullet-list, phải: code-panel)  
**Thời lượng ước tính:** ~32s

### Giọng đọc (TTS Narration):
> "Trong Python, bạn có thể định nghĩa một hàm nằm bên trong một hàm khác — gọi là nested function. Phạm vi biến của hàm cha đối với hàm con được gọi là Enclosing Scope. Nếu hàm con muốn sửa đổi biến của hàm cha mà không chạm vào biến Global, chúng ta sử dụng từ khóa nonlocal. Đây là nền tảng kỹ thuật quan trọng để xây dựng Closure và Decorator trong Python."

### Nội dung UI hiển thị:
- **Tiêu đề scene:** Enclosing Scope & Từ khóa `nonlocal`
- Trái — bullet-list:
  - Xuất hiện trong cấu trúc hàm lồng nhau (nested functions)
  - Biến thuộc hàm cha nhưng nằm ngoài hàm con
  - Từ khóa `nonlocal` cho phép hàm con sửa biến hàm cha
  - Nền tảng xây dựng Closure & Decorator
- Phải — code panel (`nonlocal_demo.py`):
```python
def outer_calculator():
    fee = 15.0  # Enclosing scope
    
    def inner_apply():
        nonlocal fee  # Sửa biến của outer_calculator
        fee = 20.0
        
    inner_apply()
    return fee

print(outer_calculator())  # 20.0
```

---

## Scene 08 — Lỗi UnboundLocalError
**Loại layout:** `split-container` (trái: alert-danger + giải thích, phải: code-panel bẫy lỗi)  
**Thời lượng ước tính:** ~30s

### Giọng đọc (TTS Narration):
> "Một trong những cái bẫy kinh điển khiến nhiều lập trình viên mới gặp lỗi là UnboundLocalError. Lỗi này xảy ra khi bạn vừa đọc vừa gán một biến trùng tên với biến toàn cục trong cùng một hàm mà không khai báo global. Python thấy lệnh gán nên đánh dấu biến đó là Local, dẫn đến việc dòng đọc giá trị trước đó bị sụp đổ vì biến Local chưa được khởi tạo."

### Nội dung UI hiển thị:
- **Tiêu đề scene:** Bẫy cú pháp — Lỗi UnboundLocalError
- Trái — alert-danger & nguyên nhân:
  - Alert-danger: `UnboundLocalError: local variable referenced before assignment`
  - Vừa đọc vừa gán biến trùng tên Global trong hàm
  - Python tự coi biến đó là Local ➔ dòng đọc bị văng lỗi
- Phải — code panel bẫy lỗi (`bug_unbound.py`):
```python
counter = 10

def invalid_increment():
    # LỖI: counter được coi là Local do phép gán phía dưới!
    print(counter)  # UnboundLocalError
    counter += 1

invalid_increment()
```

---

## Scene 09 — Lỗi NameError khi truy cập ngoài scope
**Loại layout:** `split-container` (trái: alert-danger + giải thích, phải: code-panel vi phạm)  
**Thời lượng ước tính:** ~28s

### Giọng đọc (TTS Narration):
> "Tương tự, một lỗi phổ biến khác là NameError khi bạn cố gắng truy cập một biến cục bộ từ bên ngoài hàm. Hãy nhớ rằng biến trong Local Scope sẽ biến mất ngay khi hàm kết thúc. Việc gọi tên biến đó ở scope bên ngoài là hành vi vi phạm ranh giới bộ nhớ, và Python sẽ ngắt chương trình bằng thông báo NameError ngay lập tức."

### Nội dung UI hiển thị:
- **Tiêu đề scene:** Bẫy phạm vi — Lỗi NameError
- Trái — alert-danger & nguyên nhân:
  - Alert-danger: `NameError: name 'temp_val' is not defined`
  - Cố tình gọi biến Local ở bên ngoài hàm
  - Biến Local đã bị xoá khỏi bộ nhớ khi hàm kết thúc
- Phải — code panel vi phạm (`bug_name_error.py`):
```python
def create_session():
    temp_val = "SECRET_123"  # Local
    return True

create_session()
# LỖI: temp_val không tồn tại ở Global Scope!
print(temp_val)  # NameError
```

---

## Scene 10 — Tổng kết & Best Practices
**Loại layout:** `card-full` + grid tổng kết 4 ô  
**Thời lượng ước tính:** ~31s

### Giọng đọc (TTS Narration):
> "Tổng kết lại bài học hôm nay: Bạn đã làm chủ bốn cấp độ quy tắc LEGB từ Local, Enclosing, Global đến Built-in. Hãy nhớ dùng global khi muốn sửa biến toàn cục và nonlocal khi làm việc với hàm lồng nhau. Tuy nhiên, Best practice hàng đầu trong phát triển phần mềm chuyên nghiệp là hạn chế tối đa biến toàn cục, giữ các hàm độc lập và luôn truyền nhận dữ liệu qua tham số và giá trị trả về."

### Nội dung UI hiển thị:
- **Tiêu đề scene:** Tổng kết & Best Practices
- Grid 4 thẻ tổng kết:
  - Thẻ 1 (`Local`): Sinh ra và mất đi cùng hàm
  - Thẻ 2 (`Enclosing`): Hàm cha bao ngoài, dùng `nonlocal`
  - Thẻ 3 (`Global`): Cấp file, dùng `global` khi cần ghi đè
  - Thẻ 4 (`Built-in`): Tích hợp sẵn của Python
- Alert-info: "Best Practice: Hạn chế dùng `global`, ưu tiên truyền tham số và dùng `return`."

---

## 📊 Tóm Tắt Kịch Bản Lesson 03

| Scene | Chủ đề | Layout UI | Thời lượng ước tính |
|---|---|---|---|
| Intro | Bìa bài học | Intro.html | 9.24s |
| 01 | Tổng quan & Bối cảnh | 3-column grid | ~28s |
| 02 | Local Scope | Split + code | ~30s |
| 03 | Global Scope | Split + code | ~29s |
| 04 | Quy tắc LEGB | Step-list 4 bước | ~31s |
| 05 | Từ khóa `global` | Split + code | ~30s |
| 06 | Anti-pattern `global` | Split-equal | ~28s |
| 07 | Enclosing & `nonlocal` | Split + code | ~32s |
| 08 | Lỗi UnboundLocalError | Alert-danger + code | ~30s |
| 09 | Lỗi NameError | Alert-danger + code | ~28s |
| 10 | Tổng kết & Best Practices | Grid 4 thẻ + alert | ~31s |
| Outro | Kết thúc | Outro.html | 12.15s |
| **TỔNG** | | | **~5 phút 19 giây** |

---

> ## ⏸️ CHỜ DUYỆT KỊCH BẢN (HUMAN REVIEW GATE)
> Kịch bản đã được lưu tại [SCRIPT.md](file:///d:/Rikkei%20Education/Elearning_Agent/Learning-Material/output/PM_Python/Session%2008%20-%20H%C3%A0m%20%28Function%29%20va%20Ph%E1%BA%A1m%20vi%20bi%E1%BA%BFn/Lesson%2003%20-%20Ph%E1%BA%A1m%20vi%20bi%E1%BA%BFn%20v%C3%A0%20scope/Video/SCRIPT.md).  
> **Lưu ý:** Tuyệt đối KHÔNG sửa code trong bất kỳ agent hay skill nào theo đúng yêu cầu.  
> Vui lòng kiểm tra và duyệt kịch bản trên trước khi tiến hành các bước tạo video tiếp theo.
