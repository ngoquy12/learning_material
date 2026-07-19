---
name: hyperframes_composer
description: Bộ quy chuẩn kỹ thuật sản xuất video HyperFrames cho hệ thống Elearning - bao gồm kiến trúc file, animation rules, design system và production pipeline chuẩn từ dự án dev-tutorial-video.
---

# HyperFrames Composer Skill — Quy Chuẩn Sản Xuất Video E-learning

Tài liệu này là **Nguồn sự thật duy nhất (SSOT)** cho mọi Video Director Agent khi sinh kịch bản và compositions HyperFrames. Mọi output phải tuân thủ tuyệt đối các quy tắc dưới đây.

---

## 1. Kiến trúc Project (File Structure) — BẮT BUỘC

```
{lesson_slug}/
├── index.html                    ← Root composition (master timeline)
├── meta.json                     ← { "id": "{slug}", "name": "{slug}" }
├── package.json                  ← HyperFrames CLI scripts
├── src/compositions/
│   ├── Scene_01.html             ← Scene 1 sub-composition
│   ├── Scene_02.html             ← Scene 2 sub-composition
│   └── Scene_0N.html             ← ...
└── assets/tts/
    ├── scene_01.mp3              ← TTS audio (từng scene)
    ├── scene_02.mp3
    └── durations.json            ← { "scene_01": 38.84, "scene_02": 45.24, ... }
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

## 2. Cấu trúc `index.html` (Root Composition) — BẮT BUỘC

```html
<!doctype html>
<html lang="vi">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1920px; height: 1080px; overflow: hidden; background: #0d1117; }
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
      <!-- Scene clips: data-start là timestamp tuyệt đối trong root timeline -->
      <div class="clip" data-composition-src="src/compositions/Scene_01.html"
           data-composition-id="scene-01" data-start="0" data-duration="{S1_DUR}" data-track-index="1"></div>
      <div class="clip" data-composition-src="src/compositions/Scene_02.html"
           data-composition-id="scene-02" data-start="{S1_DUR}" data-duration="{S2_DUR}" data-track-index="2"></div>
      <!-- ... tiếp tục cho mỗi scene -->

      <!-- TTS Audio: PHẢI đặt ở đây với timestamp TUYỆT ĐỐI, KHÔNG đặt trong sub-composition -->
      <audio id="tts-01" data-start="0"          data-duration="{S1_DUR}" data-track-index="20" data-volume="1" src="assets/tts/scene_01.mp3"></audio>
      <audio id="tts-02" data-start="{S1_DUR}"   data-duration="{S2_DUR}" data-track-index="21" data-volume="1" src="assets/tts/scene_02.mp3"></audio>
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

## 3. Cấu trúc Scene Sub-Composition — Template BẮT BUỘC

```html
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Scene {N} - {Scene Title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600;700&family=Inter:wght@400;600;700&display=swap" rel="stylesheet" />
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1920px; height: 1080px; overflow: hidden;
      background-color: #0f1117;
      background-image: radial-gradient(rgba(255,255,255,0.25) 1.5px, transparent 1.5px);
      background-size: 32px 32px;
      font-family: 'Inter', sans-serif;
    }
    body::before, body::after {
      content: ''; position: absolute; border-radius: 50%; filter: blur(150px); z-index: -1;
    }
    body::before { top: -200px; left: -200px; width: 800px; height: 800px; background: rgba(56,189,248,0.15); }
    body::after  { bottom: -200px; right: -200px; width: 600px; height: 600px; background: rgba(168,85,247,0.15); }

    #scene-{N} { width: 1920px; height: 1080px; position: relative; }

    .intro-title {
      position: absolute; top: 50%; left: 50%;
      transform: translate(-50%, -50%);
      font-family: 'Inter', sans-serif; font-size: 72px; font-weight: 700;
      color: #e6edf3; text-align: center; white-space: nowrap;
      z-index: 100; pointer-events: none;
    }
    /* ... CSS cho các elements khác của scene */
  </style>
</head>
<body>
  <div id="scene-{N}" class="clip" data-start="0" data-duration="{SCENE_DURATION}" data-track-index="0">

    <!-- Intro title — BẮT BUỘC cho mọi scene, track-index = MAX -->
    <div id="intro-title" class="intro-title clip" data-start="0" data-duration="{SCENE_DURATION}" data-track-index="10">
      {Scene Title}
    </div>

    <!-- Các element nội dung — track-index từ 1 trở lên -->
    <!-- ... -->

  </div>

  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    window.__timelines["scene-{N}"] = tl;

    const _build{N} = setInterval(function() {
      const root = document.getElementById("scene-{N}");
      if (!root) return;
      clearInterval(_build{N});

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

## 4. Quy tắc Timeline GSAP — BẮT BUỘC TUÂN THỦ

### Thứ tự tuyệt đối trong mỗi scene:
```
0.0s → tl.set(".clip", { autoAlpha: 1 }, 0)        ← BẮT BUỘC ĐẦU TIÊN
0.0s → tl.set(elements, { ẩn }, 0)                 ← BẮT BUỘC THỨ HAI
0.2s → intro-title fade in
3.2s → intro-title lên góc / fade out
4.0s+ → element chính bắt đầu xuất hiện            ← KHÔNG BAO GIỜ trước 4.0s
...
{DURATION}s → tl.set({}, {}, {DURATION})           ← BẮT BUỘC CUỐI TIMELINE
```

### Pattern A — Intro title lên góc trên-trái (dùng khi title giữ lại làm label):
```js
tl.to("#intro-title", { autoAlpha: 1, scale: 1, duration: 0.6, ease: "back.out(1.4)" }, 0.2);
tl.to("#intro-title", { scale: 0.38, x: -760, y: -460, duration: 0.7, ease: "power3.inOut" }, 3.2);
```

### Pattern B — Intro title fade out (dùng khi có 2 title liên tiếp):
```js
tl.to("#intro-title", { autoAlpha: 1, scale: 1, duration: 0.6, ease: "back.out(1.4)" }, 0.2);
tl.to("#intro-title", { autoAlpha: 0, scale: 0.9, duration: 0.5, ease: "power2.in" }, 3.2);
// Title thứ 2 chỉ hiện SAU KHI title 1 đã mất hẳn (3.2 + 0.5 = 3.7s + buffer 0.5s = 4.2s)
tl.to("#scene-main-title", { autoAlpha: 1, scale: 1, duration: 0.6, ease: "back.out(1.4)" }, 4.2);
tl.to("#scene-main-title", { scale: 0.38, x: 0, y: -460, duration: 0.7, ease: "power3.inOut" }, 7.5);
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
