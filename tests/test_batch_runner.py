# tests/test_batch_runner.py
import unittest
import time
from core.batch_runner import BatchLessonExecutor, execute_lessons_batch_parallel

class TestBatchLessonExecutor(unittest.TestCase):

    def test_empty_batch(self):
        """Verify handling of empty lesson list."""
        results = execute_lessons_batch_parallel([], lambda st: st, max_workers=4)
        self.assertEqual(results, [])

    def test_single_task_sequential_fallback(self):
        """Verify single task runs smoothly."""
        sample = [{"lesson_id": "Lesson_01", "status": "pending"}]
        
        def dummy_workflow(st):
            st["status"] = "completed"
            return st
            
        results = execute_lessons_batch_parallel(sample, dummy_workflow, max_workers=4)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["status"], "completed")

    def test_parallel_execution_speedup(self):
        """Verify that tasks run concurrently and complete in parallel."""
        tasks = [
            {"lesson_id": f"Lesson_0{i}", "value": i}
            for i in range(1, 5)
        ]
        
        def mock_workflow(st):
            time.sleep(0.1)  # Simulate 100ms LLM work
            st["result"] = st["value"] * 10
            return st

        start_time = time.time()
        results = execute_lessons_batch_parallel(tasks, mock_workflow, max_workers=4)
        elapsed = time.time() - start_time

        # If 4 tasks each take 0.1s sequentially, total would be ~0.4s.
        # In parallel with 4 workers, total should be ~0.1s - 0.25s.
        self.assertEqual(len(results), 4)
        self.assertLess(elapsed, 0.35)
        for i, res in enumerate(results, 1):
            self.assertEqual(res["result"], i * 10)

    def test_error_isolation(self):
        """Verify that one crashing task does not prevent other tasks from completing."""
        tasks = [
            {"lesson_id": "Lesson_01", "fail": False},
            {"lesson_id": "Lesson_02", "fail": True},
            {"lesson_id": "Lesson_03", "fail": False},
        ]

        def fragile_workflow(st):
            if st.get("fail"):
                raise ValueError("Simulated pipeline failure for Lesson_02")
            st["processed"] = True
            return st

        results = execute_lessons_batch_parallel(tasks, fragile_workflow, max_workers=3)
        self.assertEqual(len(results), 3)
        self.assertTrue(results[0].get("processed"))
        self.assertTrue(results[2].get("processed"))
        self.assertFalse(results[1].get("processed", False))


if __name__ == "__main__":
    unittest.main()
