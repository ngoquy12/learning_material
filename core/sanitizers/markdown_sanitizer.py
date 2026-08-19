"""
core/sanitizers/markdown_sanitizer.py
Markdown structure, LaTeX formula cleanup, and header normalization utilities.
"""

import re

def clean_markdown_formulas(text: str) -> str:
    """
    Sanitizes LaTeX and dollar-sign math formulas in Markdown to clean code-badged programming expressions.
    Prevents backslash escaping bugs (\frac, \text), underscore-italic collisions ($var_name$), and unrendered LaTeX tags.
    """
    if not text or not isinstance(text, str):
        return text

    # Remove \text{...} -> ...
    text = re.sub(r'\\text\{([^}]+)\}', r'\1', text)
    
    # Replace \frac{A}{B} -> (A) / (B)
    text = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', r'(\1) / (\2)', text)
    
    # Replace \times -> * and \cdot -> *
    text = re.sub(r'\\times', '*', text)
    text = re.sub(r'\\cdot', '*', text)
    
    # Process $$ formula $$ -> `formula`
    def repl_block(m):
        f = m.group(1).strip()
        f = re.sub(r'\\_', '_', f)
        return f'`{f}`'
    text = re.sub(r'\$\$(.*?)\$\$', repl_block, text, flags=re.DOTALL)
    
    # Process single dollar $var_name$ or $var\_name$ -> `var_name`
    def repl_inline(m):
        v = m.group(1).strip()
        v = re.sub(r'\\_', '_', v)
        return f'`{v}`'
    text = re.sub(r'\$([a-zA-Z_\\][a-zA-Z0-9_\\\_]*)\$', repl_inline, text)

    # Clean remaining \_ inside inline code backticks `...`
    def repl_code(m):
        c = m.group(1)
        return f'`{c.replace(r"\_", "_")}`'
    text = re.sub(r'`([^`]+)`', repl_code, text)
    
    return text

def normalize_markdown_headers(content: str) -> str:
    """
    Ensures:
    1. Every Markdown heading (#, ##, ###, ####, #####, ######) has a proper blank line before it.
    2. Every opening code fence (```lang) is placed on its own line preceded by a blank line.
    3. Every closing code fence (```) is followed by proper blank line before subsequent text/headings.
    4. Code blocks inside fences (```) are strictly protected and untouched.
    """
    if not content or not isinstance(content, str):
        return content

    parts = content.split("```")
    for i in range(len(parts)):
        if i % 2 == 0:
            # Text OUTSIDE code block
            text = parts[i]

            # Remove standalone stray '#' lines that have no title text
            text = re.sub(r'^\s*#\s*$', '', text, flags=re.MULTILINE)

            # Separate headings attached directly to preceding text
            text = re.sub(r'([^\n\r])\s*(#{1,6}\s+)', r'\1\n\n\2', text)

            lines = text.splitlines()
            fixed_lines = []
            for idx, line in enumerate(lines):
                stripped = line.strip()
                if re.match(r'^#{1,6}\s+', stripped) and idx > 0:
                    if fixed_lines and fixed_lines[-1].strip() != "":
                        fixed_lines.append("")
                fixed_lines.append(line)

            cleaned_text = "\n".join(fixed_lines)
            cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)

            # If this non-code segment precedes a code block, ensure it ends with double newlines
            if i < len(parts) - 1:
                cleaned_text = cleaned_text.rstrip() + "\n\n"
            # If this non-code segment follows a code block, ensure it starts with double newlines
            if i > 0 and cleaned_text.strip():
                cleaned_text = "\n\n" + cleaned_text.lstrip("\r\n")

            parts[i] = cleaned_text
        else:
            # Code block INSIDE fences
            code = parts[i].lstrip("\r\n")
            parts[i] = code.rstrip() + "\n"

    result = "```".join(parts)
    return result.strip() + "\n"
