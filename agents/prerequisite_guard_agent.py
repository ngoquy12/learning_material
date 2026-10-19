"""
agents/prerequisite_guard_agent.py

Agent 2 — Prerequisite Guard Agent (PGA)
=========================================
Chuyên gia kiểm duyệt PM đảm bảo tính tuần tự tri thức:
- Xây dựng Dependency Graph từ toàn bộ chương trình học
- Phát hiện vi phạm tiên quyết: "Lesson B dùng khái niệm X nhưng X chưa được dạy"
- Tạo ma trận Prerequisites cho từng Session/Lesson
- Cung cấp dữ liệu để ObsidianKnowledgeLinker tạo liên kết

Triết lý thiết kế:
- "Không có khái niệm nào xuất hiện trước khi được giới thiệu"
- "Lộ trình học = Chuỗi DAG (Directed Acyclic Graph) không vòng lặp"
- PM Reviewer phải là khâu CHẶT CHẼ NHẤT trong pipeline
"""

import json
import re
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from pathlib import Path

from core.ontology import get_ontology_for_stack
from core.knowledge_graph import (
    detect_cycles,
    find_missing_prerequisites,
    find_inverted_prerequisite_orders,
    check_bloom_progression,
    resolve_concepts_in_text
)


# ─────────────────────────────────────────────
# Data Models
# ─────────────────────────────────────────────

@dataclass
class ConceptNode:
    """Một khái niệm trong đồ thị tri thức."""
    concept_id: str                  # snake_case identifier
    concept_name: str                # Tên hiển thị
    introduced_in_session: str       # Session đầu tiên dạy khái niệm này
    introduced_in_lesson: str        # Lesson đầu tiên dạy khái niệm này
    tech_stack: str = "*"
    level: str = "basic"             # basic | intermediate | advanced
    related_concepts: List[str] = field(default_factory=list)  # concept_ids liên quan


@dataclass
class PrerequisiteViolation:
    """Một vi phạm tiên quyết được phát hiện."""
    session_id: str
    lesson_id: str
    lesson_title: str
    concept_used: str
    concept_introduced_in: str       # Session/Lesson mà concept này được dạy
    severity: str                    # "BLOCKER" | "WARNING"
    suggestion: str                  # Gợi ý sửa


@dataclass
class SessionPrerequisites:
    """Thông tin tiên quyết của một Session."""
    session_id: str
    session_title: str
    requires_sessions: List[str]     # ["Session 01", "Session 02"]
    required_concepts: List[str]     # Danh sách concept_id cần biết trước
    introduces_concepts: List[str]   # Danh sách concept_id mới trong session này
    violations: List[PrerequisiteViolation] = field(default_factory=list)


# ─────────────────────────────────────────────
# Core Agent Logic
# ─────────────────────────────────────────────

