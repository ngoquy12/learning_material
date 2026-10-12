"""
Deterministic (no LLM) self-contained HTML renderer for Session-Level Mindmaps.

Input is the tree produced by ``parse_markmap_tree``. Output is ONE .html file with inline
CSS/JS only (no CDN, no network reference): light theme, horizontal collapsible tree, per-lesson
colour, search, expand/collapse all, print-friendly and responsive (outline layout on narrow
screens). Only text that exists in the parsed tree is rendered, always HTML-escaped.
"""

import re
import textwrap
from html import escape
from pathlib import Path
from typing import Any, Dict, List

# One colour per Lesson branch (cycled). Chosen for contrast on a white background.
_PALETTE = ["#2563eb", "#059669", "#d97706", "#7c3aed", "#db2777", "#0891b2", "#65a30d", "#dc2626"]
_LINK_COLOR = "#475569"
_OPEN_DEPTH = 1  # branches (###) and deeper start collapsed: overview first

_CSS = """
:root{--ink:#0f172a;--muted:#64748b;--line:#cbd5e1;--bg:#f8fafc;--card:#ffffff}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:var(--bg);color:var(--ink);font-family:Arial,"Helvetica Neue",Helvetica,sans-serif;font-size:15px;line-height:1.45}
header.bar{position:sticky;top:0;z-index:5;display:flex;flex-wrap:wrap;gap:8px;align-items:center;padding:10px 16px;background:#fff;border-bottom:1px solid var(--line)}
header.bar h1{font-size:17px;margin:0 auto 0 0;font-weight:700;min-width:0;overflow-wrap:anywhere}
header.bar input{flex:0 1 260px;min-width:120px;padding:7px 10px;border:1px solid var(--line);border-radius:8px;font:inherit}
header.bar button{padding:7px 12px;border:1px solid var(--line);border-radius:8px;background:#fff;font:inherit;cursor:pointer;color:var(--ink)}
header.bar button:hover{background:#f1f5f9}
#count{font-size:12px;color:var(--muted)}
main{padding:20px 16px 40px;overflow-x:auto;max-width:100%}
.tree{display:inline-block;min-width:min-content}
.n{display:flex;align-items:center;position:relative}
.row{display:flex;align-items:center;gap:6px;flex:none}
.box{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--c,#475569);border-radius:8px;padding:5px 10px;max-width:360px;overflow-wrap:anywhere;word-break:break-word}
.box.has{cursor:pointer}
.box .tag{display:inline-block;font-size:11px;font-weight:700;color:#fff;background:var(--c,#475569);border-radius:4px;padding:0 6px;margin-right:6px;vertical-align:1px;white-space:nowrap}
.box code{font-family:Consolas,"Courier New",monospace;font-size:13px;background:#f1f5f9;border-radius:4px;padding:0 4px}
.box pre{margin:6px 0 2px;padding:8px 10px;background:#0f172a;color:#e2e8f0;border-radius:6px;font-family:Consolas,"Courier New",monospace;font-size:12.5px;line-height:1.4;overflow-x:auto;white-space:pre;max-width:100%}
.l0>.row>.box{background:#0f172a;color:#fff;border-color:#0f172a;font-size:18px;font-weight:700;padding:10px 16px;border-left-width:1px}
.l1>.row>.box{background:var(--c);color:#fff;border-color:var(--c);font-weight:700;font-size:16px}
.l2>.row>.box{background:color-mix(in srgb,var(--c) 12%,#fff);border-color:var(--c);font-weight:700}
.tg{flex:none;width:22px;height:22px;border-radius:50%;border:1px solid var(--line);background:#fff;color:var(--muted);font-size:12px;line-height:20px;padding:0;cursor:pointer;text-align:center}
.tg:hover{background:#f1f5f9}
.leaf .tg{visibility:hidden}
.kids{display:flex;flex-direction:column;margin-left:30px;position:relative}
.kids::before{content:"";position:absolute;left:-30px;top:50%;width:30px;border-top:2px solid var(--c,var(--line))}
.kids>.n{padding:4px 0 4px 30px}
.kids>.n::before{content:"";position:absolute;left:0;top:50%;width:30px;border-top:2px solid var(--c,var(--line))}
.kids>.n::after{content:"";position:absolute;left:0;top:0;bottom:0;border-left:2px solid var(--c,var(--line))}
.kids>.n:first-child::after{top:50%}
.kids>.n:last-child::after{bottom:50%}
.kids>.n:only-child::after{display:none}
.n.closed>.kids{display:none}
.dim>.row>.box{opacity:.35}
.hit>.row>.box{outline:3px solid #facc15;opacity:1}
@media (max-width:760px){
 header.bar h1{flex-basis:100%}
 header.bar input{flex:1 1 100%}
 .tree{display:block;min-width:0}
 .n{display:block;padding:0}
 .row{align-items:flex-start;margin:3px 0}
 .kids{display:block;margin-left:12px;padding-left:10px;border-left:2px solid var(--c,var(--line))}
 .kids::before,.kids>.n::before,.kids>.n::after{display:none}
 .kids>.n{padding:0}
 .box{max-width:calc(100vw - 80px)}
 main{padding:12px 10px 32px}
}
@media print{
 header.bar{position:static}
 header.bar input,header.bar button{display:none}
 main{overflow:visible;padding:0}
 .tree{display:block;min-width:0}
 .n{display:block;padding:0;break-inside:avoid-page}
 .row{align-items:flex-start;margin:2px 0}
 .kids{display:block;margin-left:14px;padding-left:10px;border-left:2px solid var(--c,var(--line))}
 .kids::before,.kids>.n::before,.kids>.n::after{display:none}
 .kids>.n{padding:0}
 .n.closed>.kids{display:block}
 .tg{display:none}
 .box{max-width:100%;-webkit-print-color-adjust:exact;print-color-adjust:exact}
 .box pre{white-space:pre-wrap}
}
"""

