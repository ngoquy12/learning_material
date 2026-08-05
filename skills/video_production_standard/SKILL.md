---
name: video_production_standard
description: End-to-End E-learning Video Production Standard Operating Procedure (Voice-First Pipeline & UI Component Standards) from script blueprint, Kokoro-Vietnamese TTS audio generation, to Puppeteer 1080p60 MP4 rendering. Target output language is 100% Accented Vietnamese.
---

# END-TO-END E-LEARNING VIDEO PRODUCTION STANDARD SOP

This document defines the **Standard 8-Stage Operating Procedure (8-Stage SOP)** for AI Agents (Video Director Agent, HyperFrames Writer Agent, Reviewer Agent) and Material Engineers to automate high-quality 1080p60 video creation.

---

## 📌 THE 8-STAGE STANDARD PIPELINE

### 1. Stage 1: SSOT Analysis & Pronunciation Dictionary Standardization (Pre-Script Gate)
- **Official SSOT**: Read `reading.html` / `reading.md` as the Single Source of Truth.
- **Technical Dictionary (`Kokoro-Vietnamese/configs/tech_dictionary.json`)**:
  - Preserve standard English terms (`Python`, `TypeError`, `ValueError`, `VS Code`, `Terminal`, `Console`, `Class`, `Object`, `snake_case`, `Heap`, `Stack`).
  - FORBIDDEN awkward Vietnamese phonetic spellings ("snếch-kê-xơ", "Tai-pơ É-rơ").

### 2. Stage 2: Script Design & Voice-UI Separation (Pedagogy & Voice-UI Gate)
- **Target Duration**: 3 - 6 minutes (180s - 360s) per video. If exceeding 7 minutes (420s), MUST split into multi-part episodes (`Part 1`, `Part 2`).
- **100% Separation Between Narration (TTS) & Screen Display (UI)**:
  - **Narration (TTS Script)**: Handles detailed explanations, pedagogical context, and core rationale ("WHY").
  - **Screen Display (UI)**: ABSOLUTELY FORBIDDEN to paste full narration sentences on screen. UI display ONLY contains:
    - Concise titles (3 - 5 words).
    - Technical bullet keywords (3 - 6 words).
    - Production-Ready code snippets.
    - Vector Icons (`<svg>`) or Block Diagrams.

### 3. Stage 3: Script Review & Human Approval Gate
- **MANDATORY HUMAN APPROVAL STEP (STOP & ASK FOR APPROVAL)**:
  - Agent generates `blueprint.json` and `script_review.md` summarizing scene-by-scene script details (including `narration` text and `clean_content` UI tags).
  - Agent **STOPS** and presents the script table for User review.
  - **PROCEED TO VOICE GENERATION (STAGE 4) ONLY AFTER** User approves script.

### 4. Stage 4: Voice-First Audio Generation & Duration Probe Gate
- **TTS-First Workflow**:
  1. Execute `gen_tts.py` / `VoiceDrivenVideoEngine` to generate Kokoro-Vietnamese TTS audio files (`assets/tts/Scene_01.wav` .. `Scene_XX.wav`).
  2. Use `soundfile` / `ffprobe` to measure exact duration (millisecond precision) of each `.wav` file.
  3. Export `assets/tts/durations.json`.
  4. Update actual `duration` properties in `blueprint.json` BASED ON real audio lengths (stripping excess silence).

### 5. Stage 5: Independent Audio Track Separation Gate
- **Audio Track Allocation in `index.html`**:
  - Voiceover Track (TTS): `data-track-index="20"` ➔ `"35"` (Separate track per scene).
  - Background Music (`bg-music`): MUST assign **`data-track-index="99"`** (Volume: `0.10` - `0.12`, `loop="true"`).
  - FORBIDDEN to overlay background music and voiceover on the same track index.

### 6. Stage 6: Voice-Driven HTML Composition Gate
- **MANDATORY EXECUTION SEQUENCE**: Sub-composition HTML files (`Scene_XX.html`) and Master Timeline (`index.html`) MUST ONLY BE GENERATED AFTER REAL VOICEOVER DURATIONS ARE MEASURED from Stage 4. Ensures GSAP keyframes match 100% with AI voice duration.
- **Intro & Outro Sub-composition Separation**:
  - Create 2 independent sub-composition files: `src/compositions/Intro.html` (9.24s) and `src/compositions/Outro.html` (12.15s).
  - Declare as Composition Clips in `index.html`:
    - Intro Clip: `data-composition-src="src/compositions/Intro.html"`, `data-start="0"`, `data-duration="9.24"`.
    - Outro Clip: `data-composition-src="src/compositions/Outro.html"`, `data-start="{OUTRO_START}"`, `data-duration="12.15"`.
- **Light Theme & Clean Typography Standards**:
  - **Canvas Background (1920x1080)**: Soft warm light gradient `background: linear-gradient(135deg, #f8fafc 0%, #edf2f7 100%)`.
  - **Default Typography**: **Be Vietnam Pro** (`font-family: 'Be Vietnam Pro', sans-serif;`) for crisp Vietnamese diacritics.
  - **Brand Logo**: Rikkei logo `<img>` fixed at **TOP-RIGHT** (`top: 50px; right: 80px; height: 52px; z-index: 100`).
  - **Brand Accent Color (`#ba252a` Rikkei Red)**:
    - **Main Scene Title**: Fixed at **TOP-LEFT** (`top: 50px; left: 80px; font-size: 44px; font-weight: 800; color: #ba252a`), aligned horizontally parallel to Logo.
    - **Number Badge**: Rikkei Red (`background: #ba252a; color: #ffffff`).
    - **Card Borders & Icons**: Left border accent (`border-left: 6px solid #ba252a`), sublist icon `#ba252a`.
    - **Code Card Header**: Top border accent (`border-top: 5px solid #ba252a`), language tag `#ba252a`.
  - **Strict Left-Alignment (`text-align: left !important`)**: All titles, descriptions, sub-bullets, and code snippets.
  - **Monospace Fira Code**: Use `<pre class="code-body">` left-aligned with exact 4-space indentation.

### 7. Stage 7: Local Sanity Check Gate
- Check file links: `npm run check`
- Live interactive preview in browser: `npm run dev`

### 8. Stage 8: Puppeteer 1080p60 MP4 Render Gate
- Render video: `npm run render`
- Final MP4 output saved at `renders/session_XX_lesson_YY_TIMESTAMP.mp4`.

---

## 🛠️ USER & AGENT CLI EXECUTION GUIDE

### Method 1: CLI Automated Pipeline Execution
```bash
# Generate video script & project for Lesson 01 Session 06 (Voice-First Pipeline)
python -X utf8 scratch/recreate_video_lesson01_session06.py

# Render high-quality 1080p60 MP4
cd "output/PM_Python/Session 06 - Cấu trúc dữ liệu List va Tuple/Lesson 01 - Khái niệm List và cách khởi tạo/Video/session_06_lesson_01"
npm run render
```

### Method 2: Interactive Dev Server Browser Preview
```bash
cd "output/PM_Python/Session 06 - Cấu trúc dữ liệu List va Tuple/Lesson 01 - Khái niệm List và cách khởi tạo/Video/session_06_lesson_01"
npm run dev
# Access local preview server: http://localhost:5173
```

