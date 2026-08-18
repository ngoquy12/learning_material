### **Tiêu chí chấm điểm (AI / Mentor)**

**[Tổng hợp Mindmap] Hệ thống Kiến thức & Sơ đồ Tư duy (Mindmap) — Tổng điểm: 100 điểm**

---

#### **1. Độ bao phủ kiến thức & Từ khóa trọng tâm — 30 điểm**
- ** Object Literal & Truy cập thuộc tính (10 điểm):**
  - Thể hiện rõ cấu trúc Key-Value.
  - Phân biệt chính xác Dot Notation và Bracket Notation.
  - Giải thích đúng cơ chế Dynamic Key Access (truy cập key thông qua biến).
- ** Thao tác CRUD Thuộc tính (10 điểm):**
  - Đầy đủ các thao tác: Create (Thêm), Read (Đọc), Update (Sửa), Delete (Xóa bằng toán tử `delete`).
  - Phân tích hậu quả của việc dùng `undefined` thay vì `delete`.
- ** Cấu trúc JSON & Bẫy lỗi nghiệp vụ (10 điểm):**
  - Trình bày đúng vai trò và cú pháp của `JSON.stringify()` và `JSON.parse()`.
  - Bao phủ đủ 4 bẫy lỗi chính (`ReferenceError`, `SyntaxError`, lãng phí bộ nhớ với `undefined`, và lỗi truy cập thuộc tính trên chuỗi JSON chưa được `parse`).

---

#### **2. Phân tầng logic & Mối liên kết — 30 điểm**
- ** Tầng nút trung tâm (Root Node) (5 điểm):** Đặt tên rõ ràng, làm nổi bật chủ đề *Session 12: Object & JSON trong HOTEL_BOOKING*.
- ** Tầng nhánh chính (Main Branches) (10 điểm):** Chia thành 3-4 nhánh chính logic, không bị chồng chéo khái niệm.
- ** Tầng nhánh phụ (Sub-branches) & Minh họa nghiệp vụ (15 điểm):** 
  - Phân tầng chi tiết từ khái niệm lý thuyết đến cú pháp mã nguồn và ví dụ thực tế trong bài toán Đặt phòng khách sạn (ví dụ: `bookingTicket`, `customerProfile`).
  - Thể hiện được mối liên kết giữa việc khai báo Object -> Biến đổi CRUD -> Đóng gói JSON truyền dữ liệu.

---

#### **3. Trực quan hóa & Định dạng xuất file — 20 điểm**
- ** Trực quan & Thẩm mỹ (10 điểm):** Sử dụng màu sắc phân biệt giữa các nhánh, icon minh họa bẫy lỗi (Cảnh báo/Bẫy lỗi/Thực hành tốt), chữ viết rõ ràng, không đè chữ.
- ** Định dạng tệp tin đầy đủ (10 điểm):** Có đủ file ảnh (`.png`/`.jpg`) sắc nét và file gốc (`.xmind`/`.pdf`) theo đúng yêu cầu bài toán.

---

#### **4. Bản tóm tắt giải trình (summary.md) — 10 điểm**
- ** Cấu trúc văn bản (3 điểm):** Trình bày mạch lạc bằng định dạng Markdown, có tiêu đề, danh sách, khối mã nguồn (code block).
- ** Minh họa Code JavaScript thực tế (4 điểm):** Cung cấp mã nguồn ví dụ hoàn chỉnh chạy không lỗi, áp dụng domain `HOTEL_BOOKING` (Khai báo đối tượng đặt phòng -> Thêm thuộc tính động -> Xóa token tạm bằng `delete` -> Chuyển sang JSON và ngược lại).
- ** Giải thích bẫy lỗi sâu sắc (3 điểm):** Phân tích rõ nguyên nhân và cách khắc phục cho 4 bẫy lỗi trọng tâm của buổi học.

---

#### **5. Quy chuẩn nộp bài GitHub — 10 điểm**
- ** Đặt tên Repository chuẩn (5 điểm):** Đúng cú pháp `[Tên Lớp]_[Môn Học]_Session12_Mindmap` (Ví dụ: `HNKS25CNTT1_Core_Session12_Mindmap`).
- ** Cấu trúc thư mục đúng quy chuẩn (5 điểm):** Đẩy đầy đủ các file `mindmap.png` (hoặc `.jpg`), `mindmap.xmind` (hoặc `.pdf`), và `summary.md` lên thư mục gốc của repository.