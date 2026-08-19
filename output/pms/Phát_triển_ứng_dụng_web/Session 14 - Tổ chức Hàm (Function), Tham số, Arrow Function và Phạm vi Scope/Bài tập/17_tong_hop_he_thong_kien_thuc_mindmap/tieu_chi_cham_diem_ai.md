### **Tiêu chí chấm điểm (AI / Mentor)**

**[Tổng hợp Mindmap] Hệ thống Kiến thức & Sơ đồ Tư duy (Mindmap) — Tổng điểm: 100 điểm**

---

#### **1. Độ bao phủ kiến thức & Từ khóa trọng tâm — 30 điểm**
- **Đạt tối đa (30 điểm)**:
  - Bao phủ 100% kiến thức của Session 14 bao gồm: Function Declaration, Function Expression, Hoisting, Call Stack Frame, Arrow Function, Implicit Return, Object Literal Return `()`, Default Parameters, Global Scope, Local/Block Scope, Lexical Scope, Closure và Private State.
  - Các từ khóa trọng tâm được phân loại chính xác vào từng nhánh.
- **Mức Khá (20 - 29 điểm)**: Bao phủ được 80-90% kiến thức, thiếu 1-2 khái niệm nâng cao (như Return Object Literal hoặc bẫy lỗi mặc định với `0`).
- **Mức Trung bình (10 - 19 điểm)**: Chỉ trình bày được các khái niệm hàm cơ bản, bỏ qua Closure hoặc Phạm vi Scope.
- **Mức Đạt tối thiểu (1 - 9 điểm)**: Sơ đồ quá sơ sài, thiếu trên 50% từ khóa cốt lõi.

---

#### **2. Phân tầng logic & Mối liên kết nghiệp vụ EVENT_TICKETING — 30 điểm**
- **Đạt tối đa (30 điểm)**:
  - Sơ đồ tư duy được chia nhánh chính/phụ cực kỳ khoa học, mạch lạc (Tối thiểu 3 nhánh chính ứng với 3 nội dung lớn).
  - Tích hợp nhuần nhuyễn ngữ cảnh nghiệp vụ bán vé sự kiện (**EVENT_TICKETING**) vào các nút (nodes) của sơ đồ (VD: Tính giá vé VIP, Phí đặt chỗ, Mã voucher ưu đãi, Bộ đếm vé giữ chỗ closure).
- **Mức Khá (20 - 29 điểm)**: Phân tầng tốt nhưng các ví dụ/từ khóa chưa thể hiện rõ đặc thù của domain EVENT_TICKETING (còn mang tính lý thuyết chung chung).
- **Mức Trung bình (10 - 19 điểm)**: Cấu trúc nhánh bị lộn xộn, xếp sai thứ tự quan hệ cha - con giữa các khái niệm (VD: Đặt Closure ngang hàng với Function).
- **Mức Đạt tối thiểu (1 - 9 điểm)**: Các nhánh không có tính liên kết, trình bày dạng danh sách liệt kê phẳng thay vì dạng cây tư duy.

---

#### **3. Trực quan hóa & Định dạng xuất file — 20 điểm**
- **Đạt tối đa (20 điểm)**:
  - Nộp đầy đủ cả 2 file: File thiết kế gốc (`.xmind`/`.drawio`/`.pdf`) và file ảnh (`.png`/`.jpg`).
  - Ảnh xuất ra có độ phân giải cao, sắc nét, không bị vỡ chữ.
  - Sử dụng màu sắc, icon, hiệu ứng hình ảnh hợp lý để phân biệt rõ các cấp độ nhánh (Level 1, Level 2, Level 3).
- **Mức Khá (15 - 19 điểm)**: Nộp đủ file nhưng phối màu chưa hài hòa hoặc chữ hơi nhỏ, khó đọc ở một số nhánh sâu.
- **Mức Trung bình (8 - 14 điểm)**: Chỉ nộp 1 trong 2 loại file (chỉ có ảnh hoặc chỉ có file gốc), hoặc file ảnh bị mờ.
- **Mức Đạt tối thiểu (1 - 7 điểm)**: Không nộp được file sơ đồ trực quan.

---

#### **4. Bản tóm tắt giải trình (summary.md) & Code minh họa — 10 điểm**
- **Đạt tối đa (10 điểm)**:
  - File `summary.md` giải thích sâu sắc các mối liên kết trong sơ đồ.
  - Chứa đủ **3 đoạn mã nguồn minh họa** (chuẩn JavaScript ES6+, chạy được trên Node.js) áp dụng trực tiếp cho hệ thống bán vé **EVENT_TICKETING**:
    1. Ví dụ tính tổng hóa đơn vé (Function Declaration/Expression).
    2. Ví dụ tính tiền vé sau chiết khấu voucher & tạo đối tượng giỏ vé (Arrow Function + Default Params).
    3. Ví dụ đóng gói bộ đếm vé tự tăng/giảm độc lập (Closure).
- **Mức Khá (7 - 9 điểm)**: Có giải trình và mã nguồn nhưng thiếu 1 ví dụ hoặc mã nguồn chưa bám sát nghiệp vụ EVENT_TICKETING.
- **Mức Trung bình (4 - 6 điểm)**: File `summary.md` quá sơ sài, chỉ copy lại tiêu đề bài học mà không có mã nguồn minh họa.
- **Mức Đạt tối thiểu (1 - 3 điểm)**: Không có file `summary.md`.

---

#### **5. Quy chuẩn nộp bài GitHub — 10 điểm**
- **Đạt tối đa (10 điểm)**:
  - Tên Repository đặt đúng cú pháp quy định.
  - Cấu trúc thư mục ngăn nắp, chứa đúng tên các file yêu cầu (`mindmap.png`, `summary.md`, ...).
  - Commit message viết đúng chuẩn kĩ thuật (`feat: ...`).
- **Mức Khá (7 - 9 điểm)**: Đặt tên Repo đúng nhưng commit message chưa chuẩn hóa hoặc thừa file rác.
- **Mức Trung bình (4 - 6 điểm)**: Đặt sai tên Repository hoặc nộp thiếu file trên GitHub.
- **Mức Đạt tối thiểu (0 điểm)**: Không nộp link GitHub hoặc Repo để chế độ Private.