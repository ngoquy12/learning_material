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

---

## 4. Quy tắc Narration (Lời Thoại & Thời Lượng Thong Thả)

| Tiêu chí | Yêu cầu chuẩn |
|----------|---------------|
| **Tổng Thời Lượng Video** | **5 – 10 Phút (300s – 600s)** / bài học (Chưa bao gồm Intro & Outro). Tuyệt đối không làm video vội vàng dưới 4 phút. |
| **Thời Lượng / Scene** | **30s – 60s** / scene. Đảm bảo đủ thời gian giảng giải chi tiết, không dồn dập. |
| **Tổng Số Từ** | **800 – 1500 từ** / bài học (Đảm bảo độ sâu kiến thức sư phạm). |
| **Số Từ / Scene** | **120 – 250 từ** / scene. |
| **Tốc Độ Đọc & Ngắt Nghỉ** | Tốc độ đọc thong thả, từ tốn (`speed = 0.9` – `1.0`). Bắt buộc chèn đầy đủ dấu phẩy `,`, dấu chấm `.`, dấu hai chấm `:` để giọng đọc ngắt nghỉ tự nhiên, sư phạm. |
| **Lời Mở Đầu (BẮT BUỘC SCENE 01)** | **BẮT BUỘC** câu đầu tiên của `Scene_01` (trong lời thoại & file TTS script) phải cất lên: `"Chào mừng các bạn đã quay trở lại với hệ thống Elearning của Rikkei Education."` |
| **Lời Tạm Biệt & Giới Thiệu Bài Tiếp (BẮT BUỘC SCENE CUỐI)** | **BẮT BUỘC** ở đoạn kết thúc Scene cuối cùng, voiceover phải đọc rõ tóm tắt + **tên & nội dung của Bài Học Tiếp Theo**, và cất lời tạm biệt: `"Tóm lại... Trong bài học tiếp theo, chúng ta sẽ cùng nhau tìm hiểu về [Tên_Bài_Học_Tiếp_Theo]. Cảm ơn các bạn đã theo dõi, hẹn gặp lại!"`. Đồng thời UI Banner bài học tiếp theo (`.next-step-bar`) **phải xuất hiện đồng bộ** trên màn hình lúc voice cất lời dẫn này. |
| **Hành văn & Từ Nối Chuyển Cảnh (BẮT BUỘC TỰ NHIÊN)** | **BẮT BUỘC** sử dụng các từ nối, câu dẫn dắt sư phạm tự nhiên giữa các ý và giữa các Scene (*"Bây giờ chúng ta hãy cùng đặt câu hỏi...", "Thế nhưng trong thực tế...", "Liệu có giải pháp nào...", "Đến đây, chúng ta sẽ chuyển sang..."*). **KHÔNG ĐƯỢC** đọc liệt kê khô khan như đọc slide. |
| **Cấu Trúc Kịch Bản (BẮT BUỘC ĐẶT VẤN ĐỀ TRƯỚC)** | **BẮT BUỘC** tuân theo cấu trúc **Bối cảnh -> Vấn đề/Pain point -> Giải pháp -> Thực thi mã nguồn**. Tuyệt đối không nhảy ngay vào định nghĩa/giải pháp khi người học chưa hiểu rõ lý do và ứng dụng thực tế. |
| **Từ Ngữ Cấm Dùng** | **NGHIÊM CẤM** sử dụng từ ngữ sến súa, khẩu ngữ/từ đệm thừa (`nhé`, `dạ`, `các em thân mến`, `nhé các bạn`, `à`, `ừm`...) và từ ngữ tiêu cực/kích động/gây hoảng sợ (`chết chóc`, `thảm họa`, `tiêu tùng`...). |

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

## 7. Design System & Icon Rules (BẮT BUỘC tuân theo)

```
Background: #0f1117 + dot grid + radial cyan/purple glow
Font text: Inter | Font code: Fira Code
Text colors (BẮT BUỘC SIÊU TƯƠNG PHẢN): #ffffff (Tiêu đề - 100% White), #f0f6fc (Nội dung - Bright White), font-weight: 500-700
CẤM MÀU XÁM TỐI: Không bao giờ dùng màu #8b949e, #666, #444 cho văn bản nội dung.
Syntax: keyword #ff7b72 | string #a5d6ff | variable #79c0ff | function #d2a8ff
IDE Window: VS Code Dark+ background #1e1e1e, border rgba(255,255,255,0.15)
Cards: rgba(22, 27, 34, 0.92) + border rgba(255,255,255,0.15) + border-radius 20px
Canvas: 1920×1080px, overflow hidden
```

