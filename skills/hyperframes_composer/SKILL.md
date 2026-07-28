---
name: hyperframes_composer
description: Bộ quy chuẩn kỹ thuật sản xuất video HyperFrames cho hệ thống Elearning - bao gồm kiến trúc file, animation rules, design system và production pipeline chuẩn từ dự án dev-tutorial-video.
---

# HyperFrames Composer Skill — Quy Chuẩn Sản Xuất Video E-learning

> [!IMPORTANT]
> **QUY TẮC TUÂN THỦ 100% QUY TRÌNH HYPERFRAMES (STRICT HYPERFRAMES ADHERENCE - CẤM TỰ SÁNG TẠO):**
> Tất cả các Agent (Video Director Agent, HyperFrames Writer Agent, Video Reviewer Agent) **BẮT BUỘC** tuân thủ $100\%$ quy trình, cấu trúc tệp, kịch bản, âm thanh và quy chuẩn giao diện từ thư mục gốc `hyperframes/` và tệp hướng dẫn `hyperframes/dev-tutorial-video/HYPERFRAMES_GUIDELINE.md`.
> **NGHIÊM CẤM** bất kỳ sự tự sáng tạo tùy tiện, sửa đổi tự phát hoặc đi sai lệch khỏi hệ thống quy chuẩn đã được phê duyệt trong `hyperframes/`.

> [!IMPORTANT]
> **QUY TẮC ĐƯỜNG DẪN TỆP (WORKSPACE-RELATIVE PATHS ONLY):**
> **NGHIÊM CẤM** việc hardcode tuyệt đối các đường dẫn từ ổ đĩa máy tính (ví dụ: `d:\...`, `C:\...`, `file:///d:/...`).
> **BẮT BUỘC** tất cả các đường dẫn tệp trong cấu hình, tài liệu, kịch bản, mã nguồn script và tham chiếu (link) PHẢI xuất phát từ thư mục gốc của dự án (ví dụ: `Kokoro-Vietnamese/configs/tech_dictionary.json`, `skills/hyperframes_composer/SKILL.md`, `hyperframes/components/`).

> [!IMPORTANT]
> **QUY TẮC NỐI MÃ NGUỒN HTML TRỰC TIẾP (INLINED SCENE DOM — CHỐNG MÀN HÌNH ĐEN):**
> Khi render trên Windows với giao thức `file://`, Chrome Puppeteer sẽ chặn truy cập `iframe.contentWindow.__timelines` do chính sách bảo mật cross-origin `origin null`. Điều này khiến các animation GSAP trong `iframe` bị kẹt ở frame 0 (màn hình đen).
> **BẮT BUỘC**: Nhúng trực tiếp container HTML của tất cả các Scene (`<div id="scene-01" class="clip scene-root">...</div>`) và mã GSAP timeline tương ứng vào tệp `index.html` duy nhất. Không sử dụng nested `<iframe>` trong `index.html`.

> [!IMPORTANT]
> **QUY TẮC BẮT BUỘC VỀ HÌNH ẢNH & ĐỒ HỌA MINH HỌA (DYNAMIC VISUAL ASSET & IMAGE PIPELINE):**
> **NGHIÊM CẤM** việc dựng 100% giao diện video chỉ bằng các khung chữ HTML trần trụi, gây nhàm chán cho người xem!
> **BẮT BUỘC**:
> 1. **Tạo Hình Ảnh Minh Họa Đồ Họa Công Nghệ (Generated Image Assets)**:
>    - Khi sinh kịch bản cho bài học mới, Agent **BẮT BUỘC** gọi công cụ `generate_image` để tự động tạo các tệp hình ảnh minh họa 3D/Infographic công nghệ chất lượng cao (`.png` / `.jpg`) cho mỗi Scene (VD: `assets/images/scene_01_concept.png`).
>    - Các tệp ảnh sinh ra được lưu tại `Video/{lesson_slug}/assets/images/` và nhúng trực tiếp vào thẻ HTML `<img src="assets/images/scene_XX_concept.png" class="scene-illustration" />`.
> 2. **Bố Cục Giao Diện Giàu Đồ Họa (Rich Graphical Layouts)**:
>    - Áp dụng các bố cục sinh động: **Split-Screen (Khung Ảnh Minh Họa 3D bên trái + Nội dung Thẻ bên phải)**, **Infographic Interactive Step-Cards**, **Glassmorphic Hero Showcase với Sơ Đồ Vector SVG Glowing**.
> 3. **Cập Nhật Tự Động Toàn Hệ Thống**: Tất cả các video sinh ra từ Agent sau này sẽ tự động tích hợp quy chuẩn sinh ảnh này mà không cần đi chỉnh sửa thủ công từng video lẻ.

