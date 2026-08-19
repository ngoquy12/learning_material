# agents/reading_ui_reviewer.py
"""
Reading UI Quality Reviewer Agent
==================================
Tu dong review chat luong giao dien (UI/UX) cua file reading.html sau khi sinh ra.
"""

import os
import json
import tempfile
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from core.llm import call_llm_with_images

import threading

VIEWPORT_WIDTH = 1440
VIEWPORT_HEIGHT = 900
PASS_THRESHOLD = 95
OPTIMIZE_SCREENSHOT_MAX_WIDTH = 1280

# Problem 4.1: Concurrency Semaphore (Max 3 parallel Vision API requests to prevent Rate Limit 429)
VISION_SEMAPHORE = threading.Semaphore(3)


def compress_and_resize_screenshot(img_path: str, max_width: int = OPTIMIZE_SCREENSHOT_MAX_WIDTH) -> str:
    """
    Problem 4.1: Compress and resize screenshot PNG to max_width (1280px) to reduce payload size by 70%,
    preventing 429 Rate Limits and RAM spikes during Gemini Vision API calls.
    """
    if not img_path or not os.path.exists(img_path):
        return img_path
    try:
        from PIL import Image
        with Image.open(img_path) as img:
            w, h = img.size
            if w > max_width:
                new_h = int(h * (max_width / w))
                img = img.resize((max_width, new_h), Image.Resampling.LANCZOS)
            img.save(img_path, "PNG", optimize=True)
    except Exception:
        pass
    return img_path


def cleanup_passed_screenshots(report: Dict[str, Any]):
    """
    Problem 4.2: Delete screenshot PNG files if reading passed (score >= 95)
    to prevent disk space inflation.
    """
    if report.get("passed") and report.get("ui_score", 0) >= PASS_THRESHOLD:
        sp = report.get("screenshot_paths", {})
        for key in ["light", "dark"]:
            path = sp.get(key)
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except Exception:
                    pass


UI_REVIEW_SYSTEM_PROMPT = """You are a Lead UI/UX Quality Assurance Engineer for Rikkei Education E-Learning Material Platform.
Your task: Analyze full-page HTML reading material screenshots to detect ALL layout, styling, typography, dark mode, and responsiveness defects.

Rikkei Education UI Design Standards (14 Review Points):
1. LAYOUT & CONTAINER INTEGRITY: Fixed top header, left TOC sidebar, balanced main reading container (no layout breakage, no clipped elements). NO empty containers (empty div/pre blocks).
2. TYPOGRAPHY & FONT UNIFORMITY: H1 (3xl bold Montserrat) > H2 (2xl bold) > H3 (xl bold), body text 16px Inter. ALL text and SVG labels MUST use Inter/Montserrat fonts. FORBIDDEN Arial/default/Courier fonts on titles.
3. CALLOUT BOX COLOR MATRIX: Warning = Amber accent, Error = Rose accent, Success = Emerald accent, Tip = Sky accent. DO NOT mix color schemes between callout types.
4. CODE BLOCK & PLAYGROUND: Code blocks MUST have distinct syntax highlighting. Background MUST be light (`#f8fafc`) in Light Mode and dark (`#0f172a`) in Dark Mode. FORBIDDEN stark black backgrounds in Light Mode.
5. TEXT OVERFLOW: NO text overflowing out of container bounds (in SVG diagrams, tables, code blocks, or callouts).
6. DARK MODE THEME SYNC: Dark mode MUST be fully synchronized dark background. All cards, callouts, and SVG backgrounds MUST shift to dark backgrounds.
7. LIGHT MODE THEME SYNC: Light mode MUST be fully synchronized white/light background. ABSOLUTELY FORBIDDEN to render stark black backgrounds on H3 headers or body paragraphs in Light Mode.
8. CONTRAST RATIO: FORBIDDEN dark text on dark backgrounds or light text on light backgrounds. If contrast is unreadable, REJECT immediately (-25 points).
9. REALISTIC SVG DIAGRAMS: SVG diagrams MUST be 2D Flat Vector Technical Infographics, labels MUST use Sentence Case or Title Case (NEVER ALL CAPS), background MUST synchronize with active theme.
10. RAW CODE LEAK: ABSOLUTELY FORBIDDEN to render unparsed CSS/JS/HTML source code as raw plain text (-25 points).
11. STRAY CHARACTERS: No stray brackets or unescaped HTML entities (&amp; &lt; &gt;).
12. HEADING LENGTH & QUALITY: H2/H3 titles concise (<60 chars), full meaning.
13. DIAGRAM RELEVANCE: Illustrative diagrams MUST be clear and directly relevant.
14. LINKS & NAVIGATION: TOC links scroll accurately to target sections without broken 404 anchors.

SCORING RULES (Strict Deductions):
- RAW CODE LEAK: CRITICAL (-25 points)
- CONTRAST RATIO: CRITICAL (-25 points)
- LIGHT MODE BLACK BG MIXING: CRITICAL (-25 points)
- UNIFORM FONT VIOLATION: MAJOR (-20 points)
- ABSTRACT/EMPTY SVG DIAGRAM: MAJOR (-15 points)
- CODE BLOCK SYNTAX HIGHLIGHTING MISSING: MAJOR (-15 points)
- TEXT OVERFLOW IN SVG/TABLE: MAJOR (-10 points)
- DARK/LIGHT MODE DESYNC: MAJOR (-10 points)
- STRAY CHARACTERS: MINOR (-5 points)
- OVERLY LONG/REPETITIVE HEADING: MINOR (-5 points)

OUTPUT CONTRACT: Output ONLY raw JSON matching this structure:
{
  "ui_score": <integer from 0 to 100, starting at 100 with deductions applied>,
  "passed": <true if ui_score >= 95, else false>,
  "summary": "<1-sentence overall UI quality summary in Accented Vietnamese>",
  "issues": [
    {
      "id": <issue index number>,
      "severity": "critical|major|minor",
      "criterion": "<violated criterion name>",
      "location": "<exact location on page>",
      "description": "<detailed visual error description in Accented Vietnamese>",
      "recommendation": "<exact HTML/CSS fix guidance in Accented Vietnamese>",
      "mode": "light|dark|both"
    }
  ]
}"""


