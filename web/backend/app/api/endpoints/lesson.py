import asyncio
from typing import List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import AsyncSessionLocal as SessionLocal, get_db
from app.models.artifact import Artifact
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.session import Session
from app.schemas.lesson import LessonCreate, LessonResponse
from core.graph import compile_learning_content_workflow
from core.persistence import load_checkpoint
from core.state import AgentState

router = APIRouter()


@router.get("/", response_model=List[LessonResponse])
async def get_lessons(session_id: Optional[int] = None, db: AsyncSession = Depends(get_db)):
    query = select(Lesson).order_by(Lesson.order_index.asc(), Lesson.id.asc())
    if session_id:
        query = query.where(Lesson.session_id == session_id)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/", response_model=LessonResponse)
async def create_lesson(lesson_in: LessonCreate, db: AsyncSession = Depends(get_db)):
    # get max order
    query = (
        select(Lesson.order_index)
        .where(Lesson.session_id == lesson_in.session_id)
        .order_by(Lesson.order_index.desc())
    )
    res = await db.execute(query)
    max_order = res.scalars().first()
    next_order = (max_order or 0) + 1

    new_lesson = Lesson(**lesson_in.model_dump(), order_index=next_order)
    db.add(new_lesson)
    await db.commit()
    await db.refresh(new_lesson)
    return new_lesson


class ReorderPayload(BaseModel):
    item_ids: List[int]


@router.put("/reorder")
async def reorder_lessons(payload: ReorderPayload, db: AsyncSession = Depends(get_db)):
    for idx, l_id in enumerate(payload.item_ids):
        lesson = await db.get(Lesson, l_id)
        if lesson:
            lesson.order_index = idx
    await db.commit()
    return {"status": "success"}


@router.delete("/{lesson_id}")
async def delete_lesson(lesson_id: int, db: AsyncSession = Depends(get_db)):
    lesson = await db.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    await db.execute(delete(Artifact).where(Artifact.lesson_id == lesson_id))
    await db.delete(lesson)
    await db.commit()
    return {"status": "success"}


