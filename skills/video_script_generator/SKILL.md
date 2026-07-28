---
name: video_script_generator
description: Sinh kịch bản video HyperFrames (Production Blueprint JSON) cho bài học E-learning theo chuẩn dev-tutorial-video. Bao gồm scene structure, audio architecture, GSAP timeline và design system.
---

# Video Script Generator — HyperFrames Production Standard

Skill này hướng dẫn **Video Director Agent** tạo ra `Production Blueprint JSON` — kịch bản sản xuất chuẩn HyperFrames cho mỗi bài học.

---

## 1. Pipeline Tổng Quan (3 Agents Khép Kín)

```
video_script_agent          ← Đọc Bài Đọc (reading.md) & sinh Production Blueprint JSON
       ↓
video_script_reviewer_agent ← Validate theo 9 tiêu chí HyperFrames
       ↓ (APPROVED)
hyperframes_writer_agent    ← Ghi file HTML/JSON ra đĩa & Gọi Smart G2P TTS Normalizer
```

> [!IMPORTANT]
> **QUY TẮC PHIÊN ÂM THUẬT NGỮ TỰ ĐỘNG (SMART AUTOMATED G2P PIPELINE):**
> Hệ thống TTS Kokoro-Vietnamese đã tích hợp **Smart G2P & Tech Normalizer Engine** tự động. Kịch bản và lời thoại **HOÀN TOÀN TỰ ĐỘNG** chuyển đổi các từ tiếng Anh (`Python`, `TypeError`, `ValueError`, `VS Code`, `snake_case`, `PVM`...) và CamelCase Exception classes thành phiên âm tự nhiên. Người biên soạn **KHÔNG CẦN** ngồi nhập thủ công từ điển phiên âm.

> [!IMPORTANT]
> **QUY TẮC BẮT BUỘC HÌNH ẢNH MINH HỌA & ẢNH GENERATE (DYNAMIC IMAGE & ASSET GENERATION):**
> Mỗi Scene trong video **BẮT BUỘC** phải có hình ảnh minh họa đồ họa công nghệ (`.png` / `.jpg`). Agent **BẮT BUỘC** sử dụng công cụ `generate_image` để tự động tạo các bức ảnh 3D Tech Concept / Infographic Banners chất lượng cao cho từng Scene tại thư mục `Video/{lesson_slug}/assets/images/`, sau đó nhúng trực tiếp vào HTML. Tuyệt đối không dùng 100% chữ HTML trần trụi.

---

## 2. Đầu Vào Bắt Buộc (Input Source: Bài Đọc)

Agent **BẮT BUỘC** phải lấy nội dung từ **Bài Đọc (`reading.md`)** của bài học làm nguồn tri thức duy nhất (SSOT):

1. **Đọc Bài Đọc gốc**: Đọc toàn bộ nội dung file Bài Đọc (`reading.md` / `reading_generator`) tương ứng với lesson/session cần làm video.
2. **Cô đọng kiến thức**: Trích xuất các khái niệm chính, giải thích cú pháp, các khối mã nguồn (code snippet) và các lưu ý/lỗi thường gặp từ bài đọc.
3. **Đồng bộ Lời thoại & Hình ảnh**:
   - Lời thoại (Narration) phải cô đọng ngắn gọn nhưng đúng chuẩn các thuật ngữ trong Bài Đọc.
   - Minh họa trực quan (Visuals/Code display) phải lấy đúng ví dụ mẫu và biến mẫu có trong Bài Đọc.

---

## 3. Output Format — Production Blueprint JSON

Agent **PHẢI** trả về JSON với cấu trúc sau:

```json
{
  "lesson_slug": "session_01_lesson_02_list_python",
  "lesson_title": "Tổng quan về List trong Python",
  "total_duration": 187.84,
  "scenes": [
    {
      "scene_id": "Scene_01",
      "scene_title": "Tại sao phải dùng List?",
      "start_at_root": 0,
      "duration": 38.84,
      "track_index": 1,
      "narration": "Chào mừng các em đã quay trở lại với hệ thống Elearning của Rikkei Education...",
      "visual_description": "Màn hình chia đôi. Bên trái: code biến rời gạch bỏ. Bên phải: List code xanh.",
      "html_structure": "split-container, panel-left (code cũ), panel-right (code mới)",
      "animation_timeline": [
        "0.0s: tl.set('.clip', {autoAlpha:1}, 0)",
        "0.2s: intro-title fade in",
        "3.2s: intro-title lên góc trên-trái",
        "4.5s: split-container slide in",
        "6.0s: code-left hiện từng dòng",
        "12.0s: strikethrough effect",
        "18.0s: code-right bounce in"
      ]
    }
  ],
  "tts_scripts": {
    "Scene_01": "Chào mừng các bạn đã quay trở lại với hệ thống Elearning của Rikkei Education. ...",
    "Scene_02": "...",
    "Scene_Last": "... Cảm ơn các bạn đã theo dõi, hẹn gặp lại trong bài học tiếp theo!"
  }
}
```

