import re
import html
from typing import Tuple

def repair_mermaid_code(raw: str) -> str:
    """Repair syntax errors in Mermaid diagrams to ensure flawless browser rendering."""
    code = html.unescape(raw).strip()

    # 1. Unescape common HTML entities
    code = code.replace("&quot;", '"').replace("&gt;", '>').replace("&lt;", '<').replace("&amp;", '&')

    # 2. Fix UML stereotypes first so they aren't confused with HTML tags
    code = code.replace("<<include>>", "&laquo;include&raquo;")
    code = code.replace("<<extend>>", "&laquo;extend&raquo;")

    # 3. Fix bad arrow syntax missing opening pipe:
    # -->Text| -> -->|"Text"| or -.->Text| -> -.->|"Text"|
    def fix_arrow_missing_pipe(m):
        arrow = m.group(1)
        label = m.group(2).strip()
        label = label.replace('"', "'")
        return f'{arrow}|"{label}"|'

    code = re.sub(r'(-->|-\.->|==>)([^|\n\r]+?)\|(?=\s*[A-Za-z0-9_(\[])', fix_arrow_missing_pipe, code)

    # 4. Fix invalid generalization arrow trailing pipe:
    # --|>| -> --|>
    code = re.sub(r'--\|>\|', r'--|>', code)

    # 5. Fix arrow labels that have brackets inside pipes:
    def clean_bracket_in_pipe(m):
        content = m.group(1)
        cleaned = content.replace('["', '(').replace('"]', ')').replace('[', '(').replace(']', ')')
        return f'|"{cleaned}"|'
    code = re.sub(r'\|([^|\n]*\[[^|\n]*\][^|\n]*)\|', clean_bracket_in_pipe, code)

    # 6. Fix placeholders like <Vai trò người dùng> inside node shapes:
    code = re.sub(r'<([A-Za-zÀ-ỹ0-9\s/_-]+)>', r'[\1]', code)

    # 7. Fix unquoted parentheses in node brackets:
    def quote_parentheses_in_nodes(m):
        prefix = m.group(1)
        label = m.group(2)
        return f'{prefix}["{label}"]'
    code = re.sub(r'\b([A-Za-z0-9_]+)\[([^"\]\n]*\([^"\]\n]*\)[^"\]\n]*)\]', quote_parentheses_in_nodes, code)

    return code