def prerequisite_guard_agent(
    sessions: List[Dict[str, Any]],
    tech_stack: str = "",
    strict_mode: bool = True
) -> Dict[str, Any]:
    """
    Agent chính kiểm duyệt toàn bộ chương trình học.
    
    Args:
        sessions: Danh sách session đã parse từ Excel/PM
        tech_stack: Stack công nghệ
        strict_mode: True = block pipeline nếu có BLOCKER violation
    
    Returns:
        {
            "is_valid": bool,
            "violations": List[PrerequisiteViolation],
            "session_prerequisites": Dict[session_id -> SessionPrerequisites],
            "dependency_graph": Dict (để Obsidian dùng),
            "report": str (báo cáo markdown)
        }
    """
    print("\n[PrerequisiteGuard] 🔍 Phân tích tính tuần tự tri thức của chương trình học...")

    # Bước 1: Trích xuất concept registry bằng LLM
    concept_registry = _extract_concept_registry(sessions, tech_stack)
    print(f"  - Đã trích xuất {len(concept_registry)} khái niệm trong chương trình học.")

    # Bước 2: Xây dựng "already known" set theo thứ tự tuần tự
    session_prereqs: Dict[str, SessionPrerequisites] = {}
    all_violations: List[PrerequisiteViolation] = []
    known_concepts: set = set()   # Tập khái niệm đã được dạy tính đến Session hiện tại

    for session in sessions:
        s_id = session.get("session_id", "")
        s_title = session.get("title", "")
        s_lessons = session.get("lessons", [])

        # Xác định concept mới trong session này
        introduces: List[str] = []
        requires: List[str] = []
        violations_in_session: List[PrerequisiteViolation] = []

        for lesson in s_lessons:
            l_id = lesson.get("lesson_id", "")
            l_title = lesson.get("title", "")
            l_details = lesson.get("details", "")
            l_expected = lesson.get("expected_output", "")

            lesson_content = f"{l_title} {l_details} {l_expected}"

            # Kiểm tra concept nào được dùng trong lesson này
            for concept_id, concept_node in concept_registry.items():
                concept = concept_node if isinstance(concept_node, ConceptNode) else ConceptNode(**concept_node)
                
                # Concept được giới thiệu trong lesson này
                if concept.introduced_in_session == s_id and concept.introduced_in_lesson == l_id:
                    introduces.append(concept_id)
                    known_concepts.add(concept_id)
                
                # Concept được dùng nhưng chưa được giới thiệu
                elif _concept_appears_in_content(concept, lesson_content):
                    if concept_id not in known_concepts:
                        violation = PrerequisiteViolation(
                            session_id=s_id,
                            lesson_id=l_id,
                            lesson_title=l_title,
                            concept_used=concept.concept_name,
                            concept_introduced_in=f"{concept.introduced_in_session} - {concept.introduced_in_lesson}",
                            severity="BLOCKER" if concept.level == "advanced" else "WARNING",
                            suggestion=(
                                f"Di chuyển '{concept.concept_name}' sang sau "
                                f"'{concept.introduced_in_session}', hoặc thêm Session giới thiệu trước."
                            )
                        )
                        violations_in_session.append(violation)
                        all_violations.append(violation)
                    else:
                        requires.append(concept_id)

        # Tính Session tiên quyết từ concept requirements
        required_sessions = []
        for concept_id in requires:
            concept_node = concept_registry.get(concept_id)
            if concept_node:
                concept = concept_node if isinstance(concept_node, ConceptNode) else ConceptNode(**concept_node)
                req_session = concept.introduced_in_session
                if req_session != s_id and req_session not in required_sessions:
                    required_sessions.append(req_session)

        session_prereqs[s_id] = SessionPrerequisites(
            session_id=s_id,
            session_title=s_title,
            requires_sessions=sorted(required_sessions),
            required_concepts=sorted(list(set(requires))),
            introduces_concepts=sorted(list(set(introduces))),
            violations=violations_in_session,
        )

    # Bước 2.5: Kiểm tra Chu trình tuần hoàn (Cycle Detection) & Đối chiếu Ontology chuẩn
    session_edges = [(req, s_id) for s_id, sp in session_prereqs.items() for req in sp.requires_sessions]
    cycles = detect_cycles(session_edges)
    for cycle in cycles:
        cycle_str = " → ".join(cycle)
        v = PrerequisiteViolation(
            session_id=cycle[0],
            lesson_id="",
            lesson_title="Kiến trúc tổng thể",
            concept_used=f"Chu trình phụ thuộc: {cycle_str}",
            concept_introduced_in="Vòng lặp tuần hoàn",
            severity="BLOCKER",
            suggestion=f"Loại bỏ phụ thuộc vòng tròn giữa các session: {cycle_str}"
        )
        all_violations.append(v)

    ontology = get_ontology_for_stack(tech_stack)
    missing_prereqs = []
    inverted_orders = []
    bloom_violations = []
    if ontology:
        missing_prereqs = find_missing_prerequisites(sessions, ontology)
        for mp in missing_prereqs:
            all_violations.append(PrerequisiteViolation(
                session_id=mp.session_id,
                lesson_id=mp.lesson_id,
                lesson_title="Lỗ hổng kiến thức nền tảng (Ontology Gap)",
                concept_used=f"{mp.concept_name} (Thiếu: {mp.missing_prerequisite_name})",
                concept_introduced_in=f"Chuẩn {tech_stack}",
                severity=mp.severity,
                suggestion=mp.suggestion
            ))

        inverted_orders = find_inverted_prerequisite_orders(sessions, ontology)
        for inv in inverted_orders:
            all_violations.append(PrerequisiteViolation(
                session_id=inv["dependent_session"],
                lesson_id="",
                lesson_title="Thứ tự giảng dạy bị đảo ngược",
                concept_used=f"{inv['concept_name']} (cần học sau {inv['prerequisite_name']})",
                concept_introduced_in=inv["prerequisite_session"],
                severity=inv["severity"],
                suggestion=inv["message"]
            ))

        bloom_violations = check_bloom_progression(sessions, ontology)
        for bv in bloom_violations:
            all_violations.append(PrerequisiteViolation(
                session_id=bv.session_id,
                lesson_id="",
                lesson_title="Độ dốc nhận thức Bloom bất hợp lý",
                concept_used=f"Bloom Level {bv.detected_bloom_level}",
                concept_introduced_in=f"Kỳ vọng {bv.expected_bloom_range[0]}-{bv.expected_bloom_range[1]}",
                severity=bv.severity,
                suggestion=bv.suggestion
            ))

    # Bước 3: Xây dựng Dependency Graph cho Obsidian
    dependency_graph = _build_dependency_graph(session_prereqs)

    # Bước 4: Tổng hợp báo cáo
    blocker_count = sum(1 for v in all_violations if v.severity == "BLOCKER")
    warning_count = sum(1 for v in all_violations if v.severity == "WARNING")
    is_valid = blocker_count == 0 if strict_mode else True

    report = _generate_report(
        sessions, all_violations, blocker_count, warning_count, session_prereqs,
        ontology=ontology, cycles=cycles
    )

    print(f"  - Kết quả: {blocker_count} BLOCKER, {warning_count} WARNING violations.")
    if is_valid:
        print("  ✅ [PrerequisiteGuard] PM đạt chuẩn tuần tự tri thức & Ontology.")
    else:
        print(f"  🔴 [PrerequisiteGuard] PM CÓ {blocker_count} vi phạm BLOCKER cần sửa trước khi biên dịch!")

    return {
        "is_valid": is_valid,
        "violations": [asdict(v) for v in all_violations],
        "session_prerequisites": {
            k: asdict(v) for k, v in session_prereqs.items()
        },
        "dependency_graph": dependency_graph,
        "report": report,
        "stats": {
            "total_concepts": len(concept_registry),
            "total_violations": len(all_violations),
            "blocker_count": blocker_count,
            "warning_count": warning_count,
            "cycles_count": len(cycles),
            "missing_prerequisites_count": len(missing_prereqs),
            "inverted_orders_count": len(inverted_orders),
        }
    }