**Ràng buộc bắt buộc:**
- `start_at_root[N] = sum(duration[0..N-1])`
- `total_duration = sum(all scene durations)`
- `track_index` của scenes: 1, 2, 3, ... (tăng dần)
- Audio tracks: 20, 21, 22, ... (được gán trong `index.html`)

## 4. Quy tắc Narration (Lời Thoại & Thời Lượng Thong Thả Sâu Sắc)

> [!IMPORTANT]
> **QUY TẮC NỘI DUNG CHI TIẾT NGHÊM NGẶT NGAY TỪ BAN ĐẦU (INITIAL DEEP-DETAIL BLUEPRINT):**
> **NGHIÊM CẤM** việc sinh ra kịch bản hời hợt, vắn tắt 2–3 phút để rồi sau đó phải sửa đổi từng bài học thủ công.
> Ngay từ lần khởi tạo đầu tiên, Agent **BẮT BUỘC** phải viết kịch bản chi tiết, chuyên sâu, mở rộng đầy đủ 7–10 Scene với đầy đủ ví dụ mã nguồn thực tế, phân tích cơ chế dưới hood, câu lệnh CLI từng bước và các tình huống thực chiến.

| Tiêu chí | Yêu cầu chuẩn |
|----------|---------------|
| **Tổng Thời Lượng Video** | **5 – 8 Phút (300s – 480s)** / bài học (Chưa bao gồm Intro & Outro). Tuyệt đối không sinh kịch bản dưới 4.5 phút. |
| **Thời Lượng / Scene** | **35s – 60s** / scene (Tổng số: **7 – 10 Scenes** / bài học). |
| **Tổng Số Từ Lời Thoại** | **1,200 – 1,800 từ** / bài học (Giảng giải tỉ mỉ, thong thả, sư phạm). |
| **Số Từ / Scene** | **140 – 220 từ** / scene. |
| **Tốc Độ Đọc & Ngắt Nghỉ** | Tốc độ đọc thong thả, từ tốn (`speed = 0.9` – `1.0`). Bắt buộc chèn đầy đủ dấu phẩy `,`, dấu chấm `.`, dấu hai chấm `:` để giọng đọc ngắt nghỉ tự nhiên, sư phạm. |
| **Lời Mở Đầu (BẮT BUỘC SCENE 01)** | **BẮT BUỘC** câu đầu tiên của `Scene_01` phải là: `"Chào mừng các bạn đã quay trở lại với hệ thống Elearning của Rikkei Education. Trong nội dung bài học này, chúng ta sẽ cùng tìm hiểu về [Tên_Bài_Học]."` |
| **Lời Tạm Biệt & Giới Thiệu Bài Tiếp (BẮT BUỘC SCENE CUỐI)** | **BẮT BUỘC** đoạn cuối Scene phải tóm tắt nội dung đã học, dẫn vào bài tiếp theo: `"Như vậy, trong bài học này chúng ta đã [tóm tắt]. Trong bài học tiếp theo, chúng ta sẽ tìm hiểu về [Tên_Bài_Học_Tiếp_Theo]. Xin cảm ơn và hẹn gặp lại."` Đồng thời UI Banner bài học tiếp theo **phải xuất hiện đồng bộ** trên màn hình. |
| **Hành văn & Từ Nối Chuyển Cảnh (BẮT BUỘC TỰ NHIÊN)** | **BẮT BUỘC** sử dụng các từ nối, câu dẫn dắt sư phạm tự nhiên giữa các ý và giữa các Scene (*"Hãy cùng đặt câu hỏi...", "Thế nhưng trong thực tế...", "Vậy giải pháp ở đây là...", "Tiếp theo, chúng ta sẽ chuyển sang...", "Lưu ý quan trọng ở bước này là..."*). **KHÔNG ĐƯỢC** đọc liệt kê khô khan như đọc slide. |
| **Cấu Trúc Kịch Bản (BẮT BUỘC ĐẶT VẤN ĐỀ TRƯỚC)** | **BẮT BUỘC** tuân theo cấu trúc **Bối cảnh -> Vấn đề/Pain point -> Giải pháp -> Thực thi mã nguồn sản xuất**. Tuyệt đối không nhảy ngay vào định nghĩa/giải pháp khi người học chưa hiểu rõ lý do và ứng dụng thực tế. |
| **Văn Phong Giảng Viên Đại Học (BẮT BUỘC)** | Phong cách giảng dạy bậc đại học: mạch lạc, chuyên sâu kỹ thuật, trung lập cảm xúc. Xưng hô chuẩn: **"chúng ta"** (không dùng *"các em"*, *"các bạn ơi"*). Cấm tuyệt đối mọi từ ngữ sến súa, kích động hoặc thiếu chuyên nghiệp — xem danh sách đầy đủ ở **Section 4.3**. |

