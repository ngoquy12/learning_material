"""
tests/test_paths.py — Khoá hành vi của core/paths.py.

Trọng tâm là 2 lỗi thật mà module này sinh ra để sửa, chứ không phải kiểm tra
getter trả về chuỗi:

  1. `knowledge_store.db` từng được khai báo bằng 2 hằng số riêng ở 2 module
     (agents/knowledge_memory_agent.py và core/quality_evaluator.py) — hai kho
     tri thức tách đôi mà không có gì báo lỗi.
  2. Đường dẫn tương đối theo cwd — chạy pipeline từ thư mục khác là tạo ra một bộ
     DB rỗng mới, im lặng làm mất kho kinh nghiệm đã tích luỹ.
"""

import os
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

from core import paths


@pytest.fixture
def isolated_storage(tmp_path, monkeypatch):
    """Trỏ STORAGE_DIR sang thư mục tạm và xoá cache lru để thay đổi có hiệu lực."""
    monkeypatch.setenv("STORAGE_DIR", str(tmp_path / "storage"))
    paths.reset_path_cache()
    yield tmp_path / "storage"
    paths.reset_path_cache()


class TestStorageDirResolution:
    def test_storage_dir_duoc_tao_tu_dong(self, isolated_storage):
        result = paths.get_storage_dir()
        assert result.exists() and result.is_dir()
        assert result == isolated_storage.resolve()

    def test_duong_dan_tuong_doi_neo_vao_goc_du_an_khong_phai_cwd(self, tmp_path, monkeypatch):
        """
        Đây là điểm dễ hiểu sai nhất: đặt STORAGE_DIR=data mà lại neo theo cwd thì
        chính cái bug đang sửa sẽ quay lại qua đường cấu hình.
        """
        monkeypatch.setenv("STORAGE_DIR", "data_test_tmp")
        monkeypatch.chdir(tmp_path)  # cwd khác hẳn gốc dự án
        paths.reset_path_cache()
        try:
            result = paths.get_storage_dir()
            assert result == (paths.BASE_DIR / "data_test_tmp").resolve()
            assert not (tmp_path / "data_test_tmp").exists()
        finally:
            paths.reset_path_cache()
            leftover = paths.BASE_DIR / "data_test_tmp"
            if leftover.exists():
                leftover.rmdir()

    def test_duong_dan_tuyet_doi_duoc_ton_trong(self, tmp_path, monkeypatch):
        target = tmp_path / "abs_storage"
        monkeypatch.setenv("STORAGE_DIR", str(target))
        paths.reset_path_cache()
        try:
            assert paths.get_storage_dir() == target.resolve()
        finally:
            paths.reset_path_cache()


class TestSingleSourceOfTruth:
    def test_knowledge_db_chi_co_mot_duong_dan_duy_nhat(self, isolated_storage):
        """
        Hồi quy chính: knowledge_memory_agent và quality_evaluator PHẢI ghi vào cùng
        một file. Trước đây mỗi bên tự khai báo hằng số riêng nên chỉ cần một bên đổi
        chỗ là kho tri thức tách làm đôi trong im lặng.
        """
        from agents.knowledge_memory_agent import DB_PATH as memory_db

        canonical = paths.get_knowledge_db_path()
        assert Path(memory_db).name == canonical.name == paths.KNOWLEDGE_DB_NAME

    def test_ba_db_nam_chung_mot_thu_muc_va_khac_ten(self, isolated_storage):
        db_paths = [
            paths.get_state_db_path(),
            paths.get_cache_db_path(),
            paths.get_knowledge_db_path(),
        ]
        assert len({p.parent for p in db_paths}) == 1, "3 DB phải nằm chung một thư mục"
        assert len({p.name for p in db_paths}) == 3, "3 DB không được trùng tên file"


class TestLegacyMigration:
    def test_di_tru_file_cu_o_goc_repo_kem_sidecar_wal(self, isolated_storage):
        """File DB cũ ở gốc repo phải được chuyển sang storage/ cùng -wal và -shm."""
        legacy_name = "legacy_migration_probe.db"
        legacy = paths.BASE_DIR / legacy_name
        try:
            conn = sqlite3.connect(str(legacy))
            conn.execute("CREATE TABLE probe (id INTEGER)")
            conn.execute("INSERT INTO probe VALUES (42)")
            conn.commit()
            conn.close()
            Path(str(legacy) + "-wal").write_bytes(b"")

            target = paths.get_db_path(legacy_name)

            assert target.exists(), "File phải có mặt ở vị trí mới"
            assert not legacy.exists(), "File cũ ở gốc repo phải được dọn đi"
            assert Path(str(target) + "-wal").exists(), "Sidecar WAL phải đi cùng"

            conn = sqlite3.connect(str(target))
            assert conn.execute("SELECT id FROM probe").fetchone()[0] == 42
            conn.close()
        finally:
            for suffix in ("", "-wal", "-shm"):
                for base in (legacy, isolated_storage / legacy_name):
                    candidate = Path(str(base) + suffix)
                    if candidate.exists():
                        candidate.unlink()

    def test_khong_ghi_de_file_dang_dung_bang_ban_cu(self, isolated_storage):
        """
        Nếu cả bản mới lẫn bản cũ cùng tồn tại, bản đang dùng (trong storage/) phải
        được giữ nguyên — di trú tuyệt đối không được phá dữ liệu mới bằng dữ liệu cũ.
        """
        name = "conflict_probe.db"
        legacy = paths.BASE_DIR / name
        current = paths.get_storage_dir() / name
        try:
            legacy.write_text("BAN_CU", encoding="utf-8")
            current.write_text("BAN_DANG_DUNG", encoding="utf-8")

            result = paths.get_db_path(name)

            assert result.read_text(encoding="utf-8") == "BAN_DANG_DUNG"
            assert legacy.exists(), "Bản cũ được giữ lại để người dùng tự quyết định"
        finally:
            for f in (legacy, current):
                if f.exists():
                    f.unlink()


class TestNoDbLeakIntoRepoRoot:
    def test_import_module_khong_tao_db_o_goc_repo(self, tmp_path):
        """
        Chạy trong tiến trình con với STORAGE_DIR tạm: import các module có đụng DB
        không được để lại bất kỳ file .db nào ở gốc repo.
        """
        env = dict(os.environ, STORAGE_DIR=str(tmp_path / "storage"))
        code = (
            "import core.persistence, core.semantic_cache, agents.knowledge_memory_agent;"
            "from core.paths import get_storage_dir;"
            "print(get_storage_dir())"
        )
        before = {p.name for p in paths.BASE_DIR.glob("*.db")}

        result = subprocess.run(
            [sys.executable, "-c", code],
            cwd=str(paths.BASE_DIR),
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, result.stderr
        after = {p.name for p in paths.BASE_DIR.glob("*.db")}
        assert after == before, f"Có file .db mới rơi vào gốc repo: {after - before}"