---

## 1. Kiến trúc Project (File Structure) — BẮT BUỘC

Toàn bộ code dự án video phải được lưu tại thư mục `Video/{lesson_slug}` của từng Lesson (VD: `output/PM_Python/Session 01.../Lesson 01.../Video/session_01_lesson_01`), copy cấu trúc dự án mẫu chuẩn từ `hyperframes/dev-tutorial-video`:

```
{lesson_path}/Video/{lesson_slug}/
├── index.html                    ← Root composition (master timeline chứa Intro/Outro/BGM/TTS/Scenes)
├── meta.json                     ← { "id": "{slug}", "name": "{slug}" }
├── package.json                  ← HyperFrames CLI scripts
├── prepare_assets.js / gen_tts.py← Script sinh voice TTS bằng Kokoro-Vietnamese (hung_thinh)
├── assets/                       ← Tài nguyên media (Copy từ hyperframes/assets/)
│   ├── intro.mp4                 ← Video Intro Rikkei Education (9.24s)
│   ├── outro.mp4                 ← Video Outro Rikkei Education (12.15s)
│   ├── bg-music.mp3              ← Nhạc nền Background Music
│   └── tts/
│       ├── Scene_01.mp3          ← TTS audio (từng scene)
│       ├── Scene_02.mp3
│       └── durations.json        ← { "Scene_01": 27.63, "Scene_02": 22.80, ... }
└── src/compositions/
    ├── Intro.html                ← Intro video sub-composition độc lập (9.24s)
    ├── Scene_01.html             ← Scene 1 sub-composition
    ├── Scene_02.html             ← Scene 2 sub-composition
    ├── Scene_0N.html             ← ...
    └── Outro.html                ← Outro video sub-composition độc lập (12.15s)
```

**package.json chuẩn:**
```json
{
  "name": "{lesson_slug}",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "npx --yes hyperframes@0.6.63 preview",
    "check": "npx --yes hyperframes@0.6.63 lint && npx --yes hyperframes@0.6.63 validate && npx --yes hyperframes@0.6.63 inspect",
    "render": "npx --yes hyperframes@0.6.63 render",
    "publish": "npx --yes hyperframes@0.6.63 publish"
  }
}
```

---

## 2. Cấu trúc `index.html` (Root Composition Chứa Intro/Outro/BGM/TTS) — BẮT BUỘC

```html
<!doctype html>
<html lang="vi">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1920px; height: 1080px; overflow: hidden; background: #0f172a; }
      .clip { position: absolute; visibility: hidden; }
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="{lesson_slug}"
      data-start="0"
      data-duration="{TOTAL_DURATION}"
      data-width="1920"
      data-height="1080"
    >
      <!-- Intro Composition Clip (Tách riêng tránh đè UI HTML) -->
      <div class="clip" data-composition-src="src/compositions/Intro.html"
           data-composition-id="scene-intro" data-start="0" data-duration="9.24" data-track-index="0"></div>

      <!-- Scene clips: data-start bắt đầu SAU KHI Intro kết thúc (mốc 9.24s) -->
      <div class="clip" data-composition-src="src/compositions/Scene_01.html"
           data-composition-id="scene-01" data-start="9.24" data-duration="{S1_DUR}" data-track-index="1"></div>
      <div class="clip" data-composition-src="src/compositions/Scene_02.html"
           data-composition-id="scene-02" data-start="{9.24 + S1_DUR}" data-duration="{S2_DUR}" data-track-index="2"></div>
      <!-- ... tiếp tục cho mỗi scene nội dung -->

      <!-- Outro Composition Clip (Tách riêng ở cuối timeline) -->
      <div class="clip" data-composition-src="src/compositions/Outro.html"
           data-composition-id="scene-outro" data-start="{OUTRO_START}" data-duration="12.15" data-track-index="0"></div>

      <!-- Background Music Kênh 99 -->
      <audio id="bg-music"
             data-start="0"
             data-duration="{TOTAL_DURATION}"
             data-track-index="99"
             data-volume="0.12"
             data-loop="true"
             src="assets/bg-music.mp3"></audio>

      <!-- TTS Audio: Đặt ở root timeline đồng bộ với timestamps của từng scene -->
      <audio id="tts-01" data-start="9.24"         data-duration="{S1_DUR}" data-track-index="20" data-volume="1" src="assets/tts/Scene_01.mp3"></audio>
      <audio id="tts-02" data-start="{9.24+S1_DUR}" data-duration="{S2_DUR}" data-track-index="21" data-volume="1" src="assets/tts/Scene_02.mp3"></audio>
      <!-- ... -->
    </div>
      <!-- ... -->
    </div>

    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      window.__timelines["{lesson_slug}"] = tl;
    </script>
  </body>
</html>
```