---

## 4.1. Quy Triệu Cấu Trúc Sư Phạm: Đặt Vấn Đề Trước — Giải Pháp Sau (Problem-First Narrative)

Mỗi bài học / khái niệm trong kịch bản **BẮT BUỘC** phải đi qua 4 bước sư phạm:

1. **Bước 1: Tình Huống / Bối Cảnh Thực Tế (Real-world Scenario)**
   - Mô tả tình huống thực tế mà kỹ sư phần mềm gặp phải trong các dự án công nghệ (Ví dụ: *"Khi xây dựng tính năng thanh toán ngân hàng..."*).
2. **Bước 2: Nêu Vấn Đề & Hậu Quả (Pain Point & Consequence)**
   - Nêu rõ khó khăn, rủi ro lỗi logic hoặc hiệu năng nếu xử lý theo cách thông thường (Ví dụ: *"Nếu không ép kiểu dữ liệu chuỗi sang số, phép tính sẽ ghép chuỗi thay vì cộng số, dẫn đến sai lệch tài chính nghiêm trọng..."*).
3. **Bước 3: Đưa Ra Giải Pháp & Khái Niệm Cốt Lõi (Solution & Concept)**
   - Giới thiệu khái niệm/công nghệ như một lời giải tự nhiên cho vấn đề trên (Ví dụ: *"Đó là lý do Python cung cấp hàm ép kiểu int() để giải quyết triệt để vấn đề này..."*).
4. **Bước 4: Minh Họa Mã Nguồn & Kết Quả (Code Demo & Verification)**
   - Đưa ra ví dụ mã nguồn thực tế và giải thích từng dòng lệnh giúp học viên áp dụng trực tiếp vào công việc.

---

## 4.2. Quy Tắc Từ Nối Chuyển Cảnh Tự Nhiên (Conversational Transitions)

Mỗi chuyển giao giữa các phân cảnh và các ý giảng giải **MUST (BẮT BUỘC)** sử dụng bộ từ nối sư phạm sinh động:

- **Mở đầu bài toán**: *"Hãy cùng tưởng tượng một tình huống thực tế...", "Trong quá trình phát triển dự án..."*
- **Nêu thách thức**: *"Thế nhưng, một vấn đề lớn đặt ra ở đây là...", "Nếu chỉ làm theo cách thông thường, chúng ta sẽ gặp rắc rối khi..."*
- **Chuyển sang giải pháp**: *"Vậy làm thế nào để giải quyết vấn đề này?...", "Đó chính là lý do ngôn ngữ cung cấp cơ chế..."*
- **Chuyển sang Code Demo**: *"Để thấy rõ cách hoạt động, hãy cùng quan sát đoạn mã nguồn sau...", "Bây giờ, chúng ta hãy cùng thực thi đoạn lệnh này..."*
- **Chuyển cảnh mới**: *"Tiếp nối khái niệm này, chúng ta sẽ chuyển sang một phần cực kỳ quan trọng...", "Sau khi đã hiểu rõ nguyên lý, bước tiếp theo chúng ta cần lưu ý..."*

---

## 4.3. Quy Tắc Giọng Văn Giảng Viên Đại Học & Danh Sách Từ Ngữ Bị Cấm (Academic Lecturer Tone & Forbidden Words Policy)

> [!CAUTION]
> **NGHIÊM CẤM TUYỆT ĐỐI (ZERO TOLERANCE).** Bất kỳ từ ngữ nào trong danh sách dưới đây xuất hiện trong `narration` hoặc `tts_scripts` sẽ khiến Reviewer Agent **TỪ CHỐI (REJECT)** kịch bản ngay lập tức và yêu cầu viết lại toàn bộ phân cảnh vi phạm.

