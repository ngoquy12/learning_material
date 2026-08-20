"""
core/renderers/mindmap_exporter.py
Structure parser, structural validator, and XMind Workbook exporter for Session-Level Mindmaps.
Pure stdlib (zipfile + xml.sax.saxutils) — no external markdown/xmind dependency required.
"""

import re
import zipfile
from pathlib import Path
from typing import Dict, Any, List
from xml.sax.saxutils import escape


def parse_markmap_tree(markdown_text: str) -> Dict[str, Any]:
    """
    Parses a Markmap markdown tree (# / ## / ### headings + '-' bullets, with '```' code fences
    treated as opaque text appended to the enclosing node) into a nested dict:
    {"title": str, "level": int, "children": [...]}. The returned dict is a synthetic level-0
    wrapper whose children are the actual heading nodes (normally exactly one level-1 root).
    """
    if not markdown_text:
        return {"title": "", "level": 0, "children": []}

    lines = markdown_text.splitlines()
    root: Dict[str, Any] = {"title": "", "level": 0, "children": []}
    heading_stack: List[tuple] = [(0, root)]
    bullet_stack: List[tuple] = []
    last_node: Dict[str, Any] = root
    in_fence = False

    for raw_line in lines:
        line = raw_line.rstrip("\n")
        stripped = line.strip()

        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            last_node["title"] = (last_node.get("title", "") + "\n" + line).rstrip()
            continue
        if not stripped:
            continue

        heading_match = re.match(r'^(#{1,6})\s+(.*)$', stripped)
        if heading_match:
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip()
            node = {"title": title, "level": level, "children": []}
            while heading_stack and heading_stack[-1][0] >= level:
                heading_stack.pop()
            heading_stack[-1][1]["children"].append(node)
            heading_stack.append((level, node))
            bullet_stack = []
            last_node = node
            continue

        bullet_match = re.match(r'^(\s*)-\s+(.*)$', line)
        if bullet_match:
            indent = len(bullet_match.group(1))
            title = bullet_match.group(2).strip()
            node = {"title": title, "level": 100 + indent, "children": []}
            while bullet_stack and bullet_stack[-1][0] >= indent:
                bullet_stack.pop()
            parent = bullet_stack[-1][1] if bullet_stack else heading_stack[-1][1]
            parent["children"].append(node)
            bullet_stack.append((indent, node))
            last_node = node
            continue

    return root


def validate_mindmap_structure(tree: Dict[str, Any]) -> List[str]:
    """
    Structural (not content) audit of a parsed mindmap tree, run BEFORE exporting:
    - exactly 1 root (H1)
    - each Lesson branch (H2, excluding the final "Liên kết hệ thống" branch) has exactly 4
      sub-branches (H3)
    - no H2/H3 branch is empty
    Returns a list of issue descriptions (empty list = structurally valid). Non-blocking by
    design — caller should log these as warnings, not abort the pipeline.
    """
    issues: List[str] = []
    h1_nodes = [c for c in tree.get("children", []) if c.get("level") == 1]
    if len(h1_nodes) != 1:
        issues.append(f"Phải có đúng 1 tiêu đề cấp 1 (#), hiện có {len(h1_nodes)}.")
        return issues

    root = h1_nodes[0]
    h2_nodes = [c for c in root.get("children", []) if c.get("level") == 2]
    if not h2_nodes:
        issues.append("Không tìm thấy nhánh cấp 2 (##) nào.")
        return issues

    for h2 in h2_nodes:
        title_lower = (h2.get("title") or "").lower()
        if "liên kết hệ thống" in title_lower:
            if not h2.get("children"):
                issues.append(f"Nhánh '{h2.get('title')}' rỗng, không có nội dung.")
            continue
        h3_nodes = [c for c in h2.get("children", []) if c.get("level") == 3]
        if len(h3_nodes) != 4:
            issues.append(
                f"Nhánh bài học '{h2.get('title')}' có {len(h3_nodes)} nhánh con cấp 3, yêu cầu đúng 4."
            )
        for h3 in h3_nodes:
            if not h3.get("children"):
                issues.append(
                    f"Nhánh con '{h3.get('title')}' (thuộc '{h2.get('title')}') rỗng, không có nội dung."
                )
    return issues


def _node_to_topic_xml(node: Dict[str, Any], counter: List[int]) -> str:
    counter[0] += 1
    topic_id = f"topic_{counter[0]}"
    title = escape(node.get("title") or "")
    children = node.get("children") or []
    if children:
        child_xml = "".join(_node_to_topic_xml(c, counter) for c in children)
        children_block = f'<children><topics type="attached">{child_xml}</topics></children>'
    else:
        children_block = ""
    return f'<topic id="{topic_id}"><title>{title}</title>{children_block}</topic>'


def build_xmind_file(tree: Dict[str, Any], output_path: Path) -> bool:
    """
    Builds a standard XMind 8-compatible .xmind Workbook (ZIP archive containing content.xml +
    meta.xml + META-INF/manifest.xml) from a parsed mindmap tree, using only stdlib. Returns
    True/False; never raises — a failed XMind build must not affect the already-written .md file.
    """
    try:
        h1_nodes = [c for c in tree.get("children", []) if c.get("level") == 1]
        if not h1_nodes:
            print("  [XMind Export Warning] No root (H1) node found in mindmap tree — skipping .xmind export.")
            return False

        counter = [0]
        root_xml = _node_to_topic_xml(h1_nodes[0], counter)

        content_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
            '<xmap-content xmlns="urn:xmind:xmap:xmlns:content:2.0" '
            'xmlns:fo="http://www.w3.org/1999/XSL/Format" '
            'xmlns:svg="http://www.w3.org/2000/svg" '
            'xmlns:xhtml="http://www.w3.org/1999/xhtml" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" version="2.0">'
            f'<sheet id="sheet1">{root_xml}<title>Sheet 1</title></sheet>'
            '</xmap-content>'
        )
        meta_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
            '<meta xmlns="urn:xmind:xmap:xmlns:meta:2.0" version="2.0"/>'
        )
        manifest_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
            '<manifest xmlns="urn:xmind:xmap:xmlns:manifest:1.0">'
            '<file-entry full-path="content.xml" media-type="text/xml"/>'
            '<file-entry full-path="META-INF/" media-type=""/>'
            '<file-entry full-path="META-INF/manifest.xml" media-type="text/xml"/>'
            '<file-entry full-path="meta.xml" media-type="text/xml"/>'
            '</manifest>'
        )

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("content.xml", content_xml)
            zf.writestr("meta.xml", meta_xml)
            zf.writestr("META-INF/manifest.xml", manifest_xml)
        return True
    except Exception as e:
        print(f"  [XMind Export Warning] Failed to build .xmind file: {e}")
        return False
