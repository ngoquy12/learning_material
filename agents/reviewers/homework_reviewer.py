"""
agents/reviewers/homework_reviewer.py
Reviewer Agent for Session Homework Suite.
Audits generated homework directory for:
- Completeness: 15 tiered Bloom exercises + 1 in-class synthesis + 1 mindmap exercise (17 folders total).
- Descriptive naming convention: {idx}_{level_slug}_{title_slug}, 16_tong_hop_demo_giang_vien_tren_lop, 17_tong_hop_he_thong_kien_thuc_mindmap.
- File integrity: de_bai_bai_tap.md, tieu_chi_cham_diem_ai.md in each subfolder.
- Root files: ONLY tieu_chi_danh_gia.md is kept — legacy per-exercise root files (bai_tap_1.md..
  bai_tap_15.md, bai_tap_tong_hop.md, bai_tap_mindmap.md) from an older naming convention are
  treated as stray/redundant and deleted (see ALLOWED_ROOT_FILES).
- Quality: Zero text emojis, no empty stub files.
"""

import os
import re
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional, Union, Set

ALLOWED_ROOT_FILES: Set[str] = {
    "tieu_chi_danh_gia.md"
}

ALLOWED_SUBFOLDER_FILES: Set[str] = {
    "de_bai_bai_tap.md",
    "tieu_chi_cham_diem_ai.md"
}

def cleanup_redundant_homework_assets(
    homework_dir: Union[str, Path],
    valid_folder_names: Optional[List[str]] = None
) -> Dict[str, List[str]]:
    """
    Rà soát và xóa sạch 100% các tệp tin và thư mục rác/dư thừa trong thư mục Bài tập:
    - Tại thư mục gốc: Chỉ giữ duy nhất file tổng hợp tieu_chi_danh_gia.md. Xóa sạch mọi file bài tập lẻ bai_tap_*.md.
    - Tại các thư mục con: Chỉ giữ đúng 17 thư mục bài tập chuẩn (1..15, 16, 17). Xóa mọi thư mục cũ hoặc thư mục rác.
    - Bên trong từng thư mục con: Chỉ giữ đúng 2 files chuẩn (de_bai_bai_tap.md, tieu_chi_cham_diem_ai.md). Xóa file alias trùng lặp (de_bai.md, tieu_chi.md), file rỗng/tạm.
    """
    hw_path = Path(homework_dir)
    if not hw_path.exists() or not hw_path.is_dir():
        return {"deleted_files": [], "deleted_folders": []}

    deleted_files = []
    deleted_folders = []

    # 1. Dọn dẹp các file rác ở thư mục gốc Bài tập/ (xóa sạch các file bai_tap_*.md thừa)
    for file_item in list(hw_path.iterdir()):
        if file_item.is_file():
            if file_item.name not in ALLOWED_ROOT_FILES or file_item.stat().st_size < 200:
                try:
                    file_item.unlink()
                    deleted_files.append(f"Root: {file_item.name}")
                except Exception:
                    pass

    # 2. Dọn dẹp các thư mục con rác/dư thừa
    all_subdirs = [d for d in hw_path.iterdir() if d.is_dir() and d.name != "images" and not d.name.startswith(".")]
    
    # Xác định các thư mục hợp lệ (1..17)
    valid_folders_set = set(valid_folder_names) if valid_folder_names else set()
    
    # Nếu không truyền valid_folder_names, tìm 17 thư mục đánh số chuẩn mới nhất
    numbered_map: Dict[int, Path] = {}
    for d in all_subdirs:
        m = re.match(r"^(\d+)_", d.name)
        if m:
            num = int(m.group(1))
            if 1 <= num <= 17:
                # Nếu có trùng số (do đổi tên), giữ thư mục có nội dung mới hơn
                if num not in numbered_map or d.stat().st_mtime > numbered_map[num].stat().st_mtime:
                    if num in numbered_map and numbered_map[num] != d:
                        try:
                            shutil.rmtree(numbered_map[num])
                            deleted_folders.append(numbered_map[num].name)
                        except Exception:
                            pass
                    numbered_map[num] = d
            else:
                # Số ngoài 1..17 -> Xóa
                try:
                    shutil.rmtree(d)
                    deleted_folders.append(d.name)
                except Exception:
                    pass
        elif re.match(r"^bai_\d+$", d.name):
            # Thư mục dạng cũ bai_01..bai_15 -> Xóa
            try:
                shutil.rmtree(d)
                deleted_folders.append(d.name)
            except Exception:
                pass
        elif valid_folders_set and d.name not in valid_folders_set:
            # Thư mục lạ không nằm trong danh sách -> Xóa
            try:
                shutil.rmtree(d)
                deleted_folders.append(d.name)
            except Exception:
                pass

    # 3. Dọn dẹp bên trong từng thư mục con hợp lệ (chỉ giữ de_bai_bai_tap.md và tieu_chi_cham_diem_ai.md)
    active_subdirs = [d for d in hw_path.iterdir() if d.is_dir() and d.name != "images" and not d.name.startswith(".")]
    for sub in active_subdirs:
        for sub_file in list(sub.iterdir()):
            if sub_file.is_file():
                if sub_file.name not in ALLOWED_SUBFOLDER_FILES or sub_file.stat().st_size < 200:
                    try:
                        sub_file.unlink()
                        deleted_files.append(f"{sub.name}/{sub_file.name}")
                    except Exception:
                        pass

    if deleted_files or deleted_folders:
        print(f"  🧹 [Auto-Cleanup] Đã dọn dẹp {len(deleted_files)} file rác và {len(deleted_folders)} thư mục dư thừa.")

    return {
        "deleted_files": deleted_files,
        "deleted_folders": deleted_folders
    }

