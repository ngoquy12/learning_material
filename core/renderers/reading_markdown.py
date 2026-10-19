"""
core/renderers/reading_markdown.py
Chuyển reading.html (bản chuẩn của pipeline) sang reading.md để sinh viên đọc/chép mã dễ dàng.

Giữ nguyên reading.html. Bỏ phần giao diện (sidebar, header, trình mô phỏng, sandbox, nút sao
chép), giữ lại tiêu đề, 5 section nội dung, khối mã và bảng.

Ngôn ngữ mặc định của khối mã KHÔNG đoán từ đường dẫn tệp: người gọi truyền vào từ tech_stack
của môn (xem agents.creators.quiz_creator.extract_lang_tag).
"""

import os
import sys
import re
import json
from bs4 import BeautifulSoup, NavigableString, Tag


def clean_inline_text(node):
    """Convert inline HTML formatting (strong, em, code, a) to Markdown."""
    if node is None:
        return ""
    if isinstance(node, NavigableString):
        return str(node)
    
    tag_name = node.name.lower()
    
    # Ignore icons or buttons inside text
    if tag_name in ['i', 'span'] and any(cls.startswith('ph-') for cls in node.get('class', [])):
        return ""
    if tag_name == 'button':
        return ""
    
    inner = "".join(clean_inline_text(child) for child in node.children)
    
    if tag_name in ['strong', 'b']:
        inner_trimmed = inner.strip()
        if not inner_trimmed:
            return ""
        lead = " " if inner.startswith(" ") else ""
        trail = " " if inner.endswith(" ") else ""
        return f"{lead}**{inner_trimmed}**{trail}"
    
    elif tag_name in ['em']:
        inner_trimmed = inner.strip()
        if not inner_trimmed:
            return ""
        lead = " " if inner.startswith(" ") else ""
        trail = " " if inner.endswith(" ") else ""
        return f"{lead}*{inner_trimmed}*{trail}"
    
    elif tag_name == 'code':
        code_text = node.get_text()
        code_text = code_text.replace('`', '\\`')
        return f"`{code_text}`"
    
    elif tag_name == 'a':
        href = node.get('href', '#')
        link_text = inner.strip()
        if not link_text:
            link_text = href
        return f"[{link_text}]({href})"
    
    elif tag_name == 'br':
        return "\n"
        
    return inner

def is_visualizer_heading(tag):
    """Check if an h3/h4 tag is a visualizer title."""
    if not isinstance(tag, Tag) or tag.name not in ['h3', 'h4']:
        return False
    text = tag.get_text().lower()
    return any(k in text for k in ["visualizer", "mô phỏng luồng thực thi", "step-by-step execution", "cơ chế vận hành từng bước"])

def is_visualizer_or_sandbox_element(tag):
    """Check if an element itself is a visualizer widget or interactive sandbox."""
    if not isinstance(tag, Tag):
        return False
        
    tag_id = tag.get("id", "").lower()
    tag_classes = " ".join(tag.get("class", [])).lower()
    
    if any(k in tag_id for k in ["viz-", "visualizer", "step-tracker", "sandbox", "pyodide", "wasm", "terminal-log"]):
        return True
        
    if any(k in tag_classes for k in ["viz-", "visualizer", "code-sandbox", "pyodide-", "interactive-tracker"]):
        return True
        
    if tag.name in ["canvas", "iframe"]:
        return True
        
    if tag.name in ["button", "input", "select"] and any(k in tag_id or k in tag_classes for k in ["viz-", "btn-run", "step", "sandbox"]):
        return True

    # If this div is a visualizer wrapper (contains viz buttons/controls BUT is not a broad container with headings)
    if tag.name == "div":
        if tag.find("h2") or tag.find("h3"):
            return False
            
        if tag.find(id=re.compile(r"viz-(btn|step|ram|display|control|state|terminal)")) or \
           tag.find(class_=re.compile(r"(viz-controls|sandbox-toolbar|interactive-toolbar)", re.I)):
            return True
            
        if tag.find(id="btn-run-code") or tag.find("button", string=re.compile(r"(Chạy code|Run code)", re.I)):
            return True
        
    return False

