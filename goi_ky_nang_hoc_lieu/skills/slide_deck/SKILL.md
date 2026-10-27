---
name: slide_deck
description: Build the lecture slide deck file (slide.pptx, "Slide bai giang") for a session. The agent writes ONLY a slides.json of content; the project's deck builder applies the Rikkei template, and two scripts lint the data and measure/render the result. Use for any request to create or fix a PowerPoint lecture deck from lesson readings. Not for slides.html (use slide_html). Output language is 100% accented Vietnamese.
---

# Slide Deck Skill (.pptx) — Rikkei Education

## 0. Rules that override your defaults

1. **You do not design.** Colors, fonts, layouts, card shapes, code-block colors and logos come from `templates/pptx/SLIDE TEMPLATE.pptx` through `core/renderers/pptx/deck_engine.py`. Never choose a palette. Never add gradients, shadows, glass or blur effects, colored icons, emoji, accent bars, single-side borders, centered paragraphs, extra decorative shapes or your own layouts.
2. **You write data, not slides.** Your only creative output is `slides.json`. Do not generate the file with python-pptx `add_slide`, another library, or hand-written XML.
3. **Do not report done until** the checker reports 0 errors **and** you have looked at the rendered contact sheets (`sheet_N.png`) yourself. A passing script does not prove the slides look right.
4. **Content comes from the lesson readings.** Do not invent facts, code, numbers or examples. Use only concepts taught up to the current lesson (`allowed_scope`); never introduce a later concept.

## 1. Inputs

Session title, course name, session number, the finished `reading.md`/`reading.html` of every lesson in the session, and the output folder (`.../Slide bai giang/`). If something is missing, ask before writing.

## 2. Procedure

1. Read every lesson reading. List the deck outline first: for each slide, its `type`, h1 and h2.
2. Write `slides.json` (`{"slides": [...]}`) following `reference/slide_types.md`. Start from `reference/example_slides.json`.
3. Build (this also lints the data and stops on errors):
   ```bash
   python skills/slide_deck/scripts/build_deck.py slides.json "<session folder>/Slide bai giang/slide.pptx"
   ```
4. Check and render:
   ```bash
   python skills/slide_deck/scripts/check_deck.py "<...>/slide.pptx" --json slides.json --render
   ```
   It prints errors/warnings and writes `slide_anh/sheet_N.png` (6 slides per image).
5. View every sheet. Fix the JSON (not the pptx) and repeat from step 3. At most 3 rounds; report remaining warnings to the user honestly.
6. Deliver only `slide.pptx` in the session folder; keep `slides.json` and the image folder in scratch space.

Do not run the project pipeline `main.py` to make slides when working as an IDE agent; this skill replaces it.

## 3. Mandatory deck structure (14 to 18 slides)

| Position | type | Notes |
|---|---|---|
| 1 | `cover` | session tag, session title, course name; nothing else |
| 2 | `agenda` | numbered `1.`, `2.`; at most 7 items |
| 3 | `objectives` | 4-5 goals, each starts with a measurable verb (Giải thích được, Viết được, Phân biệt được...), no CLO codes |
| 4... | content | mix of `code_right_card`, `code_trace_table`, `comparison_2col`, `grid2x2`, `flowchart`, `timeline`, `interactive` |
| n-3 | `glossary_table` | only when 6 or more new terms |
| n-2 | `exercises` | before the summary, never merged into it |
| n-1 | `summary_2col` | key rules only |
| n | `closing` | |

Choose the type by the nature of the content: process or branching → `flowchart`; stages over time → `timeline`; A versus B → `comparison_2col`; state changing step by step → `code_trace_table`; one code example with explanation → `code_right_card`; four parallel concepts → `grid2x2`. Do not repeat the same type for every slide.

## 4. Writing rules

- **Headings.** `h1` = part number and name, with `— n/m` when a part spans several slides (`"4. Kết nối mysql2 — 1/2"`), under 60 characters. `h2` = ONE full declarative sentence that states what the learner must take away (the assertion), under 100 characters, unique in the whole deck. A topic label ("Khái niệm và đặc điểm") is wrong as h2.
- **Density.** At most 4-5 items per slide, short phrases rather than sentences (about 30 words at most per item). The explanation belongs in `notes`, not on the slide.
- **Notes.** 3-5 sentences on every slide: transition, key point to say aloud, a real-life analogy, a question for the class; end with the time, `[~N phút]`. Do not repeat the slide text.
- **Active learning.** After every 3 content slides, insert one `interactive` slide (`predict_outcome`, `find_the_bug` or `quick_quiz`). The answer goes in the `answer` field; the builder puts it in the notes and never prints it on the slide.
- **One running example.** Reuse the business scenario and data of the readings throughout the deck.
- **Code.** At most 12 lines and about 45 characters per line, taken from the readings and correct as written. Identifiers in English; keep comments short.
- **Language.** Accented Vietnamese. No emoji, no square-bracket tags such as `[NOTE]`, no ALL CAPS, no phrases that point at other materials ("trong slide trước", "theo bài đọc"). Banned words: nhé, bẫy lập trình, thần thánh, bí kíp, tất tần tật, thân mến, thực chiến, gotcha, anti-pattern, khám phá, tuyệt vời.

## 5. Builder limits (do not fight them)

The builder keeps a fixed layout and silently cuts text beyond these limits; the linter treats each of them as an error so nothing is lost without notice.

| Field | Limit |
|---|---|
| `card_items`, `left_items`, `right_items` | 5 items, 150 characters each |
| `exercises`, `references` | 3 items, 95 characters each |
| `goals` | 5 |
| `grid2x2.items` | 4 |
| `flowchart.nodes` | 7 |
| `timeline.milestones` | 6 |
| `comparison_2col` code | 5 lines per side |
| code blocks | 12 lines |
| table rows (`code_trace_table`, `glossary_table`) | 8 |

Fixed sizes of the engine (14-18 pt for body text, 14 pt code) are intentional. If text does not fit, cut words or split the slide; never shrink fonts.

## 6. What the scripts check

- `deck_lint.py` (run by `build_deck.py`): slide order and count, unique h2, missing notes, items beyond builder limits, emoji, banned words, bracket tags, interactive cadence.
- `check_deck.py`: on the built file, emoji, banned words, ALL CAPS, font size, shapes beyond the slide, notes present. With `--render` on Windows with PowerPoint: measured text overflow, text touching the footer zone, overlapping text, and PNG export plus contact sheets. Without PowerPoint it only estimates and prints a warning: then you must render the slides with another tool and view them.
- They do **not** judge whether the content is correct or the layout is pleasant. That is your visual review.
- Before reporting the deck done, run the verification gate: `python -m core.harness verify <deck.pptx> --kind slide_pptx` (add `--render` on Windows with PowerPoint; exit 0 required; exit 2 means a tool was missing, so name it and do not claim verified).

## 7. Reference files

- `reference/slide_types.md` — JSON fields of every slide type.
- `reference/example_slides.json` — a complete 15-slide deck that passes the checks.