**QUYẾT ĐỐI KHÔNG:**
- Đặt `<audio>` trong sub-composition Scene_XX.html
- Quên `id` trên `<audio>` element
- Dùng `Math.random()`, `Date.now()`, fetch API trong compositions

---

## 3. Cấu trúc Scene Sub-Composition — Template BẮT BUỘC (Light Theme Standard)

```html
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1920, height=1080, initial-scale=1.0">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,400;1,700&family=Fira+Code:wght@400;500;600;700&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
  <script src="https://unpkg.com/@phosphor-icons/web"></script>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1920px; height: 1080px; overflow: hidden;
      background: #f8fafc; color: #0f172a; font-family: 'Be Vietnam Pro', system-ui, -apple-system, sans-serif;
    }
    .scene-root {
      width: 1920px; height: 1080px; position: relative; overflow: hidden;
      background: linear-gradient(135deg, #f8fafc 0%, #edf2f7 100%);
      font-family: 'Be Vietnam Pro', sans-serif;
    }
    .scene-root::before {
      content: ''; position: absolute; inset: 0;
      background-image: radial-gradient(rgba(15, 23, 42, 0.08) 1.5px, transparent 1.5px);
      background-size: 36px 36px; opacity: 0.6; pointer-events: none;
    }

    /* Fixed Top-Right Rikkei Logo Standard (Same row as title) */
    .rikkei-logo {
      position: absolute; top: 50px; right: 80px; height: 52px; z-index: 100;
      object-fit: contain; filter: drop-shadow(0 2px 8px rgba(0,0,0,0.06));
    }

    /* Top Left Title Header */
    .scene-title-header {
      position: absolute; top: 50px; left: 80px; right: 260px; z-index: 10;
      text-align: left !important;
    }
    .main-title {
      font-family: 'Be Vietnam Pro', sans-serif; font-size: 44px; font-weight: 800; color: #ba252a; line-height: 1.25;
      letter-spacing: -0.02em; text-align: left !important; margin: 0; padding: 0;
    }

    /* Main Stage Layout */
    .main-stage {
      position: absolute; top: 140px; bottom: 40px; left: 80px; right: 80px; z-index: 5;
      display: flex; flex-direction: column; justify-content: flex-start; align-items: flex-start;
      text-align: left !important; font-family: 'Be Vietnam Pro', sans-serif;
    }
    .content-box {
      width: 100%; max-width: 1760px; font-size: 26px; line-height: 1.65; color: #0f172a;
      text-align: left !important;
    }

    /* Code Container - Monospace Fira Code with Preserved Indentation */
    .content-box pre, .content-box code {
      background: #ffffff; border: 1.5px solid #cbd5e1; border-top: 5px solid #ba252a;
      border-radius: 14px; padding: 24px 28px;
      font-family: 'Fira Code', 'JetBrains Mono', monospace; font-size: 24px; line-height: 1.65 !important; color: #0f172a;
      overflow-x: auto; white-space: pre !important; word-break: normal !important;
      box-shadow: 0 10px 25px rgba(15, 23, 42, 0.05); text-align: left !important;
      margin: 0 !important; display: block !important; width: 100%; tab-size: 4; -moz-tab-size: 4;
    }
  </style>
</head>
<body>
  <div id="scene-{scene_n}" class="scene-root clip" data-composition-id="scene-{scene_n}" data-start="0" data-duration="{dur}" data-track-index="0">
    
    <!-- Fixed Top-Right Logo (Same row as title) -->
    <img src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png" alt="Rikkei Academy" class="rikkei-logo clip" data-start="0" data-duration="{dur}" data-track-index="5">

    <!-- Top Left Title Header -->
    <div class="scene-title-header clip" data-start="0" data-duration="{dur}" data-track-index="10">
      <h1 class="main-title">{scene_title}</h1>
    </div>

    <!-- Main Stage Content Slot (Dynamic Grid/Cards/Code) -->
    <div class="main-stage clip" data-start="0.5" data-duration="{dur}" data-track-index="20">
      <div class="content-box">
        {clean_content}
      </div>
    </div>

  </div>

  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    window.__timelines["{scene_slug}"] = tl;

    const _buildTimer = setInterval(function() {
      const root = document.getElementById("scene-{scene_n}");
      if (!root) return;
      clearInterval(_buildTimer);

      // ── BƯỚC 1: Set tất cả .clip visible (BẮT BUỘC ĐẦU TIÊN) ──────────
      tl.set(".clip", { autoAlpha: 1 }, 0);

      // ── BƯỚC 2: Ẩn từng element theo trạng thái ban đầu ────────────────
      tl.set("#intro-title", { autoAlpha: 0, scale: 0.8 }, 0);
      // ... ẩn các elements khác

      // ── PHASE 1: Intro title (0.2s → 3.2s) ────────────────────────────
      tl.to("#intro-title", { autoAlpha: 1, scale: 1, duration: 0.6, ease: "back.out(1.4)" }, 0.2);
      tl.to("#intro-title", { scale: 0.38, x: -760, y: -460, duration: 0.7, ease: "power3.inOut" }, 3.2);

      // ── PHASE 2+: Nội dung chính từ 4.0s ──────────────────────────────
      // (KHÔNG BAO GIỜ hiện element chính trước khi intro title kết thúc)

      // ── KHÓA CUỐI TIMELINE ────────────────────────────────────────────
      tl.set({}, {}, {SCENE_DURATION});
    }, 50);
  </script>
</body>
</html>
```

