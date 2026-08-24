"""
core/paths.py — Nguồn DUY NHẤT quyết định vị trí mọi file dữ liệu runtime (SQLite).

Bối cảnh: trước module này, 4 nơi tự đặt đường dẫn DB độc lập với nhau, và phần lớn
là đường dẫn TƯƠNG ĐỐI so với thư mục làm việc hiện tại (cwd):

    core/persistence.py               STORAGE_DIR = "storage"          -> <cwd>/storage/state_store_v2.db
    core/semantic_cache.py            Path("semantic_cache.db")        -> <cwd>/semantic_cache.db
    agents/knowledge_memory_agent.py  Path("knowledge_store.db")       -> <cwd>/knowledge_store.db
    core/quality_evaluator.py         db_path = "knowledge_store.db"   -> <cwd>/knowledge_store.db

Hai hệ quả thật, không phải giả định:

  1. `knowledge_store.db` được mở từ HAI module bằng HAI hằng số riêng biệt
     (knowledge_memory_agent ghi bảng `agent_memory`, quality_evaluator ghi bảng
     `lesson_quality_metrics`). Sửa đường dẫn ở một nơi là hai module lặng lẽ ghi
     vào hai file khác nhau mà không có gì báo lỗi.

  2. Đường dẫn tương đối theo cwd nghĩa là chạy pipeline từ thư mục khác — hoặc test
     chạy với cwd tạm — sẽ tạo ra một bộ DB mới, RỖNG, ở nơi không ai ngờ tới. Kho
     tri thức kinh nghiệm (lessons-learned) và cache ngữ nghĩa im lặng mất sạch,
     biểu hiện ra ngoài chỉ là "tự nhiên chạy chậm hơn và quên hết kinh nghiệm cũ".

Module này neo mọi đường dẫn vào thư mục gốc dự án (hoặc biến môi trường
`STORAGE_DIR`), gom hết về một thư mục `storage/`, và tự di chuyển các file DB cũ
còn nằm ở gốc repo sang vị trí mới để không mất dữ liệu đã tích lũy.
"""

from __future__ import annotations

import os
import shutil
from functools import lru_cache
from pathlib import Path
from typing import Union

# Thư mục gốc dự án — neo tuyệt đối, KHÔNG phụ thuộc cwd.
BASE_DIR = Path(__file__).resolve().parent.parent

# Các sidecar mà SQLite sinh ra ở chế độ WAL. Di chuyển file .db mà bỏ quên 2 file
# này sẽ khiến SQLite thấy WAL mồ côi và có thể mất các giao dịch chưa checkpoint.
_SQLITE_SIDECARS = ("-wal", "-shm")

# Tên logic -> tên file. Đặt tên qua hằng số để không còn chuỗi "knowledge_store.db"
# rải rác trong code: đổi tên file chỉ sửa đúng một dòng ở đây.
STATE_DB_NAME = "state_store_v2.db"
CACHE_DB_NAME = "semantic_cache.db"
KNOWLEDGE_DB_NAME = "knowledge_store.db"


def _safe_print(message: str) -> None:
    """
    In thông báo mà không bao giờ làm chết tiến trình vì lỗi encoding console.

    Console mặc định trên Windows là cp1252, không mã hoá được tiếng Việt có dấu.
    core/llm.py có gọi sys.stdout.reconfigure(encoding="utf-8") nhưng module này
    được import SỚM HƠN trong nhiều đường chạy (và trong test thì llm không hề được
    import), nên không thể dựa vào đó. Một dòng log vỡ không được phép làm hỏng
    thao tác di trú dữ liệu mà nó đang thông báo.
    """
    try:
        print(message)
    except UnicodeEncodeError:
        print(message.encode("ascii", "replace").decode("ascii"))