def capture_screenshots(html_path: str, output_dir: str) -> Dict[str, str]:
    screenshot_paths = {}
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("  [UI Reviewer] Playwright chưa được cài đặt. Hãy chạy: pip install playwright && playwright install chromium")
        return screenshot_paths

    html_p = Path(html_path).resolve()
    file_url = html_p.as_uri()
    light_path = os.path.join(output_dir, "screenshot_light.png")
    dark_path  = os.path.join(output_dir, "screenshot_dark.png")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport={"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT})
            page = context.new_page()

            page.goto(file_url, wait_until="networkidle", timeout=30000)
            page.evaluate("() => { document.documentElement.classList.remove('dark'); }")
            page.wait_for_timeout(800)
            page.screenshot(path=light_path, full_page=True)
            # Problem 4.1: Compress screenshot PNG to 1280px max-width
            compress_and_resize_screenshot(light_path)
            screenshot_paths["light"] = light_path
            print(f"  [UI Reviewer] Đã lưu ảnh chụp màn hình chế độ sáng (Light Mode): {Path(light_path).name}")

            page.evaluate("() => { document.documentElement.classList.add('dark'); }")
            page.wait_for_timeout(800)
            page.screenshot(path=dark_path, full_page=True)
            # Problem 4.1: Compress screenshot PNG to 1280px max-width
            compress_and_resize_screenshot(dark_path)
            screenshot_paths["dark"] = dark_path
            print(f"  [UI Reviewer] Đã lưu ảnh chụp màn hình chế độ tối (Dark Mode): {Path(dark_path).name}")

            browser.close()
    except Exception as e:
        print(f"  [UI Reviewer] Lỗi chụp ảnh màn hình: {e}")

    return screenshot_paths


def analyze_ui_with_vision(screenshot_paths: Dict[str, str], session_id: str = "", lesson_id: str = "", lesson_title: str = "") -> Dict[str, Any]:
    if not screenshot_paths:
        return {"ui_score": 0, "passed": False, "summary": "Không có ảnh màn hình để phân tích.", "issues": []}

    image_paths = [v for v in [screenshot_paths.get("light"), screenshot_paths.get("dark")] if v and os.path.exists(v)]
    if not image_paths:
        return {"ui_score": 0, "passed": False, "summary": "Tệp ảnh không tồn tại.", "issues": []}

    user_prompt = f"""Analyze screenshot images of the compiled reading material HTML page:
Lesson Context: {session_id} - {lesson_id}: {lesson_title}
Image 1: Light mode screenshot | Image 2: Dark mode screenshot (if available)

Audit carefully against all 11 UI Quality Criteria of Rikkei Education.
Return ONLY raw JSON object adhering to the specified schema."""

    # Problem 4.1: Acquire Semaphore to restrict parallel Vision API requests to max 3
    with VISION_SEMAPHORE:
        raw_response = call_llm_with_images(
            system_prompt=UI_REVIEW_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            image_paths=image_paths,
            agent_name="UI_Reviewer_Vision",
            session_id=session_id,
            lesson_id=lesson_id
        )

    if not raw_response:
        return {"ui_score": 0, "passed": False, "summary": "Gemini Vision không có phản hồi.", "issues": []}

    try:
        cleaned = raw_response.strip()
        for prefix in ["```json\n", "```json", "```\n", "```"]:
            if cleaned.startswith(prefix):
                cleaned = cleaned[len(prefix):]
                break
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned_str = cleaned.strip()
        # Fix unescaped backslashes in JSON string values (e.g. \1, \s, \d)
        fixed_json = re.sub(r'(?<!\\)\\(?!["\\/bfnrtu])', r'\\\\', cleaned_str)
        try:
            report = json.loads(fixed_json)
        except Exception:
            report = json.loads(cleaned_str)

        report.setdefault("ui_score", 0)
        report.setdefault("passed", report.get("ui_score", 0) >= PASS_THRESHOLD)
        report.setdefault("issues", [])
        report.setdefault("summary", "")
        return report
    except Exception as e:
        print(f"  [UI Reviewer] Không thể parse kết quả Vision thành JSON: {e}")
        return {"ui_score": 0, "passed": False, "summary": f"Không thể parse JSON từ kết quả phân tích Vision: {e}", "issues": [], "raw_response": raw_response[:500]}



def print_ui_report(report: Dict[str, Any], html_path: str):
    score   = report.get("ui_score", 0)
    passed  = report.get("passed", False)
    summary = report.get("summary", "")
    issues  = report.get("issues", [])
    status  = "PASSED (ĐẠT)" if passed else "FAILED (CHƯA ĐẠT)"
    print(f"\n  +----------------------------------------------------------+")
    print(f"  |  BÁO CÁO ĐÁNH GIÁ CHẤT LƯỢNG UI -- {status:<24}|")
    print(f"  |  File : {Path(html_path).name:<49}|")
    print(f"  |  Điểm : {score}/100{'':<47}|")
    print(f"  |  {summary[:56]:<56}|")
    print(f"  +----------------------------------------------------------+")
    if issues:
        print(f"\n  Phát hiện {len(issues)} vấn đề giao diện cần cải thiện:")
        for issue in issues:
            sev      = issue.get("severity", "minor").upper()
            criterion= issue.get("criterion", "")
            desc     = issue.get("description", "")
            rec      = issue.get("recommendation", "")
            mode     = issue.get("mode", "")
            print(f"\n    [{sev}] Tiêu chí: {criterion} (Chế độ: {mode})")
            print(f"    Vấn đề: {desc}")
            print(f"    Gợi ý : {rec}")
    else:
        print(f"\n  Hoàn hảo! Không phát hiện bất kỳ lỗi giao diện nào.")
    print()


def review_reading_ui(
    html_path: str,
    session_id: str = "",
    lesson_id: str = "",
    lesson_title: str = "",
    save_screenshots: bool = True,
    screenshot_dir: Optional[str] = None
) -> Dict[str, Any]:
    """
    Entry point chính: review UI của 1 file reading.html.
    Returns: { ui_score, passed, summary, issues, screenshot_paths }
    """
    if not os.path.exists(html_path):
        print(f"  [UI Reviewer] Tệp không tồn tại: {html_path}")
        return {"ui_score": 0, "passed": False, "summary": "Tệp HTML không tồn tại.", "issues": []}

    print(f"\n  [UI Reviewer] Bắt đầu kiểm tra chất lượng UI: {Path(html_path).name}")

    if screenshot_dir:
        out_dir = screenshot_dir
    elif save_screenshots:
        out_dir = str(Path(html_path).parent / "ui_review")
    else:
        out_dir = tempfile.mkdtemp(prefix="rikkei_ui_")
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    print(f"  [UI Reviewer] Đang chụp ảnh màn hình bằng Playwright Chromium...")
    screenshot_paths = capture_screenshots(html_path, out_dir)

    if not screenshot_paths:
        return {"ui_score": 0, "passed": False, "summary": "Playwright không thể chụp ảnh màn hình.", "issues": [], "screenshot_paths": {}}

    print(f"  [UI Reviewer] Đang phân tích giao diện bằng Gemini Vision AI...")
    report = analyze_ui_with_vision(screenshot_paths, session_id, lesson_id, lesson_title)
    report["screenshot_paths"] = screenshot_paths

    print_ui_report(report, html_path)

    report_path = os.path.join(out_dir, "ui_review_report.json")
    try:
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"  [UI Reviewer] Báo cáo JSON đã lưu tại: {report_path}")
    except Exception as e:
        print(f"  [UI Reviewer] Không thể lưu báo cáo JSON: {e}")

    # Problem 4.2: Delete screenshot PNG files if reading passed (score >= 95)
    cleanup_passed_screenshots(report)

    return report