---

## 4. Quy tắc Timeline GSAP — BẮT BUỘC TUÂN THỦ (NHỊP ĐIỆU THONG THẢ)

### Thời lượng & Nhịp điệu chuẩn:
- **Thời lượng mỗi Scene**: **30s – 60s** / scene (Tổng video bài học từ **5 – 10 phút**).
- **Khoảng nghỉ giữa các Animation**: **2.5s – 4.0s** giữa các bước xuất hiện của phần tử UI, giúp học viên kịp đọc và tiếp thu kiến thức.

### Thứ tự tuyệt đối trong mỗi scene:
```
0.0s → tl.set(".clip", { autoAlpha: 1 }, 0)        ← BẮT BUỘC ĐẦU TIÊN
0.0s → tl.set(elements, { ẩn }, 0)                 ← BẮT BUỘC THỨ HAI
0.2s → intro-title fade in
3.0s → intro-title lên góc / fade out
4.0s+ → Element UI 1 bắt đầu xuất hiện
7.5s+ → Element UI 2 bắt đầu xuất hiện (Khoảng nghỉ ≥ 3.0s)
12.0s+→ Element UI 3 bắt đầu xuất hiện (Khoảng nghỉ ≥ 3.5s)
...
{DURATION - 0.8}s → tl.to("#scene-XX", { autoAlpha: 0, duration: 0.8 }) ← BẮT BUỘC DỌN DẸP SẠCH UI
{DURATION}s → tl.set({}, {}, {DURATION})           ← BẮT BUỘC CUỐI TIMELINE
```

### Pattern A — Intro Hero Welcome Banner (Dùng cho Scene 01 khi cất lời chào):
- Từ **0.0s ➔ 3.2s**: Hiển thị Badge Thương hiệu Rikkei Education phát sáng + Hero Title 72px + Subtitle ở chính giữa màn hình.
- Tại **3.2s**: Hero Title thu nhỏ và di chuyển về góc trên-trái thành Header Bar cố định.
```js
tl.to("#intro-hero-banner", { autoAlpha: 1, scale: 1, duration: 0.6, ease: "back.out(1.4)" }, 0.2);
tl.to("#intro-hero-banner", { scale: 0.38, x: -760, y: -460, duration: 0.7, ease: "power3.inOut" }, 3.2);
// UI bài học chính xuất hiện từ 4.0s
tl.to("#main-lesson-ui", { autoAlpha: 1, y: 0, duration: 0.6, ease: "power3.out" }, 4.0);
```

