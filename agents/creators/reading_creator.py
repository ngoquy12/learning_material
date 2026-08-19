"""
agents/creators/reading_creator.py
AI Reading Creator & Single Source of Truth (SSOT) Master HTML Generator.
Delegates specialized rendering, sanitizing, and visualizer building to core.renderers.reading package.
Uses Jinja2 template templates/prompts/reading_master_prompt.j2 for LLM orchestration.
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, List

from core.state import AgentState, require_tech_stack
from core.llm import call_llm
from core.skills import load_skill_content
from core.prompts import render_prompt
from core.renderers.reading_renderer import assemble_reading_html

# Re-export modular components for 100% backward compatibility
from core.renderers.reading import (
    convert_markdown_to_html,
    ensure_sentence_ending_period,
    slugify_id,
    guard_svg_syntax,
    sanitize_mermaid_code,
    guard_mermaid_syntax,
    LANGUAGE_MAPPING_REGISTRY,
    resolve_language_info,
    get_clean_language_name,
    highlight_code_syntax,
    convert_code_to_live_sandbox,
    generate_fallback_visualizer_steps,
    build_domain_adaptive_visualizer,
    CANONICAL_DOC_LINKS,
    validate_scope_boundary,
    sanitize_llm_json_text,
    sanitize_references,
    sanitize_html_tags_and_italics,
    inject_subheading_ids,
    clean_stray_chars,
    ensure_html,
    extract_2tier_toc,
    classify_reading_type
)

def robust_parse_llm_json(raw: str) -> dict:
    """3-tier robust JSON parser designed for LLM HTML-rich output."""
    raw_clean = sanitize_llm_json_text(raw)
    cleaned = raw_clean.strip()
    for prefix in ["```json\n", "```json", "```\n", "```"]:
        if cleaned.startswith(prefix):
            cleaned = cleaned[len(prefix):]
            break
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()

    # Tier 1: direct parse
    try:
        return json.loads(cleaned)
    except Exception:
        pass

    # Tier 2: fix literal newlines/tabs inside JSON string values
    try:
        fixed = re.sub(
            r'("(?:[^"\\]|\\.)*")',
            lambda m: m.group(0).replace('\n', '\\n').replace('\r', '').replace('\t', '\\t'),
            cleaned,
            flags=re.DOTALL
        )
        return json.loads(fixed)
    except Exception:
        pass

    # Tier 3: character-level field scanner
    def scan_string_value(text: str, start: int):
        if start >= len(text) or text[start] != '"':
            return None, start
        i = start + 1
        buf = []
        while i < len(text):
            c = text[i]
            if c == '\\' and i + 1 < len(text):
                nc = text[i + 1]
                if nc == 'n': buf.append('\n')
                elif nc == 't': buf.append('\t')
                elif nc == '"': buf.append('"')
                elif nc == '\\': buf.append('\\')
                else: buf.append(nc)
                i += 2
            elif c == '"':
                return ''.join(buf), i + 1
            elif c == '\n':
                buf.append('\n')
                i += 1
            else:
                buf.append(c)
                i += 1
        return ''.join(buf), i

    result = {}
    str_fields = [
        'section1_title', 'section2_title', 'problem_html', 'diagram_svg',
        'knowledge_html', 'example_code', 'example_html', 'notes_html'
    ]
    for field in str_fields:
        search_key = f'"{field}"'
        idx = cleaned.find(search_key)
        if idx == -1:
            continue
        pos = idx + len(search_key)
        while pos < len(cleaned) and cleaned[pos] in ' \t\r\n': pos += 1
        if pos < len(cleaned) and cleaned[pos] == ':': pos += 1
        while pos < len(cleaned) and cleaned[pos] in ' \t\r\n': pos += 1
        if pos < len(cleaned) and cleaned[pos] == '"':
            val, _ = scan_string_value(cleaned, pos)
            if val is not None:
                result[field] = val

    ref_match = re.search(r'"references"\s*:\s*(\[.*?\])', cleaned, re.DOTALL)
    if ref_match:
        try:
            result['references'] = json.loads(ref_match.group(1))
        except Exception:
            pass

    st_match = re.search(r'"self_test_questions"\s*:\s*(\[.*?\])', cleaned, re.DOTALL)
    if st_match:
        try:
            result['self_test_questions'] = json.loads(st_match.group(1))
        except Exception:
            pass

    return result

def generate_reading_html(
    session_id: str,
    lesson_id: str,
    lesson_title: str,
    lesson_details: str,
    expected_output: str,
    tech_stack: str,
    state: AgentState
) -> str:
    """Generate reading.html file adhering to 5-section pedagogical structure."""
    print(f"\n  ---> [Reading Creator SSOT] Authoring reading.html for {session_id} - {lesson_id}: {lesson_title}...")
    
    allowed_scope_raw = state.get("allowed_scope") or state.get("previous_lessons") or []
    if isinstance(allowed_scope_raw, list):
        allowed_scope = ", ".join(str(x) for x in allowed_scope_raw if str(x).strip())
    else:
        allowed_scope = str(allowed_scope_raw).strip()

    forbidden_scope_raw = state.get("forbidden_scope") or []
    if isinstance(forbidden_scope_raw, list):
        forbidden_scope = ", ".join(str(x) for x in forbidden_scope_raw if str(x).strip())
    else:
        forbidden_scope = str(forbidden_scope_raw).strip()

    image_skill = load_skill_content("image_prompt_standard")
    
    from core.domain_knowledge import get_domain_for_session, format_domain_rules_for_prompt
    session_domain_data = state.get("session_domain") or get_domain_for_session(session_id)
    chosen_domain = state.get("chosen_domain") or session_domain_data.get("name_vi", "Hệ thống Doanh nghiệp")
    domain_prompt_block = format_domain_rules_for_prompt(session_domain_data)

    system_prompt = render_prompt("prompts/reading_master_prompt.j2", {
        "section1_title": f"Tại sao cần học {lesson_title}?",
        "section2_title": "Kiến thức và cú pháp cơ bản",
        "tech_stack": tech_stack,
        "image_skill": image_skill,
        "allowed_scope": allowed_scope,
        "forbidden_scope": forbidden_scope,
        "chosen_domain": chosen_domain,
        "domain_prompt_block": domain_prompt_block
    })

    blueprint = state.get("lesson_blueprint")
    if blueprint:
        blueprint_context = f"""Dữ liệu phác thảo bài học (Lesson Blueprint):
