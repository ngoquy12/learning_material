"""
core/renderers/pptx/deck_engine.py

Dynamic OOXML PowerPoint Deck Engine - ported from Create_Slide/build_deck.py.
All content is 100% data-driven from the slides_data argument.
Zero hard-coded strings. Zero LLM calls inside this module.

Supported slide types:
  cover, agenda, objectives, comparison_2col, code_right_card,
  code_trace_table, grid2x2, glossary_table, summary_2col, closing
"""
from __future__ import annotations
import os, re, shutil, sys, zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

# Design Tokens — these are DEFAULTS only. build_deck() overwrites them at build time via
# extract_design_tokens(), which scans the actual template .pptx passed in (Skill 3 Giai
# đoạn 1: trích xuất token, không hard-code cố định cho 1 template).
BRAND_COLOR    = "C00000"
BLACK          = "000000"
WHITE          = "FFFFFF"
BORDER_NEUTRAL = "D9D9D9"
BG_TINT        = "F8F9FA"
BG_DARK        = "282C34"
GRAY_TEXT      = "595959"
SUCCESS_GREEN  = "2E7D32"

# Fonts — also extracted per-template where possible.
FONT_HEADING       = "Montserrat ExtraBold"   # H1/H2 weight
FONT_HEADING_BLACK = "Montserrat Black"       # cover/closing title weight
FONT_BODY_LIGHT    = "Montserrat"             # cover subtitle / agenda label weight
FONT_BODY          = "Arial"                  # default body/table/card text
FONT_CODE          = "Consolas"               # code blocks

# Corner radius (roundRect "adj" fmla value) for normal cards — also extracted per-template.
ADJ_NORMAL = 4000
ADJ_OVAL   = 50000

# One Dark Syntax Colors
SYNTAX_KEYWORD = "C678DD"
SYNTAX_STRING  = "98C379"
SYNTAX_NUMBER  = "D19A66"
SYNTAX_FUNC    = "61AFEF"
SYNTAX_COMMENT = "5C6370"
SYNTAX_PLAIN   = "ABB2BF"

# Keys overwritten by extract_design_tokens() at build time.
_TEMPLATE_TOKEN_KEYS = (
    "BRAND_COLOR", "BORDER_NEUTRAL", "BG_TINT", "BG_DARK", "GRAY_TEXT", "SUCCESS_GREEN",
    "FONT_HEADING", "FONT_HEADING_BLACK", "FONT_BODY_LIGHT", "FONT_BODY", "FONT_CODE",
    "ADJ_NORMAL",
)


def extract_design_tokens(template_pptx_path: Union[str, Path]) -> Dict[str, Union[str, int]]:
    """
    Skill 3 — Giai đoạn 1 (Design Token Extraction): scans the given template .pptx's
    slideLayouts/*.xml for the colors, fonts, and corner-radius values actually in use
    (the declared theme1.xml often diverges from real usage — see Skill 3 §1.1), so the
    same engine renders correctly-branded decks for ANY template, not just one hard-coded
    at authoring time. Falls back to the current module defaults on any read/parse failure.
    """
    defaults: Dict[str, Union[str, int]] = {k: globals()[k] for k in _TEMPLATE_TOKEN_KEYS}
    try:
        with zipfile.ZipFile(template_pptx_path, "r") as z:
            layout_names = [n for n in z.namelist() if re.match(r"ppt/slideLayouts/slideLayout\d+\.xml$", n)]
            layout_xml = "".join(z.read(n).decode("utf-8", errors="ignore") for n in layout_names)
    except Exception:
        return defaults

    tokens = dict(defaults)

    # ── Brand color: most frequent saturated (non-neutral) srgbClr used across layouts ──
    hex_counts: Dict[str, int] = {}
    for m in re.finditer(r'<a:srgbClr val="([0-9A-Fa-f]{6})"', layout_xml):
        hexval = m.group(1).upper()
        hex_counts[hexval] = hex_counts.get(hexval, 0) + 1

    def _is_neutral(hexval: str) -> bool:
        r, g, b = int(hexval[0:2], 16), int(hexval[2:4], 16), int(hexval[4:6], 16)
        return (max(r, g, b) - min(r, g, b)) < 20  # grayscale/near-black/near-white

    brand_candidates = sorted(
        ((v, c) for v, c in hex_counts.items() if not _is_neutral(v)),
        key=lambda kv: -kv[1],
    )
    if brand_candidates:
        tokens["BRAND_COLOR"] = brand_candidates[0][0]

    # ── Fonts: heaviest-weight typeface in use = heading font ──
    typeface_counts: Dict[str, int] = {}
    for m in re.finditer(r'typeface="([^"]+)"', layout_xml):
        typeface_counts[m.group(1)] = typeface_counts.get(m.group(1), 0) + 1
    black_fonts = sorted((f for f in typeface_counts if "Black" in f), key=lambda f: -typeface_counts[f])
    bold_fonts  = sorted((f for f in typeface_counts if "ExtraBold" in f or "Bold" in f), key=lambda f: -typeface_counts[f])
    if black_fonts:
        tokens["FONT_HEADING_BLACK"] = black_fonts[0]
    if bold_fonts:
        tokens["FONT_HEADING"] = bold_fonts[0]

    # ── Corner radius: most frequent roundRect adj value in use, excluding ovals ──
    adj_counts: Dict[int, int] = {}
    for m in re.finditer(r'fmla="val (\d+)"', layout_xml):
        v = int(m.group(1))
        if v != ADJ_OVAL:
            adj_counts[v] = adj_counts.get(v, 0) + 1
    if adj_counts:
        tokens["ADJ_NORMAL"] = max(adj_counts, key=adj_counts.get)

    return tokens


class ShapeIdGenerator:
    """Per-build shape ID counter — never global state."""
    def __init__(self, start: int = 1000):
        self.current = start
    def next_id(self) -> int:
        self.current += 1
        return self.current


def xml_escape(text: str) -> str:
    if not text:
        return ""
    return (str(text).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
            .replace('"',"&quot;").replace("'","&apos;"))


# ─── Low-Level Shape Builders ──────────────────────────────────────────────

def make_h1_sp(sp_id, text, x=838200, y=509145, cx=8463742, cy=945588):
    sid = sp_id.next_id()
    return (
        f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="Title_{sid}"/>'
        f'<p:cNvSpPr txBox="1"/><p:nvPr><p:ph type="title"/></p:nvPr></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>'
        f'<p:txBody><a:bodyPr anchorCtr="0" anchor="ctr" bIns="45700" lIns="0" spcFirstLastPara="1" rIns="91425" wrap="square" tIns="45700"><a:normAutofit/></a:bodyPr>'
        f'<a:lstStyle/>'
        f'<a:p><a:pPr indent="0" lvl="0" marL="0" rtl="0" algn="l">'
        f'<a:lnSpc><a:spcPct val="150000"/></a:lnSpc>'
        f'<a:spcBef><a:spcPts val="0"/></a:spcBef>'
        f'<a:spcAft><a:spcPts val="0"/></a:spcAft><a:buNone/></a:pPr>'
        f'<a:r><a:rPr b="1" lang="vi-VN" sz="2800">'
        f'<a:solidFill><a:srgbClr val="{BRAND_COLOR}"/></a:solidFill>'
        f'<a:latin typeface="{FONT_HEADING}"/>'
        f'<a:ea typeface="{FONT_HEADING}"/>'
        f'<a:cs typeface="{FONT_HEADING}"/>'
        f'</a:rPr><a:t>{xml_escape(text)}</a:t></a:r></a:p>'
        f'</p:txBody></p:sp>'
    )


