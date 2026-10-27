# Slide types and JSON fields

Every slide has `"id"`, `"type"` and `"notes"`. Items in lists are either a plain string or `{"text": "...", "bold": true, "bullet": true}`.

| type | Fields | Use for |
|---|---|---|
| `cover` | `session_tag` ("Session 01"), `title`, `course_name` | slide 1 only |
| `agenda` | `items` (["1. ...", "2. ..."], at most 7) | slide 2 only |
| `objectives` | `h1` ("Mục tiêu bài học"), `goals` (at most 5) | slide 3 only |
| `code_right_card` | `h1`, `h2`, `code_title`, `code_snippet`, `lang_tag` ("JS", "SQL", "Bash"), `card_title`, `card_items` | one code example with notes beside it |
| `code_trace_table` | `h1`, `h2`, `code_title`, `code_snippet`, `lang_tag`, `table_headers`, `table_rows`, `col_widths` | state changing step by step |
| `comparison_2col` | `h1`, `h2`, `left_title`, `left_code`, `left_items`, `right_title`, `right_code`, `right_items` | A versus B (left card red, right card green) |
| `grid2x2` | `h1`, `h2`, `items` [{`title`, `desc`, `example` (optional)}] x4 | four parallel concepts |
| `flowchart` | `h1`, `h2`, `nodes` [{`type`: start / process / decision / io / end, `text`}] | process with branching; one start, at least one end |
| `timeline` | `h1`, `h2`, `milestones` [{`label`, `desc`}] | stages over time; keep `desc` under 30 characters |
| `interactive` | `pattern` (`predict_outcome` / `find_the_bug` / `quick_quiz`), `h1`, `h2`, `prompt`, `code_snippet` (optional), `lang_tag`, `options` (no "A." prefix), `answer` | in-class check; answer only in notes |
| `glossary_table` | `h1` ("Thuật ngữ cần nhớ"), `h2`, `headers`, `rows`, `col_widths` | 6 or more new terms |
| `exercises` | `h1`, `h2`, `exercises` (3 x 95 chars), `references` (3 x 95 chars) | third from last |
| `summary_2col` | `h1` ("Tổng kết"), `h2`, `left_title`, `left_items`, `right_title`, `right_items` | second from last |
| `closing` | `title`, `subtitle` (optional) | last slide |

Colors, fonts and card shapes are not fields: they come from the template. The `h1` of content slides is red and `h2` is black by template design.

`notes` on every slide: 3-5 sentences ending with the duration, for example `"... [~3 phút]"`. For `interactive`, the `answer` is appended to the notes automatically.