- Kịch bản thống nhất: {json.dumps(blueprint.get('real_world_scenario', {}), ensure_ascii=False)}
- Các khái niệm cốt lõi: {json.dumps(blueprint.get('key_concepts', []), ensure_ascii=False)}
- Các ví dụ thực tế lũy tiến: {json.dumps(blueprint.get('progressive_examples', []), ensure_ascii=False)}
- Lỗi thường gặp: {json.dumps(blueprint.get('gotchas_and_errors', []), ensure_ascii=False)}
"""
    else:
        blueprint_context = ""

    user_prompt = f"""{blueprint_context}
Author detailed, exhaustive reading material content for:
Session: {session_id}
Lesson: {lesson_id} - {lesson_title}
Curriculum Details: {lesson_details}
Expected Output: {expected_output}
Target Technology Stack: {tech_stack}
Allowed Knowledge Scope: {allowed_scope or 'Fundamentals up to current lesson'}
Forbidden Knowledge Scope (STRICTLY PROHIBITED): {forbidden_scope or 'Future unlearned tech/syntax'}

MANDATORY DEPTH & EXHAUSTIVE PEDAGOGY CONTRACT:
1. Section 2 MUST contain 3 full sub-sections (2.1, 2.2, 2.3) detailing syntax variants and mechanisms.
2. Section 3 MUST contain 3 progressive examples (3.1 Minimal syntax, 3.2 Business logic, 3.3 Enterprise scenario).
3. STRICT KNOWLEDGE SCOPE: 100% of code examples and explanations MUST ONLY use concepts from Allowed Knowledge Scope.
4. Section 5 MUST contain exactly 3 interactive self-test MCQ questions under self_test_questions.
5. Return ONLY raw pure JSON strictly adhering to the schema."""

    llm_resp = call_llm(
        system_prompt,
        user_prompt,
        json_mode=True,
        agent_name="Reading_Creator_SSOT",
        session_id=session_id,
        lesson_id=lesson_id
    )

    data = {}
    try:
        data = robust_parse_llm_json(llm_resp)
        if not data:
            raise ValueError("Empty parse result")
    except Exception as e:
        print(f"  [Reading Creator Warning] All JSON parse tiers failed: {e}. Using minimal fallback.")
        data = {}

    section1_title = (data.get("section1_title") or f"Tại sao cần học {lesson_title}?").strip()
    section2_title = (data.get("section2_title") or f"Kiến thức và cú pháp cơ bản").strip()

    # Apply Diagram & Syntax Guards
    prob_html = clean_stray_chars(guard_mermaid_syntax(ensure_html(data.get("problem_html") or data.get("problem_text", ""))))
    prob_html = re.sub(r'<div\s+class="[^"]*my-6[^"]*text-center[^"]*">\s*<img\b.*?</p>\s*</div>', '', prob_html, flags=re.DOTALL | re.IGNORECASE)
    prob_html = re.sub(r'<img\b[^>]*>', '', prob_html, flags=re.IGNORECASE)
    diagram_svg = guard_svg_syntax(data.get("diagram_svg", ""))
    
    clean_lesson_slug = slugify_id(lesson_title)
    dynamic_img_name = f"scene_{clean_lesson_slug}.png"
    
    has_image_on_disk = False
    if state:
        try:
            from agents.creator_agents import get_lesson_dir
            from agents.creators.mindmap_creator import generate_image_api
            lesson_dir = get_lesson_dir(state)
            images_dir = lesson_dir / "Bài đọc" / "images"
            images_dir.mkdir(parents=True, exist_ok=True)
            image_file = images_dir / dynamic_img_name
            if image_file.exists() and image_file.stat().st_size > 1000:
                has_image_on_disk = True
            else:
                image_prompt = data.get("image_prompt") or f"Clean 2D Flat Vector Technical Infographic Illustration, 16:9 widescreen, depicting {lesson_title} real-world problem scenario in {tech_stack}, clean vector icons, professional corporate palette navy slate emerald, no text overlays, minimalist."
                if generate_image_api(image_prompt, image_file):
                    has_image_on_disk = True
        except Exception as e:
            print(f"  [Image Generator Notice] Skipped scene image generation: {e}")

    if has_image_on_disk:
        sec1_visual_html = f"""<div class="my-6 text-center">
  <img src="images/{dynamic_img_name}" alt="Sơ đồ bối cảnh thực tế: {lesson_title}" class="w-full max-w-3xl h-auto mx-auto rounded-xl shadow-sm border border-slate-200" onerror="this.closest('.my-6').style.display='none';" />
  <p class="text-center text-sm text-slate-500 italic mt-3">Hình 1.1: Sơ đồ bối cảnh thực tế bài học: {lesson_title}</p>