def make_h2_sp(sp_id, text, x=838200, y=1400000, cx=10600000, cy=560000):
    sid = sp_id.next_id()
    return (
        f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="H2_{sid}"/>'
        f'<p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>'
        f'<p:txBody><a:bodyPr anchorCtr="0" anchor="t" bIns="45700" lIns="0" spcFirstLastPara="1" rIns="91425" wrap="square" tIns="45700"><a:normAutofit/></a:bodyPr>'
        f'<a:lstStyle/>'
        f'<a:p><a:pPr indent="0" lvl="0" marL="0" rtl="0" algn="l">'
        f'<a:lnSpc><a:spcPct val="150000"/></a:lnSpc>'
        f'<a:spcBef><a:spcPts val="0"/></a:spcBef>'
        f'<a:spcAft><a:spcPts val="0"/></a:spcAft><a:buNone/></a:pPr>'
        f'<a:r><a:rPr b="1" lang="vi-VN" sz="2000">'
        f'<a:solidFill><a:srgbClr val="{BLACK}"/></a:solidFill>'
        f'<a:latin typeface="{FONT_HEADING}"/>'
        f'<a:ea typeface="{FONT_HEADING}"/>'
        f'<a:cs typeface="{FONT_HEADING}"/>'
        f'</a:rPr><a:t>{xml_escape(text)}</a:t></a:r></a:p>'
        f'</p:txBody></p:sp>'
    )


def make_card_sp(sp_id, x, y, cx, cy, fill_clr=None, border_clr=None, border_w=12700, adj=None):
    # NOTE: defaults resolved inside the body (not as parameter defaults) so that template
    # tokens overridden by extract_design_tokens() at build time actually take effect —
    # Python binds parameter defaults once at function-definition time, not per-call.
    if fill_clr is None:
        fill_clr = WHITE
    if border_clr is None:
        border_clr = BORDER_NEUTRAL
    if adj is None:
        adj = ADJ_NORMAL
    sid = sp_id.next_id()
    return (
        f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="CardBg_{sid}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        f'<a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val {adj}"/></a:avLst></a:prstGeom>'
        f'<a:solidFill><a:srgbClr val="{fill_clr}"/></a:solidFill>'
        f'<a:ln w="{border_w}"><a:solidFill><a:srgbClr val="{border_clr}"/></a:solidFill></a:ln>'
        f'</p:spPr></p:sp>'
    )


def make_textbox_sp(sp_id, x, y, cx, cy, paragraphs, anchor="t"):
    sid = sp_id.next_id()
    p_xmls = []
    for p in paragraphs:
        algn    = p.get("algn", "l")
        spc_aft = p.get("spcAft", 350)
        runs_xml = []
        bt = p.get("bullet", None)
        if bt is True or bt == "●":
            bu_xml      = f'<a:buClr><a:srgbClr val="{BRAND_COLOR}"/></a:buClr><a:buSzPts val="1400"/><a:buFont typeface="{FONT_BODY}"/><a:buChar char="&#x25CF;"/>'
            indent_attr = 'indent="-250000" marL="350000"'
        else:
            bu_xml      = "<a:buNone/>"
            indent_attr = 'indent="0" marL="0"'
        for r in p.get("runs", []):
            t    = r.get("text", "")
            b    = "1" if r.get("b", False) else "0"
            iv   = "1" if r.get("i", False) else "0"
            sz   = r.get("sz", 1800)
            clr  = r.get("clr", BLACK)
            font = r.get("font", FONT_BODY)
            runs_xml.append(
                f'<a:r><a:rPr b="{b}" i="{iv}" lang="vi-VN" sz="{sz}">'
                f'<a:solidFill><a:srgbClr val="{clr}"/></a:solidFill>'
                f'<a:latin typeface="{font}"/><a:ea typeface="{font}"/><a:cs typeface="{font}"/>'
                f'</a:rPr><a:t>{xml_escape(t)}</a:t></a:r>'
            )
        p_xmls.append(
            f'<a:p><a:pPr {indent_attr} lvl="0" rtl="0" algn="{algn}">'
            f'<a:lnSpc><a:spcPct val="150000"/></a:lnSpc>'
            f'<a:spcBef><a:spcPts val="0"/></a:spcBef>'
            f'<a:spcAft><a:spcPts val="{spc_aft}"/></a:spcAft>'
            f'{bu_xml}</a:pPr>{"".join(runs_xml)}</a:p>'
        )
    return (
        f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="TextBox_{sid}"/>'
        f'<p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>'
        f'<p:txBody>'
        f'<a:bodyPr anchorCtr="0" anchor="{anchor}" bIns="45700" lIns="91425" spcFirstLastPara="1" rIns="91425" wrap="square" tIns="45700"><a:normAutofit/></a:bodyPr>'
        f'<a:lstStyle/>{"".join(p_xmls)}</p:txBody></p:sp>'
    )


# ─── Code Tokenizer ───────────────────────────────────────────────────────

_KEYWORDS = {
    "let","const","var","function","return","if","else","for","while","do",
    "switch","case","break","continue","import","export","class","async","await",
    "try","catch","new","this","typeof","instanceof","null","undefined","true","false",
    "def","lambda","yield","pass","raise","except","finally","with","as","from",
    "global","nonlocal","del","assert","not","and","or","in","is","elif","print",
    "public","private","protected","static","void","int","String","boolean","double",
    "float","long","char","byte","short","extends","implements","interface","enum","super","throws",
    "SELECT","FROM","WHERE","JOIN","LEFT","RIGHT","INNER","ON","GROUP","BY","ORDER",
    "HAVING","INSERT","INTO","UPDATE","SET","DELETE","CREATE","TABLE","ALTER","DROP",
    "VALUES","AND","OR","NOT","NULL","AS","DISTINCT",
}
_PATTERN = re.compile(
    r'("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|`[^`]*`'
    r'|\b\d+\b|[a-zA-Z_$][a-zA-Z0-9_$]*|[^\s\w])'
)

def tokenize_code_line(line):
    if not line:
        return [{"t": " ", "c": SYNTAX_PLAIN}]
    s = line.strip()
    if s.startswith("//") or s.startswith("#") or s.startswith("--"):
        return [{"t": line, "c": SYNTAX_COMMENT, "i": True}]
    tokens, last_idx = [], 0
    for m in _PATTERN.finditer(line):
        start, end = m.span()
        if start > last_idx:
            tokens.append({"t": line[last_idx:start], "c": SYNTAX_PLAIN})
        val = m.group(0)
        if val in _KEYWORDS:
            tokens.append({"t": val, "c": SYNTAX_KEYWORD, "b": True})
        elif ((val.startswith('"') and val.endswith('"')) or
              (val.startswith("'") and val.endswith("'")) or
              (val.startswith("`") and val.endswith("`"))):
            tokens.append({"t": val, "c": SYNTAX_STRING})
        elif val.isdigit():
            tokens.append({"t": val, "c": SYNTAX_NUMBER})
        elif end < len(line) and line[end:end+1] == "(":
            tokens.append({"t": val, "c": SYNTAX_FUNC})
        else:
            tokens.append({"t": val, "c": SYNTAX_PLAIN})
        last_idx = end
    if last_idx < len(line):
        tokens.append({"t": line[last_idx:], "c": SYNTAX_PLAIN})
    return tokens or [{"t": line, "c": SYNTAX_PLAIN}]