### A. Tiêu Chuẩn Giọng Văn Giảng Viên Đại Học

| Tiêu Chí | Quy Tắc Bắt Buộc |
|---|---|
| **Xưng hô** | Chỉ dùng **"chúng ta"** (ngôi số nhiều trung lập). NGHIÊM CẤM: *"các em"*, *"các em ơi"*, *"các bạn ơi"*, *"các bạn nhé"*, *"mọi người"* |
| **Giọng điệu** | Trung lập, mạch lạc, chuyên nghiệp như bài giảng tại giảng đường. Không huyên thuyên, không cảm thán thái quá |
| **Câu kết thúc ý** | Dùng cấu trúc phân tích rõ ràng: *"Như vậy...", "Kết luận rút ra là...", "Điều này có nghĩa là..."*. NGHIÊM CẤM kết thúc bằng *"nhé!"*, *"nha!"*, *"đó nha!"* |
| **Mức độ cảm xúc** | Tập trung vào lập luận kỹ thuật, ví dụ thực tế và hậu quả logic. NGHIÊM CẤM dùng ngôn ngữ kịch tính hóa để gây sợ hãi hoặc kích thích |
| **Kết thúc video** | Kết thúc lịch sự, ngắn gọn: *"Xin cảm ơn và hẹn gặp lại."*. NGHIÊM CẤM: *"Cảm ơn các em nhiều lắm!"*, *"Thích thì like nhé!"* |

### B. Danh Sách Từ Ngữ Bị Cấm Tuyệt Đối

**Nhóm 1 — Từ sến súa / thân mật quá mức:**
```
nhé, nha, nhen, ha, nghen, ơi, ơi các em, các em ơi, các em thân mến,
bạn ơi, mọi người ơi, các bạn thân mến, chúc các em, chúc các bạn,
yêu cầu, cố lên, cố gắng nhé, học tốt nhé, thành công nhé
```

**Nhóm 2 — Từ kích động / gây hoảng sợ / chết chóc:**
```
chết, chết chóc, chết người, giết, bị chết, tiêu tùng, tiêu rồi,
thảm họa, thảm khốc, thảm bại, thất bại thảm hại, sụp đổ hoàn toàn,
nguy hiểm chết người, cực kỳ nguy hiểm, rất đáng sợ, kinh khủng,
khủng khiếp, hãi hùng, ghê gớm, nguy to rồi, lỗi chết người
```

**Nhóm 3 — Từ phóng đại thái quá / thiếu nghiêm túc:**
```
siêu, cực siêu, cực kỳ tuyệt vời, tuyệt đỉnh, đỉnh của đỉnh,
huyền thoại, thần thánh, vô địch, bá đạo, ảo diệu, điên đảo,
xịn xò, ngầu lòi, hack não, ngộp thở, bùng nổ, cháy hết mình
```

**Nhóm 4 — Từ khích lệ thiếu chuyên nghiệp:**
```
like, subscribe, share, đăng ký kênh, nhấn chuông, ủng hộ kênh,
comment bên dưới, hãy chia sẻ, nếu thích thì, nếu hay thì
```

### C. Bảng So Sánh Trước/Sau (Before/After Examples)

| ❌ SAI — Cấm dùng | ✅ ĐÚNG — Giảng viên đại học |
|---|---|
| *"Các em ơi, nhớ nhé!"* | *"Đây là điểm cần lưu ý."* |
| *"Tuyệt vời quá các bạn ơi!"* | *"Như vậy, chúng ta đã hiểu được cơ chế hoạt động."* |
| *"Lỗi này chết người lắm đó!"* | *"Đây là lỗi phổ biến dẫn đến sai lệch logic nghiêm trọng."* |
| *"Nếu hay thì nhớ like nhé!"* | *(Không đề cập. Kết thúc bằng giới thiệu bài tiếp theo.)* |
| *"Cố lên các em nhé!"* | *"Để củng cố, chúng ta sẽ thực hành thêm ở bài tiếp theo."* |
| *"Thảm họa sẽ xảy ra nếu..."* | *"Trường hợp không xử lý điều kiện này, hệ thống sẽ trả về lỗi runtime."* |
| *"Chào mừng các em thân mến!"* | *"Chào mừng các bạn quay trở lại với hệ thống Elearning của Rikkei Education."* |

---

