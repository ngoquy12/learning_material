import sys
import re
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Root output directory containing all generated course materials
base_dir = Path(__file__).resolve().parent.parent / "output"
reading_files = list(base_dir.glob("**/Bài đọc/reading.html")) + list(base_dir.glob("**/reading.html"))

high_contrast_css = """
        /* High-Contrast Code Tracker Line Highlighting Standard (System Rule 1) */
        .code-line.active, 
        .code-line.active-line, 
        .code-line.bg-yellow-100, 
        .code-line.bg-yellow-200, 
        .code-line.bg-yellow-300, 
        .code-line.bg-amber-200 {
            background-color: #fef08a !important;
            color: #0f172a !important;
            border-left: 4px solid #eab308 !important;
            font-weight: 700 !important;
        }

        .code-line.active *, 
        .code-line.active-line *, 
        .code-line.bg-yellow-100 *, 
        .code-line.bg-yellow-200 *, 
        .code-line.bg-yellow-300 *, 
        .code-line.bg-amber-200 * {
            color: #0f172a !important;
            font-weight: 700 !important;
        }
"""

def fix_reading_html(content: str) -> str:
    # 1. Remove leaked JSON string keys
    content = re.sub(r'</div>",?\s*<p[^>]*>"analysis_title":\s*"[^"]*"</p>', '</div>', content)
    content = re.sub(r'<p[^>]*>\|[^|]*\|[^|]*\|[^|]*\|",?</p>\s*<p[^>]*>"solution_title":\s*"[^"]*"</p>', '', content)
    content = content.replace('</div>",', '</div>')
    content = re.sub(r'<div class="step-loc"[^>]*>Bản Chất Cơ Chế So Khớp Mẫu Của Thư Viện Biểu Thức Chính Quy \(Regex\)</div>', '', content)
    content = re.sub(r'<div class="step-loc"[^>]*>Giải Pháp Khớp Định Dạng Chuỗi Chuẩn Sử Dụng Mô-Đun re</div>', '', content)

    # 2. Fix broken SVG syntax
    content = content.replace('fill=" + ""none"', 'fill="none"')

    # 3. High contrast CSS injection for Code Tracker
    if "/* High-Contrast Code Tracker Line Highlighting Standard (System Rule 1) */" not in content:
        if ".code-line.active-line {" in content:
            content = content.replace(".code-line.active-line {", high_contrast_css + "\n        .code-line.active-line {")
        elif "</style>" in content:
            content = content.replace("</style>", high_contrast_css + "\n    </style>", 1)

    # 4. Convert plain console output bullet items under 'Kết quả hiển thị trên cửa sổ Console' to dark terminal component
    console_pattern = r'<li[^>]*><strong>Kết quả hiển thị trên cửa sổ Console[^<]*</strong>:?</li>\s*<ul[^>]*>\s*<li[^>]*>[^<]*</li>\s*<li[^>]*><code>([^<]+)</code></li>\s*</ul>'
    
    def _console_repl(m):
        code_str = m.group(1).strip()
        return f"""<div class="mt-4 mb-4">
    <div style="font-weight: 600; color: var(--text-main); margin-bottom: 8px;">Kết quả hiển thị trên cửa sổ Console (Terminal Output):</div>
    <div class="code-container" style="background: #0f172a; border: 1px solid #334155; border-radius: 8px; overflow: hidden;">
        <div class="code-header" style="background: #1e293b; padding: 8px 14px; border-bottom: 1px solid #334155; display: flex; align-items: center; justify-content: space-between;">
            <span style="font-family: var(--font-mono); font-size: 0.8rem; color: #38bdf8; font-weight: 600;">&gt;_ Console Output</span>
            <span style="font-size: 0.75rem; color: #10b981;">● Executed Successfully</span>
        </div>
        <div style="padding: 16px; font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 0.9rem; color: #4ade80; background: #0f172a; overflow-x: auto; white-space: pre-wrap;"><code>{code_str}</code></div>
    </div>
</div>"""

    content = re.sub(console_pattern, _console_repl, content, flags=re.IGNORECASE | re.DOTALL)

    # 5. Fix common un-accented Vietnamese words in SVG & Code Comments
    vn_map = {
        "XU LY VA DUP DU LIEU VA LOI DINH DANG": "XỬ LÝ & DỌN DẸP DỮ LIỆU VÀ LỖI ĐỊNH DẠNG",
        "Du Lieu Nguoi Dung": "Dữ liệu Người dùng",
        "Bo Loc Regex (re)": "Bộ lọc Regex (re)",
        "Reject: Dinh dang sai": "Từ chối: Định dạng sai",
        "(Bao loi he thong)": "(Báo lỗi hệ thống)",
        "Accept: Hop le": "Chấp nhận: Hợp lệ",
        "(Luu tru database)": "(Lưu trữ Database)",
        "# Khai bao cac bieu thuc chinh quy de xac thuc du lieu dau vao": "# Khai báo các biểu thức chính quy để xác thực dữ liệu đầu vào",
        "# Kiem tra xem chuoi co hop le theo dinh dang chua": "# Kiểm tra xem chuỗi có hợp lệ theo định dạng hay chưa",
        "# Kiem tra xem chuoi co hop le theo dinh dang so dien thoai Viet Nam": "# Kiểm tra xem chuỗi có hợp lệ theo định dạng số điện thoại Việt Nam",
        "# Danh sach cac mat hang cong nghe trong he thong thuong mai dien tu": "# Danh sách các mặt hàng công nghệ trong hệ thống thương mại điện tử",
        "# 1. Su dung List Comprehension de loc cac san pham dang o trang thai hoat dong co gia tren 200": "# 1. Sử dụng List Comprehension để lọc các sản phẩm đang ở trạng thái hoạt động có giá trên 200",
        "# 2. Sap xep danh sach da loc theo gia tri gia ca giam dan su dung key=lambda": "# 2. Sắp xếp danh sách đã lọc theo giá trị giá cả giảm dần sử dụng key=lambda"
    }

    for k, v in vn_map.items():
        content = content.replace(k, v)

    # 6. Convert ALL CAPS headers to Sentence case
    def _header_repl(m):
        tag_open = m.group(1)
        inner = m.group(2)
        tag_close = m.group(3)
        if inner.isupper() and len(inner.strip()) > 3:
            inner = inner.capitalize()
        return f"{tag_open}{inner}{tag_close}"

    content = re.sub(r'(<h[1-6][^>]*>)(.*?)(</h[1-6]>)', _header_repl, content, flags=re.IGNORECASE | re.DOTALL)

    return content

processed = set()
updated_count = 0

for file_path in reading_files:
    if not file_path.is_file() or file_path in processed:
        continue
    processed.add(file_path)

    try:
        raw_text = file_path.read_text(encoding='utf-8')
        fixed_text = fix_reading_html(raw_text)
        if fixed_text != raw_text:
            file_path.write_text(fixed_text, encoding='utf-8')
            updated_count += 1
            print(f"  ✓ Fixed: {file_path.relative_to(base_dir)}")
    except Exception as e:
        print(f"  ❌ Error processing {file_path}: {e}")

print(f"\n🎉 Successfully processed all reading materials. Updated {updated_count} files!")
