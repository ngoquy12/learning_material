---
name: video_script_generator
description: Generate Interactive HTML Studio Teleprompter Shooting Blueprints & Material Packages for Human Instructors and Studio Production Crews. Automated AI video generation is completely disabled. Target output language is 100% Accented Vietnamese. Output is saved to Video/video_script.html.
---

# Interactive HTML Studio Teleprompter Shooting Blueprint Skill — Rikkei Education Standards

## 0. Studio Production Philosophy & SSOT Extraction

Automated AI video rendering is **COMPLETELY DISABLED**.
Instead, the AI acts as a **Studio Assistant Director & Teleprompter Engineer**, extracting knowledge from the **Reading Material (`reading.html`) -> Master Slide Presentation (`slide.html`)** (the Single Source of Truth - SSOT) to generate a single-file interactive HTML Studio Teleprompter Blueprint saved to:
`[Lesson Directory]/Video/video_script.html`

---

## 1. Master HTML UI Structure & Design System Standards

The generated `Video/video_script.html` file MUST strictly adhere to the master design system established in `slide_result/video_script_lesson_1.html`:

### 1.1. Technologies & CDN Resources
- **HTML5 Standard**: `<!DOCTYPE html>` with `lang="vi"`.
- **Google Fonts**: Inter (Body), Montserrat (Headings), JetBrains Mono (Code).
- **Icons**: Phosphor Web Icons (`https://unpkg.com/@phosphor-icons/web`).
- **Styling**: Tailwind CSS CDN (`https://cdn.tailwindcss.com`) with custom color extensions (`rikkei.red: "#be111c"`, `rikkei.dark: "#0f172a"`, `rikkei.cardDark: "#151d30"`).

### 1.2. Floating Header & Interactive Controls
- **Sticky Top Bar**: `backdrop-blur-md`, responsive container.
- **Brand Title Badge**: Rikkei Red logo badge + Session ID + Lesson Title.
- **Interactive Teleprompter Font Size Control**: Buttons for Font `+`, Font `-`, and Reset `20px`.
- **Dark/Light Mode Toggle**: System auto-detect + manual toggle switch updating `document.documentElement.classList`.
- **Quick Jump Navigation Pills**: Anchor links (`#scene-0`, `#scene-1`, ..., `#scene-5`) smooth scrolling to each scene block.

### 1.3. 2-Column Scene Block Layout (`flex-col lg:flex-row gap-6`)

Every scene block MUST contain two side-by-side components:

#### Left Studio Technical Parameters Panel (`lg:w-[400px] shrink-0`)
1. **Scene Header**: Red Film Strip Badge (e.g. `Phân cảnh 01`) + Clock Duration (e.g. `00:00 - 00:45`).
2. **Scene Title & Objective Summary**: Montserrat bold title + concise 1-sentence purpose.
3. **Studio Operations Box**:
   - **Camera Angle Badge**:
     - 📷 **Cam 1 (Close-up / Primary)**: Medium Close-up on Instructor — Used for Problem Statement, Core Rationale, and Intro/Outro.
     - 💻 **Cam 2 (IDE Screen / Full Display)**: Screen display — Used for Live Coding, Code Trackers & Syntax Anatomies.
   - **Slide & Action Badges**: Slide switch cues (e.g. `Chuyển sang Slide X`) and interactive triggers.
4. **Full-Length Code Window Card** (when applicable):
   - Dark IDE Card (`bg-slate-900 border border-slate-800`).
   - File Header with Icon + Filename (e.g., `demo_init_list.py`).
   - **Copy Button** with JavaScript `copyCode(this)` function.
   - **NO SCROLLBARS**: Must show complete code vertically formatted with `whitespace-pre` and Tailwind code syntax highlighting.

#### Right Teleprompter Speech Panel (`flex-1`)
1. **Teleprompter Header**: Microphone icon + Title *"Lời thoại Teleprompter (Đọc to, rõ ràng)"* + Legend (`/ : ngắt nhịp ngắn • // : ngắt hơi nghỉ`).
2. **Teleprompter Text Box**:
   - Font size: `20px` (adjustable via header controls), `leading-[1.85]`, `font-semibold`.
   - **Pause Tags**:
     - Short pause: `<span class="pause-tag">/</span>` (styled in subtle emerald text).
     - Long breath pause: `<span class="pause-tag">//</span>` (styled in subtle rose/red text).
   - **Keyword Badges**:
     - Key tech terms: `<span class="highlight-keyword">Python List</span>` (styled in emerald badge).
     - Emphasis points: `<span class="highlight-emphasis">100 học viên</span>` (styled in indigo/sky badge).

---

## 2. Pedagogical Script & Teleprompter Directives

1. **100% Accented Vietnamese**: All speech text, titles, comments, and instructions MUST be in production-ready accented Vietnamese.
2. **Voice-UI Separation**:
   - Teleprompter text contains complete, natural, spoken sentences for the instructor.
   - Screen UI / IDE Code cards contain short code snippets, bullet points, and badges.
3. **Prerequisite Continuity Bridge (Scene 0 - Intro)**:
   - MUST begin by linking back to what was learned in the previous lesson (e.g., *"Trong bài học trước, chúng ta đã cùng nhau làm chủ Biến đơn lẻ..."*) before introducing the new topic.
4. **Forward Teaser & Practical Outcome (Closing Scene)**:
   - MUST conclude with a clear preview of the NEXT lesson topic (e.g., *"Trong Bài 2 tiếp theo, chúng ta sẽ tìm hiểu Kỹ thuật duyệt phần tử..."*) and what students will achieve with it.
5. **STRICT NO EXPLICIT SLIDE NUMBERS IN SPEECH**:
   - FORBIDDEN to say *"Nhìn vào slide 3"*, *"Ở slide 4"*, or *"Trên slide..."* in the speech text.
   - Use natural lead-in phrases instead: *"Các em hãy cùng quan sát mô hình trên màn hình..."*, *"Để hiện thực hóa trong mã nguồn..."*, *"Như các em đang quan sát trên màn hình..."*.
6. **STRICT NO HYPERBOLIC SUPERLATIVES**:
   - FORBIDDEN words: *"nhất"*, *"vô cùng"*, *"tuyệt vời"*, *"bậc nhất"*, *"triệt để"*, *"rất nhiều"*.
   - Replace *"Khám phá"* with **`Tìm hiểu`**.
   - Keep the tone academic, grounded, objective, and professional.
