import os
import re
import io
import sys
from pathlib import Path
from core.session_compilers import compile_session_html
from scratch.recompile_existing_sessions import parse_all_sessions

OUTPUT_DIR = Path("output/PM_Python_Core_Synchronized")

def fix_individual_reading_file(file_path: Path):
    content = file_path.read_text(encoding="utf-8")
    original_content = content
    
    # 1. Update font variable definitions
    content = re.sub(
        r'--font-serif:\s*ui-serif,\s*Georgia,\s*"Times New Roman",\s*serif;',
        '--font-serif: \'Montserrat\', \'Inter\', sans-serif;',
        content
    )
    content = re.sub(
        r'--font-sans:\s*system-ui,\s*-apple-system,\s*"Segoe UI",\s*Roboto,\s*sans-serif;',
        '--font-sans: \'Inter\', system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;',
        content
    )
    content = re.sub(
        r'--font-mono:\s*ui-monospace,\s*"SF Mono",\s*Menlo,\s*Monaco,\s*Consolas,\s*monospace;',
        '--font-mono: \'JetBrains Mono\', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;',
        content
    )

    # 2. Update highlight.js theme to vs2015.min.css (Visual Studio Code Dark+)
    content = content.replace('styles/dracula.min.css', 'styles/vs2015.min.css')

    # Add VSCode Dark+ high fidelity styling and anti-clipping fix
    vscode_css = """        /* VSCode Dark+ Editor High-Fidelity Styling & Anti-Clipping Fix */
        .code-container {
            background-color: #1e1e1e !important;
            border-radius: 8px !important;
            border: 1px solid #333333 !important;
            overflow: hidden !important;
            margin: 20px 0 !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3) !important;
        }
        .code-header {
            background-color: #252526 !important;
            padding: 10px 16px !important;
            border-bottom: 1px solid #333333 !important;
            display: flex !important;
            justify-content: space-between !important;
            align-items: center !important;
            color: #cccccc !important;
            font-family: var(--font-sans) !important;
            font-size: 0.85rem !important;
        }
        .code-body {
            background-color: #1e1e1e !important;
            padding: 16px 20px !important;
            overflow-x: auto !important;
            overflow-y: visible !important;
        }
        .code-body pre {
            margin: 0 !important;
            padding: 0 !important;
            background-color: transparent !important;
            border: none !important;
            overflow: visible !important;
        }
        .code-body code, .code-body pre code {
            font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace !important;
            font-size: 14px !important;
            line-height: 1.7 !important;
            color: #d4d4d4 !important;
            background-color: transparent !important;
            padding: 0 !important;
            margin: 0 !important;
            display: block !important;
            overflow: visible !important;
            white-space: pre !important;
        }
        /* Exact VSCode Dark+ Syntax Highlight Theme Overrides */
        .hljs { background: #1e1e1e !important; color: #d4d4d4 !important; }
        .hljs-comment, .hljs-quote { color: #6A9955 !important; font-style: italic !important; }
        .hljs-keyword, .hljs-selector-tag { color: #569CD6 !important; font-weight: normal !important; }
        .hljs-string, .hljs-doctag { color: #CE9178 !important; }
        .hljs-number, .hljs-literal { color: #B5CEA8 !important; }
        .hljs-title, .hljs-section, .hljs-selector-id, .hljs-title.function_ { color: #DCDCAA !important; }
        .hljs-type, .hljs-class .hljs-title { color: #4EC9B0 !important; }
        .hljs-built_in, .hljs-variable { color: #9CDCFE !important; }
        .hljs-attr, .hljs-attribute { color: #9CDCFE !important; }"""

    if "/* VSCode Dark+ Editor High-Fidelity Styling" not in content:
        content = re.sub(
            r'\.code-body\s*pre,\s*\.code-body\s*code\s*\{[^}]*\}',
            vscode_css,
            content
        )

    # 3. Update .layout definition to prevent right sidebar overlap
    if ".layout {" in content:
        layout_pattern = r'\.layout\s*\{\s*display:\s*grid;\s*grid-template-columns:\s*minmax\(0,\s*1fr\)\s*280px;[^}]*\}'
        replacement_layout = (
            ".layout {\n"
            "            display: flex;\n"
            "            flex-direction: column;\n"
            "            gap: 32px;\n"
            "            width: 100%;\n"
            "        }\n"
            "        aside {\n"
            "            position: static !important;\n"
            "            display: grid;\n"
            "            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));\n"
            "            gap: 20px;\n"
            "            width: 100%;\n"
            "        }"
        )
        content = re.sub(layout_pattern, replacement_layout, content)
        # Remove any lingering sticky aside blocks
        content = re.sub(r'/\*\s*Sticky Sidebar Column\s*\*/\s*aside\s*\{[^}]*\}', '', content)

    if content != original_content:
        file_path.write_text(content, encoding="utf-8")
        return True
    return False

def main():
    print("=== STARTING FULL CURRICULUM UI & FONT SYNCHRONIZATION ===")
    
    # Step 1: Patch all individual lesson reading.html files
    patched_count = 0
    total_readings = 0
    for root, dirs, files in os.walk(OUTPUT_DIR):
        for file in files:
            if file == "reading.html":
                total_readings += 1
                fp = Path(root) / file
                if fix_individual_reading_file(fp):
                    patched_count += 1

    print(f"Patched {patched_count}/{total_readings} individual lesson reading.html files.")

    # Step 2: Recompile all sessions using core compiler
    excel_path = r"pms\PM_Python_Core_Synchronized.xlsx"
    if os.path.exists(excel_path):
        sessions = parse_all_sessions(excel_path)
        for session in sessions:
            session_id = session["session_id"]
            session_title = session["title"]
            s_dir = OUTPUT_DIR / session_id.lower().replace(" ", "_")
            if s_dir.exists():
                print(f"\nRecompiling Session: {session_id} - {session_title}")
                compile_session_html(s_dir, session_title)

    print("\n=== ALL READINGS FULLY SYNCHRONIZED ===")

if __name__ == "__main__":
    main()
