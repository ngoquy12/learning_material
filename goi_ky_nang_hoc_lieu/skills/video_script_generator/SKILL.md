---
name: video_script_generator
description: Generate a complete Lesson-Level Video Shooting Script (kịch bản quay video) combining teleprompter narration with scene-by-scene visual/camera cues, exported as Markdown (SCRIPT.md) inside the 'Video' folder. Target output language is 100% Accented Vietnamese.
---

# Video Script Generator Skill — Rikkei Education Standards

## 0. Nguồn tổng hợp

Skill này hợp nhất 3 nguồn tham khảo thành 1 chuẩn duy nhất, đầy đủ nhất:

1. **Chuẩn nội dung/kỹ thuật chính thức** (`resources/TIÊU CHUẨN XÂY DỰNG HỆ THỐNG VIDEO.pdf`) —
   quyết định cấu trúc 3 phần bắt buộc, độ dài, phân loại theo dạng bài học.
2. **Prompt "action mode"** (kịch bản dạng bảng VISUAL/SCRIPT) từ hệ thống tham chiếu
   `backend-nestjs` — quyết định việc mỗi phân cảnh phải tách rõ "hiển thị gì" và "nói gì".
3. **Prompt "narration mode"** (kịch bản lời thoại thuần) từ cùng hệ thống tham chiếu — quyết định
   câu mở đầu/kết thúc thương hiệu bắt buộc, quy tắc chuyển đoạn tự nhiên, yêu cầu ví dụ code trong
   lời giảng.

Khác với 2 nguồn tham khảo (vốn tách rời 2 chế độ, chọn 1 trong 2), skill này **hợp nhất cả hai
thành MỘT định dạng duy nhất, đầy đủ nhất**: mỗi phân cảnh vừa có lời thoại giảng viên (narration)
vừa có chú thích hình ảnh/hành động đi kèm (visual cue) — giảng viên vừa biết nói gì, vừa biết làm
gì trên màn hình tại đúng thời điểm đó, không cần chọn giữa 2 định dạng rời rạc.

---

## 1. Tổng quan & Định hướng sư phạm

Kịch bản video là bản thiết kế chi tiết để giảng viên **quay trực tiếp trước camera** — không phải
bài đọc, không phải slide. Video là kênh sư phạm dùng **văn phong đối thoại (conversational tone)**,
KHÔNG lặp lại nguyên văn slide hay bài đọc.

- **100% linh động theo `tech_stack`/`chosen_domain`** truyền vào — TUYỆT ĐỐI không hard-code cú
  pháp/ví dụ của bất kỳ ngôn ngữ/công nghệ cụ thể nào trong skill này; mọi ví dụ dưới đây chỉ mang
  tính minh họa định dạng.
- Toàn bộ ví dụ nghiệp vụ trong 1 kịch bản phải khớp đúng **Domain SSOT** đã ấn định cho session
  (nếu có `chosen_domain` truyền vào) — không tự bịa bối cảnh khác.
- Nội dung chỉ được dùng kiến thức trong `allowed_scope`, tuyệt đối không vượt `forbidden_scope`.

---

## 2. Phân loại Video theo dạng bài học (bắt buộc xác định trước khi soạn)

Theo đúng chuẩn kỹ thuật chính thức, mỗi kịch bản PHẢI được soạn theo ĐÚNG 1 trong 3 dạng sau —
xác định dựa vào bản chất lesson (`lesson_title`/`core_ssot`), không đoán chung chung:

| Dạng bài | Khi nào dùng | Trọng tâm phần "Nội dung chính" |
|---|---|---|
| **A. Giới thiệu** (Introduction lesson) | Lesson mở đầu môn/session, định hướng lộ trình | Liệt kê đề mục toàn bài lớn, giải thích ngắn gọn từng đề mục, gây ấn tượng lý do cần học |
| **B. Lý thuyết** (Theory lesson) | Lesson dạy khái niệm/cú pháp mới | Đặt câu hỏi "nếu không có kiến thức này thì sao?" → giải quyết bằng ví dụ thực tế → chốt khái niệm kỹ thuật chuẩn |
| **C. Thực hành** (Practice lesson) | Lesson ứng dụng giải bài toán thực tế | Mô hình hóa các bước giải quyết (có thể mô tả sơ đồ luồng bằng lời) → áp dụng đúng quy trình vào 1 bài toán thực tế cụ thể |