def _extract_concept_registry(
    sessions: List[Dict[str, Any]],
    tech_stack: str
) -> Dict[str, ConceptNode]:
    """
    Dùng LLM để trích xuất toàn bộ khái niệm từ chương trình học
    và xác định chúng được giới thiệu lần đầu ở đâu.
    Hỗ trợ chia Batch tự động cho khóa học dài để không bị mất mát thông tin.
    """
    try:
        from core.llm import call_llm

        registry: Dict[str, ConceptNode] = {}
        batch_size = 10  # Xử lý theo batch 10 Session để đảm bảo bao phủ 100% môn học dài

        for i in range(0, len(sessions), batch_size):
            session_batch = sessions[i:i + batch_size]
            
            curriculum_summary = []
            for s in session_batch:
                s_entry = {
                    "session_id": s.get("session_id"),
                    "title": s.get("title"),
                    "lessons": [
                        {
                            "lesson_id": l.get("lesson_id"),
                            "title": l.get("title"),
                            "details": l.get("details", "")[:200],  # Lấy đầy đủ chi tiết hơn
                        }
                        for l in s.get("lessons", [])  # BAO PHỦ 100% LESSONS, KHÔNG CẮT GIẢM
                    ]
                }
                curriculum_summary.append(s_entry)

            system_prompt = (
                "You are an Instructional Curriculum Architect and Dependency Graph Specialist. "
                "Analyze the curriculum segment, extract ALL core technical concepts, and determine "
                "which lesson introduces each concept for the first time."
            )

            user_prompt = f"""Analyze the curriculum segment for technology stack {tech_stack} (Session {i+1} to {i+len(session_batch)}):

{json.dumps(curriculum_summary, ensure_ascii=False, indent=2)}

Extract all core technical concepts taught in this segment. Return a raw JSON object:
{{
  "concept_id_snake_case": {{
    "concept_id": "concept_id_snake_case",
    "concept_name": "Concept Title",
    "introduced_in_session": "Session XX",
    "introduced_in_lesson": "Lesson XX",
    "tech_stack": "{tech_stack}",
    "level": "basic|intermediate|advanced",
    "related_concepts": []
  }}
}}

Return ONLY raw JSON without markdown wrappers.
"""

            response = call_llm(
                system_prompt, user_prompt,
                json_mode=True,
                agent_name="PrerequisiteGuard_ConceptExtractor",
            )

            if response:
                cleaned = response.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
                try:
                    raw = json.loads(cleaned)
                    for cid, data in raw.items():
                        if isinstance(data, dict) and cid not in registry:
                            registry[cid] = ConceptNode(**{
                                k: v for k, v in data.items()
                                if k in ConceptNode.__dataclass_fields__
                            })
                except Exception as parse_err:
                    print(f"  [PrerequisiteGuard Warning] Parse batch {i//batch_size + 1} JSON failed: {parse_err}")

        if registry:
            return registry

    except Exception as e:
        print(f"  [PrerequisiteGuard Warning] LLM extract concepts failed: {e}")

    # Fallback: registry rỗng
    return {}


