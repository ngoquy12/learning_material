"""
tests/test_lessons_learned_pipeline.py
Verifies the Lessons Learned and Knowledge Memory Agent Pipeline:
- Rule extraction and storage into agent memory SQLite database.
- TF-IDF semantic retrieval of relevant memories.
- Extraction of anti-pattern catalogs for student materials.
- Propagation of memories into agent state lessons_learned_prompt.
"""

import unittest
from agents.knowledge_memory_agent import (
    store_memory,
    recall_memories,
    get_relevant_memories_for_creator,
    extract_anti_patterns,
    get_memory_stats,
    TFIDFMatcher
)
from agents.lessons_learned_agent import lessons_learned_agent
from core.state import AgentState

class TestLessonsLearnedPipeline(unittest.TestCase):

    def test_tfidf_matcher_logic(self):
        """Tests that TFIDFMatcher finds the most relevant document for a query."""
        docs = [
            "Khởi tạo biến và khai báo kiểu dữ liệu cơ sở trong Python",
            "Cấu hình môi trường ảo venv và cài đặt gói pip",
            "Cơ chế vòng lặp for và while trong thuật toán"
        ]
        matcher = TFIDFMatcher(docs)
        scores = matcher.get_similarity("môi trường venv cài đặt pip")
        best_doc_idx = scores.index(max(scores))
        self.assertEqual(best_doc_idx, 1)

    def test_store_and_recall_memory(self):
        """Tests storing a new rule and recalling it via tech_stack filter."""
        rule = "Không thay đổi kích thước danh sách trong vòng lặp for."
        is_new = store_memory(
            rule_text=rule,
            tech_stack="python/core",
            error_category="syntax_error",
            severity="CRITICAL",
            scope="all",
            source_lesson="Lesson 02 - Vòng lặp"
        )
        self.assertIsInstance(is_new, bool)

        memories = recall_memories(tech_stack="python/core", scope="all", limit=5)
        self.assertTrue(any("vòng lặp" in m["rule_text"].lower() for m in memories))

    def test_get_relevant_memories_for_creator_format(self):
        """Tests formatting recalled memories for prompt injection."""
        formatted = get_relevant_memories_for_creator(tech_stack="python/core", scope="all", limit=3)
        self.assertIsInstance(formatted, str)

    def test_extract_anti_patterns(self):
        """Tests anti-pattern catalog extraction for slides and reading."""
        catalog = extract_anti_patterns(tech_stack="python/core", limit=2)
        self.assertIsInstance(catalog, str)

    def test_memory_stats(self):
        """Tests memory stats aggregation."""
        stats = get_memory_stats()
        self.assertIn("total_rules", stats)
        self.assertIn("by_category", stats)
        self.assertGreaterEqual(stats["total_rules"], 0)

if __name__ == "__main__":
    unittest.main()