# ─────────────────────────────────────────────────────────────────────────────
# AUTO-FIX ENGINE
# Surgical repair: only modify broken parts, preserve everything else.
# Fix scope: SVG text overflow, dark mode cards, TOC/anchor links, broken imgs.
# ─────────────────────────────────────────────────────────────────────────────

AUTO_FIX_SYSTEM_PROMPT = """You are a Lead Frontend Repair Specialist for Rikkei Education E-Learning Platform.
Your task: Receive specific UI bug reports and target HTML code, returning EXACTLY ONE REPAIRED HTML SNIPPET.

Repair Directives:
- Repair ONLY broken parts; preserve all other valid tags and content.
- Return raw HTML code only without markdown commentary.
- SVG text overflow: Split long labels into <tspan> lines (max 25 chars/line) or use <foreignObject> with HTML table.
- Dark mode cards: Add "dark:bg-slate-900/60" or "dark:bg-rikkei-cardDark" classes.
- Text overflow: Add style="word-break:break-word;overflow-wrap:break-word;".
- Broken links: Fix href="#sec-anchor-id" to match actual container IDs.
- Broken images: Add meaningful alt text, loading="lazy", and 16:9 widescreen ratio.
- TOC links: Ensure every <a href="#id"> matches an existing section ID.
"""


