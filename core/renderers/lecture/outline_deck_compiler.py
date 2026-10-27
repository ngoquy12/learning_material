"""
core/renderers/lecture/outline_deck_compiler.py
Master HTML Presentation Slide Deck Compiler.
Parses an outline_bai_giang.md file and generates a full-screen, 16:9 interactive
Master Slide Deck with keyboard navigation, speaker notes drawer, and interactive quiz feedback.
"""

from __future__ import annotations
import re
from pathlib import Path
from typing import Dict, Any, List, Optional

def clean_text(text: str) -> str:
    """Removes stray markdown bolding or asterisks if needed."""
    return text.strip()

def parse_outline_markdown(md_content: str) -> Dict[str, Any]:
    """Parses outline_bai_giang.md into structured slide objects."""
    lines = md_content.splitlines()
    slides = []
    
    current_slide: Optional[Dict[str, Any]] = None
    session_title = "Slide Bài Giảng"
    
    # Try finding session title in first 5 lines
    for line in lines[:5]:
        if line.startswith("# Outline Bài Giảng:"):
            session_title = line.replace("# Outline Bài Giảng:", "").strip()
            break
        elif line.startswith("# "):
            session_title = line.replace("# ", "").strip()
            break

    for line in lines:
        slide_header_match = re.match(r'^###\s+Slide\s+(\d+)\s*:\s*\[([a-zA-Z0-9_\-]+)\]\s*(.*)', line)
        if slide_header_match:
            if current_slide:
                slides.append(current_slide)
            current_slide = {
                "num": int(slide_header_match.group(1)),
                "type": slide_header_match.group(2).strip().lower(),
                "title": slide_header_match.group(3).strip(),
                "subtitle": "",
                "speaker_notes": "",
                "timing": "~2 phút",
                "raw_lines": [],
            }
            continue

        if current_slide:
            # Check speaker notes
            note_match = re.search(r'🎙️\s*\*\*Speaker Notes:\*\*\s*(.*)', line)
            if note_match:
                note_text = note_match.group(1).strip()
                timing_match = re.search(r'\[(~\d+\s*phut|~\d+\s*phút)\]', note_text, re.IGNORECASE)
                if timing_match:
                    current_slide["timing"] = timing_match.group(1).replace("phut", "phút")
                    note_text = re.sub(r'\[(~\d+\s*phut|~\d+\s*phút)\]', '', note_text).strip()
                current_slide["speaker_notes"] = note_text
                continue
            
            # Subtitle (single line italic)
            if not current_slide["subtitle"] and line.strip().startswith("*") and line.strip().endswith("*") and not line.strip().startswith("**"):
                current_slide["subtitle"] = line.strip().strip("*").strip()
                continue
            
            current_slide["raw_lines"].append(line)

    if current_slide:
        slides.append(current_slide)

    return {
        "session_title": session_title,
        "slides": slides
    }

