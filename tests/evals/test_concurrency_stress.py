"""
tests/evals/test_concurrency_stress.py
Stress test verifying multithreaded database operations and prompt manager rendering.
Ensures zero race conditions, zero deadlocks, and thread-safe persistence under load.
"""

import os
import unittest
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.persistence import save_checkpoint, load_checkpoint
from core.prompts import PromptManager, render_prompt

class TestConcurrencyStress(unittest.TestCase):

    def test_multithreaded_sqlite_checkpoints(self):
        """Spawns 10 concurrent threads reading and writing checkpoints to SQLite."""
        num_workers = 10
        iterations = 5

        def _worker_task(worker_id: int):
            for i in range(iterations):
                key = f"stress_worker_{worker_id}_step_{i}"
                state_data = {
                    "worker_id": worker_id,
                    "iteration": i,
                    "session_id": f"Session_{worker_id}",
                    "status": "COMPLETED"
                }
                save_checkpoint(key, state_data)
                loaded = load_checkpoint(key)
                if loaded is None or loaded.get("worker_id") != worker_id:
                    return False
            return True

        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = [executor.submit(_worker_task, wid) for wid in range(num_workers)]
            for f in as_completed(futures):
                result = f.result()
                self.assertTrue(result, "Concurrent SQLite worker failed read/write assertion.")

    def test_concurrent_prompt_manager_rendering(self):
        """Spawns concurrent threads rendering Jinja2 prompt templates."""
        pm = PromptManager.get_instance()
        
        def _render_task(task_id: int):
            context = {
                "tech_stack": f"Stack_{task_id}",
                "session_id": f"Session {task_id}",
                "lesson_id": f"Lesson {task_id}",
                "lesson_title": f"Title {task_id}",
                "idx": task_id,
                "level_name": "Basic Application",
                "chosen_domain": "E-Commerce",
                "domain_rules_text": "Calculate subtotal and taxes."
            }
            res = pm.render("homework_creator.j2", context)
            return len(res) > 50

        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(_render_task, i) for i in range(16)]
            for f in as_completed(futures):
                self.assertTrue(f.result())

if __name__ == "__main__":
    unittest.main()
