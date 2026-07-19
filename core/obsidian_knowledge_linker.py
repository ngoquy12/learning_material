"""
core/obsidian_knowledge_linker.py

Agent 3 — Obsidian Knowledge Linker (OKL)
==========================================
Cải tiến obsidian_exporter.py:
- Inject prerequisite frontmatter dựa trên kết quả PrerequisiteGuardAgent
- Tạo WikiLinks tiên quyết hai chiều (A → B nghĩa là "B yêu cầu A")
- Tạo section "Concept Map" trong mỗi Session note
- Tạo section "Kiến thức cần biết trước" rõ ràng cho người học

Triết lý thiết kế:
- Obsidian Graph View = Bản đồ lộ trình học tập trực quan
- Mỗi cạnh trong đồ thị = 1 mối quan hệ tiên quyết có ý nghĩa
- Sinh viên nhìn Graph View phải hiểu ngay "phải học gì trước"
"""

import os
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional


def generate_knowledge_vault(
    excel_path: str,
    sessions: List[Dict[str, Any]],
    prerequisite_data: Optional[Dict[str, Any]] = None,
    output_dir: str = "obsidian_vault",
) -> str:
    """
    Tạo Obsidian Knowledge Vault đầy đủ với liên kết tiên quyết.
    
    Args:
        excel_path: Đường dẫn file PM Excel (để lấy tên khóa học)
        sessions: Danh sách session đã parse
        prerequisite_data: Kết quả từ prerequisite_guard_agent (có thể None)
        output_dir: Thư mục đầu ra
    
    Returns:
        Đường dẫn tới vault đã tạo
    """
    import openpyxl
    wb = openpyxl.load_workbook(excel_path)
    ws = wb.active
    course_name = ws.title.strip()
    wb.close()

    course_clean = _sanitize_path(course_name)
    vault_path = Path(output_dir) / course_clean

    if vault_path.exists():
        print(f"[OKL] Dọn dẹp vault cũ: {vault_path}")
        shutil.rmtree(vault_path)
    vault_path.mkdir(parents=True, exist_ok=True)

    # Parse prerequisite data nếu có
    session_prereqs = {}
    if prerequisite_data:
        session_prereqs = prerequisite_data.get("session_prerequisites", {})
    
    dep_graph = {}
    if prerequisite_data:
        dep_graph = prerequisite_data.get("dependency_graph", {})

    print(f"[OKL] Tạo Knowledge Vault: {course_name} ({len(sessions)} Sessions)...")

    # ── 1. index.md (Hub trung tâm) ──
    _write_index(vault_path, course_name, course_clean, sessions, dep_graph)

    # ── 2. Session notes với prerequisite links ──
    for s in sessions:
        s_id = s["session_id"]
        s_title = s.get("title", "")
        s_lessons = s.get("lessons", [])
        s_prereq = session_prereqs.get(s_id)

        s_folder_name = _session_folder(s_id, s_title)
        s_dir = vault_path / s_id.replace(" ", "_")
        s_dir.mkdir(parents=True, exist_ok=True)

        _write_session_note(
            s_dir=s_dir,
            s_id=s_id,
            s_title=s_title,
            s_folder_name=s_folder_name,
            s_lessons=s_lessons,
            s_prereq=s_prereq,
        )

        # Quiz stubs
        _write_quiz_stub(s_dir, s_id, "Entrance", s_folder_name)
        _write_quiz_stub(s_dir, s_id, "Exit", s_folder_name)

        # Lesson notes
        for l in s_lessons:
            l_id = l["lesson_id"]
            l_title = l.get("title", "")
            l_details = l.get("details", "")
            l_expected = l.get("expected_output", "")
            l_folder_name = _lesson_folder(l_id, l_title)

            l_dir = s_dir / l_id.replace(" ", "_")
            l_dir.mkdir(parents=True, exist_ok=True)

            _write_lesson_note(
                l_dir=l_dir,
                l_id=l_id,
                l_title=l_title,
                l_folder_name=l_folder_name,
                l_details=l_details,
                l_expected=l_expected,
                s_folder_name=s_folder_name,
                s_id=s_id,
            )

            # Resource stubs
            for resource_type, icon, desc in [
                ("Reading", "📖", "Bài đọc lý thuyết chuyên sâu"),
                ("Slides", "🖼️", "Slide bài giảng tương tác"),
                ("Mindmap", "🧠", "Sơ đồ tư duy bài học"),
                ("Video Script", "📹", "Kịch bản quay video"),
            ]:
                _write_resource_stub(l_dir, l_id, l_title, l_folder_name, resource_type, icon, desc)

    # ── 3. Concept Map (nếu có prerequisite data) ──
    if prerequisite_data and prerequisite_data.get("stats", {}).get("total_concepts", 0) > 0:
        _write_concept_map(vault_path, course_name, prerequisite_data)

    # ── 4. Prerequisite Map tổng quan ──
    _write_prerequisite_map(vault_path, course_name, sessions, session_prereqs)

    vault_str = str(vault_path)
    print(f"[OKL] ✅ Knowledge Vault đã tạo thành công: {vault_str}")
    return vault_str