async def generate_lesson_task(
    lesson_id: int,
    session_id: int,
    pm_input: str,
    title: str,
    technology_stack: str = "python/fastapi",
    course_dir_name: str = "Database_Course",
):
    print(f"\n[AI TRIGGER] Bắt đầu sinh học liệu cho Lesson {lesson_id} - {title}")

    session_name = f"Session {session_id}"
    lesson_name = f"Lesson {lesson_id}"

    async with SessionLocal() as db:
        try:
            lesson_obj = await db.get(Lesson, lesson_id)
            if lesson_obj:
                lesson_name = lesson_obj.name or f"Lesson {lesson_id}"
            session_obj = await db.get(Session, session_id)
            if session_obj:
                session_name = session_obj.name or f"Session {session_id}"
        except Exception as db_err:
            print(f"Error querying lesson/session names: {db_err}")

    lesson_title_lower = title.lower() if title else ""
    details_lower = pm_input.lower() if pm_input else ""
    is_practical = any(
        kw in lesson_title_lower or kw in details_lower
        for kw in ["thực hành", "thuc hanh", "practice", "project", "dự án"]
    )

    lesson_requested_parts = ["html"] if is_practical else ["html", "quiz", "video_script", "mindmap"]

    def run_sync_workflow():
        workflow = compile_learning_content_workflow()
        initial_state: AgentState = {
            "session_id": str(session_name),
            "lesson_id": str(lesson_name),
            "pm_input": f"{title}\n{pm_input}",
            "time_reference": {},
            "learning_outcomes": {},
            "program_structure": {},
            "core_ssot": {},
            "artifacts_status": {},
            "html_content": "",
            "slide_markdown": "",
            "quiz_json": {},
            "video_script_markdown": "",
            "mindmap_markdown": "",
            "review_logs": [],
            "technology_stack": technology_stack,
            "course_dir_name": course_dir_name,
            "requested_parts": lesson_requested_parts,
            "force_rebuild": True,
            "previous_lessons": [],
            "pm_approved": True,
        }
        return workflow.run(initial_state)

    # Khởi chạy luồng chạy workflow AI và poller đồng bộ checkpoint thời gian thực
    task = asyncio.create_task(asyncio.to_thread(run_sync_workflow))

    checkpoint_key = f"{session_name}_{lesson_name}"
    if course_dir_name and not session_name.startswith(course_dir_name):
        checkpoint_key = f"{course_dir_name}_{session_name}_{lesson_name}"
    saved_artifacts = set()

    async def poll_checkpoints():
        while not task.done():
            await asyncio.sleep(3)
            try:
                state = load_checkpoint(checkpoint_key)
                if not state:
                    continue

                # Check các học liệu đã hoàn thành để đồng bộ lên DB ngay lập tức
                artifacts_to_save = {
                    "reading": (state.get("html_content"), state.get("artifacts_status", {}).get("html")),
                    "quiz": (state.get("quiz_json"), state.get("artifacts_status", {}).get("quiz")),
                    "outline": (
                        state.get("mindmap_markdown") or state.get("slide_markdown"),
                        state.get("artifacts_status", {}).get("mindmap"),
                    ),
                    "walkthrough": (
                        state.get("video_script_markdown") or state.get("html_content"),
                        state.get("artifacts_status", {}).get("video_script"),
                    ),
                }

                to_commit = {}
                for art_type, (content, status) in artifacts_to_save.items():
                    if status == "Approved" and content and art_type not in saved_artifacts:
                        to_commit[art_type] = content

                if to_commit:
                    async with SessionLocal() as db:
                        for art_type, content in to_commit.items():
                            stmt = select(Artifact).where(Artifact.lesson_id == lesson_id, Artifact.type == art_type)
                            result = await db.execute(stmt)
                            art = result.scalars().first()
                            if art and art.status == "Pending":
                                art.status = "Completed"
                                if isinstance(content, (dict, list)):
                                    art.content_json = content
                                else:
                                    art.content = str(content)
                                saved_artifacts.add(art_type)
                                print(f"[AI Realtime Sync] Đồng bộ sớm thành công phần: {art_type}")
                        await db.commit()
            except Exception as poll_err:
                print(f"[AI Realtime Sync Warning] Lỗi đồng bộ sớm checkpoint: {poll_err}")

    try:
        # Giới hạn thời gian tối đa là 5 phút (300 giây) để tránh treo vô hạn
        await asyncio.wait_for(asyncio.gather(task, poll_checkpoints()), timeout=300)
        final_state = task.result()
        print(f"\n[AI SUCCESS] Hoàn tất sinh học liệu cho Lesson {lesson_id}")

        # Lưu nốt các phần còn lại nếu có
        async with SessionLocal() as db:
            artifacts_to_save = {
                "reading": final_state.get("html_content"),
                "quiz": final_state.get("quiz_json"),
                "outline": final_state.get("mindmap_markdown") or final_state.get("slide_markdown"),
                "walkthrough": final_state.get("video_script_markdown") or final_state.get("html_content"),
            }

            for artifact_type, content in artifacts_to_save.items():
                if artifact_type not in saved_artifacts:
                    try:
                        stmt = select(Artifact).where(Artifact.lesson_id == lesson_id, Artifact.type == artifact_type)
                        result = await db.execute(stmt)
                        art = result.scalars().first()

                        if art:
                            if content:
                                art.status = "Completed"
                                if isinstance(content, (dict, list)):
                                    art.content_json = content
                                else:
                                    art.content = str(content)
                            else:
                                art.status = "Failed"
                    except Exception as e:
                        print(f"Error saving artifact {artifact_type}: {e}")
            await db.commit()

            # Check if all lessons of this session are completed
            try:
                lessons_stmt = select(Lesson).where(Lesson.session_id == session_id)
                lessons_res = await db.execute(lessons_stmt)
                all_lessons = lessons_res.scalars().all()
                all_lesson_ids = [l.id for l in all_lessons]

                if all_lesson_ids:
                    pending_stmt = select(Artifact).where(
                        Artifact.lesson_id.in_(all_lesson_ids), Artifact.status == "Pending"
                    )
                    pending_res = await db.execute(pending_stmt)
                    pending_artifacts = pending_res.scalars().all()

                    if not pending_artifacts:
                        print(
                            f"[AI Session Trigger] All lessons completed, auto-triggering session artifacts compilation for session {session_id}..."
                        )
                        from app.api.endpoints.session import generate_session_artifacts_task

                        await generate_session_artifacts_task(session_id)
            except Exception as auto_sess_err:
                print(f"Error auto-triggering session artifacts: {auto_sess_err}")

    except asyncio.TimeoutError:
        print(f"\n[AI TIMEOUT] Quá thời gian tối đa 5 phút cho Lesson {lesson_id}")
        # Đánh dấu các phần chưa hoàn thành là Failed và nêu rõ lý do quá hạn
        try:
            async with SessionLocal() as db:
                stmt = select(Artifact).where(Artifact.lesson_id == lesson_id, Artifact.status == "Pending")
                result = await db.execute(stmt)
                for art in result.scalars().all():
                    art.status = "Failed"
                    art.content = "Hệ thống tự động hủy tác vụ do thời gian phản hồi từ AI vượt quá 5 phút."
                await db.commit()
        except Exception as db_err:
            print(f"Lỗi khi đánh dấu Timeout cho artifacts: {db_err}")

    except Exception as e:
        print(f"\n[AI ERROR] Lỗi khi sinh học liệu: {str(e)}")
        try:
            async with SessionLocal() as db:
                stmt = select(Artifact).where(Artifact.lesson_id == lesson_id, Artifact.status == "Pending")
                result = await db.execute(stmt)
                for art in result.scalars().all():
                    art.status = "Failed"
                await db.commit()
        except Exception as db_err:
            print(f"Lỗi khi đánh dấu Failed cho artifacts: {db_err}")