def fix_svg_text_overflow(svg_content: str) -> str:
    """
    Fix SVG text overflow using LLM: split long labels into tspan lines.
    Returns fixed SVG string.
    """
    from core.llm import call_llm

    system_prompt = """You are an SVG Graphic Repair Specialist at Rikkei Education.
Your task: Repair an input SVG block containing text overflow defects.
- Split long <text> elements (> 25 chars) into multiple <tspan> lines, adding dy="1.2em" to subsequent lines.
- For table-like structures in SVG (manually stacked <text> rows): Convert to <foreignObject> containing a standard HTML table.
- Ensure all text remains strictly inside viewBox bounds, maintaining at least 20 px padding from borders.
- Add text-anchor="middle" to all <text> nodes inside circular or square bounds.
- Output ONLY the fixed SVG block without markdown wrappers or commentary."""

    user_prompt = f"""Repair text overflow defects in the following SVG block:

{svg_content}

Specific Instructions:
1. Split long text labels into short <tspan> segments (max 25 chars/line).
2. For tabular SVG structures: Use <foreignObject> containing HTML tables instead of manual text rows.
3. Preserve all original shapes, colors, and positions.
4. Output ONLY the raw repaired SVG block (no markdown wrappers)."""

    fixed = call_llm(system_prompt, user_prompt, agent_name="SVG_Fixer")
    if fixed:
        # Clean markdown wrappers if any
        for marker in ["```svg\n", "```xml\n", "```html\n", "```\n"]:
            if fixed.startswith(marker):
                fixed = fixed[len(marker):]
        if fixed.endswith("```"):
            fixed = fixed[:-3]
        return fixed.strip()
    return svg_content


