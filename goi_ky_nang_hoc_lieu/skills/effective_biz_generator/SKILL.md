---
name: effective_biz_generator
description: Generate self-contained, high-impact interactive HTML Visualizations & Strategic Framework Diagrams (based on plannotator/effective-html) for Business Administration, Economics, Management, and Non-IT subjects. Target output language is 100% Accented Vietnamese.
---

# Effective HTML Business & Framework Visualizer Skill — Rikkei Education Standards

Adapted and standardized from the **[plannotator/effective-html](https://github.com/plannotator/effective-html)** architecture, this skill specializes in generating interactive learning materials for **Business Administration, Economics, Marketing, Finance, HR Management & Non-IT courses**.

---

## 1. "Effective HTML" Design Philosophy for Business Education
Unlike Programming (IT) courses requiring code trackers or terminal logs, Business courses demand visualization of **Conceptual Frameworks, Business Workflows, Value Chains**, and **Strategic Matrices**.

Generated HTML documents MUST adhere to the 5 core principles of `effective-html`:
1. **Full-screen High-Density Visual Stage**:
   - Central page features a high-quality interactive SVG diagram / business architecture model (`html-diagram`).
   - Nodes, paths, and strategy chips are rendered crisp and balanced, illustrating cause-and-effect relationships.
2. **Dismissible Overlay Detail Panels**:
   - Clicking any Node or step highlights related data flows and pops up a `Detail Drawer / Card Panel` detailing:
     * Definitions & Strategic Importance.
     * Key Performance Indicators (KPIs / Metrics).
     * Enterprise Case Studies / Real-world Scenarios.
   - All overlay panels MUST include a prominent close button (`[×] Close button`).
3. **Interactive Canvas Pan & Zoom**:
   - Supports 1:1 drag-to-pan in SVG canvas space and mouse wheel zooming.
   - Includes Zoom Control Panel (`[ - ] 100% [ + ] [ Reset ]`).
4. **Self-Contained Dark/Light Theme System**:
   - Built-in CSS variables on `:root` and `html.dark`.
   - Light/Dark mode switcher with `localStorage` persistence.
5. **Plan & Strategy Matrix Mode (`html-plan`)**:
   - Below the visual diagram is a strategic analysis table, action checklists, and decision matrices (e.g. SWOT/TOWS, Porter's 5 Forces, Business Model Canvas).

---

## 2. Standard Layout Architecture (Effective Business Dashboard Layout)

```
+───────────────────────────────────────────────────────────────────────────────────────────────+
| [Header] BUSINESS ADMINISTRATION PROGRAM • CORE LESSON      | [☀/🌙 Theme Toggle]  [Reset Zoom] |
+───────────────────────────────────────────────────────────────────────────────────────────────+
| [INTERACTIVE FRAMEWORK STAGE - PAN/ZOOM SVG CANVAS]                                           |
|                                                                                               |
|      +───────────────────+             +───────────────────+             +─────────────────+  |
|      | 1. Market Research|   ────────> | 2. Strategic      |   ────────> | 3. Execution &  |  |
|      | & Analysis        |             | Planning          |             | KPI Control     |  |
|      +───────────────────+             +───────────────────+             +─────────────────+  |
|               │                                  │                                 │          |
|               ▼                                  ▼                                 ▼          |
|      [ Target Customer ]               [ Competitive Edge ]              [ Revenue Dashboard ]|
+───────────────────────────────────────────────────────────────────────────────────────────────+
| [DISMISSIBLE DETAIL DRAWER - INTERACTIVE CARD PANEL]                                  [× Close]|
| • Selected Node Title: COMPETITIVE STRATEGY PLANNING                                          |
| • Definition: Brand positioning & Core Unique Selling Proposition (USP)...                    |
| • Key KPIs: Market Share %, CAC, LTV...                                                       |
| • Case Study: How Apple applies product differentiation...                                    |
+───────────────────────────────────────────────────────────────────────────────────────────────+
| [STRATEGIC PLAN & IMPLEMENTATION MATRICES (`html-plan` Section)]                              |
| <details open> 1. Enterprise Case Study Analysis & Management Challenges </details>           |
| <details> 2. Strategy Selection Matrix & Implementation Roadmap </details>                    |
| <details> 3. Case Study Workshop & Discussion </details>                                      |
+───────────────────────────────────────────────────────────────────────────────────────────────+
```

---

## 3. Code Standards for HTML/CSS/JS (Effective HTML Template Rules)

1. **Brand Typography & Curated Palette**:
   - Fonts: `Inter` for body, `Montserrat` for headings.
   - Professional Palette:
     * Primary (`--primary`): Navy / Deep Slate (`#1E293B` / `#38BDF8`).
     * Accent (`--accent`): Warm Rust / Gold (`#D97757` / `#F59E0B`).
     * Background (`--bg-body`): Clean Sand (`#FAF9F5`) for Light Mode, Deep Obsidian (`#0B0F19`) for Dark Mode.

2. **SVG Graphics & Interactive Events**:
   - All SVG elements wrapped inside `<g id="svg-content">`.
   - Native Vanilla JS handlers for `pointerdown`, `pointermove`, `pointerup` for smooth 1:1 panning.
   - SVG nodes contain `data-node-id="node-1"` and click handlers to trigger Detail Panels.

3. **100% Self-Contained Offline Portability**:
   - All CSS and JS styles MUST be embedded inside a single HTML file for offline portability.

