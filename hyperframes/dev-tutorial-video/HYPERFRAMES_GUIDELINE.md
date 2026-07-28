# HyperFrames Video Production Guideline

Tổng hợp từ thực tế sản xuất — mỗi rule ở đây đến từ một lỗi thực sự đã xảy ra.

---

## 1. Kiến trúc file — quy tắc bất di bất dịch

### Root `index.html` chứa TẤT CẢ audio

**Lỗi đã gặp:** Các `<audio>` element đặt trong sub-composition với `data-start="0"` → tất cả audio phát đồng thời ngay t=0 của root timeline.

**Nguyên nhân:** `data-start` trong sub-composition là tương đối theo local timeline, không phải root. Khi root chạy đến scene đó, local timeline bắt đầu từ 0 và audio cũng bắt đầu từ 0 — nhưng root đã ở giây 142.

**Rule:** Đặt toàn bộ `<audio>` TTS vào `index.html` với timestamp tuyệt đối theo root timeline.

```html
<!-- index.html — audio với absolute timestamps -->
<audio
  id="tts-01"
  data-start="0"
  data-duration="38.84"
  data-track-index="20"
  data-volume="1"
  src="...scene_01.mp3"
></audio>
<audio
  id="tts-02"
  data-start="38.84"
  data-duration="45.24"
  data-track-index="21"
  data-volume="1"
  src="...scene_02.mp3"
></audio>
<audio
  id="tts-03"
  data-start="84.08"
  data-duration="27.17"
  data-track-index="22"
  data-volume="1"
  src="...scene_03.mp3"
></audio>
<!-- ... tiếp tục cho từng scene -->
```

**KHÔNG bao giờ** đặt `<audio>` trong sub-composition HTML.

---

### `<audio>` element bắt buộc có `id`

**Lỗi đã gặp:** `media_missing_id` lint error khi audio không có `id`.

**Rule:** Mọi `<audio>` element phải có `id` duy nhất.

```html
<!-- SAI -->
<audio data-start="0" src="..."></audio>

<!-- ĐÚNG -->
<audio id="tts-01" data-start="0" src="..."></audio>
```

---

## 2. GSAP Timeline — thứ tự set initial states

### `tl.set(".clip", ...)` phải có position argument

**Lỗi đã gặp:** `tl.set(".clip", { autoAlpha: 1 })` không có position → GSAP append vào cuối timeline thay vì tại `0`. Kết quả: các element ẩn/hiện không theo đúng thứ tự.

**Rule:** Luôn thêm `, 0` vào mọi `tl.set()` call trong initial setup.

```js
// SAI — append vào cuối timeline
tl.set(".clip", { autoAlpha: 1 });

// ĐÚNG — đặt tại t=0
tl.set(".clip", { autoAlpha: 1 }, 0);
```

### Thứ tự set initial states trong timeline

GSAP xử lý theo thứ tự thêm vào khi cùng position. Luôn theo thứ tự này:

```js
// 1. Hiện tất cả .clip element (framework cần visibility = visible)
tl.set(".clip", { autoAlpha: 1 }, 0);

// 2. Ẩn từng element cụ thể theo trạng thái ban đầu
tl.set("#intro-title", { autoAlpha: 0, scale: 0.8 }, 0);
tl.set(".split-container", { autoAlpha: 0 }, 0);
tl.set(["#v1", "#v2"], { autoAlpha: 0, x: -50 }, 0);
// ... tiếp tục
```

**Tại sao thứ tự này đúng:** `.clip` set visible trước → các `set` ẩn phía sau override lại → đúng trạng thái ban đầu.

---

## 3. Structure mỗi Scene HTML

### Template chuẩn — copy và điền vào

