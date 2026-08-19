"""
tests/test_homework_cleanup.py
Unit tests verifying redundant/junk file detection, automated structure review, and cleanup in Homework Suite.
"""

import unittest
import tempfile
import shutil
from pathlib import Path

from agents.reviewers.homework_reviewer import (
    cleanup_redundant_homework_assets,
    review_session_homework,
    ALLOWED_ROOT_FILES
)

class TestHomeworkCleanup(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.hw_path = Path(self.test_dir) / "Bài tập"
        self.hw_path.mkdir(parents=True, exist_ok=True)

        # Create valid 18 root files
        for i in range(1, 16):
            (self.hw_path / f"bai_tap_{i}.md").write_text("# Bài tập " + "x" * 400, encoding="utf-8")
        (self.hw_path / "bai_tap_tong_hop.md").write_text("# Bài tập Tổng hợp " + "x" * 400, encoding="utf-8")
        (self.hw_path / "bai_tap_mindmap.md").write_text("# Bài tập Mindmap " + "x" * 400, encoding="utf-8")
        (self.hw_path / "tieu_chi_danh_gia.md").write_text("# Tiêu chí " + "x" * 400, encoding="utf-8")

        # Create 17 valid subfolders
        self.valid_folders = []
        for i in range(1, 16):
            f_name = f"{i}_van_dung_co_ban_test_{i}"
            self.valid_folders.append(f_name)
            sub = self.hw_path / f_name
            sub.mkdir(parents=True, exist_ok=True)
            (sub / "de_bai_bai_tap.md").write_text("# Đề bài " + "x" * 300, encoding="utf-8")
            (sub / "de_bai.md").write_text("# Đề bài " + "x" * 300, encoding="utf-8")
            (sub / "tieu_chi_cham_diem_ai.md").write_text("# Tiêu chí " + "x" * 300, encoding="utf-8")
            (sub / "tieu_chi.md").write_text("# Tiêu chí " + "x" * 300, encoding="utf-8")

        f16 = "16_tong_hop_demo_giang_vien_tren_lop"
        self.valid_folders.append(f16)
        sub16 = self.hw_path / f16
        sub16.mkdir(parents=True, exist_ok=True)
        (sub16 / "de_bai_bai_tap.md").write_text("# Đề bài 16 " + "x" * 300, encoding="utf-8")
        (sub16 / "de_bai.md").write_text("# Đề bài 16 " + "x" * 300, encoding="utf-8")
        (sub16 / "tieu_chi_cham_diem_ai.md").write_text("# Tiêu chí 16 " + "x" * 300, encoding="utf-8")
        (sub16 / "tieu_chi.md").write_text("# Tiêu chí 16 " + "x" * 300, encoding="utf-8")

        f17 = "17_tong_hop_he_thong_kien_thuc_mindmap"
        self.valid_folders.append(f17)
        sub17 = self.hw_path / f17
        sub17.mkdir(parents=True, exist_ok=True)
        (sub17 / "de_bai_bai_tap.md").write_text("# Đề bài 17 " + "x" * 300, encoding="utf-8")
        (sub17 / "de_bai.md").write_text("# Đề bài 17 " + "x" * 300, encoding="utf-8")
        (sub17 / "tieu_chi_cham_diem_ai.md").write_text("# Tiêu chí 17 " + "x" * 300, encoding="utf-8")
        (sub17 / "tieu_chi.md").write_text("# Tiêu chí 17 " + "x" * 300, encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_cleanup_redundant_files_and_folders(self):
        """Test that redundant files and folders are purged automatically."""
        # Inject junk files
        junk_root = self.hw_path / "temp_scratch.tmp"
        junk_root.write_text("junk", encoding="utf-8")
        
        legacy_folder = self.hw_path / "bai_01"
        legacy_folder.mkdir()
        (legacy_folder / "temp.txt").write_text("old", encoding="utf-8")

        junk_subfolder = self.hw_path / "extra_unknown_folder"
        junk_subfolder.mkdir()

        # Inject tiny stub file in a valid folder
        tiny_stub = self.hw_path / self.valid_folders[0] / "stub.tmp"
        tiny_stub.write_text("short", encoding="utf-8")

        # Run cleanup
        res = cleanup_redundant_homework_assets(self.hw_path, valid_folder_names=self.valid_folders)
        self.assertTrue(len(res["deleted_files"]) >= 2)
        self.assertTrue(len(res["deleted_folders"]) >= 2)

        self.assertFalse(junk_root.exists())
        self.assertFalse(legacy_folder.exists())
        self.assertFalse(junk_subfolder.exists())
        self.assertFalse(tiny_stub.exists())

    def test_review_auto_cleanup_integration(self):
        """Test review_session_homework automatically fixes and passes 100/100."""
        # Add a stray file
        (self.hw_path / "stray_rubric.txt").write_text("stray", encoding="utf-8")

        review_res = review_session_homework(self.hw_path, auto_cleanup=True)
        self.assertEqual(review_res["status"], "PASSED")
        self.assertEqual(review_res["score"], 100)
        self.assertEqual(review_res["total_folders"], 17)
        self.assertEqual(review_res["total_root_files"], 18)

if __name__ == "__main__":
    unittest.main()
