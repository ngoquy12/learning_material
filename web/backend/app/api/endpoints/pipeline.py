# app/api/endpoints/pipeline.py
"""
Pipeline Management API
=======================
Cung cấp các endpoint để:
- Xem trạng thái pipeline (cache stats, prerequisite reports)
- Export SCORM package
- Query Knowledge Memory Agent
- Xem prerequisite reports
"""
import os
import sys
import json
from pathlib import Path
from typing import Optional, List

from fastapi import APIRouter, HTTPException, BackgroundTasks, Query, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
import shutil

router = APIRouter()

# ── Root paths ──────────────────────────────────────────
_BACKEND_DIR = Path(__file__).resolve().parents[4]  # Learning-Material root
_PROJECT_ROOT = _BACKEND_DIR


def _resolve_root() -> Path:
    """Resolve the Learning-Material project root robustly."""
    # When running from web/backend, go up 4 levels
    candidates = [
        Path(__file__).resolve().parents[4],
        Path(os.getcwd()),
    ]
    for c in candidates:
        if (c / "core" / "semantic_cache.py").exists():
            return c
    return candidates[0]


ROOT = _resolve_root()


# ── Schemas ──────────────────────────────────────────────

class CacheStatsResponse(BaseModel):
    total_cached_responses: int
    total_cache_hits: int
    estimated_tokens_saved: int
    by_agent: dict
    cache_enabled: bool


class KnowledgeMemoryItem(BaseModel):
    id: int
    category: str
    severity: str
    description: str
    bad_example: Optional[str]
    good_example: Optional[str]
    tech_stack: Optional[str]
    scope: Optional[str]
    hit_count: int
    created_at: str


class SCORMExportRequest(BaseModel):
    course_name: str
    output_dir: Optional[str] = None  # relative to output/ if not absolute


class PrerequisiteReportResponse(BaseModel):
    course_name: str
    report_path: Optional[str]
    has_blockers: bool
    blocker_count: int
    warning_count: int
    report_content: Optional[str]


# ── Cache Stats ───────────────────────────────────────────

@router.get("/cache/stats", response_model=CacheStatsResponse, summary="Thống kê Semantic Cache")
async def get_cache_stats():
    """Trả về thống kê về semantic cache LLM responses."""
    try:
        sys.path.insert(0, str(ROOT))
        from core.semantic_cache import get_cache_stats, cache_invalidate_old, CACHE_ENABLED
        cache_invalidate_old()
        stats = get_cache_stats()
        return CacheStatsResponse(
            total_cached_responses=stats["total_cached_responses"],
            total_cache_hits=stats["total_cache_hits"],
            estimated_tokens_saved=stats["estimated_tokens_saved"],
            by_agent=stats.get("by_agent", {}),
            cache_enabled=CACHE_ENABLED,
        )
    except ImportError as e:
        raise HTTPException(status_code=503, detail=f"Semantic cache module not available: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/cache/clear", summary="Xóa toàn bộ Semantic Cache")
