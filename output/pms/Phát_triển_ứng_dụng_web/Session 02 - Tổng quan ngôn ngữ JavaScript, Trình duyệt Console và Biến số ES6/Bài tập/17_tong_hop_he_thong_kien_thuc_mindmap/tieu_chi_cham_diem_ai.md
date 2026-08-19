# **Tiêu chí chấm điểm (AI / Mentor)**

**[Tổng hợp Mindmap] Hệ thống Kiến thức & Sơ đồ Tư duy (Mindmap) — Tổng điểm: 100 điểm**

---

#### **1. Độ bao phủ kiến thức & Từ khóa trọng tâm (30 điểm)**
- **Phản ánh đủ 4 nhánh kiến thức cốt lõi (15 điểm)**:
  - [3.75đ] Nhánh 1: Cơ chế V8 Engine (HTML Parser -> RAM -> Ignition Bytecode), vị trí đặt thẻ `<script>`.
  - [3.75đ] Nhánh 2: Runtime Environment (Browser Console vs Node.js), Live Server HTTP vs `file:///`.
  - [3.75đ] Nhánh 3: Biến ES6 (`const`, `let`, `var`), Scope, Hoisting, Quy chuẩn đặt tên camelCase.
  - [3.75đ] Nhánh 4: Nhập/xuất dữ liệu (`prompt`, `alert`, `console.log`), ép kiểu `Number()`, Template Literals.
- **Tích hợp ngữ cảnh thực tế CLINIC_APPOINTMENT (15 điểm)**:
  - Các khái niệm và ví dụ trên sơ đồ được lồng ghép chuẩn xác vào bài toán Đặt lịch khám (ví dụ: `patientName`, `consultationFee`, `appointmentId`, tính tổng phí dịch vụ y tế).

---

#### **2. Phân tầng logic & Mối liên kết (30 điểm)**
- **Cấu trúc phân cấp mạch lạc (15 điểm)**:
  - Sơ đồ tư duy chia rõ từ Root Node (Session 02 JS Core) -> Main Branches (4 bài học) -> Sub-branches (Kiến thức chi tiết) -> Leaf Nodes (Ví dụ mã nguồn/Lỗi thường gặp).
- **Phân tích bẫy lập trình & Giải pháp (15 điểm)**:
  - Chỉ rõ các anti-patterns: Dùng `var` làm ô nhiễm scope, đặt thẻ script chặn DOM render, lỗi cộng chuỗi do quên dùng `Number()` khi đọc dữ liệu từ `prompt()`.
  - Đưa ra giải pháp chuẩn ES6 khắc phục hoàn toàn các lỗi trên.

---

#### **3. Trực quan hóa & Định dạng xuất file (20 điểm)**
- **Tính thẩm mỹ và dễ đọc (10 điểm)**:
  - Sử dụng màu sắc phân biệt giữa các nhánh logic, icon minh họa trực quan, chữ viết rõ ràng, không đè vạch liên kết.
- **Định dạng và đầy đủ file (10 điểm)**:
  - Có đủ file ảnh (`.png`/`.jpg`) chất lượng cao và file thiết kế gốc (`.xmind`/`.pdf`) trong thư mục `docs/`.

---

#### **4. Bản tóm tắt giải trình (summary.md) (10 điểm)**
- **Trình bày chuẩn Markdown (5 điểm)**:
  - Đầy đủ tiêu đề, bảng biểu so sánh (`const`/`let`/`var`), khối mã nguồn (code block) có highlight ngữ pháp JS/HTML.
- **Nội dung giải trình sâu sắc (5 điểm)**:
  - Giải thích mạch lạc luồng thực thi JS trong V8 Engine và viết được đoạn mã JS ngắn minh họa bài toán Đặt lịch khám bệnh đúng quy chuẩn ES6.

---

#### **5. Quy chuẩn nộp bài GitHub (10 điểm)**
- **Tên Repository & Cấu trúc thư mục (5 điểm)**:
  - Đặt đúng định dạng `[Tên Lớp]_[Môn Học]_Session02_Mindmap`.
  - Phân chia thư mục `docs/`, `src/` và file `summary.md` chuẩn yêu cầu.
- **Cam kết mã nguồn (Git Commits) (5 điểm)**:
  - Lịch sử commit rõ ràng, mô tả thông điệp commit đúng quy chuẩn (ví dụ: `feat: add mindmap image and summary documentation`).