</div>"""
        context_img_url = f"images/{dynamic_img_name}"
    elif diagram_svg and len(diagram_svg.strip()) > 50:
        sec1_visual_html = f"""<div class="my-6 text-center">
  <div class="max-w-3xl mx-auto">{diagram_svg}</div>
  <p class="text-center text-sm text-slate-500 italic mt-3">Hình 1.1: Sơ đồ luồng bối cảnh thực tế bài học: {lesson_title}</p>
</div>"""
        context_img_url = None
    else:
        sec1_visual_html = ""
        context_img_url = None

    know_html = clean_stray_chars(inject_subheading_ids(guard_mermaid_syntax(ensure_html(data.get("knowledge_html") or data.get("knowledge_text", "")))))
    
    has_existing_viz_in_know = (
        'id="sec-2-4' in know_html
        or 'viz-step-badge' in know_html
        or 'viz-code-display' in know_html
        or 'Mô phỏng cơ chế vận hành từng bước' in know_html
    )
    if not has_existing_viz_in_know:
        viz_spec = data.get("interactive_visualizer") or data.get("visualizer_spec")
        raw_sec2_4 = data.get("section2_4_html") or ""
        if viz_spec and isinstance(viz_spec, dict):
            section2_4 = build_domain_adaptive_visualizer(lesson_title, tech_stack, viz_spec)
        elif raw_sec2_4 and len(raw_sec2_4.strip()) > 30:
            section2_4 = raw_sec2_4
        else:
            section2_4 = ""

        if section2_4:
            know_html = know_html + "\n" + clean_stray_chars(inject_subheading_ids(section2_4))

    ex_text = clean_stray_chars(inject_subheading_ids(guard_mermaid_syntax(ensure_html(data.get("example_html") or data.get("example_text", "")))))
    notes_html = clean_stray_chars(ensure_html(data.get("notes_html") or data.get("notes_text", "")))

    prob_html = re.sub(r'^\s*<(?:h1|h2)\b[^>]*>.*?</(?:h1|h2)>\s*', '', prob_html, flags=re.DOTALL | re.IGNORECASE).strip()
    know_html = re.sub(r'^\s*<(?:h1|h2)\b[^>]*>.*?</(?:h1|h2)>\s*', '', know_html, flags=re.DOTALL | re.IGNORECASE).strip()
    ex_text = re.sub(r'^\s*<(?:h1|h2)\b[^>]*>.*?</(?:h1|h2)>\s*', '', ex_text, flags=re.DOTALL | re.IGNORECASE).strip()
    notes_html = re.sub(r'^\s*<(?:h1|h2)\b[^>]*>.*?</(?:h1|h2)>\s*', '', notes_html, flags=re.DOTALL | re.IGNORECASE).strip()

    lang_info = resolve_language_info(tech_stack)
    know_html = convert_code_to_live_sandbox(know_html, lang_info, force_static=False, sb_prefix="sec2")
    ex_text = convert_code_to_live_sandbox(ex_text, lang_info, force_static=False, sb_prefix="sec3")
    notes_html = convert_code_to_live_sandbox(notes_html, lang_info, force_static=True, sb_prefix="sec4")
    know_html = re.sub(r'(<div[^>]*id="line-\d+"[^>]*>)\s*\d+\.\s*', r'\1', know_html)

    refs_items = sanitize_references(data.get("references", []), tech_stack)
    
    json_payload = {
        "section_titles": {
            "sec1": section1_title,
            "sec2": section2_title,
            "sec3": "Các ví dụ ứng dụng thực tiễn",
            "sec4": "Tổng kết bài học & Các lỗi thường gặp",
            "sec5": "Tài liệu tham khảo & Câu hỏi ôn tập"
        },
        "sec1_html": prob_html,
        "sec1_visual_html": sec1_visual_html,
        "sec2_html": know_html,
        "sec3_html": ex_text,
        "sec4_html": notes_html,
        "context_image_url": context_img_url,
        "reference_links": refs_items,
        "show_visualizer": False,
        "self_test_questions": data.get("self_test_questions", [])
    }
    metadata = {
        "lesson_title": lesson_title,
        "tech_stack": tech_stack,
        "session_id": session_id,
        "lesson_id": lesson_id
    }
    full_html = assemble_reading_html(json_payload, metadata)
    print(f"  [Success] Compiled SSOT Master Reading HTML via Jinja2 Engine for {session_id} - {lesson_id}")
    return full_html

def html_writer_agent(state: AgentState) -> AgentState:
    """LangGraph Agent wrapper for Reading HTML SSOT generation."""
    session_id = state.get("session_id", "Session 01")
    lesson_id = state.get("lesson_id", "")
    core_ssot = state.get("core_ssot", {})
    lesson_title = core_ssot.get("session_title", "Course Session")
    lesson_details = core_ssot.get("lesson_details", "")
    expected_output = core_ssot.get("expected_output", "")
    tech_stack = require_tech_stack(state, "html_writer_agent")
    
    from agents.creator_agents import get_lesson_dir
    html_sub = None
    try:
        lesson_dir = get_lesson_dir(state)
        html_sub = lesson_dir / "Bài đọc"
        html_sub.mkdir(parents=True, exist_ok=True)
        with open(html_sub / "reading.html", "w", encoding="utf-8") as f:
            f.write(f"<!-- [ĐANG KHỞI TẠO BÀI ĐỌC...] Hệ thống đang chạy tác nhân AI để sinh nội dung cho {session_id} - {lesson_id}: {lesson_title}. Vui lòng đợi trong giây lát... -->\n")
    except Exception:
        pass

    html_content = generate_reading_html(
        session_id=session_id,
        lesson_id=lesson_id,
        lesson_title=lesson_title,
        lesson_details=lesson_details,
        expected_output=expected_output,
        tech_stack=tech_stack,
        state=state
    )
    
    state["html_content"] = html_content
    state["reading_material"] = html_content
    state.setdefault("artifacts_status", {})["html"] = "Approved"
    
    if html_sub:
        try:
            with open(html_sub / "reading.html", "w", encoding="utf-8") as f:
                f.write(html_content)
        except Exception:
            pass
            
    return state

# Stub helpers for compatibility
def unwrap_svg_and_diagrams(html_str: str) -> str:
    return html_str

def render_table(headers: List[str], rows: List[List[str]]) -> str:
    return ""

def force_center_media(html_str: str) -> str:
    return html_str

def ensure_comparison_table(html_str: str) -> str:
    return html_str

def ensure_problem_scene_image(html_str: str) -> str:
    return html_str

__all__ = [
    "generate_reading_html",
    "html_writer_agent",
    "classify_reading_type",
    "convert_markdown_to_html",
    "ensure_sentence_ending_period",
    "slugify_id",
    "guard_svg_syntax",
    "sanitize_mermaid_code",
    "guard_mermaid_syntax",
    "LANGUAGE_MAPPING_REGISTRY",
    "resolve_language_info",
    "get_clean_language_name",
    "highlight_code_syntax",
    "convert_code_to_live_sandbox",
    "generate_fallback_visualizer_steps",
    "build_domain_adaptive_visualizer",
    "CANONICAL_DOC_LINKS",
    "validate_scope_boundary",
    "sanitize_llm_json_text",
    "sanitize_references",
    "sanitize_html_tags_and_italics",
    "inject_subheading_ids",
    "clean_stray_chars",
    "ensure_html",
    "extract_2tier_toc",
    "unwrap_svg_and_diagrams",
    "render_table",
    "force_center_media",
    "ensure_comparison_table",
    "ensure_problem_scene_image"
]