def render_slide_canvas(slide: Dict[str, Any], total_slides: int) -> str:
    """Renders HTML for an individual slide canvas."""
    num = slide["num"]
    stype = slide["type"]
    title = slide["title"] or "Nội dung bài học"
    subtitle = slide["subtitle"]
    raw_text = "\n".join(slide["raw_lines"]).strip()
    num_padded = f"{num:02d}"

    # Render according to slide type
    if stype == "cover":
        m_tag = re.search(r'(Session\s*\d+)', title)
        tag_str = m_tag.group(1) if m_tag else f"Session {num_padded}"
        clean_t = re.sub(r'Session\s*\d+\s*[:-]?\s*', '', title).strip()
        if not clean_t:
            clean_t = title

        return f"""
      <!-- SLIDE {num}: COVER -->
      <section class="slide-canvas" data-slide-index="{num}" data-title="{clean_t}">
        <div class="flex items-center justify-between border-b border-slate-100 pb-4">
          <div class="flex items-center gap-3">
            <span class="px-3 py-1 bg-rikkei-red text-white text-xs font-bold rounded">KHỞI ĐẦU MÔN HỌC</span>
            <span class="text-xs font-semibold text-slate-500">Thiết Kế UI/UX Tiêu Chuẩn Doanh Nghiệp</span>
          </div>
          <span class="text-xs font-semibold text-slate-400">1.5 Giờ Học Trực Quan & Tương Tác</span>
        </div>

        <div class="my-auto max-w-4xl py-6">
          <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-rose-50 border border-rose-200 text-rikkei-red text-sm font-bold mb-6">
            <i class="ph-bold ph-sparkle"></i>
            <span>{tag_str}: Bài giảng lý thuyết & Thực chiến</span>
          </div>
          <h1 class="slide-h1 text-[44px] leading-tight mb-6">
            {clean_t}
          </h1>
          <p class="text-xl text-slate-600 font-medium leading-relaxed max-w-3xl mb-8">
            {subtitle or "Phát triển tư duy thiết kế lấy người dùng làm trung tâm, làm chủ các công cụ và nguyên lý tiêu chuẩn trong sản phẩm số hiện đại."}
          </p>

          <div class="flex items-center gap-6 text-sm text-slate-500 font-semibold border-t border-slate-100 pt-6">
            <div class="flex items-center gap-2">
              <i class="ph-bold ph-graduation-cap text-rikkei-red text-lg"></i>
              <span>Giảng viên: Ban Đào tạo Rikkei Academy</span>
            </div>
            <div class="flex items-center gap-2">
              <i class="ph-bold ph-shield-check text-slate-700 text-lg"></i>
              <span>Tiêu chuẩn chất lượng: Rikkei Education Standards</span>
            </div>
          </div>
        </div>

        <div class="flex items-center justify-between text-xs text-slate-400 border-t border-slate-100 pt-4">
          <span>© Rikkei Education — Tiêu chuẩn đào tạo kỹ sư công nghệ chất lượng cao</span>
          <span class="font-medium text-slate-500">Nhấn phím Space hoặc → để tiếp tục</span>
        </div>
        <div class="slide-corner-badge"><span>{num_padded}</span></div>
      </section>"""

    elif stype == "agenda":
        items = re.findall(r'-\s*(\d+)\.\s*(.*)', raw_text)
        if not items:
            items = re.findall(r'(\d+)\.\s*(.*)', raw_text)
        
        cards_html = []
        colors = [
            ("border-l-rikkei-red", "bg-rose-50", "text-rikkei-red"),
            ("border-l-indigo-600", "bg-indigo-50", "text-indigo-700"),
            ("border-l-amber-600", "bg-amber-50", "text-amber-700"),
            ("border-l-emerald-600", "bg-emerald-50", "text-emerald-700"),
            ("border-l-slate-700", "bg-slate-100", "text-slate-700"),
        ]

        for idx, (num_str, itext) in enumerate(items):
            c_border, c_bg, c_text = colors[idx % len(colors)]
            span_col = "md:col-span-2" if (idx == len(items) - 1 and len(items) % 2 != 0) else ""
            cards_html.append(f"""
          <div class="bento-card flex items-start gap-4 border-l-4 {c_border} {span_col}">
            <span class="w-10 h-10 rounded-xl {c_bg} {c_text} flex items-center justify-center font-montserrat font-bold text-lg shrink-0">{num_str}</span>
            <div>
              <h3 class="font-bold text-base text-slate-900">{itext}</h3>
              <p class="text-xs text-slate-500 mt-1">Trọng tâm kiến thức thực tiễn & thực hành thiết kế.</p>
            </div>
          </div>""")

        return f"""
      <!-- SLIDE {num}: AGENDA -->
      <section class="slide-canvas" data-slide-index="{num}" data-title="{title or 'Nội dung bài học'}">
        <div>
          <h2 class="slide-h2 mb-1">NỘI DUNG BÀI HỌC</h2>
          <h1 class="slide-h1 text-[32px] mb-2">{title or 'Lộ Trình Buổi Học'}</h1>
          <p class="slide-subtitle mb-6">{subtitle or 'Nội dung dẫn dắt tuần tự theo quy trình thiết kế chuyên nghiệp.'}</p>
        </div>

        <div class="my-auto grid grid-cols-1 md:grid-cols-2 gap-4">
          {''.join(cards_html)}
        </div>

        <div class="flex items-center justify-between text-xs text-slate-400 border-t border-slate-100 pt-3">
          <span>Khung chương trình: {len(items)} Module cốt lõi chuẩn doanh nghiệp</span>
          <span>Thời lượng ước tính: 90 phút</span>
        </div>
        <div class="slide-corner-badge"><span>{num_padded}</span></div>
      </section>"""

    elif stype == "objectives":
        obj_matches = re.findall(r'-\s*\[Mục tiêu\]\s*(.*)', raw_text)
        if not obj_matches:
            obj_matches = [line.strip("- *").strip() for line in raw_text.splitlines() if line.strip()]

        icons = [
            ("ph-scales", "bg-red-100", "text-rikkei-red"),
            ("ph-arrows-clockwise", "bg-indigo-100", "text-indigo-700"),
            ("ph-paint-brush", "bg-amber-100", "text-amber-700"),
            ("ph-layout", "bg-emerald-100", "text-emerald-700"),
        ]

        obj_cards = []
        for idx, otxt in enumerate(obj_matches[:4]):
            ico, ibg, itxt_col = icons[idx % len(icons)]
            obj_cards.append(f"""
          <div class="bento-card bg-slate-50/60 flex items-start gap-4">
            <div class="p-3 {ibg} {itxt_col} rounded-xl shrink-0">
              <i class="ph-bold {ico} text-2xl"></i>
            </div>
            <div>
              <span class="text-xs font-bold uppercase tracking-wider {itxt_col}">Mục tiêu {idx + 1}</span>
              <p class="text-sm text-slate-800 font-medium mt-1.5 leading-relaxed">
                {otxt}
              </p>
            </div>
          </div>""")

        return f"""
      <!-- SLIDE {num}: OBJECTIVES -->
      <section class="slide-canvas" data-slide-index="{num}" data-title="{title or 'Mục tiêu bài học'}">
        <div>
          <h2 class="slide-h2 mb-1">MỤC TIÊU BÀI HỌC</h2>
          <h1 class="slide-h1 text-[32px] mb-2">{title or 'Chuẩn Đầu Ra Buổi Học (Learning Outcomes)'}</h1>
          <p class="slide-subtitle mb-6">{subtitle or 'Sau khi hoàn thành buổi học, học viên sẽ nắm vững các năng lực cốt lõi sau đây:'}</p>
        </div>

        <div class="my-auto grid grid-cols-1 md:grid-cols-2 gap-5">
          {''.join(obj_cards)}
        </div>

        <div class="flex items-center justify-between text-xs text-slate-400 border-t border-slate-100 pt-3">
          <span>Chuẩn đầu ra bám sát khung năng lực UI/UX Product Designer</span>
          <span>Đánh giá qua: Hoạt động lớp & Bài tập thực hành</span>
        </div>
        <div class="slide-corner-badge"><span>{num_padded}</span></div>
      </section>"""

    elif stype == "comparison_2col":
        # Parse 2 columns
        col_headers = re.findall(r'\*\*([^*]+)\*\*', raw_text)
        parts = re.split(r'\*\*([^*]+)\*\*', raw_text)
        
        col1_title = col_headers[0] if len(col_headers) > 0 else "Góc nhìn 1"
        col2_title = col_headers[1] if len(col_headers) > 1 else "Góc nhìn 2"
        
        col1_bullets = []
        col2_bullets = []
        
        if len(parts) >= 3:
            col1_bullets = [b.strip("- *").strip() for b in parts[2].splitlines() if b.strip().startswith("-")]
        if len(parts) >= 5:
            col2_bullets = [b.strip("- *").strip() for b in parts[4].splitlines() if b.strip().startswith("-")]

        # Determine context semantics: UI vs UX, Anti-pattern vs Standard, Frame vs Group, or Neutral
        c1_low = col1_title.lower()
        c2_low = col2_title.lower()
        t_low = title.lower()

        is_ui_vs_ux = ("ui" in c1_low or "giao diện" in c1_low) and ("ux" in c2_low or "trải nghiệm" in c2_low)
        is_anti_pattern = any(k in c1_low or k in t_low for k in ["cảm tính", "sai lầm", "chưa tối ưu", "cần tránh", "anti-pattern", "truyền thống", "lỗi"])
        is_frame_vs_group = ("frame" in c1_low or "khung" in c1_low) and ("group" in c2_low or "nhóm" in c2_low)

        mini_card_col1 = ""
        mini_card_col2 = ""

        if is_ui_vs_ux:
            badge1 = "BỀ NỔI THỊ GIÁC (UI)"
            badge1_cls = "text-sky-800 bg-sky-100"
            border1 = "border-t-4 border-t-sky-500 bg-sky-50/20"
            icon1 = '<i class="ph-bold ph-palette text-sky-600 mt-1 shrink-0"></i>'
            
            badge2 = "LOGIC NỀN TẢNG (UX)"
            badge2_cls = "text-indigo-800 bg-indigo-100"
            border2 = "border-t-4 border-t-indigo-600 bg-indigo-50/20"
            icon2 = '<i class="ph-bold ph-brain text-indigo-600 mt-1 shrink-0"></i>'
            
            footer_note = "💡 <strong>Mối quan hệ tương hỗ:</strong> UI là bề nổi thị giác thu hút khách hàng; UX là trải nghiệm tiện dụng giữ chân người dùng lâu dài."
            
            mini_card_col1 = """
            <div class="mt-3 p-3 bg-white border border-sky-200 rounded-xl flex items-center justify-between shadow-xs">
              <div class="flex items-center gap-2.5">
                <div class="w-7 h-7 rounded-lg bg-[#ee4d2d] flex items-center justify-center text-white text-xs font-bold shadow-xs">
                  <i class="ph-bold ph-tag"></i>
                </div>
                <div>
                  <span class="text-xs font-bold text-slate-800">Visual Spec: Nút Áp Mã</span>
                  <span class="block text-[10px] text-slate-500">Color: #EE4D2D · Inter SemiBold · 8pt Grid</span>
                </div>
              </div>
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-sky-100 text-sky-800">UI SPEC</span>
            </div>"""

            mini_card_col2 = """
            <div class="mt-3 p-3 bg-white border border-indigo-200 rounded-xl flex items-center justify-between shadow-xs">
              <div class="flex items-center gap-2.5">
                <div class="w-7 h-7 rounded-lg bg-indigo-600 flex items-center justify-center text-white text-xs font-bold shadow-xs">
                  <i class="ph-bold ph-lightning"></i>
                </div>
                <div>
                  <span class="text-xs font-bold text-slate-800">Behavior Logic: Auto Suggest Mã</span>
                  <span class="block text-[10px] text-slate-500">Tiết kiệm 45s thao tác · Giảm 38% bỏ giỏ hàng</span>
                </div>
              </div>
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-indigo-100 text-indigo-800">UX VALUE</span>
            </div>"""

        elif is_anti_pattern:
            badge1 = "CẦN TRÁNH (ANTI-PATTERN)"
            badge1_cls = "text-rose-700 bg-rose-100"
            border1 = "border-t-4 border-t-rose-500 bg-rose-50/20"
            icon1 = '<i class="ph-bold ph-x-circle text-rose-500 mt-1 shrink-0"></i>'
            
            badge2 = "CHUẨN MỰC UCD (BEST PRACTICE)"
            badge2_cls = "text-emerald-800 bg-emerald-100"
            border2 = "border-t-4 border-t-emerald-600 bg-emerald-50/20"
            icon2 = '<i class="ph-bold ph-check-circle text-emerald-600 mt-1 shrink-0"></i>'
            
            footer_note = "💡 <strong>Nguyên tắc vàng:</strong> Designer không phải là người dùng. Mọi quyết định thiết kế phải xuất phát từ dữ liệu hành vi thực tế."

        elif is_frame_vs_group:
            badge1 = "CONTAINER ĐỘC LẬP (FRAME)"
            badge1_cls = "text-sky-800 bg-sky-100"
            border1 = "border-t-4 border-t-sky-500 bg-sky-50/20"
            icon1 = '<i class="ph-bold ph-frame-corners text-sky-600 mt-1 shrink-0"></i>'
            
            badge2 = "NHÓM TẬP HỢP (GROUP)"
            badge2_cls = "text-amber-800 bg-amber-100"
            border2 = "border-t-4 border-t-amber-500 bg-amber-50/20"
            icon2 = '<i class="ph-bold ph-squares-four text-amber-600 mt-1 shrink-0"></i>'
            
            footer_note = "💡 <strong>Figma Standard:</strong> Ưu tiên tuyệt đối việc sử dụng Frame để thiết lập Auto Layout và Responsive Constraints."

        else:
            badge1 = "KHÍA CẠNH 1"
            badge1_cls = "text-slate-700 bg-slate-100"
            border1 = "border-t-4 border-t-sky-500 bg-sky-50/20"
            icon1 = '<i class="ph-bold ph-circle text-sky-600 mt-1 shrink-0"></i>'
            
            badge2 = "KHÍA CẠNH 2"
            badge2_cls = "text-slate-700 bg-slate-100"
            border2 = "border-t-4 border-t-indigo-600 bg-indigo-50/20"
            icon2 = '<i class="ph-bold ph-check-circle text-indigo-600 mt-1 shrink-0"></i>'
            
            footer_note = "💡 So sánh đối chiếu trực quan giúp định hình tư duy thiết kế đa chiều và chính xác."

        c1_items = "".join([f'<li class="flex items-start gap-2.5">{icon1}<span>{b}</span></li>' for b in col1_bullets])
        c2_items = "".join([f'<li class="flex items-start gap-2.5">{icon2}<span>{b}</span></li>' for b in col2_bullets])

        return f"""
      <!-- SLIDE {num}: COMPARISON 2-COL -->
      <section class="slide-canvas" data-slide-index="{num}" data-title="{title}">
        <div>
          <div class="flex items-center justify-between">
            <h2 class="slide-h2 mb-1">SO SÁNH & ĐỐI CHIẾU</h2>
            <span class="text-xs font-bold px-2.5 py-1 bg-slate-100 text-slate-700 rounded-md">Phân tích chuyên sâu</span>
          </div>
          <h1 class="slide-h1 text-[32px] mb-2">{title}</h1>
          <p class="slide-subtitle mb-5">{subtitle or 'Đối chiếu trực quan giúp định hình tư duy thiết kế đúng đắn.'}</p>
        </div>

        <div class="my-auto grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Col 1 -->
          <div class="bento-card {border1} space-y-3 flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between border-b border-slate-200/60 pb-3 mb-3">
                <h3 class="font-montserrat font-bold text-base text-slate-900">{col1_title}</h3>
                <span class="text-xs font-bold {badge1_cls} px-2 py-0.5 rounded">{badge1}</span>
              </div>
              <ul class="space-y-2.5 text-xs text-slate-700 leading-relaxed">
                {c1_items}
              </ul>
            </div>
            {mini_card_col1}
          </div>

          <!-- Col 2 -->
          <div class="bento-card {border2} space-y-3 flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between border-b border-slate-200/60 pb-3 mb-3">
                <h3 class="font-montserrat font-bold text-base text-slate-900">{col2_title}</h3>
                <span class="text-xs font-bold {badge2_cls} px-2 py-0.5 rounded">{badge2}</span>
              </div>
              <ul class="space-y-2.5 text-xs text-slate-700 leading-relaxed">
                {c2_items}
              </ul>
            </div>
            {mini_card_col2}
          </div>
        </div>

        <div class="p-3 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-600 flex items-center justify-between">
          <span>{footer_note}</span>
          <span class="text-slate-400">Slide {num} / {total_slides}</span>
        </div>
        <div class="slide-corner-badge"><span>{num_padded}</span></div>
      </section>"""

    elif stype in ["grid2x2", "bento_grid"]:
        grid_items = re.findall(r'-\s*\*\*([^*]+)\*\*\s*(.*)', raw_text)
        if not grid_items:
            grid_items = [(f"Nguyên lý {i+1}", line.strip("- *")) for i, line in enumerate(raw_text.splitlines()) if line.strip()]

        cards_html = []
        icons = ["ph-cube", "ph-tree-structure", "ph-sliders-horizontal", "ph-shield-check"]
        bgs = [("bg-rose-50", "text-rikkei-red"), ("bg-blue-50", "text-blue-700"), ("bg-emerald-50", "text-emerald-700"), ("bg-indigo-50", "text-indigo-700")]

        for idx, (g_title, g_desc) in enumerate(grid_items[:4]):
            ico = icons[idx % len(icons)]
            bg_col, txt_col = bgs[idx % len(bgs)]
            cards_html.append(f"""
          <div class="bento-card flex items-start gap-4">
            <div class="p-3 {bg_col} {txt_col} rounded-xl shrink-0">
              <i class="ph-bold {ico} text-2xl"></i>
            </div>
            <div>
              <h3 class="font-bold text-base text-slate-900">{g_title}</h3>
              <p class="text-xs text-slate-600 mt-1 leading-relaxed">{g_desc.strip(': ')}</p>
            </div>
          </div>""")

        return f"""
      <!-- SLIDE {num}: GRID 2X2 -->
      <section class="slide-canvas" data-slide-index="{num}" data-title="{title}">
        <div>
          <div class="flex items-center justify-between">
            <h2 class="slide-h2 mb-1">CẤU TRÚC HỆ THỐNG</h2>
            <span class="text-xs font-bold px-2.5 py-1 bg-amber-50 text-amber-700 border border-amber-200 rounded-md">4 Trụ cột</span>
          </div>
          <h1 class="slide-h1 text-[32px] mb-2">{title}</h1>
          <p class="slide-subtitle mb-6">{subtitle or 'Các thành phần trụ cột liên kết hữu cơ tạo nên cấu trúc hoàn chỉnh.'}</p>
        </div>

        <div class="my-auto grid grid-cols-1 md:grid-cols-2 gap-5">
          {''.join(cards_html)}
        </div>

        <div class="p-3.5 bg-slate-50 border border-slate-200 rounded-xl flex items-center justify-between text-xs text-slate-600 font-medium">
          <span>Áp dụng đồng bộ các nguyên tắc trên giúp tối ưu hóa hiệu quả nhận thức của người dùng.</span>
          <span class="text-slate-400">Slide {num} / {total_slides}</span>
        </div>
        <div class="slide-corner-badge"><span>{num_padded}</span></div>
      </section>"""

    elif stype == "interactive":
        # Interactive quiz slide
        q_match = re.search(r'\*\*Câu hỏi:\*\*\s*(.*)', raw_text)
        question_text = q_match.group(1).strip() if q_match else "Xác định giải pháp tối ưu cho tình huống dưới đây:"
        
        opt_matches = re.findall(r'-\s*([A-D])\.\s*(.*)', raw_text)
        ans_match = re.search(r'>\s*🔑\s*\*\*Đáp án[^:]*:\*\*\s*(.*)', raw_text)
        answer_text = ans_match.group(1).strip() if ans_match else "Đáp án B"
        
        correct_letter = "B"
        m_let = re.search(r'Đáp án\s+([A-D])', answer_text, re.IGNORECASE)
        if m_let:
            correct_letter = m_let.group(1).upper()

        opt_cards = []
        qid = f"quiz_{num}"
        for letter, o_text in opt_matches:
            is_cor = (letter.upper() == correct_letter)
            cor_param = "true" if is_cor else "false"
            opt_cards.append(f"""
            <div onclick="selectQuizOption(this, {cor_param}, '{qid}', '{letter}')" class="quiz-option bento-card p-3.5 border text-sm font-medium flex items-center justify-between">
              <span><strong>{letter}.</strong> {o_text}</span>
              <i class="ph-bold ph-circle text-slate-300 text-lg"></i>
            </div>""")

        clean_ans_html = f"<strong>Chính xác! ({answer_text[:10]}):</strong> {answer_text[10:].strip() if len(answer_text) > 10 else answer_text}"

        return f"""
      <!-- SLIDE {num}: INTERACTIVE QUIZ -->
      <section class="slide-canvas" data-slide-index="{num}" data-title="{title}">
        <div>
          <div class="flex items-center justify-between">
            <h2 class="slide-h2 mb-1">HOẠT ĐỘNG TƯƠNG TÁC TẠI LỚP</h2>
            <span class="text-xs font-bold px-2.5 py-1 bg-rose-50 text-rikkei-red border border-rose-200 rounded-md">Thảo luận lớp</span>
          </div>
          <h1 class="slide-h1 text-[30px] mb-2">{title}</h1>
          <p class="slide-subtitle mb-5">{subtitle or 'Thực hành phân tích và phản xạ nhận diện bài toán thiết kế.'}</p>
        </div>

        <div class="my-auto space-y-4">
          <div class="p-4 bg-slate-50 border border-slate-200 rounded-2xl flex items-start gap-3">
            <i class="ph-bold ph-question text-rikkei-red text-2xl shrink-0 mt-0.5"></i>
            <div class="text-base text-slate-800 font-medium leading-relaxed">
              <strong>Tình huống:</strong> {question_text}
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-3" id="quiz-options-{qid}">
            {''.join(opt_cards)}
          </div>

          <div id="quiz-feedback-{qid}" class="hidden p-4 rounded-xl border text-sm font-medium leading-relaxed" data-solution="{answer_text}"></div>
        </div>

        <div class="flex items-center justify-between text-xs text-slate-400 border-t border-slate-100 pt-3">
          <button onclick="revealQuizAnswer('{qid}', '{correct_letter}')" class="text-xs text-rikkei-red font-semibold hover:underline">
            [Giảng viên] Bấm để hiển thị đáp án và phân tích
          </button>
          <span>Slide {num} / {total_slides}</span>
        </div>
        <div class="slide-corner-badge"><span>{num_padded}</span></div>
      </section>"""

    elif stype == "timeline":
        steps = re.findall(r'-\s*\*\*([^*]+)\*\*\s*(.*)', raw_text)
        if not steps:
            steps = re.findall(r'-\s*(\d+\.\s*[^*]+)\s*(.*)', raw_text)

        step_cards = []
        colors = [
            ("border-t-rose-500", "bg-rose-50/30", "bg-rose-500"),
            ("border-t-amber-500", "bg-amber-50/30", "bg-amber-500"),
            ("border-t-sky-500", "bg-sky-50/30", "bg-sky-500"),
            ("border-t-indigo-500", "bg-indigo-50/30", "bg-indigo-500"),
            ("border-t-emerald-500", "bg-emerald-50/30", "bg-emerald-500"),
        ]

        for idx, (st_name, st_desc) in enumerate(steps):
            c_top, c_bg, c_num = colors[idx % len(colors)]
            clean_sname = re.sub(r'^\d+\.\s*', '', st_name).strip(': ')
            step_cards.append(f"""
          <div class="bento-card border-t-4 {c_top} {c_bg} flex flex-col justify-between h-full p-4">
            <div>
              <span class="w-7 h-7 rounded-full {c_num} text-white font-bold text-xs flex items-center justify-center mb-2">{idx + 1}</span>
              <h3 class="font-bold text-sm text-slate-900">{clean_sname}</h3>
              <p class="text-xs text-slate-600 mt-2 leading-relaxed">{st_desc.strip(': ')}</p>
            </div>
            <div class="mt-3 pt-2 border-t border-slate-200/60 text-[11px] font-semibold text-slate-500">
              Bước {idx + 1} quy trình
            </div>
          </div>""")

        return f"""
      <!-- SLIDE {num}: TIMELINE -->
      <section class="slide-canvas" data-slide-index="{num}" data-title="{title}">
        <div>
          <div class="flex items-center justify-between">
            <h2 class="slide-h2 mb-1">QUY TRÌNH THỰC THI</h2>
            <span class="text-xs font-bold px-2.5 py-1 bg-indigo-50 text-indigo-700 border border-indigo-200 rounded-md">Quy trình chuẩn</span>
          </div>
          <h1 class="slide-h1 text-[32px] mb-2">{title}</h1>
          <p class="slide-subtitle mb-6">{subtitle or 'Quy trình lặp liên tục giúp tối ưu hóa chất lượng giải pháp sản phẩm.'}</p>
        </div>

        <div class="my-auto grid grid-cols-1 md:grid-cols-{min(len(steps), 5)} gap-3">
          {''.join(step_cards)}
        </div>

        <div class="p-3 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-600 flex items-center gap-2">
          <i class="ph-bold ph-arrows-clockwise text-indigo-600 text-base"></i>
          <span><strong>Tính lặp (Iterative):</strong> Các bước trong quy trình liên kết chặt chẽ và liên tục tiếp nhận phản hồi để hoàn thiện.</span>
        </div>
        <div class="slide-corner-badge"><span>{num_padded}</span></div>
      </section>"""

    elif stype == "code_right_card":
        # Left breakdown, Right code/spec block
        code_match = re.search(r'```([a-zA-Z]*)\n([\s\S]*?)```', raw_text)
        code_lang = code_match.group(1).lower() if code_match else "html"
        code_str = code_match.group(2).strip() if code_match else ""
        
        left_text = re.sub(r'```[\s\S]*?```', '', raw_text).strip()
        left_lines = [l.strip() for l in left_text.splitlines() if l.strip()]
        left_html_items = []
        for line in left_lines:
            m_bullet_bold = re.match(r'^[-\*]?\s*\*\*([^*]+)\*\*:?\s*(.*)', line)
            m_bullet_plain = re.match(r'^[-\*]\s*([^:]+):\s*(.*)', line)
            if m_bullet_bold:
                h = m_bullet_bold.group(1).strip()
                d = m_bullet_bold.group(2).strip()
                left_html_items.append(f"""
            <div class="p-2.5 rounded-xl border border-slate-200 bg-slate-50/80">
              <span class="text-xs font-bold text-slate-900 block truncate">{h}</span>
              <p class="text-[11px] text-slate-600 mt-0.5 leading-relaxed line-clamp-2">{d}</p>
            </div>""")
            elif m_bullet_plain:
                h = m_bullet_plain.group(1).strip()
                d = m_bullet_plain.group(2).strip()
                left_html_items.append(f"""
            <div class="p-2.5 rounded-xl border border-indigo-100 bg-indigo-50/40">
              <span class="text-xs font-bold text-indigo-900 block truncate">{h}</span>
              <p class="text-[11px] text-slate-600 mt-0.5 leading-relaxed line-clamp-2">{d}</p>
            </div>""")
            elif line.startswith("-"):
                c = line.strip("- ").strip()
                left_html_items.append(f"""
            <div class="p-2.5 rounded-xl border border-slate-200 bg-white">
              <p class="text-xs text-slate-700 leading-snug">{c}</p>
            </div>""")

        # Generate Concrete Live Result Preview (Browser view or AI Output)
        is_html = any(tag in code_str.lower() for tag in ["<!doctype", "<html", "<article", "<h1>", "<table", "<p>", "<head>", "<body>"])
        is_prompt = any(k in code_str for k in ["[Role", "Role:", "Persona", "UX Researcher"]) or "prompt" in title.lower()

        if is_html:
            m_title = re.search(r'<title>([^<]+)</title>', code_str)
            tab_title = m_title.group(1).strip() if m_title else "ShopeeFood — Món ăn"
            
            m_body = re.search(r'<body[^>]*>([\s\S]*?)</body>', code_str)
            inner_content = m_body.group(1).strip() if m_body else code_str
            inner_content = re.sub(r'<!DOCTYPE[\s\S]*?>', '', inner_content, flags=re.I)
            inner_content = re.sub(r'<html[\s\S]*?>', '', inner_content, flags=re.I)
            inner_content = re.sub(r'</html>', '', inner_content, flags=re.I)
            inner_content = re.sub(r'<head>[\s\S]*?</head>', '', inner_content, flags=re.I)
            
            # Format HTML elements nicely
            rendered = inner_content
            rendered = re.sub(
                r'<img\s+src="([^"]*)"\s+alt="([^"]*)"[^>]*>',
                r'<div class="my-2 p-2.5 bg-amber-50/80 border border-amber-200 rounded-xl flex items-center gap-3 text-amber-900"><div class="w-10 h-10 rounded-lg bg-amber-200 flex items-center justify-center text-amber-800 text-lg font-bold shrink-0"><i class="ph-bold ph-bowl-food"></i></div><div class="min-w-0"><span class="text-xs font-bold block truncate">\2</span><span class="text-[10px] text-amber-700 font-mono">img: \1</span></div></div>',
                rendered
            )
            rendered = re.sub(r'<h1>(.*?)</h1>', r'<h1 class="text-base font-bold text-slate-900 mb-1 leading-snug">\1</h1>', rendered)
            rendered = re.sub(r'<h2>(.*?)</h2>', r'<h2 class="text-sm font-bold text-slate-800 mb-1">\1</h2>', rendered)
            rendered = re.sub(r'<p>(.*?)</p>', r'<p class="text-xs text-slate-600 mb-1 leading-relaxed">\1</p>', rendered)
            rendered = re.sub(r'<a\s+href="([^"]*)"[^>]*>(.*?)</a>', r'<a href="#" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#ee4d2d] text-white text-xs font-bold hover:bg-[#d03e20] shadow-xs mt-1 transition">\2 <i class="ph-bold ph-arrow-right text-[11px]"></i></a>', rendered)

            clean_text_check = re.sub(r'<!--[\s\S]*?-->', '', inner_content).strip()
            if not clean_text_check:
                rendered = """
                <div class="p-3 bg-slate-50 rounded-xl border border-dashed border-slate-300 text-center space-y-1 my-auto">
                  <i class="ph-bold ph-browser text-2xl text-slate-400 block mb-0.5"></i>
                  <span class="text-xs font-bold text-slate-700 block">Vùng hiển thị trực quan (Body)</span>
                  <p class="text-[11px] text-slate-500 leading-relaxed">Trình duyệt chỉ hiển thị phần tử trong thẻ &lt;body&gt;. Khối &lt;head&gt; chứa siêu dữ liệu ẩn cấu hình bảng mã UTF-8 và tiêu đề tab.</p>
                </div>"""

            right_preview_card = f"""
            <div class="bento-card p-0 overflow-hidden border border-slate-200 bg-white flex flex-col justify-between h-full shadow-xs">
              <div class="px-3 py-2 bg-slate-100 border-b border-slate-200 flex items-center justify-between text-xs">
                <div class="flex items-center gap-1.5">
                  <span class="w-2.5 h-2.5 rounded-full bg-rose-500 inline-block"></span>
                  <span class="w-2.5 h-2.5 rounded-full bg-amber-500 inline-block"></span>
                  <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block"></span>
                </div>
                <div class="px-3 py-0.5 bg-white border border-slate-200 rounded-md text-[10px] font-mono text-slate-600 flex items-center gap-1 truncate max-w-[200px]">
                  <i class="ph-bold ph-lock-key text-emerald-600 text-[9px]"></i>
                  <span>shopeefood.vn/menu</span>
                </div>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800">TAB: {tab_title[:18]}</span>
              </div>
              <div class="p-4 bg-white flex-1 overflow-y-auto space-y-2 flex flex-col justify-center">
                {rendered}
              </div>
              <div class="px-3 py-1.5 bg-slate-50 border-t border-slate-200 text-[10px] text-slate-500 flex items-center justify-between font-medium">
                <span class="flex items-center gap-1 text-emerald-700 font-bold"><i class="ph-bold ph-check-circle"></i> Kết quả hiển thị thực tế trên trình duyệt</span>
                <span class="text-slate-400 font-mono">HTML5 Standards</span>
              </div>
            </div>"""

        elif is_prompt:
            right_preview_card = """
            <div class="bento-card p-0 overflow-hidden border border-slate-200 bg-white flex flex-col justify-between h-full shadow-xs">
              <div class="px-3 py-2 bg-slate-900 text-white flex items-center justify-between text-xs">
                <div class="flex items-center gap-2">
                  <i class="ph-bold ph-chat-text text-slate-300"></i>
                  <span class="font-bold">Kết quả AI Phân tích từ Prompt</span>
                </div>
                <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold border border-emerald-400/30">AI Output</span>
              </div>
              <div class="p-3.5 bg-white flex-1 space-y-2.5 overflow-y-auto text-xs">
                <div class="flex items-center gap-2.5 p-2 rounded-xl bg-slate-50 border border-slate-200">
                  <div class="w-9 h-9 rounded-full bg-indigo-100 text-indigo-700 flex items-center justify-center text-base font-bold shrink-0">
                    <i class="ph-bold ph-user"></i>
                  </div>
                  <div>
                    <h4 class="font-bold text-slate-900 text-xs">Trần Thị Mai (26 tuổi)</h4>
                    <p class="text-[10px] text-slate-500">Chuyên viên Marketing · Đặt trưa nhóm 4-6 người</p>
                  </div>
                </div>
                <div class="space-y-1">
                  <span class="text-[10px] font-bold text-slate-700 uppercase tracking-wider block">03 Điểm đau (Pain Points) nhận diện:</span>
                  <div class="p-1.5 rounded-lg bg-rose-50 border border-rose-200 text-rose-900 text-[10px] flex items-center gap-1.5">
                    <i class="ph-bold ph-warning text-rose-600 shrink-0"></i>
                    <span>DeliveryFee tăng 15k giờ trưa mưa bão</span>
                  </div>
                  <div class="p-1.5 rounded-lg bg-rose-50 border border-rose-200 text-rose-900 text-[10px] flex items-center gap-1.5">
                    <i class="ph-bold ph-warning text-rose-600 shrink-0"></i>
                    <span>Khó tìm voucher tốt nhất, chia bill thủ công</span>
                  </div>
                </div>
                <div class="p-2 rounded-lg bg-emerald-50 border border-emerald-200 text-emerald-950 text-[10px] space-y-0.5">
                  <span class="font-bold flex items-center gap-1 text-emerald-900">
                    <i class="ph-bold ph-lightbulb text-emerald-600"></i> Đề xuất tính năng UI/UX:
                  </span>
                  <p>Tính năng Gom đơn nhóm tự chia tiền + Tự áp dụng voucher tối ưu.</p>
                </div>
              </div>
              <div class="px-3 py-1 bg-slate-50 border-t border-slate-200 text-[10px] text-slate-500 flex items-center justify-between font-medium">
                <span>Dữ liệu User Persona chuẩn Usability</span>
                <span class="font-mono text-indigo-600 font-bold">ShopeeFood Case</span>
              </div>
            </div>"""
        else:
            right_preview_card = """
            <div class="bento-card p-4 bg-slate-50 border border-slate-200 flex flex-col justify-between h-full">
              <div>
                <span class="text-xs font-bold text-slate-700 uppercase">Mục tiêu ứng dụng thực tiễn:</span>
                <p class="text-xs text-slate-600 mt-2 leading-relaxed">Đặc tả này được sử dụng trực tiếp trong quy trình thiết kế và phát triển tính năng.</p>
              </div>
              <div class="p-2 bg-emerald-50 rounded text-emerald-800 text-xs font-semibold">
                ✓ Tiêu chuẩn áp dụng vào hệ thống thực tế
              </div>
            </div>"""

        bottom_chips_html = ""
        if left_html_items:
            chips_count = min(len(left_html_items), 4)
            bottom_chips_html = f"""
          <div class="grid grid-cols-2 md:grid-cols-{chips_count} gap-3 mt-3">
            {''.join(left_html_items[:chips_count])}
          </div>"""

        return f"""
      <!-- SLIDE {num}: CODE & LIVE RESULT (SIDE-BY-SIDE) -->
      <section class="slide-canvas" data-slide-index="{num}" data-title="{title}">
        <div>
          <div class="flex items-center justify-between">
            <h2 class="slide-h2 mb-1">MÃ NGUỒN & KẾT QUẢ TRỰC QUAN</h2>
            <span class="text-xs font-bold px-2.5 py-1 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-md">Side-by-Side Live Demo</span>
          </div>
          <h1 class="slide-h1 text-[30px] mb-1.5">{title}</h1>
          <p class="slide-subtitle mb-4">{subtitle or 'Đối chiếu trực tiếp giữa mã nguồn khai báo và kết quả hiển thị trên trình duyệt.'}</p>
        </div>

        <div class="my-auto space-y-3">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 items-stretch">
            <!-- Left: Code Snippet -->
            <div class="bento-card p-0 overflow-hidden border border-slate-800 bg-slate-900 flex flex-col justify-between h-full shadow-xs">
              <div class="px-3.5 py-2 bg-slate-950 border-b border-slate-800 flex items-center justify-between text-xs">
                <span class="font-mono text-[11px] font-bold text-sky-400 flex items-center gap-1.5">
                  <i class="ph-bold ph-file-code"></i> index.html
                </span>
                <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-sky-500/20 text-sky-300">MÃ NGUỒN KHAI BÁO</span>
              </div>
              <pre class="font-mono text-xs text-sky-100 leading-relaxed p-3.5 bg-slate-900 whitespace-pre-wrap overflow-x-auto flex-1">{code_str}</pre>
              <div class="px-3 py-1.5 bg-slate-950/80 border-t border-slate-800 text-[10px] text-slate-400 flex items-center justify-between">
                <span>Cú pháp chuẩn hóa W3C Standards</span>
                <span class="font-mono text-slate-500">Read-only Demo</span>
              </div>
            </div>

            <!-- Right: Concrete Live Result / Browser View -->
            {right_preview_card}
          </div>

          <!-- Bottom: Key Concept Breakdown Chips -->
          {bottom_chips_html}
        </div>

        <div class="flex items-center justify-between text-xs text-slate-400 border-t border-slate-100 pt-3">
          <span>Kỹ năng: Nhìn mã nguồn đoán được giao diện - Viết mã chuẩn để trình duyệt dựng đúng</span>
          <span>Slide {num} / {total_slides}</span>
        </div>
        <div class="slide-corner-badge"><span>{num_padded}</span></div>
      </section>"""

    elif stype == "glossary_table":
        # Table slide
        table_lines = [l for l in raw_text.splitlines() if "|" in l]
        table_rows = []
        for l in table_lines:
            cells = [c.strip() for c in l.split("|")[1:-1]]
            if cells and not all(c.startswith("-") for c in cells):
                table_rows.append(cells)

        header_cells = table_rows[0] if table_rows else ["Thuật ngữ", "Tiếng Anh", "Định nghĩa"]
        data_rows = table_rows[1:] if len(table_rows) > 1 else []

        th_html = "".join([f'<th class="py-2.5 px-4">{c}</th>' for c in header_cells])
        tbody_html = ""
        for r in data_rows:
            c1 = r[0] if len(r) > 0 else ""
            c2 = r[1] if len(r) > 1 else ""
            c3 = r[2] if len(r) > 2 else ""
            tbody_html += f"""
              <tr class="hover:bg-slate-50/50">
                <td class="py-2 px-4 font-semibold text-slate-900">{c1}</td>
                <td class="py-2 px-4 font-mono font-medium text-rikkei-red">{c2}</td>
                <td class="py-2 px-4">{c3}</td>
              </tr>"""

        return f"""
      <!-- SLIDE {num}: GLOSSARY TABLE -->
      <section class="slide-canvas" data-slide-index="{num}" data-title="{title}">
        <div>
          <div class="flex items-center justify-between">
            <h2 class="slide-h2 mb-1">TỔNG HỢP KIẾN THỨC CỐT LÕI</h2>
            <span class="text-xs font-bold px-2.5 py-1 bg-slate-100 text-slate-700 rounded-md">Tra cứu nhanh</span>
          </div>
          <h1 class="slide-h1 text-[32px] mb-2">{title}</h1>
          <p class="slide-subtitle mb-4">{subtitle or 'Các định nghĩa chuẩn mực quốc tế mà mọi Product Designer cần sử dụng thành thạo.'}</p>
        </div>

        <div class="my-auto overflow-hidden rounded-xl border border-slate-200 bg-white">
          <table class="w-full text-left text-xs border-collapse">
            <thead>
              <tr class="bg-slate-50 border-b border-slate-200 text-slate-800 font-bold">
                {th_html}
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 text-slate-600">
              {tbody_html}
            </tbody>
          </table>
        </div>

        <div class="flex items-center justify-between text-xs text-slate-400 border-t border-slate-100 pt-3">
          <span>Tiêu chuẩn thuật ngữ quốc tế đồng bộ với tài liệu bài đọc môn học</span>
          <span>Slide {num} / {total_slides}</span>
        </div>
        <div class="slide-corner-badge"><span>{num_padded}</span></div>
      </section>"""

    elif stype == "exercises":
        # 2 cards: Exercises & References
        ex_bullets = []
        ref_bullets = []
        current_cat = None
        for line in raw_text.splitlines():
            if "bài tập" in line.lower():
                current_cat = "ex"
            elif "tài liệu" in line.lower():
                current_cat = "ref"
            elif line.strip().startswith("-") or line.strip().startswith("*"):
                content = line.strip("- *").strip()
                if current_cat == "ex":
                    ex_bullets.append(content)
                else:
                    ref_bullets.append(content)

        ex_items = "".join([f'<li class="flex items-start gap-2"><span class="w-5 h-5 rounded-full bg-rose-100 text-rikkei-red font-bold text-xs flex items-center justify-center shrink-0">{i+1}</span><span>{b}</span></li>' for i, b in enumerate(ex_bullets)])
        ref_items = "".join([f'<li class="flex items-start gap-2"><i class="ph-bold ph-arrow-square-out text-indigo-600 text-base shrink-0 mt-0.5"></i><span>{b}</span></li>' for b in ref_bullets])

        return f"""
      <!-- SLIDE {num}: EXERCISES -->
      <section class="slide-canvas" data-slide-index="{num}" data-title="{title}">
        <div>
          <div class="flex items-center justify-between">
            <h2 class="slide-h2 mb-1">VẬN DỤNG THỰC TẾ</h2>
            <span class="text-xs font-bold px-2.5 py-1 bg-rose-50 text-rikkei-red border border-rose-200 rounded-md">Yêu cầu sau buổi học</span>
          </div>
          <h1 class="slide-h1 text-[32px] mb-2">{title}</h1>
          <p class="slide-subtitle mb-6">{subtitle or 'Vận dụng kiến thức bài học vào thực hành nghiên cứu và giải quyết bài toán giao diện thực tế.'}</p>
        </div>

        <div class="my-auto grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="bento-card border-t-4 border-t-rikkei-red space-y-3 bg-rose-50/10">
            <div class="flex items-center gap-2 border-b border-rose-100 pb-2">
              <i class="ph-bold ph-pencil-simple text-rikkei-red text-xl"></i>
              <h3 class="font-bold text-base text-slate-900">Bài Tập Thực Hành Bắt Buộc</h3>
            </div>
            <ul class="text-xs text-slate-700 space-y-2.5 leading-relaxed">
              {ex_items}
            </ul>
            <div class="p-2.5 bg-white border border-rose-200 rounded-lg text-[11px] text-slate-600 font-semibold">
              Hạn nộp: Trước buổi học tiếp theo trên hệ thống LMS Rikkei Academy.
            </div>
          </div>

          <div class="bento-card border-t-4 border-t-indigo-600 space-y-3 bg-indigo-50/10">
            <div class="flex items-center gap-2 border-b border-indigo-100 pb-2">
              <i class="ph-bold ph-books text-indigo-600 text-xl"></i>
              <h3 class="font-bold text-base text-slate-900">Tài Liệu Tham Khảo Tiêu Chuẩn</h3>
            </div>
            <ul class="text-xs text-slate-700 space-y-2.5 leading-relaxed">
              {ref_items}
            </ul>
            <div class="p-2.5 bg-white border border-indigo-200 rounded-lg text-[11px] text-slate-600 font-semibold">
              Toàn bộ slide và tài liệu đọc đã được đồng bộ trong thư mục môn học.
            </div>
          </div>
        </div>

        <div class="flex items-center justify-between text-xs text-slate-400 border-t border-slate-100 pt-3">
          <span>Đánh giá rèn luyện: Tính vào điểm thành phần quá trình môn học</span>
          <span>Slide {num} / {total_slides}</span>
        </div>
        <div class="slide-corner-badge"><span>{num_padded}</span></div>
      </section>"""

    elif stype in ["summary", "summary_2col"]:
        headers = re.findall(r'\*\*([^*]+)\*\*', raw_text)
        parts = re.split(r'\*\*([^*]+)\*\*', raw_text)
        
        p1_title = headers[0] if len(headers) > 0 else "Nguyên Tắc Cốt Lõi 1"
        p2_title = headers[1] if len(headers) > 1 else "Nguyên Tắc Cốt Lõi 2"
        
        p1_bullets = []
        p2_bullets = []
        if len(parts) >= 3:
            p1_bullets = [b.strip("- *").strip() for b in parts[2].splitlines() if b.strip().startswith("-")]
        if len(parts) >= 5:
            p2_bullets = [b.strip("- *").strip() for b in parts[4].splitlines() if b.strip().startswith("-")]

        p1_items = "".join([f'<li class="flex items-start gap-2"><i class="ph-bold ph-check-circle text-rikkei-red text-base shrink-0 mt-0.5"></i><span>{b}</span></li>' for b in p1_bullets])
        p2_items = "".join([f'<li class="flex items-start gap-2"><i class="ph-bold ph-check-circle text-indigo-600 text-base shrink-0 mt-0.5"></i><span>{b}</span></li>' for b in p2_bullets])

        return f"""
      <!-- SLIDE {num}: SUMMARY -->
      <section class="slide-canvas" data-slide-index="{num}" data-title="{title}">
        <div>
          <div class="flex items-center justify-between">
            <h2 class="slide-h2 mb-1">TỔNG KẾT BÀI HỌC</h2>
            <span class="text-xs font-bold px-2.5 py-1 bg-rikkei-red text-white rounded-md">Ghi nhớ cốt lõi</span>
          </div>
          <h1 class="slide-h1 text-[32px] mb-2">{title}</h1>
          <p class="slide-subtitle mb-6">{subtitle or 'Các nguyên tắc vàng cần ghi nhớ và áp dụng trong công việc thiết kế.'}</p>
        </div>

        <div class="my-auto grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="bento-card border-l-4 border-l-rikkei-red bg-rose-50/20 space-y-3">
            <div class="flex items-center gap-2 border-b border-rose-100 pb-2">
              <i class="ph-bold ph-seal-check text-rikkei-red text-2xl"></i>
              <h3 class="font-montserrat font-bold text-base text-slate-900">{p1_title}</h3>
            </div>
            <ul class="text-xs text-slate-700 space-y-3 leading-relaxed">
              {p1_items}
            </ul>
          </div>

          <div class="bento-card border-l-4 border-l-indigo-600 bg-indigo-50/20 space-y-3">
            <div class="flex items-center gap-2 border-b border-indigo-100 pb-2">
              <i class="ph-bold ph-sparkle text-indigo-600 text-2xl"></i>
              <h3 class="font-montserrat font-bold text-base text-slate-900">{p2_title}</h3>
            </div>
            <ul class="text-xs text-slate-700 space-y-3 leading-relaxed">
              {p2_items}
            </ul>
          </div>
        </div>

        <div class="p-3.5 bg-slate-900 text-white rounded-xl flex items-center justify-between text-xs">
          <span class="font-medium">Hệ thống đào tạo Lập trình & Thiết kế Tiêu chuẩn Rikkei Academy</span>
          <span class="text-slate-400">Slide {num} / {total_slides}</span>
        </div>
        <div class="slide-corner-badge"><span>{num_padded}</span></div>
      </section>"""

    elif stype == "closing":
        return f"""
      <!-- SLIDE {num}: CLOSING -->
      <section class="slide-canvas" data-slide-index="{num}" data-title="{title}">
        <div class="flex items-center justify-between border-b border-slate-100 pb-4">
          <span class="px-3 py-1 bg-rikkei-red text-white text-xs font-bold rounded">KẾT THÚC BUỔI HỌC</span>
          <span class="text-xs font-semibold text-slate-400">Hẹn Gặp Lại Buổi Học Tiếp Theo</span>
        </div>

        <div class="my-auto max-w-3xl py-4 text-center mx-auto space-y-6">
          <div class="w-16 h-16 rounded-full bg-rose-50 text-rikkei-red mx-auto flex items-center justify-center text-3xl">
            <i class="ph-bold ph-hand-waving"></i>
          </div>
          <h1 class="slide-h1 text-[42px] leading-tight">
            {title or 'Cảm Ơn Các Bạn Đã Tham Gia!'}
          </h1>
          <p class="text-lg text-slate-600 leading-relaxed max-w-2xl mx-auto">
            {subtitle or 'Hãy hoàn thành bài tập thực hành trên hệ thống và chuẩn bị sẵn sàng cho buổi học tiếp theo.'}
          </p>

          <div class="p-4 bg-slate-50 border border-slate-200 rounded-2xl max-w-xl mx-auto text-left space-y-2">
            <div class="text-xs font-bold text-rikkei-red uppercase tracking-wider flex items-center gap-1.5">
              <i class="ph-bold ph-calendar-check"></i>
              <span>Chuẩn bị cho buổi học tiếp theo:</span>
            </div>
            <p class="text-sm font-bold text-slate-900">
              Ôn tập kiến thức và hoàn thiện các bài tập thực hành được giao.
            </p>
            <ul class="text-xs text-slate-600 space-y-1 list-disc pl-4">
              <li>Cài đặt sẵn tài khoản và công cụ phần mềm cần thiết.</li>
              <li>Xem trước đề cương bài học kế tiếp trong syllabus môn học.</li>
            </ul>
          </div>
        </div>

        <div class="flex items-center justify-between text-xs text-slate-400 border-t border-slate-100 pt-4">
          <span>Hệ thống Đào tạo Lập trình & Thiết kế Tiêu chuẩn Rikkei Academy</span>
          <span class="font-medium text-slate-500">Hoàn thành {num} / {total_slides} Slide</span>
        </div>
        <div class="slide-corner-badge"><span>{num_padded}</span></div>
      </section>"""

    elif stype == "flowchart":
        flow_lines = [l.strip("- ").strip() for l in raw_text.splitlines() if l.strip().startswith("-")]
        mermaid_nodes = []
        for fl in flow_lines:
            if fl.startswith("[start]") or fl.startswith("[end]"):
                clean_n = re.sub(r'\[(start|end)\]\s*', '', fl).strip()
                if clean_n:
                    mermaid_nodes.append((f'N{len(mermaid_nodes)}', f'(["{clean_n}"])', 'start_end'))
            elif fl.startswith("[decision]"):
                clean_n = re.sub(r'\[decision\]\s*', '', fl).strip()
                if clean_n:
                    mermaid_nodes.append((f'N{len(mermaid_nodes)}', f'{{"{clean_n}"}}', 'decision'))
            else:
                clean_n = re.sub(r'\[process\]\s*', '', fl).strip()
                if clean_n:
                    mermaid_nodes.append((f'N{len(mermaid_nodes)}', f'["{clean_n}"]', 'process'))
        
        node_defs = "\n    ".join([f"{nid}{shape}" for nid, shape, _ in mermaid_nodes])
        flow_links = []
        for i in range(len(mermaid_nodes) - 1):
            curr_id, _, curr_type = mermaid_nodes[i]
            next_id, _, _ = mermaid_nodes[i+1]
            if curr_type == 'decision':
                flow_links.append(f"{curr_id} -->|Khả thi| {next_id}")
            else:
                flow_links.append(f"{curr_id} --> {next_id}")
        
        link_defs = "\n    ".join(flow_links)
        mermaid_code = f"flowchart LR\n    {node_defs}\n    {link_defs}"

        return f"""
      <!-- SLIDE {num}: FLOWCHART -->
      <section class="slide-canvas" data-slide-index="{num}" data-title="{title}">
        <div>
          <div class="flex items-center justify-between">
            <h2 class="slide-h2 mb-1">SƠ ĐỒ QUY TRÌNH</h2>
            <span class="text-xs font-bold px-2.5 py-1 bg-amber-50 text-amber-700 border border-amber-200 rounded-md">Quy trình trực quan</span>
          </div>
          <h1 class="slide-h1 text-[32px] mb-2">{title}</h1>
          <p class="slide-subtitle mb-4">{subtitle or 'Quy trình vận hành logic theo tiêu chuẩn thiết kế sản phẩm.'}</p>
        </div>

        <div class="my-auto bg-slate-50 border border-slate-200 rounded-2xl p-6 flex flex-col items-center justify-center">
          <div class="mermaid w-full flex justify-center text-xs">
{mermaid_code}
          </div>
        </div>

        <div class="p-3 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-600 flex items-center justify-between">
          <span>Quy trình chuẩn hóa 5 hình khối theo tiêu chuẩn Rikkei Education.</span>
          <span class="text-slate-400">Slide {num} / {total_slides}</span>
        </div>
        <div class="slide-corner-badge"><span>{num_padded}</span></div>
      </section>"""

    else:
        # Generic fallback content card
        bullets = [b.strip("- *").strip() for b in raw_text.splitlines() if b.strip()]
        b_items = "".join([f'<li class="flex items-start gap-2.5"><i class="ph-bold ph-check text-rikkei-red mt-1 shrink-0"></i><span>{b}</span></li>' for b in bullets])

        return f"""
      <!-- SLIDE {num}: GENERIC -->
      <section class="slide-canvas" data-slide-index="{num}" data-title="{title}">
        <div>
          <h2 class="slide-h2 mb-1">KIẾN THỨC CHUYÊN SÂU</h2>
          <h1 class="slide-h1 text-[32px] mb-2">{title}</h1>
          <p class="slide-subtitle mb-6">{subtitle or 'Nội dung bài học chuẩn hóa.'}</p>
        </div>

        <div class="my-auto bento-card p-6 bg-slate-50/50 border border-slate-200">
          <ul class="space-y-4 text-sm text-slate-700 leading-relaxed">
            {b_items}
          </ul>
        </div>

        <div class="flex items-center justify-between text-xs text-slate-400 border-t border-slate-100 pt-3">
          <span>Rikkei Education</span>
          <span>Slide {num} / {total_slides}</span>
        </div>
        <div class="slide-corner-badge"><span>{num_padded}</span></div>
      </section>"""