```html
<!DOCTYPE html>
<html lang="vi">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Scene XX - [Tên scene]</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,400;1,700&family=Fira+Code:wght@400;500;600;700&display=swap"
      rel="stylesheet"
    />
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
    <style>
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }
      body {
        width: 1920px;
        height: 1080px;
        overflow: hidden;
        background: #f8fafc;
        color: #0f172a;
        font-family:
          "Be Vietnam Pro",
          system-ui,
          -apple-system,
          sans-serif;
      }
      .scene-root {
        width: 1920px;
        height: 1080px;
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, #f8fafc 0%, #edf2f7 100%);
        font-family: "Be Vietnam Pro", sans-serif;
      }
      .scene-root::before {
        content: "";
        position: absolute;
        inset: 0;
        background-image: radial-gradient(
          rgba(15, 23, 42, 0.08) 1.5px,
          transparent 1.5px
        );
        background-size: 36px 36px;
        opacity: 0.6;
        pointer-events: none;
      }

      /* Fixed Top-Right Rikkei Logo Standard (Same row as title) */
      .rikkei-logo {
        position: absolute;
        top: 50px;
        right: 80px;
        height: 52px;
        z-index: 100;
        object-fit: contain;
        filter: drop-shadow(0 2px 8px rgba(0, 0, 0, 0.06));
      }

      /* Top Left Title Header */
      .scene-title-header {
        position: absolute;
        top: 50px;
        left: 80px;
        right: 260px;
        z-index: 10;
        text-align: left !important;
      }
      .main-title {
        font-family: "Be Vietnam Pro", sans-serif;
        font-size: 44px;
        font-weight: 800;
        color: #ba252a;
        line-height: 1.25;
        letter-spacing: -0.02em;
        text-align: left !important;
        margin: 0;
        padding: 0;
      }
    </style>
  </head>
  <body>
    <div
      id="scene-XX"
      class="scene-root clip"
      data-composition-id="scene-XX"
      data-start="0"
      data-duration="[DURATION]"
      data-track-index="0"
    >
      <!-- Fixed Top-Right Logo (Same row as title) -->
      <img
        src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png"
        alt="Rikkei Academy"
        class="rikkei-logo clip"
        data-start="0"
        data-duration="[DURATION]"
        data-track-index="5"
      />

      <!-- Top Left Title Header -->
      <div
        class="scene-title-header clip"
        data-start="0"
        data-duration="[DURATION]"
        data-track-index="10"
      >
        <h1 class="main-title">[Tên scene]</h1>
      </div>

      <!-- Các element khác của scene -->
    </div>

    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      window.__timelines["scene-XX"] = tl;

      const _buildXX = setInterval(function () {
        const root = document.getElementById("scene-XX");
        if (!root) return;
        clearInterval(_buildXX);

        // ── BƯỚC 1: Set tất cả .clip visible ─────────────────────────────
        tl.set(".clip", { autoAlpha: 1 }, 0);

        // ── BƯỚC 2: Ẩn tất cả element theo trạng thái ban đầu ────────────
        tl.set("#intro-title", { autoAlpha: 0, scale: 0.8 }, 0);
        // ... ẩn các element khác

        // ── PHASE 1: Intro title (0.2s → 3.2s) ───────────────────────────
        tl.to(
          "#intro-title",
          { autoAlpha: 1, scale: 1, duration: 0.6, ease: "back.out(1.4)" },
          0.2,
        );
        tl.to(
          "#intro-title",
          {
            scale: 0.38,
            x: -760,
            y: -460,
            duration: 0.7,
            ease: "power3.inOut",
          },
          3.2,
        );
        // Hoặc fade out hoàn toàn nếu scene có 2 title liên tiếp:
        // tl.to("#intro-title", { autoAlpha: 0, scale: 0.9, duration: 0.5, ease: "power2.in" }, 3.2);

        // ── PHASE 2+: Các element còn lại bắt đầu từ ~4.0s ───────────────
        // (Không bao giờ hiện element chính trước khi intro title đã lên góc/fade out)

        // ── KHOÁ THỜI GIAN CUỐI ──────────────────────────────────────────
        tl.set({}, {}, [DURATION]);
      }, 50);
    </script>
  </body>
</html>
```

---

## 4. Quy tắc animation intro title

Mỗi scene có một intro title xuất hiện giữa màn hình rồi hoặc:

- **Thu nhỏ lên góc** (dùng khi title cần giữ lại làm label)
- **Fade out** (dùng khi có title thứ 2 xuất hiện ngay sau đó)

### Pattern A — Thu nhỏ lên góc trên-trái

```js
tl.to(
  "#intro-title",
  { autoAlpha: 1, scale: 1, duration: 0.6, ease: "back.out(1.4)" },
  0.2,
);
tl.to(
  "#intro-title",
  { scale: 0.38, x: -760, y: -460, duration: 0.7, ease: "power3.inOut" },
  3.2,
);
// Elements chính bắt đầu từ 4.0s trở đi
```

### Pattern B — Fade out (khi có 2 title liên tiếp)

```js
// Title 1: hiện rồi fade out
tl.to(
  "#intro-title",
  { autoAlpha: 1, scale: 1, duration: 0.6, ease: "back.out(1.4)" },
  0.2,
);
tl.to(
  "#intro-title",
  { autoAlpha: 0, scale: 0.9, duration: 0.5, ease: "power2.in" },
  3.2,
);

// Title 2: chỉ hiện SAU KHI title 1 đã mất hoàn toàn (3.2 + 0.5 = 3.7s, buffer thêm 0.5s)
tl.to(
  "#scene-main-title",
  { autoAlpha: 1, scale: 1, duration: 0.6, ease: "back.out(1.4)" },
  4.2,
);
// Title 2 thu nhỏ lên góc
tl.to(
  "#scene-main-title",
  { scale: 0.38, x: 0, y: -460, duration: 0.7, ease: "power3.inOut" },
  7.5,
);
// Elements chính bắt đầu từ 8.4s trở đi
```

