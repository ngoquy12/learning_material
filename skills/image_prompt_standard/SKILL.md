---
name: image_prompt_standard
description: Standard for writing image generation prompts (Imagen, DALL-E, Stable Diffusion) for Rikkei learning materials: clean 2D flat vector infographics in 16:9, left-to-right flow, concrete values, accented Vietnamese labels, no text banner, no code blocks, no emoji, no 3D or neon. The prompt is returned as one line `*Prompt tạo ảnh: ...*`. Used for the hero illustration of readings and for diagrams in other materials.
---

# Image Prompt Standard — Rikkei Education

## 1. Output contract

- The prompt is ONE block of English text. Where it is embedded in Markdown (mindmaps, requirement documents, lab and exercise text), wrap it exactly as `*Prompt tạo ảnh: <prompt>*` (one leading asterisk, the prefix, the prompt, one closing asterisk): parsers in the pipeline find the prompt by this pattern, so do not change the prefix, add line breaks inside, or use asterisks inside the prompt. Where it is a JSON field such as `image_prompt` (readings), return only the plain prompt text, with no wrapper, because the field is sent to the image service as is.
- The prompt is in English. Every label that must appear inside the image is quoted in accented Vietnamese.
- One image per prompt.

## 2. What the image must be

1. **A clean 2D flat vector technical illustration**, minimalist but concrete: 3 to 6 nodes or objects, no decoration.
2. **Understood in 3 seconds.** A beginner sees the business problem at once. Use friendly flat objects of the session's business domain (for example a receipt, a truck, a user card, a database cylinder), not abstract machinery.
3. **Concrete values, never placeholders.** Nodes carry real data tied to the scenario: `Đơn hàng 1.500.000 VNĐ`, `tồn kho = 25`, `if total >= 500000`, array `[72, 85, 91]`; never `data`, `value`, `item`, `x`.
4. **Left-to-right horizontal flow** (input, decision or process, outcome), always in 16:9 landscape.
5. **Color-coded zones** with a muted corporate palette: navy `#0f172a`, slate `#334155`, soft emerald `#10b981` for the true or success path, rose `#f43f5e` for the false or error path, teal `#0d9488` as a secondary accent, warm gray `#f8fafc` background.
6. **Standard shapes:** diamond for a decision, rectangle for a process step, parallelogram for input or output, cylinder for a database or storage, oval for start and end. Solid arrows for the main flow, dashed arrows for the auxiliary flow. Short annotations on arrows only when they carry a state change (`i = 0`, `i++`).
7. **Labels:** 1 to 3 words, accented Vietnamese (`Đầu vào đơn hàng`, `Đúng`, `Sai`, `Bắt đầu`, `Kết thúc`). Technical terms, identifiers and code expressions stay in standard English and exact case (`if`, `else`, `range()`, `print()`, `API`, `SQL`). Never mix Vietnamese and English jargon in one label.
8. **Text style:** clean sans-serif, dark text (`#0f172a` or `#334155`) on light backgrounds, Sentence case or Title case.
9. **Layout:** 16:9, the artwork fills the canvas edge to edge with a safe inner margin of about 32 px so no text is clipped; no large empty white borders.
10. **Counters and badges:** numbers in a sequence ascend strictly (1, 2, 3, 4, 5); each status badge (warning, success) appears exactly once at the bottom of its panel.

## 3. Forbidden

- Emoji or pictograms drawn as text characters; use flat vector icons and symbols only.
- A title banner or heading baked into the image (the page already has the heading and caption).
- Code blocks, listings or IDE window cards inside the image: generated code text is full of spelling errors. Code appears only as short expressions inside nodes (about 20 characters at most).
- 3D, isometric, glowing neon, cyberpunk, futuristic or photorealistic rendering; gradients and drop shadows used as decoration.
- ALL CAPS labels, giant text, long sentences inside shapes, abstract gears or circuit-board lines, side-by-side "old way versus new way" boxes unless the lesson is explicitly a comparison.
- Duplicate badges, skipped or repeated numbers, uppercase code keywords (`IF`, `Else`).

## 4. Blueprint formula

```text
*Prompt tạo ảnh: A clean 2D flat vector technical illustration of [the business scenario and flow with concrete values, left to right]. Wide horizontal 16:9 landscape, left-to-right flow, artwork filling the canvas with a safe inner margin of about 32px. No title banner, no code blocks, no text emojis (use clean flat vector icons only). All labels in accented Vietnamese ('Đầu vào đơn hàng', 'Đúng', 'Sai'), 1 to 3 words each; technical terms and code expressions in English with exact case ('if total >= 500000'). Standard shapes: diamond for decision, rectangle for process, parallelogram for input/output, cylinder for database, oval for start/end; solid arrows for the main flow, dashed for auxiliary. Muted corporate palette: navy, slate gray, soft emerald for the true path, rose red for the false path, warm gray background. Clean sans-serif, Sentence case, never ALL CAPS. No 3D, no glowing neon, no gradients.*
```

## 5. Good versus bad

| Aspect | Bad | Good |
|---|---|---|
| Title | Giant heading across the top of the image | No banner; the page supplies the heading |
| Language | `INPUT ORDER`, `NET TOTAL` | `Đầu vào đơn hàng`, `Tổng thanh toán` |
| Values | `data`, `x = 5`, `if condition` | `Đơn hàng 150.000 VNĐ`, `if total > 500000` |
| Code | A multi-line listing inside the picture | Short expression in a node |
| Icons | Emoji characters | Flat vector icons |
| Style | 3D neon, ALL CAPS labels | 2D flat, muted palette, Sentence case |
| Format | Square or vertical | 16:9, left to right |
| Badges | Same badge repeated | Each badge once |

## 6. Checklist before returning the prompt

1. English, single block; wrapped as `*Prompt tạo ảnh: ...*` in Markdown, plain text in a JSON field.
2. 16:9, left-to-right, 3 to 6 nodes, concrete values.
3. No title banner, no code blocks, no emoji, no 3D or neon, no ALL CAPS.
4. Vietnamese labels of 1 to 3 words; code expressions in exact English case.
5. Palette, shapes and arrows as in section 2; numbers ascending; each badge once.
6. After the image is generated, look at it: wrong spelling, clipped text or duplicated elements mean the prompt must be fixed and the image regenerated.