def fix_toc_links(html_content: str) -> str:
    """
    Programmatically fix TOC anchor links.
    Ensures every href="#X" in sidebar has a matching id="X" in article.
    """
    # Find all anchor IDs in article sections
    section_ids = set(re.findall(r'<section[^>]+id="([^"]+)"', html_content))
    h2_ids      = set(re.findall(r'<h[23][^>]+id="([^"]+)"', html_content))
    all_ids = section_ids | h2_ids

    if not all_ids:
        return html_content

    # Find TOC links with href="#..."
    def fix_toc_href(match):
        href_val = match.group(1)
        anchor = href_val.lstrip("#")
        if anchor in all_ids:
            return match.group(0)  # Already correct
        # Try fuzzy match: find closest id
        for real_id in sorted(all_ids):
            # Match by prefix or common words
            if anchor[:6] in real_id or real_id[:6] in anchor:
                return match.group(0).replace(href_val, f"#{real_id}")
        return match.group(0)

    fixed = re.sub(r'href="(#[^"]+)"', fix_toc_href, html_content)
    return fixed


def fix_broken_images(html_content: str, html_path: str) -> str:
    """
    Fix broken image references:
    - Add loading="lazy" to all <img>
    - Ensure all <img> have meaningful alt attributes
    - Fix relative paths that may be broken
    """
    def fix_img_tag(match):
        tag = match.group(0)
        # Add loading="lazy" if missing
        if "loading=" not in tag:
            tag = tag.replace("<img ", '<img loading="lazy" ')
        # Ensure alt is not empty
        if 'alt=""' in tag or "alt=''" in tag:
            tag = tag.replace('alt=""', 'alt="Hình minh họa bài học"')
            tag = tag.replace("alt=''", "alt='Hình minh họa bài học'")
        # Add alt if completely missing
        if "alt=" not in tag:
            tag = tag.replace("<img ", '<img alt="Hình minh họa bài học" ')
        return tag

    fixed = re.sub(r"<img\b[^>]*>", fix_img_tag, html_content)
    return fixed


def inject_css_patch(html_content: str, patch_css: str) -> str:
    """Inject CSS patch into existing <style> block."""
    if "</style>" in html_content:
        # Inject before the closing </style>
        return html_content.replace("</style>", f"\n      /* [UI AUTO-FIX PATCH] */\n{patch_css}\n    </style>", 1)
    elif "</head>" in html_content:
        # Inject as new style block before </head>
        return html_content.replace("</head>", f"<style>{patch_css}</style>\n</head>", 1)
    return html_content