**Lỗi đã gặp:** Title 1 shrink lên góc đồng thời với title 2 xuất hiện → hai title overlap nhau. Fix: dùng fade out cho title 1, chờ nó mất hẳn mới hiện title 2.

---

## 5. Checklist trước khi render

Chạy theo thứ tự này, fix từng bước trước khi qua bước tiếp:

```bash
# Bước 1: Lint
npx hyperframes lint --verbose

# Bước 2: Validate + Inspect (full check)
npm run check

# Bước 3: Render
npm run render
```

### Những lỗi lint hay gặp và cách fix

| Lỗi                       | Nguyên nhân                                  | Fix                                |
| ------------------------- | -------------------------------------------- | ---------------------------------- |
| `media_missing_id`        | `<audio>` không có `id`                      | Thêm `id="tts-XX"`                 |
| `clip_missing_data_start` | Element có `class="clip"` thiếu `data-start` | Thêm đầy đủ 3 data attributes      |
| `track_index_collision`   | Hai element cùng `data-track-index`          | Dùng index unique trong từng scene |
| `determinism_violation`   | Dùng `Math.random()` hoặc `Date.now()`       | Xóa bỏ, dùng giá trị cố định       |

---

## 6. Cấu trúc timeline — thứ tự ưu tiên

```
0.0s  → tl.set(".clip", { autoAlpha: 1 }, 0)         ← BẮT BUỘC đầu tiên
0.0s  → tl.set(elements, { ẩn }, 0)                  ← BẮT BUỘC thứ hai
0.2s  → intro-title fade in
3.2s  → intro-title lên góc / fade out
4.0s+ → element chính bắt đầu xuất hiện (KHÔNG bao giờ trước 4.0s)
...
[DURATION]s → tl.set({}, {}, [DURATION])             ← BẮT BUỘC cuối timeline
```

**Lỗi hay gặp:** Hiện element chính quá sớm (trước khi intro title kết thúc animation) → màn hình lộn xộn, element chồng lên nhau.

---

## 7. `data-track-index` — quy ước đánh số

Trong mỗi sub-composition, `data-track-index` là local (không liên quan đến root). Quy ước:

```
0   → wrapper scene chính (#scene-XX)
1   → element quan trọng nhất / hiện sớm nhất
2   → element thứ hai
...
MAX → intro-title (luôn đặt track cao nhất để z-index render đúng)
```

Trong `index.html` (root):

```
1-6   → scene clips
20-25 → audio tracks (đặt cao để tránh collision với scene tracks)
```

---

## 8. Các animation pattern tái sử dụng

### Slide in từ trái (code lines, list items)

```js
tl.set("#el", { autoAlpha: 0, x: -50 }, 0);
tl.to("#el", { autoAlpha: 1, x: 0, duration: 0.45, ease: "power3.out" }, TIME);
```

### Fade + scale in (cards, titles)

```js
tl.set("#el", { autoAlpha: 0, scale: 0.9 }, 0);
tl.to(
  "#el",
  { autoAlpha: 1, scale: 1, duration: 0.7, ease: "back.out(1.4)" },
  TIME,
);
```

### Slide up (bottom elements)

```js
tl.set("#el", { autoAlpha: 0, y: 40 }, 0);
tl.to("#el", { autoAlpha: 1, y: 0, duration: 0.6, ease: "power3.out" }, TIME);
```

### Bounce drop (items rơi vào ô)

```js
tl.set("#el", { autoAlpha: 0, y: -60 }, 0);
tl.to("#el", { autoAlpha: 1, y: 0, duration: 0.4, ease: "bounce.out" }, TIME);
```

### Stagger group

```js
tl.to(
  ["#el-0", "#el-1", "#el-2"],
  {
    autoAlpha: 1,
    x: 0,
    duration: 0.4,
    ease: "power3.out",
    stagger: 0.15,
  },
  TIME,
);
```

### Strikethrough (gạch ngang text)

```js
tl.to("#el", { color: "rgba(110,118,129,0.5)", duration: 0.25 }, TIME);
tl.add(() => {
  const el = document.querySelector("#el");
  if (el && !el.querySelector(".strike")) {
    const s = document.createElement("span");
    s.className = "strike";
    s.style.cssText =
      "position:absolute;left:0;top:50%;height:2px;background:#f85149;width:0;transform:translateY(-50%);border-radius:2px;";
    el.style.position = "relative";
    el.appendChild(s);
    gsap.to(s, { width: "100%", duration: 0.35, ease: "power2.inOut" });
  }
}, TIME + 0.1);
```

### Fade in code line (thay typewriter — không bị giật)

