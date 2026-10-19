"""
core/ontology/models.py
Data models and graph structure for standard curriculum ontologies and prerequisite tracking.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional, Any


@dataclass
class OntologyConcept:
    """A canonical knowledge concept defined in an industry/academic standard ontology."""
    concept_id: str                      # snake_case identifier e.g. 'python_oop_classes'
    canonical_name_vi: str               # Tên chuẩn tiếng Việt e.g. 'Lập trình hướng đối tượng & Class'
    canonical_name_en: str               # English standard name e.g. 'Object-Oriented Programming & Classes'
    synonyms: List[str] = field(default_factory=list)  # Synonyms in VI/EN e.g. ['oop', 'class', 'lớp', 'đối tượng']
    prerequisites: List[str] = field(default_factory=list)  # Required concept_ids before learning this
    bloom_level: int = 2                 # 1: Remember, 2: Understand, 3: Apply, 4: Analyze, 5: Evaluate, 6: Create
    category: str = "core"               # syntax | oop | data_structures | architecture | tooling
    tech_stack: str = "*"
    description: str = ""

    def matches_term(self, term: str) -> bool:
        """Checks if a string term matches this concept's canonical names or synonyms."""
        t_lower = term.lower().strip()
        if not t_lower:
            return False
        if t_lower == self.concept_id.replace("_", " "):
            return True
        if t_lower in self.canonical_name_vi.lower() or t_lower in self.canonical_name_en.lower():
            return True
        return any(t_lower == s.lower() or t_lower in s.lower() for s in self.synonyms)


@dataclass
class MissingPrerequisiteViolation:
    """Represents a foundational concept required by the ontology that is missing from the curriculum."""
    concept_id: str
    concept_name: str
    missing_prerequisite_id: str
    missing_prerequisite_name: str
    session_id: str
    lesson_id: str = ""
    severity: str = "BLOCKER"            # BLOCKER | WARNING
    suggestion: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "MISSING_PREREQUISITE",
            "concept_id": self.concept_id,
            "concept_name": self.concept_name,
            "missing_prerequisite_id": self.missing_prerequisite_id,
            "missing_prerequisite_name": self.missing_prerequisite_name,
            "session_id": self.session_id,
            "lesson_id": self.lesson_id,
            "severity": self.severity,
            "suggestion": self.suggestion,
        }


@dataclass
class CycleViolation:
    """Represents a circular dependency in the curriculum prerequisite graph."""
    cycle_path: List[str]                # e.g. ["Session 01", "Session 03", "Session 01"]
    severity: str = "BLOCKER"
    message: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "CIRCULAR_DEPENDENCY",
            "cycle_path": self.cycle_path,
            "severity": self.severity,
            "message": self.message or f"Phát hiện chu trình phụ thuộc vòng tròn: {' -> '.join(self.cycle_path)}"
        }


@dataclass
class BloomProgressionViolation:
    """Represents an irrational cognitive jump or improper cognitive load distribution."""
    session_id: str
    session_title: str
    detected_bloom_level: int
    expected_bloom_range: Tuple[int, int]
    severity: str = "WARNING"
    suggestion: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "BLOOM_PROGRESSION_ERROR",
            "session_id": self.session_id,
            "session_title": self.session_title,
            "detected_bloom_level": self.detected_bloom_level,
            "expected_bloom_range": list(self.expected_bloom_range),
            "severity": self.severity,
            "suggestion": self.suggestion
        }


class CurriculumOntologyGraph:
    """Holds a directed graph of domain knowledge concepts and their relationships."""

    def __init__(self, tech_stack: str, domain_name: str = ""):
        self.tech_stack = tech_stack
        self.domain_name = domain_name or tech_stack
        self.concepts: Dict[str, OntologyConcept] = {}

    def add_concept(self, concept: OntologyConcept) -> None:
        self.concepts[concept.concept_id] = concept

    def get_concept(self, concept_id: str) -> Optional[OntologyConcept]:
        return self.concepts.get(concept_id)

    def find_concept_by_term(self, term: str) -> Optional[OntologyConcept]:
        """Finds a matching concept by term or synonym."""
        t_clean = term.lower().strip()
        if not t_clean:
            return None
        # Exact ID match
        if t_clean in self.concepts:
            return self.concepts[t_clean]
        # Match by name or synonym
        for c in self.concepts.values():
            if c.matches_term(t_clean):
                return c
        return None

    def get_all_prerequisites_recursive(self, concept_id: str) -> Set[str]:
        """Recursively collects all transitive prerequisite concept_ids for a given concept."""
        visited: Set[str] = set()

        def _dfs(cid: str):
            c = self.concepts.get(cid)
            if not c:
                return
            for prereq in c.prerequisites:
                if prereq not in visited:
                    visited.add(prereq)
                    _dfs(prereq)

        _dfs(concept_id)
        return visited

    def __len__(self) -> int:
        return len(self.concepts)