def make_code_block(sp_id, x, y, cx, cy, title, code_str, lang_tag="JS"):
    shapes = [make_card_sp(sp_id, x, y, cx, cy, fill_clr=BG_DARK, border_clr=BORDER_NEUTRAL)]
    header_h = 360000
    shapes.append(make_textbox_sp(sp_id, x+100000, y+50000, cx-200000, header_h, [
        {"algn":"l","spcAft":0,"bullet":None,
         "runs":[{"text":f"{lang_tag}: {title}","b":True,"sz":1400,"clr":WHITE,"font":FONT_BODY}]}
    ]))
    code_p = []
    for line in code_str.strip().split("\n"):
        toks = tokenize_code_line(line)
        runs = [{"text":t["t"],"b":t.get("b",False),"i":t.get("i",False),
                 "sz":t.get("sz",1400),"clr":t.get("c",SYNTAX_PLAIN),"font":FONT_CODE} for t in toks]
        code_p.append({"algn":"l","spcAft":80,"bullet":None,"runs":runs})
    shapes.append(make_textbox_sp(sp_id, x+100000, y+header_h+60000, cx-200000, cy-header_h-100000, code_p))
    return "".join(shapes)


def make_table_sp(sp_id, x, y, cx, cy, headers, rows, col_widths=None):
    sid = sp_id.next_id()
    nc  = len(headers)
    if nc == 0:
        return ""
    if col_widths is None:
        cw_px = [cx // nc] * nc
    else:
        tot   = sum(col_widths)
        cw_px = [int(w*cx/tot) for w in col_widths]
    grid_xml = "".join([f'<a:gridCol w="{w}"/>' for w in cw_px])
    h_cells  = []
    for h in headers:
        h_cells.append(
            f'<a:tc><a:txBody>'
            f'<a:bodyPr anchor="ctr" lIns="91425" rIns="91425" tIns="45700" bIns="45700"/>'
            f'<a:lstStyle/><a:p>'
            f'<a:pPr algn="ctr"><a:lnSpc><a:spcPct val="120000"/></a:lnSpc><a:buNone/></a:pPr>'
            f'<a:r><a:rPr b="1" lang="vi-VN" sz="1500">'
            f'<a:solidFill><a:srgbClr val="{WHITE}"/></a:solidFill>'
            f'<a:latin typeface="{FONT_HEADING}"/></a:rPr>'
            f'<a:t>{xml_escape(h)}</a:t></a:r></a:p></a:txBody>'
            f'<a:tcPr><a:solidFill><a:srgbClr val="{BRAND_COLOR}"/></a:solidFill></a:tcPr></a:tc>'
        )
    row_xmls = [f'<a:tr h="450000">{"".join(h_cells)}</a:tr>']
    for ri, row in enumerate(rows):
        fc = BG_TINT if ri%2==1 else WHITE
        cells = []
        for cv in row:
            cells.append(
                f'<a:tc><a:txBody>'
                f'<a:bodyPr anchor="ctr" lIns="91425" rIns="91425" tIns="45700" bIns="45700"/>'
                f'<a:lstStyle/><a:p>'
                f'<a:pPr algn="l"><a:lnSpc><a:spcPct val="120000"/></a:lnSpc><a:buNone/></a:pPr>'
                f'<a:r><a:rPr lang="vi-VN" sz="1400">'
                f'<a:solidFill><a:srgbClr val="{BLACK}"/></a:solidFill>'
                f'<a:latin typeface="{FONT_BODY}"/></a:rPr>'
                f'<a:t>{xml_escape(str(cv))}</a:t></a:r></a:p></a:txBody>'
                f'<a:tcPr><a:solidFill><a:srgbClr val="{fc}"/></a:solidFill></a:tcPr></a:tc>'
            )
        row_xmls.append(f'<a:tr h="400000">{"".join(cells)}</a:tr>')
    return (
        f'<p:graphicFrame>'
        f'<p:nvGraphicFramePr>'
        f'<p:cNvPr id="{sid}" name="Table_{sid}"/>'
        f'<p:cNvGraphicFramePr><a:graphicFrameLocks noGrp="1"/></p:cNvGraphicFramePr>'
        f'<p:nvPr/></p:nvGraphicFramePr>'
        f'<p:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></p:xfrm>'
        f'<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/table">'
        f'<a:tbl><a:tblPr firstRow="1" bandRow="1"/>'
        f'<a:tblGrid>{grid_xml}</a:tblGrid>{"".join(row_xmls)}</a:tbl>'
        f'</a:graphicData></a:graphic></p:graphicFrame>'
    )


# ─── XML Slide/Notes Wrappers ──────────────────────────────────────────────

def wrap_slide_xml(shapes_xml):
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
        ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
        ' xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
        '<p:cSld><p:spTree>'
        '<p:nvGrpSpPr><p:cNvPr id="1" name="Root"/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
        '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
        '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
        f'{shapes_xml}'
        '</p:spTree></p:cSld>'
        '<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>'
    )


def make_notes_slide_xml(sp_id, notes_text):
    sid  = sp_id.next_id()
    pars = []
    for line in (notes_text or "").strip().split("\n"):
        lc = line.strip()
        if not lc:
            continue
        pars.append(
            f'<a:p><a:pPr indent="0" lvl="0" marL="0" rtl="0" algn="l">'
            f'<a:lnSpc><a:spcPct val="150000"/></a:lnSpc><a:buNone/></a:pPr>'
            f'<a:r><a:rPr lang="vi-VN" sz="1200">'
            f'<a:solidFill><a:srgbClr val="{BLACK}"/></a:solidFill>'
            f'<a:latin typeface="{FONT_BODY}"/></a:rPr>'
            f'<a:t>{xml_escape(lc)}</a:t></a:r></a:p>'
        )
    if not pars:
        pars.append('<a:p><a:r><a:rPr lang="vi-VN" sz="1200"/><a:t>Ghi chú bài giảng...</a:t></a:r></a:p>')
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<p:notes xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
        ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
        ' xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
        '<p:cSld><p:spTree>'
        '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
        '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
        '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
        f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="SldImg"/>'
        f'<p:cNvSpPr><a:spLocks noGrp="1" noRot="1" noChangeAspect="1"/></p:cNvSpPr>'
        f'<p:nvPr><p:ph type="sldImg"/></p:nvPr></p:nvSpPr><p:spPr/></p:sp>'
        f'<p:sp><p:nvSpPr><p:cNvPr id="{sid+1}" name="Notes"/>'
        f'<p:cNvSpPr txBox="1"/>'
        f'<p:nvPr><p:ph idx="1" type="body"/></p:nvPr></p:nvSpPr><p:spPr/>'
        f'<p:txBody><a:bodyPr/><a:lstStyle/>{"".join(pars)}</p:txBody></p:sp>'
        '</p:spTree></p:cSld>'
        '<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:notes>'
    )


# ─── Helpers ─────────────────────────────────────────────────────────────

def _truncate_text(text: str, max_chars: int) -> str:
    text = str(text)
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + "…"