def _concept_appears_in_content(concept: ConceptNode, content: str) -> bool:
    """Kiểm tra xem concept có xuất hiện trong nội dung lesson không với regex ranh giới từ an toàn."""
    content_lower = content.lower()
    c_name = concept.concept_name.lower().strip()
    c_id_space = concept.concept_id.lower().replace("_", " ").strip()

    # Nếu tên concept ngắn (< 3 ký tự như OS, IP, C), bắt buộc khớp regex ranh giới từ để tránh false match
    if len(c_name) < 3:
        pattern = r"\b" + re.escape(c_name) + r"\b"
        return bool(re.search(pattern, content_lower))

    return c_name in content_lower or c_id_space in content_lower


def _build_dependency_graph(
    session_prereqs: Dict[str, SessionPrerequisites]
) -> Dict[str, Any]:
    """
    Xây dựng Directed Acyclic Graph của Session dependencies.
    Format tương thích với Obsidian WikiLinks và D3.js visualization.
    """
    nodes = []
    edges = []

    for s_id, s_prereq in session_prereqs.items():
        nodes.append({
            "id": s_id,
            "title": s_prereq.session_title,
            "introduces_count": len(s_prereq.introduces_concepts),
            "requires_count": len(s_prereq.required_concepts),
            "has_violations": len(s_prereq.violations) > 0,
        })
        for req_session in s_prereq.requires_sessions:
            edges.append({
                "from": req_session,
                "to": s_id,
                "type": "prerequisite",
                "label": "phải học trước",
            })

    return {
        "nodes": nodes,
        "edges": edges,
        "metadata": {
            "total_sessions": len(nodes),
            "total_dependencies": len(edges),
        }
    }