def review_session_homework(
    homework_dir: Union[str, Path],
    expected_domain: Optional[str] = None,
    auto_cleanup: bool = True
) -> Dict[str, Any]:
    """
    Audits the generated homework directory for completeness, structure, domain alignment, and quality.
    Tự động rà soát và xóa sạch các file/thư mục rác nếu auto_cleanup=True.
    """
    hw_path = Path(homework_dir)
    if not hw_path.exists() or not hw_path.is_dir():
        return {
            "status": "REJECTED",
            "score": 0,
            "feedback": f"Thư mục bài tập không tồn tại: {homework_dir}",
            "errors": [f"Thư mục không tồn tại: {homework_dir}"],
            "deleted_assets": {"deleted_files": [], "deleted_folders": []}
        }

    # 1. Tự động kích hoạt dọn dẹp file rác nếu auto_cleanup=True
    deleted_info = {"deleted_files": [], "deleted_folders": []}
    if auto_cleanup:
        deleted_info = cleanup_redundant_homework_assets(hw_path)

    errors = []
    warnings = []

    # 2. Check root files: Chỉ duy nhất tieu_chi_danh_gia.md ở thư mục gốc
    root_files = {f.name: f for f in hw_path.iterdir() if f.is_file()}
    if "tieu_chi_danh_gia.md" not in root_files:
        errors.append("Thiếu file Bảng tiêu chí đánh giá tổng hợp ở thư mục gốc: tieu_chi_danh_gia.md")
    elif root_files["tieu_chi_danh_gia.md"].stat().st_size < 300:
        errors.append("File tieu_chi_danh_gia.md rỗng hoặc quá ngắn (<300 bytes)")

    # Kiểm tra xem còn file thừa nào ở root không (không được để file lẻ bai_tap_*.md ở root)
    surplus_root_files = [f for f in root_files.keys() if f not in ALLOWED_ROOT_FILES]
    if surplus_root_files:
        errors.append(f"Phát hiện file thừa không theo cấu trúc ở thư mục gốc (các bài tập phải nằm trong thư mục con tương ứng): {surplus_root_files}")

    # 3. Check subfolders (chính xác 17 subfolders)
    subdirs = [d for d in hw_path.iterdir() if d.is_dir() and d.name != "images" and not d.name.startswith(".")]
    
    # Check for legacy non-descriptive folders (like bai_01)
    legacy_folders = [d.name for d in subdirs if re.match(r"^bai_\d+$", d.name)]
    if legacy_folders:
        errors.append(f"Phát hiện thư mục đặt tên cũ chưa có mô tả: {legacy_folders}")

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
            # Check de_bai_bai_tap.md
            has_de_bai = (folder / "de_bai_bai_tap.md").exists()
            if not has_de_bai:
                errors.append(f"Thư mục {folder.name} thiếu file đề bài chuẩn (de_bai_bai_tap.md)")
            # Check tieu_chi_cham_diem_ai.md
            has_tieu_chi = (folder / "tieu_chi_cham_diem_ai.md").exists()
            if not has_tieu_chi:
                errors.append(f"Thư mục {folder.name} thiếu file tiêu chí chấm chuẩn (tieu_chi_cham_diem_ai.md)")

    # Check folder 16 (in-class synthesis)
    if 16 not in numbered_folders:
        errors.append("Thiếu thư mục Bài tập tổng hợp trên lớp (16_tong_hop_demo_giang_vien_tren_lop)")
    else:
        folder_16 = numbered_folders[16]
        if not (folder_16 / "de_bai_bai_tap.md").exists():
            errors.append("Thư mục 16_tong_hop_demo_giang_vien_tren_lop thiếu file de_bai_bai_tap.md")
        if not (folder_16 / "tieu_chi_cham_diem_ai.md").exists():
            errors.append("Thư mục 16_tong_hop_demo_giang_vien_tren_lop thiếu file tieu_chi_cham_diem_ai.md")

    # Check folder 17 (mindmap)
    if 17 not in numbered_folders:
        errors.append("Thiếu thư mục Bài tập sơ đồ tư duy mindmap (17_tong_hop_he_thong_kien_thuc_mindmap)")
    else:
        folder_17 = numbered_folders[17]
        if not (folder_17 / "de_bai_bai_tap.md").exists():
            errors.append("Thư mục 17_tong_hop_he_thong_kien_thuc_mindmap thiếu file de_bai_bai_tap.md")
        if not (folder_17 / "tieu_chi_cham_diem_ai.md").exists():
            errors.append("Thư mục 17_tong_hop_he_thong_kien_thuc_mindmap thiếu file tieu_chi_cham_diem_ai.md")

    # 4. Check for emoji or bad content
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
        "deleted_assets": deleted_info,
        "errors": errors,
        "warnings": warnings,
        "feedback": "Bộ bài tập đạt chuẩn 100% Rikkei Education." if status == "PASSED" else f"Phát hiện {len(errors)} lỗi cần khắc phục."
    }

class HomeworkReviewerAgent:
    """Wrapper class for Homework Reviewer Agent."""
    def __init__(self):
        pass

    def review(self, homework_dir: Union[str, Path], auto_cleanup: bool = True) -> Dict[str, Any]:
        return review_session_homework(homework_dir, auto_cleanup=auto_cleanup)

__all__ = [
    "review_session_homework",
    "cleanup_redundant_homework_assets",
    "HomeworkReviewerAgent",
    "ALLOWED_ROOT_FILES",
    "ALLOWED_SUBFOLDER_FILES"
]
