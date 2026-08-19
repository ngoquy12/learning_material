"""
core/renderers/pptx/slide_deck_builder.py
High-Fidelity OOXML PowerPoint Slide Deck Generator adhering 100% strictly to
Create_Slide (workspace-bai-giang-du-an) Skill 1, Skill 2, and Skill 3 standards.
"""

from __future__ import annotations
import os
import shutil
import zipfile
import xml.etree.ElementTree as ET
import re
import unicodedata
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Union

# Colors
BRAND_COLOR = "C00000"     # Rikkei Red
BLACK = "000000"
WHITE = "FFFFFF"
BORDER_NEUTRAL = "D9D9D9"
BG_TINT = "F8F9FA"
BG_DARK = "282C34"
GRAY_TEXT = "595959"
SUCCESS_GREEN = "2E7D32"

# Code syntax colors (One Dark Theme)
SYNTAX_KEYWORD = "C678DD"  # purple
SYNTAX_STRING = "98C379"   # green
SYNTAX_NUMBER = "D19A66"   # orange
SYNTAX_VAR = "E06C75"      # red
SYNTAX_FUNC = "61AFEF"     # blue
SYNTAX_COMMENT = "5C6370"  # gray
SYNTAX_PLAIN = "ABB2BF"    # light gray

def xml_escape(text: str) -> str:
    if not text:
        return ""
    return (str(text).replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&apos;"))

class ShapeIdGenerator:
    def __init__(self, start: int = 1000):
        self.current = start

    def next_id(self) -> int:
        self.current += 1
        return self.current

sp_gen = ShapeIdGenerator()

def make_h1_sp(text: str, x: int = 838200, y: int = 509145, cx: int = 8463742, cy: int = 945588) -> str:
    sid = sp_gen.next_id()
    return f"""<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="{sid}" name="Title_{sid}"/>
    <p:cNvSpPr txBox="1"/>
    <p:nvPr><p:ph type="title"/></p:nvPr>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    <a:noFill/><a:ln><a:noFill/></a:ln>
  </p:spPr>
  <p:txBody>
    <a:bodyPr anchorCtr="0" anchor="ctr" bIns="45700" lIns="0" spcFirstLastPara="1" rIns="91425" wrap="square" tIns="45700"><a:normAutofit/></a:bodyPr>
    <a:lstStyle/>
    <a:p>
      <a:pPr indent="0" lvl="0" marL="0" rtl="0" algn="l">
        <a:lnSpc><a:spcPct val="150000"/></a:lnSpc>
        <a:spcBef><a:spcPts val="0"/></a:spcBef>
        <a:spcAft><a:spcPts val="0"/></a:spcAft>
        <a:buNone/>
      </a:pPr>
      <a:r>
        <a:rPr b="1" lang="vi-VN" sz="2800">
          <a:solidFill><a:srgbClr val="{BRAND_COLOR}"/></a:solidFill>
          <a:latin typeface="Montserrat ExtraBold"/><a:ea typeface="Montserrat ExtraBold"/><a:cs typeface="Montserrat ExtraBold"/>
        </a:rPr>
        <a:t>{xml_escape(text)}</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>"""

def make_h2_sp(text: str, x: int = 838200, y: int = 1400000, cx: int = 10600000, cy: int = 460000) -> str:
    sid = sp_gen.next_id()
    return f"""<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="{sid}" name="H2_Subtitle_{sid}"/>
    <p:cNvSpPr txBox="1"/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    <a:noFill/><a:ln><a:noFill/></a:ln>
  </p:spPr>
  <p:txBody>
    <a:bodyPr anchorCtr="0" anchor="t" bIns="45700" lIns="0" spcFirstLastPara="1" rIns="91425" wrap="square" tIns="45700"><a:normAutofit/></a:bodyPr>
    <a:lstStyle/>
    <a:p>
      <a:pPr indent="0" lvl="0" marL="0" rtl="0" algn="l">
        <a:lnSpc><a:spcPct val="150000"/></a:lnSpc>
        <a:spcBef><a:spcPts val="0"/></a:spcBef>
        <a:spcAft><a:spcPts val="0"/></a:spcAft>
        <a:buNone/>
      </a:pPr>
      <a:r>
        <a:rPr b="1" lang="vi-VN" sz="2000">
          <a:solidFill><a:srgbClr val="{BLACK}"/></a:solidFill>
          <a:latin typeface="Montserrat ExtraBold"/><a:ea typeface="Montserrat ExtraBold"/><a:cs typeface="Montserrat ExtraBold"/>
        </a:rPr>
        <a:t>{xml_escape(text)}</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>"""

def make_card_sp(x: int, y: int, cx: int, cy: int, fill_clr: str = WHITE, border_clr: str = BORDER_NEUTRAL, border_w: int = 12700, adj: int = 4000) -> str:
    sid = sp_gen.next_id()
    return f"""<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="{sid}" name="CardBg_{sid}"/>
    <p:cNvSpPr/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
    <a:prstGeom prst="roundRect">
      <a:avLst><a:gd name="adj" fmla="val {adj}"/></a:avLst>
    </a:prstGeom>
    <a:solidFill><a:srgbClr val="{fill_clr}"/></a:solidFill>
    <a:ln w="{border_w}">
      <a:solidFill><a:srgbClr val="{border_clr}"/></a:solidFill>
    </a:ln>
  </p:spPr>
</p:sp>"""

def make_textbox_sp(x: int, y: int, cx: int, cy: int, paragraphs: List[Dict[str, Any]], anchor: str = "t") -> str:
    sid = sp_gen.next_id()
    p_xmls = []
    for p in paragraphs:
        algn = p.get('algn', 'l')
        spcAft = p.get('spcAft', 350)
        runs_xml = []
        
        bullet_type = p.get('bullet', None)
        if bullet_type is True or bullet_type == '●':
            bu_xml = f'<a:buClr><a:srgbClr val="{BRAND_COLOR}"/></a:buClr><a:buSzPts val="1400"/><a:buFont typeface="Arial"/><a:buChar char="●"/>'
            indent_attr = 'indent="-250000" marL="350000"'
        else:
            bu_xml = '<a:buNone/>'
            indent_attr = 'indent="0" marL="0"'
            
        for r in p.get('runs', []):
            t = r.get('text', '')
            b = '1' if r.get('b', False) else '0'
            i = '1' if r.get('i', False) else '0'
            sz = r.get('sz', 1800)
            clr = r.get('clr', BLACK)
            font = r.get('font', 'Arial')
            
            runs_xml.append(f"""<a:r>
        <a:rPr b="{b}" i="{i}" lang="vi-VN" sz="{sz}">
          <a:solidFill><a:srgbClr val="{clr}"/></a:solidFill>
          <a:latin typeface="{font}"/><a:ea typeface="{font}"/><a:cs typeface="{font}"/>
        </a:rPr>
        <a:t>{xml_escape(t)}</a:t>
      </a:r>""")
            
        p_xmls.append(f"""<a:p>
      <a:pPr {indent_attr} lvl="0" rtl="0" algn="{algn}">
        <a:lnSpc><a:spcPct val="150000"/></a:lnSpc>
        <a:spcBef><a:spcPts val="0"/></a:spcBef>
        <a:spcAft><a:spcPts val="{spcAft}"/></a:spcAft>
        {bu_xml}
      </a:pPr>
      {''.join(runs_xml)}
    </a:p>""")
        
    return f"""<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="{sid}" name="TextBox_{sid}"/>
    <p:cNvSpPr txBox="1"/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    <a:noFill/><a:ln><a:noFill/></a:ln>
  </p:spPr>
  <p:txBody>
    <a:bodyPr anchorCtr="0" anchor="{anchor}" bIns="45700" lIns="91425" spcFirstLastPara="1" rIns="91425" wrap="square" tIns="45700"><a:normAutofit/></a:bodyPr>
    <a:lstStyle/>
    {''.join(p_xmls)}
  </p:txBody>
</p:sp>"""

def tokenize_code_line(line: str) -> List[Dict[str, Any]]:
    """Tokenize a programming code line into colored runs (One Dark Palette)."""
    if not line:
        return [{'t': ' ', 'c': SYNTAX_PLAIN}]
    
    stripped = line.strip()
    if stripped.startswith("//") or stripped.startswith("#"):
        return [{'t': line, 'c': SYNTAX_COMMENT, 'i': True}]
    
    tokens = []
    pattern = re.compile(r'("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|\`[^\`]*\`|\b(?:let|const|var|function|return|if|else|for|while|do|switch|case|break|continue|import|export|class|def|async|await|try|catch|new|this)\b|\b\d+\b|[a-zA-Z_$][a-zA-Z0-9_$]*|[^\s\w])')
    
    last_idx = 0
    keywords = {"let", "const", "var", "function", "return", "if", "else", "for", "while", "do", "switch", "case", "break", "continue", "import", "export", "class", "def", "async", "await", "try", "catch", "new", "this"}
    
    for match in pattern.finditer(line):
        start, end = match.span()
        if start > last_idx:
            tokens.append({'t': line[last_idx:start], 'c': SYNTAX_PLAIN})
        
        val = match.group(0)
        if val in keywords:
            tokens.append({'t': val, 'c': SYNTAX_KEYWORD, 'b': True})
        elif (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")) or (val.startswith("`") and val.endswith("`")):
            tokens.append({'t': val, 'c': SYNTAX_STRING})
        elif val.isdigit():
            tokens.append({'t': val, 'c': SYNTAX_NUMBER})
        elif end < len(line) and line[end:end+1] == '(':
            tokens.append({'t': val, 'c': SYNTAX_FUNC})
        else:
            tokens.append({'t': val, 'c': SYNTAX_PLAIN})
        
        last_idx = end
        
    if last_idx < len(line):
        tokens.append({'t': line[last_idx:], 'c': SYNTAX_PLAIN})
        
    return tokens if tokens else [{'t': line, 'c': SYNTAX_PLAIN}]

def make_code_block(x: int, y: int, cx: int, cy: int, title: str, code_str: str) -> str:
    shapes = []
    shapes.append(make_card_sp(x, y, cx, cy, fill_clr=BG_DARK, border_clr=BORDER_NEUTRAL, adj=4000))
    header_h = 360000
    shapes.append(make_textbox_sp(x + 100000, y + 50000, cx - 200000, header_h, [
        {
            'algn': 'l', 'spcAft': 0, 'bullet': None,
            'runs': [
                {'text': f"JS: {title}", 'b': True, 'sz': 1400, 'clr': WHITE, 'font': 'Arial'}
            ]
        }
    ]))
    
    lines = code_str.strip().split('\n')
    code_p = []
    for line in lines:
        toks = tokenize_code_line(line)
        runs = []
        for tok in toks:
            runs.append({
                'text': tok['t'],
                'b': tok.get('b', False),
                'i': tok.get('i', False),
                'sz': tok.get('sz', 1400),
                'clr': tok.get('c', SYNTAX_PLAIN),
                'font': 'Consolas'
            })
        code_p.append({
            'algn': 'l',
            'spcAft': 80,
            'bullet': None,
            'runs': runs
        })
    shapes.append(make_textbox_sp(x + 100000, y + header_h + 60000, cx - 200000, cy - header_h - 100000, code_p))
    return "".join(shapes)

def make_table_sp(x: int, y: int, cx: int, cy: int, headers: List[str], rows: List[List[str]], col_widths: Optional[List[int]] = None) -> str:
    sid = sp_gen.next_id()
    num_cols = len(headers)
    if num_cols == 0:
        return ""
    
    if col_widths is None:
        cw = cx // num_cols
        col_widths = [cw] * num_cols
    else:
        tot = sum(col_widths)
        col_widths = [int(w * cx / tot) for w in col_widths]
        
    grid_xml = "".join([f'<a:gridCol w="{w}"/>' for w in col_widths])
    
    h_cells = []
    for h in headers:
        h_cells.append(f"""<a:tc>
  <a:txBody>
    <a:bodyPr anchor="ctr" lIns="91425" rIns="91425" tIns="45700" bIns="45700"/>
    <a:lstStyle/>
    <a:p>
      <a:pPr algn="ctr"><a:lnSpc><a:spcPct val="120000"/></a:lnSpc><a:buNone/></a:pPr>
      <a:r>
        <a:rPr b="1" lang="vi-VN" sz="1500"><a:solidFill><a:srgbClr val="{WHITE}"/></a:solidFill><a:latin typeface="Montserrat ExtraBold"/></a:rPr>
        <a:t>{xml_escape(h)}</a:t>
      </a:r>
    </a:p>
  </a:txBody>
  <a:tcPr><a:solidFill><a:srgbClr val="{BRAND_COLOR}"/></a:solidFill></a:tcPr>
</a:tc>""")
        
    row_xmls = [f'<a:tr h="450000">{"".join(h_cells)}</a:tr>']
    
    for r_idx, row in enumerate(rows):
        fill_c = BG_TINT if (r_idx % 2 == 1) else WHITE
        r_cells = []
        for cell_val in row:
            r_cells.append(f"""<a:tc>
  <a:txBody>
    <a:bodyPr anchor="ctr" lIns="91425" rIns="91425" tIns="45700" bIns="45700"/>
    <a:lstStyle/>
    <a:p>
      <a:pPr algn="l"><a:lnSpc><a:spcPct val="120000"/></a:lnSpc><a:buNone/></a:pPr>
      <a:r>
        <a:rPr lang="vi-VN" sz="1400"><a:solidFill><a:srgbClr val="{BLACK}"/></a:solidFill><a:latin typeface="Arial"/></a:rPr>
        <a:t>{xml_escape(cell_val)}</a:t>
      </a:r>
    </a:p>
  </a:txBody>
  <a:tcPr><a:solidFill><a:srgbClr val="{fill_c}"/></a:solidFill></a:tcPr>
</a:tc>""")
        row_xmls.append(f'<a:tr h="400000">{"".join(r_cells)}</a:tr>')
        
    return f"""<p:graphicFrame>
  <p:nvGraphicFramePr>
    <p:cNvPr id="{sid}" name="Table_{sid}"/>
    <p:cNvGraphicFramePr><a:graphicFrameLocks noGrp="1"/></p:cNvGraphicFramePr>
    <p:nvPr/>
  </p:nvGraphicFramePr>
  <p:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></p:xfrm>
  <a:graphic>
    <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/table">
      <a:tbl>
        <a:tblPr firstRow="1" bandRow="1"/>
        <a:tblGrid>{grid_xml}</a:tblGrid>
        {''.join(row_xmls)}
      </a:tbl>
    </a:graphicData>
  </a:graphic>
</p:graphicFrame>"""

def wrap_slide_xml(sp_tree_children_xml: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
       xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
       xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr>
        <p:cNvPr id="1" name="Root"/>
        <p:cNvGrpSpPr/>
        <p:nvPr/>
      </p:nvGrpSpPr>
      <p:grpSpPr>
        <a:xfrm>
          <a:off x="0" y="0"/>
          <a:ext cx="0" cy="0"/>
          <a:chOff x="0" y="0"/>
          <a:chExt cx="0" cy="0"/>
        </a:xfrm>
      </p:grpSpPr>
      {sp_tree_children_xml}
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>"""

def make_notes_slide_xml(notes_text: str) -> str:
    sid = sp_gen.next_id()
    paragraphs_xml = []
    for line in notes_text.strip().split('\n'):
        line_clean = line.strip()
        if not line_clean:
            continue
        paragraphs_xml.append(f"""<a:p>
      <a:pPr indent="0" lvl="0" marL="0" rtl="0" algn="l">
        <a:lnSpc><a:spcPct val="150000"/></a:lnSpc>
        <a:buNone/>
      </a:pPr>
      <a:r>
        <a:rPr lang="vi-VN" sz="1200"><a:solidFill><a:srgbClr val="{BLACK}"/></a:solidFill><a:latin typeface="Arial"/></a:rPr>
        <a:t>{xml_escape(line_clean)}</a:t>
      </a:r>
    </a:p>""")
    if not paragraphs_xml:
        paragraphs_xml.append(f'<a:p><a:r><a:rPr lang="vi-VN" sz="1200"/><a:t>Ghi chú bài giảng...</a:t></a:r></a:p>')
        
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:notes xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
         xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
         xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr>
        <p:cNvPr id="1" name=""/>
        <p:cNvGrpSpPr/>
        <p:nvPr/>
      </p:nvGrpSpPr>
      <p:grpSpPr>
        <a:xfrm>
          <a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/>
        </a:xfrm>
      </p:grpSpPr>
      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="{sid}" name="Slide Image Placeholder"/>
          <p:cNvSpPr><a:spLocks noGrp="1" noRot="1" noChangeAspect="1"/></p:cNvSpPr>
          <p:nvPr><p:ph type="sldImg"/></p:nvPr>
        </p:nvSpPr>
        <p:spPr/>
      </p:sp>
      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="{sid+1}" name="Notes Placeholder"/>
          <p:cNvSpPr txBox="1"/>
          <p:nvPr><p:ph idx="1" type="body"/></p:nvPr>
        </p:nvSpPr>
        <p:spPr/>
        <p:txBody>
          <a:bodyPr/>
          <a:lstStyle/>
          {''.join(paragraphs_xml)}
        </p:txBody>
      </p:sp>
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:notes>"""

class SlideDeckBuilder:
    """
    Core OOXML PowerPoint Engine that builds standard, branded PPTX Slide Decks
    from SLIDE TEMPLATE.pptx.
    """
    def __init__(self, template_pptx_path: Optional[Union[str, Path]] = None):
        if template_pptx_path:
            self.template_path = Path(template_pptx_path)
        else:
            default_p = Path(__file__).resolve().parent.parent.parent.parent / "templates" / "pptx" / "SLIDE TEMPLATE.pptx"
            self.template_path = default_p

    def build_deck_from_slides_data(
        self,
        slides_data: List[Dict[str, Any]],
        output_pptx_path: Union[str, Path],
        temp_build_dir: Optional[Union[str, Path]] = None
    ) -> Path:
        """
        Builds a complete valid PPTX presentation deck from structured slides_data.
        """
        output_path = Path(output_pptx_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if temp_build_dir:
            build_dir = Path(temp_build_dir)
        else:
            import tempfile
            build_dir = Path(tempfile.mkdtemp(prefix="pptx_build_"))
            
        unpacked_dir = build_dir / "unpacked"
        if unpacked_dir.exists():
            shutil.rmtree(unpacked_dir, ignore_errors=True)
        unpacked_dir.mkdir(parents=True, exist_ok=True)

        if not self.template_path.exists():
            raise FileNotFoundError(f"PowerPoint Template not found at: {self.template_path}")

        # 1. Unpack template
        with zipfile.ZipFile(self.template_path, 'r') as z_in:
            z_in.extractall(unpacked_dir)

        # 2. Prepare directories
        slides_dir = unpacked_dir / "ppt" / "slides"
        slides_rels_dir = slides_dir / "_rels"
        notes_dir = unpacked_dir / "ppt" / "notesSlides"
        notes_rels_dir = notes_dir / "_rels"
        
        slides_dir.mkdir(parents=True, exist_ok=True)
        slides_rels_dir.mkdir(parents=True, exist_ok=True)
        notes_dir.mkdir(parents=True, exist_ok=True)
        notes_rels_dir.mkdir(parents=True, exist_ok=True)

        # Clean old slides
        for f in list(slides_dir.glob("*.xml")): f.unlink()
        for f in list(slides_rels_dir.glob("*.rels")): f.unlink()
        for f in list(notes_dir.glob("*.xml")): f.unlink()
        for f in list(notes_rels_dir.glob("*.rels")): f.unlink()

        num_slides = len(slides_data)
        
        # 3. Render slide XMLs
        for idx, s in enumerate(slides_data, 1):
            layout_name = s.get("layout", "slideLayout2.xml")
            s_type = s.get("type", "content")
            h1_title = s.get("title", f"Slide {idx}")
            h2_subtitle = s.get("subtitle", "")
            notes_text = s.get("speaker_notes", f"Giảng viên giải thích nội dung Slide {idx}.")
            
            shapes = []
            
            if s_type == "cover":
                # Title slide matching Create_Slide Slide 1
                layout_name = "slideLayout3.xml"
                session_tag = s.get("session_id", "Session")
                course_title = s.get("course_name", "Lập trình Web")
                shapes.append(f"""
<p:sp>
  <p:nvSpPr><p:cNvPr id="101" name="SessionId"/><p:cNvSpPr txBox="1"/><p:nvPr><p:ph idx="2" type="body"/></p:nvPr></p:nvSpPr>
  <p:spPr><a:xfrm><a:off x="1562200" y="1974300"/><a:ext cx="8154600" cy="554100"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>
  <p:txBody><a:bodyPr anchorCtr="0" anchor="t" bIns="45700" lIns="91425" spcFirstLastPara="1" rIns="91425" wrap="square" tIns="45700"><a:noAutofit/></a:bodyPr><a:lstStyle/>
    <a:p><a:pPr indent="0" lvl="0" marL="0" rtl="0" algn="l"><a:lnSpc><a:spcPct val="90000"/></a:lnSpc><a:buNone/></a:pPr>
      <a:r><a:rPr b="1" lang="vi-VN" sz="3000"><a:solidFill><a:srgbClr val="{BRAND_COLOR}"/></a:solidFill><a:latin typeface="Montserrat ExtraBold"/><a:ea typeface="Montserrat ExtraBold"/><a:cs typeface="Montserrat ExtraBold"/></a:rPr><a:t>{xml_escape(session_tag)}</a:t></a:r>
    </a:p>
  </p:txBody>
</p:sp>
<p:sp>
  <p:nvSpPr><p:cNvPr id="102" name="Title"/><p:cNvSpPr txBox="1"/><p:nvPr><p:ph type="ctrTitle"/></p:nvPr></p:nvSpPr>
  <p:spPr><a:xfrm><a:off x="1697675" y="2660574"/><a:ext cx="8500000" cy="947700"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>
  <p:txBody><a:bodyPr anchorCtr="0" anchor="t" bIns="0" lIns="0" spcFirstLastPara="1" rIns="0" wrap="square" tIns="0"><a:noAutofit/></a:bodyPr><a:lstStyle/>
    <a:p><a:pPr indent="0" lvl="0" marL="0" rtl="0" algn="l"><a:lnSpc><a:spcPct val="90000"/></a:lnSpc><a:buNone/></a:pPr>
      <a:r><a:rPr b="1" lang="vi-VN" sz="3000"><a:solidFill><a:srgbClr val="{BLACK}"/></a:solidFill><a:latin typeface="Montserrat Black"/><a:ea typeface="Montserrat Black"/><a:cs typeface="Montserrat Black"/></a:rPr><a:t>{xml_escape(h1_title)}</a:t></a:r>
    </a:p>
  </p:txBody>
</p:sp>
<p:sp>
  <p:nvSpPr><p:cNvPr id="103" name="CourseModule"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr><a:xfrm><a:off x="1697669" y="3664241"/><a:ext cx="8500000" cy="360000"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>
  <p:txBody><a:bodyPr anchorCtr="0" anchor="t" bIns="0" lIns="0" spcFirstLastPara="1" rIns="0" wrap="square" tIns="0"><a:noAutofit/></a:bodyPr><a:lstStyle/>
    <a:p><a:pPr indent="-228600" lvl="0" marL="228600" rtl="0" algn="l"><a:lnSpc><a:spcPct val="90000"/></a:lnSpc><a:buNone/></a:pPr>
      <a:r><a:rPr b="0" lang="vi-VN" sz="1800"><a:solidFill><a:srgbClr val="{BLACK}"/></a:solidFill><a:latin typeface="Montserrat"/><a:ea typeface="Montserrat"/><a:cs typeface="Montserrat"/></a:rPr><a:t>Môn học: {xml_escape(course_title)}</a:t></a:r>
    </a:p>
  </p:txBody>
</p:sp>
""")
            elif s_type == "agenda":
                # Agenda slide matching Create_Slide Slide 2
                layout_name = "slideLayout1.xml"
                parts = s.get("agenda_items", [])
                p_items_xml = []
                for p_idx, item in enumerate(parts, 1):
                    p_items_xml.append(f"""
    <a:p><a:pPr indent="0" lvl="0" marL="0" rtl="0" algn="l"><a:lnSpc><a:spcPct val="150000"/></a:lnSpc><a:spcBef><a:spcPts val="0"/></a:spcBef><a:spcAft><a:spcPts val="550"/></a:spcAft><a:buNone/></a:pPr>
      <a:r><a:rPr b="1" lang="vi-VN" sz="2400"><a:solidFill><a:srgbClr val="{BLACK}"/></a:solidFill><a:latin typeface="Montserrat ExtraBold"/><a:ea typeface="Montserrat ExtraBold"/><a:cs typeface="Montserrat ExtraBold"/></a:rPr><a:t>{p_idx}. {xml_escape(str(item))}</a:t></a:r>
    </a:p>""")

                shapes.append(f"""
<p:sp>
  <p:nvSpPr><p:cNvPr id="185" name="Title"/><p:cNvSpPr txBox="1"/><p:nvPr><p:ph type="title"/></p:nvPr></p:nvSpPr>
  <p:spPr><a:xfrm rot="5400000"><a:off x="-1686375" y="1500953"/><a:ext cx="5085300" cy="1845300"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>
  <p:txBody><a:bodyPr anchorCtr="0" anchor="b" bIns="45700" lIns="91425" spcFirstLastPara="1" rIns="91425" wrap="square" tIns="45700"><a:normAutofit/></a:bodyPr><a:lstStyle/>
    <a:p><a:pPr indent="0" lvl="0" marL="0" rtl="0" algn="l"><a:lnSpc><a:spcPct val="90000"/></a:lnSpc><a:buNone/></a:pPr>
      <a:r><a:rPr lang="vi-VN"><a:solidFill><a:srgbClr val="{BRAND_COLOR}"/></a:solidFill><a:latin typeface="Montserrat Black"/><a:ea typeface="Montserrat Black"/><a:cs typeface="Montserrat Black"/></a:rPr><a:t> NỘI DUNG</a:t></a:r>
    </a:p>
  </p:txBody>
</p:sp>
<p:pic>
  <p:nvPicPr><p:cNvPr id="186" name="DecorTriangle"/><p:cNvPicPr preferRelativeResize="0"/><p:nvPr/></p:nvPicPr>
  <p:blipFill rotWithShape="1"><a:blip r:embed="rId3"><a:alphaModFix/></a:blip><a:srcRect b="0" l="0" r="0" t="0"/><a:stretch/></p:blipFill>
  <p:spPr><a:xfrm><a:off x="-1863816" y="5111676"/><a:ext cx="3515280" cy="3492645"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>
</p:pic>
<p:sp>
  <p:nvSpPr><p:cNvPr id="184" name="AgendaList"/><p:cNvSpPr txBox="1"/><p:nvPr><p:ph idx="1" type="body"/></p:nvPr></p:nvSpPr>
  <p:spPr><a:xfrm><a:off x="2000000" y="1261300"/><a:ext cx="9500000" cy="4935600"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>
  <p:txBody><a:bodyPr anchorCtr="0" anchor="t" bIns="45700" lIns="91425" spcFirstLastPara="1" rIns="91425" wrap="square" tIns="45700"><a:normAutofit/></a:bodyPr><a:lstStyle/>
    {''.join(p_items_xml)}
  </p:txBody>
</p:sp>
""")
            elif s_type == "objectives":
                # Objectives slide matching Create_Slide Slide 3
                layout_name = "slideLayout2.xml"
                shapes.append(make_h1_sp(h1_title))
                goals = s.get("goals", [])
                card_y = 1650000
                card_h = 820000
                card_gap = 160000
                for g_idx, goal_text in enumerate(goals[:4], 1):
                    y_pos = card_y + (g_idx - 1) * (card_h + card_gap)
                    shapes.append(make_card_sp(838200, y_pos, 10600000, card_h, fill_clr=WHITE, border_clr=BORDER_NEUTRAL, adj=4000))
                    shapes.append(make_textbox_sp(980000, y_pos + 150000, 10300000, card_h - 300000, [
                        {
                            'algn': 'l', 'spcAft': 0, 'bullet': None,
                            'runs': [
                                {'text': f"{g_idx}.  ", 'b': True, 'sz': 1800, 'clr': BLACK, 'font': 'Montserrat ExtraBold'},
                                {'text': str(goal_text), 'b': True, 'sz': 1800, 'clr': BLACK, 'font': 'Montserrat ExtraBold'}
                            ]
                        }
                    ]))
            elif s_type == "code":
                # Code slide side-by-side matching Create_Slide Slides 6, 7, 8
                layout_name = "slideLayout2.xml"
                shapes.append(make_h1_sp(h1_title))
                if h2_subtitle:
                    shapes.append(make_h2_sp(h2_subtitle))
                
                # Left: Code Sandbox
                code_text = s.get("code_snippet", "// Mã nguồn...")
                code_title = s.get("code_title", "Cú pháp thực thi")
                shapes.append(make_code_block(838200, 2000000, 5200000, 3900000, code_title, code_text))
                
                # Right: Explanation Card
                bullets = s.get("bullets", [])
                card_title = s.get("card_title", "Phân tích kỹ thuật")
                shapes.append(make_card_sp(6238200, 2000000, 5200000, 3900000, fill_clr=WHITE, border_clr=BORDER_NEUTRAL, adj=4000))
                p_list = [
                    {
                        'algn': 'l', 'spcAft': 250, 'bullet': None,
                        'runs': [{'text': card_title, 'b': True, 'sz': 1800, 'clr': BRAND_COLOR, 'font': 'Arial'}]
                    }
                ]
                for b in bullets:
                    p_list.append({
                        'algn': 'l', 'spcAft': 180, 'bullet': '●',
                        'runs': [{'text': str(b), 'b': False, 'sz': 1600, 'clr': BLACK, 'font': 'Arial'}]
                    })
                shapes.append(make_textbox_sp(6438200, 2180000, 4800000, 3500000, p_list))
            elif s_type == "comparison":
                # Comparison Cards (2 columns) matching Create_Slide Slide 4
                layout_name = "slideLayout2.xml"
                shapes.append(make_h1_sp(h1_title))
                if h2_subtitle:
                    shapes.append(make_h2_sp(h2_subtitle))
                
                left_col = s.get("left_col", {})
                right_col = s.get("right_col", {})
                box_w = 5150000
                box_y = 2000000
                box_h = 3900000
                
                # Left card
                shapes.append(make_card_sp(838200, box_y, box_w, box_h, fill_clr=WHITE, border_clr=BORDER_NEUTRAL, adj=4000))
                p_left = [{
                    'algn': 'l', 'spcAft': 250, 'bullet': None,
                    'runs': [{'text': left_col.get('title', 'Cách tiếp cận A'), 'b': True, 'sz': 1800, 'clr': BRAND_COLOR, 'font': 'Arial'}]
                }]
                if left_col.get('code'):
                    p_left.append({
                        'algn': 'l', 'spcAft': 200, 'bullet': None,
                        'runs': [{'text': left_col['code'], 'b': False, 'sz': 1400, 'clr': GRAY_TEXT, 'font': 'Consolas'}]
                    })
                for b in left_col.get('bullets', []):
                    p_left.append({
                        'algn': 'l', 'spcAft': 150, 'bullet': '●',
                        'runs': [{'text': str(b), 'b': False, 'sz': 1500, 'clr': BLACK}]
                    })
                shapes.append(make_textbox_sp(1038200, box_y + 180000, box_w - 400000, box_h - 360000, p_left))
                
                # Right card
                shapes.append(make_card_sp(6288200, box_y, box_w, box_h, fill_clr=WHITE, border_clr=BORDER_NEUTRAL, adj=4000))
                p_right = [{
                    'algn': 'l', 'spcAft': 250, 'bullet': None,
                    'runs': [{'text': right_col.get('title', 'Cách tiếp cận B'), 'b': True, 'sz': 1800, 'clr': SUCCESS_GREEN, 'font': 'Arial'}]
                }]
                if right_col.get('code'):
                    p_right.append({
                        'algn': 'l', 'spcAft': 200, 'bullet': None,
                        'runs': [{'text': right_col['code'], 'b': False, 'sz': 1400, 'clr': BLACK, 'font': 'Consolas'}]
                    })
                for b in right_col.get('bullets', []):
                    p_right.append({
                        'algn': 'l', 'spcAft': 150, 'bullet': '●',
                        'runs': [{'text': str(b), 'b': False, 'sz': 1500, 'clr': BLACK}]
                    })
                shapes.append(make_textbox_sp(6488200, box_y + 180000, box_w - 400000, box_h - 360000, p_right))
            elif s_type == "grid4":
                # 2x2 Grid Cards matching Create_Slide Slide 5 & Slide 12 (Terminology)
                layout_name = "slideLayout2.xml"
                shapes.append(make_h1_sp(h1_title))
                if h2_subtitle:
                    shapes.append(make_h2_sp(h2_subtitle))
                items = s.get("items", [])
                grid_w = 5150000
                grid_h = 1850000
                coords = [
                    (838200, 2000000),
                    (6288200, 2000000),
                    (838200, 4000000),
                    (6288200, 4000000)
                ]
                for g_idx, (pos_x, pos_y) in enumerate(coords):
                    if g_idx >= len(items): break
                    it = items[g_idx]
                    shapes.append(make_card_sp(pos_x, pos_y, grid_w, grid_h, fill_clr=WHITE, border_clr=BORDER_NEUTRAL, adj=4000))
                    p_grid = [
                        {
                            'algn': 'l', 'spcAft': 150, 'bullet': None,
                            'runs': [{'text': it.get('title', f'Mục {g_idx+1}'), 'b': True, 'sz': 1700, 'clr': BRAND_COLOR, 'font': 'Arial'}]
                        },
                        {
                            'algn': 'l', 'spcAft': 150, 'bullet': None,
                            'runs': [{'text': it.get('desc', ''), 'b': False, 'sz': 1500, 'clr': BLACK, 'font': 'Arial'}]
                        }
                    ]
                    if it.get('example'):
                        p_grid.append({
                            'algn': 'l', 'spcAft': 0, 'bullet': None,
                            'runs': [{'text': f"Ví dụ: {it['example']}", 'b': True, 'sz': 1400, 'clr': GRAY_TEXT, 'font': 'Consolas'}]
                        })
                    shapes.append(make_textbox_sp(pos_x + 180000, pos_y + 140000, grid_w - 360000, grid_h - 280000, p_grid))
            elif s_type == "table":
                # Table slide
                layout_name = "slideLayout2.xml"
                shapes.append(make_h1_sp(h1_title))
                if h2_subtitle:
                    shapes.append(make_h2_sp(h2_subtitle))
                headers = s.get("table_headers", ["Tiêu chí", "Phương án A", "Phương án B"])
                rows = s.get("table_rows", [["Mục 1", "Giá trị 1", "Giá trị 2"]])
                col_w = s.get("col_widths", None)
                shapes.append(make_table_sp(838200, 2000000, 10600000, 3900000, headers, rows, col_w))
            elif s_type == "closing":
                # Closing slide matching Create_Slide Slide 14
                layout_name = "slideLayout3.xml"
                shapes.append(make_h1_sp(h1_title, x=838200, y=2800000, cx=10500000, cy=1200000))
                closing_msg = s.get("message", "Cảm ơn các bạn đã theo dõi bài giảng!")
                shapes.append(make_h2_sp(closing_msg, x=838200, y=4100000, cx=10500000, cy=600000))
            else:
                # Default Content Slide
                layout_name = "slideLayout2.xml"
                shapes.append(make_h1_sp(h1_title))
                if h2_subtitle:
                    shapes.append(make_h2_sp(h2_subtitle))
                shapes.append(make_card_sp(838200, 1950000, 10600000, 4450000, fill_clr=WHITE))
                bullets = s.get("bullets", [])
                p_list = []
                for b in bullets:
                    p_list.append({
                        'algn': 'l', 'spcAft': 350, 'bullet': True,
                        'runs': [{'text': str(b), 'b': False, 'sz': 1700, 'clr': BLACK, 'font': 'Arial'}]
                    })
                shapes.append(make_textbox_sp(1100000, 2150000, 10000000, 4000000, p_list))

            # Write slide XML
            slide_xml_content = wrap_slide_xml("".join(shapes))
            (slides_dir / f"slide{idx}.xml").write_text(slide_xml_content, encoding="utf-8")
            
            # Write slide rels
            extra_rel = ""
            if idx == 2 and s_type == "agenda":
                extra_rel = '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/image8.png"/>'
            
            s_rels_content = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/{layout_name}"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide" Target="../notesSlides/notesSlide{idx}.xml"/>
  {extra_rel}
</Relationships>"""
            (slides_rels_dir / f"slide{idx}.xml.rels").write_text(s_rels_content, encoding="utf-8")

            # Write notesSlide XML & rels
            notes_xml_content = make_notes_slide_xml(notes_text)
            (notes_dir / f"notesSlide{idx}.xml").write_text(notes_xml_content, encoding="utf-8")
            
            n_rels_content = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="../slides/slide{idx}.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesMaster" Target="../notesMasters/notesMaster1.xml"/>
</Relationships>"""
            (notes_rels_dir / f"notesSlide{idx}.xml.rels").write_text(n_rels_content, encoding="utf-8")

        # 4. Update presentation.xml
        pres_path = unpacked_dir / "ppt" / "presentation.xml"
        sld_id_lst_entries = "".join([f'<p:sldId id="{255 + i}" r:id="rId{100 + i}"/>' for i in range(1, num_slides + 1)])
        pres_xml = pres_path.read_text(encoding="utf-8")
        pres_xml = re.sub(r'<p:sldIdLst>.*?</p:sldIdLst>', f'<p:sldIdLst>{sld_id_lst_entries}</p:sldIdLst>', pres_xml, flags=re.S)
        pres_path.write_text(pres_xml, encoding="utf-8")

        # 5. Update ppt/_rels/presentation.xml.rels
        pres_rels_path = unpacked_dir / "ppt" / "_rels" / "presentation.xml.rels"
        pres_rels_xml = pres_rels_path.read_text(encoding="utf-8")
        pres_rels_xml = re.sub(r'<Relationship Id="rId\d+" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide"[^>]*/>', '', pres_rels_xml)
        slide_rels_entries = "".join([f'<Relationship Id="rId{100 + i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>' for i in range(1, num_slides + 1)])
        pres_rels_xml = pres_rels_xml.replace('</Relationships>', f'{slide_rels_entries}</Relationships>')
        pres_rels_path.write_text(pres_rels_xml, encoding="utf-8")

        # 6. Update [Content_Types].xml
        ct_path = unpacked_dir / "[Content_Types].xml"
        ct_xml = ct_path.read_text(encoding="utf-8")
        ct_xml = re.sub(r'<Override ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide\+xml"[^>]*/>', '', ct_xml)
        ct_xml = re.sub(r'<Override ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesSlide\+xml"[^>]*/>', '', ct_xml)
        overrides = []
        for i in range(1, num_slides + 1):
            overrides.append(f'<Override ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml" PartName="/ppt/slides/slide{i}.xml"/>')
            overrides.append(f'<Override ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml" PartName="/ppt/notesSlides/notesSlide{i}.xml"/>')
        ct_xml = ct_xml.replace('</Types>', f'{"".join(overrides)}</Types>')
        ct_path.write_text(ct_xml, encoding="utf-8")

        # 7. Zip package to final PPTX
        if output_path.exists():
            output_path.unlink()
            
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as z_out:
            for root, dirs, files in os.walk(unpacked_dir):
                for file in files:
                    full_p = os.path.join(root, file)
                    rel_p = os.path.relpath(full_p, unpacked_dir)
                    z_out.write(full_p, rel_p)

        if not temp_build_dir:
            shutil.rmtree(build_dir, ignore_errors=True)

        return output_path

slide_deck_builder = SlideDeckBuilder()