### Pattern B — Outro Next-Lesson Preview Banner (Dùng cho Scene cuối khi cất lời tạm biệt):
- **0.0s ➔ 4.0s**: Hiển thị Thẻ Tổng Kết Key Takeaways.
- **4.0s+**: Banner Bài Học Tiếp Theo viền tím phát sáng xuất hiện cùng nút bấm `[ TIẾP TỤC ➔ ]` nhấp nháy thu hút người xem.
```js
tl.to("#recap-card", { autoAlpha: 1, y: 0, duration: 0.6, ease: "power3.out" }, 1.5);
tl.to("#next-lesson-banner", { autoAlpha: 1, y: 0, duration: 0.6, ease: "back.out(1.2)" }, 4.0);
tl.to("#next-lesson-banner", { scale: 1.02, boxShadow: "0 0 40px rgba(168,85,247,0.4)", duration: 0.5, yoyo: true, repeat: 1 }, 7.0);
```

---

## 5. Animation Patterns Tái Sử Dụng

```js
// Slide in từ trái (code lines, list items)
tl.set("#el", { autoAlpha: 0, x: -50 }, 0);
tl.to("#el", { autoAlpha: 1, x: 0, duration: 0.45, ease: "power3.out" }, TIME);

// Fade + scale in (cards, titles)
tl.set("#el", { autoAlpha: 0, scale: 0.9 }, 0);
tl.to("#el", { autoAlpha: 1, scale: 1, duration: 0.7, ease: "back.out(1.4)" }, TIME);

// Slide up (bottom elements)
tl.set("#el", { autoAlpha: 0, y: 40 }, 0);
tl.to("#el", { autoAlpha: 1, y: 0, duration: 0.6, ease: "power3.out" }, TIME);

// Bounce drop (items rơi vào ô)
tl.set("#el", { autoAlpha: 0, y: -60 }, 0);
tl.to("#el", { autoAlpha: 1, y: 0, duration: 0.4, ease: "bounce.out" }, TIME);

// Stagger group
tl.to(["#el-0","#el-1","#el-2"], {
  autoAlpha: 1, x: 0, duration: 0.4, ease: "power3.out", stagger: 0.15
}, TIME);

// Fade in code (KHÔNG dùng typewriter — bị giật khi render)
// Set innerHTML trước, rồi fade in element
tl.set("#code-el", { autoAlpha: 0 }, 0);
tl.to("#code-el", { autoAlpha: 1, duration: 0.5, ease: "power2.out" }, TIME);
```

---

## 6. Design System — Màu sắc và Typography Chuẩn

```css
/* Background */
background-color: #0f1117;
background-image: radial-gradient(rgba(255,255,255,0.25) 1.5px, transparent 1.5px);
background-size: 32px 32px;

/* Glow effects */
body::before { background: rgba(56,189,248,0.15); }  /* Cyan glow */
body::after  { background: rgba(168,85,247,0.15); }  /* Purple glow */

/* Syntax highlighting */
--keyword:  #ff7b72;   /* if, for, def, class */
--string:   #a5d6ff;   /* "text" */
--variable: #79c0ff;   /* tên biến */
--operator: #d2a8ff;   /* =, +, - */
--bracket:  #d2a8ff;   /* [], {}, () */
--comment:  #8b949e;   /* # comment */
--function: #d2a8ff;   /* print(), len() */

/* Semantic */
--good:    #3fb950;    /* panel phải, kết quả tốt */
--bad:     #f85149;    /* panel trái, lỗi */
--accent:  #ffa657;    /* highlight */

/* Text */
--text-primary:   #e6edf3;
--text-secondary: #c9d1d9;
--text-muted:     #8b949e;

/* Card standard */
background: rgba(9,9,11,0.7);
border: 1px solid rgba(255,255,255,0.08);
border-radius: 20px;
backdrop-filter: blur(16px);

/* Font */
font-family: 'Inter', sans-serif;        /* Text thường */
font-family: 'Fira Code', monospace;     /* Code blocks */
```

---

## 7. Quy tắc data-track-index

