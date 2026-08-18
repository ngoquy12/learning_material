# agents/classroom_lecture_generator_agent.py
"""
agents/classroom_lecture_generator_agent.py

Tác nhân tạo Bài giảng trên lớp dạng HTML (Classroom Lecture Presentation Agent)
================================================================================
Chuẩn hóa cấu trúc Bài giảng trên lớp theo Rikkei Academy Golden Standard:
- Sinh file HTML tương tác hoàn chỉnh: Session XX/Bài giảng trên lớp/slides.html
- Layout Bento Grid hiện đại, Tailwind CSS, Phosphor Icons, Mermaid.js v10, Highlight.js
- Triết lý review 2h trên lớp: Khối bên trái là lý thuyết cốt lõi (2-3 thẻ tinh gọn),
  khối bên phải là live code demo & runtime trace trực quan.
- Kiến trúc Generic Base đa môn học (Zero hardcoding): Python, Java, C++, Web JS, SQL, Git, Linux, Docker, etc.
"""

from __future__ import annotations

import os
import re
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from core.llm import call_llm
from core.skills import load_skill_content


class ClassroomLectureGeneratorAgent:
    """
    Classroom Lecture Generator Agent:
    Compiles a complete Master HTML Presentation Deck and Interactive Visualizer Dashboard
    for all lessons in a Session, strictly matching the classroom_lecture_generator skill.
    Saves output files to: Session XX/Bài giảng trên lớp/slides.html and Visualizer/index.html.
    """

    LOGO_URL = "https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png"

    def __init__(self):
        pass

    def sanitize_slide_text(self, text: str) -> str:
        """
        Enforces pedagogical language rules:
        1. Forbids AI/academic buzzwords ('thách thức kỹ thuật', 'phân tích thực tế', etc.)
        2. Strips hyperbolic words ('nhất', 'quá', 'vô cùng', 'tuyệt vời', 'bậc nhất', 'triệt để', 'khám phá', 'khai phá')
        3. Enforces Sentence Case (capitalizes first letter & proper technical terms, lowercase rest).
        """
        if not text:
            return ""

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

        hyperboles = [
            r"\bnhất\b", r"\bquá\b", r"\bvô cùng\b", r"\btuyệt vời\b", r"\bbậc nhất\b", r"\btriệt để\b",
        ]
        for pattern in hyperboles:
            text = re.sub(pattern, "", text, flags=re.IGNORECASE)

        text = re.sub(r"\s+", " ", text).strip()

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
        """Clean raw identifier/snake_case titles into synchronized formatted Vietnamese title strings."""
        if not text:
            return ""
        clean = text.strip()
        # Strip lesson prefixes (e.g. Lesson 01 - , Bài 01 - )
        clean = re.sub(r'^\s*(?:Session\s*\d+|Lesson\s*\d+|Bài\s*\d+|\[\d+\.\d+\]|\d+\.)\s*[\:\-]?\s*', '', clean, flags=re.IGNORECASE).strip()
        
        # If snake_case identifier
        if '_' in clean and ' ' not in clean:
            words = clean.split('_')
            clean_words = []
            for w in words:
                w_lower = w.lower()
                if w_lower in ['py', 'pvm', 'cli', 'api', 'http', 'crud', 'sql', 'orm', 'json', 'url', 'id', 'vs', 'code', 'wasm', 'git', 'vcs', 'pr', 'ui', 'ux', 'es6', 'v8', 'node', 'js']:
                    clean_words.append(w.upper())
                elif w_lower in ['va']:
                    clean_words.append("và")
                else:
                    clean_words.append(w.capitalize())
            clean = " ".join(clean_words)
            
        clean = re.sub(r'\s+', ' ', clean).strip()
        return clean

    def extract_session_summary_bullets(self, lessons_data: List[Dict[str, Any]], core_ssot: Optional[Dict[str, Any]] = None) -> List[str]:
        """Extract summary bullets directly from actual lesson scenes and content."""
        raw_bullets = []
        seen_keys = set()

        def clean_and_add(txt: str):
            if not txt:
                return
            cleaned = str(txt).strip()
            cleaned = re.sub(r'^\s*[\-\•\*\d\.]+\s*', '', cleaned).strip()
            cleaned = re.sub(r'<[^>]+>', '', cleaned).strip()
            cleaned = re.sub(r'^\s*(Nguyên lý|Quy chuẩn|Phòng tránh|Chuẩn hóa|Bẫy lỗi|Gotchas|Lưu ý)\s*[\&A-Za-z\s]*\:\s*', '', cleaned, flags=re.IGNORECASE).strip()
            cleaned = re.sub(r'\.+$', '', cleaned) + '.'

            words = cleaned.split()
            if len(words) > 28:
                cleaned = " ".join(words[:28]) + "..."

            key = cleaned.lower()[:30]
            if len(cleaned) > 10 and key not in seen_keys:
                seen_keys.add(key)
                raw_bullets.append(cleaned)

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

        if len(raw_bullets) < 3 and core_ssot and isinstance(core_ssot, dict):
            concepts = core_ssot.get("concepts")
            if isinstance(concepts, dict):
                for cname, cdesc in concepts.items():
                    clean_and_add(f"{cname}: {cdesc}")
            elif isinstance(concepts, list):
                for c in concepts:
                    clean_and_add(str(c))

        if len(raw_bullets) < 3:
            for l_data in lessons_data:
                l_title = l_data.get("lesson_title") or ""
                clean_lt = self.clean_title_string(l_title)
                clean_lt = re.sub(r'^\s*(Session\s*\d+|Lesson\s*\d+|Bài\s*\d+|\[\d+\.\d+\]|\d+\.)\s*[\:\-]?\s*', '', clean_lt, flags=re.IGNORECASE).strip()
                clean_lt = re.sub(r'^(Session\s*\d+\s*[\:\-]?\s*)+', '', clean_lt, flags=re.IGNORECASE).strip()
                if clean_lt:
                    clean_and_add(f"Thực hành thành thạo: {clean_lt}")

        return raw_bullets[:4]

    def _render_scene_content_html(self, scene: Dict[str, Any], clean_stitle: str, is_cli_or_tooling: bool = False) -> str:
        """Renders inner HTML slide content matching Bento Grid layout archetypes."""
        layout_type = str(scene.get("layout_type") or "").upper()
        
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

        # 1. IMAGE EXPLAINER LAYOUT
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

        # 2. MERMAID DIAGRAM LAYOUT
        elif "MERMAID" in layout_type or mermaid_code:
            clean_mermaid = mermaid_code.strip()
            return f"""
          <div class="w-full flex justify-center bg-slate-50 p-6 rounded-xl border border-slate-200 mt-9 mb-auto items-center h-fit">
            <div class="mermaid w-full max-w-4xl scale-105">
              {clean_mermaid}
            </div>
          </div>
"""

        # 3. CODE EXPLAINER LAYOUT
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

        # 4. GOOD VS BAD COMPARISON LAYOUT
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

        # 5. DEFAULT 2-COLUMN BENTO GRID CARDS LAYOUT
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
        """Master HTML Lecture Deck Compiler for 1 Session matching slide_result/index.html."""
        current_year = datetime.now().year
        copyright_text = f"© {current_year} By Rikkei Education - All rights reserved."

        clean_session_title = self.clean_title_string(session_title)
        clean_session_title = re.sub(r'^(Session\s*\d+\s*[\:\-]?\s*Lesson\s*\d+\s*[\:\-]?\s*)+', '', clean_session_title, flags=re.IGNORECASE).strip()
        clean_session_title = re.sub(r'^(Session\s*\d+\s*[\:\-]\s*)+', r'\1', clean_session_title, flags=re.IGNORECASE).strip()
        
        m_sess = re.search(r'^(Session\s*\d+)\s*[:-]?\s*(.*)', clean_session_title, re.IGNORECASE)
        if m_sess:
            session_tag_text = m_sess.group(1).strip()
            main_title_text = m_sess.group(2).strip()
        else:
            session_tag_text = "Session 01"
            main_title_text = clean_session_title

        clean_module_name = module_name.strip()
        if not clean_module_name or clean_module_name.upper() in ["PYTHON", "GIT", "WEB", "IT"]:
            clean_module_name = "Chương trình Đào tạo Công nghệ Thông tin"

        ts_lower = (session_title + " " + module_name).lower()
        is_cli_or_tooling = any(k in ts_lower for k in ["git", "vcs", "terminal", "cli", "bash", "docker", "agile", "scrum", "uml", "figma", "ui", "design"])

        slide_wrappers_html = []

        # ── 1. COVER SLIDE ─────────────────────────────
        slide_wrappers_html.append(f"""
      <!-- Slide 0: Cover Slide -->
      <div class="slide-wrapper" id="slide-1" data-slide-index="0">
        <section class="slide-card relative bg-white border border-slate-200 rounded-2xl flex flex-col justify-between p-16 overflow-hidden">
          <div class="absolute left-0 top-1/2 -translate-y-1/2 w-12 h-40 bg-rikkei-red" style="clip-path: polygon(0 0, 0 100%, 100% 50%)"></div>
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
          <div class="absolute bottom-4 left-1/2 -translate-x-1/2 flex flex-col items-center gap-3 w-full max-w-200 text-center">
            <img alt="Rikkei Academy Logo" class="h-10 object-contain" src="{self.LOGO_URL}"/>
            <span class="text-[16px] text-black font-normal">
              {copyright_text}
            </span>
          </div>
          <div class="absolute right-0 bottom-0 w-24 h-24 bg-rikkei-red z-30" style="clip-path: polygon(100% 0, 0 100%, 100% 100%)">
            <span class="absolute text-white font-montserrat font-bold text-[18px] select-none z-40" style="right: 14px; bottom: 10px;">1</span>
          </div>
        </section>
      </div>""")

        # ── 2. AGENDA SLIDE ────────────────────────────
        agenda_items_html = ""
        agenda_index = 1
        for l_data in lessons_data:
            l_title = l_data.get("lesson_title") or f"Bài học {agenda_index}"
            clean_l_title = self.clean_title_string(l_title)
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
            <div class="flex justify-between items-start select-none shrink-0 mb-9 w-full">
              <div class="text-[36px] font-montserrat font-extrabold text-rikkei-red leading-none">
                NỘI DUNG BÀI HỌC
              </div>
              <img alt="Rikkei Academy Logo" class="h-10 object-contain shrink-0 mt-0.5" src="{self.LOGO_URL}"/>
            </div>
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

        # ── 3..N. CONTENT SLIDES ─────────────────────────
        page_counter = 3
        slide_wrapper_idx = 2

        for l_idx, l_data in enumerate(lessons_data, 1):
            l_title = l_data.get("lesson_title") or f"Bài học {l_idx}"
            clean_l_title = self.clean_title_string(l_title)
            clean_l_title = re.sub(r'^\s*(Session\s*\d+|Lesson\s*\d+|Bài\s*\d+|\[\d+\.\d+\]|\d+\.)\s*[\:\-]?\s*', '', clean_l_title, flags=re.IGNORECASE).strip()
            clean_l_title = re.sub(r'^(Session\s*\d+\s*[\:\-]?\s*)+', '', clean_l_title, flags=re.IGNORECASE).strip()

            scenes = l_data.get("scenes", [])
            for s_idx, scene in enumerate(scenes, 1):
                raw_stitle = scene.get("action_title") or scene.get("short_title") or scene.get("scene_title") or f"Chủ đề {s_idx}"
                clean_stitle = self.clean_title_string(raw_stitle)
                clean_stitle = re.sub(r'^\s*(\[\d+\.\d+\]|\d+\.)\s*', '', clean_stitle).strip()
                clean_stitle = re.sub(r'\s+(Trong|Dành cho|Với)\s+.*$', '', clean_stitle, flags=re.IGNORECASE).strip()
                
                main_large_title = f"{l_idx}. {clean_l_title}"
                inner_content = self._render_scene_content_html(scene, clean_stitle, is_cli_or_tooling=is_cli_or_tooling)

                slide_wrappers_html.append(f"""
      <!-- Slide {slide_wrapper_idx}: Content Slide -->
      <div class="slide-wrapper" id="slide-{page_counter}" data-slide-index="{slide_wrapper_idx}" data-lesson-id="lesson-{l_idx}">
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

        # ── 4. SUMMARY SLIDE ──────────────────────────────
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
            <div class="flex justify-between items-start select-none shrink-0 mb-9 w-full">
              <div class="text-[36px] font-montserrat font-extrabold text-rikkei-red leading-none">
                TỔNG KẾT BÀI HỌC
              </div>
              <img alt="Rikkei Academy Logo" class="h-10 object-contain shrink-0 mt-0.5" src="{self.LOGO_URL}"/>
            </div>
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

        template_file = Path("templates/slide_template.html")
        if template_file.exists():
            template_content = template_file.read_text(encoding="utf-8")
            nav_links_list = []
            current_slide_idx = 2
            for idx, l_data in enumerate(lessons_data, 1):
                l_title = l_data.get("lesson_title") or f"Bài học {idx}"
                clean_l_title = self.clean_title_string(l_title)
                clean_l_title = re.sub(r'^\s*(Session\s*\d+|Lesson\s*\d+|Bài\s*\d+|\[\d+\.\d+\]|\d+\.)\s*[\:\-]?\s*', '', clean_l_title, flags=re.IGNORECASE).strip()
                
                nav_links_list.append(f"""
          <a id="nav-lesson-{idx}" href="#slide-{current_slide_idx + 1}" class="hover:text-rikkei-red transition-all border-b-2 border-transparent pb-1 text-slate-600">
            {clean_l_title}
          </a>""")
                num_scenes = len(l_data.get("scenes", [])) or 3
                current_slide_idx += num_scenes
                
            nav_links_html = "".join(nav_links_list)
            
            full_html = template_content
            full_html = full_html.replace("{{SESSION_TITLE}}", f"{clean_session_title} — Rikkei Master Presentation")
            full_html = full_html.replace("{{MODULE_NAME}}", clean_module_name)
            full_html = full_html.replace("{{NAV_LINKS}}", nav_links_html)
            full_html = full_html.replace("{{SLIDES_CONTENT}}", "".join(slide_wrappers_html))
            
            return full_html
        else:
            raise FileNotFoundError("Master slide template file not found at templates/slide_template.html")

    def _get_icon_for_topic(self, topic: str, tech_stack: str = "") -> str:
        """Dynamically picks a Phosphor icon class based on topic keywords."""
        t_lower = topic.lower()
        if any(k in t_lower for k in ["toán tử", "operator", "tính toán", "biểu thức"]):
            return "ph-calculator"
        if any(k in t_lower for k in ["so sánh", "comparison", "equal", "logic", "boolean"]):
            return "ph-scales"
        if any(k in t_lower for k in ["điều kiện", "rẽ nhánh", "if", "else", "switch"]):
            return "ph-git-fork"
        if any(k in t_lower for k in ["vòng lặp", "loop", "for", "while"]):
            return "ph-arrows-clockwise"
        if any(k in t_lower for k in ["hàm", "function", "scope", "arrow"]):
            return "ph-brackets-curly"
        if any(k in t_lower for k in ["mảng", "array", "list", "danh sách"]):
            return "ph-list-numbers"

    def _derive_unified_session_scenario(self, session_title: str, tech_stack: str) -> str:
        """
        Establishes ONE unified concrete real-world business domain scenario
        for all lessons in the session to maintain pedagogical consistency (Directive 16).
        """
        st_lower = (session_title or "").lower()
        if any(k in st_lower for k in ["toán tử", "operator", "số học", "gán gộp", "tính toán"]):
            return "Hệ thống Giỏ hàng & Thanh toán Đơn hàng E-Commerce (Shopee/Tiki Checkout)"
        elif any(k in st_lower for k in ["biến", "variable", "nhập xuất", "console", "kiểu dữ liệu", "primitive"]):
            return "Hệ thống Đăng ký & Quản lý Hồ sơ Khách hàng Trực tuyến"
        elif any(k in st_lower for k in ["điều kiện", "rẽ nhánh", "if", "else", "switch", "ternary"]):
            return "Hệ thống Phân loại Khách hàng & Xét duyệt Đơn vay Tín dụng Ngân hàng"
        elif any(k in st_lower for k in ["vòng lặp", "loop", "for", "while"]):
            return "Hệ thống Quản lý Kho hàng & Tự động Xử lý Danh mục Sản phẩm"
        elif any(k in st_lower for k in ["mảng", "array", "list", "crud"]):
            return "Hệ thống Quản lý Hồ sơ Nhân sự & Đánh giá KPI Doanh nghiệp"
        elif any(k in st_lower for k in ["hàm", "function", "scope"]):
            return "Hệ thống Xử lý Giao dịch Thanh toán Đa cổng (Payment Gateway Integration)"
        elif any(k in st_lower for k in ["dom", "event", "giao diện", "ui"]):
            return "Giao diện Bảng điều khiển Quản trị Doanh nghiệp (Admin Dashboard)"
        elif any(k in st_lower for k in ["async", "promise", "fetch", "api"]):
            return "Hệ thống Đồng bộ Dữ liệu Thời tiết & Tỷ giá Hối đoái Quốc tế"
        else:
            return "Hệ thống Vận hành Dịch vụ Trực tuyến Doanh nghiệp"

    def _find_pm_syllabus_for_session_and_lesson(
        self,
        session_dir: Optional[Path],
        session_title: str,
        lesson_title: str
    ) -> Dict[str, Any]:
        """
        Extracts ground-truth curriculum metadata from PM_*.md or syllabus files.
        Returns: {
            "curriculum_details": "...",
            "curriculum_goals": "...",
            "forbidden_scope": "...",
            "learned_prerequisites": "..."
        }
        """
        default_res = {
            "curriculum_details": "",
            "curriculum_goals": "",
            "forbidden_scope": "",
            "learned_prerequisites": ""
        }
        if not session_dir:
            return default_res

        search_dirs = [session_dir.parent, session_dir, Path("output/pms")]
        pm_files = []
        for d in search_dirs:
            if d and d.exists():
                for f in d.glob("**/PM_*.md"):
                    if f.is_file() and f not in pm_files:
                        pm_files.append(f)

        clean_lt = self.clean_title_string(lesson_title).lower()
        clean_st = self.clean_title_string(session_title).lower()

        for pm_path in pm_files:
            try:
                content = pm_path.read_text(encoding="utf-8")
                for line in content.splitlines():
                    if "|" in line:
                        parts = [p.strip() for p in line.split("|")]
                        if len(parts) >= 8:
                            row_text = line.lower()
                            if any(w in row_text for w in clean_lt.split() if len(w) > 3) or clean_st in row_text:
                                return {
                                    "curriculum_details": parts[6] if len(parts) > 6 else "",
                                    "curriculum_goals": parts[7] if len(parts) > 7 else "",
                                    "forbidden_scope": parts[8] if len(parts) > 8 else "",
                                    "learned_prerequisites": parts[9] if len(parts) > 9 else ""
                                }
            except Exception:
                continue

        return default_res

    def _infer_scope_boundary_rules(
        self,
        session_title: str,
        tech_stack: str,
        pm_syllabus: Dict[str, Any]
    ) -> str:
        """
        Infers strict knowledge scope boundary and forbidden/allowed constructs
        to prevent concept leakage into earlier sessions.
        """
        st_lower = (session_title or "").lower()
        forbidden_pm = pm_syllabus.get("forbidden_scope", "")
        learned_pm = pm_syllabus.get("learned_prerequisites", "")

        m = re.search(r'session\s*(\d+)', st_lower)
        sess_num = int(m.group(1)) if m else 99

        if sess_num <= 5:
            scope_desc = (
                "STRICT KNOWLEDGE SCOPE BOUNDARY (Sessions 01-05):\n"
                "- FORBIDDEN CONSTRUCTS: DO NOT declare functions (`function name(...)`, `def func(...)`), "
                "DO NOT use `if/else` or `switch-case` statements, DO NOT use loops (`for`, `while`), "
                "DO NOT use classes/OOP, DO NOT use DOM APIs or `Math.round`/`Number.isNaN` utilities.\n"
                "- MANDATORY CONSTRUCTS: Use ONLY direct sequential variable declarations (`const`, `let`), "
                "direct operator expressions, and standard output (`console.log(...)` or `print(...)`).\n"
            )
        elif sess_num <= 7:
            scope_desc = (
                "STRICT KNOWLEDGE SCOPE BOUNDARY (Sessions 06-07):\n"
                "- FORBIDDEN CONSTRUCTS: DO NOT use loops (`for`, `while`), arrays, functions, classes, DOM, async.\n"
                "- ALLOWED CONSTRUCTS: Variable declarations, operators, `if-else`, `switch-case`, ternary `? :`, console.log.\n"
            )
        else:
            scope_desc = "Adhere strictly to the session's level of advancement.\n"

        if forbidden_pm:
            scope_desc += f"- PM Matrix Restrictions: {forbidden_pm}\n"
        if learned_pm:
            scope_desc += f"- PM Matrix Learned Scope: {learned_pm}\n"

        return scope_desc

    def _extract_concise_topic_name(self, title: str) -> str:
        """Extracts a concise, punchy topic name for titles, sidebar pills, and badges without text bloat."""
        clean = self.clean_title_string(title)
        clean = re.sub(r'^\s*(Session\s*\d+|Lesson\s*\d+|Bài\s*\d+|\[\d+\.\d+\]|\d+\.)\s*[\:\-]?\s*', '', clean, flags=re.IGNORECASE).strip()
        clean = re.sub(r'^(?:Tìm hiểu|Giới thiệu|Khái niệm về|Khái niệm|Tổng quan về|Câu lệnh|Biểu thức)\s+', '', clean, flags=re.IGNORECASE).strip()
        words = clean.split()
        if len(words) > 7:
            clean = " ".join(words[:7])
        return clean

    def generate_interactive_visualizer_html(
        self,
        session_title: str,
        module_name: str,
        lessons_data: List[Dict[str, Any]],
        core_ssot: Optional[Dict[str, Any]] = None,
        session_dir_path: Optional[str] = None
    ) -> str:
        """
        Builds the complete Interactive Visual Classroom Lecture Dashboard HTML.
        Renders layout (header, footer, styles, grid) via Jinja2 template (templates/classroom_lecture.html.j2),
        injecting AI-generated dynamic theory cards and interactive simulators for full cross-session synchronicity.
        """
        import jinja2

        clean_session_title = self.clean_title_string(session_title)
        clean_module_name = module_name.strip() if module_name else "Khóa học Công nghệ"
        
        session_dir = Path(session_dir_path) if session_dir_path else None
        unified_scenario = self._derive_unified_session_scenario(clean_session_title, clean_module_name)
        
        nav_items = []
        sections_data = []
        js_functions = []
        init_calls = []
        
        for idx, l_data in enumerate(lessons_data, 1):
            sec_id = f"s{idx}"
            l_title = l_data.get("lesson_title") or f"Bài học {idx}"
            clean_lt = self.clean_title_string(l_title)
            concise_nav_title = self._extract_concise_topic_name(clean_lt)
            icon = l_data.get("icon") or self._get_icon_for_topic(clean_lt, clean_module_name)
            
            nav_items.append({
                "id": sec_id,
                "title": concise_nav_title,
                "icon": icon
            })

            # Render Section Structured Content with unified scenario & scope boundary
            sec_dict = self._render_interactive_section(
                sec_id=sec_id,
                sec_num=idx,
                lesson_title=clean_lt,
                icon=icon,
                lesson_data=l_data,
                tech_stack=clean_module_name,
                session_title=clean_session_title,
                unified_scenario=unified_scenario,
                session_dir=session_dir
            )
            sections_data.append(sec_dict)
            js_functions.append(sec_dict["js_code"])
            init_calls.append(sec_dict["init_call"])

        # Load and render Jinja2 template
        template_file = Path("templates/classroom_lecture.html.j2")
        if template_file.exists():
            template_str = template_file.read_text(encoding="utf-8")
            j2_template = jinja2.Template(template_str)
            full_html = j2_template.render(
                session_title=clean_session_title,
                module_name=clean_module_name,
                logo_url=self.LOGO_URL,
                nav_items=nav_items,
                sections=sections_data,
                client_scripts="\n\n".join(js_functions),
                init_calls="\n        ".join(init_calls),
                current_year=datetime.now().year
            )
            return full_html
        else:
            raise FileNotFoundError("Classroom lecture Jinja2 template not found at templates/classroom_lecture.html.j2")

    def _extract_knowledge_from_lesson_folder(
        self,
        session_dir: Optional[Path],
        session_title: str,
        lesson_title: str
    ) -> Dict[str, Any]:
        """
        Extracts verified knowledge bullets, gotchas, and curriculum syllabus metadata
        to guarantee 100% scope adherence and strict curriculum synchronization.
        """
        pm_meta = self._find_pm_syllabus_for_session_and_lesson(session_dir, session_title, lesson_title)
        
        bullets = []
        gotchas = []

        if session_dir and session_dir.exists():
            clean_target = self.clean_title_string(lesson_title).lower()
            matched_file = None

            for l_dir in session_dir.iterdir():
                if l_dir.is_dir() and "lesson" in l_dir.name.lower():
                    clean_dir = self.clean_title_string(l_dir.name).lower()
                    if clean_target in clean_dir or any(w in clean_dir for w in clean_target.split() if len(w) > 3):
                        for pf in [l_dir / "Bài đọc" / "reading.html", l_dir / "reading.html", l_dir / "Bài đọc" / "reading_master.md"]:
                            if pf.exists():
                                matched_file = pf
                                break
                    if matched_file:
                        break

            if matched_file and matched_file.exists():
                try:
                    content = matched_file.read_text(encoding="utf-8")
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(content, "html.parser")

                    # Extract bullets from Section 2 or core lists
                    sec2 = soup.find(id="section-2") or soup.find("section", id=lambda x: x and "2" in str(x))
                    if sec2:
                        for li in sec2.find_all("li"):
                            t = li.get_text().strip()
                            if t and len(t) > 15 and t not in bullets:
                                clean_t = re.sub(r'\s+', ' ', t)
                                bullets.append(clean_t)

                    # Extract gotchas from Section 4
                    sec4 = soup.find(id="section-4") or soup.find("section", id=lambda x: x and "4" in str(x))
                    if sec4:
                        for el in sec4.find_all(["p", "li"]):
                            t = el.get_text().strip()
                            if any(k in t.lower() for k in ["lỗi", "tránh", "lưu ý", "sai sót", "ngoại lệ", "rủi ro"]):
                                if len(t) > 20 and t not in gotchas:
                                    gotchas.append(re.sub(r'\s+', ' ', t))
                except Exception:
                    pass

        return {
            "bullets": bullets[:4] if bullets else [],
            "gotcha_text": gotchas[0] if gotchas else "",
            "pm_meta": pm_meta
        }

    def _detect_file_info_for_tech_stack(self, tech_stack: str, lesson_title: str) -> tuple[str, str]:
        """Detects the appropriate filename and language identifier for any tech stack."""
        ts_lower = (tech_stack or "").lower()
        t_lower = (lesson_title or "").lower()

        if "python" in ts_lower:
            return "main.py", "python"
        elif "java" in ts_lower and "javascript" not in ts_lower:
            return "Main.java", "java"
        elif "typescript" in ts_lower or bool(re.search(r'\bts\b', ts_lower)):
            return "app.ts", "typescript"
        elif "javascript" in ts_lower or bool(re.search(r'\bjs\b', ts_lower)) or "es6" in ts_lower:
            return "script.js", "javascript"
        elif "c++" in ts_lower or "cpp" in ts_lower:
            return "main.cpp", "cpp"
        elif "c#" in ts_lower or "csharp" in ts_lower or ".net" in ts_lower:
            return "Program.cs", "csharp"
        elif "sql" in ts_lower or "database" in ts_lower or "cơ sở dữ liệu" in ts_lower:
            return "query.sql", "sql"
        elif "git" in ts_lower or "linux" in ts_lower or "bash" in ts_lower or "docker" in ts_lower or "devops" in ts_lower:
            return "terminal.sh", "bash"
        elif "html" in ts_lower or "css" in ts_lower:
            return "index.html", "html"
        elif "php" in ts_lower:
            return "index.php", "php"
        elif "go" in ts_lower or "golang" in ts_lower:
            return "main.go", "go"
        else:
            return "script.js", "javascript"

    def _clean_and_parse_llm_json(self, raw_text: str) -> Optional[Dict[str, Any]]:
        """Robust multi-pass JSON extractor for LLM responses."""
        if not raw_text:
            return None
        cleaned = raw_text.strip()
        if "```json" in cleaned:
            cleaned = cleaned.split("```json", 1)[1].split("```", 1)[0].strip()
        elif "```" in cleaned:
            cleaned = cleaned.split("```", 1)[1].split("```", 1)[0].strip()

        # Pass 1: Standard json.loads
        try:
            return json.loads(cleaned, strict=False)
        except Exception:
            pass

        # Pass 2: Clean unescaped newlines inside string values
        try:
            # Replace control chars
            sanitized = re.sub(r'[\r\n\t]', ' ', cleaned)
            return json.loads(sanitized, strict=False)
        except Exception:
            pass

        # Pass 3: Regex match outermost JSON object
        try:
            m = re.search(r'(\{[\s\S]*\})', cleaned)
            if m:
                candidate = m.group(1)
                fixed = re.sub(r'[\x00-\x1f]', ' ', candidate)
                return json.loads(fixed, strict=False)
        except Exception:
            pass

        return None

    def _generate_section_with_llm(
        self,
        sec_id: str,
        sec_num: int,
        lesson_title: str,
        tech_stack: str,
        session_title: str,
        unified_scenario: str,
        extracted_knowledge: Dict[str, Any],
        lesson_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Uses LLM to dynamically generate concise 2-hour review lecture content for ANY subject.
        Enforces Strict Knowledge Scope Boundaries and Single Unified Real-World Scenario.
        """
        filename, lang = self._detect_file_info_for_tech_stack(tech_stack, lesson_title)
        bullets_text = "\n".join(f"- {b}" for b in extracted_knowledge.get("bullets", []))
        gotcha_text = extracted_knowledge.get("gotcha_text", "")
        pm_meta = extracted_knowledge.get("pm_meta", {})
        curriculum_details = pm_meta.get("curriculum_details", "")
        scope_rules = self._infer_scope_boundary_rules(session_title, tech_stack, pm_meta)

        system_prompt = f"""You are a Lead Curriculum & Classroom Lecture Architect at Rikkei Education.
Your task is to produce structured semantic JSON content for a 2-hour interactive classroom lecture dashboard.

CORE PEDAGOGICAL DIRECTIVES:
1. 2-HOUR REVIEW ON CLASS: The instructor only has 2 hours to review key concepts and conduct live coding demos with students.
   - Keep theory concise, focused, and practical.
   - `concept_bullets`: 2-3 concise bullet points covering 100% of the syllabus sub-topics for this lesson.
   - `gotcha_points`: 2 concise real-world gotchas/pitfalls with concrete examples.
   - DO NOT dump low-level engine minutiae (like bytecode/internal compilers) that overwhelm students.

2. MANDATORY SINGLE UNIFIED BUSINESS SCENARIO (Directive 16):
   - The entire session dashboard uses EXACTLY ONE unified scenario: '{unified_scenario}'.
   - 100% of code snippets, variables, parameter inputs, and testcase scenarios across all lessons in this session MUST strictly belong to and expand on this scenario.

3. STRICT KNOWLEDGE SCOPE BOUNDARY (Directive 12):
{scope_rules}

4. DEDICATED MULTI-INPUT PARAMETER SEPARATION DIRECTIVE:
   - If the code demo involves multiple variables/parameters (e.g. price, quantity, voucher, shipping, VIP status):
   - ABSOLUTELY FORBIDDEN to bundle them into a single string!
   - You MUST define separate parameters in the `parameters` array with clear Vietnamese labels and IDs.

5. CONCISE, PUNCHY & MEANINGFUL TITLES (Directive E):
   - `demo_title`: Keep short & punchy under 5-8 words (e.g. "Trực quan: Tính toán Giỏ hàng", "Trực quan: So sánh Voucher & VIP", "Trực quan: Điều kiện Freeship").
   - ABSOLUTELY FORBIDDEN to append the whole session scenario description or repeat long lesson title verbatim into demo_title!

6. MODULAR MICRO-STEP DEMO STRUCTURE (Directive F):
   - Do NOT bundle all concepts into one giant monolithic 30-line code block!
   - Structure `code_snippet` into 2-3 clear, progressive, commented micro-steps (e.g. `// --- Bước 1: Khởi tạo & Phép toán cơ bản ---`, `// --- Bước 2: Thao tác gán gộp / Tăng giảm ---`, `// --- Bước 3: Đánh giá kết quả ---`).
   - `trace_steps`: Align 1-to-1 with each discrete micro-step.

OUTPUT CONTRACT:
- Return ONLY a valid JSON object matching the schema below.
- 100% of text labels, trace explanations, bullets, and gotchas MUST be in 100% Accented Vietnamese (Tiếng Việt có dấu).
"""

        concise_topic_default = self._extract_concise_topic_name(lesson_title)
        user_prompt = f"""Generate lecture section data for:
- Lesson Title: {lesson_title}
- Concise Topic Name: {concise_topic_default}
- Session Title: {session_title}
- Subject / Tech Stack: {tech_stack}
- File to simulate: {filename} ({lang})
- Mandatory Unified Scenario: {unified_scenario}
- Syllabus Sub-topics to Cover: {curriculum_details if curriculum_details else lesson_title}
- Extracted Theory Bullets from Reading:
{bullets_text if bullets_text else "N/A"}
- Extracted Gotchas:
{gotcha_text if gotcha_text else "N/A"}

JSON SCHEMA:
{{
  "concept_title": "Khái niệm & Cú pháp Cốt lõi",
  "concept_bullets": [
    "Cú pháp khai báo và bản chất kỹ thuật theo chuẩn {tech_stack}...",
    "Quy chuẩn thực thi và cơ chế hoạt động..."
  ],
  "gotcha_title": "Lưu ý & Bẫy lỗi Thường gặp",
  "gotcha_points": [
    "Bẫy lỗi thực tế sinh viên hay mắc phải khi viết code...",
    "Lưu ý kiểm tra điều kiện biên và an toàn kiểu dữ liệu..."
  ],
  "demo_title": "Trực quan: {concise_topic_default}",
  "code_snippet": "// Code sequential in 2-3 modular steps with comment dividers",
  "parameters": [
    {{"id": "param1", "label": "Nhãn tham số 1 (VNĐ)", "type": "number", "default": "120000"}},
    {{"id": "param2", "label": "Nhãn tham số 2 (món)", "type": "number", "default": "2"}}
  ],
  "scenarios": [
    {{
      "name": "1. Trường hợp Chuẩn (Standard)",
      "param_values": {{"param1": "120000", "param2": "2"}},
      "trace_steps": [
        "1. Bước 1: Tính toán tiền hàng cơ bản...",
        "2. Bước 2: Áp dụng chiết khấu và gán gộp...",
        "3. Bước 3: Đánh giá kết quả tổng thanh toán"
      ],
      "result_value": "Kết quả chuẩn",
      "status_badge": "Thành công"
    }},
    {{
      "name": "2. Trường hợp Biên (Edge Case)",
      "param_values": {{"param1": "120000", "param2": "10"}},
      "trace_steps": [
        "1. Bước 1: Khởi tạo giá trị tại điểm biên...",
        "2. Bước 2: Đánh giá điều kiện biên an toàn...",
        "3. Bước 3: Trả về kết quả biên"
      ],
      "result_value": "Kết quả biên",
      "status_badge": "Biên an toàn"
    }},
    {{
      "name": "3. Tình huống Ngoại lệ (Gotcha / Error)",
      "param_values": {{"param1": "120000", "param2": "2"}},
      "trace_steps": [
        "1. Bước 1: Phát hiện tình huống bẫy kiểu hoặc giá trị falsy...",
        "2. Bước 2: Cơ chế xử lý an toàn...",
        "3. Bước 3: Trả về kết quả cảnh báo"
      ],
      "result_value": "Kết quả cảnh báo",
      "status_badge": "Cảnh báo Lỗi"
    }}
  ]
}}
"""

        try:
            response_str = call_llm(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                json_mode=True,
                agent_name="classroom_lecture_agent",
                session_id=str(sec_id),
                lesson_id=str(sec_num)
            )

            if not response_str:
                return None

            data = self._clean_and_parse_llm_json(response_str)
            if not (isinstance(data, dict) and ("concept_bullets" in data or "knowledge_cards" in data)):
                return None

            # Render structured semantic data into presentation containers
            if "knowledge_cards" in data and isinstance(data["knowledge_cards"], list):
                knowledge_cards = data["knowledge_cards"]
            else:
                c_bullets = data.get("concept_bullets", [])
                c_title = data.get("concept_title", "Khái niệm & Cú pháp Cốt lõi")
                g_points = data.get("gotcha_points", [])
                g_title = data.get("gotcha_title", "Lưu ý & Bẫy lỗi Thường gặp")

                b_items = "".join(f"<li>{b}</li>" for b in c_bullets[:3])
                g_items = "".join(f"<p>{p}</p>" for p in g_points[:2])

                knowledge_cards = [
                    {
                        "title": c_title,
                        "icon": "ph-bold ph-lightbulb text-amber-500",
                        "badge": "KHÁI NIỆM & CÚ PHÁP",
                        "badge_style": "bg-amber-50 text-amber-700 border border-amber-200",
                        "border_color": "border-slate-200/80",
                        "content_html": f"""
                        <ul class="space-y-2 list-disc pl-4 text-slate-700">
                          {b_items}
                        </ul>
                        """
                    },
                    {
                        "title": g_title,
                        "icon": "ph-bold ph-warning-octagon text-rose-600",
                        "badge": "LƯU Ý THỰC HÀNH",
                        "badge_style": "bg-rose-50 text-rose-700 border border-rose-200",
                        "border_color": "border-rose-200 bg-rose-50/40",
                        "title_color": "text-rose-950",
                        "content_html": f"""
                        <div class="space-y-2 text-rose-950 leading-relaxed">
                          {g_items}
                        </div>
                        """
                    }
                ]

            raw_demo_title = data.get("demo_title", "")
            if not raw_demo_title or len(raw_demo_title.split()) > 9:
                demo_title = f"Trực quan: {concise_topic_default}"
            else:
                demo_title = raw_demo_title
            code_snippet = data.get("code_snippet", "")
            code_box_html = f"""<pre class="font-mono text-xs leading-relaxed whitespace-pre-wrap"><code id="{sec_id}-code-snippet">{code_snippet}</code></pre>"""

            scenarios = data.get("scenarios", [])
            if not scenarios or not isinstance(scenarios, list):
                scenarios = [
                    {
                        "name": "1. Trường hợp Chuẩn (Standard)",
                        "param_values": {},
                        "trace_steps": ["1. Khởi tạo tham số chuẩn", "2. Thực thi biểu thức", "3. Đạt kết quả mong đợi"],
                        "result_value": "Thành công",
                        "status_badge": "Thành công"
                    }
                ]

            params = data.get("parameters", [])
            opt_html = []
            for s_idx, sc in enumerate(scenarios):
                s_name = sc.get("name", f"Kịch bản {s_idx + 1}")
                opt_html.append(f'<option value="scen_{s_idx}">{s_name}</option>')

            options_str = "\n".join(opt_html)

            # Build separate dedicated controller inputs
            if params and isinstance(params, list) and len(params) > 0:
                col_span_class = f"grid-cols-1 sm:grid-cols-2 lg:grid-cols-{min(len(params), 4)}"
                param_inputs_html = []
                for p in params:
                    p_id = p.get("id", "p")
                    p_lbl = p.get("label", p_id)
                    p_type = p.get("type", "text")
                    p_def = p.get("default", "")
                    param_inputs_html.append(f"""
                  <div class="min-w-0">
                    <label class="block text-xs font-semibold text-slate-500 mb-1.5 truncate">{p_lbl}:</label>
                    <input type="{p_type}" id="{sec_id}-{p_id}" value="{p_def}" class="w-full px-3 py-2 border border-slate-200 rounded-xl font-mono text-xs focus:outline-none focus:border-rikkei-red bg-slate-50/50" oninput="run_{sec_id}_sim()" />
                  </div>""")
                
                params_grid_str = "\n".join(param_inputs_html)
                controllers_html = f"""
            <div class="space-y-3.5">
              <div class="min-w-0">
                <label class="block text-xs font-semibold text-slate-500 mb-1.5">Kịch bản Thử nghiệm (Scenario):</label>
                <select id="{sec_id}-scenario" class="w-full px-3 py-2 border border-slate-200 rounded-xl font-mono text-xs focus:outline-none focus:border-rikkei-red bg-white font-medium truncate" onchange="on_change_{sec_id}_scenario()">
                  {options_str}
                </select>
              </div>
              <div class="grid {col_span_class} gap-3">
                {params_grid_str}
              </div>
            </div>"""
            else:
                default_param = scenarios[0].get("param_value", "")
                controllers_html = f"""
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div class="min-w-0">
                <label class="block text-xs font-semibold text-slate-500 mb-1.5">Kịch bản Thử nghiệm (Scenario):</label>
                <select id="{sec_id}-scenario" class="w-full px-3 py-2 border border-slate-200 rounded-xl font-mono text-xs focus:outline-none focus:border-rikkei-red bg-white font-medium truncate" onchange="run_{sec_id}_sim()">
                  {options_str}
                </select>
              </div>
              <div class="min-w-0">
                <label class="block text-xs font-semibold text-slate-500 mb-1.5">Giá trị Tham số (Input Value):</label>
                <input type="text" id="{sec_id}-val" value="{default_param}" class="w-full px-3 py-2 border border-slate-200 rounded-xl font-mono text-xs focus:outline-none focus:border-rikkei-red bg-slate-50/50" oninput="run_{sec_id}_sim()" />
              </div>
            </div>"""

            # Build JS simulation map
            js_scen_map = {}
            for s_idx, sc in enumerate(scenarios):
                pv = sc.get("param_values") if "param_values" in sc else {"val": sc.get("param_value", "")}
                js_scen_map[f"scen_{s_idx}"] = {
                    "params": pv,
                    "val": sc.get("param_value", ""),
                    "trace": "".join(f"<div class='text-slate-400'>> {st}</div>" for st in sc.get("trace_steps", [])),
                    "res": sc.get("result_value", "Success"),
                    "badge": sc.get("status_badge", "Thành công")
                }

            scen_json_str = json.dumps(js_scen_map, ensure_ascii=False)

            js_code = f"""
      const {sec_id}_scenMap = {scen_json_str};

      function on_change_{sec_id}_scenario() {{
        const scenSelect = document.getElementById("{sec_id}-scenario");
        if (!scenSelect) return;
        const scenData = {sec_id}_scenMap[scenSelect.value] || {sec_id}_scenMap["scen_0"];
        if (scenData && scenData.params) {{
          for (const [k, v] of Object.entries(scenData.params)) {{
            const el = document.getElementById("{sec_id}-" + k);
            if (el) el.value = v;
          }}
        }}
        run_{sec_id}_sim();
      }}

      function run_{sec_id}_sim() {{
        const scenSelect = document.getElementById("{sec_id}-scenario");
        const traceBox = document.getElementById("{sec_id}-trace-box");
        const resVal = document.getElementById("{sec_id}-res-val");
        const resBadge = document.getElementById("{sec_id}-res-badge");

        if (!scenSelect || !traceBox || !resVal || !resBadge) return;

        const currentScen = scenSelect.value;
        const scenData = {sec_id}_scenMap[currentScen] || {sec_id}_scenMap["scen_0"];

        traceBox.innerHTML = scenData.trace;
        resVal.innerText = scenData.res;
        resBadge.innerText = scenData.badge;
        resBadge.className = "font-mono text-xs px-2.5 py-1 " + (currentScen === "scen_2" ? "bg-rose-50 text-rose-700 border border-rose-200" : currentScen === "scen_1" ? "bg-amber-50 text-amber-700 border border-amber-200" : "bg-emerald-50 text-emerald-700 border border-emerald-200") + " rounded-full font-semibold";
      }}"""

            first_trace = "".join(f"<div class='text-slate-400'>> {st}</div>" for st in scenarios[0].get("trace_steps", []))

            return {
                "knowledge_cards": knowledge_cards,
                "sim_title": demo_title,
                "snippet_filename": filename,
                "controllers_html": controllers_html,
                "code_box_html": code_box_html,
                "initial_trace_html": first_trace if first_trace else f"<div class='text-slate-400'>> Sẵn sàng thực thi mã nguồn {filename}.</div>",
                "default_res_val": scenarios[0].get("result_value", "Success"),
                "default_res_badge": scenarios[0].get("status_badge", "Thành công"),
                "js_code": js_code,
                "init_call": f"run_{sec_id}_sim();"
            }

        except Exception as e:
            print(f"  [Classroom Lecture Agent] LLM parse error: {e}")

        return None

    def _build_generic_multi_subject_section(
        self,
        sec_id: str,
        sec_num: int,
        lesson_title: str,
        icon: str,
        tech_stack: str,
        session_title: str,
        unified_scenario: str,
        extracted_knowledge: Dict[str, Any],
        lesson_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Universal Generic Multi-Subject Fallback Base (Zero Hardcoding).
        Generates domain-aware, scope-safe theory cards and interactive simulations
        matching the specific topic category (Arithmetic, Comparison, Logic, etc.).
        """
        filename, lang = self._detect_file_info_for_tech_stack(tech_stack, lesson_title)
        clean_tech = tech_stack.split(",")[0].strip() if "," in tech_stack else tech_stack
        lt_lower = lesson_title.lower()
        pm_meta = extracted_knowledge.get("pm_meta", {})
        curriculum_details = pm_meta.get("curriculum_details", "")

        # 1. Topic Category Recognition for Scope-Safe Pedagogical Fallback
        is_arithmetic = any(k in lt_lower for k in ["số học", "arithmetic", "gán gộp", "assignment", "toán tử số"])
        is_comparison = any(k in lt_lower for k in ["so sánh", "comparison", "equal", "strict", "==="])
        is_logic = any(k in lt_lower for k in ["logic", "ngắn mạch", "short-circuit", "boolean", "&&", "||"])

        # 2. Build Rich Theory Cards
        if is_arithmetic:
            c_bullets = [
                "Toán tử số học (+, -, *, /, %, **) thực hiện các phép toán đại số cơ bản; toán tử gán gộp (+=, -=, *=, /=) giúp cập nhật giá trị biến ngắn gọn.",
                "Toán tử tăng giảm (++ / --): Tiền tố (++x) tăng giá trị trước rồi mới trả về; Hậu tố (x++) trả về giá trị hiện tại rồi mới tăng.",
                "Thứ tự ưu tiên toán tử: Lũy thừa (**) -> Nhân / Chia / Chia lấy dư (*, /, %) -> Cộng / Trừ (+, -). Dùng ngoặc đơn () để điều khiển thứ tự."
            ]
            g_points = [
                "Bẫy ép kiểu chuỗi với '+': Nếu một trong hai toán hạng là chuỗi (String), toán tử '+' sẽ nối chuỗi thay vì cộng số (ví dụ: 10 + '5' = '105').",
                "Sai số số thực (Floating-point): Các phép tính thập phân có thể có sai số nhị phân (ví dụ: 0.1 + 0.2 = 0.30000000000000004)."
            ]
        elif is_comparison:
            c_bullets = [
                "Toán tử === (bằng nghiêm ngặt) và !== (khác nghiêm ngặt) so sánh cả giá trị và kiểu dữ liệu mà KHÔNG ép kiểu ngầm định.",
                "Toán tử so sánh quan hệ (>, <, >=, <=) dùng để kiểm tra thứ tự lớn bé giữa các giá trị số và chuỗi theo bảng mã chuẩn.",
                "Quy chuẩn lập trình ES6+: Luôn sử dụng === và !== thay cho == và != để đảm bảo tính an toàn và minh bạch tuyệt đối của mã nguồn."
            ]
            g_points = [
                "Bẫy ép kiểu ngầm định của '==': Phép so sánh lỏng lẻo có thể gây lỗi logic nguy hiểm (ví dụ: 0 == false là true, '' == 0 là true, null == undefined là true).",
                "Dữ liệu từ biểu mẫu/DOM luôn ở dạng String; so sánh '18' === 18 sẽ luôn trả về false nếu chưa ép kiểu sang Number."
            ]
        elif is_logic:
            c_bullets = [
                "Toán tử logic kết hợp biểu thức: && (AND - cả 2 đúng), || (OR - một trong hai đúng), ! (NOT - đảo ngược giá trị boolean).",
                "Cơ chế Ngắn mạch (Short-circuit): A && B dừng ngay và trả về A nếu A là Falsy; A || B dừng ngay và trả về A nếu A là Truthy.",
                "Danh sách 6 giá trị Falsy trong JavaScript: false, 0, '' (chuỗi rỗng), null, undefined, NaN. Mọi giá trị khác đều là Truthy."
            ]
            g_points = [
                "Toán tử || và && không chỉ trả về true/false mà trả về giá trị thực tế của toán hạng quyết định (ví dụ: '' || 'Khách' trả về 'Khách').",
                "Bẫy Falsy với số 0: Sử dụng || để gán giá trị mặc định có thể ghi đè nhầm số lượng 0 hợp lệ (ví dụ: quantity || 10 sẽ biến 0 thành 10)."
            ]
        else:
            bullets_raw = extracted_knowledge.get("bullets", [])
            c_bullets = bullets_raw[:3] if bullets_raw else [
                f"Nắm vững bản chất cú pháp và nguyên lý thực thi của <code>{lesson_title}</code>.",
                f"Áp dụng chuẩn quy ước đặt tên và cấu trúc mã nguồn theo tiêu chuẩn của <code>{clean_tech}</code>.",
                f"Đảm bảo xử lý đầy đủ các điều kiện biên và kiểm soát luồng dữ liệu an toàn."
            ]
            g_points = [
                extracted_knowledge.get("gotcha_text") or f"Luôn kiểm tra ràng buộc kiểu dữ liệu, các giá trị biên (null/undefined/0/rỗng) khi triển khai {lesson_title}."
            ]

        knowledge_cards = [
            {
                "title": "Khái niệm & Cú pháp Cốt lõi",
                "icon": "ph-bold ph-lightbulb text-amber-500",
                "badge": "KHÁI NIỆM & CÚ PHÁP",
                "badge_style": "bg-amber-50 text-amber-700 border border-amber-200",
                "border_color": "border-slate-200/80",
                "content_html": f"""
                <ul class="space-y-2 list-disc pl-4 text-slate-700">
                  {"".join(f"<li>{b}</li>" for b in c_bullets)}
                </ul>
                """
            },
            {
                "title": "Lưu ý & Bẫy lỗi Thường gặp",
                "icon": "ph-bold ph-warning-octagon text-rose-600",
                "badge": "LƯU Ý THỰC HÀNH",
                "badge_style": "bg-rose-50 text-rose-700 border border-rose-200",
                "border_color": "border-rose-200 bg-rose-50/40",
                "title_color": "text-rose-950",
                "content_html": f"""
                <div class="space-y-2 text-rose-950 leading-relaxed">
                  {"".join(f"<p>{p}</p>" for p in g_points)}
                </div>
                """
            }
        ]

        # 3. Topic-Specific Scope-Safe Code Demos & Interactive Simulators (Multi-Input Separation & Modular Steps)
        concise_topic = self._extract_concise_topic_name(lesson_title)
        if is_arithmetic:
            sim_title = "Trực quan: Toán tử Số học & Gán gộp (Giỏ hàng)"
            code_sample = """// --- Bước 1: Tính tiền hàng ban đầu (Số học *, +) ---
let unitPrice = 120000;
let quantity = 2;
let subtotal = unitPrice * quantity; // 120000 * 2 = 240000 VNĐ
let shippingFee = 15000;

// --- Bước 2: Áp dụng giảm giá & Cập nhật gán gộp (-=, ++) ---
subtotal -= 30000;                   // Gán gộp trừ (-= 30k) -> 210000 VNĐ
quantity++;                          // Tăng hậu tố (++) -> Số lượng: 3 món

// --- Bước 3: Đánh giá tổng thanh toán & Quay số trúng thưởng ---
let grandTotal = subtotal + shippingFee; // Tổng: 225000 VNĐ
let orderLuckyParity = 105 % 2;      // Chia lấy dư (%): 1 (Số lẻ - Trúng thưởng)
console.log(`Tổng thanh toán: ${grandTotal} VNĐ | Lượt quay: ${orderLuckyParity}`);"""
            params = [
                {"id": "price", "label": "Đơn giá (VNĐ)", "type": "number", "default": "120000"},
                {"id": "qty", "label": "Số lượng (món)", "type": "number", "default": "2"},
                {"id": "discount", "label": "Mã giảm giá (VNĐ)", "type": "number", "default": "30000"},
                {"id": "shipping", "label": "Phí ship (VNĐ)", "type": "number", "default": "15000"}
            ]
            scenarios = [
                {
                    "name": "1. Mua 2 sản phẩm (Chuẩn)",
                    "param_values": {"price": "120000", "qty": "2", "discount": "30000", "shipping": "15000"},
                    "trace_steps": [
                        "1. Bước 1: Tính tiền hàng ban đầu: 120000 * 2 = 240000 VNĐ",
                        "2. Bước 2: Áp dụng gán gộp giảm giá (-= 30000): 240000 - 30000 = 210000 VNĐ",
                        "3. Bước 3: Cộng phí ship (+ 15000) và tính dư chẵn lẻ (105 % 2 = 1)"
                    ],
                    "result_value": "225,000 VNĐ",
                    "status_badge": "Thành công"
                },
                {
                    "name": "2. Đơn hàng số lượng lớn (Biên)",
                    "param_values": {"price": "120000", "qty": "10", "discount": "100000", "shipping": "0"},
                    "trace_steps": [
                        "1. Bước 1: Tính tiền hàng số lượng 10: 120000 * 10 = 1200000 VNĐ",
                        "2. Bước 2: Áp dụng gán gộp giảm giá lớn (-= 100000): 1100000 VNĐ",
                        "3. Bước 3: Miễn phí vận chuyển (0đ) -> Tổng: 1100000 VNĐ"
                    ],
                    "result_value": "1,100,000 VNĐ",
                    "status_badge": "Biên an toàn"
                },
                {
                    "name": "3. Bẫy dữ liệu chuỗi String (Gotcha)",
                    "param_values": {"price": "120000", "qty": "2", "discount": "30000", "shipping": "15000"},
                    "trace_steps": [
                        "1. Bước 1: Biến price chứa kiểu String '120000' từ ô nhập liệu",
                        "2. Bước 2: Bẫy cộng chuỗi: '120000' + 15000 = '12000015000'",
                        "3. Bước 3: Khắc phục: Phải dùng Number(price) trước khi thực hiện phép cộng"
                    ],
                    "result_value": "Cảnh báo Nối chuỗi",
                    "status_badge": "Cảnh báo Lỗi"
                }
            ]
        elif is_comparison:
            sim_title = "Trực quan: So sánh Nghiêm ngặt (===) & Ép kiểu"
            code_sample = """// --- Bước 1: So sánh nghiêm ngặt mã Voucher (===) ---
const inputVoucher = "FREESHIP";
const isVoucherMatch = (inputVoucher === "FREESHIP");  // true (cùng kiểu String)

// --- Bước 2: Kiểm tra mức đơn hàng tối thiểu (>=) ---
const orderAmount = 250000;
const MIN_REQUIRED = 200000;
const isMinTotalReached = (orderAmount >= MIN_REQUIRED); // true

// --- Bước 3: Phân biệt Bẫy ép kiểu '==' vs '===' an toàn ---
const looseCheck = ("250000" == orderAmount);   // true (Ép kiểu ngầm nguy hiểm)
const strictCheck = ("250000" === orderAmount); // false (Kiểm tra an toàn kiểu dữ liệu)
console.log(`Voucher khớp: ${isVoucherMatch}, Đạt mức tối thiểu: ${isMinTotalReached}`);"""
            params = [
                {"id": "voucher", "label": "Mã Voucher nhập vào", "type": "text", "default": "FREESHIP"},
                {"id": "amount", "label": "Giá trị đơn hàng (VNĐ)", "type": "number", "default": "250000"},
                {"id": "tier", "label": "Hạng thành viên (ID)", "type": "text", "default": "101"}
            ]
            scenarios = [
                {
                    "name": "1. Voucher chuẩn & Đủ điều kiện (Chuẩn)",
                    "param_values": {"voucher": "FREESHIP", "amount": "250000", "tier": "101"},
                    "trace_steps": [
                        "1. Bước 1: So sánh nghiêm ngặt mã voucher: 'FREESHIP' === 'FREESHIP' -> true",
                        "2. Bước 2: So sánh quan hệ giá trị đơn: 250000 >= 200000 -> true",
                        "3. Bước 3: Kết luận: Đủ điều kiện kích hoạt miễn phí vận chuyển"
                    ],
                    "result_value": "Hợp lệ (Approved)",
                    "status_badge": "Thành công"
                },
                {
                    "name": "2. Giá trị đơn hàng sát biên 200k (Biên)",
                    "param_values": {"voucher": "FREESHIP", "amount": "200000", "tier": "101"},
                    "trace_steps": [
                        "1. Bước 1: Kiểm tra điều kiện >= tại giá trị biên: 200000 >= 200000 -> true",
                        "2. Bước 2: Mã voucher hợp lệ -> Phê duyệt thành công tại điểm biên",
                        "3. Bước 3: Xác nhận kích hoạt ưu đãi biên"
                    ],
                    "result_value": "Đạt biên (200k)",
                    "status_badge": "Biên an toàn"
                },
                {
                    "name": "3. Bẫy dữ liệu chuỗi DOM '250000' (Gotcha)",
                    "param_values": {"voucher": "FREESHIP", "amount": "250000", "tier": "101"},
                    "trace_steps": [
                        "1. Bước 1: So sánh '250000' === 250000 -> false (khác kiểu String vs Number)",
                        "2. Bước 2: So sánh '250000' == 250000 -> true (ép kiểu ngầm nguy hiểm)",
                        "3. Bước 3: Khắc phục: Sử dụng === và ép kiểu chủ động bằng Number()"
                    ],
                    "result_value": "String !== Number",
                    "status_badge": "Cảnh báo Lỗi"
                }
            ]
        elif is_logic:
            sim_title = "Trực quan: Toán tử Logic & Ngắn mạch (Freeship)"
            code_sample = """// --- Bước 1: Đánh giá điều kiện Freeship (Logic &&, ||) ---
const isVipCustomer = true;
const hasEventCoupon = false;
const orderTotal = 350000;
const isEligibleFreeShip = (isVipCustomer && hasEventCoupon) || (orderTotal >= 300000);

// --- Bước 2: Gán giá trị mặc định an toàn qua Ngắn mạch (||) ---
const inputCustomerName = ""; // Falsy value (chuỗi rỗng)
const displayName = inputCustomerName || "Khách hàng vãng lai"; // Lấy vế sau vì vế 1 là Falsy

// --- Bước 3: Kiểm tra trạng thái đơn hàng bằng toán tử NOT (!) ---
const isOrderInvalid = !isEligibleFreeShip && (orderTotal < 100000);
console.log(`Được Freeship: ${isEligibleFreeShip} | Tên hiển thị: ${displayName}`);"""
            params = [
                {"id": "isvip", "label": "Khách VIP (true/false)", "type": "select", "options": [("true", "Khách VIP (true)"), ("false", "Khách thường (false)")], "default": "true"},
                {"id": "hascoupon", "label": "Có Coupon sự kiện", "type": "select", "options": [("false", "Không có (false)"), ("true", "Có coupon (true)")], "default": "false"},
                {"id": "total", "label": "Giá trị đơn hàng (VNĐ)", "type": "number", "default": "350000"},
                {"id": "name", "label": "Tên khách nhập vào", "type": "text", "default": "", "placeholder": "(để trống = Falsy)"}
            ]
            scenarios = [
                {
                    "name": "1. Đơn hàng trên 300k được Freeship (Chuẩn)",
                    "param_values": {"isvip": "true", "hascoupon": "false", "total": "350000", "name": ""},
                    "trace_steps": [
                        "1. Bước 1: Đánh giá (true && false) -> false, vế 2: 350000 >= 300000 -> true",
                        "2. Bước 2: Biểu thức logic chung: false || true -> true (Được Freeship)",
                        "3. Bước 3: Ngắn mạch tên: '' || 'Khách hàng vãng lai' -> 'Khách hàng vãng lai'"
                    ],
                    "result_value": "Freeship: true (350k)",
                    "status_badge": "Thành công"
                },
                {
                    "name": "2. Khách VIP có Coupon dừng sớm (Biên)",
                    "param_values": {"isvip": "true", "hascoupon": "true", "total": "100000", "name": "Nguyễn Văn A"},
                    "trace_steps": [
                        "1. Bước 1: Đánh giá vế 1 (true && true) -> true",
                        "2. Bước 2: Ngắn mạch toán tử ||: JS DỪNG NGAY không cần kiểm tra vế 2",
                        "3. Bước 3: Tối ưu hiệu năng: Biểu thức lập tức trả về true"
                    ],
                    "result_value": "Short-circuit: true",
                    "status_badge": "Biên an toàn"
                },
                {
                    "name": "3. Bẫy Falsy với giá trị 0 (Gotcha)",
                    "param_values": {"isvip": "false", "hascoupon": "false", "total": "0", "name": ""},
                    "trace_steps": [
                        "1. Bước 1: Giá trị total = 0 là một giá trị Falsy trong JS",
                        "2. Bước 2: Biểu thức (0 || 50000) sẽ trả về 50000 (ghi đè nhầm số 0)",
                        "3. Bước 3: Khắc phục: Dùng Nullish Coalescing (??) hoặc kiểm tra rõ ràng"
                    ],
                    "result_value": "Bẫy Falsy (0 || 50k)",
                    "status_badge": "Cảnh báo Lỗi"
                }
            ]
        else:
            sim_title = f"Trực quan: {concise_topic}"
            code_sample = f"""// --- Bước 1: Khởi tạo giá trị cơ sở ---
const targetVal = 100;

// --- Bước 2: Thực thi biểu thức tính toán ---
const processedResult = targetVal * 2;

// --- Bước 3: Xuất kết quả đánh giá ---
console.log(`Kết quả xử lý theo tiêu chuẩn {clean_tech}: ${{processedResult}}`);"""
            params = [
                {"id": "p1", "label": "Tham số 1 (Giá trị cơ sở)", "type": "number", "default": "100"},
                {"id": "p2", "label": "Tham số 2 (Hệ số xử lý)", "type": "number", "default": "2"}
            ]
            scenarios = [
                {
                    "name": "1. Trường hợp Chuẩn (Standard)",
                    "param_values": {"p1": "100", "p2": "2"},
                    "trace_steps": [
                        "1. Bước 1: Nhận giá trị tham số đầu vào: 100",
                        "2. Bước 2: Thực thi xử lý: 100 * 2 = 200",
                        "3. Bước 3: Đạt kết quả mong đợi"
                    ],
                    "result_value": "Success (200)",
                    "status_badge": "Thành công"
                }
            ]

        # Build separated multi-input controller grid
        opt_html = [f'<option value="scen_{s_idx}">{sc["name"]}</option>' for s_idx, sc in enumerate(scenarios)]
        options_str = "\n".join(opt_html)

        param_inputs_html = []
        for p in params:
            p_id = p.get("id", "p")
            p_lbl = p.get("label", p_id)
            p_type = p.get("type", "text")
            p_def = p.get("default", "")
            p_ph = p.get("placeholder", "")
            if p_type == "select":
                opts = p.get("options", [])
                opt_str = "\n".join(f'<option value="{v}" {"selected" if v == p_def else ""}>{lbl}</option>' for v, lbl in opts)
                param_inputs_html.append(f"""
              <div class="min-w-0">
                <label class="block text-xs font-semibold text-slate-500 mb-1.5 truncate">{p_lbl}:</label>
                <select id="{sec_id}-{p_id}" class="w-full px-3 py-2 border border-slate-200 rounded-xl font-mono text-xs focus:outline-none focus:border-rikkei-red bg-white font-medium truncate" onchange="run_{sec_id}_sim()">
                  {opt_str}
                </select>
              </div>""")
            else:
                param_inputs_html.append(f"""
              <div class="min-w-0">
                <label class="block text-xs font-semibold text-slate-500 mb-1.5 truncate">{p_lbl}:</label>
                <input type="{p_type}" id="{sec_id}-{p_id}" value="{p_def}" placeholder="{p_ph}" class="w-full px-3 py-2 border border-slate-200 rounded-xl font-mono text-xs focus:outline-none focus:border-rikkei-red bg-slate-50/50" oninput="run_{sec_id}_sim()" />
              </div>""")

        col_span_class = f"grid-cols-1 sm:grid-cols-2 lg:grid-cols-{min(len(params), 4)}"
        controllers_html = f"""
        <div class="space-y-3.5">
          <div class="min-w-0">
            <label class="block text-xs font-semibold text-slate-500 mb-1.5">Kịch bản Thử nghiệm (Scenario):</label>
            <select id="{sec_id}-scenario" class="w-full px-3 py-2 border border-slate-200 rounded-xl font-mono text-xs focus:outline-none focus:border-rikkei-red bg-white font-medium truncate" onchange="on_change_{sec_id}_scenario()">
              {options_str}
            </select>
          </div>
          <div class="grid {col_span_class} gap-3">
            {"\n".join(param_inputs_html)}
          </div>
        </div>"""

        js_scen_map = {}
        for s_idx, sc in enumerate(scenarios):
            pv = sc.get("param_values", {})
            js_scen_map[f"scen_{s_idx}"] = {
                "params": pv,
                "trace": "".join(f"<div class='text-slate-400'>> {st}</div>" for st in sc.get("trace_steps", [])),
                "res": sc.get("result_value", "Success"),
                "badge": sc.get("status_badge", "Thành công")
            }

        scen_json_str = json.dumps(js_scen_map, ensure_ascii=False)
        js_code = f"""
      const {sec_id}_scenMap = {scen_json_str};

      function on_change_{sec_id}_scenario() {{
        const scenSelect = document.getElementById("{sec_id}-scenario");
        if (!scenSelect) return;
        const scenData = {sec_id}_scenMap[scenSelect.value] || {sec_id}_scenMap["scen_0"];
        if (scenData && scenData.params) {{
          for (const [k, v] of Object.entries(scenData.params)) {{
            const el = document.getElementById("{sec_id}-" + k);
            if (el) el.value = v;
          }}
        }}
        run_{sec_id}_sim();
      }}

      function run_{sec_id}_sim() {{
        const scenSelect = document.getElementById("{sec_id}-scenario");
        const traceBox = document.getElementById("{sec_id}-trace-box");
        const resVal = document.getElementById("{sec_id}-res-val");
        const resBadge = document.getElementById("{sec_id}-res-badge");

        if (!scenSelect || !traceBox || !resVal || !resBadge) return;

        const currentScen = scenSelect.value;
        const scenData = {sec_id}_scenMap[currentScen] || {sec_id}_scenMap["scen_0"];

        traceBox.innerHTML = scenData.trace;
        resVal.innerText = scenData.res;
        resBadge.innerText = scenData.badge;
        resBadge.className = "font-mono text-xs px-2.5 py-1 " + (currentScen === "scen_2" ? "bg-rose-50 text-rose-700 border border-rose-200" : currentScen === "scen_1" ? "bg-amber-50 text-amber-700 border border-amber-200" : "bg-emerald-50 text-emerald-700 border border-emerald-200") + " rounded-full font-semibold";
      }}"""

        first_trace = "".join(f"<div class='text-slate-400'>> {st}</div>" for st in scenarios[0].get("trace_steps", []))

        return {
            "id": sec_id,
            "num": sec_num,
            "title": lesson_title,
            "icon": icon,
            "knowledge_cards": knowledge_cards,
            "sim_title": sim_title,
            "snippet_filename": filename,
            "controllers_html": controllers_html,
            "code_box_html": f"""<pre class="font-mono text-xs leading-relaxed whitespace-pre-wrap"><code id="{sec_id}-code-snippet">{code_sample}</code></pre>""",
            "initial_trace_html": first_trace if first_trace else f"<div class='text-slate-400'>> Sẵn sàng thực thi mã nguồn {filename} ({clean_tech}).</div>",
            "default_res_val": scenarios[0].get("result_value", "Success"),
            "default_res_badge": scenarios[0].get("status_badge", "Thành công"),
            "js_code": js_code,
            "init_call": f"run_{sec_id}_sim();"
        }

    def _render_interactive_section(
        self,
        sec_id: str,
        sec_num: int,
        lesson_title: str,
        icon: str,
        lesson_data: Dict[str, Any],
        tech_stack: str,
        session_title: str = "",
        unified_scenario: str = "",
        session_dir: Optional[Path] = None
    ) -> Dict[str, Any]:
        """Renders structured interactive visualizer data for 1 lesson section across ANY subject."""
        
        # 1. Extract verified knowledge directly from lesson reading material & PM matrix
        extracted = self._extract_knowledge_from_lesson_folder(session_dir, session_title, lesson_title)

        # 2. Attempt LLM-driven generation first for high pedagogical quality and subject adaptability
        llm_data = None
        if os.getenv("SKIP_LIVE_LLM_TESTS") != "1":
            try:
                llm_data = self._generate_section_with_llm(
                    sec_id=sec_id,
                    sec_num=sec_num,
                    lesson_title=lesson_title,
                    tech_stack=tech_stack,
                    session_title=session_title,
                    unified_scenario=unified_scenario,
                    extracted_knowledge=extracted,
                    lesson_data=lesson_data
                )
            except Exception as e:
                print(f"  [Classroom Lecture Agent] LLM generation error: {e}, falling back to Generic Base.")
                llm_data = None
                
        if llm_data and isinstance(llm_data, dict) and llm_data.get("knowledge_cards"):
            llm_data["id"] = sec_id
            llm_data["num"] = sec_num
            llm_data["title"] = lesson_title
            llm_data["icon"] = icon
            llm_data["init_call"] = f"run_{sec_id}_sim();"
            return llm_data

        # 3. Universal Generic Multi-Subject Fallback Base (Zero hardcoding)
        return self._build_generic_multi_subject_section(
            sec_id=sec_id,
            sec_num=sec_num,
            lesson_title=lesson_title,
            icon=icon,
            tech_stack=tech_stack,
            session_title=session_title,
            unified_scenario=unified_scenario,
            extracted_knowledge=extracted,
            lesson_data=lesson_data
        )

    def generate_lecture(
        self,
        session_id: str,
        session_title: str,
        session_dir_path: str,
        tech_stack: str,
        previous_lessons_text: str,
        lessons_data: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """
        Generates complete Interactive Visual Lecture Dashboard for all lessons in a Session.
        Saves output to: Session XX/Bài giảng trên lớp/slides.html and Visualizer/index.html.
        """
        session_dir = Path(session_dir_path)
        session_dir.mkdir(parents=True, exist_ok=True)
        
        slides_dir = session_dir / "Bài giảng trên lớp"
        slides_dir.mkdir(exist_ok=True)

        visualizer_dir = session_dir / "Visualizer"
        visualizer_dir.mkdir(exist_ok=True)
        
        print(f"\n  ---> [Classroom Lecture Agent] Đang tạo Bài giảng trên lớp Trực quan Tương tác cho Session: {session_id} - {session_title}...")
        
        # 1. Parse lesson titles
        parsed_lessons = []
        if lessons_data and len(lessons_data) > 0:
            parsed_lessons = lessons_data
        else:
            raw_matches = re.findall(r'BÀI HỌC\s*(?:Lesson\s*\d+|Bài\s*\d+|\d+)?[\:\-]?\s*(.*?)(?=\n|$)', previous_lessons_text, re.IGNORECASE)
            if not raw_matches:
                raw_matches = re.findall(r'Lesson\s*\d+\s*[\:\-]?\s*(.*?)(?=\n|$)', previous_lessons_text, re.IGNORECASE)
            
            for idx, match in enumerate(raw_matches, 1):
                clean_t = match.strip()
                clean_t = re.sub(r'^\s*(Session\s*\d+|Lesson\s*\d+|Bài\s*\d+|\[\d+\.\d+\]|\d+\.)\s*[\:\-]?\s*', '', clean_t, flags=re.IGNORECASE).strip()
                if clean_t and clean_t not in [l.get("lesson_title") for l in parsed_lessons]:
                    parsed_lessons.append({
                        "lesson_id": f"Lesson {idx:02d}",
                        "lesson_title": clean_t,
                        "summary_text": ""
                    })

        if not parsed_lessons:
            parsed_lessons = [{
                "lesson_id": "Lesson 01",
                "lesson_title": session_title,
                "summary_text": previous_lessons_text[:300]
            }]

        final_html = self.generate_interactive_visualizer_html(
            session_title=session_title,
            module_name=tech_stack,
            lessons_data=parsed_lessons,
            session_dir_path=str(session_dir)
        )

        out_html_file = slides_dir / "slides.html"
        with open(out_html_file, "w", encoding="utf-8") as f:
            f.write(final_html)

        # Also save to Visualizer/index.html
        vis_file = visualizer_dir / "index.html"
        with open(vis_file, "w", encoding="utf-8") as f:
            f.write(final_html)

        print(f"  [Success] Lưu Bài giảng trên lớp HTML ({len(parsed_lessons)} lessons): {out_html_file}")
        print(f"  [Success] Lưu Visualizer HTML: {vis_file}")
        return final_html


classroom_lecture_generator_agent = ClassroomLectureGeneratorAgent()

__all__ = [
    "ClassroomLectureGeneratorAgent",
    "classroom_lecture_generator_agent",
]