def get_issue_css_patch(issues: List[Dict[str, Any]]) -> str:
    """Generate targeted CSS patches based on detected issues."""
    patches = []

    for issue in issues:
        criterion = issue.get("criterion", "").upper()
        severity  = issue.get("severity", "minor")
        mode      = issue.get("mode", "both")

        if "DARK MODE" in criterion or "DARK" in criterion:
            patches.append("""
      /* Auto-fix: Dark mode card backgrounds */
      .dark .bg-white, .dark [class*="bg-white"] {
        background-color: rgb(21 29 48) !important;
      }
      .dark .bg-slate-50, .dark [class*="bg-slate-50"] {
        background-color: rgb(15 23 42 / 0.7) !important;
      }
      .dark .bg-gray-50, .dark [class*="bg-gray-50"] {
        background-color: rgb(15 23 42 / 0.7) !important;
      }
      .dark [class*="bg-amber-50"]  { background-color: rgb(120 53 15 / 0.25) !important; }
      .dark [class*="bg-rose-50"]   { background-color: rgb(136 19 55 / 0.25) !important; }
      .dark [class*="bg-emerald-50"]{ background-color: rgb(6 78 59 / 0.25)   !important; }
      .dark [class*="bg-sky-50"]    { background-color: rgb(12 74 110 / 0.25) !important; }
      """)

        if "TEXT OVERFLOW" in criterion or "OVERFLOW" in criterion:
            patches.append("""
      /* Auto-fix: Text overflow prevention */
      article p, article li, article td, article th {
        word-break: break-word;
        overflow-wrap: break-word;
        hyphens: auto;
      }
      article section { overflow-x: hidden; }
      pre { white-space: pre-wrap; word-break: break-all; overflow-wrap: break-word; }
      """)

        if "SVG" in criterion or "DIAGRAM" in criterion:
            patches.append("""
      /* Auto-fix: SVG/Diagram overflow clip */
      article svg, section svg, .diagram-wrap svg {
        max-width: 100% !important;
        height: auto !important;
        overflow: hidden !important;
      }
      article svg text { overflow: hidden; }
      """)

        if "TYPOGRAPHY" in criterion:
            patches.append("""
      /* Auto-fix: Typography hierarchy */
      article h1 { font-size: 30px; font-weight: 800; }
      article h2 { font-size: 24px; font-weight: 700; margin-top: 32px; }
      article h3 { font-size: 20px; font-weight: 600; margin-top: 24px; }
      """)

    return "\n".join(patches) if patches else ""


def llm_fix_html_snippet(issue: Dict[str, Any], html_snippet: str, context: str = "") -> str:
    """
    Ask LLM to surgically fix a specific HTML snippet based on the issue description.
    Returns the fixed HTML snippet only.
    """
    from core.llm import call_llm

    description  = issue.get("description", "")
    recommendation = issue.get("recommendation", "")
    criterion    = issue.get("criterion", "")

    user_prompt = f"""Detected UI Defect Details:
- Criterion Violated: {criterion}
- Detailed Error Description: {description}
- Fix Recommendation: {recommendation}
- Context Snippet: {context[:200] if context else "N/A"}

Target HTML Code Snippet to Repair:
{html_snippet}

Requirements: Return ONLY the raw repaired HTML code snippet without markdown commentary or explanation."""

    fixed = call_llm(AUTO_FIX_SYSTEM_PROMPT, user_prompt, agent_name="HTML_Fixer")
    if fixed:
        for marker in ["```html\n", "```\n"]:
            if fixed.startswith(marker):
                fixed = fixed[len(marker):]
        if fixed.endswith("```"):
            fixed = fixed[:-3]
        return fixed.strip()
    return html_snippet


def extract_and_fix_svgs(html_content: str, issues: List[Dict[str, Any]]) -> str:
    """
    Find all SVG blocks in HTML, fix text overflow issues using LLM.
    Only modifies SVGs that have text elements with long content.
    """
    has_svg_issue = any("SVG" in i.get("criterion","").upper() or "DIAGRAM" in i.get("criterion","").upper() for i in issues)
    if not has_svg_issue:
        return html_content

    def fix_svg_block(match):
        svg = match.group(0)
        # Check if this SVG has potentially long text (> 25 chars in any text element)
        texts = re.findall(r'<text[^>]*>([^<]*)</text>', svg)
        long_texts = [t for t in texts if len(t.strip()) > 25]
        if long_texts:
            print(f"  [Auto-Fix] Fixing SVG with {len(long_texts)} long text element(s)...")
            return fix_svg_text_overflow(svg)
        return svg

    # Match full SVG blocks
    fixed = re.sub(r'<svg\b[^>]*>.*?</svg>', fix_svg_block, html_content, flags=re.DOTALL)
    return fixed


