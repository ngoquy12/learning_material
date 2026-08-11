---
name: image_prompt_standard
description: Technical image generation prompt standard (Imagen 3 / DALL-E / Stable Diffusion) — 2D flat vector technical infographics, strict no text emoji prohibition, vector icons/SVG, concise accented Vietnamese main titles, IDE code window cards, no duplicate badges, sequential number integrity, safe 32px outer margin, rich technical detail, 16:9 aspect ratio, strict no ALL CAPS, no 3D/neon. Target output language is 100% Accented Vietnamese.
---

# Technical Image Prompt Standard Skill — Rikkei Education Standards

## 1. Overview & Visual Design Philosophy

This skill defines the technical standards for constructing Image Prompts (Imagen 3 / DALL-E / Stable Diffusion) across all Rikkei Education learning materials.

### 1.1. Visual Style (Minimalist Yet Detailed Technical Illustration)

Clean 2D flat vector diagrams and minimalist technical infographics. Clean lines and spacious layout, yet **rich in technical detail to convey complete pedagogical context** without requiring external text.

### 1.2. Mandatory Technical Depth & Creative Detail

**Core Rule**: Minimalist does NOT mean superficial. Every image MUST be **rich in creative technical detail**:

1. **Concrete Data Values**:
   - FORBIDDEN to use abstract generic placeholders (`data`, `value`, `item`).
   - MUST use **concrete values** tied to real business contexts:
     - Arrays: `[72, 85, 91, 68, 95]` instead of `[a, b, c, d, e]`.
     - Variables: `user_age = 25`, `total_price = 150000` instead of `x = 5`.
     - Conditions: `if total > 500000` instead of `if condition`.
2. **Visual Creative Highlights**:
   - Use **color-coded zones** to group related stages (Slate for init, Emerald for main processing, Navy for output).
   - Highlight **active elements** with bold borders or contrasting background fills.
   - Use **inline micro-annotations on arrows** (`i = 0`, `i++`, `return result`) describing state transitions.
   - Add a **mini state table** in the image corner showing variable evolution (`i: 0→1→2`, `sum: 0→72→157`).
3. **Information Layering**:
   - **Layer 1 (Primary)**: Main diagram flow — geometric nodes + arrows + short labels.
   - **Layer 2 (Secondary)**: Inline arrow annotations, concrete variable values, array indices.
   - **Layer 3 (Tertiary)**: Mini State Table or Legend explaining color codes in corner.

### 1.3. Direct Real-World Problem Scenario Illustration (No 'Cách cũ / Cách mới' Comparison Split)

- 🎯 **Direct Scenario Illustration**: Section 1 image MUST illustrate the **concrete real-world business problem scenario directly** (e.g., E-commerce Order Checkout Rules Engine, Student Qualification Flow, User Credit Check).
- ⛔ **FORBIDDEN FORMULAIC COMPARISON SPLITS**: ABSOLUTELY FORBIDDEN to create artificial formulaic 'Cách cũ' vs 'Cách mới' comparison boxes or split panels.
- 🇻🇳 **Mandatory Preference**: Panel text, labels, and status badges MUST be in **concise, accented Vietnamese** so students immediately understand the pedagogical message.
  - GOOD Examples: `Luồng xử lý chiết khấu đơn hàng Shopee`, `Quy trình kiểm tra điều kiện qua môn`, `Cơ chế xác thực tài khoản VIP`.
  - BAD Examples: `Cách cũ vs Cách mới` (Formulaic comparison), `Flowchart diagram` (Abstract English).
- 📌 *Note*: Programming keywords and tech stack names (`if`, `else`, `for`, `while`, `range()`, `FastAPI`, `PostgreSQL`) remain in standard lowercase English.

### 1.4. Strict Text Emoji Prohibition Directive (Vector/SVG Icons Only)

- ⛔ **ABSOLUTELY FORBIDDEN TEXT EMOJIS**: 100% forbidden to render text emojis (❌, ✅, ⚠️, 🔴, 🟢, ▶, 📌, ⚡, 🚀, 💡).
- ✅ **CLEAN 2D FLAT VECTOR / SVG ICONS ONLY**: Use clean vector icons (e.g. `clean flat checkmark symbol`, `subtle warning triangle icon`, `minimalist database cylinder icon`).
- Prompt keyword: `Strictly NO text emojis (never use emoji characters like ❌, ✅, ⚠️, 🔴, 🟢, ▶). Only use clean 2D flat vector icons, symbols, and Phosphor-style vector graphics.`

### 1.5. 4 Advanced AI Error Reduction Directives

