import re
from bs4 import BeautifulSoup

def convert_html_table_to_markdown(html_str: str) -> str:
    """Converts raw HTML table to standard GFM Markdown table."""
    soup = BeautifulSoup(html_str, "html.parser")
    rows = soup.find_all("tr")
    if not rows:
        return html_str
    
    table_data = []
    for r in rows:
        cells = r.find_all(["th", "td"])
        row_text = []
        for c in cells:
            t = re.sub(r"\s+", " ", c.get_text().strip())
            t = t.replace("|", "&#124;")
            row_text.append(t)
        if any(row_text):
            table_data.append(row_text)
            
    if not table_data:
        return html_str
        
    num_cols = max(len(r) for r in table_data)
    for r in table_data:
        while len(r) < num_cols:
            r.append("")
            
    header = table_data[0]
    separator = [":---" for _ in range(num_cols)]
    
    md_lines = [
        "",
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(separator) + " |"
    ]
    for row in table_data[1:]:
        md_lines.append("| " + " | ".join(row) + " |")
    md_lines.append("")
    
    return "\n".join(md_lines)

def sanitize_mermaid_block(code: str) -> str:
    """Sanitizes Mermaid syntax so it renders without errors in any Markdown renderer."""
    lines = code.strip().splitlines()
    fixed_lines = []
    
    for line in lines:
        l = line.strip()
        if not l:
            continue
            
        # Keep diagram declaration and structural keywords
        if any(l.startswith(kw) for kw in [
            "flowchart", "graph", "sequenceDiagram", "classDiagram", 
            "stateDiagram", "stateDiagram-v2", "erDiagram", "gitGraph", "subgraph", "end"
        ]):
            # Check subgraph label: e.g. subgraph ID[Label with spaces or colons]
            sub_m = re.match(r'^(subgraph\s+\w+)\s*\[\s*([^"\[\]\n]+)\s*\]', l)
            if sub_m:
                l = f'{sub_m.group(1)}["{sub_m.group(2).strip()}"]'
            fixed_lines.append(l)
            continue

        # Standardize link syntax: convert 'A -- label --> B' to 'A -->|label| B'
        l = re.sub(r'\s+--\s+([^->\n]+?)\s+-->\s+', r' -->|\1| ', l)

        # Fix square brackets inside link text: e.g. -->|[Đúng: Đã đủ 5]| -> -->|"Đúng: Đã đủ 5"|
        def fix_link_text(m):
            txt = m.group(1).strip().strip('[').strip(']')
            return f'-->|"{txt}"|'
        l = re.sub(r'-->\|\[([^|\]\n]+)\]\|', fix_link_text, l)

        # Fix invalid stadium ending: ([ ... ]/) -> (["..."])
        l = re.sub(r'(\b\w+)\s*\(\[\s*["\']?(.*?)["\']?\s*\]/\)', r'\1(["\2"])', l)
        
        # Stadium nodes: ([ ... ]) -> always quote
        def quote_stadium(m):
            nid = m.group(1)
            c = m.group(2).strip().strip('"').strip("'")
            return f'{nid}(["{c}"])'
        l = re.sub(r'(\b\w+)\s*\(\[\s*["\']?(.*?)["\']?\s*\]\)', quote_stadium, l)

        # Diamond nodes: { ... } -> always quote
        def quote_diamond(m):
            nid = m.group(1)
            c = m.group(2).strip().strip('"').strip("'")
            return f'{nid}{{"{c}"}}'
        l = re.sub(r'(\b\w+)\s*\{\s*["\']?([^"{}\n]+)["\']?\s*\}', quote_diamond, l)

        # Input / Output nodes: [/ ... /]
        def quote_io(m):
            nid = m.group(1)
            c = m.group(2).strip().strip('"').strip("'")
            return f'{nid}[/"{c}"/]'
        l = re.sub(r'(\b\w+)\s*\[/\s*["\']?(.*?)["\']?\s*/\]', quote_io, l)

        # Cylinder nodes: [( ... )]
        def quote_cylinder(m):
            nid = m.group(1)
            c = m.group(2).strip().strip('"').strip("'")
            return f'{nid}[("{c}")]'
        l = re.sub(r'(\b\w+)\s*\[\(\s*["\']?(.*?)["\']?\s*\)\]', quote_cylinder, l)

        # Rectangle nodes: [ ... ] -> quote if contains colon, parens, quotes, accents, or special chars
        def quote_rect(m):
            nid = m.group(1)
            c = m.group(2).strip()
            # Already quoted or special shape
            if c.startswith('"') or c.startswith("'") or c.startswith('/') or c.startswith('('):
                return m.group(0)
            return f'{nid}["{c}"]'
        l = re.sub(r'(\b\w+)\s*\[\s*([^\[\]\n/]+)\s*\]', quote_rect, l)

        fixed_lines.append("    " + l)
        
    return "```mermaid\n" + "\n".join(fixed_lines) + "\n```"