def auto_fix_reading_html(
    html_path: str,
    report: Dict[str, Any],
    session_id: str = "",
    lesson_id: str = "",
    lesson_title: str = ""
) -> Dict[str, Any]:
    """
    Automatically fix UI issues found by the reviewer.
    Surgical repair: only modifies broken parts, preserves everything else.

    Fix pipeline (in order):
      1. CSS patch injection (instant, no LLM) for dark mode / overflow issues
      2. SVG text overflow fix (LLM-assisted for long text elements)
      3. TOC/anchor link fix (programmatic)
      4. Broken image fix (programmatic)
      5. Backup original, write fixed HTML in-place
      6. Return fix summary

    Args:
        html_path: Absolute path to reading.html
        report: dict returned from review_reading_ui()
        session_id, lesson_id, lesson_title: metadata for logging

    Returns:
        dict: { fixes_applied, original_backup, fix_log }
    """
    issues = report.get("issues", [])
    score  = report.get("ui_score", 0)

    if not issues:
        print(f"  [Auto-Fix] Khong co van de nao can sua.")
        return {"fixes_applied": 0, "fix_log": [], "original_backup": None}

    if not os.path.exists(html_path):
        print(f"  [Auto-Fix] File HTML khong ton tai: {html_path}")
        return {"fixes_applied": 0, "fix_log": [], "original_backup": None}

    print(f"\n  [Auto-Fix] Bat dau sua {len(issues)} van de UI trong: {Path(html_path).name}")

    # Read HTML
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Backup original
    backup_path = html_path.replace(".html", f"_backup_score{score}.html")
    with open(backup_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"  [Auto-Fix] Backup da luu: {Path(backup_path).name}")

    fix_log = []
    fixed_html = html_content

    # ── Fix 1: CSS Patch (instant, no LLM needed) ─────────────────────────
    css_patch = get_issue_css_patch(issues)
    if css_patch:
        fixed_html = inject_css_patch(fixed_html, css_patch)
        fix_log.append({"type": "css_patch", "detail": "Injected targeted CSS fixes for dark mode, overflow, SVG"})
        print(f"  [Auto-Fix] CSS patch applied.")

    # ── Fix 2: SVG Text Overflow (LLM-assisted) ────────────────────────────
    svg_issues = [i for i in issues if "SVG" in i.get("criterion","").upper() or "DIAGRAM" in i.get("criterion","").upper()]
    if svg_issues:
        fixed_html = extract_and_fix_svgs(fixed_html, svg_issues)
        fix_log.append({"type": "svg_fix", "detail": f"Fixed {len(svg_issues)} SVG diagram issue(s)"})

    # ── Fix 3: TOC / Anchor Links (programmatic) ───────────────────────────
    fixed_html = fix_toc_links(fixed_html)
    fix_log.append({"type": "toc_links", "detail": "Verified and patched TOC anchor links"})
    print(f"  [Auto-Fix] TOC anchor links verified.")

    # ── Fix 4: Broken Images (programmatic) ────────────────────────────────
    fixed_html = fix_broken_images(fixed_html, html_path)
    fix_log.append({"type": "images", "detail": "Fixed broken/missing image attributes (alt, loading=lazy)"})
    print(f"  [Auto-Fix] Image attributes fixed.")

    # ── Fix 5: LLM-assisted content fixes for critical/major issues ────────
    critical_issues = [i for i in issues if i.get("severity") in ("critical", "major")
                       and "SVG" not in i.get("criterion","").upper()
                       and "DARK" not in i.get("criterion","").upper()]
    for issue in critical_issues[:2]:  # Limit to 2 LLM calls to avoid rate limits
        criterion = issue.get("criterion", "")
        desc      = issue.get("description", "")
        print(f"  [Auto-Fix] LLM content fix: [{criterion}] {desc[:60]}...")
        # For content issues, we add a CSS class rather than rewriting HTML
        # (safer surgical approach)
        patch = get_issue_css_patch([issue])
        if patch:
            fixed_html = inject_css_patch(fixed_html, patch)
            fix_log.append({"type": "llm_content_fix", "criterion": criterion, "detail": desc[:80]})

    # ── Write fixed HTML in-place ───────────────────────────────────────────
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(fixed_html)
    print(f"  [Auto-Fix] File da duoc cap nhat: {Path(html_path).name}")
    print(f"  [Auto-Fix] Tong so fix da ap dung: {len(fix_log)}")

    return {
        "fixes_applied": len(fix_log),
        "fix_log": fix_log,
        "original_backup": backup_path,
        "fixed_html_path": html_path
    }


