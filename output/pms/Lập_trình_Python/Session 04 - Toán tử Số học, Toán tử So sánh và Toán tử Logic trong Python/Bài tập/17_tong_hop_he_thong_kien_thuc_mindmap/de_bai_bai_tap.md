# <center>[Tổng hợp Mindmap] Hệ thống Kiến thức & Sơ đồ Tư duy (Mindmap) - Session 04</center>

### **1. Mục tiêu**
- Hệ thống hóa toàn bộ kiến thức cốt lõi về **Toán tử Số học**, **Toán tử So sánh**, **Toán tử Logic** và **Thứ tự ưu tiên tính toán** trong Python.
- Trực quan hóa cấu trúc dữ liệu, biểu thức điều kiện và luồng đánh giá biểu thức logic bằng Sơ đồ Tư duy (Mindmap) gắn với bài toán thực tế hệ thống **Quản lý Đặt phòng Khách sạn (HOTEL_BOOKING)**.
- Rèn luyện kỹ năng phân tầng logic, phát hiện các "bẫy" sai số (như chia số thực `/` vs chia số nguyên `//`, bẫy ưu tiên toán tử logic `not`, `and`, `or`) và kết nối tri thức hệ thống một cách khoa học.

### **2. Bối cảnh & Vấn đề**
Bạn là một **Software Engineer** phụ trách phát triển Module Tính toán Chi phí & Phê duyệt Ưu đãi Đặt phòng cho hệ thống **HOTEL_BOOKING** (Hệ thống Khách sạn Quốc tế "Grand Luxury Stay"). Để phục vụ việc onboarding các kỹ sư mới và tài liệu hóa chuẩn kiến thức nền tảng của hệ thống, bạn được giao nhiệm vụ thiết kế một Sơ đồ tư duy (Mindmap) chuẩn hóa và viết bản giải trình hệ thống (`summary.md`).

Mindmap của bạn cần thể hiện rõ cách thức Python xử lý các toán tử thông qua các bài toán nghiệp vụ khách sạn cụ thể: tính tổng tiền thanh toán, số tuần/ngày lẻ stay, xác thực hạng thẻ Loyalty, phê duyệt mã giảm giá VIP, và kiểm tra danh sách hạn chế (Blacklist).

---

### **3. Quy tắc nghiệp vụ**
Sơ đồ tư duy BẮT BUỘC bao phủ 4 nhánh kiến thức chính với các từ khóa và mã nguồn minh họa nghiệp vụ `HOTEL_BOOKING`:

#### **Nhánh 1: Toán tử Số học (Arithmetic Operators) trong Tính hóa đơn Khách sạn**
- **Toán tử cơ bản**: `+` (cộng tiền dịch vụ), `-` (trừ voucher giảm giá), `*` (nhân đơn giá phòng với số đêm), `/` (chia trả ra float).
- **Toán tử đặc biệt**:
  - `//` (Chia lấy phần nguyên): Tính số tuần lưu trú đầy đủ (`stay_nights // 7`).
  - `%` (Chia lấy phần dư): Tính số ngày lẻ còn lại sau khi quy đổi ra tuần (`stay_nights % 7`).
  - `**` (Lũy thừa): Tính phí phạt trễ hạn theo công thức lãi kép hoặc hệ số tăng giá mùa cao điểm.
- *Ví dụ minh họa nghiệp vụ*:

```python
total_nights = 17
weeks_stay = total_nights // 7

# 2 tuần
extra_nights = total_nights % 7

# 3 ngày lẻ
room_rate = 2000000
total_raw = total_nights * room_rate
```

# **Nhánh 2: Toán tử So sánh (Comparison Operators) trong Kiểm tra Điều kiện Đặt phòng**
- **Các toán tử**: `==` (bằng), `!=` (khác), `>` (lớn hơn), `<` (nhỏ hơn), `>=` (lớn hơn hoặc bằng), `<=` (nhỏ hơn hoặc bằng).
- **Kiểu dữ liệu trả về**: Luôn là `Boolean` (`True` / `False`).
- *Nghiệp vụ áp dụng*: So sánh số dư tài khoản của khách với tiền cọc phòng, so sánh điểm loyalty (`loyalty_points >= 1000`), kiểm tra phòng trống (`available_rooms > 0`).

