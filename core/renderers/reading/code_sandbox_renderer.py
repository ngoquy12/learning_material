"""
core/renderers/reading/code_sandbox_renderer.py
Code Sandbox & Static Card Transformer for Pyodide Wasm, JS Workers, and Static Syntax Cards.
"""

import re
import html
from typing import Dict, Any, List

LANGUAGE_MAPPING_REGISTRY = {
    "python": {"hljs": "language-python", "engine": "pyodide", "name": "Python"},
    "py": {"hljs": "language-python", "engine": "pyodide", "name": "Python"},
    "javascript": {"hljs": "language-javascript", "engine": "js_worker", "name": "JavaScript"},
    "js": {"hljs": "language-javascript", "engine": "js_worker", "name": "JavaScript"},
    "typescript": {"hljs": "language-typescript", "engine": "js_worker", "name": "TypeScript"},
    "ts": {"hljs": "language-typescript", "engine": "js_worker", "name": "TypeScript"},
    "java": {"hljs": "language-java", "engine": "code_tracker", "name": "Java"},
    "c": {"hljs": "language-c", "engine": "code_tracker", "name": "C"},
    "cpp": {"hljs": "language-cpp", "engine": "code_tracker", "name": "C++"},
    "c++": {"hljs": "language-cpp", "engine": "code_tracker", "name": "C++"},
    "sql": {"hljs": "language-sql", "engine": "sql_sim", "name": "SQL"},
    "html": {"hljs": "language-xml", "engine": "code_tracker", "name": "HTML"},
    "css": {"hljs": "language-css", "engine": "code_tracker", "name": "CSS"},
}

def resolve_language_info(tech_stack: str) -> Dict[str, str]:
    """Resolve language metadata from tech_stack string without hardcoded fallbacks."""
    if not tech_stack or not str(tech_stack).strip():
        raise ValueError("❌ [LỖI THIẾU TECHNOLOGY STACK] resolve_language_info: 'tech_stack' bị trống. Vui lòng truyền --tech-stack chính xác từ PM.")
    
    tech_lower = str(tech_stack).lower().strip()
    non_coding_keywords = [
        "git", "vcs", "github", "gitlab", "terminal", "bash", "shell", "cli", "cmd",
        "powershell", "docker", "kubernetes", "devops", "linux", "unix",
        "agile", "scrum", "diagram", "uml", "design", "word", "excel", "powerpoint",
        "office", "tin học văn phòng", "phân tích", "thiết kế", "phân tích và thiết kế",
        "phân tích thiết kế", "system analysis", "software architecture", "kiến trúc",
        "management", "devops", "pm", "theory", "concept", "process", "quy trình"
    ]
    if any(kw in tech_lower for kw in non_coding_keywords):
        is_cli = any(kw in tech_lower for kw in ["git", "vcs", "github", "gitlab", "terminal", "bash", "shell", "cli", "cmd", "powershell", "docker", "devops", "linux", "unix"])
        return {
            "hljs": "language-bash" if is_cli else "language-plaintext",
            "engine": "static",
            "name": tech_stack
        }
        
    for key, info in LANGUAGE_MAPPING_REGISTRY.items():
        if key in tech_lower:
            return info
    return {"hljs": "language-plaintext", "engine": "static", "name": tech_stack}

def get_clean_language_name(tech_stack: str) -> str:
    """Normalize tech stack string to a clean, canonical language / tool name."""
    if not tech_stack:
        return "Mã nguồn"
    t = tech_stack.lower()
    if any(k in t for k in ["typescript", "ts"]):
        return "TypeScript"
    elif any(k in t for k in ["javascript", "js", "node", "react", "vue", "next"]):
        return "JavaScript (ES6+)"
    elif any(k in t for k in ["python", "py", "django", "flask", "fastapi"]):
        return "Python 3"
    elif any(k in t for k in ["java", "spring"]):
        return "Java"
    elif "c++" in t or "cpp" in t:
        return "C++"
    elif "c#" in t or "csharp" in t or "dotnet" in t or ".net" in t:
        return "C#"
    elif "sql" in t or "mysql" in t or "postgres" in t:
        return "SQL"
    elif any(k in t for k in ["bash", "sh", "linux", "git"]):
        return "Bash/CLI"
    elif "html" in t or "css" in t:
        return "HTML/CSS"
    else:
        words = tech_stack.split()
        return words[0].capitalize() if words else "Mã nguồn"