1. 🚫 **NO DUPLICATE BADGES**:
   - Status badges (Warning box, Success box) MUST appear EXACTLY ONCE at the bottom of their panel.
   - Prompt keyword: `Each status badge must appear EXACTLY ONCE at the bottom of its panel. Never duplicate badges.`
2. 🔢 **SEQUENTIAL NUMBERING INTEGRITY IN CODE**:
   - Loop code examples MUST use logically ascending numbers (`1, 2, 3, 4, 5..., 100`). Never skip or duplicate numbers randomly.
   - Prompt keyword: `Sequential numbers in code examples must follow strict logical sequence (1, 2, 3, 4, 5... 100). Never repeat or skip numbers randomly.`
3. 💻 **IDE-STYLE CODE WINDOW CARDS**:
   - Code snippets MUST be enclosed inside **IDE Code Window Cards** (with 3 window dots at top-left: red, yellow, green) using monospace font.
   - Prompt keyword: `Enclose code snippets inside a clean IDE editor window card with 3 subtle window dots at top left. Use crisp monospace font for code text.`
4. 📐 **CROPPED TIGHT EDGE-TO-EDGE CANVAS FILLING (ZERO BLANK BACKGROUND MARGINS)**:
   - Visual illustration elements MUST stretch and fill 100% edge-to-edge across the entire image canvas horizontally and vertically.
   - ABSOLUTELY FORBIDDEN giant empty white background borders, top/bottom/left/right padding spaces, or small graphics floating in a large white void.
   - Prompt keyword: `Cropped tight, edge-to-edge 2D flat vector technical illustration filling 100% of the image canvas with NO blank white outer margins, NO top or bottom empty borders. Visual elements span edge-to-edge across the full image area.`

### 1.6. Mandatory 16:9 Widescreen Aspect Ratio
MUST use `16:9 aspect ratio` matching `reading.html` `max-w-4xl` image containers and Marp slide decks.

### 1.7. Top-to-Bottom Vertical Flow Priority
- Default: `top-to-bottom vertical flowchart layout`.
- Exception: Use `left-to-right horizontal layout` only for wide 3-tier architecture diagrams or complex >6 step flows.

### 1.8. Standard Diagram Geometry
- 🔷 **Diamond**: Decision nodes (`if age >= 18`).
- ▭ **Rectangle**: Process blocks (`user_count = 10`).
- ▱ **Parallelogram**: I/O operations (`print(result)`).
- 🛢️ **Cylinder**: Database / Storage nodes.
- 🧱 **Grid Cells**: Stack frame / Heap memory representation.
- ⬭ **Oval**: Start / End terminators (`Bắt đầu` / `Kết thúc`).

### 1.9. Connectors & Arrow Rules
- **Solid Lines**: Main control execution flow.
- **Dashed Lines**: Auxiliary data flow or secondary branch.

### 1.10. Case-Sensitive Syntax Integrity
Code keywords (`if`, `else`, `elif`, `for`, `while`, `print()`, `def`, `return`) MUST preserve original lowercase syntax. FORBIDDEN uppercase (`IF`, `Else`).

### 1.11. Ultra-Concise Minimal Labels (1 to 3 Words)
- ⛔ FORBIDDEN long Vietnamese sentences inside geometric nodes.
- ✅ MUST use concise 1-3 word labels or short expressions (`if age >= 18`, `True`, `False`, `Bắt đầu`, `Kết thúc`).

### 1.12. Clean Typography & High Contrast
Sans-serif typography (`clean sans-serif typography`), dark text (`#0f172a`, `#334155`) on light background (`#ffffff`, `#f8fafc`).

### 1.13. Muted Corporate Color Palette
Corporate Navy `#0f172a`, Slate Gray `#334155`, Soft Emerald `#10b981`, Teal `#0d9488`, Rose Red `#f43f5e`, Warm Gray `#f8fafc`.

### 1.14. FORBIDDEN 3D/NEON AI KEYWORDS
⛔ FORBIDDEN: `3D`, `isometric factory`, `glowing neon`, `cyberpunk`, `futuristic`, `sci-fi`, `hyper-realistic rendering`.

### 1.15. STRICT NO ALL CAPS DIRECTIVE
⛔ FORBIDDEN: ALL CAPS text labels (`RAW INPUT STREAM`, `ERROR LOG`). Use **Sentence case** or **Title case**.

---

## 2. Master Image Prompt Blueprint Formula

Every generated English image prompt MUST strictly follow this blueprint formula:

```text
*Prompt tạo ảnh: A clean 2D flat vector technical illustration of [Detailed logic/business workflow description here]. Main title in meaningful concise Vietnamese (e.g. 'Cách cũ: Viết thủ công 100 dòng vs Cách mới: Vòng lặp for 2 dòng'). Strictly NO text emojis (never use emoji characters like ❌, ✅, ⚠️, 🔴, 🟢, ▶). Only use clean 2D flat vector icons, symbols, and Phosphor-style vector graphics. 16:9 aspect ratio, spacious layout with at least 32px safe outer margin on all sides. Code snippets enclosed inside clean IDE editor window cards with 3 window dots at top left, using crisp monospace font. Sequential numbers in code examples follow strict logical sequence (1, 2, 3, 4, 5... 100). Each status badge appears EXACTLY ONCE at the bottom of its panel (never duplicate badges). Rich in technical detail: concrete data values in nodes, color-coded zones, active element highlighted with bold border, inline micro-annotations on arrows. Standard diagram geometry: diamond shapes for decision nodes, rectangles for process blocks, cylinders for databases, rounded ovals for start/end. Solid lines for main control flow, dashed lines for auxiliary data flow. Ultra-concise minimal 1-3 word labels ('Bắt đầu', 'if age >= 18', 'Đúng', 'Sai', 'if block', 'else block', 'Kết thúc'). Exact syntax case-sensitive code keywords ('if', 'else', 'for', 'range()'). Minimalist infographics style, clean white background, muted corporate color palette (navy blue, slate gray, soft emerald for True path, subtle rose red for False path). Clean sans-serif font, no 3D elements, no glowing neon effects. All labels in Sentence Case or Title Case (NEVER ALL CAPS).*
```

---

## 3. Good vs Bad Image Prompt Reference

| Criterion | BAD Prompt (REJECTED) ❌ | GOOD Prompt (APPROVED) ✅ |
| :--- | :--- | :--- |
| **Icons & Emojis** | Embeds text emojis (`❌`, `✅`, `⚠️`, `▶`) making images look unprofessional | **100% TEXT EMOJI PROHIBITED**. Use **2D Vector Icons / SVG Symbols** (`clean flat vector checkmark icon`, `warning triangle symbol`) |
| **Status Badges** | Duplicates same badge 2-3 times across panel | Each status badge appears **EXACTLY ONCE** at panel bottom |
| **Sequential Code Numbers** | Random out-of-order sequence (`1, 2, 3... 10, 10, 17`) | Ascending sequential numbers (`1, 2, 3, 4, 5... 100`) |
| **Code Display** | Plain text floating over shapes | Code enclosed inside **IDE Editor Window Cards** (Monospace font + 3 dots) |
| **Outer Margins** | Text clipped at image edges | **Safe outer margin at least 32px** on all sides |
| **Main Image Title** | Abstract English title | **Meaningful concise Accented Vietnamese title** (`Cách cũ: Viết thủ công 100 dòng vs Cách mới: Vòng lặp for 2 dòng`) |
| **Detail Level** | Shallow with 3 empty boxes | Rich detail: concrete values (`[72, 85, 91]`), variable state tables, color-coded zones |
| **Aspect Ratio** | Square (1:1) or Vertical (9:16) | **16:9 Widescreen aspect ratio** (`16:9 aspect ratio`) |
| **Code Syntax** | `IF`, `Else`, `PRINT("Lỗi")` | 100% exact syntax: `if`, `else`, `print()`, `user_input` |
| **Visual Style & Text Case** | 3D neon, ALL CAPS labels | 2D flat, muted corporate colors, Sentence Case / Title Case labels |

---

## 4. Image Prompt Quality Gate Checklist

Every image prompt MUST pass all 12 quality criteria:

1. `[ ]` Strictly NO text emojis (❌, ✅, ⚠️, ▶); vector icons/SVG symbols ONLY.
2. `[ ]` Main title in meaningful concise Accented Vietnamese.
3. `[ ]` Code snippets enclosed in IDE Editor Window Cards with monospace font.
4. `[ ]` Each status badge appears EXACTLY ONCE at bottom.
5. `[ ]` Sequential numbers in code examples follow strict logical sequence (1, 2, 3, 4, 5... 100).
6. `[ ]` Safe outer margin of at least 32px.
7. `[ ]` Style: `clean 2D flat vector technical illustration / minimalist infographics`.
8. `[ ]` Aspect ratio: `16:9 aspect ratio`.
9. `[ ]` Rich technical detail: concrete values, color-coded zones, inline arrow annotations.
10. `[ ]` NO 3D or glowing neon effects (`no 3D`, `no glowing neon`).
11. `[ ]` Strictly NO ALL CAPS (`NEVER ALL CAPS` / `Sentence Case`).
12. `[ ]` Exact case-sensitive syntax code keywords (`if`, `else`, `range()`, `print()`).