def compile_outline_to_html(md_path: Path, output_html_path: Path, module_name: str = ""):
    """Compiles an outline markdown file into a full presentation HTML file."""
    md_content = md_path.read_text(encoding="utf-8")
    data = parse_outline_markdown(md_content)
    slides = data["slides"]
    total = len(slides)
    session_title = data["session_title"]

    canvases_html = []
    notes_dict = {}

    for s in slides:
        canvases_html.append(render_slide_canvas(s, total))
        notes_dict[s["num"]] = {
            "timing": s["timing"],
            "text": s["speaker_notes"] or f"Giảng viên giải thích chi tiết nội dung slide {s['num']} và tương tác hỏi đáp với học viên.",
        }

    import json
    notes_json = json.dumps(notes_dict, ensure_ascii=False, indent=2)

    full_html = f"""<!doctype html>
<html lang="vi" class="h-full overflow-hidden select-none">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{session_title} — Bài giảng trên lớp - Rikkei Education</title>

    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Montserrat:wght@600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap"
      rel="stylesheet"
    />

    <!-- Phosphor Icons -->
    <script src="https://unpkg.com/@phosphor-icons/web"></script>

    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
      tailwind.config = {{
        theme: {{
          extend: {{
            fontFamily: {{
              sans: ["Inter", "sans-serif"],
              montserrat: ["Montserrat", "sans-serif"],
              mono: ["JetBrains Mono", "monospace"],
            }},
            colors: {{
              rikkei: {{
                red: "#be111c",
                darkred: "#90000a",
                dark: "#0f172a",
              }},
            }},
          }},
        }},
      }};
    </script>

    <!-- Mermaid.js for Diagrams -->
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
      mermaid.initialize({{
        startOnLoad: false,
        theme: "neutral",
        securityLevel: "loose",
        flowchart: {{ useMaxWidth: true, htmlLabels: true, curve: "basis" }},
      }});
    </script>

    <style>
      html, body {{
        height: 100%;
        margin: 0;
        padding: 0;
        overflow: hidden;
        background-color: #0f172a;
        color: #1e293b;
        font-family: 'Inter', sans-serif;
      }}

      #presentation-viewport {{
        position: relative;
        width: 100vw;
        height: 100vh;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #0b1120;
      }}

      .slide-canvas {{
        position: absolute;
        width: 100%;
        height: 100%;
        display: none;
        flex-direction: column;
        justify-content: space-between;
        background: #ffffff;
        padding: 5rem 5rem 4.5rem 5rem;
        box-sizing: border-box;
        overflow-y: auto;
        opacity: 0;
        transition: opacity 0.25s cubic-bezier(0.4, 0, 0.2, 1);
      }}

      .slide-canvas.active {{
        display: flex;
        opacity: 1;
        z-index: 10;
      }}

      @media (min-aspect-ratio: 16/9) {{
        .slide-canvas {{
          max-width: 177.78vh;
          box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        }}
      }}

      .slide-h1 {{
        font-family: 'Montserrat', sans-serif;
        font-weight: 800;
        font-size: 2.25rem;
        line-height: 1.25;
        color: #0f172a;
      }}
      .slide-h2 {{
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
        font-size: 1.5rem;
        line-height: 1.35;
        color: #be111c;
      }}
      .slide-subtitle {{
        font-size: 1.125rem;
        line-height: 1.5;
        color: #475569;
        font-style: italic;
      }}

      .bento-card {{
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease;
      }}
      .bento-card:hover {{
        border-color: #cbd5e1;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
      }}

      .slide-corner-badge {{
        position: absolute;
        right: 0;
        bottom: 0;
        width: 5.5rem;
        height: 5.5rem;
        background: #be111c;
        clip-path: polygon(100% 0, 0 100%, 100% 100%);
        display: flex;
        align-items: flex-end;
        justify-content: flex-end;
        padding: 0.75rem 1rem;
        z-index: 20;
      }}
      .slide-corner-badge span {{
        font-family: 'Montserrat', sans-serif;
        font-weight: 800;
        font-size: 1.25rem;
        color: #ffffff;
        line-height: 1;
      }}

      #speaker-notes-drawer {{
        position: fixed;
        bottom: 4.5rem;
        left: 50%;
        transform: translateX(-50%) translateY(120%);
        width: min(90%, 960px);
        background: #0f172a;
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 1rem;
        color: #f8fafc;
        padding: 1.25rem 1.75rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        z-index: 60;
        transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      }}
      #speaker-notes-drawer.open {{
        transform: translateX(-50%) translateY(0);
      }}

      .quiz-option {{
        cursor: pointer;
        transition: all 0.2s ease;
      }}
      .quiz-option:hover {{
        border-color: #be111c;
        background-color: #fff1f2;
      }}
      .quiz-option.correct {{
        border-color: #10b981 !important;
        background-color: #ecfdf5 !important;
        color: #065f46 !important;
      }}
      .quiz-option.wrong {{
        border-color: #ef4444 !important;
        background-color: #fef2f2 !important;
        color: #991b1b !important;
      }}
    </style>
  </head>
  <body>
    <!-- FIXED TOP HEADER -->
    <header class="fixed top-0 left-0 right-0 h-16 bg-white border-b border-slate-200 z-50 flex items-center justify-between px-8">
      <div class="flex items-center gap-4">
        <img
          src="https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png"
          alt="Rikkei Academy Logo"
          class="h-9 object-contain"
        />
        <div class="h-6 w-[1px] bg-slate-200 hidden sm:block"></div>
        <span class="text-sm font-bold text-slate-800 hidden sm:block">
          {module_name}
        </span>
      </div>

      <div class="hidden md:flex items-center gap-2 px-4 py-1.5 bg-slate-100 rounded-full border border-slate-200">
        <span class="w-2 h-2 rounded-full bg-rikkei-red"></span>
        <span id="header-slide-title" class="text-xs font-semibold text-slate-700">
          Slide 1: {slides[0]['title']}
        </span>
      </div>

      <div class="flex items-center gap-3">
        <span class="px-3 py-1 bg-rose-50 text-rikkei-red rounded-full text-xs font-bold border border-rose-200">
          {session_title[:15]}
        </span>
        <button
          onclick="toggleSpeakerNotes()"
          class="flex items-center gap-1.5 px-3 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-xs font-semibold transition"
          title="Bật/Tắt Ghi chú giảng viên (Phím N)"
        >
          <i class="ph-bold ph-chats-circle text-sm text-rikkei-red"></i>
          <span>Ghi chú</span>
        </button>
      </div>

      <div class="absolute bottom-0 left-0 h-[3px] bg-slate-100 w-full">
        <div id="deck-progress" class="h-full bg-rikkei-red transition-all duration-300 w-0"></div>
      </div>
    </header>

    <!-- PRESENTATION VIEWPORT -->
    <main id="presentation-viewport">
      {''.join(canvases_html)}
    </main>

    <!-- FLOATING BOTTOM TOOLBAR -->
    <nav class="fixed bottom-4 left-1/2 -translate-x-1/2 bg-white border border-slate-200 shadow-sm rounded-full px-5 py-2 z-50 flex items-center gap-4">
      <button
        onclick="prevSlide()"
        class="w-8 h-8 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-700 flex items-center justify-center transition"
        title="Slide trước (Mũi tên trái / ↑)"
      >
        <i class="ph-bold ph-caret-left text-base"></i>
      </button>

      <div class="flex items-center gap-1.5 px-3 py-1 bg-slate-50 border border-slate-200 rounded-full">
        <span id="current-slide-num" class="font-montserrat font-bold text-sm text-rikkei-red">1</span>
        <span class="text-xs text-slate-400 font-bold">/</span>
        <span id="total-slide-num" class="font-montserrat font-semibold text-xs text-slate-600">{total}</span>
      </div>

      <button
        onclick="nextSlide()"
        class="w-8 h-8 rounded-full bg-rikkei-red hover:bg-rikkei-darkred text-white flex items-center justify-center transition shadow-sm"
        title="Slide tiếp theo (Mũi tên phải / Space / ↓)"
      >
        <i class="ph-bold ph-caret-right text-base"></i>
      </button>

      <div class="h-4 w-[1px] bg-slate-200"></div>

      <button
        onclick="toggleFullScreen()"
        class="w-8 h-8 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-700 flex items-center justify-center transition"
        title="Toàn màn hình (Phím F)"
      >
        <i class="ph-bold ph-corners-out text-base" id="fullscreen-icon"></i>
      </button>

      <button
        onclick="toggleSpeakerNotes()"
        class="flex items-center gap-1 px-3 py-1.5 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold transition"
        title="Xem lời giảng mẫu (Phím N)"
      >
        <i class="ph-bold ph-chat-teardrop-text text-sm text-rikkei-red"></i>
        <span class="hidden sm:inline">Lời giảng</span>
      </button>
    </nav>

    <!-- SPEAKER NOTES DRAWER -->
    <aside id="speaker-notes-drawer" class="select-text">
      <div class="flex items-center justify-between border-b border-slate-700/60 pb-2 mb-2.5">
        <div class="flex items-center gap-2">
          <i class="ph-bold ph-broadcast text-rikkei-red text-base"></i>
          <span class="font-bold text-xs text-slate-300">Ghi chú & Lời thoại Giảng viên (Speaker Notes)</span>
        </div>
        <div class="flex items-center gap-3">
          <span id="notes-timing-badge" class="px-2 py-0.5 rounded bg-slate-800 text-[11px] font-mono text-amber-400 border border-slate-700">
            Thời lượng: ~2 phút
          </span>
          <button onclick="toggleSpeakerNotes()" class="text-slate-400 hover:text-white text-base">
            <i class="ph-bold ph-x"></i>
          </button>
        </div>
      </div>
      <p id="speaker-notes-content" class="text-sm text-slate-200 leading-relaxed font-sans"></p>
      <div class="mt-2 pt-2 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400">
        <span>Mẹo giảng: Dành thời gian tương tác hỏi học viên trước khi chuyển slide.</span>
        <span>Phím tắt: Bấm phím [N] để đóng mở</span>
      </div>
    </aside>

    <script>
      const speakerNotes = {notes_json};
      let currentSlide = 1;
      const totalSlides = {total};
      const slides = document.querySelectorAll(".slide-canvas");
      const progressEl = document.getElementById("deck-progress");
      const curNumEl = document.getElementById("current-slide-num");
      const headerTitleEl = document.getElementById("header-slide-title");
      const speakerNotesDrawer = document.getElementById("speaker-notes-drawer");
      const speakerNotesContent = document.getElementById("speaker-notes-content");
      const notesTimingBadge = document.getElementById("notes-timing-badge");

      function updateSlide(targetIndex) {{
        if (targetIndex < 1 || targetIndex > totalSlides) return;
        currentSlide = targetIndex;

        slides.forEach((s, idx) => {{
          if (idx + 1 === currentSlide) {{
            s.classList.add("active");
            s.scrollTop = 0;
            const title = s.getAttribute("data-title") || "";
            headerTitleEl.innerText = `Slide ${{currentSlide}}: ${{title}}`;
          }} else {{
            s.classList.remove("active");
          }}
        }});

        curNumEl.innerText = currentSlide;
        const progressPct = ((currentSlide - 1) / (totalSlides - 1)) * 100;
        progressEl.style.width = `${{progressPct}}%`;

        const note = speakerNotes[currentSlide];
        if (note) {{
          speakerNotesContent.innerText = note.text;
          notesTimingBadge.innerText = `Thời lượng: ${{note.timing}}`;
        }}

        // Lazy render Mermaid if present
        const activeSlide = slides[currentSlide - 1];
        if (activeSlide) {{
          const mermaidEl = activeSlide.querySelector(".mermaid");
          if (mermaidEl && !mermaidEl.hasAttribute("data-processed")) {{
            setTimeout(() => {{
              mermaid.run({{ nodes: [mermaidEl] }});
            }}, 100);
          }}
        }}
      }}

      function nextSlide() {{
        if (currentSlide < totalSlides) updateSlide(currentSlide + 1);
      }}

      function prevSlide() {{
        if (currentSlide > 1) updateSlide(currentSlide - 1);
      }}

      function toggleSpeakerNotes() {{
        speakerNotesDrawer.classList.toggle("open");
      }}

      function toggleFullScreen() {{
        const icon = document.getElementById("fullscreen-icon");
        if (!document.fullscreenElement) {{
          document.documentElement.requestFullscreen().catch(() => {{}});
          icon.classList.remove("ph-corners-out");
          icon.classList.add("ph-corners-in");
        }} else {{
          if (document.exitFullscreen) {{
            document.exitFullscreen();
            icon.classList.remove("ph-corners-in");
            icon.classList.add("ph-corners-out");
          }}
        }}
      }}

      document.addEventListener("keydown", (e) => {{
        if (e.key === "ArrowRight" || e.key === "ArrowDown" || e.key === " " || e.key === "PageDown") {{
          e.preventDefault();
          nextSlide();
        }} else if (e.key === "ArrowLeft" || e.key === "ArrowUp" || e.key === "PageUp") {{
          e.preventDefault();
          prevSlide();
        }} else if (e.key === "Home") {{
          e.preventDefault();
          updateSlide(1);
        }} else if (e.key === "End") {{
          e.preventDefault();
          updateSlide(totalSlides);
        }} else if (e.key === "n" || e.key === "N") {{
          e.preventDefault();
          toggleSpeakerNotes();
        }} else if (e.key === "f" || e.key === "F") {{
          e.preventDefault();
          toggleFullScreen();
        }}
      }});

      function selectQuizOption(element, isCorrect, quizId, letter) {{
        const container = document.getElementById(`quiz-options-${{quizId}}`);
        const feedbackBox = document.getElementById(`quiz-feedback-${{quizId}}`);
        const allOptions = container.querySelectorAll(".quiz-option");

        allOptions.forEach((opt) => {{
          opt.classList.remove("correct", "wrong");
          const icon = opt.querySelector("i");
          if (icon) icon.className = "ph-bold ph-circle text-slate-300 text-lg";
        }});

        const currentIcon = element.querySelector("i");
        const solutionText = feedbackBox.getAttribute("data-solution") || "";
        if (isCorrect) {{
          element.classList.add("correct");
          if (currentIcon) currentIcon.className = "ph-bold ph-check-circle text-emerald-600 text-lg";
          feedbackBox.className = "p-4 rounded-xl border border-emerald-300 bg-emerald-50 text-emerald-900 text-sm font-medium leading-relaxed block";
          feedbackBox.innerHTML = `<strong>Chính xác! (${{letter}}):</strong> ${{solutionText}}`;
        }} else {{
          element.classList.add("wrong");
          if (currentIcon) currentIcon.className = "ph-bold ph-x-circle text-rose-600 text-lg";
          feedbackBox.className = "p-4 rounded-xl border border-rose-300 bg-rose-50 text-rose-900 text-sm font-medium leading-relaxed block";
          feedbackBox.innerHTML = `<strong>Chưa chính xác:</strong> Hãy phân tích kỹ các yếu tố nguyên lý thị giác và cấu trúc tương tác để tìm đáp án chuẩn nhất!`;
        }}
      }}

      function revealQuizAnswer(quizId, correctLetter) {{
        const container = document.getElementById(`quiz-options-${{quizId}}`);
        const options = container.querySelectorAll(".quiz-option");
        options.forEach(opt => {{
          if (opt.innerText.trim().startsWith(correctLetter)) {{
            selectQuizOption(opt, true, quizId, correctLetter);
          }}
        }});
      }}

      updateSlide(1);
    </script>
  </body>
</html>"""

    output_html_path.parent.mkdir(parents=True, exist_ok=True)
    output_html_path.write_text(full_html, encoding="utf-8")
    print(f"  [Deck Compiler] Successfully generated {total} slides -> {output_html_path}")
    return output_html_path