def _generate_report(
    sessions: List[Dict],
    violations: List[PrerequisiteViolation],
    blocker_count: int,
    warning_count: int,
    session_prereqs: Dict[str, SessionPrerequisites],
    ontology: Optional[Any] = None,
    cycles: Optional[List[List[str]]] = None
) -> str:
    """Tạo báo cáo Markdown cho PM Reviewer với Đồ thị Mermaid và đối chiếu Ontology."""
    lines = [
        "# 🔍 Báo cáo Kiểm duyệt Tiên quyết Tri thức (Prerequisite Guard & Ontology)",
        "",
        f"**Tổng vi phạm:** {len(violations)} "
        f"({blocker_count} 🔴 BLOCKER | {warning_count} 🟡 WARNING)",
        "",
    ]

    if ontology:
        lines += [
            f"**Ontology đối chuẩn:** `{ontology.domain_name}` ({len(ontology.concepts)} khái niệm chuẩn ngành)",
            ""
        ]

    if cycles:
        lines += [
            "## 🔴 Chu trình tuần hoàn (Circular Dependencies)",
            "Hệ thống phát hiện các mối quan hệ phụ thuộc vòng tròn gây tắc nghẽn lộ trình học:",
            ""
        ]
        for c in cycles:
            lines.append(f"- ⚠️ **Vòng lặp:** `{' → '.join(c)}`")
        lines.append("")

    if violations:
        lines.append("## ❌ Danh sách vi phạm chi tiết")
        for v in violations:
            icon = "🔴" if v.severity == "BLOCKER" else "🟡"
            lines += [
                f"",
                f"### {icon} [{v.severity}] {v.session_id} - {v.lesson_title}",
                f"- **Khái niệm / Lỗi:** `{v.concept_used}`",
                f"- **Nguồn đối chiếu:** {v.concept_introduced_in}",
                f"- **Gợi ý khắc phục:** {v.suggestion}",
            ]
    else:
        lines.append("## ✅ Không có vi phạm nào được phát hiện")

    lines += [
        "",
        "## 📊 Lộ trình học tập (Dependency Chain)",
    ]
    for s_id, s_prereq in session_prereqs.items():
        if s_prereq.requires_sessions:
            reqs = " → ".join(s_prereq.requires_sessions + [s_id])
            lines.append(f"- {reqs}")

    # Mermaid Dependency Graph
    lines += [
        "",
        "## 🗺️ Bản đồ Đồ thị Phụ thuộc (Mermaid Graph)",
        "```mermaid",
        "graph TD"
    ]
    edges_added = False
    for s_id, s_prereq in session_prereqs.items():
        clean_s_id = s_id.replace(" ", "_")
        for req in s_prereq.requires_sessions:
            clean_req = req.replace(" ", "_")
            lines.append(f"    {clean_req} --> {clean_s_id}")
            edges_added = True
    if not edges_added:
        for i in range(len(sessions) - 1):
            s1 = sessions[i].get("session_id", f"Session_{i+1}").replace(" ", "_")
            s2 = sessions[i+1].get("session_id", f"Session_{i+2}").replace(" ", "_")
            lines.append(f"    {s1} --> {s2}")
    lines.append("```")

    return "\n".join(lines)


# ─────────────────────────────────────────────
# Tích hợp vào Main Pipeline
# ─────────────────────────────────────────────

def run_prerequisite_check_for_pm(
    sessions: List[Dict[str, Any]],
    tech_stack: str,
    output_report_path: Optional[str] = None,
) -> Tuple[bool, Dict[str, Any]]:
    """
    Hàm tiện ích để gọi từ main.py trước khi bắt đầu biên dịch học liệu.
    Trả về True nếu PM hợp lệ, False nếu có BLOCKER violations.
    """
    result = prerequisite_guard_agent(sessions, tech_stack, strict_mode=True)

    # Lưu báo cáo nếu được yêu cầu
    if output_report_path and result.get("report"):
        Path(output_report_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_report_path, "w", encoding="utf-8") as f:
            f.write(result["report"])
        print(f"  [PrerequisiteGuard] Đã lưu báo cáo: {output_report_path}")

    return result["is_valid"], result
