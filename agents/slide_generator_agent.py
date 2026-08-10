"""
agents/slide_generator_agent.py

Master HTML Slide Presentation Compiler (Rikkei Academy Golden Standard)
========================================================================
Generates 100% compliant HTML presentation decks matching slide_result/index.html:
- Tailwind CSS CDN with custom Rikkei palette (rikkei.red = #be111c, rikkei.dark = #0f172a)
- Phosphor Icons + Highlight.js + Mermaid.js v10
- Scroll-Snap 100vh full-screen deck (#slides-container with scroll-snap-type: y mandatory)
- Standard Cover Slide, Agenda Slide, Content Slides (Bento Cards, Theory/Code 2-column, Mermaid diagrams, 3-Card Columns)
- Bottom-right red triangle page number badge on every slide
- Bottom copyright footer & logo
"""

from __future__ import annotations

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class SlideGeneratorAgent:
    """Master Slide Generator Agent enforcing slide_result/index.html standards across all courses."""

    LOGO_URL = "https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png"

    def __init__(self):
        pass

    def sanitize_slide_text(self, text: str) -> str:
        """
        Enforces slide pedagogical language rules:
        1. Forbids AI/academic buzzwords ('thách thức kỹ thuật', 'phân tích thực tế', etc.)
        2. Strips hyperbolic words ('nhất', 'quá', 'vô cùng', 'tuyệt vời', 'bậc nhất', 'triệt để', 'khám phá', 'khai phá')
        3. Enforces Sentence Case (capitalizes first letter & proper technical terms, lowercase rest).
        """
        if not text:
            return ""

        # 1. Replace AI buzzwords & academic boilerplate phrases with clean dev terms
        buzzwords_map = [
            (r"bối cảnh thực tế\s*&\s*thách thức kỹ thuật", "Bối cảnh dự án & vấn đề cần giải quyết"),
            (r"trực quan hóa luồng kiến trúc\s*&\s*thao tác cốt lõi", "Sơ đồ kiến trúc & quy trình vận hành"),
            (r"quy chuẩn thực thi chuẩn\s*vs\s*anti-pattern", "Lỗi thường gặp & cách xử lý chuẩn"),
            (r"thách thức\s*&\s*bối cảnh thực tế", "Vấn đề thực tế"),
            (r"giải pháp hiện đại chuẩn doanh nghiệp", "Giải pháp áp dụng thực tế"),
            (r"thách thức kỹ thuật", "vấn đề kỹ thuật"),
            (r"bối cảnh\s*&\s*phân tích thực tế", "Bối cảnh & phân tích dự án"),
            (r"chuẩn hóa quy trình kỹ thuật\s*&\s*tự động hóa vận hành doanh nghiệp", "Quy trình vận hành & tự động hóa hệ thống"),
            (r"kiến trúc cốt lõi", "Kiến trúc hệ thống"),
            (r"khai phá", "Tìm hiểu"),
            (r"khám phá", "Tìm hiểu"),
        ]

        for pattern, replacement in buzzwords_map:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

        # 2. Strip hyperbolic words (nhất, quá, vô cùng, tuyệt vời, bậc nhất, triệt để)
        hyperboles = [
            r"\bnhất\b",
            r"\bquá\b",
            r"\bvô cùng\b",
            r"\btuyệt vời\b",
            r"\bbậc nhất\b",
            r"\btriệt để\b",
        ]
        for pattern in hyperboles:
            text = re.sub(pattern, "", text, flags=re.IGNORECASE)

        # Clean multi-spaces
        text = re.sub(r"\s+", " ", text).strip()

        # 3. Enforce Sentence Case (Capitalize 1st letter & proper technical terms, rest lowercase)
        proper_tech_terms = {
            "Git", "VCS", "CLI", "Python", "JS", "JavaScript", "TypeScript", "Java", "SQL", "HTML", "CSS",
            "Docker", "Linux", "Windows", "MacOS", "VS", "Code", "WASM", "Pyodide", "API", "REST", "JSON",
            "Anti-Pattern", "Best", "Practice", "Conventional", "Commits", "CI/CD", "RAM", "CPU", "Bento", "Rikkei",
            "Staging", "Area", "Commit", "Log", "Tree", "Working", "Restore", "Branch", "Merge", "Pull", "Push", "Rebase"
        }

        words = text.split()
        if len(words) > 1:
            title_cased_words = sum(1 for w in words if w[0].isupper() and w not in proper_tech_terms)
            if title_cased_words >= len(words) * 0.4:
                res_words = []
                for idx, w in enumerate(words):
                    clean_w = re.sub(r"[^\w\-\/]", "", w)
                    if idx == 0:
                        res_words.append(w[0].upper() + w[1:].lower())
                    elif clean_w in proper_tech_terms or clean_w.isupper():
                        res_words.append(w)
                    else:
                        res_words.append(w.lower())
                text = " ".join(res_words)

        if text:
            text = text[0].upper() + text[1:]

        return text

    def clean_title_string(self, text: str) -> str:
        """Clean raw identifier/snake_case titles into formatted Vietnamese title strings."""
        if not text:
            return ""
        clean = text.strip()
        if '_' in clean and ' ' not in clean:
            words = clean.split('_')
            clean_words = []
            for w in words:
                w_lower = w.lower()
                if w_lower in ['py', 'pvm', 'cli', 'api', 'http', 'crud', 'sql', 'orm', 'json', 'url', 'id', 'vs', 'code', 'wasm', 'git', 'vcs', 'pr', 'ui', 'ux']:
                    clean_words.append(w.upper())
                elif w_lower in ['va']:
                    clean_words.append("và")
                else:
                    clean_words.append(w.capitalize())
            clean = " ".join(clean_words)
        return self.sanitize_slide_text(clean)

    def extract_session_summary_bullets(self, lessons_data: List[Dict[str, Any]], core_ssot: Optional[Dict[str, Any]] = None) -> List[str]:
        """
        Dynamically extracts concise, fluid, high-impact summary key points (12-25 words each)
        directly from actual lesson scenes and content.
        NO static prefixes (no 'Nguyên lý...', 'Phòng tránh rủi ro...', 'Bẫy lỗi...').
        100% dynamic, flexible, and concise.
        """
        raw_bullets = []
        seen_keys = set()

        def clean_and_add(txt: str):
            if not txt:
                return
            cleaned = str(txt).strip()
            # Strip bullet markers and any HTML tags
            cleaned = re.sub(r'^\s*[\-\•\*\d\.]+\s*', '', cleaned).strip()
            cleaned = re.sub(r'<[^>]+>', '', cleaned).strip()
            # Strip static prefixes like "Nguyên lý...", "Phòng tránh...", "Gotchas:", "Bẫy lỗi:"
            cleaned = re.sub(r'^\s*(Nguyên lý|Quy chuẩn|Phòng tránh|Chuẩn hóa|Bẫy lỗi|Gotchas|Lưu ý)\s*[\&A-Za-z\s]*\:\s*', '', cleaned, flags=re.IGNORECASE).strip()
            
            # Ensure single closing period
            cleaned = re.sub(r'\.+$', '', cleaned) + '.'

            # Cap length to keep bullet items crisp and readable on slide (max 28 words)
            words = cleaned.split()
            if len(words) > 28:
                cleaned = " ".join(words[:28]) + "..."

            key = cleaned.lower()[:30]
            if len(cleaned) > 10 and key not in seen_keys:
                seen_keys.add(key)
                raw_bullets.append(cleaned)

        # 1. Extract directly from actual lesson scenes (bullets and key points)
        for l_data in lessons_data:
            if not isinstance(l_data, dict):
                continue
            scenes = l_data.get("scenes", [])
            for scene in scenes:
                if not isinstance(scene, dict):
                    continue
                sc_bullets = scene.get("bullets") or scene.get("summary_bullets") or scene.get("key_takeaways")
                if isinstance(sc_bullets, list):
                    for b in sc_bullets:
                        b_str = str(b).strip()
                        if ':' in b_str and not b_str.startswith("http"):
                            parts = b_str.split(':', 1)
                            clean_and_add(f"{parts[0].strip()} - {parts[1].strip()}")
                        else:
                            clean_and_add(b_str)

        # 2. Extract concepts from core_ssot if needed
        if len(raw_bullets) < 3 and core_ssot and isinstance(core_ssot, dict):
            concepts = core_ssot.get("concepts")
            if isinstance(concepts, dict):
                for cname, cdesc in concepts.items():
                    clean_and_add(f"{cname}: {cdesc}")
            elif isinstance(concepts, list):
                for c in concepts:
                    clean_and_add(str(c))

        # 3. Fallback synthesis from actual lesson titles if bullets are short
        if len(raw_bullets) < 3:
            for l_data in lessons_data:
                l_title = l_data.get("lesson_title") or ""
                clean_lt = self.clean_title_string(l_title)
                clean_lt = re.sub(r'^\s*(Session\s*\d+|Lesson\s*\d+|Bài\s*\d+|\[\d+\.\d+\]|\d+\.)\s*[\:\-]?\s*', '', clean_lt, flags=re.IGNORECASE).strip()
                clean_lt = re.sub(r'^(Session\s*\d+\s*[\:\-]?\s*)+', '', clean_lt, flags=re.IGNORECASE).strip()
                if clean_lt:
                    clean_and_add(f"Thực hành thành thạo: {clean_lt}")

        return raw_bullets[:4]

    def truncate_title(self, title: str, max_chars: int = 60) -> str:
        """Truncate overly long titles gracefully for header presentation."""
        if not title:
            return "Nội dung bài học"
        clean = self.clean_title_string(title)
        clean = re.sub(r'^\d+[\.\:]\s*', '', clean)
        if len(clean) <= max_chars:
            return clean
        words = clean.split()
        short_words = []
        char_count = 0
        for w in words:
            if char_count + len(w) > max_chars:
                break
            short_words.append(w)
            char_count += len(w) + 1
        return " ".join(short_words) + "..." if short_words else clean[:max_chars] + "..."

    def _render_scene_content_html(self, scene: Dict[str, Any], clean_stitle: str, is_cli_or_tooling: bool = False) -> str:
        """Renders inner HTML slide content matching slide_result/index.html layout archetypes."""
        layout_type = str(scene.get("layout_type") or "").upper()
        
        # 1. CUSTOM RAW HTML
        if layout_type == "CUSTOM_RAW" and scene.get("html_content"):
            return scene.get("html_content")

        narration = scene.get("narration") or scene.get("explanation") or ""
        bullets = scene.get("bullets", [])
        code_sample = scene.get("code_sample") or scene.get("code") or ""
        mermaid_code = scene.get("mermaid") or scene.get("diagram") or ""
        image_url = scene.get("image_url") or scene.get("image_path") or scene.get("image") or ""
        image_caption = scene.get("image_caption") or scene.get("caption") or "Hình minh họa bối cảnh kỹ thuật thực tế"

        if not bullets and narration:
            raw_sentences = [s.strip() for s in re.split(r'[\.\;\n]', narration) if len(s.strip()) > 10]
            bullets = raw_sentences[:4]

        # 2. IMAGE EXPLAINER LAYOUT (16:9 Technical Image + Explainer Notes)
        if "IMAGE" in layout_type or image_url:
            bullet_items_html = ""
            if bullets:
                for b in bullets[:4]:
                    parts = b.split(':', 1) if ':' in b else [b, ""]
                    title_p = self.sanitize_slide_text(re.sub(r'[\u274c\u2705\u26a0\ufe0f]', '', parts[0]).strip())
                    desc_p = self.sanitize_slide_text(re.sub(r'[\u274c\u2705\u26a0\ufe0f]', '', parts[1] if len(parts) > 1 else parts[0]).strip())
                    bullet_items_html += f"""
                <div class="flex items-start gap-3">
                  <i class="ph-bold ph-check-circle text-rikkei-red text-xl shrink-0 mt-0.5"></i>
                  <div>
                    <div class="font-bold text-slate-900 text-[17px] mb-1">{title_p}</div>
                    <p class="text-slate-700 text-[15px] leading-relaxed font-normal">{desc_p}</p>
                  </div>
                </div>"""
            else:
                bullet_items_html = f"""
                <div class="text-slate-700 text-[15px] leading-relaxed">
                  {self.sanitize_slide_text(narration[:300]) if narration else 'Hình ảnh minh họa bối cảnh thực tế và quy trình vận hành hệ thống.'}
                </div>"""

            image_caption_clean = self.sanitize_slide_text(image_caption)
            return f"""
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 w-full mt-9 mb-auto items-start">
            <div class="flex flex-col justify-start items-center w-full h-fit">
              <img src="{image_url}" alt="{clean_stitle}" class="w-full max-h-[440px] object-contain rounded-xl" onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1200&q=80';"/>
              <p class="text-slate-500 text-[14px] italic mt-3 text-center font-medium">{image_caption_clean}</p>
            </div>
            <div class="bento-card p-6 rounded-xl bg-slate-50 border border-slate-200 flex flex-col justify-start gap-4 text-left h-fit shadow-sm">
              <div>
                <h5 class="font-bold text-slate-900 text-[20px] mb-4 flex items-center gap-2.5">
                  <i class="ph-bold ph-lightbulb text-rikkei-red text-2xl"></i> Bối cảnh &amp; phân tích dự án
                </h5>
                <div class="space-y-4">
                  {bullet_items_html}
                </div>
              </div>
              <div class="mt-2 p-3 bg-white border border-slate-200 rounded-xl flex items-center gap-2.5 text-slate-800 text-[14px] font-semibold shadow-sm">
                <i class="ph-bold ph-shield-check text-emerald-600 text-lg shrink-0"></i>
                <span>Quy trình vận hành &amp; tự động hóa hệ thống.</span>
              </div>
            </div>
          </div>
"""

        # 3. VISUAL MINDMAP LAYOUT (Sơ đồ tư duy dạng khối trực quan)
        elif "MINDMAP" in layout_type or scene.get("mindmap_branches"):
            center_title = scene.get("mindmap_center") or clean_stitle or "Kiến trúc hệ thống"
            center_title = self.sanitize_slide_text(re.sub(r'[\u274c\u2705\u26a0\ufe0f]', '', center_title).strip())
            branches = scene.get("mindmap_branches") or []
            if not branches and bullets:
                branches = []
                icons = ["ph-tree-structure", "ph-arrows-left-right", "ph-database", "ph-shield-check"]
                for idx, b in enumerate(bullets[:4]):
                    parts = b.split(':', 1) if ':' in b else [b, ""]
                    branches.append({
                        "title": re.sub(r'[\u274c\u2705\u26a0\ufe0f]', '', parts[0]).strip(),
                        "icon": icons[idx % len(icons)],
                        "description": re.sub(r'[\u274c\u2705\u26a0\ufe0f]', '', parts[1] if len(parts) > 1 else parts[0]).strip()
                    })

            branch_cards_html = ""
            for br in branches[:4]:
                b_title = self.sanitize_slide_text(re.sub(r'[\u274c\u2705\u26a0\ufe0f]', '', br.get("title") or "Thành phần").strip())
                b_icon = br.get("icon") or "ph-diamonds-four"
                b_desc = self.sanitize_slide_text(re.sub(r'[\u274c\u2705\u26a0\ufe0f]', '', br.get("description") or "").strip())
                branch_cards_html += f"""
              <div class="bento-card p-5 rounded-xl border border-slate-200 bg-white text-left flex flex-col justify-start gap-3 shadow-sm h-fit">
                <div>
                  <h6 class="font-bold text-slate-900 text-[18px] mb-2 flex items-center gap-2">
                    <i class="ph-bold {b_icon} text-rikkei-red text-lg"></i> {b_title}
                  </h6>
                  <p class="text-slate-600 text-[14px] leading-relaxed mt-1.5">{b_desc}</p>
                </div>
                <div class="mt-2 pt-2.5 border-t border-slate-100 flex items-center gap-1.5 text-rikkei-red text-[11px] font-bold uppercase tracking-wider">
                  <i class="ph-bold ph-check text-xs"></i> Core Standard
                </div>
              </div>"""

            return f"""
          <div class="flex flex-col gap-5 w-full mt-9 mb-auto justify-start">
            <div class="w-full bg-slate-900 text-white p-4 rounded-xl text-center shadow-md border border-slate-800 flex items-center justify-center gap-3">
              <i class="ph-bold ph-brain text-rikkei-red text-2xl"></i>
              <span class="font-montserrat font-extrabold text-[20px] tracking-wide">{center_title}</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 w-full items-start">
              {branch_cards_html}
            </div>
          </div>
"""

        # 4. MERMAID DIAGRAM LAYOUT
        elif "MERMAID" in layout_type or mermaid_code:
            clean_mermaid = mermaid_code.strip()
            return f"""
          <div class="w-full flex justify-center bg-slate-50 p-6 rounded-xl border border-slate-200 mt-9 mb-auto items-center h-fit">
            <div class="mermaid w-full max-w-4xl scale-105">
              {clean_mermaid}
            </div>
          </div>
"""

        # 5. CODE / COMMAND EXPLAINER LAYOUT (Theory + Code Box)
        elif code_sample or "CODE" in layout_type:
            lang = "bash" if is_cli_or_tooling else "python"
            bullet_items_html = ""
            if bullets:
                for b in bullets[:4]:
                    parts = b.split(':', 1) if ':' in b else [b, ""]
                    title_p = self.sanitize_slide_text(re.sub(r'[\u274c\u2705\u26a0\ufe0f]', '', parts[0]).strip())
                    desc_p = self.sanitize_slide_text(re.sub(r'[\u274c\u2705\u26a0\ufe0f]', '', parts[1] if len(parts) > 1 else parts[0]).strip())
                    bullet_items_html += f"""
                <div>
                  <div class="font-bold text-slate-900 text-[17px] mb-1 flex items-center gap-2">
                    <i class="ph-bold ph-caret-right text-rikkei-red"></i> {title_p}:
                  </div>
                  <p class="text-slate-600 text-[14px] leading-relaxed pl-5">{desc_p}</p>
                </div>"""
            else:
                bullet_items_html = f"""
                <div>
                  <div class="font-bold text-slate-900 text-[17px] mb-1 flex items-center gap-2">
                    <i class="ph-bold ph-caret-right text-rikkei-red"></i> Nguyên lý thực thi thực tế:
                  </div>
                  <p class="text-slate-600 text-[14px] leading-relaxed pl-5">{self.sanitize_slide_text(narration[:240]) if narration else 'Mã nguồn minh họa cơ chế hoạt động của hệ thống.'}</p>
                </div>"""

            safe_code = code_sample.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            return f"""
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 w-full mt-9 mb-auto items-start">
            <div class="bento-card p-6 rounded-xl bg-slate-50 border border-slate-200 flex flex-col justify-start gap-4 text-left h-fit shadow-sm">
              <div>
                <h5 class="font-bold text-slate-900 text-[20px] mb-4 flex items-center gap-2.5">
                  <i class="ph-bold ph-book-open text-rikkei-red text-2xl"></i> Nguyên lý &amp; lưu ý thực thi
                </h5>
                <div class="space-y-4 text-slate-800 text-[15px]">
                  {bullet_items_html}
                </div>
              </div>
              <div class="mt-2 p-3 bg-white border border-slate-200 rounded-xl flex items-center gap-2.5 text-slate-800 text-[14px] font-semibold shadow-sm">
                <i class="ph-bold ph-terminal-window text-rikkei-red text-lg shrink-0"></i>
                <span>Thao tác thực thi theo quy chuẩn kỹ thuật.</span>
              </div>
            </div>
            <div class="flex flex-col h-fit">
              <pre class="bg-slate-900 text-emerald-400 p-6 rounded-xl font-mono text-[14px] overflow-auto border border-slate-800 shadow-xl leading-relaxed max-h-[380px] h-fit"><code class="language-{lang}">{safe_code}</code></pre>
            </div>
          </div>
"""

        # 6. GOOD VS BAD PRACTICE COMPARISON LAYOUT
        elif "COMPARISON" in layout_type or scene.get("bad_practice") or scene.get("good_practice"):
            bad = scene.get("bad_practice") or {}
            good = scene.get("good_practice") or {}
            
            bad_raw = bad.get("title") or "Thao tác thủ công"
            bad_clean = self.sanitize_slide_text(re.sub(r'^(Anti-Pattern|Cách làm sai)\s*[\:\-]?\s*', '', re.sub(r'[\u274c\u2705\u26a0\ufe0f]', '', bad_raw).strip(), flags=re.IGNORECASE).strip())
            bad_code = bad.get("code") or (bullets[0] if len(bullets) > 0 else "Thao tác thủ công không qua kiểm thử")
            bad_reason = self.sanitize_slide_text(bad.get("reason") or "Dễ phát sinh lỗi hệ thống và rò rỉ dữ liệu.")

            good_raw = good.get("title") or "Quy trình tự động hóa"
            good_clean = self.sanitize_slide_text(re.sub(r'^(Best Practice|Quy chuẩn đúng)\s*[\:\-]?\s*', '', re.sub(r'[\u274c\u2705\u26a0\ufe0f]', '', good_raw).strip(), flags=re.IGNORECASE).strip())
            good_code = good.get("code") or (bullets[1] if len(bullets) > 1 else "Chuẩn hóa quy trình vận hành tự động")
            good_reason = self.sanitize_slide_text(good.get("reason") or "Đảm bảo tính ổn định và tối ưu hiệu năng làm việc.")

            return f"""
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 w-full mt-9 mb-auto items-start">
            <div class="bento-card p-6 rounded-xl border border-red-200 bg-red-500/5 text-left flex flex-col justify-start gap-4 relative overflow-hidden h-fit shadow-sm">
              <div class="select-none">
                <h5 class="font-bold text-red-900 text-[20px] flex items-center gap-2.5 mb-3.5">
                  <i class="ph-bold ph-x-circle text-2xl text-red-600 shrink-0"></i> <span>Anti-Pattern: {bad_clean}</span>
                </h5>
                <pre class="bg-red-100/60 text-red-950 p-4 rounded-xl font-mono text-sm mb-3.5 border border-red-200 shadow-sm"><code>{bad_code}</code></pre>
                <p class="text-slate-800 text-[15px] leading-relaxed font-medium">
                  {bad_reason}
                </p>
              </div>
              <div class="p-3 bg-red-100/70 border border-red-200 rounded-xl text-red-900 text-xs font-semibold flex items-center gap-2 mt-1">
                <i class="ph-bold ph-warning text-red-600 text-base shrink-0"></i>
                <span>Cảnh báo rủi ro phát sinh sự cố.</span>
              </div>
            </div>
            <div class="bento-card p-6 rounded-xl border border-emerald-200 bg-emerald-500/5 text-left flex flex-col justify-start gap-4 relative overflow-hidden h-fit shadow-sm">
              <div class="select-none">
                <h5 class="font-bold text-emerald-900 text-[20px] flex items-center gap-2.5 mb-3.5">
                  <i class="ph-bold ph-check-circle text-2xl text-emerald-600 shrink-0"></i> <span>Best Practice: {good_clean}</span>
                </h5>
                <pre class="bg-emerald-100/60 text-emerald-950 p-4 rounded-xl font-mono text-sm mb-3.5 border border-emerald-200 shadow-sm"><code>{good_code}</code></pre>
                <p class="text-slate-800 text-[15px] leading-relaxed font-medium">
                  {good_reason}
                </p>
              </div>
              <div class="p-3 bg-emerald-100/70 border border-emerald-200 rounded-xl text-emerald-900 text-xs font-semibold flex items-center gap-2 mt-1">
                <i class="ph-bold ph-seal-check text-emerald-600 text-base shrink-0"></i>
                <span>Quy trình chuẩn hóa thực tế.</span>
              </div>
            </div>
          </div>
"""

        # 7. DEFAULT 2-COLUMN BENTO GRID CARDS LAYOUT
        else:
            p_text1 = self.sanitize_slide_text(bullets[0] if len(bullets) > 0 else (narration[:240] if narration else f"Hạn chế khi phát triển hệ thống với {clean_stitle}."))
            p_text2 = self.sanitize_slide_text(bullets[1] if len(bullets) > 1 else (narration[240:480] if len(narration) > 240 else f"Giải pháp quy trình cho {clean_stitle}."))
            
            c1_title = self.sanitize_slide_text(re.sub(r'[\u274c\u2705\u26a0\ufe0f]', '', scene.get("col1_title") or "Vấn đề thực tế").strip())
            c2_title = self.sanitize_slide_text(re.sub(r'[\u274c\u2705\u26a0\ufe0f]', '', scene.get("col2_title") or "Giải pháp áp dụng").strip())

            return f"""
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 w-full mt-9 mb-auto items-start">
            <div class="bento-card p-6 rounded-xl border border-red-200 bg-red-500/5 text-left flex flex-col justify-start gap-4 relative overflow-hidden h-fit shadow-sm">
              <div class="select-none">
                <h5 class="font-bold text-red-900 text-[20px] flex items-center gap-2.5 mb-3.5">
                  <i class="ph-bold ph-x-circle text-2xl text-red-600 shrink-0"></i> <span>{c1_title}</span>
                </h5>
                <p class="text-slate-800 text-[15px] leading-relaxed font-medium">
                  {p_text1}
                </p>
              </div>
              <div class="p-3 bg-red-100/70 border border-red-200 rounded-xl text-red-900 text-xs font-semibold flex items-center gap-2 mt-1">
                <i class="ph-bold ph-warning text-red-600 text-base shrink-0"></i>
                <span>Rủi ro phát sinh lỗi và chậm tiến độ.</span>
              </div>
            </div>
            <div class="bento-card p-6 rounded-xl border border-emerald-200 bg-emerald-500/5 text-left flex flex-col justify-start gap-4 relative overflow-hidden h-fit shadow-sm">
              <div class="select-none">
                <h5 class="font-bold text-emerald-900 text-[20px] flex items-center gap-2.5 mb-3.5">
                  <i class="ph-bold ph-check-circle text-2xl text-emerald-600 shrink-0"></i> <span>{c2_title}</span>
                </h5>
                <p class="text-slate-800 text-[15px] leading-relaxed font-medium">
                  {p_text2}
                </p>
              </div>
              <div class="p-3 bg-emerald-100/70 border border-emerald-200 rounded-xl text-emerald-900 text-xs font-semibold flex items-center gap-2 mt-1">
                <i class="ph-bold ph-seal-check text-emerald-600 text-base shrink-0"></i>
                <span>Tối ưu hiệu năng và quy trình làm việc.</span>
              </div>
            </div>
          </div>
"""

    def generate_session_deck_html(self, session_title: str, module_name: str, lessons_data: List[Dict[str, Any]], core_ssot: Optional[Dict[str, Any]] = None) -> str:
        """Master HTML Slide Presentation Deck Compiler for 1 Session matching slide_result/index.html."""
        current_year = datetime.now().year
        copyright_text = f"© {current_year} By Rikkei Education - All rights reserved."

        clean_session_title = self.clean_title_string(session_title)
        # Clean duplicate Session XX / Lesson YY prefixes
        clean_session_title = re.sub(r'^(Session\s*\d+\s*[\:\-]?\s*Lesson\s*\d+\s*[\:\-]?\s*)+', '', clean_session_title, flags=re.IGNORECASE).strip()
        clean_session_title = re.sub(r'^(Session\s*\d+\s*[\:\-]\s*)+', r'\1', clean_session_title, flags=re.IGNORECASE).strip()
        
        # Parse Session Tag (e.g. Session 01, Session 02)
        m_sess = re.search(r'^(Session\s*\d+)\s*[:-]?\s*(.*)', clean_session_title, re.IGNORECASE)
        if m_sess:
            session_tag_text = m_sess.group(1).strip()
            main_title_text = m_sess.group(2).strip()
        else:
            session_tag_text = "Session 01"
            main_title_text = clean_session_title

        # Preserve course name cleanly without fallback to generic "Chương trình Đào tạo Doanh nghiệp"
        clean_module_name = module_name.strip()
        if not clean_module_name or clean_module_name.upper() in ["PYTHON", "GIT", "WEB", "IT"]:
            clean_module_name = "Chương trình Đào tạo Công nghệ Thông tin"

        ts_lower = (session_title + " " + module_name).lower()
        is_cli_or_tooling = any(k in ts_lower for k in ["git", "vcs", "terminal", "cli", "bash", "docker", "agile", "scrum", "uml", "figma", "ui", "design"])

        slide_wrappers_html = []

        # ── 1. COVER SLIDE (Slide Index 0, Page 1) ─────────────────────────────
        slide_wrappers_html.append(f"""
      <!-- Slide 0: Cover Slide -->
      <div class="slide-wrapper" id="slide-1" data-slide-index="0">
        <section class="slide-card relative bg-white border border-slate-200 rounded-2xl flex flex-col justify-between p-16 overflow-hidden">
          <!-- Left red banner decoration -->
          <div class="absolute left-0 top-1/2 -translate-y-1/2 w-12 h-40 bg-rikkei-red" style="clip-path: polygon(0 0, 0 100%, 100% 50%)"></div>
          <!-- Right decorative triangle grid -->
          <svg class="absolute -right-4 top-1/2 -translate-y-1/2 h-[80%] w-[35%] text-rikkei-red select-none pointer-events-none opacity-80" fill="currentColor" viewBox="0 0 200 400">
            <polygon points="180,60 190,65 180,70"></polygon>
            <polygon points="180,90 190,95 180,100"></polygon>
            <polygon points="180,120 190,125 180,130"></polygon>
            <polygon points="180,150 190,155 180,160"></polygon>
            <polygon points="180,180 190,185 180,190"></polygon>
            <polygon points="180,210 190,215 180,220"></polygon>
            <polygon points="180,240 190,245 180,250"></polygon>
            <polygon points="180,270 190,275 180,280"></polygon>
            <polygon points="180,300 190,305 180,310"></polygon>
            <polygon points="180,330 190,335 180,340"></polygon>
            <polygon points="160,80 170,85 160,90"></polygon>
            <polygon points="160,110 170,115 160,120"></polygon>
            <polygon points="160,140 170,145 160,150"></polygon>
            <polygon points="160,170 170,175 160,180"></polygon>
            <polygon points="160,200 170,205 160,210"></polygon>
            <polygon points="160,230 170,235 160,240"></polygon>
            <polygon points="160,260 170,265 160,270"></polygon>
            <polygon points="160,290 170,295 160,300"></polygon>
            <polygon points="160,320 170,325 160,330"></polygon>
            <polygon points="140,100 150,105 140,110"></polygon>
            <polygon points="140,130 150,135 140,140"></polygon>
            <polygon points="140,160 150,165 140,170"></polygon>
            <polygon points="140,190 150,195 140,200"></polygon>
            <polygon points="140,220 150,225 140,230"></polygon>
            <polygon points="140,250 150,255 140,260"></polygon>
            <polygon points="140,280 150,285 140,290"></polygon>
            <polygon points="140,300 150,305 140,310"></polygon>
            <polygon points="120,120 130,125 120,130"></polygon>
            <polygon points="120,150 130,155 120,160"></polygon>
            <polygon points="120,180 130,185 120,190"></polygon>
            <polygon points="120,210 130,215 120,220"></polygon>
            <polygon points="120,240 130,245 120,250"></polygon>
            <polygon points="120,270 130,275 120,280"></polygon>
          </svg>
          <!-- Text Contents -->
          <div class="my-auto ml-10 space-y-5 text-left select-none max-w-none w-full pr-12">
            <h2 class="font-montserrat font-extrabold text-[38px] text-rikkei-red">
              {session_tag_text}:
            </h2>
            <h1 class="font-montserrat font-extrabold text-[52px] text-black leading-tight break-words w-full">
              {main_title_text}
            </h1>
            <div class="pt-8 space-y-2 text-slate-600 text-[22px] font-medium">
              <p>Môn học: {clean_module_name}</p>
            </div>
          </div>
          <!-- Bottom Logo & Footer -->
          <div class="absolute bottom-4 left-1/2 -translate-x-1/2 flex flex-col items-center gap-3 w-full max-w-200 text-center">
            <img alt="Rikkei Academy Logo" class="h-10 object-contain" src="{self.LOGO_URL}"/>
            <span class="text-[16px] text-black font-normal">
              {copyright_text}
            </span>
          </div>
          <!-- Bottom right red triangle page number -->
          <div class="absolute right-0 bottom-0 w-24 h-24 bg-rikkei-red z-30" style="clip-path: polygon(100% 0, 0 100%, 100% 100%)">
            <span class="absolute text-white font-montserrat font-bold text-[18px] select-none z-40" style="right: 14px; bottom: 10px;">1</span>
          </div>
        </section>
      </div>""")

        # ── 2. AGENDA SLIDE (Slide Index 1, Page 2) ────────────────────────────
        agenda_items_html = ""
        agenda_index = 1
        for l_data in lessons_data:
            l_title = l_data.get("lesson_title") or f"Bài học {agenda_index}"
            clean_l_title = self.clean_title_string(l_title)
            # Strip ALL prefixes: Session XX, Lesson YY, Bài XX, [01.01], digits + dot, colons
            clean_l_title = re.sub(r'^\s*(Session\s*\d+|Lesson\s*\d+|Bài\s*\d+|\[\d+\.\d+\]|\d+\.)\s*[\:\-]?\s*', '', clean_l_title, flags=re.IGNORECASE).strip()
            clean_l_title = re.sub(r'^(Session\s*\d+\s*[\:\-]?\s*)+', '', clean_l_title, flags=re.IGNORECASE).strip()
            agenda_items_html += f"""
            <div class="flex items-start gap-5 text-[30px] font-sans font-bold text-black leading-snug w-full">
              <span class="w-10 shrink-0 text-black">{agenda_index}.</span>
              <span class="flex-1 break-words">{clean_l_title}</span>
            </div>"""
            agenda_index += 1

        slide_wrappers_html.append(f"""
      <!-- Slide 1: Agenda Slide -->
      <div class="slide-wrapper" id="slide-2" data-slide-index="1">
        <section class="slide-card relative bg-white border border-slate-200 rounded-2xl flex flex-col justify-between p-12 overflow-hidden">
          <div class="w-full flex-1 flex flex-col justify-start">
            <!-- Header Area -->
            <div class="flex justify-between items-start select-none shrink-0 mb-9 w-full">
              <div class="text-[36px] font-montserrat font-extrabold text-rikkei-red leading-none">
                NỘI DUNG BÀI HỌC
              </div>
              <img alt="Rikkei Academy Logo" class="h-10 object-contain shrink-0 mt-0.5" src="{self.LOGO_URL}"/>
            </div>
            <!-- List Content -->
            <div class="w-full flex flex-col justify-start pl-4 pr-4">
              <div class="space-y-8 text-left select-none w-full max-w-none">
                {agenda_items_html}
              </div>
            </div>
          </div>
          <div class="absolute bottom-4 left-1/2 -translate-x-1/2 text-center w-full max-w-200">
            <span class="text-[16px] text-black font-normal">
              {copyright_text}
            </span>
          </div>
          <div class="absolute right-0 bottom-0 w-24 h-24 bg-rikkei-red z-30" style="clip-path: polygon(100% 0, 0 100%, 100% 100%)">
            <span class="absolute text-white font-montserrat font-bold text-[18px] select-none z-40" style="right: 14px; bottom: 10px;">2</span>
          </div>
        </section>
      </div>""")

        # ── 3..N. CONTENT SLIDES (Slide Index 2..N, Pages 3..N+2) ─────────────
        page_counter = 3
        slide_wrapper_idx = 2

        for l_idx, l_data in enumerate(lessons_data, 1):
            l_title = l_data.get("lesson_title") or f"Bài học {l_idx}"
            clean_l_title = self.clean_title_string(l_title)
            # Strip ALL Session XX, Lesson YY, Bài XX prefixes from main title
            clean_l_title = re.sub(r'^\s*(Session\s*\d+|Lesson\s*\d+|Bài\s*\d+|\[\d+\.\d+\]|\d+\.)\s*[\:\-]?\s*', '', clean_l_title, flags=re.IGNORECASE).strip()
            clean_l_title = re.sub(r'^(Session\s*\d+\s*[\:\-]?\s*)+', '', clean_l_title, flags=re.IGNORECASE).strip()

            scenes = l_data.get("scenes", [])
            for s_idx, scene in enumerate(scenes, 1):
                raw_stitle = scene.get("action_title") or scene.get("short_title") or scene.get("scene_title") or f"Chủ đề {s_idx}"
                clean_stitle = self.clean_title_string(raw_stitle)
                clean_stitle = re.sub(r'^\s*(\[\d+\.\d+\]|\d+\.)\s*', '', clean_stitle).strip()
                # Sanitize action sub-title: keep short & punchy, strip trailing 'Trong ...' repeating lesson name
                clean_stitle = re.sub(r'\s+(Trong|Dành cho|Với)\s+.*$', '', clean_stitle, flags=re.IGNORECASE).strip()
                
                main_large_title = f"{l_idx}. {clean_l_title}"
                inner_content = self._render_scene_content_html(scene, clean_stitle, is_cli_or_tooling=is_cli_or_tooling)

                slide_wrappers_html.append(f"""
      <!-- Slide {slide_wrapper_idx}: Content Slide -->
      <div class="slide-wrapper" id="slide-{page_counter}" data-slide-index="{slide_wrapper_idx}">
        <section class="slide-card relative bg-white border border-slate-200 rounded-2xl flex flex-col justify-between p-12 overflow-hidden">
          <div class="w-full flex-1 flex flex-col justify-start h-full">
            <div class="flex justify-between items-start select-none shrink-0 mb-0 w-full">
              <div class="w-full pr-8">
                <div class="text-[34px] font-montserrat font-extrabold text-rikkei-red leading-snug w-full break-words">
                  {main_large_title}
                </div>
                <div class="text-[24px] font-sans font-bold text-black mt-3 w-full break-words">
                  {clean_stitle}
                </div>
              </div>
              <img alt="Rikkei Academy Logo" class="h-10 object-contain shrink-0 mt-0.5" src="{self.LOGO_URL}"/>
            </div>
            {inner_content}
          </div>
          <div class="absolute bottom-4 left-1/2 -translate-x-1/2 text-center w-full max-w-200">
            <span class="text-[16px] text-black font-normal">
              {copyright_text}
            </span>
          </div>
          <div class="absolute right-0 bottom-0 w-24 h-24 bg-rikkei-red z-30" style="clip-path: polygon(100% 0, 0 100%, 100% 100%)">
            <span class="absolute text-white font-montserrat font-bold text-[18px] select-none z-40" style="right: 14px; bottom: 10px;">{page_counter}</span>
          </div>
        </section>
      </div>""")
                page_counter += 1
                slide_wrapper_idx += 1

        # ── 4. SUMMARY SLIDE (Final Slide) ──────────────────────────────────
        summary_bullets = self.extract_session_summary_bullets(lessons_data, core_ssot)

        summary_items_html = ""
        for s_bullet in summary_bullets:
            summary_items_html += f"""
            <div class="flex items-start gap-4 text-[26px] font-sans font-bold text-black leading-relaxed w-full">
              <i class="ph-bold ph-check-circle text-rikkei-red text-3xl shrink-0 mt-1"></i>
              <span class="flex-1 break-words">{s_bullet}</span>
            </div>"""

        slide_wrappers_html.append(f"""
      <!-- Slide {slide_wrapper_idx}: Summary Slide -->
      <div class="slide-wrapper" id="slide-{page_counter}" data-slide-index="{slide_wrapper_idx}">
        <section class="slide-card relative bg-white border border-slate-200 rounded-2xl flex flex-col justify-between p-12 overflow-hidden">
          <div class="w-full flex-1 flex flex-col justify-start">
            <!-- Header Area -->
            <div class="flex justify-between items-start select-none shrink-0 mb-9 w-full">
              <div class="text-[36px] font-montserrat font-extrabold text-rikkei-red leading-none">
                TỔNG KẾT BÀI HỌC
              </div>
              <img alt="Rikkei Academy Logo" class="h-10 object-contain shrink-0 mt-0.5" src="{self.LOGO_URL}"/>
            </div>
            <!-- List Content -->
            <div class="w-full flex flex-col justify-start pl-4 pr-4">
              <div class="space-y-6 text-left select-none w-full max-w-none">
                {summary_items_html}
              </div>
            </div>
          </div>
          <div class="absolute bottom-4 left-1/2 -translate-x-1/2 text-center w-full max-w-200">
            <span class="text-[16px] text-black font-normal">
              {copyright_text}
            </span>
          </div>
          <div class="absolute right-0 bottom-0 w-24 h-24 bg-rikkei-red z-30" style="clip-path: polygon(100% 0, 0 100%, 100% 100%)">
            <span class="absolute text-white font-montserrat font-bold text-[18px] select-none z-40" style="right: 14px; bottom: 10px;">{page_counter}</span>
          </div>
        </section>
      </div>""")

        full_html = f"""<!DOCTYPE html>
<html class="scroll-smooth" lang="vi">
<head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
  <title>{clean_session_title} — Rikkei Master Presentation</title>
  <!-- Google Fonts -->
  <link href="https://fonts.googleapis.com" rel="preconnect"/>
  <link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Montserrat:wght@400;500;700;800&family=Fira+Code:wght@400;500;600&display=swap" rel="stylesheet"/>
  <!-- Phosphor Icons -->
  <script src="https://unpkg.com/@phosphor-icons/web"></script>
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          colors: {{
            rikkei: {{
              red: "#be111c",
              darkred: "#90000a",
              dark: "#0f172a",
              bgDark: "#0a0a0f",
              cardDark: "#13131f",
              borderDark: "rgba(255, 255, 255, 0.08)",
            }},
          }},
          fontFamily: {{
            sans: ["Montserrat", "sans-serif"],
            mono: ["Fira Code", "monospace"],
          }},
        }},
      }},
    }};
  </script>
  <!-- Highlight.js for Code Highlighting -->
  <link href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/vs.min.css" id="hljs-theme" rel="stylesheet"/>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/python.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/bash.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/javascript.min.js"></script>
  <!-- Mermaid.js for Diagrams -->
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <script>
    mermaid.initialize({{
      startOnLoad: false,
      theme: "default",
      securityLevel: "loose",
      flowchart: {{ useMaxWidth: true, htmlLabels: true }},
    }});
  </script>
  <style>
    html {{
      height: 100vh;
      overflow: hidden !important;
      scrollbar-width: none;
      -ms-overflow-style: none;
    }}
    html::-webkit-scrollbar {{
      display: none;
    }}
    body {{
      margin: 0;
      height: 100vh;
      overflow: hidden !important;
      background-color: #ffffff;
    }}
    .slide-wrapper {{
      scroll-snap-align: start;
      scroll-snap-stop: always;
      height: 100vh;
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      box-sizing: border-box;
    }}
    .slide-card {{
      width: 100% !important;
      height: 100% !important;
      box-shadow: none !important;
      border-radius: 0px !important;
      border: none !important;
    }}
    pre, pre code {{
      background-color: #f8fafc !important;
      color: #0f172a !important;
      border: none !important;
      white-space: pre-wrap !important;
      word-wrap: break-word !important;
      overflow-x: hidden !important;
    }}
    pre code.hljs {{
      background: transparent !important;
      color: #0f172a !important;
    }}
    .hljs-keyword {{
      color: #be111c !important;
      font-weight: 700 !important;
    }}
    .hljs-string {{
      color: #15803d !important;
    }}
    .hljs-number {{
      color: #ea580c !important;
    }}
    .hljs-built_in, .hljs-name, .hljs-title {{
      color: #1d4ed8 !important;
    }}
    .hljs-comment {{
      color: #64748b !important;
      font-style: italic !important;
    }}
    pre code {{
      font-family: "Fira Code", "JetBrains Mono", monospace !important;
      font-size: 13px !important;
      line-height: 1.55 !important;
    }}
    .bento-card {{
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .bento-card:hover {{
      transform: translateY(-2px);
    }}
  </style>
</head>
<body class="font-sans antialiased text-slate-900 bg-white">
  <!-- Main Content Slides Container -->
  <div id="slides-container" class="w-full h-full overflow-y-auto scroll-smooth relative" style="scroll-snap-type: y mandatory;">
    <div class="w-full flex flex-col">
{"".join(slide_wrappers_html)}
    </div>
  </div>
  <script>
    document.addEventListener("DOMContentLoaded", () => {{
      if (window.hljs) {{
        hljs.highlightAll();
      }}
      if (window.mermaid) {{
        try {{ mermaid.run(); }} catch(e) {{}}
      }}

      const container = document.getElementById("slides-container");
      if (!container) return;

      // 1. Restore slide position from URL hash on load (e.g. #slide-3 or #3)
      function restoreSlideFromHash() {{
        const hash = window.location.hash;
        if (hash) {{
          const match = hash.match(/#slide-(\\d+)/i) || hash.match(/#(\\d+)/i);
          if (match) {{
            const pageNum = parseInt(match[1], 10);
            const targetSlide = document.getElementById("slide-" + pageNum);
            if (targetSlide) {{
              setTimeout(() => {{
                targetSlide.scrollIntoView({{ behavior: "instant", block: "start" }});
              }}, 50);
            }}
          }}
        }}
      }}

      restoreSlideFromHash();

      // 2. Dynamic Scroll Observer: Sync current slide to URL hash as user scrolls
      let isScrollingTimer = null;
      container.addEventListener("scroll", () => {{
        if (isScrollingTimer) clearTimeout(isScrollingTimer);
        isScrollingTimer = setTimeout(() => {{
          const slideHeight = window.innerHeight;
          const currentSlideIdx = Math.round(container.scrollTop / slideHeight);
          const activeSlide = container.querySelectorAll(".slide-wrapper")[currentSlideIdx];
          if (activeSlide) {{
            const pageNum = activeSlide.id ? activeSlide.id.replace("slide-", "") : (currentSlideIdx + 1);
            const newHash = "#slide-" + pageNum;
            if (window.location.hash !== newHash) {{
              history.replaceState(null, "", newHash);
            }}
          }}
        }}, 100);
      }});
    }});

    window.addEventListener("keydown", (e) => {{
      const container = document.getElementById("slides-container");
      if (!container) return;
      const slideHeight = window.innerHeight;
      if (e.key === "ArrowDown" || e.key === "PageDown" || e.key === " ") {{
        e.preventDefault();
        container.scrollBy({{ top: slideHeight, behavior: "smooth" }});
      }} else if (e.key === "ArrowUp" || e.key === "PageUp") {{
        e.preventDefault();
        container.scrollBy({{ top: -slideHeight, behavior: "smooth" }});
      }} else if (e.key === "Home") {{
        e.preventDefault();
        container.scrollTo({{ top: 0, behavior: "smooth" }});
      }} else if (e.key === "End") {{
        e.preventDefault();
        container.scrollTo({{ top: container.scrollHeight, behavior: "smooth" }});
      }}
    }});
  </script>
</body>
</html>"""
        return full_html

    def generate_deck_html(self, lesson_title: str, module_name: str, scenes: List[Dict[str, Any]], lessons_data: Optional[List[Dict[str, Any]]] = None, core_ssot: Optional[Dict[str, Any]] = None) -> str:
        """Lesson deck wrapper delegates to generate_session_deck_html."""
        clean_title = re.sub(r'^(Session\s*\d+\s*[\:\-]?\s*Lesson\s*\d+\s*[\:\-]?\s*)+', '', lesson_title, flags=re.IGNORECASE).strip()
        if not lessons_data:
            lessons_data = [{
                "lesson_id": "Lesson 01",
                "lesson_title": clean_title,
                "scenes": scenes
            }]
        return self.generate_session_deck_html(session_title=clean_title, module_name=module_name, lessons_data=lessons_data, core_ssot=core_ssot)

    def generate_deck_pptx(self, lesson_title: str, module_name: str, scenes: List[Dict[str, Any]], output_path: Optional[str] = None, lessons_data: Optional[List[Dict[str, Any]]] = None, core_ssot: Optional[Dict[str, Any]] = None) -> bytes:
        """Generates native Microsoft PowerPoint (.pptx) deck delegating to PPTXGeneratorAgent."""
        from agents.pptx_generator_agent import pptx_generator_agent
        clean_title = re.sub(r'^(Session\s*\d+\s*[\:\-]?\s*Lesson\s*\d+\s*[\:\-]?\s*)+', '', lesson_title, flags=re.IGNORECASE).strip()
        if not lessons_data:
            lessons_data = [{
                "lesson_id": "Lesson 01",
                "lesson_title": clean_title,
                "scenes": scenes
            }]
        return pptx_generator_agent.generate_deck_pptx(session_title=clean_title, module_name=module_name, lessons_data=lessons_data, output_path=output_path, core_ssot=core_ssot)


slide_generator_agent = SlideGeneratorAgent()