def _items_to_paras(items, sz=1600, bold=False, max_items=5, max_chars=150):
    # Skill 2 content-density rule ("mỗi bullet ngắn gọn, tối đa 4-5 bullet/slide") enforced
    # defensively here — even when an LLM output blows past it, this keeps text inside the
    # fixed-height card instead of overflowing onto the footer (a real defect the PNG visual
    # QA step caught: an unbounded 3rd exercise bullet overran the slide bottom).
    items = list(items)[:max_items]
    result = []
    n = len(items)
    for i, item in enumerate(items):
        last = i == n-1
        if isinstance(item, str):
            result.append({"algn":"l","spcAft":0 if last else 150,"bullet":True,
                           "runs":[{"text":_truncate_text(item, max_chars),"b":bold,"sz":sz,"clr":BLACK}]})
        elif isinstance(item, dict):
            result.append({"algn":"l","spcAft":0 if last else 150,
                           "bullet":item.get("bullet",True),
                           "runs":[{"text":_truncate_text(item.get("text",""), max_chars),
                                    "b":item.get("bold",bold),
                                    "sz":item.get("sz",sz),
                                    "clr":item.get("clr",BLACK),
                                    "font":item.get("font",FONT_BODY)}]})
    return result


# ─── Slide Type Renderers ────────────────────────────────────────────────

def _render_cover(sp_id, s):
    tag   = s.get("session_tag","Session")
    title = s.get("title","")
    cname = s.get("course_name","")
    shapes = (
        f'<p:sp><p:nvSpPr><p:cNvPr id="101" name="SessionId"/>'
        f'<p:cNvSpPr txBox="1"/><p:nvPr><p:ph idx="2" type="body"/></p:nvPr></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="1562200" y="1974300"/><a:ext cx="8154600" cy="554100"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>'
        f'<p:txBody><a:bodyPr anchorCtr="0" anchor="t" bIns="45700" lIns="91425" spcFirstLastPara="1" rIns="91425" wrap="square" tIns="45700"><a:noAutofit/></a:bodyPr>'
        f'<a:lstStyle/><a:p><a:pPr indent="0" lvl="0" marL="0" rtl="0" algn="l">'
        f'<a:lnSpc><a:spcPct val="90000"/></a:lnSpc><a:buNone/></a:pPr>'
        f'<a:r><a:rPr b="1" lang="vi-VN" sz="3000"><a:solidFill><a:srgbClr val="{BRAND_COLOR}"/></a:solidFill>'
        f'<a:latin typeface="{FONT_HEADING}"/><a:ea typeface="{FONT_HEADING}"/><a:cs typeface="{FONT_HEADING}"/>'
        f'</a:rPr><a:t>{xml_escape(tag)}</a:t></a:r></a:p></p:txBody></p:sp>'

        f'<p:sp><p:nvSpPr><p:cNvPr id="102" name="CoverTitle"/>'
        f'<p:cNvSpPr txBox="1"/><p:nvPr><p:ph type="ctrTitle"/></p:nvPr></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="1697675" y="2660574"/><a:ext cx="8500000" cy="947700"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>'
        f'<p:txBody><a:bodyPr anchorCtr="0" anchor="t" bIns="0" lIns="0" spcFirstLastPara="1" rIns="0" wrap="square" tIns="0"><a:noAutofit/></a:bodyPr>'
        f'<a:lstStyle/><a:p><a:pPr indent="0" lvl="0" marL="0" rtl="0" algn="l">'
        f'<a:lnSpc><a:spcPct val="90000"/></a:lnSpc><a:buNone/></a:pPr>'
        f'<a:r><a:rPr b="1" lang="vi-VN" sz="3200"><a:solidFill><a:srgbClr val="{BLACK}"/></a:solidFill>'
        f'<a:latin typeface="{FONT_HEADING_BLACK}"/><a:ea typeface="{FONT_HEADING_BLACK}"/><a:cs typeface="{FONT_HEADING_BLACK}"/>'
        f'</a:rPr><a:t>{xml_escape(title)}</a:t></a:r></a:p></p:txBody></p:sp>'

        f'<p:sp><p:nvSpPr><p:cNvPr id="103" name="CourseModule"/>'
        f'<p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="1697669" y="3664241"/><a:ext cx="8500000" cy="360000"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>'
        f'<p:txBody><a:bodyPr anchorCtr="0" anchor="t" bIns="0" lIns="0" spcFirstLastPara="1" rIns="0" wrap="square" tIns="0"><a:noAutofit/></a:bodyPr>'
        f'<a:lstStyle/><a:p><a:pPr indent="0" lvl="0" marL="0" rtl="0" algn="l">'
        f'<a:lnSpc><a:spcPct val="90000"/></a:lnSpc><a:buNone/></a:pPr>'
        f'<a:r><a:rPr b="0" lang="vi-VN" sz="1800"><a:solidFill><a:srgbClr val="{BLACK}"/></a:solidFill>'
        f'<a:latin typeface="{FONT_BODY_LIGHT}"/><a:ea typeface="{FONT_BODY_LIGHT}"/><a:cs typeface="{FONT_BODY_LIGHT}"/>'
        f'</a:rPr><a:t>Môn học: {xml_escape(cname)}</a:t></a:r></a:p></p:txBody></p:sp>'
    )
    return shapes, "slideLayout3.xml"


def _render_agenda(sp_id, s):
    items = s.get("items", [])
    p_items = "".join([
        f'<a:p><a:pPr indent="0" lvl="0" marL="0" rtl="0" algn="l">'
        f'<a:lnSpc><a:spcPct val="150000"/></a:lnSpc>'
        f'<a:spcBef><a:spcPts val="0"/></a:spcBef>'
        f'<a:spcAft><a:spcPts val="550"/></a:spcAft><a:buNone/></a:pPr>'
        f'<a:r><a:rPr b="1" lang="vi-VN" sz="2400">'
        f'<a:solidFill><a:srgbClr val="{BLACK}"/></a:solidFill>'
        f'<a:latin typeface="{FONT_HEADING}"/><a:ea typeface="{FONT_HEADING}"/><a:cs typeface="{FONT_HEADING}"/>'
        f'</a:rPr><a:t>{xml_escape(str(item))}</a:t></a:r></a:p>'
        for item in items
    ])
    shapes = (
        f'<p:sp><p:nvSpPr><p:cNvPr id="185" name="AgendaLabel"/>'
        f'<p:cNvSpPr txBox="1"/><p:nvPr><p:ph type="title"/></p:nvPr></p:nvSpPr>'
        f'<p:spPr><a:xfrm rot="5400000"><a:off x="-1686375" y="1500953"/><a:ext cx="5085300" cy="1845300"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>'
        f'<p:txBody><a:bodyPr anchorCtr="0" anchor="b" bIns="45700" lIns="91425" spcFirstLastPara="1" rIns="91425" wrap="square" tIns="45700"><a:normAutofit/></a:bodyPr>'
        f'<a:lstStyle/><a:p><a:pPr indent="0" lvl="0" marL="0" rtl="0" algn="l">'
        f'<a:lnSpc><a:spcPct val="90000"/></a:lnSpc><a:buNone/></a:pPr>'
        f'<a:r><a:rPr lang="vi-VN"><a:solidFill><a:srgbClr val="{BRAND_COLOR}"/></a:solidFill>'
        f'<a:latin typeface="{FONT_HEADING_BLACK}"/><a:ea typeface="{FONT_HEADING_BLACK}"/><a:cs typeface="{FONT_HEADING_BLACK}"/>'
        f'</a:rPr><a:t> NỘI DUNG</a:t></a:r></a:p></p:txBody></p:sp>'

        f'<p:sp><p:nvSpPr><p:cNvPr id="184" name="AgendaList"/>'
        f'<p:cNvSpPr txBox="1"/><p:nvPr><p:ph idx="1" type="body"/></p:nvPr></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="2000000" y="1261300"/><a:ext cx="9500000" cy="4935600"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>'
        f'<p:txBody><a:bodyPr anchorCtr="0" anchor="t" bIns="45700" lIns="91425" spcFirstLastPara="1" rIns="91425" wrap="square" tIns="45700"><a:normAutofit/></a:bodyPr>'
        f'<a:lstStyle/>{p_items}</p:txBody></p:sp>'
    )
    return shapes, "slideLayout1.xml"


