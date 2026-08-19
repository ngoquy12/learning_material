# **Tiêu chí chấm điểm (AI / Mentor)**

**[Tổng hợp Mindmap] Hệ thống Kiến thức & Sơ đồ Tư duy (Mindmap) — Tổng điểm: 100 điểm**

---

#### **1. Độ bao phủ kiến thức & Từ khóa trọng tâm — 30 điểm**
- **[10 điểm]** Thể hiện đầy đủ và chính xác cú pháp, bản chất hoạt động của `if / else if / else` (Lesson 01). Có minh họa bẫy sắp xếp thứ tự kiểm tra khoảng giá trị và tầm quan trọng của khối scope `{}`.
- **[10 điểm]** Thể hiện đầy đủ cú pháp `switch-case`, `break`, `default` (Lesson 02). Chỉ rõ bẫy trôi lệnh (Fall-through) khi quên `break` và bẫy so sánh bằng nghiêm ngặt `===`.
- **[10 điểm]** Thể hiện chính xác cú pháp toán tử ba ngôi `? :` (Lesson 03). Phân định rõ trường hợp nên dùng (gán giá trị đơn giản) và cảnh báo lỗi chống mẫu lồng ghép ba ngôi (Nested Ternary).

#### **2. Phân tầng logic & Mối liên kết — 30 điểm**
- **[15 điểm]** Cấu trúc cây sơ đồ tư duy có tính phân tầng logic chặt chẽ (Root Node -> Main Branches -> Sub-branches -> Technical Details -> Anti-patterns).
- **[15 điểm]** Tích hợp sáng tạo và hợp lý bối cảnh hệ thống **AIRLINE_CHECKIN** (Tính phí hành lý quá cước, Định tuyến trạng thái Check-in, Gán lối đi ưu tiên Fast-Track) vào từng nhánh kiến thức tương ứng.

#### **3. Trực quan hóa & Định dạng xuất file — 20 điểm**
- **[10 điểm]** Thiết kế sơ đồ có tính thẩm mỹ: Phối màu có ý đồ (Phân biệt giữa Thực hành tốt - Good practice và Bẫy lỗi - Anti-patterns), biểu tượng icon minh họa trực quan, bố cục cân đối.
- **[10 điểm]** Đầy đủ các định dạng xuất file theo yêu cầu (File ảnh `.png`/`.jpg` chất lượng cao + File thiết kế gốc `.xmind`/`.pdf`/`.drawio`).

#### **4. Bản tóm tắt giải trình (summary.md) — 10 điểm**
- **[5 điểm]** Giải thích rõ ràng luồng tư duy rẽ nhánh logic và nguyên tắc chọn lựa giữa `if-else`, `switch-case` và `Ternary Operator` trong dự án thực tế.
- **[5 điểm]** Có mã nguồn minh họa minh bạch bằng JavaScript chuẩn Clean Code cho cả 3 kịch bản nghiệp vụ AIRLINE_CHECKIN (Có so sánh mẫu code đúng vs mẫu code dính lỗi anti-pattern).

#### **5. Quy chuẩn nộp bài GitHub — 10 điểm**
- **[5 điểm]** Cấu trúc Repository và tên thư mục đặt chuẩn theo định dạng yêu cầu: `[Tên Lớp]_[Môn Học]_Session06_Mindmap`.
- **[5 điểm]** Commit message rõ ràng, file `summary.md` được định dạng Markdown chuẩn mực, đẹp mắt, không bị lỗi hiển thị.
