"""
agents/reviewers/homework_reviewer.py
Reviewer Agent for Session Homework Suite.
Audits generated homework directory for:
- Completeness: 15 tiered Bloom exercises + 1 in-class synthesis + 1 mindmap exercise (17 folders total).
- Descriptive naming convention: {idx}_{level_slug}_{title_slug}, 16_tong_hop_demo_giang_vien_tren_lop, 17_tong_hop_he_thong_kien_thuc_mindmap.
- File integrity: de_bai_bai_tap.md, tieu_chi_cham_diem_ai.md in each subfolder.
- Root files: bai_tap_1.md to bai_tap_15.md, bai_tap_tong_hop.md, bai_tap_mindmap.md, tieu_chi_danh_gia.md.
- Quality: Zero text emojis, no empty stub files.
"""

import os
import re
from pathlib import Path
from typing import Dict, Any, List, Union

def review_session_homework(homework_dir: Union[str, Path]) -> Dict[str, Any]:
    """
    Audits the generated homework directory for completeness, structure, and quality.
    """
    hw_path = Path(homework_dir)
    if not hw_path.exists() or not hw_path.is_dir():
        return {
            "status": "REJECTED",
            "score": 0,
            "feedback": f"Thư mục bài tập không tồn tại: {homework_dir}",
            "errors": [f"Thư mục không tồn tại: {homework_dir}"]
        }

    errors = []
    warnings = []

    # 1. Check root files
    root_files = {f.name: f for f in hw_path.iterdir() if f.is_file()}
    for i in range(1, 16):
        expected_root_file = f"bai_tap_{i}.md"
        if expected_root_file not in root_files:
            errors.append(f"Thiếu file bài tập ở thư mục gốc: {expected_root_file}")
        elif root_files[expected_root_file].stat().st_size < 300:
            errors.append(f"File bài tập rỗng hoặc quá ngắn (<300 bytes): {expected_root_file}")

    if "bai_tap_tong_hop.md" not in root_files:
        errors.append("Thiếu file Bài tập tổng hợp trên lớp: bai_tap_tong_hop.md")
    elif root_files["bai_tap_tong_hop.md"].stat().st_size < 300:
        errors.append("File bai_tap_tong_hop.md rỗng hoặc quá ngắn")

    if "bai_tap_mindmap.md" not in root_files:
        errors.append("Thiếu file Bài tập sơ đồ tư duy mindmap: bai_tap_mindmap.md")
    elif root_files["bai_tap_mindmap.md"].stat().st_size < 300:
        errors.append("File bai_tap_mindmap.md rỗng hoặc quá ngắn")

    if "tieu_chi_danh_gia.md" not in root_files:
        errors.append("Thiếu file Bảng tiêu chí đánh giá tổng hợp: tieu_chi_danh_gia.md")

    # 2. Check subfolders (expecting 17 subfolders)
    subdirs = [d for d in hw_path.iterdir() if d.is_dir() and d.name != "images" and not d.name.startswith(".")]
    
    # Check for legacy non-descriptive folders (like bai_01)
    legacy_folders = [d.name for d in subdirs if re.match(r"^bai_\d+$", d.name)]
    if legacy_folders:
        warnings.append(f"Phát hiện thư mục đặt tên cũ chưa có mô tả: {legacy_folders}")

    # Check for 15 numbered tiered folders
    numbered_folders = {}
    for d in subdirs:
        m = re.match(r"^(\d+)_", d.name)
        if m:
            num = int(m.group(1))
            numbered_folders[num] = d

    for i in range(1, 16):
        if i not in numbered_folders:
            errors.append(f"Thiếu thư mục bài tập số {i} theo chuẩn định danh (ví dụ: {i}_van_dung_...)")
        else:
            folder = numbered_folders[i]
            # Check de_bai
            has_de_bai = (folder / "de_bai_bai_tap.md").exists() or (folder / "de_bai.md").exists()
            if not has_de_bai:
                errors.append(f"Thư mục {folder.name} thiếu file đề bài (de_bai_bai_tap.md hoặc de_bai.md)")
            # Check tieu_chi
            has_tieu_chi = (folder / "tieu_chi_cham_diem_ai.md").exists() or (folder / "tieu_chi.md").exists()
            if not has_tieu_chi:
                errors.append(f"Thư mục {folder.name} thiếu file tiêu chí chấm (tieu_chi_cham_diem_ai.md hoặc tieu_chi.md)")

    # Check folder 16 (in-class synthesis)
    if 16 not in numbered_folders:
        warnings.append("Khuyến nghị có thư mục riêng cho Bài tập tổng hợp trên lớp (16_tong_hop_demo_giang_vien_tren_lop)")

    # Check folder 17 (mindmap)
    if 17 not in numbered_folders:
        warnings.append("Khuyến nghị có thư mục riêng cho Bài tập sơ đồ tư duy mindmap (17_tong_hop_he_thong_kien_thuc_mindmap)")

    # 3. Check for emoji or bad content
    for f in hw_path.glob("**/*.md"):
        try:
            content = f.read_text(encoding="utf-8")
            emojis = re.findall(r'[\U00010000-\U0010ffff\u2600-\u26ff\u2700-\u27bf]', content)
            if emojis:
                warnings.append(f"Phát hiện emoji trong file {f.relative_to(hw_path)}: {set(emojis)}")
        except Exception:
            pass

    status = "PASSED" if not errors else "REJECTED"
    score = 100 if not errors and not warnings else (85 if not errors else max(0, 70 - len(errors) * 10))

    return {
        "status": status,
        "score": score,
        "total_folders": len(subdirs),
        "total_root_files": len(root_files),
        "errors": errors,
        "warnings": warnings,
        "feedback": "Bộ bài tập đạt chuẩn 100% Rikkei Education." if status == "PASSED" else f"Phát hiện {len(errors)} lỗi cần khắc phục."
    }

class HomeworkReviewerAgent:
    """Wrapper class for Homework Reviewer Agent."""
    def __init__(self):
        pass

    def review(self, homework_dir: Union[str, Path]) -> Dict[str, Any]:
        return review_session_homework(homework_dir)

__all__ = [
    "review_session_homework",
    "HomeworkReviewerAgent"
]