---

## 3. Cấu trúc 3 phần bắt buộc (Mở đầu — Nội dung chính — Kết luận)

Mọi kịch bản, bất kể dạng nào ở mục 2, đều phải theo đúng khung 3 phần:

### PHẦN 1 — MỞ ĐẦU (Introduction)
- **Câu mở đầu bắt buộc, nguyên văn, không đổi**:
  > "Chào mừng các em đã quay trở lại với hệ thống Elearning của Rikkei Education, trong nội dung
  > bài học này, chúng ta sẽ cùng nhau tìm hiểu về {chủ đề lesson}."
- Theo dạng bài (mục 2): Giới thiệu → liệt kê đề mục; Lý thuyết → nêu khái niệm sắp học; Thực hành
  → nêu bài toán/phương pháp sắp áp dụng.
- Gây ấn tượng, giải thích ngắn gọn lý do học viên cần xem hết video.

### PHẦN 2 — NỘI DUNG CHÍNH (Main content)
- Đặt câu hỏi tình huống / kể tình huống thực tế nhỏ liên quan chủ đề trước khi đi vào chi tiết kỹ
  thuật (KHÔNG liệt kê định nghĩa khô khan ngay từ đầu).
- **Chuyển đoạn tự nhiên bắt buộc** giữa các tiểu mục — dùng các cụm nối kiểu: "Bây giờ chúng ta
  cùng chuyển sang phần tiếp theo", "Các em lưu ý phần quan trọng này nhé" (không lặp lại y hệt 2
  lần trong cùng 1 video).
- **Bắt buộc ≥ 1 ví dụ code/thao tác cụ thể** minh họa khi giảng lý thuyết, đặt trong khối Markdown
  \`\`\`{tech_stack}\`\`\`, đồng bộ đúng cú pháp `tech_stack` được truyền vào.
- Với dạng Thực hành: phải có tối thiểu 1 bài toán thực tế áp dụng trọn vẹn quy trình vừa mô tả.

### PHẦN 3 — KẾT LUẬN (Conclusion)
- Tóm tắt ý chính ngắn gọn bằng lời (không liệt kê dài dòng).
- Lời kêu gọi hành động (Call to Action) — khuyến khích học viên thực hành/ôn lại.
- **TUYỆT ĐỐI KHÔNG** thêm phần "Kiến thức mở rộng" ở cuối (làm loãng trọng tâm bài học).
- **Câu kết thúc bắt buộc, nguyên văn, không đổi**:
  > "Cảm ơn các em đã theo dõi, hẹn gặp lại trong các bài học tiếp theo."

---

## 4. Cấu trúc phân cảnh (Scene Structure) — hợp nhất Visual + Script

Nội dung PHẦN 2 (và có thể cả Phần 1/3 nếu có hành động đặc biệt) được chia thành các **Phân cảnh
(Scene)** đánh số tuần tự. Mỗi phân cảnh PHẢI có đủ 3 trường:

1. **Thời lượng ước tính** (`00:00 - 00:45` dạng phút:giây, cộng dồn hợp lý theo tổng thời lượng).
2. **Hành động/Hình ảnh** (Visual cue) — mô tả NGẮN GỌN (1 dòng) những gì xuất hiện trên màn hình
   tại thời điểm đó: chuyển slide, gõ code trực tiếp, chạy chương trình, hiển thị sơ đồ, zoom vào
   dòng lệnh cụ thể...
3. **Lời thoại** (Script/Narration) — CHỈ chứa lời giảng viên nói, văn phong đối thoại tự nhiên;
   dùng **`[Chú thích]`** in đậm giữa lời thoại để đánh dấu 1 hành động nhỏ đồng thời (vd
   **[Gõ dòng lệnh trên màn hình]**) khi cần nhấn mạnh đồng bộ lời nói với thao tác.

---

## 5. Ràng buộc thời lượng & văn phong (Kỹ thuật)

- **Độ dài lý tưởng: 3–7 phút.** Độ dài tối đa tuyệt đối: **15 phút**.
- Nếu nội dung lesson quá dài để vừa 15 phút, PHẢI chủ động chia thành nhiều video con theo từng
  tiểu mục, mỗi video vẫn tuân đủ khung 3 phần ở mục 3 (không cắt cụt giữa chừng).
- Văn phong đối thoại (Conversational tone) — tránh thuật ngữ hàn lâm không giải thích; nếu bắt
  buộc dùng thuật ngữ kỹ thuật, phải giải thích ngay bằng ví dụ đời thường.
- 100% tiếng Việt có dấu chuẩn sản xuất. Nghiêm cấm text emoji, từ ngữ sáo rỗng AI ("thực chiến",
  "khai phá", "vô cùng", "tuyệt vời", "bậc nhất", "triệt để").
- Nghiêm cấm các cụm quy chiếu nguồn trung gian gây khó hiểu khi tách rời khỏi ngữ cảnh gốc (ví dụ
  "như đã thấy ở slide trước", "theo tài liệu đã đọc") — kịch bản video phải tự đầy đủ ngữ nghĩa,
  không phụ thuộc học viên đã xem tài nguyên khác.

---

## 6. Chuẩn file đầu ra (`SCRIPT.md`)

Lưu tại `Video/SCRIPT.md`. Cấu trúc Markdown bắt buộc:

```markdown
# Kịch bản Video: [Tên lesson thuần túy, không tiền tố Session/Lesson]

