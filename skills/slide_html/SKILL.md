---
name: slide_html
description: Build the in-class lecture slides (slides.html, "Bai giang tren lop") for a session from the finished lesson readings, on the approved Rikkei light frame, and verify that every slide fits the screen. Use for any request to create or fix slides.html, projected lecture slides, or interactive class slides. Not for slide.pptx (use slide_deck) and not for dashboards. Output language is 100% accented Vietnamese.
---

# Slide HTML Skill (slides.html) — Rikkei Education

## 0. Rules that override your defaults

1. **Start from the approved frame.** Copy `reference/slides_frame.html` and replace only the slide sections and the `{{...}}` placeholders. Do not write a new page, do not restyle the frame, do not invent a new look.
2. **Flat light style only.** White and slate surfaces, Rikkei red `#be111c` for chips, buttons and headings. Forbidden: glass or blur effects (`backdrop-filter`, `glass-card`), gradients, neon, pulsing or bouncing animation, colored decorative icons, emoji, dark page backgrounds, ALL CAPS badges. A short fade between slides is the only animation.
3. **It is a slide deck, not a dashboard.** One idea per slide, big text, nothing to scroll. Never use the `classroom_lecture_generator` dashboard layout for slides.
4. **Every slide must fit the screen without scrolling** at 1366x768 and 1920x1080 (and stay within a few pixels at 1280x720). This is the most common defect; the checker measures it.
5. **Content comes from the finished readings.** Same names, data, messages and code as the readings; every number shown by a simulation comes from a real run, never from your head. Use only concepts taught up to the lesson.
6. **Do not report done** until `check_slides_html.py` reports 0 errors **and** you have looked at the screenshots.

## 1. Inputs

Session title, the list of lessons with their finished readings, the output folder (`.../Bai giang tren lop/`), the course technology and the running business scenario of the readings. If the readings are not finished, stop: write the slides after the readings.

## 2. Procedure

1. Read every reading. Outline the deck as a table: slide number, lesson, purpose, left panel, right panel.
2. Copy `reference/slides_frame.html` to `<session folder>/Bai giang tren lop/slides.html`. Set the `<title>`; replace the example slides. The navigation script counts slides itself.
3. Write the slides with the recipes in section 3. Put simulation code in the final `<script>` block, one function group per slide with the slide id as prefix (`s4Next`, `s4Reset`).
4. Check and take screenshots:
   ```bash
   python skills/slide_html/scripts/check_slides_html.py "<...>/slides.html" --shots "<scratch>/shots"
   ```
5. View every `sheet_N.png`. Fix, and repeat step 4. At most 3 rounds; report what remains honestly.

## 3. Deck structure and recipes

- **Size.** 15-20 slides per session (`AGENTS.md`). A session with several lessons may need more (about 4 per lesson plus cover and summary); say why in the final report.
- **Slide 1:** cover with the session tag and a contents map; every row is a `map-row` button that jumps to the first slide of that lesson.
- **Per lesson:** a concept slide, a worked example slide with a simulation, one "Lỗi thường gặp" slide with a quiz, and a recap in the last lesson slide.
- **Last slides:** summary (3-6 key points, flat numbered list, same layout as the contents) then closing.
- **Two-column layout.** Left card (2/5 width): 3 numbered points, each under 30 words. Right column (3/5): code and simulation.
- **Code and simulation share one column** through the two tabs `Mã nguồn` / `Mô phỏng` (function `paneTab`, see the frame). Never stack both: the slide would not fit.
- **Text rules.** At most 3 main points per slide (3-30-300 rule: 3 points, 30 words each), body text at least 18px and labels at least 16px (the frame already sets this), code at most 12 lines.
- **Headings.** Short title in `h2.h-title`; one sentence in `p.h-sub` stating what the learner must take away.
- **Status line.** Each interactive slide has a `.status` line at the bottom telling the learner what to try; update it with `setMsg`.
- **Simulations.** Plain JavaScript in the page; no new libraries beyond what the frame loads. Every simulation needs at least one control the learner can operate (buttons, select, input) and must show the result it produces. Precompute tables from real runs and embed them as data.
- **Quizzes.** Answer options of equal length and style, one correct answer, feedback shown in the status line. Do not point at other materials ("theo bài đọc").

## 4. Language rules

Accented Vietnamese, English technical terms and identifiers. No emoji or pictograms, no `[NOTE]` tags, no `<a href="#">`, no ALL CAPS, no words: nhé, bẫy lập trình, thần thánh, bí kíp, tất tần tật, thân mến, thực chiến, gotcha, anti-pattern, khám phá, tuyệt vời. Icons: only the Phosphor glyphs already used in the frame, neutral and not for decoration.

## 5. What the checker does and does not do

It measures, for every slide at 1366x768, 1920x1080 and 1280x720: vertical overflow in the default state and after clicking each button (up to 15 per slide), horizontal overflow, console errors; and scans for leftover `{{...}}`, `href="#"`, glass/gradient/blur tokens, emoji, banned words, text smaller than 15px. It does not judge whether the content is correct or the slide looks good; that is your review of the screenshots. If Playwright or Chrome is missing, tell the user and do not claim the slides were verified.

Before reporting the deck done, run the verification gate: `python -m core.harness verify <slides.html> --kind slide_html --runtime` (exit 0 required; exit 2 means a tool was missing, so name it and do not claim verified).

## 6. Reference files

- `reference/slides_frame.html` — the approved frame (head, styles, header, navigation, tabs, helpers) with two example slides.