def is_selftest_or_question_element(tag):
    """Check if an element is a self-test assessment question or form."""
    if not isinstance(tag, Tag):
        return False
    tag_id = tag.get("id", "").lower()
    tag_classes = " ".join(tag.get("class", [])).lower()
    
    if any(k in tag_id for k in ["selftest", "self-test"]):
        return True
    if any(k in tag_classes for k in ["selftest", "self-test"]):
        return True
        
    text = tag.get_text().lower()
    if tag.name in ['h3', 'h4', 'h5'] and any(k in text for k in ["câu hỏi ôn tập", "tự đánh giá", "self-test"]):
        return True
        
    # Check for question box in Section 5
    if tag.name == 'div' and "câu hỏi ôn tập nhận thức" in text:
        return True
        
    return False

def convert_table(table_tag):
    """Convert HTML table to GitHub Flavored Markdown table."""
    rows = []
    tr_tags = table_tag.find_all("tr")
    if not tr_tags:
        return ""
        
    headers = []
    first_tr = tr_tags[0]
    th_tags = first_tr.find_all(["th", "td"])
    for th in th_tags:
        cell_text = clean_inline_text(th).strip().replace("\n", " ").replace("|", "\\|")
        headers.append(cell_text if cell_text else "---")
        
    rows.append("| " + " | ".join(headers) + " |")
    rows.append("| " + " | ".join([":---" for _ in headers]) + " |")
    
    for tr in tr_tags[1:]:
        td_tags = tr.find_all(["td", "th"])
        if not td_tags:
            continue
        cells = []
        for td in td_tags:
            cell_text = clean_inline_text(td).strip().replace("\n", "<br>").replace("|", "\\|")
            cells.append(cell_text)
        while len(cells) < len(headers):
            cells.append("")
        cells = cells[:len(headers)]
        rows.append("| " + " | ".join(cells) + " |")
        
    return "\n".join(rows) + "\n\n"

def convert_code_block(pre_tag, is_terminal_output=False, default_lang="text"):
    """Convert <pre><code> to Markdown fenced code block."""
    code_tag = pre_tag.find("code")
    raw_code = code_tag.get_text() if code_tag else pre_tag.get_text()
    raw_code = raw_code.strip("\r\n")
    if not raw_code.strip():
        return ""
    
    if is_terminal_output:
        return f"```text\n{raw_code}\n```\n\n"
        
    classes = " ".join(pre_tag.get("class", []) + (code_tag.get("class", []) if code_tag else [])).lower()
    class_tokens = classes.split()
    if any(k in classes for k in ["javascript", "language-javascript", "language-js", "js"]) or "node" in classes:
        lang = "javascript"
    elif any(k in classes for k in ["python", "language-python", "py"]):
        lang = "python"
    elif any(k in classes for k in ["bash", "terminal", "shell", "sh"]):
        lang = "bash"
    elif "mermaid" in classes:
        lang = "mermaid"
    elif "sql" in classes:
        lang = "sql"
    elif "html" in classes:
        lang = "html"
    elif "css" in classes:
        lang = "css"
    elif any(cls in ["c", "cpp", "language-c", "language-cpp"] for cls in class_tokens):
        lang = "c"
    elif any(k in classes for k in ["plaintext", "text"]):
        lang = "text"
    else:
        lang = default_lang
        
    return f"```{lang}\n{raw_code}\n```\n\n"

def convert_list(list_tag, depth=0):
    """Convert <ul> and <ol> to Markdown lists."""
    md_items = []
    is_ordered = (list_tag.name == 'ol')
    idx = 1
    indent = "  " * depth
    
    for li in list_tag.find_all("li", recursive=False):
        nested_lists = li.find_all(["ul", "ol"], recursive=False)
        
        li_copy = BeautifulSoup(str(li), "html.parser").find("li")
        for nl in li_copy.find_all(["ul", "ol"], recursive=False):
            nl.decompose()
            
        li_text = clean_inline_text(li_copy).strip()
        li_text = re.sub(r'\s+', ' ', li_text)
        
        bullet = f"{idx}. " if is_ordered else "- "
        md_items.append(f"{indent}{bullet}{li_text}")
        idx += 1
        
        for nl in nested_lists:
            nested_md = convert_list(nl, depth + 1)
            if nested_md:
                md_items.append(nested_md)
                
    return "\n".join(md_items)