## 5. Quy tắc Layout, Animation Timeline & Nhịp Điệu UI (Spacious Keyframing & Time Offset)

### A. Layout Tiêu Đề Top Header Bar (CHỐNG ĐÈ GIAO DIỆN):
- **NGHIÊM CẤM** việc đặt tiêu đề khổng lồ ở giữa màn hình rồi phóng to/thu nhỏ đè lên các thẻ nội dung!
- **BẮT BUỘC** sử dụng **Scene Header Bar** đặt ở vị trí cố định trên cùng (`top: 50px; left: 60px`):
  ```html
  <div class="scene-header">
    <div class="header-badge">PYTHON BASE</div>
    <h1 class="scene-title">Thách Thức Tốc Độ Sản Xuất Phần Mềm</h1>
  </div>
  ```

### B. Quy Tắc CSS Initial Hiding (CHỐNG HIỆN TRƯỚC / FLASH ELEMENT):
- **BẮT BUỘC**: Tất cả phần tử UI xuất hiện theo animation (`.main-layout`, `.concept-card`, `.step-node`, `.side-card`, `.vscode-window`, `.recap-container`) **PHẢI** khai báo `opacity: 0; visibility: hidden;` trong thẻ `<style>` CSS nguyên bản. Đảm bảo khi nạp frame 0 không bị hiện trước cả đống UI.

### C. Trừ Thời Gian Lời Chào & Lời Tạm Biệt (Voice Time Offset):
1. **Scene 01 (Trừ Lời Chào ~4.5s–5.0s)**:
   - Trong `0s – 5.0s` khi voice đang đọc câu chào *"Chào mừng các bạn..."*, màn hình **CHỈ HIỂN THỊ** Header Bar và nền hiệu ứng.
   - Thẻ UI nội dung chính **CHỈ ĐƯỢC XUẤT HIỆN TỪ mốc 5.0s+** khi lời thoại chuyển sang kiến thức chuyên môn.
2. **Scene Cuối Cùng (Trừ Lời Tạm Biệt ~7.0s–8.0s)**:
   - Thẻ tổng kết và Banner bài tiếp theo phải xuất hiện hoàn chỉnh trước mốc `DURATION - 8.0s`. Khi voice cất lời *"Cảm ơn các bạn đã theo dõi..."*, màn hình đã sẵn sàng đầy đủ thông tin.

### D. Timeline GSAP Nhịp Điệu Thong Thả:
```
0.0s  → tl.set(".clip", { autoAlpha: 1 }, 0)             ← BẮT BUỘC ĐẦU TIÊN
0.3s  → Header Bar fade in (top: 50px)
5.0s  → Thẻ UI 1 xuất hiện (Sau khi xong câu chào)     ← BẮT BUỘC 5.0s+ CHO SCENE 01
11.0s → Thẻ UI 2 / Step 1 xuất hiện                      ← Khoảng nghỉ ≥ 4.0s
17.0s → Thẻ UI 3 / Step 2 xuất hiện                      ← Khoảng nghỉ ≥ 4.0s
...
{DUR-0.8}s → tl.to("#scene-XX", { autoAlpha: 0, duration: 0.8 }) ← Clean Fade-Out
{DUR}s     → tl.set({}, {}, {DUR})                      ← BẮT BUỘC CUỐI TIMELINE
```

---

## 6. Chia Scene theo Loại Bài Học

**Theory Lesson (5-6 scenes):**
1. **Giới thiệu & Vấn đề** — Hook, bài toán thực tế
2. **Khái niệm cốt lõi** — Definition, so sánh
3. **Code Demo** — Code block reveal, syntax highlight
4. **Áp dụng thực tế** — Use case, example
5. **Lỗi thường gặp** — Pitfalls, warnings
6. **Tổng kết** — Key takeaways, CTA

**Practical Lesson (4-5 scenes):**
1. **Lab Setup** — Mục tiêu, môi trường
2. **Bước 1-2** — Hướng dẫn từng bước
3. **Bước 3-4** — Coding walkthrough
4. **Test & Debug** — Chạy thử, xử lý lỗi
5. **Kết quả & Review** — Verify output

---

## 7. Design System & Layout Standard (BẮT BUỘC tuân theo Light Theme Standard)