def highlight_code_syntax(line: str, tech_stack: str = "") -> str:
    """
    Lightweight, multi-language syntax highlighter returning HTML with Tailwind CSS classes.
    """
    if not line:
        return "&nbsp;"
    
    indent_len = len(line) - len(line.lstrip())
    indent_str = line[:indent_len]
    content = line[indent_len:]
    
    if not content:
        return html.escape(line)
        
    pattern = re.compile(
        r'(?P<COMMENT>//.*$|#.*$|--.*$)|'
        r'(?P<STRING>"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'|`(?:[^`\\]|\\.)*`)|'
        r'(?P<KEYWORD>\b(?:const|let|var|function|return|def|class|if|else|elif|for|while|import|from|in|as|try|except|catch|finally|throw|new|typeof|instanceof|async|await|yield|public|private|protected|static|void|int|double|boolean|String|SELECT|FROM|WHERE|INSERT|UPDATE|DELETE|JOIN|ORDER|BY|GROUP|HAVING)\b)|'
        r'(?P<NUMBER>\b\d+(?:\.\d+)?\b)|'
        r'(?P<FUNC>\b[a-zA-Z_]\w*(?=\s*\())|'
        r'(?P<OPERATOR>=>|->|===|!==|==|!=|<=|>=|\+\+|--|\+=|-=|\*=|&&|\|\||[+\-*/%=<>!&|^~])|'
        r'(?P<IDENTIFIER>\b[a-zA-Z_$][a-zA-Z0-9_$]*\b)|'
        r'(?P<OTHER>[^\s\w]+|\s+)'
    )
    
    out_tokens = []
    pos = 0
    for m in pattern.finditer(content):
        start, end = m.span()
        if start > pos:
            out_tokens.append(html.escape(content[pos:start]))
        pos = end
        
        kind = m.lastgroup
        val = html.escape(m.group(0))
        
        if kind == "COMMENT":
            out_tokens.append(f'<span class="text-slate-400 italic">{val}</span>')
        elif kind == "STRING":
            out_tokens.append(f'<span class="text-emerald-600 font-medium">{val}</span>')
        elif kind == "KEYWORD":
            out_tokens.append(f'<span class="text-purple-600 font-bold">{val}</span>')
        elif kind == "NUMBER":
            out_tokens.append(f'<span class="text-amber-600 font-mono">{val}</span>')
        elif kind == "FUNC":
            out_tokens.append(f'<span class="text-blue-600 font-semibold">{val}</span>')
        elif kind == "OPERATOR":
            out_tokens.append(f'<span class="text-sky-600 font-bold">{val}</span>')
        elif kind == "IDENTIFIER":
            out_tokens.append(f'<span class="text-slate-800">{val}</span>')
        else:
            out_tokens.append(val)
            
    if pos < len(content):
        out_tokens.append(html.escape(content[pos:]))
        
    return html.escape(indent_str) + "".join(out_tokens)

def convert_code_to_live_sandbox(html_text: str, lang_meta: Dict[str, str], force_static: bool = False, sb_prefix: str = "sb") -> str:
    """
    Transforms code blocks into Pyodide Wasm / JS Worker Sandbox or static macOS code cards.
    """
    if not html_text:
        return ""
    
    counter = 0
    is_python = (lang_meta.get("engine") == "pyodide") and not force_static
    lang_name = lang_meta.get("name", "Code")
    is_js = (lang_meta.get("engine") == "js_worker" or lang_name in ["JavaScript", "TypeScript"]) and not force_static
    is_executable = (is_python or is_js) and not force_static
    hljs_class = lang_meta.get("hljs", "language-python")

    def create_sandbox(code_str: str) -> str:
        nonlocal counter
        counter += 1
        sb_id = f"{sb_prefix}-{counter}"
        code_clean = re.sub(r'</?(?:code|span|div|p|br|em|strong|b|i)\b[^>]*>', '', code_str)
        raw_code = html.unescape(code_clean.strip())
        
        if any(kw in raw_code for kw in ["Mã nguồn thi hành", "Mã nguồn đang thực thi", "Màn hình Console", "Màn hình in kết quả", "Chương trình sẵn sàng", "Lần lặp"]):
            return f'<div class="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">{raw_code}</div>'
            
        raw_code = re.sub(r'(:)[ \t]{4,}(\S)', r':\n    \2', raw_code)
        raw_code = re.sub(r'(#[^\n]*?)[ \t]{4,}(\S)', r'\1\n\2', raw_code)

        escaped_code = html.escape(raw_code)
        attr_code = escaped_code.replace('\n', '&#10;').replace('\r', '')

        # Detected per BLOCK, not once for the whole lesson — a single tech_stack-wide decision
        # (e.g. "this lesson is Python") previously meant EVERY code block got wrapped as an
        # executable Python sandbox regardless of what it actually contained. A Windows cmd
        # snippet or a raw SQL query embedded in a Python/JS lesson would get a "Chạy chương
        # trình" (Run) button attached and fail, since neither can run via runPythonCode/
        # runJsCode — confirmed real bug (the CLI keyword list only ever covered Unix tools).
        is_cli_cmd = any(raw_code.strip().startswith(prefix) for prefix in [
            "git ", "$ git", "$git", "docker ", "npm ", "npx ", "pip ", "cd ", "mkdir ", "curl ", "wget ", "sudo ", "chmod ", "apt ", "yum ", "systemctl ", "python -m ",
            # Windows CLI / cmd.exe
            "dir ", "dir\n", "set ", "echo off", "cls", "copy ", "del ", "ren ", "move ", "type ",
            "findstr ", "tasklist", "cmd.exe", "net user", "ipconfig", "ping ", "taskkill ",
            "where ", "attrib ", "C:\\>", "C:\\Users",
        ]) or any(cmd in raw_code.lower() for cmd in [
            "git commit", "git push", "git pull", "git checkout", "git branch", "git status", "git add", "git init", "git clone"
        ])

        is_sql_or_config = bool(re.match(
            r'^\s*(SELECT|INSERT\s+INTO|UPDATE|DELETE\s+FROM|CREATE\s+(?:TABLE|DATABASE|INDEX|VIEW)|ALTER\s+TABLE|DROP\s+TABLE)\b',
            raw_code, re.IGNORECASE
        )) or raw_code.strip().startswith('---')

        is_abstract_syntax = force_static or is_sql_or_config or any(kw in raw_code for kw in [
            "statement_block", "if_statement_block", "else_statement_block", "default_statement_block",
            "condition_1", "condition_2", "condition_3", "if condition:"
        ])

        if is_executable and not is_cli_cmd and not is_abstract_syntax:
            run_fn = "runPythonCode" if is_python else "runJsCode"
            return f'''<div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm my-5 bg-slate-50">
  <div class="relative bg-slate-50/50 text-slate-800 font-mono text-sm border-b border-slate-200">
    <div class="absolute top-2.5 right-2.5 flex items-center gap-1.5 z-10 bg-white/90 backdrop-blur px-2 py-1 rounded-md border border-slate-200 shadow-sm">
      <button onclick="clearSandbox('code-sb-{sb_id}', 'output-sb-{sb_id}', 'container-sb-{sb_id}')" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Khôi phục code gốc">
        <i class="ph-bold ph-arrow-counter-clockwise text-xs"></i>
      </button>
      <button onclick="{run_fn}('code-sb-{sb_id}', 'output-sb-{sb_id}', 'container-sb-{sb_id}')" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Chạy chương trình">
        <i class="ph-bold ph-play text-xs"></i>
      </button>
      <button onclick="copySandboxCode('code-sb-{sb_id}', this)" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Sao chép">
        <i class="ph-bold ph-copy text-xs"></i>
      </button>
    </div>
    <pre class="m-0 p-0 bg-transparent"><code id="code-sb-{sb_id}" class="{hljs_class}" contenteditable="true" spellcheck="false" data-original="{attr_code}" style="display:block; padding:0.75rem 6rem 0.75rem 0.75rem; min-height:2.5rem; outline:none !important; border:none !important; box-shadow:none !important; white-space:pre; overflow-x:auto;">{escaped_code}</code></pre>
  </div>
  <div id="container-sb-{sb_id}" class="hidden bg-slate-100/90 border-t border-slate-200 p-3.5">
    <div class="flex items-center justify-between text-xs text-slate-500 font-mono mb-1">
      <span class="text-slate-700 font-bold flex items-center gap-1.5">
        <i class="ph-bold ph-terminal text-rikkei-red"></i> KẾT QUẢ THỰC THI (CONSOLE OUTPUT):
      </span>
    </div>
    <pre id="output-sb-{sb_id}" class="font-mono text-sm text-slate-800 bg-white p-2.5 rounded-lg border border-slate-200 select-text whitespace-pre-wrap m-0 shadow-inner"></pre>
  </div>
</div>'''
        else:
            block_label = f"Cú pháp mẫu {lang_name.capitalize()}" if force_static else f"Mã nguồn minh họa {lang_name.capitalize()}"
            return f'''<div class="my-5 rounded-xl overflow-hidden border border-slate-200 bg-slate-50 shadow-sm">
  <div class="px-3.5 py-2 bg-slate-100/90 text-xs font-sans text-slate-700 border-b border-slate-200 flex justify-between items-center">
    <span class="flex items-center gap-2">
      <span class="w-3 h-3 rounded-full bg-[#ff5f56] border border-[#e0443e] inline-block shadow-sm"></span>
      <span class="w-3 h-3 rounded-full bg-[#ffbd2e] border border-[#dea123] inline-block shadow-sm"></span>
      <span class="w-3 h-3 rounded-full bg-[#27c93f] border border-[#1aab29] inline-block shadow-sm"></span>
      <span class="ml-2 font-semibold text-slate-800">{block_label}</span>
    </span>
    <button onclick="navigator.clipboard.writeText(this.closest('.my-5').querySelector('code').innerText)" class="hover:text-rikkei-red px-2.5 py-1 rounded-md bg-white border border-slate-200 text-slate-600 text-xs transition-all flex items-center gap-1 shadow-sm" title="Sao chép mã nguồn"><i class="ph-bold ph-copy text-xs"></i> Sao chép</button>
  </div>
  <pre class="m-0 overflow-x-auto"><code class="hljs {hljs_class}">{escaped_code}</code></pre>
</div>'''

    def strip_pre_wrappers(text: str) -> str:
        prev = None
        max_passes = 6
        passes = 0
        while text != prev and passes < max_passes:
            prev = text
            passes += 1
            text = re.sub(
                r'<div\s+class="(?![^"]*px-3\.5)[^"]*(?:rounded|border|bg-|shadow|overflow|p-\d|font-mono)[^"]*"[^>]*>\s*'
                r'(?:<div\s+class="(?![^"]*px-3\.5)[^"]*(?:bg-|flex|border|px-|py-|text-)[^"]*"[^>]*>(?:(?!</div>).){0,200}</div>\s*)?'
                r'(<pre\b[^>]*>(?:(?!</pre>).)*?</pre>)\s*'
                r'</div>',
                r'\1',
                text,
                flags=re.DOTALL
            )
        return text

    def convert_fake_llm_cards_to_pre(text: str) -> str:
        pattern = re.compile(
            r'<div\s+class="[^"]*rounded-xl[^"]*border[^"]*bg-slate-50[^"]*">\s*'
            r'<div\s+class="px-4\s+py-2\s+bg-slate-100[^"]*">.*?<span\s+class="[^"]*bg-[a-z]+-\d{3}".*?</div>\s*'
            r'<div\s+class="[^"]*font-mono[^"]*">(.*?)</div>\s*</div>',
            re.DOTALL | re.IGNORECASE
        )
        def replacer(m):
            code_html = m.group(1)
            code_text = code_html.replace('<br>', '\n').replace('&nbsp;', ' ')
            code_text = html.unescape(code_text)
            return f'<pre><code class="{hljs_class}">{html.escape(code_text)}</code></pre>'
        return pattern.sub(replacer, text)

    html_text = convert_fake_llm_cards_to_pre(html_text)
    html_text = strip_pre_wrappers(html_text)

    pattern_pre = re.compile(r'<pre\b[^>]*>(.*?)</pre>', re.DOTALL)
    result = pattern_pre.sub(lambda m: create_sandbox(m.group(1)), html_text)

    def strip_card_wrappers(text: str) -> str:
        STATIC_SIG = 'class="my-5 rounded-xl overflow-hidden border border-slate-200 bg-slate-50 shadow-sm"'
        SANDBOX_SIG = 'class="border border-slate-200 rounded-xl overflow-hidden shadow-sm my-5 bg-slate-50"'

        for sig in [STATIC_SIG, SANDBOX_SIG]:
            out = []
            i = 0
            while i < len(text):
                card_pos = text.find(f'<div {sig}', i)
                if card_pos == -1:
                    out.append(text[i:])
                    break

                before_chunk = text[i:card_pos]
                outer_match = re.search(
                    r'<div\s+class="(?![^"]*px-3\.5)[^"]*(?:rounded|border|bg-|shadow)[^"]*"[^>]*>\s*$',
                    before_chunk
                )
                if outer_match:
                    out.append(before_chunk[:outer_match.start()])
                    search_start = card_pos
                    depth = 0
                    j = search_start
                    card_end = -1
                    while j < len(text):
                        open_pos = text.find('<div', j)
                        close_pos = text.find('</div>', j)
                        if open_pos == -1 and close_pos == -1:
                            break
                        if open_pos != -1 and (close_pos == -1 or open_pos < close_pos):
                            depth += 1
                            j = open_pos + 4
                        else:
                            depth -= 1
                            j = close_pos + 6
                            if depth == 0:
                                card_end = j
                                break
                    if card_end == -1:
                        out.append(before_chunk)
                        out.append(text[card_pos:card_pos + len(f'<div {sig}')])
                        i = card_pos + len(f'<div {sig}')
                        continue
                    out.append(text[card_pos:card_end])
                    after = text[card_end:]
                    after_stripped = after.lstrip()
                    if after_stripped.startswith('</div>'):
                        i = card_end + (len(after) - len(after_stripped)) + 6
                    else:
                        i = card_end
                else:
                    out.append(before_chunk)
                    out.append(text[card_pos:card_pos + len(f'<div {sig}')])
                    i = card_pos + len(f'<div {sig}')
            text = ''.join(out)
        return text

    result = strip_card_wrappers(result)

    def strip_llm_card_wrappers(text: str) -> str:
        prev = None
        max_passes = 6
        passes = 0
        while text != prev and passes < max_passes:
            prev = text
            passes += 1
            text = re.sub(
                r'<div\s+class="[^"]*(?:my-4|my-6)[^"]*rounded-xl[^"]*border[^"]*(?:overflow-hidden|shadow)[^"]*"[^>]*>\s*'
                r'<div\s+class="[^"]*bg-slate-100[^"]*px-4[^"]*py-2[^"]*border-b[^"]*"[^>]*>'
                r'(?:(?!</div>).)*?'
                r'</div>\s*'
                r'(<div\s+class="my-5\s+rounded-xl[^"]*overflow-hidden[^"]*border[^"]*"[^>]*>'
                r'(?:(?!</div>\s*</div>).)*?'
                r'</div>)\s*'
                r'</div>',
                r'\1',
                text,
                flags=re.DOTALL
            )
        return text

    result = strip_llm_card_wrappers(result)
    return result