def _render_objectives(sp_id, s):
    h1_text = s.get("h1", "Mục tiêu bài học")
    goals   = s.get("goals", [])
    shps    = [make_h1_sp(sp_id, h1_text)]
    paras = []
    n = len(goals[:5])
    for i, g in enumerate(goals[:5]):
        paras.append({
            "algn": "l", "spcAft": 0 if i == n - 1 else 400, "bullet": None,
            "runs": [{"text": f"{i+1}.  ", "b": True, "sz": 1800, "clr": BLACK, "font": FONT_HEADING},
                     {"text": str(g), "b": False, "sz": 1800, "clr": BLACK, "font": FONT_BODY}],
        })
    shps.append(make_textbox_sp(sp_id, 980000, 1900000, 10300000, 4500000, paras))
    return "".join(shps), "slideLayout2.xml"


def _render_comparison_2col(sp_id, s):
    shps = [make_h1_sp(sp_id, s.get("h1","")), make_h2_sp(sp_id, s.get("h2",""))]
    for side, px, clr in [("left",838200,BRAND_COLOR),("right",6288200,SUCCESS_GREEN)]:
        title = s.get(f"{side}_title","")
        code  = s.get(f"{side}_code","")
        items = s.get(f"{side}_items",[])
        shps.append(make_card_sp(sp_id, px, 2000000, 5150000, 3900000, fill_clr=WHITE, border_clr=BORDER_NEUTRAL))
        paras = []
        if title:
            paras.append({"algn":"l","spcAft":250,"bullet":None,"runs":[{"text":title,"b":True,"sz":1800,"clr":clr,"font":FONT_BODY}]})
        if code:
            for cl in code.strip().split("\n")[:5]:
                paras.append({"algn":"l","spcAft":80,"bullet":None,"runs":[{"text":cl,"b":False,"sz":1400,"clr":GRAY_TEXT if side=="left" else BLACK,"font":FONT_CODE}]})
            paras.append({"algn":"l","spcAft":150,"bullet":None,"runs":[{"text":"","sz":800}]})
        paras.extend(_items_to_paras(items, sz=1600))
        shps.append(make_textbox_sp(sp_id, px+200000, 2180000, 4750000, 3500000, paras))
    return "".join(shps), "slideLayout2.xml"


def _render_code_right_card(sp_id, s):
    shps = [make_h1_sp(sp_id, s.get("h1","")), make_h2_sp(sp_id, s.get("h2",""))]
    shps.append(make_code_block(sp_id, 838200, 2000000, 5200000, 3900000,
                                s.get("code_title",""), s.get("code_snippet",""), s.get("lang_tag","JS")))
    ct = s.get("card_title","")
    ci = s.get("card_items",[])
    shps.append(make_card_sp(sp_id, 6238200, 2000000, 5200000, 3900000, fill_clr=WHITE, border_clr=BORDER_NEUTRAL))
    paras = []
    if ct:
        paras.append({"algn":"l","spcAft":250,"bullet":None,"runs":[{"text":ct,"b":True,"sz":1800,"clr":BRAND_COLOR,"font":FONT_BODY}]})
    paras.extend(_items_to_paras(ci, sz=1600))
    shps.append(make_textbox_sp(sp_id, 6438200, 2180000, 4800000, 3500000, paras))
    return "".join(shps), "slideLayout2.xml"


def _render_code_trace_table(sp_id, s):
    shps = [make_h1_sp(sp_id, s.get("h1","")), make_h2_sp(sp_id, s.get("h2",""))]
    shps.append(make_code_block(sp_id, 838200, 2000000, 4800000, 3900000,
                                s.get("code_title",""), s.get("code_snippet",""), s.get("lang_tag","JS")))
    shps.append(make_table_sp(sp_id, 5838200, 2000000, 5600000, 3900000,
                              s.get("table_headers",[]), s.get("table_rows",[]), s.get("col_widths",None)))
    return "".join(shps), "slideLayout2.xml"


def _render_grid2x2(sp_id, s):
    shps   = [make_h1_sp(sp_id, s.get("h1","")), make_h2_sp(sp_id, s.get("h2",""))]
    items  = s.get("items",[])[:4]
    coords = [(838200,2000000),(6288200,2000000),(838200,4000000),(6288200,4000000)]
    gw, gh = 5150000, 1850000
    for i, (px, py) in enumerate(coords):
        if i >= len(items): break
        it = items[i]
        shps.append(make_card_sp(sp_id, px, py, gw, gh, fill_clr=WHITE, border_clr=BORDER_NEUTRAL))
        paras = [
            {"algn":"l","spcAft":150,"bullet":None,"runs":[{"text":it.get("title",f"Mục {i+1}"),"b":True,"sz":1700,"clr":BRAND_COLOR,"font":FONT_BODY}]},
            {"algn":"l","spcAft":150,"bullet":None,"runs":[{"text":it.get("desc",""),"b":False,"sz":1500,"clr":BLACK,"font":FONT_BODY}]},
        ]
        if it.get("example"):
            paras.append({"algn":"l","spcAft":0,"bullet":None,"runs":[{"text":it["example"],"b":True,"sz":1400,"clr":GRAY_TEXT,"font":FONT_CODE}]})
        shps.append(make_textbox_sp(sp_id, px+180000, py+140000, gw-360000, gh-280000, paras))
    return "".join(shps), "slideLayout2.xml"


def _render_glossary_table(sp_id, s):
    shps = [make_h1_sp(sp_id, s.get("h1","Thuật ngữ cần nhớ")), make_h2_sp(sp_id, s.get("h2",""))]
    shps.append(make_table_sp(sp_id, 838200, 2000000, 10600000, 3900000,
                              s.get("headers",["Thuật ngữ","Tiếng Anh","Định nghĩa"]),
                              s.get("rows",[]), s.get("col_widths",None)))
    return "".join(shps), "slideLayout2.xml"


def _render_summary_2col(sp_id, s):
    shps = [make_h1_sp(sp_id, s.get("h1","")), make_h2_sp(sp_id, s.get("h2",""))]
    for side, px, clr in [("left",838200,BRAND_COLOR),("right",6288200,SUCCESS_GREEN)]:
        t = s.get(f"{side}_title","")
        items = s.get(f"{side}_items",[])
        shps.append(make_card_sp(sp_id, px, 2000000, 5150000, 3900000, fill_clr=WHITE, border_clr=BORDER_NEUTRAL))
        paras = []
        if t:
            paras.append({"algn":"l","spcAft":200,"bullet":None,"runs":[{"text":t,"b":True,"sz":1700,"clr":clr,"font":FONT_BODY}]})
        paras.extend(_items_to_paras(items, sz=1500))
        shps.append(make_textbox_sp(sp_id, px+200000, 2180000, 4750000, 3500000, paras))
    return "".join(shps), "slideLayout2.xml"