_JS = """
(function(){
 var tree=document.querySelector('.tree');
 var nodes=[].slice.call(tree.querySelectorAll('.n'));
 function norm(s){return s.normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').replace(/\\u0111/g,'d').replace(/\\u0110/g,'D').toLowerCase();}
 function setOpen(n,open){
  var kids=n.querySelector(':scope>.kids'); if(!kids) return;
  n.classList.toggle('closed',!open);
  var t=n.querySelector(':scope>.row>.tg'); if(t){t.textContent=open?'\\u2212':'+';t.setAttribute('aria-expanded',open?'true':'false');}
 }
 function toggle(n){setOpen(n,n.classList.contains('closed'));}
 nodes.forEach(function(n){
  if(!n.querySelector(':scope>.kids')) return;
  setOpen(n,!n.classList.contains('closed'));
  var row=n.querySelector(':scope>.row');
  row.addEventListener('click',function(e){e.stopPropagation();toggle(n);});
 });
 document.getElementById('expand').onclick=function(){nodes.forEach(function(n){setOpen(n,true);});};
 document.getElementById('collapse').onclick=function(){nodes.forEach(function(n){
  setOpen(n,n.classList.contains('l0'));});};
 var box=document.getElementById('q'),count=document.getElementById('count');
 box.addEventListener('input',function(){
  var q=norm(box.value.trim()),hits=0;
  nodes.forEach(function(n){n.classList.remove('hit','dim');});
  if(!q){count.textContent='';return;}
  nodes.forEach(function(n){
   var b=n.querySelector(':scope>.row>.box');
   if(norm(b.textContent).indexOf(q)>=0){hits++;n.classList.add('hit');var p=n.parentElement;
    while(p&&p!==tree){if(p.classList.contains('n')) setOpen(p,true);p=p.parentElement;}}
   else n.classList.add('dim');
  });
  count.textContent=hits+' kết quả';
  var first=tree.querySelector('.hit');if(first&&first.scrollIntoView) first.scrollIntoView({block:'center',inline:'center'});
 });
})();
"""

