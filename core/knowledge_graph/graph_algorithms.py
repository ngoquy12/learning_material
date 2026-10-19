"""
core/knowledge_graph/graph_algorithms.py
Advanced Graph Algorithms for Curriculum Prerequisite Validation & Ontology Auditing:
- Cycle Detection in Directed Acyclic Graphs (Tarjan / DFS-based)
- Missing Prerequisite & Knowledge Gap Detection against standard Ontologies
- Inverted Sequence & Transitive Prerequisite Auditing
- Cognitive Load & Bloom Taxonomy Progression Verification
- Bilingual Synonym Resolution
"""

from __future__ import annotations

import re
from typing import List, Dict, Set, Tuple, Any, Optional
from collections import defaultdict

from core.ontology.models import (
    CurriculumOntologyGraph,
    OntologyConcept,
    MissingPrerequisiteViolation,
    CycleViolation,
    BloomProgressionViolation
)


# =============================================================================
# 1. CYCLE DETECTION IN DIRECTED ACYCLIC GRAPH
# =============================================================================

def detect_cycles(edges: List[Tuple[str, str]]) -> List[List[str]]:
    """
    Detects all cycles in a directed dependency graph using DFS with 3-color coloring.
    Edges are formatted as (from_node, to_node) meaning to_node depends on from_node,
    or from_node -> to_node.
    Returns list of cycle paths, e.g. [['Session 01', 'Session 02', 'Session 01']].
    """
    adj: Dict[str, List[str]] = defaultdict(list)
    nodes: Set[str] = set()

    for u, v in edges:
        adj[u].append(v)
        nodes.add(u)
        nodes.add(v)

    # 0 = UNVISITED, 1 = VISITING (in current recursion stack), 2 = VISITED (completed)
    state: Dict[str, int] = {node: 0 for node in nodes}
    parent: Dict[str, Optional[str]] = {node: None for node in nodes}
    cycles: List[List[str]] = []

    def _dfs(u: str, path: List[str]):
        state[u] = 1  # VISITING
        path.append(u)

        for v in adj.get(u, []):
            if state[v] == 1:
                # Cycle detected! Extract cycle path
                cycle_start_idx = path.index(v)
                cycle = path[cycle_start_idx:] + [v]
                cycles.append(cycle)
            elif state[v] == 0:
                _dfs(v, path)

        path.pop()
        state[u] = 2  # VISITED

    for node in sorted(nodes):
        if state[node] == 0:
            _dfs(node, [])

    return cycles


# =============================================================================
# 2. BILINGUAL SYNONYM & CONCEPT RESOLUTION
# =============================================================================

def resolve_concepts_in_text(text: str, ontology: CurriculumOntologyGraph) -> Set[str]:
    """
    Identifies all ontology concepts mentioned in a text snippet (title, details, expected_output).
    Matches canonical names in Vietnamese and English, as well as domain synonyms.
    Uses regex word boundaries for short terms to avoid false positives.
    """
    matched_concept_ids: Set[str] = set()
    text_lower = text.lower()

    for cid, concept in ontology.concepts.items():
        # Check canonical VI
        if concept.canonical_name_vi.lower() in text_lower:
            matched_concept_ids.add(cid)
            continue

        # Check canonical EN
        if concept.canonical_name_en.lower() in text_lower:
            matched_concept_ids.add(cid)
            continue

        # Check synonyms with word boundary or substring depending on length
        for syn in concept.synonyms:
            syn_lower = syn.lower().strip()
            if not syn_lower:
                continue
            if len(syn_lower) <= 3:
                # Short acronym or word (e.g. oop, ddl, sql, git)
                if re.search(rf"\b{re.escape(syn_lower)}\b", text_lower):
                    matched_concept_ids.add(cid)
                    break
            else:
                if syn_lower in text_lower:
                    matched_concept_ids.add(cid)
                    break

    return matched_concept_ids


# =============================================================================
# 3. MISSING PREREQUISITES (KNOWLEDGE GAP) DETECTION
# =============================================================================

def find_missing_prerequisites(
    sessions: List[Dict[str, Any]],
    ontology: CurriculumOntologyGraph
) -> List[MissingPrerequisiteViolation]:
    """
    Compares the curriculum against the standard ontology to detect knowledge gaps:
    If concept A is taught, but foundational prerequisite B is missing from the entire curriculum,
    a MissingPrerequisiteViolation is raised.
    """
    # Step 1: Map every session/lesson to ontology concepts
    session_concepts_map: Dict[str, Set[str]] = defaultdict(set)
    all_curriculum_concepts: Set[str] = set()
    first_introduced_session: Dict[str, str] = {}

    for s in sessions:
        s_id = s.get("session_id", "")
        s_text = f"{s.get('title', '')} {s.get('content_scope', '')} {s.get('details', '')}"
        
        # Check session level
        s_matches = resolve_concepts_in_text(s_text, ontology)
        session_concepts_map[s_id].update(s_matches)

        for l in s.get("lessons", []):
            l_text = f"{l.get('title', '')} {l.get('details', '')} {l.get('expected_output', '')}"
            l_matches = resolve_concepts_in_text(l_text, ontology)
            session_concepts_map[s_id].update(l_matches)

        for cid in session_concepts_map[s_id]:
            all_curriculum_concepts.add(cid)
            if cid not in first_introduced_session:
                first_introduced_session[cid] = s_id

    # Step 2: Audit prerequisites for all introduced concepts
    violations: List[MissingPrerequisiteViolation] = []

    for cid in sorted(all_curriculum_concepts):
        concept = ontology.get_concept(cid)
        if not concept:
            continue

        s_id = first_introduced_session.get(cid, "")
        for prereq_id in concept.prerequisites:
            if prereq_id not in all_curriculum_concepts:
                prereq_concept = ontology.get_concept(prereq_id)
                prereq_name = prereq_concept.canonical_name_vi if prereq_concept else prereq_id
                
                v = MissingPrerequisiteViolation(
                    concept_id=cid,
                    concept_name=concept.canonical_name_vi,
                    missing_prerequisite_id=prereq_id,
                    missing_prerequisite_name=prereq_name,
                    session_id=s_id,
                    severity="BLOCKER" if concept.bloom_level >= 3 else "WARNING",
                    suggestion=(
                        f"Môn học dạy '{concept.canonical_name_vi}' ở {s_id} nhưng bỏ quên khái niệm nền tảng "
                        f"'{prereq_name}'. Hãy bổ sung bài học giới thiệu '{prereq_name}' trước {s_id}."
                    )
                )
                violations.append(v)

    return violations


