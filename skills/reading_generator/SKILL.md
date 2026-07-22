---
name: reading_generator
description: Generate rich, interactive, W3Schools-style educational reading materials with step-by-step Code Trackers, Good vs. Bad code comparison cards, Note/Warning callouts, and comprehensive theory explanations.
---

# Kỹ năng Xây dựng Bài đọc Học liệu Chuẩn W3Schools (W3Schools Educational Standard Skill)

## 1. Triết lý Đào tạo Chuẩn W3Schools (W3Schools Educational Philosophy)
Tài liệu bài đọc tự học (`reading.html`) đóng vai trò là **Nguồn Sự Thật Duy Nhất (Single Source of Truth - SSOT)** cho toàn bộ môn học. Tất cả các tài nguyên khác (Slide, Quiz, Kịch bản Video, Mindmap) đều được trích xuất từ bài đọc này.

11: Bài đọc phải đạt tiêu chuẩn W3Schools:
12: 1. **Rõ ràng, trực quan, đi thẳng vào bản chất (Clean & Direct)**: Giải thích dễ hiểu, cấu trúc chuẩn hóa, typography hiện đại.
13: 2. **Độ sâu lý thuyết & Bối cảnh doanh nghiệp (Deep & Practical Theory)**: Bài đọc đầy đủ 400 - 800 từ, giải thích cơ chế vận hành nội bộ (low-level internals), không viết ngắn tóm tắt 100 từ.
14: 3. **TUYỆT ĐỐI CẤM SỬ DỤNG EMOJI (Emoji Icons Forbidden)**: Tuyệt đối KHÔNG sử dụng biểu tượng cảm xúc/emoji (như ℹ️, 💡, ⚠️, ✅, ❌, 🚀, 🔥,...) trong toàn bộ bài đọc, bài tập, slide. Sử dụng văn bản thuần túy `[GHI CHÚ]`, `[MẸO]`, `[CẢNH BÁO]`, `[BEST PRACTICE]`, `[ANTI-PATTERN]` hoặc Phosphor Icon dạng HTML `<i class="ph-duotone ph-...">`.
15: 4. **Đối chiếu Mã nguồn Đúng vs. Sai (Good vs. Bad Code Comparison)**:
16:    - **[BEST PRACTICE] GOOD Example**: Khối code chuẩn doanh nghiệp, tối ưu, dễ bảo trì kèm giải thích lý do.
17:    - **[ANTI-PATTERN] BAD Example**: Khối code hay bị lỗi, kém hiệu quả kèm giải thích bẫy cú pháp.
18: 5. **Thẻ ghi chú W3Schools Callouts (Note, Tip, Warning Boxes)**:
19:    - `[NOTE] Note Box`: Nhấn mạnh kiến thức trọng tâm.
20:    - `[TIP] Tip Box`: Mẹo viết code nhanh và tối ưu.
21:    - `[WARNING] Warning Box`: Cảnh báo lỗi nguy hiểm và bẫy khi chạy production.
22: 6. **Khu vực Trực quan hóa Code (Try It Yourself / Interactive Code Tracker)**:
23:    - Cho phép học viên theo dõi dòng lệnh đang chạy (`active-line`), bấm nút thử nghiệm, quan sát Console Log thời gian thực.
24: 7. **Bảng So sánh Markdown Chuẩn W3Schools (Mandatory Comparison Tables)**:
25:    - Mọi nội dung so sánh khái niệm, cú pháp hay phương pháp BẮT BUỘC phải được thiết lập dạng BẢNG MARKDOWN COMPARISON TABLE với chiều dài 100% màn hình (thay vì đoạn văn bản text) với tối thiểu 3-4 tiêu chí so sánh trực quan.

---

## 2. Cấu Trúc Bố Cục Bài Đọc W3Schools (W3Schools Document Architecture)

