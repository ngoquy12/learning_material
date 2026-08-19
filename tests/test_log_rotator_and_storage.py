"""
tests/test_log_rotator_and_storage.py
Unit tests for core.storage.log_rotator and log administration features.
"""

import unittest
import tempfile
import os
import time
from pathlib import Path
from core.storage import (
    rotate_trace_logs,
    clean_old_logs,
    vacuum_trace_logs,
    get_storage_metrics,
)

class TestLogRotatorAndStorage(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_rotate_trace_logs(self):
        """Tests log file rotation when file size exceeds threshold."""
        log_file = self.storage_path / "trace_logs.jsonl"
        # Write dummy lines
        log_file.write_text("line1\nline2\nline3\n", encoding="utf-8")

        # Threshold 0.0 MB forces rotation
        rotated = rotate_trace_logs(str(log_file), max_size_mb=0.0, backup_count=3)
        self.assertTrue(rotated)

        # Original file should be empty (touched)
        self.assertTrue(log_file.exists())
        self.assertEqual(log_file.read_text(encoding="utf-8"), "")

        # Backup .1 should contain original content
        backup1 = self.storage_path / "trace_logs.jsonl.1"
        self.assertTrue(backup1.exists())
        self.assertEqual(backup1.read_text(encoding="utf-8"), "line1\nline2\nline3\n")

    def test_vacuum_trace_logs(self):
        """Tests pruning trace log to maximum number of entries."""
        log_file = self.storage_path / "trace_logs.jsonl"
        lines = [f'{{"idx": {i}}}' for i in range(10)]
        log_file.write_text("\n".join(lines) + "\n", encoding="utf-8")

        pruned = vacuum_trace_logs(str(log_file), max_entries=3)
        self.assertEqual(pruned, 7)

        remaining = log_file.read_text(encoding="utf-8").strip().splitlines()
        self.assertEqual(len(remaining), 3)
        self.assertIn('{"idx": 9}', remaining[-1])

    def test_clean_old_logs(self):
        """Tests removal of logs older than max_age_days."""
        old_log = self.storage_path / "trace_logs.jsonl.5"
        old_log.write_text("old data", encoding="utf-8")

        # Manipulate mtime to be 40 days in the past
        past_time = time.time() - (40 * 86400)
        os.utime(str(old_log), (past_time, past_time))

        removed = clean_old_logs(str(self.storage_path), max_age_days=30)
        self.assertEqual(removed, 1)
        self.assertFalse(old_log.exists())

    def test_get_storage_metrics(self):
        """Tests metrics calculation of storage directory."""
        log_file = self.storage_path / "trace_logs.jsonl"
        log_file.write_text("a" * 1024, encoding="utf-8")

        metrics = get_storage_metrics(str(self.storage_path), str(self.storage_path))
        self.assertGreaterEqual(metrics["storage_size_bytes"], 1024)
        self.assertGreaterEqual(metrics["trace_log_size_bytes"], 1024)

if __name__ == "__main__":
    unittest.main()