@lru_cache(maxsize=1)
def get_storage_dir() -> Path:
    """
    Trả về thư mục chứa toàn bộ dữ liệu runtime, đã đảm bảo tồn tại.

    Thứ tự ưu tiên:
      1. Biến môi trường `STORAGE_DIR` (cho phép test và container trỏ đi nơi khác).
      2. `<gốc dự án>/storage`.

    Đường dẫn tương đối trong `STORAGE_DIR` được hiểu là tương đối so với gốc dự án,
    KHÔNG phải cwd — để đặt biến môi trường này không tái tạo lại đúng cái bug mà
    module đang sửa.
    """
    raw = os.getenv("STORAGE_DIR", "").strip()
    if raw:
        candidate = Path(raw)
        storage = candidate if candidate.is_absolute() else (BASE_DIR / candidate)
    else:
        storage = BASE_DIR / "storage"

    storage.mkdir(parents=True, exist_ok=True)
    return storage.resolve()


def _migrate_legacy_db(file_name: str, target: Path) -> None:
    """
    Chuyển file DB cũ còn nằm ở gốc repo sang `storage/`, kèm các sidecar WAL.

    Chỉ chạy khi đích CHƯA tồn tại: nếu cả hai cùng tồn tại thì file ở vị trí mới là
    bản đang dùng, và ta tuyệt đối không ghi đè nó bằng bản cũ ở gốc repo.
    """
    legacy = BASE_DIR / file_name
    if target.exists() or not legacy.exists() or legacy.resolve() == target.resolve():
        return

    try:
        shutil.move(str(legacy), str(target))
        for suffix in _SQLITE_SIDECARS:
            legacy_sidecar = Path(str(legacy) + suffix)
            if legacy_sidecar.exists():
                shutil.move(str(legacy_sidecar), str(target) + suffix)
        _safe_print(f"  [Paths] Đã chuyển kho dữ liệu cũ '{file_name}' về {target}")
    except Exception as e:
        # Không chặn tiến trình: cùng lắm là hệ thống khởi tạo một DB rỗng ở vị trí
        # mới. Nhưng phải in ra, vì im lặng ở đây chính là kịch bản mất kho tri thức.
        _safe_print(f"  [Paths Warning] Không di chuyển được '{file_name}' sang {target}: {e}")


def get_db_path(file_name: str) -> Path:
    """
    Trả về đường dẫn tuyệt đối tới một file SQLite trong kho dữ liệu runtime.

    Tự động di trú file cũ ở gốc repo (nếu có) trước khi trả về, nên mọi caller chỉ
    cần gọi hàm này là chắc chắn trỏ tới đúng một file duy nhất trong toàn hệ thống.
    """
    target = get_storage_dir() / file_name
    _migrate_legacy_db(file_name, target)
    return target


def get_state_db_path() -> Path:
    """DB checkpoint trạng thái pipeline (core/persistence.py)."""
    return get_db_path(STATE_DB_NAME)


def get_cache_db_path() -> Path:
    """DB cache ngữ nghĩa của LLM (core/semantic_cache.py)."""
    return get_db_path(CACHE_DB_NAME)


def get_knowledge_db_path() -> Path:
    """
    DB kho tri thức dùng chung: bảng `agent_memory` (kinh nghiệm rút ra từ các lần
    sinh trước) và bảng `lesson_quality_metrics` (điểm PQM từng bài).

    Cả agents/knowledge_memory_agent.py lẫn core/quality_evaluator.py PHẢI đi qua
    hàm này thay vì tự khai báo hằng số riêng.
    """
    return get_db_path(KNOWLEDGE_DB_NAME)


def reset_path_cache() -> None:
    """Xoá cache thư mục lưu trữ — dùng cho test khi đổi `STORAGE_DIR` giữa chừng."""
    get_storage_dir.cache_clear()


__all__ = [
    "BASE_DIR",
    "STATE_DB_NAME",
    "CACHE_DB_NAME",
    "KNOWLEDGE_DB_NAME",
    "get_storage_dir",
    "get_db_path",
    "get_state_db_path",
    "get_cache_db_path",
    "get_knowledge_db_path",
    "reset_path_cache",
]