# ─────────────────────────────────────────────
# Writer Functions
# ─────────────────────────────────────────────

def _write_index(
    vault_path: Path,
    course_name: str,
    course_clean: str,
    sessions: List[Dict],
    dep_graph: Dict,
) -> None:
    """Viết file index.md — Hub trung tâm của toàn bộ vault."""
    session_links = "\n".join([
        f"- [[{_session_folder(s['session_id'], s.get('title', ''))}]]"
        for s in sessions
    ])

    # Tạo lộ trình học tập tuần tự
    learning_path = ""
    if dep_graph.get("edges"):
        chains = _compute_learning_chains(sessions, dep_graph)
        if chains:
            learning_path = "\n## 🗺️ Lộ trình học tập khuyến nghị\n\n"
            for chain in chains[:3]:  # Top 3 chains
                learning_path += "```\n" + " → ".join(chain) + "\n```\n\n"

    content = f"""---
type: course
id: {course_clean}
title: "{course_name}"
tags:
  - learning-material
  - obsidian-graph
  - knowledge-hub
---

# 📚 Môn học: {course_name}

Chào mừng đến với **Bản đồ Tri thức** môn học. Đây là điểm neo trung tâm liên kết toàn bộ tài nguyên học tập.

> 💡 **Cách dùng**: Mở **Graph View** (Ctrl+G) để xem bản đồ lộ trình học tập trực quan. Các đường nối thể hiện mối quan hệ tiên quyết giữa các Session.

## 📅 Danh sách Sessions

{session_links}

## 🔍 Công cụ điều hướng
- [[Prerequisite Map|📊 Bản đồ Tiên quyết Tri thức]]
- [[Concept Map|🧩 Bản đồ Khái niệm]]
{learning_path}
"""
    with open(vault_path / "index.md", "w", encoding="utf-8") as f:
        f.write(content)


def _write_session_note(
    s_dir: Path,
    s_id: str,
    s_title: str,
    s_folder_name: str,
    s_lessons: List[Dict],
    s_prereq: Optional[Any],
) -> None:
    """
    Viết Session note với prerequisite frontmatter và links.
    
    ĐIỂM CẢI TIẾN CHÍNH: Thêm:
    - frontmatter `requires:` danh sách Session tiên quyết
    - Section "📋 Yêu cầu tiên quyết" rõ ràng
    - Section "🎯 Kiến thức sẽ học" (introduces)
    - WikiLinks hai chiều đến Session trước
    """
    requires_sessions = []
    introduces_concepts = []
    required_concepts = []
    violations_text = ""

    if s_prereq:
        # s_prereq có thể là dataclass hoặc dict
        if hasattr(s_prereq, "requires_sessions"):
            requires_sessions = s_prereq.requires_sessions
            introduces_concepts = s_prereq.introduces_concepts
            required_concepts = s_prereq.required_concepts
            violations = s_prereq.violations
        elif isinstance(s_prereq, dict):
            requires_sessions = s_prereq.get("requires_sessions", [])
            introduces_concepts = s_prereq.get("introduces_concepts", [])
            required_concepts = s_prereq.get("required_concepts", [])
            violations = s_prereq.get("violations", [])

        if violations:
            violations_text = "\n> ⚠️ **PM Warnings:**\n"
            for v in violations:
                v_dict = v if isinstance(v, dict) else vars(v)
                violations_text += f"> - [{v_dict.get('severity')}] {v_dict.get('concept_used')} chưa được giới thiệu\n"

    # Frontmatter YAML với prerequisites
    requires_yaml = ""
    if requires_sessions:
        requires_yaml = "requires:\n" + "\n".join(f'  - "{r}"' for r in requires_sessions)

    # Prerequisite section
    prereq_section = ""
    if requires_sessions:
        prereq_section = "\n## 📋 Yêu cầu tiên quyết\n"
        prereq_section += "> 🔴 **Phải hoàn thành trước khi học Session này:**\n\n"
        for req in requires_sessions:
            # Tìm title của session tiên quyết
            prereq_section += f"- [[{req}|✅ {req}]] — Hoàn thành bắt buộc\n"
    else:
        prereq_section = "\n## 📋 Yêu cầu tiên quyết\n"
        prereq_section += "> ✅ Đây là Session **đầu tiên**, không có yêu cầu tiên quyết.\n"

    # Introduces section
    introduces_section = ""
    if introduces_concepts:
        introduces_section = "\n## 🎯 Khái niệm mới sẽ học\n"
        for c in introduces_concepts[:10]:
            introduces_section += f"- `{c.replace('_', ' ')}`\n"

    lesson_links = "\n".join([
        f"- [[{_lesson_folder(l['lesson_id'], l.get('title', ''))}]]"
        for l in s_lessons
    ])

    content = f"""---
type: session
id: {s_id}
title: "{s_title}"
{requires_yaml}
tags:
  - learning-material
  - obsidian-graph
---

# 🗓️ {s_id}: {s_title}

[[index|🏠 Trang chủ môn học]]
{prereq_section}
{violations_text}
{introduces_section}

## 📝 Đề kiểm tra đánh giá
- [[{s_id} - Entrance Quiz|📝 Kiểm tra đầu giờ]]
- [[{s_id} - Exit Quiz|📝 Kiểm tra cuối giờ]]

## 📖 Các bài học
{lesson_links}
"""
    s_filename = f"{s_folder_name}.md"
    with open(s_dir / s_filename, "w", encoding="utf-8") as f:
        f.write(content)