```
+───────────────────────────────────────────────────────────────────────────────────────────────+
| [Header/Navbar]  TÊN MÔN HỌC & BÀI HỌC • Badges: [Thực Tiễn • Sáng Tạo • W3Schools Standard] |
+───────────────────────────────────────────────────────────────────────────────────────────────+
| 1. KHÁI NIỆM & BỐI CẢNH THỰC TẾ (Introduction & Real-world Problem)                           |
| • Giải thích rõ ràng bài toán thực tế doanh nghiệp gặp phải.                                  |
| • [ℹ️ W3Schools Note Box]: Nhấn mạnh điểm quan trọng.                                         |
+───────────────────────────────────────────────────────────────────────────────────────────────+
| 2. CÚ PHÁP & CƠ CHẾ VẬN HÀNH NỘI BỘ (Syntax & Low-Level Internals)                             |
| • Phân tích cú pháp chi tiết từng tham số/dòng lệnh.                                          |
| • [💡 W3Schools Tip Box]: Mẹo viết code sạch (Clean Code).                                     |
+───────────────────────────────────────────────────────────────────────────────────────────────+
| 3. ĐỐI CHIẾU MÃ NGUỒN: ĐÚNG (BEST PRACTICE) VS SAI (ANTI-PATTERN)                             |
| +──────────────────────────────────────────────┬────────────────────────────────────────────+ |
| | ✅ GOOD Example (Best Practice)              | ❌ BAD Example (Anti-Pattern / Common Bug)  | |
| | code_good_here...                            | code_bad_here...                           | |
| +──────────────────────────────────────────────┴────────────────────────────────────────────+ |
+───────────────────────────────────────────────────────────────────────────────────────────────+
| 4. TRỰC QUAN HÓA MÃ NGUỒN & CODE TRACKER (Interactive Playground / Try it Yourself)           |
| • Live Code Tracker highlight dòng lệnh đang chạy.                                           |
| • Console Log nhật ký hệ thống thời gian thực.                                               |
+───────────────────────────────────────────────────────────────────────────────────────────────+
| 5. LƯU Ý QUAN TRỌNG & BẪY LẬP TRÌNH (Important Warnings & Pitfalls)                           |
| • [⚠️ W3Schools Warning Box]: Cảnh báo các lỗi đắt giá khi chạy thực tế.                      |
+───────────────────────────────────────────────────────────────────────────────────────────────+
| 6. BỘ CÂU HỎI TỰ KHẢO THÍ & BÀI TẬP THỰC HÀNH (Self-Test & Exercises)                          |
| • <details> Câu hỏi tự khảo thí kèm đáp án chi tiết </details>                                |
+───────────────────────────────────────────────────────────────────────────────────────────────+
```

---

## 3. Quy Chuẩn Kỹ Thuật CSS W3Schools Callouts

```css
/* W3Schools Callout Note Boxes */
.w3-note {
    background-color: #eff6ff;
    border-left: 6px solid #3b82f6;
    color: #1e3a8a;
    padding: 16px;
    border-radius: 8px;
    margin: 16px 0;
}

.w3-tip {
    background-color: #f0fdf4;
    border-left: 6px solid #10b981;
    color: #065f46;
    padding: 16px;
    border-radius: 8px;
    margin: 16px 0;
}

.w3-warning {
    background-color: #fef2f2;
    border-left: 6px solid #ef4444;
    color: #991b1b;
    padding: 16px;
    border-radius: 8px;
    margin: 16px 0;
}
```

---

## 5. Quy Chuẩn Kỹ Thuật JavaScript & Chống Reload Trang (Strict JS & Anti-Reload Rules)
1. **Bắt buộc 100% thẻ `<button>` phải khai báo `type="button"`**:
   - Mọi nút bấm trong giao diện bài đọc và bảng điều khiển trực quan hóa (Visualizer Panel) tuyệt đối phải ghi rõ `<button type="button" ...>` để ngăn ngừa hành vi tự động reload/submit form của trình duyệt.
2. **Chống Reload khi click hoặc bấm Enter**:
   - Tất cả các sự kiện click, gõ phím trong form hoặc input phải có `event.preventDefault()` để tránh làm trang bị tải lại.
3. **Mã nguồn Trực quan hóa chi tiết (Detailed Code Visualizer Logic)**:
   - Bộ Visualizer phải mô phỏng chính xác từng bước chạy mã nguồn theo thời gian thực (Step-by-step Execution Tracker).
   - Phải có 3 phân vùng hiển thị đồng bộ:
     a) **Code Tracker Box**: Highlight dòng lệnh đang chạy (`.active-line`).
     b) **Memory State / Variable Table**: Hiển thị tên biến, kiểu dữ liệu và giá trị biến thay đổi theo từng bước.
     c) **Console Execution Log**: Nhật ký log hiển thị kết quả in ra màn hình hoặc trạng thái hệ thống.
4. **Cô lập Scope JavaScript**:
   - Mã nguồn JS phải tự chứa (self-contained), khai báo biến và hàm chuẩn xác, không được dùng stub `// todo` hay dùng biến chưa khai báo.

---

## 6. Tiêu Chuẩn Phê Duyệt Bài Đọc (Approval Rubric)
1. **Độ chính xác ngữ cảnh**: Bài đọc chỉ tập trung 100% vào nội dung Lesson hiện tại, không rò rỉ môn khác hay kiến thức chưa học.
2. **Độ sâu học thuật**: Giải thích đầy đủ cơ chế, không tóm tắt dưới 200 từ.
3. **Có khối Good vs. Bad Code**: Bắt buộc có khối ví dụ đối chiếu mã đúng vs mã sai.
4. **Trực quan hóa hoạt động**: Khung Code Tracker / Playground hoạt động tương tác thực sự trên trình duyệt, không reload trang.