```
Background: #f8fafc canvas + linear-gradient(135deg, #f8fafc 0%, #edf2f7 100%) + dark dot grid overlay (rgba(15,23,42,0.08))
Font text: Be Vietnam Pro (font-family: 'Be Vietnam Pro', sans-serif)
Font code: Monospace Fira Code (font-family: 'Fira Code', monospace)
Brand Logo: Fixed top-right Rikkei logo (top: 50px; right: 80px; height: 52px; z-index: 100)
Main Title: Top-left title (top: 50px; left: 80px; font-size: 44px; font-weight: 800; color: #ba252a - Rikkei Red)
Alignment: 100% Strict Left-Alignment (text-align: left !important) for all text elements
Text colors: #0f1117 / #0f172a (Slate 900 for text)
Cards: #ffffff + 1.5px solid #e2e8f0 + 6px solid #ba252a left border + border-radius 14px + box-shadow(0 8px 20px rgba(15,23,42,0.04))
Code Container: #ffffff + 1.5px solid #cbd5e1 + 5px solid #ba252a top border + Fira Code monospace + tab-size 4
Canvas: 1920×1080px, overflow hidden
```

**QUY TẮC ICON & TỪ NGỮ GIAO DIỆN (UI):**
1. **NGHIÊM CẤM DÙNG EMOJI TRÊN UI**: Sử dụng 100% SVG Vector Icons (`<svg>...</svg>`) cho mọi nhãn, nút, badge, sidebar.
2. **PHÂN TÁCH 100% GIỮA TTS SCRIPT VÀ UI DISPLAY**:
   - `TTS Script` (để đọc voice): Dùng phiên âm (`Pai-thừn`, `snếch-kê-xơ`, `P-Vi-Em`) để mô hình đọc tiếng Anh chuẩn.
   - `UI Display Text` (hiển thị hình ảnh): **BẮT BUỘC** dùng từ chuẩn tiếng Anh / tiếng Việt kỹ thuật: `Python`, `snake_case`, `PVM`, `compiler`, `PEP 8`.
3. **KHÔNG DÁN ĐOẠN VĂN DÀI LÊN UI**: Giao diện UI chỉ chứa Keywords, Bullet Points (tối đa 5–10 từ), Code Snippets hoặc Diagrams. Không bao giờ chép lại nguyên đoạn văn lời thoại lên UI.
4. **FADE-OUT CLEAN CUỐI SCENE**: Ở 0.8s cuối của mỗi Scene timeline, **BẮT BUỘC** fade out toàn bộ scene (`tl.to("#scene-XX", {autoAlpha:0, duration:0.8})`) để tránh đè layout sang Scene tiếp theo hoặc Outro video.
5. **CẤM SỬA LẺ TỪNG VIDEO**: Tất cả video bài học phải được sinh và đóng gói tự động thông qua quy chuẩn SKILL và UIComponentRenderer chuẩn.
6. **NGHIÊM CẤM ĐƯỜNG DẪN Ổ ĐĨA TỦ MÁY TÍNH (WORKSPACE-RELATIVE PATHS ONLY)**: **BẮT BUỘC** tất cả các đường dẫn tệp trong cấu hình, tài liệu, kịch bản, mã nguồn script và tham chiếu (link) PHẢI xuất phát từ thư mục gốc của dự án (ví dụ: `Kokoro-Vietnamese/configs/tech_dictionary.json`, `skills/video_script_generator/SKILL.md`). **NGHIÊM CẤM** việc ghi đường dẫn tuyệt đối bắt đầu từ ổ đĩa máy tính (`d:\...`, `C:\...`, `file:///d:...`).

---

## 7.1. Quy Tắc Kịch Bản Video Chuyên Nghiệp Quốc Tế (6 Advanced Features)

Để kịch bản đạt trình độ sản xuất chuyên nghiệp đỉnh cao như các kênh công nghệ quốc tế (*Fireship, ByteByteGo*), kịch bản **PHẢI** tích hợp 6 tính năng sau:

1. **Scene Live-Debugging & Pitfall Scene (BẮT BUỘC ÍT NHẤT 1 SCENE)**:
   - Kịch bản không chỉ dạy Happy Path mà **phải có ít nhất 1 Scene cố tình tạo lỗi thực tế** (`TypeError`, `AttributeError`, `HTTP 500`).
   - Giảng viên đọc Stack trace, phân tích dòng code lỗi và hướng dẫn sửa lại mã nguồn chuẩn.