def extract_selftest_from_js(html_content):
    """Extract answers and explanations dictionary from checkSelfTest() script."""
    answers = {}
    explanations = {}
    
    ans_match = re.search(r'const\s+answers\s*=\s*(\{.*?\});', html_content, re.DOTALL)
    if ans_match:
        try:
            ans_str = ans_match.group(1).replace("'", '"')
            answers = json.loads(ans_str)
        except Exception:
            for k, v in re.findall(r'["\']?(\d+)["\']?\s*:\s*["\']([A-D])["\']', ans_match.group(1)):
                answers[str(k)] = v
                
    exp_match = re.search(r'const\s+explanations\s*=\s*(\{.*?\});', html_content, re.DOTALL)
    if exp_match:
        try:
            exp_str = exp_match.group(1).replace("'", '"')
            explanations = json.loads(exp_str)
        except Exception:
            for k, v in re.findall(r'["\']?(\d+)["\']?\s*:\s*["\'](.*?)["\']\s*[,}]', exp_match.group(1)):
                explanations[str(k)] = v
                
    return answers, explanations

def convert_selftest_section(sec5_soup, raw_html):
    """Self-test section is omitted in Markdown per LMS requirements."""
    return ""

def convert_node_to_markdown(node, raw_html="", default_lang="text"):
    """Recursively convert DOM node to clean Markdown."""
    if isinstance(node, NavigableString):
        text = str(node).strip()
        return text + " " if text else ""
        
    if not isinstance(node, Tag):
        return ""
        
    if is_visualizer_or_sandbox_element(node) or is_visualizer_heading(node) or is_selftest_or_question_element(node):
        return ""
        
    tag_name = node.name.lower()
    classes = " ".join(node.get("class", []))
    node_id = node.get("id", "")
    
    if tag_name == 'h2':
        text = clean_inline_text(node).strip()
        return f"\n## {text}\n\n"
        
    elif tag_name in ['h3', 'h4']:
        text = clean_inline_text(node).strip()
        if any(k in text.lower() for k in ["câu hỏi ôn tập", "tự đánh giá", "self-test"]):
            return ""
        prefix = "###" if tag_name == 'h3' else "####"
        return f"\n{prefix} {text}\n\n"
        
    elif tag_name == 'p':
        text = clean_inline_text(node).strip()
        if not text:
            return ""
        if "italic" in classes:
            return f"*{text}*\n\n"
        return f"{text}\n\n"
        
    elif tag_name in ['ul', 'ol']:
        list_md = convert_list(node)
        return f"{list_md}\n\n" if list_md else ""
        
    elif tag_name == 'table':
        return convert_table(node)
        
    elif tag_name == 'img':
        src = node.get("src", "")
        alt = node.get("alt", "")
        if src:
            return f"![{alt}]({src})\n\n"
        return ""
        
    elif tag_name == 'pre':
        return convert_code_block(node, default_lang=default_lang)
        
    elif tag_name == 'div':
        # Self-test section
        if node_id == "selftest-section":
            return convert_selftest_section(node, raw_html)
            
        # Code block container with toolbar
        if node.find("pre", recursive=False) or (len(list(node.children)) <= 3 and node.find("pre")):
            pre = node.find("pre")
            header = node.find("div")
            header_text = header.get_text(strip=True) if header else ""
            
            is_terminal = any(k in header_text.lower() or k in classes.lower() for k in ["terminal", "kết quả", "console", "output"])
            code_md = convert_code_block(pre, is_terminal_output=is_terminal, default_lang=default_lang)
            
            if re.search(r'\b[a-zA-Z0-9_\-]+\.(c|h|py|sh|js|ts)\b', header_text):
                fname = re.search(r'\b[a-zA-Z0-9_\-]+\.(c|h|py|sh|js|ts)\b', header_text).group(0)
                return f"**Tập tin: `{fname}`**\n\n{code_md}"
            return code_md
            
        # Good vs Bad comparison box in Section 4
        is_bad_code = any(k in classes for k in ["border-rose", "bg-rose"]) and node.find("pre")
        is_good_code = any(k in classes for k in ["border-emerald", "bg-emerald"]) and node.find("pre")
        
        if is_bad_code:
            pre = node.find("pre")
            return f"**Mã nguồn lỗi (Cần tránh):**\n\n{convert_code_block(pre, default_lang=default_lang)}"
        elif is_good_code:
            pre = node.find("pre")
            return f"**Mã nguồn chuẩn (Nên áp dụng):**\n\n{convert_code_block(pre, default_lang=default_lang)}"
            
        is_callout = any(k in classes for k in ["border-sky", "bg-sky", "border-amber", "bg-amber", "border-rose", "bg-rose", "border-emerald", "bg-emerald", "border-l-4"])
        
        # Traverse children with visualizer heading and intro suppression
        inner_md = []
        skip_next_p = False
        
        for child in node.children:
            if not child.name:
                continue
                
            # Check visualizer heading
            if is_visualizer_heading(child):
                skip_next_p = True
                continue
                
            if skip_next_p and child.name == 'p':
                skip_next_p = False
                continue
            skip_next_p = False
            
            # Check visualizer container
            if is_visualizer_or_sandbox_element(child) or is_selftest_or_question_element(child):
                continue
                
            res = convert_node_to_markdown(child, raw_html, default_lang=default_lang)
            if res:
                inner_md.append(res)
                
        joined = "".join(inner_md).strip()
        if not joined:
            return ""
            
        if is_callout and not node.find("pre") and not node.find("table"):
            bq = "\n".join(["> " + line if line.strip() else ">" for line in joined.splitlines()])
            return f"{bq}\n\n"
        return f"{joined}\n\n"
        
    elif tag_name == 'section':
        inner_md = []
        skip_next_p = False
        
        for child in node.children:
            if not child.name:
                continue
            if is_visualizer_heading(child):
                skip_next_p = True
                continue
            if skip_next_p and child.name == 'p':
                skip_next_p = False
                continue
            skip_next_p = False
            
            if is_visualizer_or_sandbox_element(child) or is_selftest_or_question_element(child):
                continue
                
            res = convert_node_to_markdown(child, raw_html, default_lang=default_lang)
            if res:
                inner_md.append(res)
        return "".join(inner_md)
        
    else:
        inner_md = []
        for child in node.children:
            res = convert_node_to_markdown(child, raw_html, default_lang=default_lang)
            if res:
                inner_md.append(res)
        return "".join(inner_md)