> **Dạng bài:** [Giới thiệu / Lý thuyết / Thực hành]
> **Thời lượng dự kiến:** [X phút Y giây]
> **Công nghệ/Môn học:** {{ tech_stack }}

## PHẦN 1 — MỞ ĐẦU

### Phân cảnh 1 (00:00 - 00:XX)
**Hình ảnh/Hành động:** [Mô tả 1 dòng]

**Lời thoại:**
Chào mừng các em đã quay trở lại với hệ thống Elearning của Rikkei Education, trong nội dung bài
học này, chúng ta sẽ cùng nhau tìm hiểu về [chủ đề lesson]. [Tiếp tục dẫn dắt theo dạng bài...]

## PHẦN 2 — NỘI DUNG CHÍNH

### Phân cảnh 2 (00:XX - 00:XX)
**Hình ảnh/Hành động:** [Mô tả 1 dòng]

**Lời thoại:**
[Đặt vấn đề/tình huống thực tế...] **[Chú thích hành động nếu có]** [tiếp tục lời thoại...]

\`\`\`{tech_stack}
# Ví dụ code minh họa đồng bộ đúng lời thoại đang giảng
\`\`\`

### Phân cảnh 3 (00:XX - 00:XX)
...(lặp lại theo số lượng tiểu mục cần thiết, không giới hạn cứng số phân cảnh)

## PHẦN 3 — KẾT LUẬN

### Phân cảnh cuối (00:XX - 00:XX)
**Hình ảnh/Hành động:** [Mô tả 1 dòng]

**Lời thoại:**
[Tóm tắt ý chính...] [Lời kêu gọi hành động...] Cảm ơn các em đã theo dõi, hẹn gặp lại trong các
bài học tiếp theo.
```

---

## 7. Checklist tuân thủ

- [ ] Đã xác định đúng 1 trong 3 dạng bài (Giới thiệu/Lý thuyết/Thực hành) và áp dụng đúng trọng
      tâm Phần 2 tương ứng.
- [ ] Đủ khung 3 phần Mở đầu — Nội dung chính — Kết luận.
- [ ] Câu mở đầu và câu kết thúc đúng NGUYÊN VĂN bắt buộc.
- [ ] Mỗi phân cảnh có đủ 3 trường: thời lượng, hình ảnh/hành động, lời thoại.
- [ ] Có ít nhất 1 ví dụ code/thao tác cụ thể đúng `tech_stack`, đặt trong khối Markdown.
- [ ] Tổng thời lượng ước tính trong khoảng 3–15 phút; nếu vượt 15 phút đã được chia nhỏ hợp lý.
- [ ] Không có phần "Kiến thức mở rộng" ở cuối.
- [ ] Bối cảnh nghiệp vụ khớp Domain SSOT của session (nếu có `chosen_domain`).
- [ ] Không vượt phạm vi kiến thức (`forbidden_scope`).
- [ ] Không có text emoji, từ ngữ sáo rỗng AI, hoặc cụm quy chiếu nguồn trung gian.
