"""
tests/test_ontology_knowledge_graph.py
Unit and integration tests for:
- Standard Curriculum Ontologies (Python, Java, SQL, Agile).
- Graph cycle detection in curriculum dependencies.
- Missing prerequisite & knowledge gap detection against ontologies.
- Inverted order auditing.
- Bloom progression checks.
- PrerequisiteGuardAgent ontology integration.
"""

import unittest
from core.ontology import (
    get_ontology_for_stack,
    build_python_ontology,
    build_sql_ontology,
    CurriculumOntologyGraph,
    OntologyConcept
)
from core.knowledge_graph import (
    detect_cycles,
    find_missing_prerequisites,
    find_inverted_prerequisite_orders,
    check_bloom_progression,
    resolve_concepts_in_text
)
from agents.prerequisite_guard_agent import prerequisite_guard_agent


class TestOntologyKnowledgeGraph(unittest.TestCase):

    def test_ontology_loading_and_retrieval(self):
        """Tests that standard ontologies can be retrieved by stack keywords."""
        py_ont = get_ontology_for_stack("Python Core")
        self.assertIsNotNone(py_ont)
        self.assertGreaterEqual(len(py_ont.concepts), 10)

        sql_ont = get_ontology_for_stack("SQL Database & Backend")
        self.assertIsNotNone(sql_ont)
        self.assertIn("sql_ddl_tables", sql_ont.concepts)

        java_ont = get_ontology_for_stack("Java Fullstack")
        self.assertIsNotNone(java_ont)

        agile_ont = get_ontology_for_stack("Agile Scrum")
        self.assertIsNotNone(agile_ont)

    def test_transitive_prerequisites(self):
        """Tests recursive prerequisite collection in ontology graph."""
        py_ont = build_python_ontology()
        # Polymorphism -> Inheritance -> Classes -> Functions -> Loops -> Conditionals -> Operators -> Variables
        prereqs = py_ont.get_all_prerequisites_recursive("python_oop_polymorphism")
        self.assertIn("python_oop_inheritance", prereqs)
        self.assertIn("python_oop_classes", prereqs)
        self.assertIn("python_functions", prereqs)
        self.assertIn("python_loops", prereqs)

    def test_concept_resolution_in_text(self):
        """Tests resolving concepts from Vietnamese and English text."""
        py_ont = build_python_ontology()
        text = "Buổi học về Lập trình hướng đối tượng, định nghĩa Class và kế thừa (inheritance)."
        matched = resolve_concepts_in_text(text, py_ont)
        self.assertIn("python_oop_classes", matched)
        self.assertIn("python_oop_inheritance", matched)

    def test_cycle_detection(self):
        """Tests detecting circular dependencies in directed graphs."""
        # Simple cycle: A -> B -> A
        edges_with_cycle = [
            ("Session 01", "Session 02"),
            ("Session 02", "Session 03"),
            ("Session 03", "Session 01"),
        ]
        cycles = detect_cycles(edges_with_cycle)
        self.assertEqual(len(cycles), 1)
        self.assertEqual(cycles[0][0], cycles[0][-1])  # loop starts and ends at same node

        # Acyclic graph: A -> B -> C
        acyclic_edges = [
            ("Session 01", "Session 02"),
            ("Session 02", "Session 03"),
        ]
        no_cycles = detect_cycles(acyclic_edges)
        self.assertEqual(len(no_cycles), 0)

    def test_missing_prerequisite_detection(self):
        """Tests detecting foundational concepts missing entirely from syllabus."""
        py_ont = build_python_ontology()
        # Flawed syllabus: Teaches Inheritance in Session 1, but Classes is completely omitted!
        flawed_curriculum = [
            {
                "session_id": "Session 01",
                "title": "Kế thừa và Đa hình trong Python",
                "details": "Tìm hiểu inheritance và override phương thức",
                "lessons": [
                    {"lesson_id": "Lesson 01", "title": "Kế thừa (Inheritance)", "details": "Kế thừa lớp cha"}
                ]
            }
        ]
        missing = find_missing_prerequisites(flawed_curriculum, py_ont)
        missing_ids = [m.missing_prerequisite_id for m in missing]
        # Must detect that python_oop_classes is missing!
        self.assertIn("python_oop_classes", missing_ids)

    def test_inverted_order_detection(self):
        """Tests detecting when a prerequisite is taught after a dependent concept."""
        py_ont = build_python_ontology()
        # Inverted curriculum: Session 1 teaches Inheritance, Session 2 teaches Classes
        inverted_curriculum = [
            {
                "session_id": "Session 01",
                "title": "Tính kế thừa (Inheritance)",
                "details": "Tìm hiểu inheritance và lớp con",
                "lessons": []
            },
            {
                "session_id": "Session 02",
                "title": "Lớp và Đối tượng (Class and Object)",
                "details": "Định nghĩa class, khởi tạo đối tượng",
                "lessons": []
            }
        ]
        inverted = find_inverted_prerequisite_orders(inverted_curriculum, py_ont)
        self.assertGreaterEqual(len(inverted), 1)
        self.assertEqual(inverted[0]["type"], "INVERTED_ORDER")
        self.assertEqual(inverted[0]["concept_id"], "python_oop_inheritance")

    def test_bloom_progression_check(self):
        """Tests flagging cognitive shock in opening sessions."""
        # Session 1 jumping straight to Bloom 5
        shock_curriculum = [
            {
                "session_id": "Session 01",
                "title": "Kiến trúc hệ thống lớn và Thiết kế phần mềm nâng cao",
                "details": "Kiến trúc hệ thống, phân rã microservices",
                "lessons": []
            }
        ]
        custom_ont = CurriculumOntologyGraph("python")
        custom_ont.add_concept(OntologyConcept(
            concept_id="python_architecture",
            canonical_name_vi="Kiến trúc hệ thống lớn",
            canonical_name_en="System Architecture",
            synonyms=["kiến trúc hệ thống"],
            bloom_level=5
        ))
        violations = check_bloom_progression(shock_curriculum, custom_ont)
        self.assertGreaterEqual(len(violations), 1)
        self.assertEqual(violations[0].session_id, "Session 01")

    def test_prerequisite_guard_agent_end_to_end_with_ontology(self):
        """Tests prerequisite_guard_agent running with ontology and report generation."""
        sessions = [
            {
                "session_id": "Session 01",
                "title": "Biến và Kiểu dữ liệu trong Python",
                "details": "Khai báo biến int, str, float",
                "lessons": [
                    {"lesson_id": "Lesson 01", "title": "Cú pháp biến", "details": "x = 10"}
                ]
            },
            {
                "session_id": "Session 02",
                "title": "Toán tử và Cấu trúc rẽ nhánh điều kiện",
                "details": "Toán tử so sánh, câu lệnh if else",
                "lessons": [
                    {"lesson_id": "Lesson 01", "title": "Câu lệnh if", "details": "if age >= 18"}
                ]
            }
        ]
        result = prerequisite_guard_agent(sessions, tech_stack="python", strict_mode=False)
        self.assertIn("report", result)
        self.assertIn("Mermaid Graph", result["report"])
        self.assertIn("graph TD", result["report"])
        self.assertIn("stats", result)


if __name__ == "__main__":
    unittest.main()