2. **Director Cue Markups (Thẻ Đạo Diễn Kỹ Thuật trong Lời Thoại)**:
   - Nhúng trực tiếp các thẻ chỉ dẫn vào `narration` để hỗ trợ giọng đọc TTS và hiệu ứng GSAP:
     - `[stress: từ_khóa]`: Nhấn giọng ngắt nghỉ tại từ khóa quan trọng.
     - `[zoom: line_12-15]`: Ra lệnh GSAP tự động phóng to (Zoom-in) vào vị trí code/element tương ứng.
     - `[pause: 1.5s]`: Tạo khoảng dừng để học viên kịp suy ngẫm thông tin phức tạp.

3. **Cognitive Load & Pacing Control (Quản Lý Nhịp Điệu Bài Giảng)**:
   - Mỗi Scene khai báo thuộc tính `pacing_mode`:
     - `"fast_hook"` (Intro / Đặt vấn đề): Tốc độ đọc nhanh, sôi nổi (`speed = 1.05`).
     - `"dense_code"` (Lý thuyết khó/Code phức tạp): Tốc độ đọc thong thả (`speed = 0.88`), có khoảng dừng.
     - `"recap_outro"` (Tóm tắt): Nhịp điệu dứt khoát, chắc chắn.

4. **Semantic Code Reading Protocol (Quy Tắc Đọc Code Theo Ý Nghĩa Nghiệp Vụ)**:
   - Tuyệt đối không đọc vẹt từng ký tự cú pháp (`if i == 0:`).
   - Đọc theo bản chất nghiệp vụ (Ví dụ: *"Nếu người dùng chưa đăng nhập, hệ thống sẽ chuyển hướng sang trang Login"*).

5. **Micro-Engagement Checkpoints (Thử Thách Tương Tác 5 Giây)**:
   - Ở giữa video (Scene 4 hoặc 5), kịch bản chèn 1 mốc thử thách tương tác: Màn hình dừng lại với 1 câu hỏi tình huống ngắn và đếm ngược 3..2..1 trước khi hé lộ đáp án.

6. **Data-Flow Continuity (Nối Mạch Thị Giác Dữ Liệu)**:
   - Khai báo `continuity_anchor` (ví dụ: `"#user-dto-card"`) để phần tử dữ liệu chuyển động mềm mại giữa các Scene liên tiếp.

7. **UI Visual Buffer for Greetings (Intro Hero Banner & Outro Next-Lesson Banner)**:
   - **Scene 01 (Lời Chào Mở Đầu)**: Từ `0.0s ➔ 3.2s` (khi cất lời chào thương hiệu), màn hình hiển thị **Hero Brand Banner** (Badge Rikkei Education + Hero Title 72px + Subtitle Lộ trình) nằm chính giữa màn hình. Ở `3.2s`, Hero Banner thu nhỏ (`scale: 0.38`) và di chuyển lên góc trên-trái thành Header Bar cố định trước khi UI chính xuất hiện lúc `4.0s`.
   - **Scene Cuối (Lời Tạm Biệt & Kết Thúc)**: Hiển thị Thẻ Tổng Kết Key Takeaways kết hợp với **Next Lesson Preview Banner** viền tím gradient phát sáng (`[ TIẾP TỤC ➔ ]`) để lấp đầy khoảng trống lời tạm biệt trước khi chuyển sang Video Outro.

---

## 8. Quy Trình Bắt Buộc: Phân Tích Kịch Bản & Tự Huấn Luyện Từ Điển Đọc (Pre-TTS Phonetic Analysis & Dictionary Training)

**TRƯỚC KHI SINH BẤT KỲ VOICE TTS NÀO, AGENT BẮT BUỘC PHẢI:**
1. **Quét (Scan) toàn bộ kịch bản lời thoại (Narration Text)**: Tìm tất cả các từ viết tắt (Abbreviations: `PVM`, `PEP`, `IDE`, `API`, `HTML`, `CSS`, `VS Code`...), thuật ngữ tiếng Anh khó đọc (`Python`, `snake_case`, `Guido van Rossum`, `TypeError`, `ValueError`, `built-in`, `compiler`, `interpreter`, `bytecode`, `input`, `print`, `int`, `str`...).
2. **Cập nhật Từ Điển Kỹ Thuật Dùng Chung (Central Phonetic Dictionary)**:
   - File cấu hình: `Kokoro-Vietnamese/configs/tech_dictionary.json`
   - Lưu trữ cặp mapping `Từ_Gốc: Phiên_Âm_Chuẩn` (Ví dụ: `"Python": "Pai-thòn"`, `"TypeError": "tai-é-rơ"`).