#### **Nhánh 3: Toán tử Logic (Logical Operators) & Đánh giá Ngắn mạch (Short-circuit Evaluation)**
- **Toán tử `and`**: Trả về `True` khi TẤT CẢ các điều kiện thành phần là `True`. (Ví dụ: Khách đủ tuổi AND có căn cước hợp lệ).
- **Toán tử `or`**: Trả về `True` khi CÓ ÍT NHẤT MỘT điều kiện thành phần là `True`. (Ví dụ: Đạt hạng thẻ VIP OR có mã Voucher đặc biệt).
- **Toán tử `not`**: Đảo ngược giá trị logic. (`not is_blacklisted` -> Khách không thuộc danh sách đen).
- **Cơ chế Short-circuit**:
  - Trong `and`: Nếu mệnh đề đầu là `False`, Python dừng đánh giá mệnh đề sau.
  - Trong `or`: Nếu mệnh đề đầu là `True`, Python dừng đánh giá mệnh đề sau.

#### **Nhánh 4: Thứ tự Ưu tiên Tính toán (Operator Precedence) trong Biểu thức Phê duyệt**
- Thứ tự ưu tiên từ cao xuống thấp:
  1. Dấu ngoặc đơn `()` (Ưu tiên tuyệt đối).
  2. Lũy thừa `**`.
  3. Nhân, Chia, Chia nguyên, Chia dư `*`, `/`, `//`, `%`.
  4. Cộng, Trừ `+`, `-`.
  5. Toán tử so sánh `==`, `!=`, `>`, `<`, `>=`, `<=`.
  6. Toán tử logic `not`.
  7. Toán tử logic `and`.
  8. Toán tử logic `or`.
- *Mã nguồn mẫu nghiệp vụ phê duyệt ưu đãi phòng*:

```python

# Thông tin hồ sơ đặt phòng khách sạn
account_balance = 45000000
loyalty_points = 750
is_vip_guest = True
is_blacklisted = False

# Kiểm tra điều kiện 1: Đủ số dư cọc HOẶC là khách VIP
is_eligible_tier = (account_balance >= 50000000) or is_vip_guest

# Kiểm tra điều kiện 2: Đạt điểm Loyalty tối thiểu (>= 700)
is_score_qualified = loyalty_points >= 700

# Phê duyệt booking: (Đủ điều kiện hạng khách AND Đạt điểm) AND KHÔNG bị hạn chế (not blacklisted)
is_approved = (is_eligible_tier and is_score_qualified) and (not is_blacklisted)

print("Kết quả nhóm điều kiện ưu tiên:", is_eligible_tier)

# True
print("Kết quả kiểm tra điểm loyalty:", is_score_qualified)

# True
print("Kết quả phê duyệt đặt phòng cuối cùng:", is_approved)

# True
```

---

### **4. Yêu cầu bài toán (Sản phẩm nộp)**
Học viên cần hoàn thiện và nộp bộ sản phẩm bao gồm:
1. **File ảnh Sơ đồ tư duy** (`mindmap.png` hoặc `mindmap.jpg`): Trực quan, phối màu rõ ràng theo phân cấp (Root node -> Main branches -> Sub-branches -> Code Examples).
2. **File thiết kế gốc** (`mindmap.xmind` hoặc `mindmap.pdf`): Chứa đầy đủ dữ liệu cấu trúc mindmap.
3. **Bản tóm tắt giải trình Markdown** (`summary.md`):
   - Giải thích chi tiết logic các nhánh trong Mindmap.
   - Phân tích ví dụ biểu thức phê duyệt phòng khách sạn và lý do thứ tự thực thi toán tử tạo ra kết quả chính xác.
   - Chỉ ra 3 lỗi phổ biến học viên hay gặp phải (ví dụ: nhầm lẫn `=` và `==`, sai thứ tự `and`/`or` khi không dùng ngoặc, dùng `/` thay vì `//` dẫn đến sai kiểu dữ liệu).

---

### **5. Yêu cầu nộp bài**
Học viên nộp bài theo quy chuẩn GitHub:
* Đẩy toàn bộ mã nguồn, file thiết kế và sơ đồ lên GitHub Repository theo cấu trúc tên: `[Tên Lớp]_[Môn Học]_Session04_Mindmap`.
  - *Ví dụ*: `HNKS25CNTT1_PythonCore_Session04_Mindmap`
* Cấu trúc thư mục repository:

```text
  ├── mindmap.png (hoặc mindmap.jpg)
  ├── mindmap.xmind (hoặc mindmap.pdf)
  └── summary.md
```