def convert_html_to_markdown(html_path, default_lang: str = "text"):
    """Convert a single reading.html file to clean Markdown string."""
    with open(html_path, "r", encoding="utf-8", errors="ignore") as fp:
        raw_html = fp.read()
        
    soup = BeautifulSoup(raw_html, "html.parser")
    
    # 1. Extract Main Title (h1)
    h1_tag = soup.find("h1")
    if h1_tag:
        title = clean_inline_text(h1_tag).strip()
    else:
        title = soup.title.get_text().strip() if soup.title else "Bài đọc lý thuyết"
        title = re.sub(r'\s*-\s*Rikkei\s*Education.*$', '', title, flags=re.I).strip()
        
    md_doc = [f"# {title}\n\n"]
    
    # 2. Extract sections
    sections = soup.find_all("section")
    content_sections = []
    for s in sections:
        s_id = s.get("id", "")
        if s_id in ["section-1", "section-2", "section-3", "section-4", "section-5"] or re.match(r'section-[1-5]', s_id):
            content_sections.append(s)
            
    if not content_sections:
        main_container = soup.find("article") or soup.find("main") or soup.body
        if main_container:
            content_sections = main_container.find_all("section", recursive=False)
            if not content_sections:
                content_sections = [main_container]
                
    for sec in content_sections:
        sec_md = convert_node_to_markdown(sec, raw_html, default_lang=default_lang).strip()
        if not sec_md:
            continue
            
        # Clean up Section 5 heading: "5. Tài liệu tham khảo & Câu hỏi ôn tập" -> "5. Tài liệu tham khảo"
        sec_md = re.sub(r'##\s*5\.\s*Tài liệu tham khảo\s*(&|\+|và)\s*Câu hỏi ôn tập.*', '## 5. Tài liệu tham khảo', sec_md, flags=re.I)
        
        # Check if section only contains a heading and no body content
        lines = [l.strip() for l in sec_md.splitlines() if l.strip()]
        non_header_lines = [l for l in lines if not l.startswith('#')]
        if not non_header_lines:
            continue
            
        md_doc.append(sec_md + "\n\n")
            
    full_md = "".join(md_doc)
    
    # Cleanup: remove 3+ consecutive newlines -> 2
    full_md = re.sub(r'\n{3,}', '\n\n', full_md).strip() + "\n"
    
    # Cleanup leftover artifacts
    full_md = re.sub(r'thường gặp thường gặp', 'thường gặp', full_md, flags=re.I)
    full_md = re.sub(r'(?m)^\s*Sao chép\s*$', '', full_md)
    full_md = re.sub(r'(?m)^\s*Mã nguồn minh họa (C|JavaScript|Python|JS)\s*$', '', full_md, flags=re.I)
    full_md = re.sub(r'(?m)^\s*Cú pháp mẫu (C|JavaScript|Python|JS)\s*$', '', full_md, flags=re.I)
    full_md = re.sub(r'\n{3,}', '\n\n', full_md).strip() + "\n"
    
    return full_md