def _write_lesson_note(
    l_dir: Path,
    l_id: str,
    l_title: str,
    l_folder_name: str,
    l_details: str,
    l_expected: str,
    s_folder_name: str,
    s_id: str,
) -> None:
    """Viết Lesson note."""
    content = f"""---
type: lesson
id: {l_id}
title: "{l_title}"
session: "{s_id}"
tags:
  - learning-material
  - obsidian-graph
---

# 🎓 {l_id}: {l_title}

[[{s_folder_name}|⬅️ Quay lại Session cha]]

## 🎯 Chi tiết nội dung học tập
- **Nội dung chi tiết**: {l_details}
- **Sản phẩm mong đợi**: {l_expected}

## 📚 Tài nguyên học tập
- [[{l_id} - Reading|📖 Bài đọc lý thuyết]]
- [[{l_id} - Slides|🖼️ Slide bài giảng]]
- [[{l_id} - Mindmap|🧠 Sơ đồ tư duy]]
- [[{l_id} - Video Script|📹 Kịch bản video]]
"""
    with open(l_dir / f"{l_folder_name}.md", "w", encoding="utf-8") as f:
        f.write(content)


def _write_quiz_stub(s_dir: Path, s_id: str, quiz_type: str, s_folder_name: str) -> None:
    """Viết quiz stub."""
    is_entrance = quiz_type == "Entrance"
    filename = f"{s_id} - {quiz_type} Quiz.md"
    content = f"""---
type: quiz
id: {s_id}-{quiz_type.lower()}
title: "{quiz_type} Quiz - {s_id}"
tags:
  - learning-material
  - obsidian-graph
---

# 📝 {s_id} - {quiz_type} Quiz ({'Đầu giờ' if is_entrance else 'Cuối giờ'})

[[{s_folder_name}|⬅️ Quay lại Session cha]]

- **Số câu hỏi**: 45 câu
- **Mục đích**: {'Ôn tập kiến thức cũ + chuẩn bị bài mới' if is_entrance else 'Đánh giá mức độ tiếp thu bài học'}
"""
    with open(s_dir / filename, "w", encoding="utf-8") as f:
        f.write(content)


def _write_resource_stub(
    l_dir: Path,
    l_id: str,
    l_title: str,
    l_folder_name: str,
    resource_type: str,
    icon: str,
    desc: str,
) -> None:
    """Viết resource stub (Reading, Slides, Mindmap, Video Script)."""
    type_map = {"Reading": "reading", "Slides": "slide", "Mindmap": "mindmap", "Video Script": "video"}
    content = f"""---
type: {type_map.get(resource_type, 'resource')}
id: {l_id}-{resource_type.lower().replace(' ', '-')}
title: "{resource_type} - {l_title}"
tags:
  - learning-material
  - obsidian-graph
---

# {icon} {resource_type}: {l_title}

[[{l_folder_name}|↩️ Quay lại Bài học chính]]

{desc}.
"""
    filename = f"{l_id} - {resource_type}.md"
    with open(l_dir / filename, "w", encoding="utf-8") as f:
        f.write(content)