**QUY TẮC ICON & TỪ NGỮ GIAO DIỆN (UI):**
1. **NGHIÊM CẤM DÙNG EMOJI TRÊN UI**: Sử dụng 100% SVG Vector Icons (`<svg>...</svg>`) cho mọi nhãn, nút, badge, sidebar.
2. **PHÂN TÁCH 100% GIỮA TTS SCRIPT VÀ UI DISPLAY**:
   - `TTS Script` (để đọc voice): Dùng phiên âm (`Pai-thòn`, `snếch-kê-xơ`, `P-Vi-Em`) để mô hình đọc tiếng Anh chuẩn.
   - `UI Display Text` (hiển thị hình ảnh): **BẮT BUỘC** dùng từ chuẩn tiếng Anh / tiếng Việt kỹ thuật: `Python`, `snake_case`, `PVM`, `compiler`, `PEP 8`.
3. **KHÔNG DÁN ĐOẠN VĂN DÀI LÊN UI**: UI Cards chỉ chứa Keywords, Bullet Points (tối đa 5–10 từ/card), Code Snippets hoặc Diagrams. Không bao giờ chép lại nguyên đoạn văn lời thoại lên UI.
4. **FADE-OUT CLEAN CUỐI SCENE**: Ở 0.8s cuối của mỗi Scene timeline, **BẮT BUỘC** fade out toàn bộ scene (`tl.to("#scene-XX", {autoAlpha:0, duration:0.8})`) để tránh đè layout sang Scene tiếp theo hoặc Outro video.
5. **CẤM SỬA LẺ TỪNG VIDEO**: Tất cả video bài học phải được sinh và đóng gói tự động thông qua quy chuẩn SKILL và bộ Component Reusable (`hyperframes/components/`).
6. **NGHIÊM CẤM ĐƯỜNG DẪN Ổ ĐĨA TỦ MÁY TÍNH (WORKSPACE-RELATIVE PATHS ONLY)**: **BẮT BUỘC** tất cả các đường dẫn tệp trong cấu hình, tài liệu, kịch bản, mã nguồn script và tham chiếu (link) PHẢI xuất phát từ thư mục gốc của dự án (ví dụ: `Kokoro-Vietnamese/configs/tech_dictionary.json`, `skills/video_script_generator/SKILL.md`, `hyperframes/components/`). **NGHIÊM CẤM** việc ghi đường dẫn tuyệt đối bắt đầu từ ổ đĩa máy tính (`d:\...`, `C:\...`, `file:///d:...`).

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
9. ✅ **Không từ sến súa/kích động**: Không chứa `nhé`, `dạ`, `các em thân mến`, `chết chóc`, `thảm họa`...
10. ✅ **Nguồn kiến thức từ Bài Đọc**: Trích xuất 100% từ file Bài Đọc (`reading.md`) làm nguồn tri thức SSOT.
11. ✅ **Phân Tích & Tự Huấn Luyện Từ Điển TTS**: Bắt buộc quét từ khó/tiếng Anh và lưu phiên âm vào `configs/tech_dictionary.json` trước khi sinh voice.
12. ✅ **Chuẩn hóa SVG Icons & Tên Kỹ Thuật trên UI**: Không dùng Emoji trên UI; Không đưa từ phiên âm (`Pai-thòn`) lên UI Display text (chỉ dùng `Python`).
13. ✅ **UI Ngắn gọn & Clean Fade-out**: UI Cards chỉ dùng từ khóa/bullet points (không chứa văn bản dài); Bắt buộc có Fade-out ở cuối mỗi Scene.
14. ✅ **Bắt Buộc Đường Dẫn Tương Đối Tới Gốc Dự Án**: Không được hardcode đường dẫn ổ đĩa máy tính (`d:\...`, `C:\...`, `file:///d:...`). Tất cả đường dẫn tệp phải bắt đầu từ thư mục gốc dự án (`Kokoro-Vietnamese/configs/...`, `skills/...`).
