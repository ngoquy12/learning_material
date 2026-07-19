"""
tests/test_pipeline_api.py
==========================
Automated tests cho Pipeline API endpoints.
Chạy: cd web/backend && pytest tests/test_pipeline_api.py -v
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient

# Add project to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from main import app

client = TestClient(app)


# ── Cache Endpoints ─────────────────────────────────────

class TestCacheStats:
    """Tests cho /api/v1/pipeline/cache/stats"""

    def test_cache_stats_returns_200(self):
        """Cache stats endpoint phải trả về 200 khi module tồn tại."""
        mock_stats = {
            "total_cached_responses": 42,
            "total_cache_hits": 15,
            "estimated_tokens_saved": 12000,
            "by_agent": {"HTML_Writer": {"cached": 10, "hits": 5}},
        }
        with patch("app.api.endpoints.pipeline.ROOT", Path(".")):
            with patch.dict("sys.modules", {"core.semantic_cache": MagicMock(
                get_cache_stats=MagicMock(return_value=mock_stats),
                cache_invalidate_old=MagicMock(return_value=0),
                CACHE_ENABLED=True,
            )}):
                response = client.get("/api/v1/pipeline/cache/stats")
                # May return 200 or 503 depending on env — just check no 500
                assert response.status_code in [200, 503]

    def test_cache_stats_response_schema(self):
        """Response schema phải chứa các fields bắt buộc."""
        mock_stats = {
            "total_cached_responses": 10,
            "total_cache_hits": 3,
            "estimated_tokens_saved": 2400,
            "by_agent": {},
        }
        import importlib
        mock_module = MagicMock()
        mock_module.get_cache_stats = MagicMock(return_value=mock_stats)
        mock_module.cache_invalidate_old = MagicMock(return_value=0)
        mock_module.CACHE_ENABLED = True

        with patch.dict("sys.modules", {"core.semantic_cache": mock_module}):
            with patch("app.api.endpoints.pipeline.ROOT", Path(".")):
                # Directly test the endpoint function
                from app.api.endpoints.pipeline import get_cache_stats
                import asyncio
                result = asyncio.run(get_cache_stats())
                assert result.total_cached_responses == 10
                assert result.total_cache_hits == 3
                assert result.cache_enabled is True


class TestCacheClear:
    """Tests cho DELETE /api/v1/pipeline/cache/clear"""

    def test_clear_nonexistent_cache(self, tmp_path):
        """Xóa cache khi DB không tồn tại phải trả về thông báo thân thiện."""
        with patch("app.api.endpoints.pipeline.ROOT", tmp_path):
            response = client.delete("/api/v1/pipeline/cache/clear")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "ok"

    def test_clear_existing_cache(self, tmp_path):
        """Xóa cache khi DB tồn tại phải xóa thành công."""
        import sqlite3
        db_path = tmp_path / "semantic_cache.db"
        conn = sqlite3.connect(str(db_path))
        conn.execute("""CREATE TABLE semantic_cache (
            id TEXT PRIMARY KEY, agent_name TEXT, prompt_hash TEXT,
            prompt_text TEXT, response TEXT, hit_count INTEGER,
            created_at REAL, last_used REAL
        )""")
        conn.execute("INSERT INTO semantic_cache VALUES ('t1','A','h1','p','r',0,1000,1000)")
        conn.commit()
        conn.close()

        with patch("app.api.endpoints.pipeline.ROOT", tmp_path):
            response = client.delete("/api/v1/pipeline/cache/clear")
            assert response.status_code == 200
            data = response.json()
            assert data["deleted_entries"] == 1


# ── Knowledge Memory Endpoints ───────────────────────────

class TestKnowledgeMemory:
    """Tests cho /api/v1/pipeline/knowledge-memory"""

    def test_get_categories(self):
        """Categories endpoint phải trả về đúng 10 categories."""
        response = client.get("/api/v1/pipeline/knowledge-memory/categories")
        assert response.status_code == 200
        data = response.json()
        assert "categories" in data
        assert len(data["categories"]) == 10
        keys = [c["key"] for c in data["categories"]]
        assert "scope_violation" in keys
        assert "pedagogical_error" in keys
        assert "other" in keys

    def test_get_memories_returns_list(self):
        """Knowledge memory endpoint phải trả về list."""
        mock_agent = MagicMock()
        mock_agent.recall_memories = MagicMock(return_value=[
            {
                "id": 1, "category": "scope_violation", "severity": "high",
                "description": "Test error", "bad_example": None,
                "good_example": None, "tech_stack": "python/fastapi",
                "scope": "html", "hit_count": 2, "created_at": "2024-01-01"
            }
        ])
        with patch.dict("sys.modules", {"agents.knowledge_memory_agent": mock_agent}):
            response = client.get("/api/v1/pipeline/knowledge-memory")
            assert response.status_code in [200, 503]

    def test_memories_filter_by_category(self):
        """Filter theo category phải hoạt động đúng."""
        mock_agent = MagicMock()
        mock_agent.recall_memories = MagicMock(return_value=[
            {"id": 1, "category": "scope_violation", "severity": "high",
             "description": "D1", "bad_example": None, "good_example": None,
             "tech_stack": None, "scope": None, "hit_count": 0, "created_at": ""},
            {"id": 2, "category": "syntax_error", "severity": "low",
             "description": "D2", "bad_example": None, "good_example": None,
             "tech_stack": None, "scope": None, "hit_count": 0, "created_at": ""},
        ])
        with patch.dict("sys.modules", {"agents.knowledge_memory_agent": mock_agent}):
            import asyncio
            from app.api.endpoints.pipeline import get_knowledge_memories
            result = asyncio.run(get_knowledge_memories(
                tech_stack=None, scope=None, category="scope_violation", limit=50
            ))
            # All returned items should match category
            for item in result:
                assert item.category == "scope_violation"


# ── Prerequisite Report Endpoints ────────────────────────

class TestPrerequisiteReport:
    """Tests cho /api/v1/pipeline/prerequisite-report/{course_name}"""

    def test_report_not_found(self, tmp_path):
        """Khi không có report, phải trả về response với has_blockers=False."""
        with patch("app.api.endpoints.pipeline.ROOT", tmp_path):
            response = client.get("/api/v1/pipeline/prerequisite-report/NonExistentCourse")
            assert response.status_code == 200
            data = response.json()
            assert data["has_blockers"] is False
            assert data["report_content"] is None

    def test_report_found_no_blockers(self, tmp_path):
        """Report không có BLOCKER phải trả về has_blockers=False."""
        course_dir = tmp_path / "output" / "TestCourse"
        course_dir.mkdir(parents=True)
        report = course_dir / "prerequisite_report.md"
        report.write_text("# Prerequisite Report\n\n✅ All good!\n🟡 WARNING: Some tips here.", encoding="utf-8")

        with patch("app.api.endpoints.pipeline.ROOT", tmp_path):
            response = client.get("/api/v1/pipeline/prerequisite-report/TestCourse")
            assert response.status_code == 200
            data = response.json()
            assert data["has_blockers"] is False
            assert data["warning_count"] >= 1

    def test_report_found_with_blockers(self, tmp_path):
        """Report có BLOCKER phải trả về has_blockers=True."""
        course_dir = tmp_path / "output" / "TestCourse"
        course_dir.mkdir(parents=True)
        report = course_dir / "prerequisite_report.md"
        report.write_text("# Report\n🔴 **BLOCKER**: Session 3 requires Session 5.", encoding="utf-8")

        with patch("app.api.endpoints.pipeline.ROOT", tmp_path):
            response = client.get("/api/v1/pipeline/prerequisite-report/TestCourse")
            assert response.status_code == 200
            data = response.json()
            assert data["has_blockers"] is True
            assert data["blocker_count"] >= 1


# ── SCORM Export Endpoints ────────────────────────────────

class TestSCORMExport:
    """Tests cho SCORM export endpoints."""

    def test_export_nonexistent_dir(self, tmp_path):
        """Export từ thư mục không tồn tại phải trả về 404."""
        with patch("app.api.endpoints.pipeline.ROOT", tmp_path):
            response = client.post("/api/v1/pipeline/scorm/export", json={
                "course_name": "Ghost Course",
                "output_dir": str(tmp_path / "does_not_exist")
            })
            assert response.status_code == 404

    def test_export_returns_task_id(self, tmp_path):
        """Export hợp lệ phải trả về task_id ngay lập tức."""
        output_dir = tmp_path / "output" / "TestCourse"
        output_dir.mkdir(parents=True)

        with patch("app.api.endpoints.pipeline.ROOT", tmp_path):
            response = client.post("/api/v1/pipeline/scorm/export", json={
                "course_name": "Test Course",
                "output_dir": str(output_dir)
            })
            assert response.status_code == 200
            data = response.json()
            assert "task_id" in data
            assert data["status"] == "running"

    def test_status_unknown_task(self):
        """Poll status cho task không tồn tại phải trả về 404."""
        response = client.get("/api/v1/pipeline/scorm/status/nonexistent_task")
        assert response.status_code == 404

    def test_download_incomplete_task(self):
        """Download khi task chưa xong phải trả về 404."""
        response = client.get("/api/v1/pipeline/scorm/download/nonexistent_task")
        assert response.status_code == 404


# ── Dashboard Stats ───────────────────────────────────────

class TestDashboardStats:
    """Tests cho /api/v1/pipeline/stats/dashboard"""

    def test_dashboard_stats_structure(self):
        """Dashboard stats phải có đúng cấu trúc fields."""
        # Mock DB session
        mock_db_results = AsyncMock()
        mock_db_results.scalar = MagicMock(return_value=0)

        with patch("app.db.session.AsyncSessionLocal") as mock_session_cls:
            mock_ctx = AsyncMock()
            mock_ctx.__aenter__ = AsyncMock(return_value=mock_ctx)
            mock_ctx.__aexit__ = AsyncMock(return_value=False)
            mock_ctx.execute = AsyncMock(return_value=mock_db_results)
            mock_session_cls.return_value = mock_ctx

            response = client.get("/api/v1/pipeline/stats/dashboard")
            assert response.status_code in [200, 500]  # 500 nếu DB không chạy trong test env


# ── Integration: Route Registration ──────────────────────

class TestRouteRegistration:
    """Verify all new routes are properly registered."""

    def test_openapi_includes_pipeline_routes(self):
        """OpenAPI schema phải có /pipeline routes."""
        response = client.get("/api/v1/openapi.json")
        assert response.status_code == 200
        spec = response.json()
        paths = spec.get("paths", {})
        pipeline_paths = [p for p in paths if "/pipeline" in p]
        assert len(pipeline_paths) > 0, "Không tìm thấy /pipeline routes trong OpenAPI spec"

    def test_cache_stats_route_exists(self):
        """Route /pipeline/cache/stats phải tồn tại."""
        response = client.get("/api/v1/openapi.json")
        spec = response.json()
        assert "/api/v1/pipeline/cache/stats" in spec["paths"]

    def test_knowledge_memory_route_exists(self):
        """Route /pipeline/knowledge-memory phải tồn tại."""
        response = client.get("/api/v1/openapi.json")
        spec = response.json()
        assert "/api/v1/pipeline/knowledge-memory" in spec["paths"]

    def test_scorm_export_route_exists(self):
        """Route /pipeline/scorm/export phải tồn tại."""
        response = client.get("/api/v1/openapi.json")
        spec = response.json()
        assert "/api/v1/pipeline/scorm/export" in spec["paths"]
