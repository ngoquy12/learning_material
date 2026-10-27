---
name: session_reading_compiler
description: Synchronize master session reading hub (reading_all.html) with modern light theme, Rikkei Education branding, redundant header stripping, and opacity-based iframe positioning for crisp Mermaid rendering. Target output language is 100% Accented Vietnamese.

---

# Session Reading Compiler Skill — Rikkei Education Standards

## 1. Core Architectural & Visual Directives

> [!IMPORTANT]
> **LIGHT THEME & SESSION READING HUB DIRECTIVES (`reading_all.html`):**
>
> 1. **Bright Light Theme & Rikkei Education Branding**:
>    - Master Hub interface of `reading_all.html` MUST use a clean white background (`#f8fafc` / `#ffffff`), with the top Header featuring the **Official Rikkei Education Logo**: `https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png`.
> 2. **Opacity-Based Viewport Positioning (Prevent Mermaid Render Crashes)**:
>    - **FORBIDDEN TO USE `display: none` ON LESSON IFRAMES**: Using `display: none` sets bounding boxes to zero (`getBBox() = 0x0`), causing Mermaid 10.9.6 rendering engine to crash with `Syntax error in text`.
>    - **MANDATORY TO USE CSS OPACITY & Z-INDEX**:
>      ```css
>      .viewport-panel {
>        flex: 1;
>        height: 100%;
>        background: #ffffff;
>        position: relative;
>      }
>      .lesson-frame {
>        position: absolute;
>        top: 0;
>        left: 0;
>        width: 100%;
>        height: 100%;
>        border: none;
>        opacity: 0;
>        pointer-events: none;
>        z-index: 1;
>        transition: opacity 0.15s ease-in-out;
>      }
>      .lesson-frame.active {
>        opacity: 1;
>        pointer-events: auto;
>        z-index: 10;
>      }
>      ```
> 3. **Inner Header Stripping**:
>    - When loading individual lesson readings (`reading.html`) into `reading_all.html`, **MUST STRIP OR HIDE** inner lesson headers (`#sticky-header`, `header`) to prevent duplication with the Session Master Header.
> 4. **Pure Static JS Logic (No Auto-Reload / No History Triggers)**:
>    - FORBIDDEN to use `history.replaceState`, `location.hash`, or `localStorage` inside tab switching handlers to avoid triggering Live Server auto-reloads.

---

## 2. Layout & UI Standards

The `reading_all.html` document is engineered to corporate branding standards:

1. **Single Master Header Bar**:
   - Display **Rikkei Education Logo** (`https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png`) on top left.
   - Session Title in Montserrat font (`#0f172a`).

2. **Left Navigation Sidebar (Light Theme)**:
   - Clean white panel (`#ffffff`), subtle borders (`#e2e8f0`).
   - List lessons with brand red index badges (`#be111c`).
   - Active state: Light crimson background `rgba(190, 17, 28, 0.08)`, brand red text `#be111c`, border `rgba(190, 17, 28, 0.25)`.

3. **Pure Isolated Viewport**:
   - Use `<iframe class="lesson-frame" src="Lesson XX.../reading.html"></iframe>` to isolate CSS styles and preserve original HTML formatting.