def unwrap_all_markdown_blocks(content: str) -> str:
    """
    Finds ANY ```markdown ... ``` code block in the content and unwraps it
    into properly rendered Markdown elements (Headings, Tables, Gherkin blocks, Bash blocks).
    """
    lines = content.splitlines()
    output_lines = []
    i = 0
    in_md_block = False
    gherkin_buffer = []
    bash_buffer = []

    def flush_sub_blocks():
        nonlocal gherkin_buffer, bash_buffer, output_lines
        if gherkin_buffer:
            output_lines.append("")
            output_lines.append("```gherkin")
            output_lines.extend(gherkin_buffer)
            output_lines.append("```")
            output_lines.append("")
            gherkin_buffer = []
        if bash_buffer:
            output_lines.append("")
            output_lines.append("```bash")
            output_lines.extend(bash_buffer)
            output_lines.append("```")
            output_lines.append("")
            bash_buffer = []

    while i < len(lines):
        line = lines[i]
        l_strip = line.strip()

        # Check opening of ```markdown
        if not in_md_block and l_strip == "```markdown":
            in_md_block = True
            i += 1
            continue

        # Check closing of ```markdown
        if in_md_block and l_strip == "```":
            in_md_block = False
            flush_sub_blocks()
            i += 1
            continue

        if in_md_block:
            # Check for Gherkin keywords
            is_gherkin = any(l_strip.startswith(kw) for kw in [
                "Scenario:", "Given ", "When ", "Then ", "And ", "But ", "As a ", "I want ", "So that "
            ])
            # Check for Bash commands
            is_bash = any(l_strip.startswith(kw) for kw in [
                "mkdir ", "cd ", "git ", "touch ", "npm ", "python ", "# Tạo thư mục", "# Khởi tạo"
            ])

            if (l_strip.startswith("Scenario:") or l_strip.startswith("As a ")) and not bash_buffer:
                flush_sub_blocks()
                gherkin_buffer.append(line)
                i += 1
                continue
            elif gherkin_buffer and is_gherkin:
                gherkin_buffer.append(line)
                i += 1
                continue
            elif gherkin_buffer and (l_strip.startswith("#") or l_strip.startswith("|") or re.match(r"^\d+\.", l_strip) or l_strip.startswith("-") or not l_strip):
                flush_sub_blocks()

            if is_bash and not gherkin_buffer and not l_strip.startswith("# TÀI LIỆU") and not l_strip.startswith("# Kịch bản"):
                bash_buffer.append(line)
                i += 1
                continue
            elif bash_buffer and (l_strip.startswith("# ") or l_strip.startswith("## ") or l_strip.startswith("|") or not l_strip):
                flush_sub_blocks()

            # Format headings inside the unwrapped markdown block
            if l_strip.startswith("# "):
                output_lines.append("")
                output_lines.append("### " + l_strip[2:])
                output_lines.append("")
            elif l_strip.startswith("## "):
                output_lines.append("")
                output_lines.append("#### " + l_strip[3:])
                output_lines.append("")
            elif l_strip.startswith("### "):
                output_lines.append("")
                output_lines.append("##### " + l_strip[4:])
                output_lines.append("")
            elif l_strip.startswith("|"):
                # Table line - ensure blank line before table start
                if output_lines and not output_lines[-1].strip().startswith("|") and output_lines[-1].strip() != "":
                    output_lines.append("")
                output_lines.append(line)
            else:
                output_lines.append(line)
        else:
            output_lines.append(line)

        i += 1

    flush_sub_blocks()
    return "\n".join(output_lines)

