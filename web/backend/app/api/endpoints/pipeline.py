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
_BACKEND_DIR = Path(__file__).resolve().parents[5]  # Learning-Material root
_PROJECT_ROOT = _BACKEND_DIR


def _resolve_root() -> Path:
    """Resolve the Learning-Material project root robustly."""
    # When running from web/backend, go up 5 levels
    candidates = [
        Path(__file__).resolve().parents[5],
        Path(os.getcwd()),
    ]
    for c in candidates:
        if (c / "core" / "semantic_cache.py").exists():
            return c
    return candidates[0]


ROOT = _resolve_root()

def safe_print(msg: str):
    try:
        print(msg)
    except UnicodeEncodeError:
        try:
            print(msg.encode('ascii', errors='replace').decode('ascii'))
        except Exception:
            pass


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
    draft: bool = False


async def run_cmd_async(cmd: List[str]):
    import asyncio
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        err_msg = stderr.decode("utf-8", errors="replace")
        raise Exception(f"Command {' '.join(cmd)} failed with exit code {proc.returncode}: {err_msg}")
    return stdout


async def assemble_final_video(project_dir: Path, output_file: Path, final_render_path: Path):
    import asyncio
    import json
    assets_dir = project_dir / "assets"
    temp_dir = project_dir / "temp_assembly"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # 1. Probe out.mp4
        probe_cmd = [
            "ffprobe", "-v", "error", 
            "-show_entries", "stream=width,height,r_frame_rate,pix_fmt,codec_type,sample_rate,channels",
            "-of", "json", str(output_file)
        ]
        probe_stdout = await run_cmd_async(probe_cmd)
        probe_data = json.loads(probe_stdout.decode("utf-8"))
        
        video_stream = next((s for s in probe_data.get("streams", []) if s.get("codec_type") == "video"), None)
        audio_stream = next((s for s in probe_data.get("streams", []) if s.get("codec_type") == "audio"), None)
        
        width = video_stream.get("width", 1920) if video_stream else 1920
        height = video_stream.get("height", 1080) if video_stream else 1080
        pix_fmt = video_stream.get("pix_fmt", "yuv420p") if video_stream else "yuv420p"
        
        fps_str = video_stream.get("r_frame_rate", "30/1") if video_stream else "30/1"
        if "/" in fps_str:
            num, den = fps_str.split("/")
            framerate = float(num) / float(den) if float(den) != 0 else 30.0
        else:
            framerate = float(fps_str)
            
        has_audio = audio_stream is not None
        sample_rate = int(audio_stream.get("sample_rate", 44100)) if has_audio else 44100
        channels = int(audio_stream.get("channels", 2)) if has_audio else 2
        
        # 2. Check bg-music
        bg_music = assets_dir / "bg-music.mp3"
        temp_main = temp_dir / "temp_main.mp4"
        
        if bg_music.exists():
            if has_audio:
                mix_cmd = [
                    "ffmpeg", "-y", "-i", str(output_file),
                    "-stream_loop", "-1", "-i", str(bg_music),
                    "-filter_complex", "[1:a]volume=0.05[bgm];[0:a][bgm]amix=inputs=2:duration=first[a]",
                    "-map", "0:v", "-map", "[a]",
                    "-c:v", "copy", "-c:a", "aac", "-ar", str(sample_rate), "-ac", str(channels),
                    str(temp_main)
                ]
            else:
                mix_cmd = [
                    "ffmpeg", "-y", "-i", str(output_file),
                    "-stream_loop", "-1", "-i", str(bg_music),
                    "-map", "0:v", "-map", "1:a", "-shortest",
                    "-c:v", "copy", "-c:a", "aac", "-ar", str(sample_rate), "-ac", str(channels),
                    str(temp_main)
                ]
            await run_cmd_async(mix_cmd)
        else:
            if not has_audio:
                silent_cmd = [
                    "ffmpeg", "-y", "-i", str(output_file),
                    "-f", "lavfi", "-i", f"anullsrc=r={sample_rate}:cl=stereo",
                    "-map", "0:v", "-map", "1:a", "-shortest",
                    "-c:v", "copy", "-c:a", "aac", "-ar", str(sample_rate), "-ac", str(channels),
                    str(temp_main)
                ]
                await run_cmd_async(silent_cmd)
            else:
                shutil.copy2(output_file, temp_main)
                
        # 3. Normalize intro
        intro_file = assets_dir / "intro.mp4"
        intro_norm = temp_dir / "temp_intro.mp4"
        if intro_file.exists():
            intro_probe_cmd = [
                "ffprobe", "-v", "error", "-show_entries", "stream=codec_type",
                "-of", "json", str(intro_file)
            ]
            intro_probe_stdout = await run_cmd_async(intro_probe_cmd)
            intro_probe = json.loads(intro_probe_stdout.decode("utf-8"))
            intro_has_audio = any(s.get("codec_type") == "audio" for s in intro_probe.get("streams", []))
            
            if intro_has_audio:
                norm_intro_cmd = [
                    "ffmpeg", "-y", "-i", str(intro_file),
                    "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2",
                    "-r", str(framerate), "-pix_fmt", pix_fmt,
                    "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                    "-c:a", "aac", "-ar", str(sample_rate), "-ac", str(channels),
                    str(intro_norm)
                ]
            else:
                norm_intro_cmd = [
                    "ffmpeg", "-y", "-i", str(intro_file),
                    "-f", "lavfi", "-i", f"anullsrc=r={sample_rate}:cl=stereo",
                    "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2",
                    "-r", str(framerate), "-pix_fmt", pix_fmt, "-shortest",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                    "-c:a", "aac", "-ar", str(sample_rate), "-ac", str(channels),
                    str(intro_norm)
                ]
            await run_cmd_async(norm_intro_cmd)
            
        # 4. Normalize outro
        outro_file = assets_dir / "outro.mp4"
        outro_norm = temp_dir / "temp_outro.mp4"
        if outro_file.exists():
            outro_probe_cmd = [
                "ffprobe", "-v", "error", "-show_entries", "stream=codec_type",
                "-of", "json", str(outro_file)
            ]
            outro_probe_stdout = await run_cmd_async(outro_probe_cmd)
            outro_probe = json.loads(outro_probe_stdout.decode("utf-8"))
            outro_has_audio = any(s.get("codec_type") == "audio" for s in outro_probe.get("streams", []))
            
            if outro_has_audio:
                norm_outro_cmd = [
                    "ffmpeg", "-y", "-i", str(outro_file),
                    "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2",
                    "-r", str(framerate), "-pix_fmt", pix_fmt,
                    "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                    "-c:a", "aac", "-ar", str(sample_rate), "-ac", str(channels),
                    str(outro_norm)
                ]
            else:
                norm_outro_cmd = [
                    "ffmpeg", "-y", "-i", str(outro_file),
                    "-f", "lavfi", "-i", f"anullsrc=r={sample_rate}:cl=stereo",
                    "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2",
                    "-r", str(framerate), "-pix_fmt", pix_fmt, "-shortest",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                    "-c:a", "aac", "-ar", str(sample_rate), "-ac", str(channels),
                    str(outro_norm)
                ]
            await run_cmd_async(norm_outro_cmd)
            
        # 5. Concatenate
        if intro_norm.exists() or outro_norm.exists():
            concat_list_path = temp_dir / "list.txt"
            with open(concat_list_path, "w", encoding="utf-8") as f:
                if intro_norm.exists():
                    f.write(f"file '{intro_norm.as_posix()}'\n")
                f.write(f"file '{temp_main.as_posix()}'\n")
                if outro_norm.exists():
                    f.write(f"file '{outro_norm.as_posix()}'\n")
                    
            concat_cmd = [
                "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list_path),
                "-c", "copy", str(final_render_path)
            ]
            await run_cmd_async(concat_cmd)
        else:
            shutil.copy2(temp_main, final_render_path)
            
    finally:
        # Cleanup temp_dir
        if temp_dir.exists():
            try:
                shutil.rmtree(temp_dir)
            except Exception:
                pass