```js
// Set innerHTML trước, rồi fade in — KHÔNG dùng typewriter char-by-char
document.getElementById("line1").innerHTML =
  "...html với syntax highlighting...";
tl.set("#line1", { autoAlpha: 0 }, 0);
tl.to("#line1", { autoAlpha: 1, duration: 0.5, ease: "power2.out" }, TIME);
```

**Lỗi đã gặp:** Typewriter effect (set innerHTML từng ký tự) bị giật khi render vì renderer capture frame tại thời điểm cụ thể, không phải realtime. Fix: set full innerHTML ngay từ đầu, dùng GSAP `autoAlpha` để fade in.

---

## 9. CSS design system — màu sắc chuẩn

```css
/* Background */
--bg-main: #0f1117;
--bg-card: rgba(9, 9, 11, 0.7);
--bg-border: rgba(255, 255, 255, 0.08);

/* Syntax highlighting */
--keyword: #ff7b72; /* if, for, def, class */
--string: #a5d6ff; /* "text" */
--variable: #79c0ff; /* tên biến */
--operator: #d2a8ff; /* =, +, - */
--bracket: #d2a8ff; /* [], {}, () */
--comment: #8b949e; /* # comment */
--function: #d2a8ff; /* print(), len() */

/* Semantic */
--good: #3fb950; /* panel phải, kết quả tốt */
--bad: #f85149; /* panel trái, lỗi */
--accent: #ffa657; /* highlight, element */
--index: #d2a8ff; /* index label */

/* Text */
--text-primary: #e6edf3;
--text-secondary: #c9d1d9;
--text-muted: #8b949e;
```

---

## 10. Quy trình sản xuất tối ưu — thứ tự làm việc

### Bước 1: Lập timeline tổng thể trước khi code

Tạo bảng này trước khi viết 1 dòng HTML:

| Scene | Start (root) | Duration | Audio file   | Nội dung chính      |
| ----- | ------------ | -------- | ------------ | ------------------- |
| 01    | 0s           | 38.84s   | scene_01.mp3 | Tại sao dùng List   |
| 02    | 38.84s       | 45.24s   | scene_02.mp3 | Khái niệm & Cú pháp |
| 03    | 84.08s       | 27.17s   | scene_03.mp3 | Thuật ngữ           |

### Bước 2: Setup `index.html` trước

- Tạo tất cả scene clip stubs
- Thêm tất cả `<audio>` với absolute timestamps
- Chạy `npm run check` → phải pass 0 errors

### Bước 3: Viết từng scene theo template

- Copy template từ Section 3
- Lên timeline animation cho scene đó (viết comment trước, code sau)
- Chạy `npm run check` sau mỗi scene

### Bước 4: Review animation timing trên paper trước khi code

```
Scene 01 (38.84s):
0.2  → intro fade in
3.2  → intro fade out
4.2  → main title fade in
7.5  → main title lên góc
8.4  → split container hiện
9.0  → v1 slide in
...
```

Viết ra trước, code sau. Tránh sửa đi sửa lại.

### Bước 5: Render một lần duy nhất

Chỉ render khi:

- `npm run check` pass 0 errors
- Đã review animation timing trên paper
- Tất cả scene đã xong

---

## 11. Những điều KHÔNG làm

```js
// ❌ KHÔNG dùng Math.random()
Math.random() * 100

// ❌ KHÔNG dùng Date.now()
Date.now()

// ❌ KHÔNG đặt audio trong sub-composition
// (trong Scene_XX.html)
<audio data-start="0" src="..."></audio>

// ❌ KHÔNG dùng typewriter effect
setInterval(() => { el.textContent += chars[i++]; }, 50)

// ❌ KHÔNG hiện element chính trước khi intro title kết thúc
tl.to("#intro-title", ..., 0.2);
tl.to("#main-content", ..., 1.0); // quá sớm, intro title chưa xong

// ❌ KHÔNG quên position argument trong tl.set()
tl.set(".clip", { autoAlpha: 1 }); // thiếu , 0

// ❌ KHÔNG quên id trên audio element
<audio data-start="0" src="..."></audio> // thiếu id
```

---

## 12. Quick reference — các giá trị hay dùng

```js
// Intro title lên góc trên-trái
{ scale: 0.38, x: -760, y: -460 }

// Intro title lên góc trên-căn giữa
{ scale: 0.38, x: 0, y: -460 }

// Card standard
{ background: "rgba(9,9,11,0.7)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: "20px" }

// Glow xanh lá (good)
{ boxShadow: "0 0 50px rgba(63,185,80,0.25)" }

// Glow xanh dương (info)
{ boxShadow: "0 0 40px rgba(121,192,255,0.2)" }

// Ease hay dùng
"back.out(1.4)"   // spring nhẹ cho title
"power3.out"      // slide in nhanh
"power2.in"       // fade out
"bounce.out"      // bounce drop
"power3.inOut"    // di chuyển vị trí
```