3. **Áp dụng Tự Động Cho Tất Cả Bài Học Sau**:
   - Trình chuẩn hóa `text_norm.py` của Kokoro-Vietnamese sẽ tự động đọc `tech_dictionary.json` và chuyển đổi toàn bộ thuật ngữ tiếng Anh / từ viết tắt sang âm đọc chuẩn xác trước khi mô hình tổng hợp tiếng nói.

---

## 9. Reviewer Checklist (14 Tiêu Chí Kiểm Định Bắt Buộc)

Reviewer agent sẽ **REJECT (TỪ CHỐI)** nếu vi phạm bất kỳ tiêu chí nào:

1. ✅ JSON có đủ fields: `lesson_slug`, `lesson_title`, `total_duration`, `scenes`, `tts_scripts`
2. ✅ Đủ 4–6 scenes per lesson
3. ✅ Mỗi scene có đủ: `scene_id`, `scene_title`, `start_at_root`, `duration`, `track_index`, `narration`, `animation_timeline`
4. ✅ Timeline liên tục: `start_at_root[N] = sum(duration[0..N-1])`
5. ✅ **Narration 800–1500 từ tổng bài học** (Thời lượng 5–10 phút).
6. ✅ **BẮT BUỘC Lời Mở Đầu, Giới Thiệu Bài Tiếp & Lời Tạm Biệt**:
   - Scene 01 cất lời: `"Chào mừng các bạn đã quay trở lại với hệ thống Elearning của Rikkei Education."`
   - Scene cuối cất lời giới thiệu bài tiếp theo: `"Trong bài học tiếp theo, chúng ta sẽ cùng nhau tìm hiểu về [Tên_Bài_Học_Tiếp_Theo]. Cảm ơn các bạn đã theo dõi, hẹn gặp lại!"` (Đồng thời UI Banner xuất hiện đồng bộ).
7. ✅ `tts_scripts` có đủ entry cho mọi `scene_id`
8. ✅ `track_index` tăng dần: 1, 2, 3, ...
9. ✅ **Tuân thủ Giọng Văn Giảng Viên Đại Học (Section 4.3 — Zero Tolerance)**: Reviewer sẽ REJECT ngay nếu narration vi phạm BẤT KỲ quy tắc nào trong Section 4.3, bao gồm nhưng không giới hạn:
   - Xưng hô sai: `các em`, `các em ơi`, `các em thân mến`, `bạn ơi`, `mọi người ơi`
   - Từ sến súa: `nhé`, `nha`, `nhen`, `cố lên nhé`, `học tốt nhé`, `thành công nhé`
   - Từ chết chóc / kích động: `chết`, `chết người`, `tiêu tùng`, `thảm họa`, `thảm khốc`, `kinh khủng`, `nguy hiểm chết người`
   - Từ phóng đại: `siêu`, `đỉnh của đỉnh`, `huyền thoại`, `thần thánh`, `bá đạo`, `ảo diệu`, `bùng nổ`
   - Lời kêu gọi mạng xã hội: `like`, `subscribe`, `đăng ký kênh`, `nhấn chuông`, `comment bên dưới`
10. ✅ **Nguồn kiến thức từ Bài Đọc (Reading-First SSOT Dependency)**: Kịch bản video CHỈ được phép biên soạn **SAU KHI Bài Đọc HTML (`reading.md`) đã được tạo và phê duyệt 100%**. Trích xuất 100% nội dung kiến thức từ file Bài Đọc để đảm bảo tính đồng bộ và chính xác tuyệt đối.
11. ✅ **Phân Tích & Tự Huấn Luyện Từ Điển TTS**: Bắt buộc quét từ khó/tiếng Anh và lưu phiên âm vào `configs/tech_dictionary.json` trước khi sinh voice.
12. ✅ **Chuẩn hóa SVG Icons & Tên Kỹ Thuật trên UI**: Không dùng Emoji trên UI; Không đưa từ phiên âm (`Pai-thòn`) lên UI Display text (chỉ dùng `Python`).
13. ✅ **UI Ngắn gọn & Clean Fade-out**: UI Cards chỉ dùng từ khóa/bullet points (không chứa văn bản dài); Bắt buộc có Fade-out ở cuối mỗi Scene.
14. ✅ **Bắt Buộc Đường Dẫn Tương Đối Tới Gốc Dự Án**: Không được hardcode đường dẫn ổ đĩa máy tính (`d:\...`, `C:\...`, `file:///d:...`). Tất cả đường dẫn tệp phải bắt đầu từ thư mục gốc dự án (`Kokoro-Vietnamese/configs/...`, `skills/...`).
