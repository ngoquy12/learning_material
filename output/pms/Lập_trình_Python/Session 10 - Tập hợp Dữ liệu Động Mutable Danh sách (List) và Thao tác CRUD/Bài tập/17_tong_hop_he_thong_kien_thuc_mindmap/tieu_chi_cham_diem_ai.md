# **Tiêu chí chấm điểm (AI / Mentor)**

**[Tổng hợp Mindmap] Hệ thống Kiến thức & Sơ đồ Tư duy (Mindmap) — Tổng điểm: 100 điểm**

#### **1. Độ bao phủ kiến thức & Từ khóa trọng tâm — 30 điểm**
- **Đầy đủ khái niệm (15 điểm):** Bao phủ chính xác các khái niệm: Tính chất Mutable của List, cú pháp gán cập nhật `list[i] = val`, câu lệnh xóa `del list[i]`, cơ chế dịch chuyển chỉ số (Index Shifting), hàm đếm độ dài `len()`, và lỗi `IndexError`.
- **Ánh xạ miền nghiệp vụ GRAB_RIDE (15 điểm):** Lồng ghép thành công ngữ cảnh quản lý chuyến xe/cước phí GRAB_RIDE vào các ví dụ và nhánh kiến thức trên sơ đồ.

#### **2. Phân tầng logic & Mối liên kết — 30 điểm**
- **Cấu trúc phân cấp (15 điểm):** Sơ đồ tư duy phân nhánh rõ ràng từ Root Node (List & Thao tác CRUD trong Python) đến các Branch cấp 1 (Khái niệm & Mutable, Thao tác Update, Thao tác Delete, Hàm len(), lỗi thường gặp & Best Practices) và các Sub-branches chi tiết.
- **Tính liên kết logic (15 điểm):** Thể hiện được mối quan hệ giữa việc thay đổi/xóa phần tử với sự thay đổi kết quả của hàm `len()` và sự dịch chuyển chỉ số của danh sách.

#### **3. Trực quan hóa & Định dạng xuất file — 20 điểm**
- **Tính thẩm mỹ & Trực quan (10 điểm):** Sử dụng màu sắc phân loại nhánh hợp lý, biểu tượng (icons) minh họa trực quan, font chữ dễ đọc, không đè chữ.
- **Định dạng file nộp (10 điểm):** Xuất đầy đủ file ảnh chất lượng cao (`.png`/`.jpg`) và file gốc thiết kế (`.xmind`/`.pdf`).

#### **4. Bản tóm tắt giải trình (summary.md) — 10 điểm**
- Có file `summary.md` giải thích chi tiết ý tưởng thiết kế sơ đồ.
- Chứa đoạn mã minh họa chuẩn Python 3.12 (có Type Hints, chuẩn PEP 8) mô phỏng chính xác kịch bản GRAB_RIDE:

```python

# Ví dụ minh họa kịch bản GRAB_RIDE
  cuoc_phi_chuyen_xe: list[float] = [35.0, 50.0, 120.0, 45.0, 80.0]

# Cập nhật cước phí chuyến số 2 do tính phụ phí mưa
  cuoc_phi_chuyen_xe[2] = 140.0

# Xóa chuyến xe bị khách hủy tại chỉ số 1
  del cuoc_phi_chuyen_xe[1]

# Đếm số chuyến xe hợp lệ còn lại
  so_chuyen_con_lai: int = len(cuoc_phi_chuyen_xe)
```

# **5. Quy chuẩn nộp bài GitHub — 10 điểm**
- Repository đặt tên đúng cấu trúc quy định: `[Tên Lớp]_[Môn Học]_Session10_Mindmap`.
- Thư mục nộp bài ngăn nắp, có file `README.md` hoặc `summary.md` mô tả chi tiết, commit message rõ ràng.