def _write_prerequisite_map(
    vault_path: Path,
    course_name: str,
    sessions: List[Dict],
    session_prereqs: Dict,
) -> None:
    """
    Viết file Prerequisite Map — Bản đồ lộ trình học tập tổng quan.
    File này là "Navigation Hub" cho Graph View của Obsidian.
    """
    lines = [
        "---",
        "type: prerequisite-map",
        f'title: "Bản đồ Tiên quyết - {course_name}"',
        "tags:",
        "  - learning-material",
        "  - obsidian-graph",
        "  - navigation",
        "---",
        "",
        f"# 📊 Bản đồ Tiên quyết Tri thức: {course_name}",
        "",
        "[[index|🏠 Trang chủ môn học]]",
        "",
        "## 🗺️ Lộ trình học tập (Đọc từ trên xuống)",
        "",
        "> Mỗi Session cần hoàn thành TRƯỚC KHI học Session tiếp theo.",
        "",
    ]

    for s in sessions:
        s_id = s["session_id"]
        s_title = s.get("title", "")
        s_prereq_data = session_prereqs.get(s_id)

        requires = []
        if s_prereq_data:
            if isinstance(s_prereq_data, dict):
                requires = s_prereq_data.get("requires_sessions", [])
            elif hasattr(s_prereq_data, "requires_sessions"):
                requires = s_prereq_data.requires_sessions

        folder_name = _session_folder(s_id, s_title)

        if requires:
            req_str = " + ".join([f"[[{r}]]" for r in requires])
            lines.append(f"- {req_str} → **[[{folder_name}]]**")
        else:
            lines.append(f"- 🏁 **[[{folder_name}]]** ← Điểm bắt đầu")

    with open(vault_path / "Prerequisite Map.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def _write_concept_map(
    vault_path: Path,
    course_name: str,
    prerequisite_data: Dict,
) -> None:
    """Viết Concept Map nếu có dữ liệu từ PrerequisiteGuardAgent."""
    stats = prerequisite_data.get("stats", {})
    lines = [
        "---",
        "type: concept-map",
        f'title: "Bản đồ Khái niệm - {course_name}"',
        "tags:",
        "  - learning-material",
        "  - obsidian-graph",
        "  - concept-map",
        "---",
        "",
        f"# 🧩 Bản đồ Khái niệm: {course_name}",
        "",
        "[[index|🏠 Trang chủ môn học]]",
        "",
        f"**Tổng số khái niệm:** {stats.get('total_concepts', 0)}",
        f"**Tổng vi phạm tiên quyết:** {stats.get('total_violations', 0)}",
        "",
        "> 💡 Xem Graph View để thấy mạng lưới phụ thuộc giữa các khái niệm.",
    ]

    with open(vault_path / "Concept Map.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def _sanitize_path(name: str) -> str:
    """Làm sạch tên để dùng làm tên thư mục."""
    import re
    name = name.replace("&", "va").replace("/", "_").replace("\\", "_")
    name = re.sub(r'[*?:"<>|]', "", name)
    return name.strip().replace(" ", "_")


def _session_folder(s_id: str, s_title: str) -> str:
    title_clean = s_title.replace("/", "_").replace("\\", "_").replace(":", "-")
    return f"{s_id} - {title_clean}"


def _lesson_folder(l_id: str, l_title: str) -> str:
    title_clean = l_title.replace("/", "_").replace("\\", "_").replace(":", "-")
    return f"{l_id} - {title_clean}"


def _compute_learning_chains(
    sessions: List[Dict],
    dep_graph: Dict,
) -> List[List[str]]:
    """Tính các chuỗi học tập tuyến tính từ dependency graph."""
    edges = dep_graph.get("edges", [])
    adj: Dict[str, List[str]] = {}
    for e in edges:
        src = e["from"]
        dst = e["to"]
        if src not in adj:
            adj[src] = []
        adj[src].append(dst)

    # Tìm root nodes (không có incoming edges)
    all_targets = set(e["to"] for e in edges)
    roots = [s["session_id"] for s in sessions if s["session_id"] not in all_targets]

    chains = []
    for root in roots[:3]:
        chain = [root]
        current = root
        while current in adj:
            nexts = adj[current]
            current = nexts[0]
            chain.append(current)
            if len(chain) > 10:
                break
        chains.append(chain)

    return chains