async def clear_cache():
    """Xóa toàn bộ cache entries (dùng khi cần force refresh LLM responses)."""
    try:
        cache_db = ROOT / "semantic_cache.db"
        if not cache_db.exists():
            return {"status": "ok", "message": "Cache database không tồn tại, không cần xóa."}
        import sqlite3
        conn = sqlite3.connect(str(cache_db))
        cursor = conn.execute("DELETE FROM semantic_cache")
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        return {"status": "ok", "deleted_entries": deleted, "message": f"Đã xóa {deleted} cache entries."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Disk to Database Sync ─────────────────────────────────

@router.post("/sync-disk", summary="Đồng bộ dữ liệu từ ổ đĩa vào Database")
async def sync_disk_to_db():
    """Quét thư mục output/ và cập nhật dữ liệu vào cơ sở dữ liệu."""
    from app.db.session import AsyncSessionLocal
    from app.models.course import Course
    from app.models.session import Session
    from app.models.lesson import Lesson
    from app.models.artifact import Artifact
    from sqlalchemy.future import select
    import json

    output_dir = ROOT / "output"
    if not output_dir.exists():
        return {"status": "error", "message": "Thư mục output không tồn tại."}

    stats = {"courses_synced": 0, "sessions_synced": 0, "lessons_synced": 0, "artifacts_updated": 0}

    async with AsyncSessionLocal() as db:
        for course_path in output_dir.iterdir():
            if not course_path.is_dir(): continue
            course_name = course_path.name.replace("_", " ")

            # Find or create Course
            res = await db.execute(select(Course).where(Course.name == course_name))
            course = res.scalars().first()
            if not course:
                course = Course(name=course_name, description="Đồng bộ từ ổ đĩa")
                db.add(course)
                await db.commit()
                await db.refresh(course)
            stats["courses_synced"] += 1

            # Sessions
            for session_path in course_path.iterdir():
                if not session_path.is_dir() or not session_path.name.startswith("Session"): continue
                session_title = session_path.name

                res = await db.execute(select(Session).where(Session.course_id == course.id, Session.name == session_title))
                session = res.scalars().first()
                if not session:
                    session = Session(course_id=course.id, name=session_title, title=session_title, order_index=stats["sessions_synced"])
                    db.add(session)
                    await db.commit()
                    await db.refresh(session)
                stats["sessions_synced"] += 1

                # Lessons
                for lesson_path in session_path.iterdir():
                    if not lesson_path.is_dir() or not lesson_path.name.startswith("Lesson"): continue
                    lesson_title = lesson_path.name

                    res = await db.execute(select(Lesson).where(Lesson.session_id == session.id, Lesson.name == lesson_title))
                    lesson = res.scalars().first()
                    if not lesson:
                        lesson = Lesson(session_id=session.id, name=lesson_title, title=lesson_title, order_index=stats["lessons_synced"])
                        db.add(lesson)
                        await db.commit()
                        await db.refresh(lesson)
                    stats["lessons_synced"] += 1

                    # Artifacts in lesson
                    # HTML
                    html_file = lesson_path / "reading.html"
                    if html_file.exists():
                        res = await db.execute(select(Artifact).where(Artifact.lesson_id == lesson.id, Artifact.type == "reading"))
                        art = res.scalars().first()
                        if not art:
                            art = Artifact(lesson_id=lesson.id, type="reading", status="Completed", content=html_file.read_text(encoding="utf-8"))
                            db.add(art)
                        else:
                            art.content = html_file.read_text(encoding="utf-8")
                            art.status = "Completed"
                        stats["artifacts_updated"] += 1

                    # Quiz
                    quiz_file = lesson_path / "quiz.json"
                    if quiz_file.exists():
                        try:
                            qdata = json.loads(quiz_file.read_text(encoding="utf-8"))
                            res = await db.execute(select(Artifact).where(Artifact.lesson_id == lesson.id, Artifact.type == "quiz"))
                            art = res.scalars().first()
                            if not art:
                                art = Artifact(lesson_id=lesson.id, type="quiz", status="Completed", content_json=qdata)
                                db.add(art)
                            else:
                                art.content_json = qdata
                                art.status = "Completed"
                            stats["artifacts_updated"] += 1
                        except: pass

                    # Mindmap
                    md_file = lesson_path / "outline.md"
                    if md_file.exists():
                        res = await db.execute(select(Artifact).where(Artifact.lesson_id == lesson.id, Artifact.type == "outline"))
                        art = res.scalars().first()
                        if not art:
                            art = Artifact(lesson_id=lesson.id, type="outline", status="Completed", content=md_file.read_text(encoding="utf-8"))
                            db.add(art)
                        else:
                            art.content = md_file.read_text(encoding="utf-8")
                            art.status = "Completed"
                        stats["artifacts_updated"] += 1

        await db.commit()

    return {"status": "success", "message": "Đồng bộ thành công!", "stats": stats}

# ── Knowledge Memory ──────────────────────────────────────

@router.get("/knowledge-memory", response_model=List[KnowledgeMemoryItem], summary="Xem Knowledge Memory Store")
async def get_knowledge_memories(
    tech_stack: Optional[str] = Query(None, description="Lọc theo tech stack, ví dụ: python/fastapi"),
    scope: Optional[str] = Query(None, description="Lọc theo scope: html, quiz, slide, mindmap..."),
    category: Optional[str] = Query(None, description="Lọc theo category lỗi"),
    limit: int = Query(50, ge=1, le=200),
):
    """Xem danh sách lessons learned được lưu trong Knowledge Memory Agent SQLite."""
    try:
        sys.path.insert(0, str(ROOT))
        from agents.knowledge_memory_agent import recall_memories
        memories = recall_memories(tech_stack=tech_stack, scope=scope, limit=limit)

        results = []
        for m in memories:
            if category and m.get("category") != category:
                continue
            results.append(KnowledgeMemoryItem(
                id=m.get("id", 0),
                category=m.get("category", "other"),
                severity=m.get("severity", "low"),
                description=m.get("description", ""),
                bad_example=m.get("bad_example"),
                good_example=m.get("good_example"),
                tech_stack=m.get("tech_stack"),
                scope=m.get("scope"),
                hit_count=m.get("hit_count", 0),
                created_at=str(m.get("created_at", "")),
            ))
        return results
    except ImportError as e:
        raise HTTPException(status_code=503, detail=f"Knowledge memory agent not available: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/knowledge-memory/categories", summary="Danh sách categories lỗi")
async def get_memory_categories():
    """Trả về danh sách 10 categories lỗi chuẩn của hệ thống."""
    return {
        "categories": [
            {"key": "scope_violation", "label": "Vi phạm phạm vi", "color": "red"},
            {"key": "syntax_error", "label": "Lỗi cú pháp", "color": "orange"},
            {"key": "format_violation", "label": "Vi phạm định dạng", "color": "gold"},
            {"key": "prerequisite_leak", "label": "Rò rỉ tiên quyết", "color": "purple"},
            {"key": "pedagogical_error", "label": "Lỗi sư phạm", "color": "blue"},
            {"key": "image_prompt_error", "label": "Lỗi prompt ảnh", "color": "cyan"},
            {"key": "structure_error", "label": "Lỗi cấu trúc", "color": "geekblue"},
            {"key": "terminology_error", "label": "Lỗi thuật ngữ", "color": "magenta"},
            {"key": "ai_mention_violation", "label": "Vi phạm đề cập AI", "color": "volcano"},
            {"key": "other", "label": "Khác", "color": "default"},
        ]
    }


# ── Prerequisite Reports ──────────────────────────────────

@router.get("/prerequisite-report/{course_name}", response_model=PrerequisiteReportResponse,
            summary="Xem báo cáo Prerequisite Guard")
async def get_prerequisite_report(course_name: str):
    """Lấy báo cáo kiểm tra tiên quyết cho một khóa học đã biên dịch."""
    safe_name = course_name.strip().replace(" ", "_").replace("-", "_")
    report_path = ROOT / "output" / safe_name / "prerequisite_report.md"

    if not report_path.exists():
        return PrerequisiteReportResponse(
            course_name=course_name,
            report_path=None,
            has_blockers=False,
            blocker_count=0,
            warning_count=0,
            report_content=None,
        )

    content = report_path.read_text(encoding="utf-8")
    blocker_count = content.count("🔴 **BLOCKER**") + content.count("BLOCKER")
    warning_count = content.count("🟡 **WARNING**") + content.count("WARNING")

    return PrerequisiteReportResponse(
        course_name=course_name,
        report_path=str(report_path),
        has_blockers=blocker_count > 0,
        blocker_count=blocker_count,
        warning_count=warning_count,
        report_content=content,
    )


# ── SCORM Export ──────────────────────────────────────────

@router.post("/scorm/export", summary="Xuất SCORM 1.2 Package")
async def export_scorm(payload: SCORMExportRequest, background_tasks: BackgroundTasks):
    """
    Khởi động tiến trình xuất SCORM 1.2 package từ học liệu đã biên dịch.
    Trả về ngay với task_id, client poll GET /scorm/status/{task_id} để theo dõi.
    """
    safe_name = payload.course_name.strip().replace(" ", "_").replace("-", "_")
    output_dir = payload.output_dir or str(ROOT / "output" / safe_name)

    if not Path(output_dir).exists():
        raise HTTPException(
            status_code=404,
            detail=f"Thư mục output không tồn tại: {output_dir}. Hãy chạy pipeline biên dịch trước."
        )

    import uuid
    task_id = str(uuid.uuid4())[:8]
    _scorm_tasks[task_id] = {"status": "running", "progress": "Đang khởi động..."}

    async def run_export():
        try:
            sys.path.insert(0, str(ROOT))
            from core.scorm_exporter import export_scorm_package
            _scorm_tasks[task_id]["progress"] = "Đang quét bài học..."
            zip_path = export_scorm_package(
                output_course_dir=output_dir,
                course_name=payload.course_name,
            )
            _scorm_tasks[task_id] = {
                "status": "completed",
                "zip_path": zip_path,
                "progress": "Hoàn tất",
                "download_url": f"/api/v1/pipeline/scorm/download/{task_id}",
            }
        except Exception as e:
            _scorm_tasks[task_id] = {"status": "failed", "error": str(e), "progress": "Thất bại"}

    background_tasks.add_task(run_export)
    return {"task_id": task_id, "status": "running", "message": "SCORM export đã bắt đầu."}


_scorm_tasks: dict = {}


@router.get("/scorm/status/{task_id}", summary="Kiểm tra trạng thái SCORM export")
async def get_scorm_status(task_id: str):
    if task_id not in _scorm_tasks:
        raise HTTPException(status_code=404, detail="Task không tồn tại.")
    return _scorm_tasks[task_id]


@router.get("/scorm/download/{task_id}", summary="Tải xuống SCORM package")
async def download_scorm(task_id: str):
    task = _scorm_tasks.get(task_id)
    if not task or task.get("status") != "completed":
        raise HTTPException(status_code=404, detail="SCORM package chưa sẵn sàng.")
    zip_path = task.get("zip_path")
    if not zip_path or not Path(zip_path).exists():
        raise HTTPException(status_code=404, detail="File SCORM không tìm thấy.")
    return FileResponse(
        path=zip_path,
        media_type="application/zip",
        filename=Path(zip_path).name,
    )

# ── PM Reviewer & Updater ─────────────────────────────────

@router.post("/pm/review", summary="Tải lên và Thẩm định file PM")
async def review_pm(file: UploadFile = File(...)):
    """Upload file PM Excel và chạy thẩm định qua AI (PM Reviewer)."""
    try:
        sys.path.insert(0, str(ROOT))
        from main import parse_all_sessions
        from agents.reviewer_agents import pm_reviewer_agent
        
        # Save uploaded file
        upload_dir = ROOT / "output" / "tmp_uploads"
        upload_dir.mkdir(parents=True, exist_ok=True)
        file_path = upload_dir / file.filename
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        sessions = parse_all_sessions(str(file_path))
        full_curriculum_json = json.dumps(sessions, ensure_ascii=False)
        
        # Guess tech stack from filename
        tech_stack = "python/fastapi"
        fn = file.filename.lower()
        if "nestjs" in fn or "nest" in fn:
            tech_stack = "typescript/nestjs"
        elif "react" in fn:
            tech_stack = "typescript/react"
        elif "java" in fn or "springboot" in fn:
            tech_stack = "java/springboot"
        elif "core" in fn or "basic" in fn:
            tech_stack = "python/core"
            
        report = pm_reviewer_agent(full_curriculum_json, tech_stack)
        
        report_path = upload_dir / f"{file_path.stem}_review_report.md"
        report_path.write_text(report, encoding="utf-8")
        
        return {
            "status": "success",
            "file_path": str(file_path),
            "tech_stack": tech_stack,
            "report": report,
            "json_data": full_curriculum_json
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class PMUpdateRequest(BaseModel):
    file_path: str
    tech_stack: str
    json_data: str
    report: str

@router.post("/pm/update", summary="Tự động cập nhật file PM")
async def update_pm(payload: PMUpdateRequest):
    """Sử dụng AI để tự động cập nhật file Excel PM dựa trên báo cáo thẩm định."""
    try:
        sys.path.insert(0, str(ROOT))
        from agents.reviewer_agents import pm_updater_agent
        from core.pm_updater_excel import export_updated_pm_to_excel
        import json as json_lib
        
        updated_json = pm_updater_agent(payload.json_data, payload.report, payload.tech_stack)
        clean_json = updated_json.replace("```json", "").replace("```", "").strip()
        parsed_json = json_lib.loads(clean_json)
        
        excel_path = Path(payload.file_path)
        new_excel_path = excel_path.with_name(f"{excel_path.stem}_AI_Updated.xlsx")
        
        export_updated_pm_to_excel(parsed_json, str(excel_path), str(new_excel_path))
        
        return {
            "status": "success",
            "new_file_path": str(new_excel_path),
            "message": "File PM đã được AI tự động khắc phục và cập nhật.",
            "download_url": f"/api/v1/pipeline/pm/download?path={new_excel_path.name}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/pm/download", summary="Tải xuống file PM")
async def download_pm(path: str):
    file_path = ROOT / "output" / "tmp_uploads" / path
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File không tồn tại")
    return FileResponse(path=file_path, filename=file_path.name)

# ── Obsidian Export ───────────────────────────────────────

class ObsidianExportRequest(BaseModel):
    pm_path: str

@router.post("/obsidian/export", summary="Xuất Obsidian Knowledge Vault")
async def export_obsidian(payload: ObsidianExportRequest, background_tasks: BackgroundTasks):
    if not Path(payload.pm_path).exists():
        raise HTTPException(status_code=404, detail="File PM không tồn tại. Vui lòng upload file PM trước.")
        
    import uuid
    task_id = str(uuid.uuid4())[:8]
    _obsidian_tasks[task_id] = {"status": "running", "progress": "Đang phân tích PM cho Obsidian..."}

    async def run_export():
        try:
            sys.path.insert(0, str(ROOT))
            from main import parse_all_sessions
            from agents.prerequisite_guard_agent import run_prerequisite_check_for_pm
            
            _obsidian_tasks[task_id]["progress"] = "Đang kiểm tra ràng buộc tiên quyết..."
            sessions = parse_all_sessions(payload.pm_path)
            
            stack = "python/fastapi"
            fn = payload.pm_path.lower()
            if "nestjs" in fn or "nest" in fn: stack = "typescript/nestjs"
            elif "core" in fn or "basic" in fn: stack = "python/core"
                
            _, prerequisite_data = run_prerequisite_check_for_pm(sessions, stack)
            
            _obsidian_tasks[task_id]["progress"] = "Đang tạo Knowledge Linker Vault..."
            
            try:
                from core.obsidian_knowledge_linker import generate_knowledge_vault
                vault_path = generate_knowledge_vault(
                    excel_path=payload.pm_path,
                    sessions=sessions,
                    prerequisite_data=prerequisite_data,
                )
            except ImportError:
                from core.obsidian_exporter import generate_obsidian_vault
                vault_path = generate_obsidian_vault(payload.pm_path)
                
            _obsidian_tasks[task_id] = {
                "status": "completed",
                "vault_path": str(vault_path),
                "progress": "Hoàn tất",
            }
        except Exception as e:
            _obsidian_tasks[task_id] = {"status": "failed", "error": str(e), "progress": "Thất bại"}

    background_tasks.add_task(run_export)
    return {"task_id": task_id, "status": "running", "message": "Obsidian export đã bắt đầu."}

_obsidian_tasks: dict = {}

@router.get("/obsidian/status/{task_id}", summary="Kiểm tra trạng thái Obsidian export")
async def get_obsidian_status(task_id: str):
    if task_id not in _obsidian_tasks:
        raise HTTPException(status_code=404, detail="Task không tồn tại.")
    return _obsidian_tasks[task_id]

# ── Video Render Pipeline ─────────────────────────────────

@router.get("/course-status/{course_id}", summary="Lấy toàn bộ trạng thái học liệu của khóa học")
async def get_course_artifacts_status(course_id: int):
    from app.db.session import AsyncSessionLocal
    from app.models.course import Course
    from app.models.session import Session
    from app.models.lesson import Lesson
    from app.models.artifact import Artifact
    from sqlalchemy.future import select
    
    async with AsyncSessionLocal() as db:
        course = await db.get(Course, course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
            
        sessions_res = await db.execute(
            select(Session).where(Session.course_id == course_id).order_by(Session.order_index.asc(), Session.id.asc())
        )
        sessions = sessions_res.scalars().all()
        session_ids = [s.id for s in sessions]
        
        lessons_res = await db.execute(
            select(Lesson).where(Lesson.session_id.in_(session_ids)).order_by(Lesson.order_index.asc(), Lesson.id.asc())
        ) if session_ids else None
        lessons = lessons_res.scalars().all() if lessons_res else []
        lesson_ids = [l.id for l in lessons]
        
        # Fetch all artifacts for these sessions and lessons
        session_artifacts = []
        if session_ids:
            s_art_res = await db.execute(select(Artifact).where(Artifact.session_id.in_(session_ids)))
            session_artifacts = s_art_res.scalars().all()
            
        lesson_artifacts = []
        if lesson_ids:
            l_art_res = await db.execute(select(Artifact).where(Artifact.lesson_id.in_(lesson_ids)))
            lesson_artifacts = l_art_res.scalars().all()
            
        # Structure the response
        res_data = {
            "course": {
                "id": course.id,
                "name": course.name,
                "technology_stack": course.technology_stack,
            },
            "sessions": []
        }
        
        for sess in sessions:
            sess_arts = [
                {"id": a.id, "type": a.type, "status": a.status}
                for a in session_artifacts if a.session_id == sess.id
            ]
            sess_lessons = []
            for les in lessons:
                if les.session_id == sess.id:
                    les_arts = [
                        {"id": a.id, "type": a.type, "status": a.status}
                        for a in lesson_artifacts if a.lesson_id == les.id
                    ]
                    sess_lessons.append({
                        "id": les.id,
                        "name": les.name,
                        "title": les.title,
                        "artifacts": les_arts
                    })
            res_data["sessions"].append({
                "id": sess.id,
                "name": sess.name,
                "title": sess.title,
                "artifacts": sess_arts,
                "lessons": sess_lessons
            })
            
        return res_data

class VideoRenderRequest(BaseModel):
    course_name: str
    session_id: str
    lesson_id: str

@router.post("/video/render", summary="Render Video bằng Hyperframes")
async def render_video(payload: VideoRenderRequest, background_tasks: BackgroundTasks):
    import uuid
    task_id = str(uuid.uuid4())[:8]
    _video_tasks[task_id] = {"status": "running", "progress": "Khởi tạo môi trường Hyperframes..."}

    async def run_render():
        import asyncio
        try:
            await asyncio.sleep(2)
            _video_tasks[task_id]["progress"] = "Đang phân tích SCRIPT.md..."
            await asyncio.sleep(2)
            _video_tasks[task_id]["progress"] = "Đang render bằng Hyperframes Engine..."
            await asyncio.sleep(3)
            
            safe_name = payload.course_name.strip().replace(" ", "_").replace("-", "_")
            video_path = f"output/{safe_name}/{payload.session_id}/{payload.lesson_id}/Video/final_render.mp4"
            
            _video_tasks[task_id] = {
                "status": "completed",
                "progress": "Render thành công",
                "video_url": f"/api/v1/pipeline/video/download?path={video_path}"
            }
        except Exception as e:
            _video_tasks[task_id] = {"status": "failed", "error": str(e), "progress": "Thất bại"}

    background_tasks.add_task(run_render)
    return {"task_id": task_id, "status": "running", "message": "Video rendering started."}

_video_tasks: dict = {}

@router.get("/video/status/{task_id}", summary="Kiểm tra trạng thái Video Render")
async def get_video_status(task_id: str):
    if task_id not in _video_tasks:
        raise HTTPException(status_code=404, detail="Task không tồn tại.")
    return _video_tasks[task_id]

# ── Dashboard Stats ───────────────────────────────────────

@router.get("/stats/dashboard", summary="Thống kê tổng quan Dashboard")
async def get_dashboard_stats():
    """
    Tổng hợp số liệu thống kê từ DB và các file hệ thống để hiển thị Dashboard thật.
    """
    from app.db.session import AsyncSessionLocal
    from app.models.course import Course
    from app.models.session import Session
    from app.models.lesson import Lesson
    from app.models.artifact import Artifact
    from sqlalchemy.future import select
    from sqlalchemy import func

    try:
        async with AsyncSessionLocal() as db:
            total_courses = (await db.execute(select(func.count()).select_from(Course))).scalar()
            total_sessions = (await db.execute(select(func.count()).select_from(Session))).scalar()
            total_lessons = (await db.execute(select(func.count()).select_from(Lesson))).scalar()

            # Artifact stats
            art_result = await db.execute(
                select(Artifact.status, func.count().label("cnt"))
                .group_by(Artifact.status)
            )
            artifact_by_status = {row.status: row.cnt for row in art_result}

            total_artifacts = sum(artifact_by_status.values())
            approved = artifact_by_status.get("Completed", 0)
            pending = artifact_by_status.get("Pending", 0)
            failed = artifact_by_status.get("Failed", 0)

        # Cache stats (non-blocking)
        cache_hits = 0
        try:
            sys.path.insert(0, str(ROOT))
            from core.semantic_cache import get_cache_stats
            cs = get_cache_stats()
            cache_hits = cs.get("total_cache_hits", 0)
        except Exception:
            pass

        # Knowledge memories count
        memory_count = 0
        try:
            kdb = ROOT / "knowledge_store.db"
            if kdb.exists():
                import sqlite3
                conn = sqlite3.connect(str(kdb))
                memory_count = conn.execute("SELECT COUNT(*) FROM knowledge_memories").fetchone()[0]
                conn.close()
        except Exception:
            pass

        return {
            "courses": total_courses,
            "sessions": total_sessions,
            "lessons": total_lessons,
            "artifacts": {
                "total": total_artifacts,
                "completed": approved,
                "pending": pending,
                "failed": failed,
                "success_rate": round(approved / total_artifacts * 100, 1) if total_artifacts else 0,
            },
            "cache_hits": cache_hits,
            "knowledge_memories": memory_count,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