def ensure_table_blank_lines(content: str) -> str:
    """Ensures blank lines before and after every markdown table."""
    lines = content.splitlines()
    new_lines = []
    in_code = False
    in_table = False
    
    for i, line in enumerate(lines):
        l_strip = line.strip()
        if l_strip.startswith("```"):
            in_code = not in_code
            new_lines.append(line)
            continue
            
        if in_code:
            new_lines.append(line)
            continue
            
        is_table_row = l_strip.startswith("|") and l_strip.endswith("|")
        
        if is_table_row and not in_table:
            # Table is starting!
            if new_lines and new_lines[-1].strip() != "":
                new_lines.append("")
            in_table = True
            new_lines.append(line)
        elif not is_table_row and in_table:
            # Table just ended!
            in_table = False
            if line.strip() != "":
                new_lines.append("")
            new_lines.append(line)
        else:
            new_lines.append(line)
            
    return "\n".join(new_lines)

def sanitize_headings_and_structure(content: str) -> str:
    """Sanitizes headings: space after #, remove <center>, remove lone #, ensure blank lines."""
    # 1. Clean # <center>
    content = re.sub(r"^(#{1,6})\s*<center>(.*?)</center>\s*$", r"\1 \2", content, flags=re.MULTILINE | re.IGNORECASE)

    # 2. Fix headings without space: e.g. ##Heading -> ## Heading
    content = re.sub(r"^(#{1,6})([^\s#\n][^\n]*)$", r"\1 \2", content, flags=re.MULTILINE)

    # 3. Remove lone heading lines (# or ## alone)
    lines = [l for l in content.splitlines() if l.strip() not in ["#", "##", "###", "####", "#####", "######"]]
    content = "\n".join(lines)

    # 4. Remove stray </table> or unclosed HTML tags
    content = re.sub(r"^\s*</table>\s*$", "", content, flags=re.MULTILINE | re.IGNORECASE)

    # 5. Convert raw HTML tables to Markdown
    content = re.sub(r"<table\b[^>]*>.*?</table>", lambda m: convert_html_table_to_markdown(m.group(0)), content, flags=re.DOTALL | re.IGNORECASE)

    # 6. Ensure blank lines before and after headings
    content = re.sub(r"([^\n])\n(#{1,6}\s+[^\n]+)", r"\1\n\n\2", content)
    content = re.sub(r"(#{1,6}\s+[^\n]+)\n([^\n#])", r"\1\n\n\2", content)

    # 7. Ensure blank lines around horizontal rules
    content = re.sub(r"([^\n])\n---\n", r"\1\n\n---\n\n", content)
    content = re.sub(r"\n---\n([^\n])", r"\n\n---\n\n\1", content)

    # 8. Clean redundant blank lines (3+ to 2)
    content = re.sub(r"\n{3,}", "\n\n", content)

    return content.strip() + "\n"

def sanitize_full_markdown(content: str) -> str:
    """Applies the complete suite of formatting and rendering sanitizations to markdown content."""
    if not content:
        return ""
    # Strip emojis
    content = re.sub(r'[\U00010000-\U0010ffff\u2600-\u26ff\u2700-\u27bf]', '', content)
    # Fix Mermaid blocks
    content = re.sub(r"```mermaid(.*?)```", lambda m: sanitize_mermaid_block(m.group(1)), content, flags=re.DOTALL)
    # Unwrap any ```markdown blocks
    content = unwrap_all_markdown_blocks(content)
    # Sanitize headings, tables, stray HTML tags
    content = sanitize_headings_and_structure(content)
    # Ensure tables have blank lines before and after
    content = ensure_table_blank_lines(content)
    # Final whitespace cleanup
    content = re.sub(r"\n{3,}", "\n\n", content).strip() + "\n"
    return content