@router.post("/video/render", summary="Render Video bằng Hyperframes")
async def render_video(payload: VideoRenderRequest, background_tasks: BackgroundTasks):
    import uuid
    task_id = str(uuid.uuid4())[:8]
    _video_tasks[task_id] = {"status": "running", "progress": "Khởi tạo..."}

    async def run_render():
        import asyncio
        import shutil
        
        try:
            # 1. Locate the video project directory dynamically
            safe_course = payload.course_name.strip().replace(" ", "_").replace("-", "_")
            course_path = ROOT / "output" / safe_course
            
            if not course_path.exists():
                raise Exception(f"Không tìm thấy thư mục khóa học: {course_path}")
                
            session_dir = None
            for item in course_path.iterdir():
                if item.is_dir() and (item.name.startswith(payload.session_id + " ") or item.name == payload.session_id):
                    session_dir = item
                    break
                    
            if not session_dir:
                raise Exception(f"Không tìm thấy thư mục Session: {payload.session_id}")
                
            lesson_dir = None
            for item in session_dir.iterdir():
                if item.is_dir() and (item.name.startswith(payload.lesson_id + " ") or item.name == payload.lesson_id):
                    lesson_dir = item
                    break
                    
            if not lesson_dir:
                raise Exception(f"Không tìm thấy thư mục Lesson: {payload.lesson_id}")
                
            video_dir = lesson_dir / "Video"
            if not video_dir.exists():
                raise Exception("Không tìm thấy thư mục Video trong bài học")
                
            project_dir = None
            for item in video_dir.iterdir():
                if item.is_dir() and (item / "package.json").exists():
                    project_dir = item
                    break
                    
            if not project_dir:
                if (video_dir / "package.json").exists():
                    project_dir = video_dir
                    
            if not project_dir:
                raise Exception("Không tìm thấy thư mục dự án HyperFrames (thiếu package.json)")
            
            # 2. Run check/lint to validate (unless it's a draft rendering)
            if not payload.draft:
                _video_tasks[task_id]["progress"] = "Đang kiểm tra chất lượng (npx hyperframes check)..."
                safe_print(f"[{task_id}] Running check in {project_dir}...")
                
                check_process = await asyncio.create_subprocess_shell(
                    "npm run check",
                    cwd=str(project_dir),
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                check_stdout, check_stderr = await check_process.communicate()
                if check_process.returncode != 0:
                    check_out = (check_stderr or check_stdout or b"").decode("utf-8", errors="replace")
                    safe_print(f"[{task_id}] Check warnings/errors:\n{check_out}")
            else:
                safe_print(f"[{task_id}] Skipping check stage because it's a draft rendering.")
            
            # 3. Run render
            quality = "low" if payload.draft else "high"
            _video_tasks[task_id]["progress"] = f"Đang render video ({quality} quality)..."
            safe_print(f"[{task_id}] Running render in {project_dir} with {quality} quality...")
            
            output_file = project_dir / "out.mp4"
            # Remove existing out.mp4 if present to avoid stale file reads
            if output_file.exists():
                try:
                    output_file.unlink()
                except Exception:
                    pass
            
            _video_tasks[task_id]["percent"] = 5
            render_cmd = f"npx --yes hyperframes@0.6.63 render --quality {quality} --output out.mp4"
            render_process = await asyncio.create_subprocess_shell(
                render_cmd,
                cwd=str(project_dir),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            render_out_lines = []
            render_err_lines = []
            import re
            
            async def read_stdout():
                while True:
                    line = await render_process.stdout.readline()
                    if not line:
                        break
                    line_str = line.decode("utf-8", errors="replace")
                    render_out_lines.append(line_str)
                    clean_line = line_str.strip()
                    if clean_line:
                        safe_print(f"[{task_id}] [STDOUT] {clean_line}")
                        pct_match = re.search(r"(\d+)%", clean_line)
                        if pct_match:
                            pct = int(pct_match.group(1))
                            _video_tasks[task_id]["progress"] = f"Rendering: {pct}%"
                            _video_tasks[task_id]["percent"] = pct
                        elif "Frame " in clean_line:
                            frame_match = re.search(r"Frame (\d+)/(\d+)", clean_line)
                            if frame_match:
                                curr, total = int(frame_match.group(1)), int(frame_match.group(2))
                                pct = int((curr / total) * 100)
                                _video_tasks[task_id]["progress"] = f"Rendering frame {curr}/{total} ({pct}%)"
                                _video_tasks[task_id]["percent"] = pct
                                
            async def read_stderr():
                while True:
                    line = await render_process.stderr.readline()
                    if not line:
                        break
                    line_str = line.decode("utf-8", errors="replace")
                    render_err_lines.append(line_str)
                    clean_line = line_str.strip()
                    if clean_line:
                        safe_print(f"[{task_id}] [STDERR] {clean_line}")
                        pct_match = re.search(r"(\d+)%", clean_line)
                        if pct_match:
                            pct = int(pct_match.group(1))
                            _video_tasks[task_id]["progress"] = f"Rendering: {pct}%"
                            _video_tasks[task_id]["percent"] = pct
                            
            await asyncio.gather(read_stdout(), read_stderr())
            await render_process.wait()
            
            render_out = "".join(render_out_lines)
            render_err = "".join(render_err_lines)
            
            if render_process.returncode != 0 or not output_file.exists() or output_file.stat().st_size == 0:
                raise Exception(f"Render failed (exit {render_process.returncode}): {render_err or render_out or 'Không có file out.mp4 được tạo ra.'}")
                
            # Assemble the final video with background music, intro, and outro
            _video_tasks[task_id]["progress"] = "Đang ghép intro, outro và nhạc nền..."
            final_render_path = project_dir / "final_render.mp4"
            await assemble_final_video(project_dir, output_file, final_render_path)
            
            # Get video download path relative to ROOT
            rel_video_path = final_render_path.relative_to(ROOT).as_posix()
            
            _video_tasks[task_id] = {
                "status": "completed",
                "progress": "Hoàn tất render",
                "video_url": f"/api/v1/pipeline/video/download?path={rel_video_path}"
            }
            safe_print(f"[{task_id}] Render completed successfully!")
            
        except Exception as e:
            safe_print(f"[{task_id}] Render failed with error: {e}")
            _video_tasks[task_id] = {"status": "failed", "error": str(e), "progress": f"Thất bại: {e}"}

    background_tasks.add_task(run_render)
    return {"task_id": task_id, "status": "running", "message": "Video rendering started."}

_video_tasks: dict = {}

@router.get("/video/status/{task_id}", summary="Kiểm tra trạng thái Video Render")
async def get_video_status(task_id: str):
    if task_id not in _video_tasks:
        raise HTTPException(status_code=404, detail="Task không tồn tại.")
    return _video_tasks[task_id]

@router.get("/video/download", summary="Tải xuống video đã render")
async def download_video(path: str):
    file_path = ROOT / path
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Video không tồn tại hoặc chưa được render")
    return FileResponse(path=file_path, media_type="video/mp4", filename=file_path.name)

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

def get_video_project_dir(course_name: str, session_id: str, lesson_id: str) -> Path:
    safe_course = course_name.strip().replace(" ", "_").replace("-", "_")
    course_path = ROOT / "output" / safe_course
    if not course_path.exists():
        raise Exception(f"Không tìm thấy thư mục khóa học: {course_path}")
        
    session_dir = None
    for item in course_path.iterdir():
        if item.is_dir() and (item.name.startswith(session_id + " ") or item.name == session_id):
            session_dir = item
            break
            
    if not session_dir:
        raise Exception(f"Không tìm thấy thư mục Session: {session_id}")
        
    lesson_dir = None
    for item in session_dir.iterdir():
        if item.is_dir() and (item.name.startswith(lesson_id + " ") or item.name == lesson_id):
            lesson_dir = item
            break
            
    if not lesson_dir:
        raise Exception(f"Không tìm thấy thư mục Lesson: {lesson_id}")
        
    video_dir = lesson_dir / "Video"
    if not video_dir.exists():
        raise Exception("Không tìm thấy thư mục Video trong bài học")
        
    project_dir = None
    for item in video_dir.iterdir():
        if item.is_dir() and (item / "package.json").exists():
            project_dir = item
            break
            
    if not project_dir:
        if (video_dir / "package.json").exists():
            project_dir = video_dir
            
    if not project_dir:
        raise Exception("Không tìm thấy thư mục dự án HyperFrames (thiếu package.json)")
        
    return project_dir

class SaveVideoFileRequest(BaseModel):
    course_name: str
    session_id: str
    lesson_id: str
    filename: str
    content: str

@router.get("/video/project-details", summary="Lấy chi tiết dự án video để xem preview và chỉnh sửa")
async def get_video_project_details(course_name: str, session_id: str, lesson_id: str):
    try:
        project_dir = get_video_project_dir(course_name, session_id, lesson_id)
        
        index_html_path = project_dir / "index.html"
        index_html_content = ""
        if index_html_path.exists():
            with open(index_html_path, "r", encoding="utf-8") as f:
                index_html_content = f.read()
                
        script_md_path = project_dir / "SCRIPT.md"
        script_md_content = ""
        if script_md_path.exists():
            with open(script_md_path, "r", encoding="utf-8") as f:
                script_md_content = f.read()
                
        # Calculate preview URL relative to /static (which serves ROOT / output)
        output_dir = ROOT / "output"
        rel_index_path = index_html_path.relative_to(output_dir).as_posix()
        preview_url = f"/static/{rel_index_path}"
        
        # Check if rendered video exists
        final_render_path = project_dir / "final_render.mp4"
        video_url = None
        if final_render_path.exists():
            rel_video_path = final_render_path.relative_to(ROOT).as_posix()
            video_url = f"/api/v1/pipeline/video/download?path={rel_video_path}"
            
        return {
            "status": "success",
            "project_found": True,
            "index_html": index_html_content,
            "script_md": script_md_content,
            "preview_url": preview_url,
            "video_url": video_url,
            "project_dir": str(project_dir)
        }
    except Exception as e:
        return {
            "status": "error",
            "project_found": False,
            "message": str(e)
        }

@router.post("/video/save-file", summary="Lưu tệp chỉnh sửa trực tiếp của video")
async def save_video_file(payload: SaveVideoFileRequest):
    try:
        project_dir = get_video_project_dir(payload.course_name, payload.session_id, payload.lesson_id)
        
        if payload.filename not in ["index.html", "SCRIPT.md"]:
            raise HTTPException(status_code=400, detail="Chỉ hỗ trợ chỉnh sửa index.html hoặc SCRIPT.md")
            
        target_path = project_dir / payload.filename
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(payload.content)
            
        return {
            "status": "success",
            "message": f"Đã lưu tệp {payload.filename} thành công."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