def sanitize_reading_html(content: str) -> Tuple[str, bool]:
    orig = content

    # 1. Robust Mermaid.js runner with enlarged fonts and spacious layout in <head>
    mermaid_head = """  <!-- Mermaid.js for Visual Diagram Rendering -->
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <style>
    /* Large & High-Clarity Visual Diagrams */
    .mermaid {
      display: flex !important;
      justify-content: center !important;
      align-items: center !important;
      width: 100% !important;
      padding: 1.5rem 0.5rem !important;
      overflow-x: auto !important;
    }
    .mermaid svg {
      min-width: min(100%, 780px) !important;
      width: 100% !important;
      max-width: 100% !important;
      height: auto !important;
      font-size: 15px !important;
      filter: drop-shadow(0 1px 3px rgba(0,0,0,0.03));
    }
    .mermaid svg text,
    .mermaid svg .nodeLabel,
    .mermaid svg .edgeLabel,
    .mermaid svg .label {
      font-size: 15px !important;
      font-weight: 500 !important;
    }
    /* Standalone Vector SVG Diagrams */
    svg.rikkei-diagram,
    .diagram-wrap svg,
    article svg:not(.lucide):not(.ph) {
      min-width: min(100%, 750px) !important;
      max-width: 100% !important;
      height: auto !important;
    }
  </style>
  <script>
    function initMermaid() {
      if (typeof mermaid !== "undefined") {
        mermaid.initialize({
          startOnLoad: false,
          theme: 'neutral',
          fontFamily: 'Inter, sans-serif',
          fontSize: 16,
          securityLevel: 'loose',
          flowchart: {
            htmlLabels: true,
            curve: 'basis',
            useMaxWidth: false,
            nodeSpacing: 50,
            rankSpacing: 55
          },
          sequence: {
            useMaxWidth: false,
            messageFontSize: 15,
            actorFontSize: 16,
            noteFontSize: 14
          },
          er: {
            useMaxWidth: false,
            fontSize: 15
          },
          themeVariables: {
            fontSize: '15px',
            fontFamily: 'Inter, sans-serif'
          }
        });
        document.querySelectorAll('.mermaid').forEach((el, idx) => {
          mermaid.run({ nodes: [el] }).catch(err => {
            console.warn("Mermaid render error on diagram #" + (idx + 1), err);
          });
        });
      }
    }
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", initMermaid);
    } else {
      initMermaid();
    }
  </script>
</head>"""

    if "cdn.jsdelivr.net/npm/mermaid" in content:
        content = re.sub(
            r'<!-- Mermaid\.js for Visual Diagram Rendering -->.*?</head>',
            mermaid_head,
            content,
            flags=re.DOTALL
        )
    elif "</head>" in content and "mermaid" in content.lower():
        # Chỉ nạp thư viện Mermaid (kèm CSS và mã khởi tạo) khi trang THỰC SỰ có sơ đồ Mermaid.
        # Bản trước chèn vào mọi bài đọc: thêm phụ thuộc CDN và CSS !important cho cả trang không có sơ đồ.
        content = content.replace("</head>", mermaid_head, 1)

    # 2. Transform Mermaid code boxes into visual diagram containers
    def replace_mermaid_code_box(m):
        full_box = m.group(0)
        code_content = m.group(1)
        unescaped_code = html.unescape(code_content).strip()
        
        if any(unescaped_code.startswith(kw) for kw in [
            "graph ", "graph\n", "flowchart ", "flowchart\n", "sequenceDiagram", "classDiagram", "stateDiagram", "stateDiagram-v2", "erDiagram", "gantt"
        ]):
            repaired_code = repair_mermaid_code(unescaped_code)
            return f'''<div class="my-6 rounded-xl overflow-hidden border border-slate-200 bg-white shadow-sm">
  <div class="px-4 py-2.5 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
    <span class="flex items-center gap-2 font-semibold text-xs text-slate-700">
      <i class="ph-bold ph-tree-structure text-rikkei-red text-sm"></i> Sơ đồ quy trình trực quan
    </span>
    <span class="text-[11px] px-2 py-0.5 rounded bg-slate-200/70 text-slate-600 font-medium">Trực quan hóa</span>
  </div>
  <div class="p-6 overflow-x-auto flex justify-center bg-white">
    <div class="mermaid text-center">
{repaired_code}
    </div>
  </div>
</div>'''
        return full_box

    content = re.sub(
        r'<div class="my-5 rounded-xl overflow-hidden border border-slate-200 bg-slate-50 shadow-sm">\s*<div class="px-3.5 py-2 bg-slate-100/90 text-xs font-sans text-slate-700 border-b border-slate-200 flex justify-between items-center">.*?</div>\s*<pre class="m-0 overflow-x-auto"><code[^>]*>(.*?)</code></pre>\s*</div>',
        replace_mermaid_code_box,
        content,
        flags=re.DOTALL
    )

    # Also repair any existing <div class="mermaid text-center"> blocks
    def fix_existing_mermaid_div(m):
        inner_code = m.group(1)
        fixed_inner = repair_mermaid_code(inner_code)
        return f'<div class="mermaid text-center">\n{fixed_inner}\n    </div>'

    content = re.sub(
        r'<div class="mermaid text-center">(.*?)</div>',
        fix_existing_mermaid_div,
        content,
        flags=re.DOTALL
    )

    # 3. Convert specification / Gherkin BDD code boxes (remove copy button & Mac dots)
    def replace_specification_box(m):
        code_content = m.group(1)
        unescaped = html.unescape(code_content).strip()
        escaped_display = html.escape(unescaped)
        
        first_part = unescaped[:200]
        if any(kw in first_part for kw in ["Tính năng:", "Kịch bản:", "Scenario:", "Given ", "Feature:", "Giả sử"]):
            title = "Đặc tả kịch bản kiểm thử nghiệp vụ (Gherkin BDD)"
            badge = "Quy chuẩn BDD"
            icon = "ph-clipboard-text text-sky-600"
            badge_cls = "bg-sky-50 text-sky-700 border border-sky-200"
        elif any(kw in first_part for kw in ["SELECT ", "CREATE TABLE", "INSERT INTO", "UPDATE "]):
            title = "Mã truy vấn cơ sở dữ liệu (SQL)"
            badge = "Cơ sở dữ liệu"
            icon = "ph-database text-amber-600"
            badge_cls = "bg-amber-50 text-amber-700 border border-amber-200"
        elif any(kw in first_part for kw in ["git ", "npm ", "docker ", "mvn ", "mkdir "]):
            title = "Lệnh thao tác hệ thống (CLI)"
            badge = "Dòng lệnh"
            icon = "ph-terminal-window text-slate-600"
            badge_cls = "bg-slate-100 text-slate-700 border border-slate-200"
        else:
            title = "Đặc tả cấu trúc nghiệp vụ"
            badge = "Đặc tả nghiệp vụ"
            icon = "ph-file-text text-slate-600"
            badge_cls = "bg-slate-100 text-slate-700 border border-slate-200"

        return f'''<div class="my-6 rounded-xl overflow-hidden border border-slate-200 bg-white shadow-sm">
  <div class="px-4 py-2.5 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
    <span class="flex items-center gap-2 font-semibold text-xs text-slate-800">
      <i class="ph-bold {icon} text-sm"></i> {title}
    </span>
    <span class="text-[11px] px-2 py-0.5 rounded {badge_cls} font-medium">{badge}</span>
  </div>
  <div class="p-4 bg-slate-50/60 text-slate-800 font-mono text-xs overflow-x-auto leading-relaxed">
    <pre class="m-0 whitespace-pre text-slate-800 font-sans sm:font-mono">{escaped_display}</pre>
  </div>
</div>'''

    content = re.sub(
        r'<div class="my-5 rounded-xl overflow-hidden border border-slate-200 bg-slate-50 shadow-sm">\s*<div class="px-3.5 py-2 bg-slate-100/90 text-xs font-sans text-slate-700 border-b border-slate-200 flex justify-between items-center">.*?</div>\s*<pre class="m-0 overflow-x-auto"><code[^>]*>(.*?)</code></pre>\s*</div>',
        replace_specification_box,
        content,
        flags=re.DOTALL
    )

    # 4. Fix text-white on pastel backgrounds
    def fix_pastel_text(m):
        cls = m.group(1)
        cls = re.sub(r'\btext-white\b', 'text-slate-800', cls)
        return f'class="{cls}"'
    content = re.sub(r'class="([^"]*bg-(?:rose|emerald|sky|amber|indigo|blue|red|green|slate|yellow|purple)-(?:50|100)[^"]*)"', fix_pastel_text, content)

    def fix_pastel_compound(m):
        return m.group(0).replace("text-white", "text-slate-800")
    content = re.sub(r'\bbg-(?:rose|emerald|sky|amber|indigo|blue|red|green|slate|yellow|purple)-(?:50|100)(?:/[0-9]+)?\s+text-white\b', fix_pastel_compound, content)
    content = re.sub(r'\btext-white\s+bg-(?:rose|emerald|sky|amber|indigo|blue|red|green|slate|yellow|purple)-(?:50|100)(?:/[0-9]+)?\b', fix_pastel_compound, content)

    # 5. Remove leaked image prompt callouts & comments
    content = re.sub(
        r'<div class="p-4 rounded-xl border border-sky-200 bg-sky-50/60[^"]*">\s*<div class="flex items-start gap-3">.*?Mô tả chi tiết kỹ thuật tạo ảnh minh họa:.*?</div>\s*</div>\s*</div>',
        '',
        content,
        flags=re.DOTALL
    )
    content = re.sub(
        r'<div class="p-4 rounded-xl border border-sky-200 bg-sky-50/60[^"]*">\s*<div class="flex items-start gap-3">.*?Prompt tạo ảnh:.*?</div>\s*</div>\s*</div>',
        '',
        content,
        flags=re.DOTALL
    )
    content = re.sub(
        r'<p class="text-slate-600 mb-4 leading-relaxed">\s*(?:Prompt tạo ảnh:|Mô tả chi tiết kỹ thuật tạo ảnh minh họa:).*?</p>',
        '',
        content,
        flags=re.DOTALL
    )
    content = re.sub(
        r'<p class="[^"]*">\s*(?:Mô tả chi tiết kỹ thuật tạo ảnh minh họa:|Prompt tạo ảnh:|Prompt hình ảnh:)\s*.*?</p>',
        '',
        content,
        flags=re.DOTALL
    )
    def strip_prompt_comments(text):
        def repl(m):
            comment = m.group(0)
            if 'Prompt tạo ảnh' in comment or 'Mô tả chi tiết kỹ thuật tạo ảnh' in comment or 'Image Prompt' in comment:
                return ''
            return comment
        return re.sub(r'<!--[\s\S]*?-->', repl, text)

    content = strip_prompt_comments(content)

    # 6. Eliminate AI clichés & buzzwords
    replacements = [
        # Callout specific phrases
        (r'Thảm họa từ sự phân mảnh yêu cầu nghiệp vụ', 'Rủi ro khi phân mảnh yêu cầu nghiệp vụ'),
        (r'Thảm họa khi\b', 'Rủi ro lớn khi'),
        (r'thảm họa\b', 'rủi ro nghiêm trọng'),
        (r'Thảm họa\b', 'Rủi ro nghiêm trọng'),
        # Anti-pattern
        (r'\(ANTI-PATTERN\)', '(Mẫu sai lầm phổ biến)'),
        (r'\bANTI-PATTERN\b', 'Mẫu sai lầm phổ biến'),
        (r'\(BEST PRACTICE\)', '(Thực hành chuẩn mực)'),
        (r'\bBEST PRACTICE\b', 'Thực hành chuẩn mực'),
        (r'SAI LẦM:', 'Sai lầm:'),
        (r'CHUẨN HÓA:', 'Chuẩn hóa:'),
        (r'\(Anti-patterns vs Best Practices\)', '(Sai sót thường gặp và Thực hành chuẩn mực)'),
        (r'Mẫu chống khuyến nghị \(Anti-pattern\)', 'Mẫu sai lầm phổ biến'),
        (r'mẫu chống khuyến nghị \(anti-pattern\)', 'mẫu sai lầm phổ biến'),
        (r'mẫu chống khuyến nghị', 'mẫu sai lầm phổ biến'),
        (r'Mẫu chống khuyến nghị', 'Mẫu sai lầm phổ biến'),
        (r'\bAnti-pattern\b', 'Mẫu sai lầm phổ biến'),
        (r'\banti-pattern\b', 'mẫu sai lầm phổ biến'),
        (r'\bAnti-Pattern\b', 'Mẫu sai lầm phổ biến'),
        # Gotcha
        (r'\bGotcha\b', 'Lưu ý quan trọng'),
        (r'\bgotcha\b', 'lưu ý quan trọng'),
        # Bẫy
        (r'\bBẫy lỗi\b', 'Lỗi thường gặp'),
        (r'\bbẫy lỗi\b', 'lỗi thường gặp'),
        (r'\bBẫy cú pháp\b', 'Sai sót cú pháp'),
        (r'\bbẫy cú pháp\b', 'sai sót cú pháp'),
        (r'\bBẫy lập trình\b', 'Sai lầm phổ biến'),
        (r'\bbẫy lập trình\b', 'sai lầm phổ biến'),
        (r'\bBẫy hiểu nhầm\b', 'Hiểu lầm phổ biến'),
        (r'\bbẫy hiểu nhầm\b', 'hiểu lầm phổ biến'),
        (r'\bBẫy rủi ro\b', 'Rủi ro tiềm ẩn'),
        (r'\bbẫy rủi ro\b', 'rủi ro tiềm ẩn'),
        (r'\bBẫy thực tế\b', 'Sai sót thực tế'),
        (r'\bbẫy thực tế\b', 'sai sót thực tế'),
        (r'\bBẫy phổ biến\b', 'Sai sót phổ biến'),
        (r'\bbẫy phổ biến\b', 'sai sót phổ biến'),
        (r'\bBẫy\b', 'Sai sót'),
        (r'\bbẫy\b', 'sai sót'),
        # Marketing hype
        (r'\bKhám phá\b', 'Tìm hiểu'),
        (r'\bkhám phá\b', 'tìm hiểu'),
        (r'\bTìm hiểu ngay\b', 'Tìm hiểu chi tiết'),
        (r'\btìm hiểu ngay\b', 'tìm hiểu chi tiết'),
        (r'\bBí kíp\b', 'Nguyên tắc then chốt'),
        (r'\bbí kíp\b', 'nguyên tắc then chốt'),
        (r'\bTất tần tật\b', 'Tổng quan toàn diện'),
        (r'\btất tần tật\b', 'tổng quan toàn diện'),
        (r'\bThần thánh\b', 'Tối ưu'),
        (r'\bthần thánh\b', 'tối ưu'),
        (r'\bViên ngọc\b', 'Điểm sáng'),
        (r'\bviên ngọc\b', 'điểm sáng'),
        (r'\bTuyệt vời\b', 'Hiệu quả'),
        (r'\btuyệt vời\b', 'hiệu quả'),
        (r'\bBậc nhất\b', 'Hàng đầu'),
        (r'\bbậc nhất\b', 'hàng đầu'),
    ]
    for pattern, repl in replacements:
        content = re.sub(pattern, repl, content)

    return content, (content != orig)