@router.get("/{lesson_id}", response_model=LessonResponse)
async def get_lesson_by_id(lesson_id: int, db: AsyncSession = Depends(get_db)):
    lesson = await db.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


@router.post("/{lesson_id}/generate")
async def generate_lesson(
    lesson_id: int, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)
):
    lesson = await db.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    # Tạo các Artifact Pending ngay lập tức để UI render trạng thái Loading
    await db.execute(delete(Artifact).where(Artifact.lesson_id == lesson_id))

    lesson_title_lower = lesson.title.lower() if lesson.title else ""
    details_lower = lesson.details.lower() if lesson.details else ""
    is_practical = any(
        kw in lesson_title_lower or kw in details_lower
        for kw in ["thực hành", "thuc hanh", "practice", "project", "dự án"]
    )

    pending_types = ["reading"] if is_practical else ["outline", "reading", "quiz", "walkthrough"]
    for p_type in pending_types:
        db.add(Artifact(lesson_id=lesson_id, type=p_type, status="Pending"))
    await db.commit()

    session_res = await db.get(Session, lesson.session_id)
    tech_stack = "python/fastapi"
    course_dir_name = "Database_Course"
    if session_res:
        course_res = await db.get(Course, session_res.course_id)
        if course_res:
            if course_res.technology_stack:
                raw_tech = course_res.technology_stack
                tech_stack = (
                    "python/core"
                    if "python" in raw_tech.lower() and "fastapi" not in raw_tech.lower()
                    else raw_tech
                )
            if course_res.name:
                course_dir_name = course_res.name.strip().replace(" ", "_").replace("-", "_")

    pm_input = lesson.details if lesson.details else "Vui lòng phân tích và sinh bài học chi tiết."
    background_tasks.add_task(
        generate_lesson_task,
        lesson.id,
        lesson.session_id,
        pm_input,
        lesson.title,
        tech_stack,
        course_dir_name,
    )

    return {"status": "success", "message": f"AI bắt đầu sinh học liệu cho bài học: {lesson.title}"}