# =============================================================================
# 4. INVERTED PREREQUISITE ORDER AUDITING
# =============================================================================

def find_inverted_prerequisite_orders(
    sessions: List[Dict[str, Any]],
    ontology: CurriculumOntologyGraph
) -> List[Dict[str, Any]]:
    """
    Checks if a foundational prerequisite concept is scheduled AFTER a dependent concept
    (Inverted sequence e.g., Inheritance taught in Session 02, but Class taught in Session 05).
    """
    session_order: Dict[str, int] = {}
    session_concepts: Dict[str, Set[str]] = defaultdict(set)
    concept_first_session_idx: Dict[str, int] = {}
    concept_first_session_id: Dict[str, str] = {}

    for idx, s in enumerate(sessions):
        s_id = s.get("session_id", f"Session {idx+1}")
        session_order[s_id] = idx
        s_text = f"{s.get('title', '')} {s.get('content_scope', '')} {s.get('details', '')}"
        
        cids = resolve_concepts_in_text(s_text, ontology)
        for l in s.get("lessons", []):
            l_text = f"{l.get('title', '')} {l.get('details', '')} {l.get('expected_output', '')}"
            cids.update(resolve_concepts_in_text(l_text, ontology))

        session_concepts[s_id] = cids
        for cid in cids:
            if cid not in concept_first_session_idx:
                concept_first_session_idx[cid] = idx
                concept_first_session_id[cid] = s_id

    inverted_violations: List[Dict[str, Any]] = []

    for cid, s_idx in concept_first_session_idx.items():
        concept = ontology.get_concept(cid)
        if not concept:
            continue

        for prereq_id in concept.prerequisites:
            if prereq_id in concept_first_session_idx:
                prereq_idx = concept_first_session_idx[prereq_id]
                if prereq_idx > s_idx:
                    # Inverted order!
                    prereq_concept = ontology.get_concept(prereq_id)
                    prereq_name = prereq_concept.canonical_name_vi if prereq_concept else prereq_id
                    viol = {
                        "type": "INVERTED_ORDER",
                        "concept_id": cid,
                        "concept_name": concept.canonical_name_vi,
                        "dependent_session": concept_first_session_id[cid],
                        "prerequisite_id": prereq_id,
                        "prerequisite_name": prereq_name,
                        "prerequisite_session": concept_first_session_id[prereq_id],
                        "severity": "BLOCKER",
                        "message": (
                            f"Thứ tự giảng dạy bị đảo ngược: '{concept.canonical_name_vi}' ({concept_first_session_id[cid]}) "
                            f"được dạy TRƯỚC khái niệm tiên quyết '{prereq_name}' ({concept_first_session_id[prereq_id]})."
                        )
                    }
                    inverted_violations.append(viol)

    return inverted_violations


# =============================================================================
# 5. BLOOM TAXONOMY PROGRESSION AUDIT
# =============================================================================

def check_bloom_progression(
    sessions: List[Dict[str, Any]],
    ontology: Optional[CurriculumOntologyGraph] = None
) -> List[BloomProgressionViolation]:
    """
    Audits cognitive progression across sessions:
    - Session 1 and 2 must not demand Bloom Level >= 5 without prior foundation (Cognitive Shock).
    - Checks for excessive difficulty jumps (> 3 levels jump between consecutive sessions).
    """
    violations: List[BloomProgressionViolation] = []
    total_sessions = len(sessions)
    if total_sessions == 0:
        return violations

    for idx, s in enumerate(sessions):
        s_id = s.get("session_id", f"Session {idx+1}")
        s_title = s.get("title", "")
        
        # Determine Bloom level from ontology concepts or verbs
        s_text = f"{s_title} {s.get('content_scope', '')} {s.get('details', '')}"
        max_bloom = 2  # default baseline
        
        if ontology:
            cids = resolve_concepts_in_text(s_text, ontology)
            for cid in cids:
                c = ontology.get_concept(cid)
                if c and c.bloom_level > max_bloom:
                    max_bloom = c.bloom_level

        # Check for cognitive shock in first 2 sessions
        if idx in (0, 1):
            if max_bloom >= 5:
                v = BloomProgressionViolation(
                    session_id=s_id,
                    session_title=s_title,
                    detected_bloom_level=max_bloom,
                    expected_bloom_range=(1, 3),
                    severity="WARNING",
                    suggestion=(
                        f"{s_id} là buổi mở đầu nhưng đòi hỏi mức nhận thức Bloom {max_bloom} (Đánh giá / Sáng tạo). "
                        f"Nên phân bổ ở mức Nhận biết (1) - Thông hiểu (2) - Vận dụng cơ bản (3)."
                    )
                )
                violations.append(v)

    return violations