Trong sub-composition (Scene_XX.html) — local index:
```
0   → wrapper scene chính (#scene-{N})
1   → element quan trọng nhất / hiện sớm nhất
2   → element thứ hai
...
MAX → intro-title (luôn cao nhất để z-index đúng)
```

Trong `index.html` (root) — global index:
```
1-N   → scene clips (theo thứ tự scene)
20-2N → audio tracks (cao để tránh collision với scene tracks)
```

---

## 8. Cấu trúc JSON Output của Video Director Agent

Agent **PHẢI** trả về JSON theo cấu trúc sau — đây là "kịch bản sản xuất" (production blueprint):

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
      "narration": "Ok, Xin chào tất cả các bạn! Trong bài học ngày hôm nay...",
      "visual_description": "Màn hình chia đôi. Bên trái: code cũ gạch bỏ. Bên phải: List code mới.",
      "html_structure": "Mô tả HTML elements cần tạo: split-container, panel-left, panel-right, code-block",
      "animation_timeline": [
        "0.0s: tl.set('.clip', {autoAlpha:1}, 0)",
        "0.2s: intro-title fade in",
        "3.2s: intro-title fade out",
        "4.2s: scene-main-title fade in",
        "7.5s: scene-main-title lên góc",
        "8.4s: split-container hiện",
        "9.0-10.2s: v1..v5 slide in từ trái",
        "12.0s: strikethrough v1..v5",
        "25.5s: new-code-block hiện"
      ]
    }
  ],
  "tts_scripts": {
    "Scene_01": "Ok, Xin chào tất cả các bạn! ...",
    "Scene_02": "Vậy tóm lại, List là gì? ..."
  }
}
```

---

## 9. Checklist Kiểm Tra Trước Khi Xuất File

Reviewer PHẢI kiểm tra tất cả các điểm sau:

**Audio Architecture:**
- [ ] Tất cả `<audio>` nằm trong `index.html`, không trong sub-composition
- [ ] Mọi `<audio>` có `id` duy nhất (tts-01, tts-02, ...)
- [ ] `data-start` trong `index.html` là timestamp tuyệt đối root timeline
- [ ] Audio track-index ≥ 20

**GSAP Timeline:**
- [ ] `tl.set(".clip", { autoAlpha: 1 }, 0)` là lệnh ĐẦU TIÊN
- [ ] Mọi `tl.set()` có position argument `, 0`
- [ ] Intro title xuất hiện lúc 0.2s, kết thúc lúc 3.2s
- [ ] Nội dung chính KHÔNG xuất hiện trước 4.0s
- [ ] Timeline kết thúc bằng `tl.set({}, {}, {DURATION})`
- [ ] `window.__timelines["{id}"] = tl` được đăng ký

**Scene Structure:**
- [ ] Canvas 1920×1080px, overflow hidden
- [ ] Mọi element có timing đều có `class="clip"`, `data-start`, `data-duration`, `data-track-index`
- [ ] Intro-title có track-index cao nhất trong scene
- [ ] KHÔNG có `Math.random()`, `Date.now()`, typewriter effect, fetch API

**Design:**
- [ ] Background: `#0f1117` + dot grid + radial glow
- [ ] Font: Inter cho text, Fira Code cho code
- [ ] Màu sắc theo design system chuẩn

**Narration:**
- [ ] Mở đầu bằng "Chào mừng các em đã quay trở lại với hệ thống Elearning của Rikkei Education..."
- [ ] Kết thúc bằng "Cảm ơn các em đã theo dõi, hẹn gặp lại trong bài học tiếp theo!"
- [ ] Tổng từ narration: 400–800 từ (4–5 phút video)
- [ ] Có câu chuyển cảnh mượt mà giữa các scene

---

## 10. Production Pipeline — Thứ Tự Bắt Buộc

```
Step 1: Video Director Agent sinh production blueprint JSON
         ↓
Step 2: Video Script Reviewer validate JSON theo checklist trên
         ↓ (nếu APPROVED)
Step 3: Ghi file durations.json (lấy duration từ JSON)
Step 4: Ghi index.html (root composition)
Step 5: Ghi từng Scene_XX.html (sub-compositions)
Step 6: Ghi meta.json + package.json
         ↓
Step 7: TTS Generation — sinh audio file từng scene narration
Step 8: npm run check (lint + validate + inspect)
Step 9: npm run render → MP4
```
