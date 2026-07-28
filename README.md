# 🤖 Elearning Content Factory — Multi-Agent Learning Material Generator

> **Hệ thống sản xuất học liệu tự động đa tác nhân (Multi-Agent Architecture) quy mô lớn — 100% Dynamic, Generic, Stack-Agnostic & Schema-Driven (Tuyệt đối Không Hardcode).**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![Node.js 18+](https://img.shields.io/badge/Node.js-18+-green?logo=nodedotjs)](https://nodejs.org)
[![LangGraph / Antigravity](https://img.shields.io/badge/Orchestration-Antigravity-purple)](.)
[![Schema-Driven](https://img.shields.io/badge/Architecture-Pydantic%20Schema%20Driven-emerald)](.)
[![HyperFrames Video](https://img.shields.io/badge/Video%20Engine-HyperFrames-red)](.)
[![SCORM 1.2](https://img.shields.io/badge/Export-SCORM%201.2-green)](.)

---

## 📋 Mục Lục

1. [Giới thiệu tổng quan](#-giới-thiệu-tổng-quan)
2. [Các loại học liệu hệ thống sinh tự động](#-các-loại-học-liệu-hệ-thống-sinh-tự-động)
3. [Yêu cầu tiền đề (Prerequisites)](#-yêu-cầu-tiền-đề-prerequisites)
4. [Hướng dẫn cài đặt chi tiết (Installation Guide)](#-hướng-dẫn-cài-đặt-chi-tiết-installation-guide)
5. [Cấu hình biến môi trường (.env)](#-cấu-hình-biến-môi-trường-env)
6. [Hướng dẫn sử dụng & Khởi chạy hệ thống (Usage Guide)](#-hướng-dẫn-sử-dụng--khởi-chạy-hệ-thống-usage-guide)
   - [6.1. Sinh bộ học liệu đầy đủ qua CLI Workflow](#61-sinh-bộ-học-liệu-đầy-đủ-qua-cli-workflow)
   - [6.2. Sản xuất Video HyperFrames (Audio TTS ➔ GSAP ➔ MP4)](#62-sản-xuất-video-hyperframes-audio-tts--gsap--mp4)
   - [6.3. Kiểm thử các Module Core & Validator](#63-kiểm-thử-các-module-core--validator)
7. [Cấu trúc thư mục dự án](#-cấu-trúc-thư-mục-dự-án)
8. [Quy chuẩn thiết kế học liệu chuẩn hệ thống (AGENTS.md)](#-quy-chuẩn-thiết-kế-học-liệu-chuẩn-hệ-thống-agentsmd)
9. [FAQ & Xử lý lỗi thường gặp](#-faq--xử-lý-lỗi-thường-gặp)

---

## 🌟 Giới Thiệu Tổng Quan

**Elearning Content Factory** là hệ thống AI đa tác nhân chuyên nghiệp tự động hóa việc chuyển đổi chương trình khung `syllabus.json` (hoặc PM Excel) thành bộ tài nguyên học liệu đa phương tiện hoàn chỉnh cho **bất kỳ công nghệ nào** (Python, Java, React, SQL, Flutter, DevOps...):

- **100% Tiếng Việt có dấu chuẩn sản xuất** & thuật ngữ tiếng Anh `snake_case` / `camelCase`.
- **Phân định phạm vi kiến thức động (Dynamic Scope Boundaries)**: Tự động chặn từ khóa vượt cấp.
- **Pipeline Video Voice-Driven (HyperFrames)**: Đồng bộ hoạt họa UI GSAP theo từng miligiây giọng đọc TTS (Kokoro AI).

---

## 📚 Các Loại Học Liệu Hệ Thống Sinh Tự Động

| Loại Học Liệu | Định dạng Đầu ra | Đặc tả & Tiêu chuẩn Sư phạm |
|---|---|---|
| 📖 **Bài đọc lý thuyết** | `reading.html` & `reading_all.html` | Cấu trúc list ngắt ý ngắn gọn, 100% tiếng Việt có dấu, ảnh bối cảnh 16:9, Dark Terminal Console, Self-Test left-alignment. |
| 🖼️ **Slide bài giảng** | `slides.html` | Master HTML Slides (15-20 slides/session), Bento Grid modern, 3-30-300 typography, Card Color Coding, Dual Theme (Light/Dark), NO Emoji. |
| 📝 **Bài tập thực hành** | Markdown + Code files | 6 bài tập theo bối cảnh doanh nghiệp (4 cấp độ Bloom: Vận dụng ➔ Phân tích ➔ Sáng tạo). Code 100% tiếng Anh. |
| 🧪 **Mini Project / Lab** | Markdown + Checklist | Bố cục 3 phần: Mục tiêu ➔ Các bước thực hiện ➔ Checklist đánh giá định lượng `[ ]`. |
| ❓ **Quizz Trắc nghiệm** | Excel (.xlsx) + JSON | 5 câu/lesson (Bloom), Entrance Quiz 45 câu (30 cũ + 15 mới), Exit Quiz 45 câu (100% mới). 7 nguyên tắc sư phạm Quizz. |
| 🎬 **Video HyperFrames** | MP4 Video (1080p) | 8-Stage Pipeline: Script ➔ Human Review Gate ➔ Kokoro TTS ➔ Duration Probing ➔ Voice-Driven GSAP HTML Compositions ➔ Puppeteer MP4 Render. |
| 🗺️ **Visualizer & Mindmap** | HTML / JS Interactive | Interactive DOM canvas (`#visualizer-canvas`), high-contrast code tracker highlighting, console log panel. |

---

## 🛠️ Yêu Cầu Tiền Đề (Prerequisites)

Trước khi cài đặt, hãy đảm bảo máy tính của bạn đã cài đặt các công cụ sau:

1. **Python**: Phiên bản `3.10` trở lên ([Tải Python](https://www.python.org/downloads/)).
2. **Node.js & npm**: Phiên bản `18.0.0` trở lên ([Tải Node.js](https://nodejs.org/)).
3. **FFmpeg**: Cần thiết cho quá trình render & merge audio/video MP4 ([Tải FFmpeg](https://ffmpeg.org/download.html)).
4. **Git**: Công cụ quản lý mã nguồn.

---

## 📥 Hướng Dẫn Cài Đặt Chi Tiết (Installation Guide)

### Bước 1: Clone repository về máy
```bash
git clone https://github.com/ngoquy12/learning_material.git
cd Learning-Material
```

### Bước 2: Khởi tạo và kích hoạt môi trường ảo Python
* **Trên Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```
* **Trên macOS / Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### Bước 3: Cài đặt các thư viện Python
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Bước 4: Cài đặt các gói Node.js (cho HyperFrames Render Engine)
```bash
npm install
```

### Bước 5: Kiểm tra cài đặt Puppeteer (Browser Renderer)
Cài đặt Chromium cho Puppeteer để phục vụ render video MP4:
```bash
npx puppeteer browsers install chrome
```

---

## ⚙️ Cấu Hình Biến Môi Trường (.env)

Tạo file `.env` tại thư mục gốc của dự án `Learning-Material/.env`:

```env
# API Keys cho hệ thống Multi-Agent
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Cấu hình giọng đọc Kokoro TTS (Default: hung_thinh / speed: 0.95)
KOKORO_TTS_VOICE=hung_thinh
KOKORO_TTS_SPEED=0.95

# Cấu hình Output Directory
DEFAULT_OUTPUT_DIR=output/PM_Python
```

---

## 🚀 Hướng Dẫn Sử Dụng & Khởi Chạy Hệ Thống (Usage Guide)

### 6.1. Sinh bộ học liệu đầy đủ qua CLI Workflow

Để khởi chạy toàn bộ hệ thống tự động sinh tài nguyên cho một khóa học từ `syllabus.json`:

```bash
python main.py --syllabus "path/to/syllabus.json" --output "output/PM_Python"
```

Hoặc sử dụng các cờ tùy chọn nâng cao:
```bash
# Chỉ sinh Bài đọc & Slide bài giảng
python main.py --syllabus "path/to/syllabus.json" --types reading,slide

# Sinh Bài tập & Quizz trắc nghiệm xuất file Excel
python main.py --syllabus "path/to/syllabus.json" --types exercise,quiz
```

---

### 6.2. Sản xuất Video HyperFrames (Audio TTS ➔ GSAP ➔ MP4)

Quy trình sản xuất Video HyperFrames gồm **6 Giai Đoạn Chuẩn Hóa**:

```
 ┌────────────────┐     ┌──────────────────────┐     ┌───────────────────────┐
 │ Stage 1: Setup │ ──► │ Stage 2 & 3: Kokoro  │ ──► │ Stage 4: Probed Audio │
 │ Project Dirs   │     │ TTS Parallel Synth   │     │ Durations (json)      │
 └────────────────┘     └──────────────────────┘     └───────────┬───────────┘
                                                                 │
 ┌────────────────┐     ┌──────────────────────┐                 │
 │ Stage 6: Render│ ◄── │ Stage 5: Voice-Driven│ ◄───────────────┘
 │ Puppeteer MP4  │     │ GSAP HTML Comps      │
 └────────────────┘     └──────────────────────┘
```

#### Bước 1: Viết kịch bản & Trình bày Review Gate (`SCRIPT.md`)
Tạo kịch bản bài học với Lời thoại TTS tự nhiên (dẫn dắt bối cảnh ➔ khái niệm ➔ ví dụ ➔ câu chốt) và giao diện Dark Theme (`#09090b`, tiêu đề trắng `#ffffff`).

#### Bước 2: Khởi chạy Pipeline sinh Video Project bằng Script Python
Tạo hoặc chạy script build trong thư mục `scratch/`:

```bash
python -X utf8 scratch/build_lesson02_s08.py
```

*Script sẽ tự động:*
1. Tổng hợp giọng đọc tiếng Việt bằng Kokoro TTS.
2. Bóc tách thời lượng âm thanh thực tế millisecond vào `assets/tts/durations.json`.
3. Sinh các phân cảnh `Scene_01.html`, `Scene_02.html`... được căn thời gian hoạt họa GSAP khớp 100% với giọng đọc.
4. Đóng gói file master `index.html` và `package.json`.

#### Bước 3: Render xuất file MP4 hoàn chỉnh
Di chuyển vào thư mục video project được sinh ra và chạy lệnh render:

```bash
cd "output/PM_Python/Session 08 - Hàm (Function) va Phạm vi biến/Lesson 02 - Tham số và giá trị trả về/Video/session_08_lesson_02"
npm run render
```

Video MP4 hoàn chỉnh sẽ được lưu tại thư mục `renders/session_08_lesson_XX_YYYY-MM-DD_HH-MM-SS.mp4`.

---

### 6.3. Kiểm thử các Module Core & Validator

Bạn có thể kiểm thử trực tiếp từng thành phần lõi của hệ thống:

```bash
# 1. Kiểm thử Master Programmatic Validator
python -c "from core.validators.master_validator import validate_resource; print(validate_resource('READING', '<div>Nội dung học liệu...</div>'))"

# 2. Kiểm thử Scope Calculator Engine
python -c "from core.scope_calculator import ScopeCalculator; calc = ScopeCalculator(); print(calc.get_allowed_scope(1))"

# 3. Kiểm thử Code Sandbox Adapter
python -c "from core.sandbox_adapter import get_sandbox_config; print(get_sandbox_config('python'))"
```

---

## 📁 Cấu Trúc Thư Mục Dự Án

```
Learning-Material/
├── .agents/                  # Quy chuẩn hệ thống & Quy định thiết kế (AGENTS.md)
│   └── AGENTS.md             # Single Source of Truth cho Quy chuẩn Sư phạm & UI
├── agents/                   # Đội ngũ Multi-Agent (Creator, Reviewer, Writer)
│   ├── creator_agents.py     # Prompt & Logic sinh bài đọc, bài giảng, video
│   ├── reviewer_agents.py    # Agent kiểm định tích hợp Master Validator
│   └── hyperframes_writer_agent.py # Agent chuyên sinh composition HTML video
├── core/                     # Động cơ lõi (Core Infrastructure)
│   ├── scope_calculator.py   # Tính toán phạm vi kiến thức động
│   ├── sandbox_adapter.py    # Bộ chuyển đổi Code Sandbox động (Pyodide/Worker)
│   ├── session_compilers.py  # Bộ gộp bài học thành reading_all.html & slides
│   ├── schemas/              # Pydantic Declarative JSON Schemas
│   ├── renderers/            # Generic Static Renderers
│   └── validators/           # Master Programmatic Validation Layer
├── hyperframes/              # Động cơ sản xuất Video AI (HyperFrames Engine)
│   ├── video_pipeline_engine.py  # VoiceDrivenVideoEngine điều phối 6 giai đoạn
│   ├── ui_manager.py         # Thư viện UI Component & Renderer
│   └── dev-tutorial-video/   # Remotion / Puppeteer Template base
├── skills/                   # Bộ Kỹ năng Chuyên biệt (Skill Repository)
│   ├── reading_generator/    # Kỹ năng sinh Bài đọc học liệu
│   ├── exercise_generator/   # Kỹ năng sinh Bài tập 6 cấp độ
│   ├── lab_generator/        # Kỹ năng sinh Bài thực hành Lab
│   ├── quiz_generator/       # Kỹ năng sinh Quizz & Ma trận đề
│   ├── slide_generator/      # Kỹ năng sinh Slide HTML Master
│   └── video_production_standard/ # Quy chuẩn sản xuất Video 8 giai đoạn
├── output/                   # Kết quả học liệu đã xuất theo môn học & Session
├── scratch/                  # Scripts hỗ trợ build & test nhanh
├── requirements.txt          # Danh sách thư viện Python
├── package.json              # Danh sách gói Node.js
└── main.py                   # Điểm khởi chạy chính của CLI
```

---

## 🛡️ Quy Chuẩn Thiết Kế Học Liệu Chuẩn Hệ Thống (AGENTS.md)

Tất cả các Agent và Module trong hệ thống bắt buộc phải tuân thủ nghiêm ngặt **Quy chuẩn Thiết kế Học liệu** được quy định tại [.agents/AGENTS.md](file:///.agents/AGENTS.md):

1. **Bài Đọc (`reading.html`)**: Scannable Bullets (`- Ý chính` / `  - Chi tiết`), 100% tiếng Việt có dấu, ảnh bối cảnh 16:9, Code Cards (Good vs Bad), Dark Terminal Console, Self-Test left-alignment.
2. **Bài Tập (6 Exercises)**: Đặt trong bối cảnh thực tế doanh nghiệp (LMS, Điểm danh, Khảo thí...), 4 cấp độ Bloom (Vận dụng ➔ Phân tích ➔ Sáng tạo). Code 100% tiếng Anh `snake_case`.
3. **Bài Thực Hành Lab**: 3 phần chuẩn hóa (Mục tiêu ➔ Các bước ➔ Checklist đánh giá `[ ]`).
4. **Quizz Trắc Nghiệm**: 7 nguyên tắc sư phạm Quizz, ma trận đề 5 câu/lesson, 45 câu Entrance Quiz (30 cũ + 15 mới), 45 câu Exit Quiz (100% mới).
5. **Slide Bài Giảng**: Limit 15-20 slides/session, Bento Grid modern, Typography 3-30-300, Card Color Coding, Dual Theme (Light/Dark), NO Emoji.
6. **Video HyperFrames**: Voice-UI Separation, Human Script Review Gate, Voice-Driven GSAP animation, Dark Theme (`#09090b`), tiêu đề trắng (`#ffffff !important`), **CẤM `border-left` màu accent**, **CẤM badge số thứ tự thừa**.
7. **System Rules**: Strict No ALL CAPS (dùng `Sentence case`), High-Contrast Dark Code syntax highlighting, Synchronized Visualizer DOM IDs.

---

## ❓ FAQ & Xử Lý Lỗi Thường Gặp

* **Q: Làm sao để thay đổi môn học hoặc ngôn ngữ lập trình khác?**
  * *Trả lời:* Cung cấp file `syllabus.json` của môn học đó. Hệ thống sẽ tự động tính toán Scope, cấm từ khóa vượt cấp và áp dụng quy chuẩn Naming Convention tương ứng (`snake_case` cho Python/DB, `camelCase` cho JS/Java).
* **Q: Lỗi `Puppeteer render failed` hoặc thiếu Chrome browser khi render MP4?**
  * *Trả lời:* Chạy lệnh `npx puppeteer browsers install chrome` để tải Chrome binary cho Puppeteer.
* **Q: Giọng đọc Kokoro TTS bị thiếu hoặc lỗi âm thanh khi build video?**
  * *Trả lời:* Đảm bảo đã tải hoặc đặt runtime Kokoro-Vietnamese trong dự án hoặc cấu hình `KOKORO_TTS_VOICE=hung_thinh` trong `.env`.
* **Q: Làm thế nào để điều chỉnh thời lượng các phân cảnh video?**
  * *Trả lời:* Động cơ `VoiceDrivenVideoEngine` tự động đo thời lượng audio TTS mili-giây và lưu vào `assets/tts/durations.json`. Thời lượng UI GSAP sẽ tự động dãn/co theo giọng đọc thực tế.

---

**Elearning Content Factory** — *Giải pháp tự động hóa học liệu chuẩn quốc tế cho mọi môn học công nghệ.*