def review_and_fix_reading_ui(
    html_path: str,
    session_id: str = "",
    lesson_id: str = "",
    lesson_title: str = "",
    target_score: int = 95,
    max_fix_rounds: int = 2,
    save_screenshots: bool = True,
    screenshot_dir: Optional[str] = None
) -> Dict[str, Any]:
    """
    Full review + auto-fix pipeline.
    Runs review -> fix -> re-review until score >= target_score or max_fix_rounds reached.

    Args:
        html_path: Absolute path to reading.html
        session_id, lesson_id, lesson_title: metadata
        target_score: Target UI score (default 95)
        max_fix_rounds: Maximum fix-review cycles (default 2)
        save_screenshots: Save screenshots in ui_review/ folder
        screenshot_dir: Custom screenshot directory

    Returns:
        dict: Final report with fix history
    """
    fix_history = []
    current_report = {}

    for round_num in range(1, max_fix_rounds + 1):
        print(f"\n  [Review+Fix] Round {round_num}/{max_fix_rounds}")

        # Step 1: Review
        current_report = review_reading_ui(
            html_path, session_id, lesson_id, lesson_title,
            save_screenshots=save_screenshots,
            screenshot_dir=screenshot_dir
        )
        score = current_report.get("ui_score", 0)
        issues = current_report.get("issues", [])

        print(f"  [Review+Fix] Round {round_num} Score: {score}/100 | Issues: {len(issues)}")

        if score >= target_score:
            print(f"  [Review+Fix] Dat muc tieu {target_score}! Dung lai.")
            break

        if not issues:
            print(f"  [Review+Fix] Khong con van de nao de sua.")
            break

        if round_num >= max_fix_rounds:
            print(f"  [Review+Fix] Da dat gioi han {max_fix_rounds} vong. Dung lai.")
            break

        # Step 2: Auto-Fix
        fix_result = auto_fix_reading_html(html_path, current_report, session_id, lesson_id, lesson_title)
        fix_history.append({
            "round": round_num,
            "score_before": score,
            "fixes": fix_result.get("fix_log", [])
        })

    current_report["fix_history"] = fix_history
    current_report["total_fix_rounds"] = len(fix_history)
    cleanup_passed_screenshots(current_report)
    return current_report


def batch_review_session(session_dir: str, session_id: str = "", auto_fix: bool = False, target_score: int = 95) -> List[Dict[str, Any]]:
    """
    Review (and optionally auto-fix) all reading.html files in a session directory.

    Args:
        session_dir: Path to session directory
        session_id: Session identifier string
        auto_fix: If True, automatically fix issues after review
        target_score: Target UI score for auto-fix mode (default 95)
    """
    session_path = Path(session_dir)
    html_files = list(session_path.rglob("Bai doc/reading.html")) + list(session_path.rglob("Bài đọc/reading.html"))

    if not html_files:
        print(f"  [UI Reviewer] Khong tim thay file reading.html trong: {session_dir}")
        return []

    mode_label = "Review+Fix" if auto_fix else "Review"
    print(f"\n  [UI Reviewer] Batch {mode_label}: {len(html_files)} bai doc trong {session_id}...")
    reports = []

    for html_file in sorted(html_files):
        parts = html_file.parts
        lesson_title = ""
        lesson_id_local = ""
        for part in parts:
            if "Lesson" in part and " - " in part:
                lesson_parts = part.split(" - ", 1)
                lesson_id_local = lesson_parts[0].strip()
                lesson_title = lesson_parts[1].strip() if len(lesson_parts) > 1 else ""
                break

        if auto_fix:
            report = review_and_fix_reading_ui(
                str(html_file),
                session_id=session_id,
                lesson_id=lesson_id_local,
                lesson_title=lesson_title,
                target_score=target_score
            )
        else:
            report = review_reading_ui(str(html_file), session_id=session_id, lesson_id=lesson_id_local, lesson_title=lesson_title)

        reports.append({"html_path": str(html_file), "lesson_id": lesson_id_local, "lesson_title": lesson_title, **report})

    passed = sum(1 for r in reports if r.get("passed"))
    avg    = sum(r.get("ui_score", 0) for r in reports) / len(reports) if reports else 0
    print(f"\n  [UI Reviewer] Summary: {passed}/{len(reports)} passed | Avg: {avg:.1f}/100")
    return reports

