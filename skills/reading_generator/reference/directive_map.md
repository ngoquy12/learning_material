# Directive map and enforcement status

The previous version of this skill listed 25 numbered directives. This table maps each old number to the rule that now holds it, so existing references ("Directive 12", "Directive 16") can be resolved. The full old text is archived at `docs/archive/reading_generator_SKILL_before_rewrite_2026-10-27.md`.

| Old # | Old name (short) | Now |
|---|---|---|
| 1 | Fixed 5-section architecture | R1 |
| 2 | 15-minute micro-learning | R2 |
| 3 | Conversational storytelling for Section 1 | R6 |
| 4 | 2D flat vector image, no manual SVG | R18 (hero image or 16:9 SVG; Sections 2-4 inline SVG or Mermaid) |
| 5 | Plain developer language, banned jargon | R14 |
| 6 | English identifiers | R13 (language convention, not always snake_case) |
| 7 | Progressive syntax sandbox per sub-section | R7, R11 |
| 8 | Human-like quality, domain agnostic | R13, R14, R11 |
| 9 | JSON payload and Jinja2 template | pipeline detail; for hand-written readings copy the approved frame (section 0) |
| 10 | Domain-adaptive component registry | R11 |
| 11 | Requirement box and single scenario | R8, R3 |
| 12 | Vietnamese code comments | R13 |
| 13 | Step visualizer UX | section 2 blueprint 2.4, `reference/html_snippets.md` section 6 (light panel, icons instead of emoji) |
| 14 | Dark terminal output | R16 |
| 15 | Minimal italics | R15 |
| 16 | Strict domain isolation, no hardcoded fallback | R11, section 0.4 |
| 17 | 100% live executable sandboxes | R11 (only where an engine exists) |
| 18 | Syntax, breakdown, example order | R7 |
| 19 | Vietnamese technical terminology | R14 |
| 20 | Clean sub-headings, no prefix fluff | R8 |
| 21 | 2D flat vector infographics | R18 |
| 22 | Single unified scenario | R3 |
| 23 | Banned AI buzzwords | R14 |
| 24 | Progressive difficulty | R4 |
| 25 | Session-wide domain persistence | R3 |

## What the code really enforces

As listed by the repository at the time of writing. Verify in the named files before relying on a row.

| Rule | Enforced by |
|---|---|
| Five section ids `section-1` to `section-5`; Section 3 has a code block and at least 3 `h3` | `core/validators/reading_validator.py` |
| Emoji ban | `check_forbidden_emojis` in `agents/reviewer_agents.py`, called by the reading validator |
| Banned buzzwords | `reading_validator.py` (list) and `html_sanitizer.py` (`strip_ai_cliches_from_title`, `FORBIDDEN_AI_CLICHES`) |
| Word budget 1,500-2,000 (reject above about 2,400 or below about 750) | `reading_validator.py` when `metadata["enforce_word_budget"]` is true; constants in `core/reading_budget.py` |
| Requirement box above a sandbox | `reading_validator.py` (looks for "Yêu cầu bài toán" or the sky box classes) |
| Pyodide compatibility of Python code | `core/validators/syntax_linter.py`, only for Python courses |
| Orientation lesson has no sandbox | `reading_validator.py` |
| Non-code subjects have no source code | `reading_validator.py` |
| "Section 2.4" simulator marker | `core/validators/visual_linter.py` (regex for `sec-2-4`, "mô phỏng cơ chế vận hành", `viz-line-`, `mech-line-`) |
| Unknown `tech_stack` raises instead of defaulting to Python | `resolve_domain_engine()` in `core/renderers/reading_renderer.py` |
| Runtime script isolation per stack | `templates/html/reading_master.html.j2` |
| Images stripped from Sections 2-4, inline SVG syntax guard | `_strip_stray_images()`, `_guard_inline_svgs()` in `agents/creators/reading_creator.py` |
| Italic ban and per-block sandbox decision | `convert_inline_markdown()`, `sanitize_html_tags_and_italics()`, `convert_code_to_live_sandbox()` |

Everything not in this table is guidance, not a gate: treat it as best effort and check it yourself.

## Known inconsistencies in the code (for maintainers)

- `core/pm_validators/quality_gates.py` Gate 1 looks for the legacy anchors (`problem-intro`, `data-structure`, `interactive-demo`, `summary-notes`, `self-test`) and tolerates up to two missing, while `reading_validator.py` and the templates use `section-1` to `section-5`. The two should agree on one set.
- The "Section 2.4" regex in `visual_linter.py` fails readings that place the simulator at the end of Section 3 (the ReactJS and NodeJS variant); either accept both placements in the linter or keep that variant out of the validator.
- The Pyodide compatibility check is skipped for non-Python stacks, but its stack list is a hand-written keyword list; a new stack must be added there.