_TAG_RE = re.compile(r'^([^:`*]{2,24}?):\s+(\S.*)$')


def _inline(text: str) -> str:
    """Escape, then apply minimal inline formatting (`code`, **bold**) on the escaped text."""
    s = escape(text, quote=True)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    return s


def _node_content(title: str, with_tag: bool) -> str:
    """Render a node title: first line = text, remaining lines (from code fences) = <pre>."""
    lines = (title or "").split("\n")
    head = lines[0].strip()
    code = textwrap.dedent("\n".join(lines[1:])).strip("\n") if len(lines) > 1 else ""
    out = ""
    if head:
        m = _TAG_RE.match(head) if with_tag else None
        if m and len(m.group(1).split()) <= 3:
            out += f'<span class="tag">{escape(m.group(1).strip())}</span>{_inline(m.group(2))}'
        else:
            out += _inline(head)
    if code:
        out += f'<pre>{escape(code)}</pre>'
    return out


def _render(node: Dict[str, Any], depth: int, color: str, lesson_idx: List[int]) -> str:
    level = node.get("level", 0)
    if depth == 1:
        if "liên kết hệ thống" in (node.get("title") or "").lower():
            color = _LINK_COLOR
        else:
            color = _PALETTE[lesson_idx[0] % len(_PALETTE)]
            lesson_idx[0] += 1
    children = node.get("children") or []
    tier = depth if depth < 2 or level == 3 else 3
    cls = f"n l{tier}"
    if not children:
        cls += " leaf"
    elif depth > _OPEN_DEPTH:
        cls += " closed"
    style = f' style="--c:{color}"' if depth == 1 else ""
    content = _node_content(node.get("title", ""), with_tag=depth >= 3 and level >= 100)
    has = " has" if children else ""
    toggle = ('<button class="tg" type="button" aria-label="Thu gọn hoặc mở rộng">−</button>'
              if children else '<span class="tg"></span>')
    kids = ""
    if children:
        kids = '<div class="kids">' + "".join(_render(c, depth + 1, color, lesson_idx) for c in children) + "</div>"
    return f'<div class="{cls}"{style}><div class="row">{toggle}<div class="box{has}">{content}</div></div>{kids}</div>'


def build_mindmap_html(tree: Dict[str, Any], output_path: Path, title: str = "") -> bool:
    """
    Writes a self-contained interactive HTML mindmap. Returns True/False; never raises, so a
    renderer failure cannot affect the already-written .md/.xmind files.
    """
    try:
        h1 = [c for c in tree.get("children", []) if c.get("level") == 1]
        if not h1:
            print("  [HTML Mindmap Warning] No root (H1) node found — skipping .html export.")
            return False
        root = h1[0]
        page_title = (title or root.get("title") or "Sơ đồ tư duy").strip()
        body = _render(root, 0, "#475569", [0])
        html = (
            '<!DOCTYPE html>\n<html lang="vi"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{escape(page_title)}</title><style>{_CSS}</style></head><body>'
            f'<header class="bar"><h1>{escape(page_title)}</h1>'
            '<input id="q" type="search" placeholder="Tìm kiếm trong sơ đồ…" aria-label="Tìm kiếm">'
            '<span id="count"></span>'
            '<button id="expand" type="button">Mở rộng tất cả</button>'
            '<button id="collapse" type="button">Thu gọn tất cả</button>'
            '<button type="button" onclick="window.print()">In</button></header>'
            f'<main><div class="tree">{body}</div></main><script>{_JS}</script></body></html>'
        )
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html, encoding="utf-8")
        return True
    except Exception as e:
        print(f"  [HTML Mindmap Warning] Failed to build .html file: {e}")
        return False