def _render_exercises(sp_id, s):
    """8th mandatory Skill 2 slide type — kept separate from summary_2col so exercises
    are never silently folded into the closing summary (see Skill 2 §3 slide-type table)."""
    shps = [make_h1_sp(sp_id, s.get("h1", "Bài tập & Tài liệu tham khảo")), make_h2_sp(sp_id, s.get("h2", ""))]
    cols = [
        ("Bài tập thực hành", s.get("exercises", []), 838200, BRAND_COLOR),
        ("Tài liệu tham khảo", s.get("references", []), 6288200, SUCCESS_GREEN),
    ]
    for title, items, px, clr in cols:
        shps.append(make_card_sp(sp_id, px, 2000000, 5150000, 3900000, fill_clr=WHITE, border_clr=BORDER_NEUTRAL))
        paras = [{"algn":"l","spcAft":200,"bullet":None,"runs":[{"text":title,"b":True,"sz":1700,"clr":clr,"font":FONT_BODY}]}]
        # Exercise/reference items tend to be long-form sentences (often with inline code) —
        # tighter caps than the generic default so 3 items reliably fit this card's height.
        paras.extend(_items_to_paras(items, sz=1400, max_items=3, max_chars=95))
        shps.append(make_textbox_sp(sp_id, px+200000, 2180000, 4750000, 3500000, paras))
    return "".join(shps), "slideLayout2.xml"


# ─── Active-Learning (Interactive) Slide ───────────────────────────────────
# Skill 2 §6 mandates >=1 interactive slide every 3-4 content slides, chosen from
# exactly these 3 patterns. The answer is deliberately NOT printed on the slide
# (it goes into speaker notes only) — printing it would defeat the in-class prompt.

_INTERACTIVE_LABELS = {
    "predict_outcome": "Hoạt động: Dự đoán kết quả",
    "find_the_bug":    "Hoạt động: Tìm lỗi sai",
    "quick_quiz":      "Hoạt động: Quiz nhanh",
}


def _render_interactive(sp_id, s):
    pattern = s.get("pattern", "quick_quiz")
    h1 = s.get("h1") or _INTERACTIVE_LABELS.get(pattern, "Hoạt động tương tác")
    shps = [make_h1_sp(sp_id, h1), make_h2_sp(sp_id, s.get("h2", ""))]

    code_snippet = s.get("code_snippet", "")
    prompt_text  = s.get("prompt", "")
    options      = s.get("options", [])

    if code_snippet:
        shps.append(make_code_block(sp_id, 838200, 2000000, 5600000, 3900000,
                                    s.get("code_title", "Code"), code_snippet, s.get("lang_tag", "JS")))
        card_x, card_w = 6638200, 4800000
    else:
        card_x, card_w = 838200, 10600000

    shps.append(make_card_sp(sp_id, card_x, 2000000, card_w, 3900000, fill_clr=WHITE, border_clr=BORDER_NEUTRAL))
    paras = []
    if prompt_text:
        paras.append({"algn":"l","spcAft":250,"bullet":None,
                      "runs":[{"text":prompt_text,"b":True,"sz":1700,"clr":BRAND_COLOR,"font":FONT_BODY}]})
    letters = "ABCDEFGH"
    for i, opt in enumerate(options[:8]):
        # Strip a leading "A." / "A)" the LLM may have already prepended, so the renderer's
        # own letter prefix never doubles up (e.g. "A. A. 15000").
        opt_text = re.sub(r'^\s*[A-Ha-h][.)]\s*', '', str(opt))
        paras.append({"algn":"l","spcAft":150,"bullet":None,
                      "runs":[{"text":f"{letters[i]}. ","b":True,"sz":1600,"clr":BLACK,"font":FONT_BODY},
                              {"text":opt_text,"b":False,"sz":1600,"clr":BLACK,"font":FONT_BODY}]})
    shps.append(make_textbox_sp(sp_id, card_x+200000, 2180000, card_w-400000, 3500000, paras))
    return "".join(shps), "slideLayout2.xml"


# ─── Flowchart / Timeline Illustrations (Skill 3 §2b) ──────────────────────
# Shape grammar per role: oval = start/end, roundRect = process, diamond = decision,
# parallelogram = I/O. Minimum spacing between shapes: >=180000 EMU.

_FLOW_GEOM = {"start": "ellipse", "end": "ellipse", "process": "roundRect",
              "decision": "diamond", "io": "parallelogram"}


def make_flow_shape_sp(sp_id, prst, x, y, cx, cy, text, fill_clr=None, border_clr=None, text_clr=None, sz=1400, bold=True):
    if fill_clr is None:
        fill_clr = WHITE
    if border_clr is None:
        border_clr = BRAND_COLOR
    if text_clr is None:
        text_clr = BLACK
    sid = sp_id.next_id()
    b = "1" if bold else "0"
    return (
        f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="Flow_{sid}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        f'<a:prstGeom prst="{prst}"><a:avLst/></a:prstGeom>'
        f'<a:solidFill><a:srgbClr val="{fill_clr}"/></a:solidFill>'
        f'<a:ln w="19050"><a:solidFill><a:srgbClr val="{border_clr}"/></a:solidFill></a:ln>'
        f'</p:spPr>'
        f'<p:txBody><a:bodyPr anchor="ctr" anchorCtr="1" wrap="square" lIns="45700" rIns="45700" tIns="22900" bIns="22900"><a:normAutofit/></a:bodyPr>'
        f'<a:lstStyle/>'
        f'<a:p><a:pPr algn="ctr"><a:lnSpc><a:spcPct val="110000"/></a:lnSpc><a:buNone/></a:pPr>'
        f'<a:r><a:rPr b="{b}" lang="vi-VN" sz="{sz}">'
        f'<a:solidFill><a:srgbClr val="{text_clr}"/></a:solidFill>'
        f'<a:latin typeface="{FONT_BODY}"/></a:rPr><a:t>{xml_escape(text)}</a:t></a:r></a:p>'
        f'</p:txBody></p:sp>'
    )


def make_connector_sp(sp_id, x1, y1, x2, y2, clr=None):
    if clr is None:
        clr = GRAY_TEXT
    sid = sp_id.next_id()
    dcx, dcy = x2 - x1, y2 - y1
    flip_h = "1" if dcx < 0 else "0"
    flip_v = "1" if dcy < 0 else "0"
    return (
        f'<p:cxnSp><p:nvCxnSpPr><p:cNvPr id="{sid}" name="Connector_{sid}"/>'
        f'<p:cNvCxnSpPr/><p:nvPr/></p:nvCxnSpPr>'
        f'<p:spPr><a:xfrm flipH="{flip_h}" flipV="{flip_v}">'
        f'<a:off x="{min(x1,x2)}" y="{min(y1,y2)}"/><a:ext cx="{abs(dcx)}" cy="{abs(dcy)}"/></a:xfrm>'
        f'<a:prstGeom prst="straightConnector1"><a:avLst/></a:prstGeom>'
        f'<a:ln w="19050"><a:solidFill><a:srgbClr val="{clr}"/></a:solidFill>'
        f'<a:tailEnd type="triangle" w="med" len="med"/></a:ln></p:spPr></p:cxnSp>'
    )


def _render_flowchart(sp_id, s):
    """Vertical flow of start/process/decision/io/end nodes with connecting arrows."""
    shps = [make_h1_sp(sp_id, s.get("h1", "")), make_h2_sp(sp_id, s.get("h2", ""))]
    nodes = s.get("nodes", [])[:7]
    if not nodes:
        return "".join(shps), "slideLayout2.xml"

    # Same content-zone convention as every other slide type (y=2000000, h=3900000) so the
    # flowchart never extends further down than its siblings and collides with the footer.
    area_x, area_y, area_w, area_h = 3200000, 2000000, 5800000, 3900000
    gap = 220000  # > 180000 EMU minimum per Skill 3 §2b.1
    n = len(nodes)
    node_h = min(750000, max(500000, (area_h - gap * (n - 1)) // n))

    y = area_y
    centers = []
    for node in nodes:
        ntype = node.get("type", "process")
        prst  = _FLOW_GEOM.get(ntype, "roundRect")
        text  = node.get("text", "")
        is_terminal = ntype in ("start", "end")
        w = int(area_w * 0.6) if is_terminal else area_w
        x = area_x + (area_w - w) // 2
        fill      = BRAND_COLOR if is_terminal else WHITE
        text_clr  = WHITE if is_terminal else BLACK
        shps.append(make_flow_shape_sp(sp_id, prst, x, y, w, node_h, text, fill_clr=fill, text_clr=text_clr))
        centers.append((x + w // 2, y, y + node_h))
        y += node_h + gap

    for i in range(len(centers) - 1):
        x_cur, _, y_bottom = centers[i]
        x_next, y_top_next, _ = centers[i + 1]
        shps.append(make_connector_sp(sp_id, x_cur, y_bottom, x_next, y_top_next))

    return "".join(shps), "slideLayout2.xml"


def _render_timeline(sp_id, s):
    """Horizontal milestone timeline with alternating above/below labels."""
    shps = [make_h1_sp(sp_id, s.get("h1", "")), make_h2_sp(sp_id, s.get("h2", ""))]
    milestones = s.get("milestones", [])[:6]
    n = len(milestones)
    if n == 0:
        return "".join(shps), "slideLayout2.xml"

    area_x, area_w = 900000, 10400000
    line_y = 3900000
    marker_r = 180000
    shps.append(make_connector_sp(sp_id, area_x, line_y, area_x + area_w, line_y, clr=BORDER_NEUTRAL))

    step = area_w // (n - 1) if n > 1 else 0
    for i, m in enumerate(milestones):
        cx_pt = area_x + (step * i if n > 1 else area_w // 2)
        shps.append(make_flow_shape_sp(
            sp_id, "ellipse", cx_pt - marker_r, line_y - marker_r, marker_r * 2, marker_r * 2,
            str(i + 1), fill_clr=BRAND_COLOR, text_clr=WHITE, sz=1200,
        ))
        label = m.get("label", "") if isinstance(m, dict) else str(m)
        desc  = m.get("desc", "") if isinstance(m, dict) else ""
        above = (i % 2 == 0)
        ty = line_y - 900000 if above else line_y + marker_r + 120000
        paras = [{"algn":"ctr","spcAft":80,"bullet":None,"runs":[{"text":label,"b":True,"sz":1500,"clr":BRAND_COLOR,"font":FONT_BODY}]}]
        if desc:
            paras.append({"algn":"ctr","spcAft":0,"bullet":None,"runs":[{"text":desc,"b":False,"sz":1300,"clr":BLACK,"font":FONT_BODY}]})
        shps.append(make_textbox_sp(sp_id, cx_pt - 900000, ty, 1800000, 700000, paras, anchor="t" if not above else "b"))

    return "".join(shps), "slideLayout2.xml"


def _make_ctr_title_sp(sp_id, text, x=279991, y=3969209, cx=9144000, cy=1464417, sz=3600, clr=None, font=None):
    if clr is None:
        clr = WHITE
    if font is None:
        font = FONT_HEADING_BLACK
    sid = sp_id.next_id()
    return (
        f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="ClosingTitle_{sid}"/>'
        f'<p:cNvSpPr txBox="1"/><p:nvPr><p:ph type="ctrTitle"/></p:nvPr></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>'
        f'<p:txBody><a:bodyPr anchorCtr="0" anchor="b" bIns="45700" lIns="91425" spcFirstLastPara="1" rIns="91425" wrap="square" tIns="45700"><a:normAutofit/></a:bodyPr>'
        f'<a:lstStyle/>'
        f'<a:p><a:pPr indent="0" lvl="0" marL="0" rtl="0" algn="l">'
        f'<a:lnSpc><a:spcPct val="90000"/></a:lnSpc><a:buNone/></a:pPr>'
        f'<a:r><a:rPr b="1" lang="vi-VN" sz="{sz}">'
        f'<a:solidFill><a:srgbClr val="{clr}"/></a:solidFill>'
        f'<a:latin typeface="{font}"/><a:ea typeface="{font}"/><a:cs typeface="{font}"/>'
        f'</a:rPr><a:t>{xml_escape(text)}</a:t></a:r></a:p>'
        f'</p:txBody></p:sp>'
    )


def _make_sub_title_sp(sp_id, text, x=279991, y=5433627, cx=9144000, cy=1655762, sz=1600, clr=None):
    if clr is None:
        clr = WHITE
    sid = sp_id.next_id()
    return (
        f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="ClosingSubtitle_{sid}"/>'
        f'<p:cNvSpPr txBox="1"/><p:nvPr><p:ph idx="1" type="subTitle"/></p:nvPr></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>'
        f'<p:txBody><a:bodyPr anchorCtr="0" anchor="t" bIns="45700" lIns="91425" spcFirstLastPara="1" rIns="91425" wrap="square" tIns="45700"><a:normAutofit/></a:bodyPr>'
        f'<a:lstStyle/>'
        f'<a:p><a:pPr indent="0" lvl="0" marL="0" rtl="0" algn="l">'
        f'<a:lnSpc><a:spcPct val="90000"/></a:lnSpc><a:buNone/></a:pPr>'
        f'<a:r><a:rPr lang="vi-VN" sz="{sz}">'
        f'<a:solidFill><a:srgbClr val="{clr}"/></a:solidFill>'
        f'<a:latin typeface="{FONT_BODY_LIGHT}"/><a:ea typeface="{FONT_BODY_LIGHT}"/><a:cs typeface="{FONT_BODY_LIGHT}"/>'
        f'</a:rPr><a:t>{xml_escape(text)}</a:t></a:r></a:p>'
        f'</p:txBody></p:sp>'
    )


def _render_closing(sp_id, s):
    title    = s.get("title", "Cảm ơn các bạn!")
    subtitle = s.get("subtitle", "")
    shps = [_make_ctr_title_sp(sp_id, title)]
    if subtitle:
        shps.append(_make_sub_title_sp(sp_id, subtitle))
    return "".join(shps), "slideLayout9.xml"


_RENDERERS = {
    "cover":            _render_cover,
    "agenda":           _render_agenda,
    "objectives":       _render_objectives,
    "comparison_2col":  _render_comparison_2col,
    "code_right_card":  _render_code_right_card,
    "code_trace_table": _render_code_trace_table,
    "grid2x2":          _render_grid2x2,
    "glossary_table":   _render_glossary_table,
    "summary_2col":     _render_summary_2col,
    "exercises":        _render_exercises,
    "interactive":      _render_interactive,
    "flowchart":        _render_flowchart,
    "timeline":         _render_timeline,
    "closing":          _render_closing,
}


def build_slide(sp_id, slide_data):
    """Dispatch to renderer based on slide_data['type']."""
    renderer = _RENDERERS.get(slide_data.get("type",""))
    if renderer:
        return renderer(sp_id, slide_data)
    # fallback generic
    shps = [make_h1_sp(sp_id, slide_data.get("h1", slide_data.get("title","")))]
    h2   = slide_data.get("h2", slide_data.get("subtitle",""))
    if h2:
        shps.append(make_h2_sp(sp_id, h2))
    shps.append(make_card_sp(sp_id, 838200, 1950000, 10600000, 4450000, fill_clr=WHITE))
    bullets = slide_data.get("bullets", slide_data.get("items",[]))
    shps.append(make_textbox_sp(sp_id, 1100000, 2150000, 10000000, 4000000, _items_to_paras(bullets, sz=1700)))
    return "".join(shps), "slideLayout2.xml"


# ─── Main Build Function ──────────────────────────────────────────────────

def build_deck(slides_data, output_pptx_path, template_pptx_path=None):
    """
    Build a complete PPTX presentation from dynamic slides_data.

    Args:
        slides_data         : List[dict] — each dict must have 'type' key.
        output_pptx_path    : str | Path — destination .pptx file.
        template_pptx_path  : str | Path | None — SLIDE TEMPLATE.pptx path.
                              If None, auto-resolved relative to this file.
    Returns:
        Path to the built .pptx.
    """
    output_path = Path(output_pptx_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if template_pptx_path is None:
        _this      = Path(__file__).resolve()
        candidates = [
            _this.parent.parent.parent.parent / "templates" / "pptx" / "SLIDE TEMPLATE.pptx",
        ]
        tmpl = next((c for c in candidates if c.exists()), None)
        if tmpl is None:
            raise FileNotFoundError(
                "SLIDE TEMPLATE.pptx not found. "
                "Pass template_pptx_path explicitly to build_deck()."
            )
    else:
        tmpl = Path(template_pptx_path)
        if not tmpl.exists():
            raise FileNotFoundError(f"Template not found: {tmpl}")

    # Skill 3 Giai đoạn 1: re-derive brand color/fonts/corner-radius from THIS template
    # before rendering, so the engine stays correct when a different template is passed.
    globals().update(extract_design_tokens(tmpl))

    import tempfile
    build_dir = Path(tempfile.mkdtemp(prefix="deck_engine_"))
    unpacked  = build_dir / "unpacked"
    unpacked.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(tmpl, "r") as z:
        z.extractall(unpacked)

    slides_dir      = unpacked / "ppt" / "slides"
    slides_rels_dir = slides_dir / "_rels"
    notes_dir       = unpacked / "ppt" / "notesSlides"
    notes_rels_dir  = notes_dir / "_rels"
    for d in [slides_dir, slides_rels_dir, notes_dir, notes_rels_dir]:
        d.mkdir(parents=True, exist_ok=True)

    for f in slides_dir.glob("*.xml"):       f.unlink()
    for f in slides_rels_dir.glob("*.rels"): f.unlink()
    for f in notes_dir.glob("*.xml"):        f.unlink()
    for f in notes_rels_dir.glob("*.rels"):  f.unlink()

    num_slides = len(slides_data)
    sp_id      = ShapeIdGenerator()   # fresh counter per deck

    for idx, slide in enumerate(slides_data, 1):
        shapes_xml, layout_name = build_slide(sp_id, slide)
        notes_text = slide.get("notes", slide.get("speaker_notes", ""))
        if slide.get("type") == "interactive" and slide.get("answer"):
            # Answer is deliberately kept off the printed slide (see _render_interactive) —
            # it only reaches the instructor via speaker notes.
            notes_text = f'{notes_text}\nĐáp án: {slide["answer"]}'.strip()

        (slides_dir / f"slide{idx}.xml").write_text(
            wrap_slide_xml(shapes_xml), encoding="utf-8")

        extra_rel = ""
        if slide.get("type") == "agenda":
            extra_rel = ('<Relationship Id="rId3" '
                         'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
                         'Target="../media/image8.png"/>')
        s_rels = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            f'<Relationship Id="rId1" '
            f'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" '
            f'Target="../slideLayouts/{layout_name}"/>'
            f'<Relationship Id="rId2" '
            f'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide" '
            f'Target="../notesSlides/notesSlide{idx}.xml"/>'
            f'{extra_rel}'
            '</Relationships>'
        )
        (slides_rels_dir / f"slide{idx}.xml.rels").write_text(s_rels, encoding="utf-8")

        (notes_dir / f"notesSlide{idx}.xml").write_text(
            make_notes_slide_xml(sp_id, notes_text), encoding="utf-8")

        n_rels = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            f'<Relationship Id="rId1" '
            f'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" '
            f'Target="../slides/slide{idx}.xml"/>'
            f'<Relationship Id="rId2" '
            f'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesMaster" '
            f'Target="../notesMasters/notesMaster1.xml"/>'
            '</Relationships>'
        )
        (notes_rels_dir / f"notesSlide{idx}.xml.rels").write_text(n_rels, encoding="utf-8")

    # presentation.xml
    pres_path   = unpacked / "ppt" / "presentation.xml"
    pres_xml    = pres_path.read_text(encoding="utf-8")
    sld_entries = "".join([f'<p:sldId id="{255+i}" r:id="rId{100+i}"/>' for i in range(1, num_slides+1)])
    pres_xml    = re.sub(r"<p:sldIdLst>.*?</p:sldIdLst>",
                         f"<p:sldIdLst>{sld_entries}</p:sldIdLst>",
                         pres_xml, flags=re.S)
    pres_path.write_text(pres_xml, encoding="utf-8")

    # presentation.xml.rels
    pres_rels_path = unpacked / "ppt" / "_rels" / "presentation.xml.rels"
    pres_rels_xml  = pres_rels_path.read_text(encoding="utf-8")
    pres_rels_xml  = re.sub(
        r'<Relationship Id="rId\d+" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide"[^>]*/>', "",
        pres_rels_xml)
    slide_rels = "".join([
        f'<Relationship Id="rId{100+i}" '
        f'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" '
        f'Target="slides/slide{i}.xml"/>'
        for i in range(1, num_slides+1)
    ])
    pres_rels_xml = pres_rels_xml.replace("</Relationships>", f"{slide_rels}</Relationships>")
    pres_rels_path.write_text(pres_rels_xml, encoding="utf-8")

    # [Content_Types].xml
    ct_path = unpacked / "[Content_Types].xml"
    ct_xml  = ct_path.read_text(encoding="utf-8")
    ct_xml  = re.sub(r'<Override ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide\+xml"[^>]*/>', "", ct_xml)
    ct_xml  = re.sub(r'<Override ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesSlide\+xml"[^>]*/>', "", ct_xml)
    overrides = []
    for i in range(1, num_slides+1):
        overrides.append(f'<Override ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml" PartName="/ppt/slides/slide{i}.xml"/>')
        overrides.append(f'<Override ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml" PartName="/ppt/notesSlides/notesSlide{i}.xml"/>')
    ct_xml = ct_xml.replace("</Types>", f'{"".join(overrides)}</Types>')
    ct_path.write_text(ct_xml, encoding="utf-8")

    # Pack to PPTX
    if output_path.exists():
        output_path.unlink()
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as z_out:
        for root, _, files in os.walk(unpacked):
            for file in files:
                full = os.path.join(root, file)
                z_out.write(full, os.path.relpath(full, unpacked))

    shutil.rmtree(build_dir, ignore_errors=True)
    return output_path
