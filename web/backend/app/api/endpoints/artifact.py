from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.db.session import get_db
from app.models.artifact import Artifact
from app.schemas.artifact import ArtifactResponse, ArtifactCreate
from app.utils.artifact import rewrite_artifacts_list, rewrite_artifact_response

router = APIRouter()

@router.get("/", response_model=List[ArtifactResponse])
async def get_artifacts(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Artifact))
    artifacts = result.scalars().all()
    return await rewrite_artifacts_list(db, artifacts, str(request.base_url))

@router.post("/", response_model=ArtifactResponse)
async def create_artifact(request: Request, artifact_in: ArtifactCreate, db: AsyncSession = Depends(get_db)):
    new_artifact = Artifact(**artifact_in.model_dump())
    db.add(new_artifact)
    await db.commit()
    await db.refresh(new_artifact)
    return await rewrite_artifact_response(db, new_artifact, str(request.base_url))

@router.get("/lesson/{lesson_id}", response_model=List[ArtifactResponse])
async def get_artifacts_by_lesson(lesson_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Artifact).where(Artifact.lesson_id == lesson_id))
    artifacts = result.scalars().all()
    return await rewrite_artifacts_list(db, artifacts, str(request.base_url))

from fastapi import HTTPException, BackgroundTasks
from app.schemas.artifact import ArtifactUpdate
from pydantic import BaseModel

class SelectVersionRequest(BaseModel):
    version_id: int

@router.put("/{artifact_id}", response_model=ArtifactResponse)
async def update_artifact(artifact_id: int, request: Request, artifact_in: ArtifactUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Artifact).where(Artifact.id == artifact_id))
    artifact = result.scalars().first()
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")
    
    update_data = artifact_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(artifact, key, value)
        
    await db.commit()
    await db.refresh(artifact)
    return await rewrite_artifact_response(db, artifact, str(request.base_url))

class RegenerateRequest(BaseModel):
    exercise_index: int = None

@router.post("/{artifact_id}/regenerate", response_model=ArtifactResponse)
async def regenerate_single_artifact(
    artifact_id: int,
    request: Request,
    background_tasks: BackgroundTasks,
    req_body: RegenerateRequest = None,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Artifact).where(Artifact.id == artifact_id)
    res = await db.execute(stmt)
    artifact = res.scalars().first()
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")
        
    artifact.status = "Pending"
    await db.commit()
    await db.refresh(artifact)
    
    exercise_index = req_body.exercise_index if req_body else None
    background_tasks.add_task(generate_single_artifact_task, artifact_id, exercise_index)
    return await rewrite_artifact_response(db, artifact, str(request.base_url))

@router.post("/{artifact_id}/select-version", response_model=ArtifactResponse)
async def select_artifact_version(
    artifact_id: int,
    req_body: SelectVersionRequest,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Artifact).where(Artifact.id == artifact_id)
    res = await db.execute(stmt)
    artifact = res.scalars().first()
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")
        
    versions = artifact.versions or []
    target_version = None
    for v in versions:
        if v.get("version_id") == req_body.version_id:
            target_version = v
            break
            
    if not target_version:
        raise HTTPException(status_code=400, detail="Version not found in history")
        
    artifact.content = target_version.get("content")
    artifact.content_json = target_version.get("content_json")
    await db.commit()
    await db.refresh(artifact)
    return await rewrite_artifact_response(db, artifact, str(request.base_url))

async def generate_single_artifact_task(artifact_id: int, exercise_index: int = None):
    from app.db.session import AsyncSessionLocal
    from app.models.session import Session
    from app.models.course import Course
    from app.models.lesson import Lesson
    from app.models.artifact import Artifact
    from sqlalchemy import select
    from app.ai_engine.agents.creator_agents import get_base_topic_key, get_base_topic_key_for_core
    from app.ai_engine.core.quiz_engine import generate_entrance_quiz, generate_exit_quiz
    from app.ai_engine.core.session_compilers import _build_session_reading_html, compile_session_mindmap_markdown
    import datetime
    import asyncio
    from pathlib import Path
    import traceback

    def log_task_error(msg: str):
        print(msg)
        traceback.print_exc()
        try:
            log_dir = Path(__file__).resolve().parents[5] / "output"
            log_dir.mkdir(parents=True, exist_ok=True)
            log_file = log_dir / "debug_regenerate.log"
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"\n--- ERROR AT {datetime.datetime.now().isoformat()} ---\n")
                f.write(f"{msg}\n")
                traceback.print_exc(file=f)
        except Exception as log_err:
            print(f"Failed to write to debug log file: {log_err}")
    
    print(f"[AI Regenerate Single] Started task for Artifact ID {artifact_id}")
    try:
        async with AsyncSessionLocal() as db:
            stmt = select(Artifact).where(Artifact.id == artifact_id)
            res = await db.execute(stmt)
            art = res.scalars().first()
            if not art:
                print(f"[Error] Artifact {artifact_id} not found")
                return
                
            session_id = art.session_id
            if not session_id:
                print(f"[Warning] Artifact {artifact_id} does not have a session_id, skipping versioned regeneration.")
                return

            result = await db.execute(select(Session).where(Session.id == session_id))
            session = result.scalars().first()
            if not session:
                print(f"[Error] Session {session_id} not found")
                return
                
            result = await db.execute(select(Course).where(Course.id == session.course_id))
            course = result.scalars().first()
            raw_tech = course.technology_stack if course else "python/fastapi"
            tech_stack = "python/core" if "python" in raw_tech.lower() and "fastapi" not in raw_tech.lower() else raw_tech

            lessons_result = await db.execute(
                select(Lesson).where(Lesson.session_id == session_id).order_by(Lesson.order_index.asc(), Lesson.id.asc())
            )
            lessons = lessons_result.scalars().all()
            lesson_ids = [l.id for l in lessons]

            is_core = "core" in tech_stack.lower()
            if is_core:
                current_topic = get_base_topic_key_for_core(session.name)
            else:
                current_topic = get_base_topic_key(session.name)

            prev_session_stmt = select(Session).where(
                Session.course_id == session.course_id,
                Session.order_index < session.order_index
            ).order_by(Session.order_index.desc())
            prev_sess_res = await db.execute(prev_session_stmt)
            prev_session = prev_sess_res.scalars().first()
            
            if prev_session:
                if is_core:
                    previous_topic = get_base_topic_key_for_core(prev_session.name)
                else:
                    previous_topic = get_base_topic_key(prev_session.name)
            else:
                previous_topic = "core_intro" if is_core else "intro"

            generated_content = None
            generated_json = None
            task_error = None
            
            if art.type == "pre_quiz":
                try:
                    pre_quiz_json = await asyncio.to_thread(generate_entrance_quiz, session.name, current_topic, previous_topic, tech_stack)
                    generated_json = {"quiz": pre_quiz_json}
                except Exception as e:
                    task_error = f"Lỗi tạo quizz đầu giờ: {str(e)}"
                    log_task_error(f"[Error] Failed to generate pre_quiz: {e}")
                    
            elif art.type == "post_quiz":
                try:
                    post_quiz_json = await asyncio.to_thread(generate_exit_quiz, session.name, current_topic, tech_stack)
                    generated_json = {"quiz": post_quiz_json}
                except Exception as e:
                    task_error = f"Lỗi tạo quizz cuối giờ: {str(e)}"
                    log_task_error(f"[Error] Failed to generate post_quiz: {e}")
                    
            elif art.type == "session_mindmap":
                if lesson_ids:
                    stmt = select(Artifact).where(Artifact.lesson_id.in_(lesson_ids), Artifact.type == "outline", Artifact.status == "Completed")
                    outline_res = await db.execute(stmt)
                    outline_arts = {o.lesson_id: o for o in outline_res.scalars().all()}
                    mindmap_md_data = []
                    for idx, lesson in enumerate(lessons, 1):
                        out_art = outline_arts.get(lesson.id)
                        if out_art and out_art.content:
                            mindmap_md_data.append({
                                "title": lesson.title,
                                "content": out_art.content
                            })
                    if mindmap_md_data:
                        try:
                            full_session_title = f"{session.name} - {session.title}"
                            generated_content = await asyncio.to_thread(compile_session_mindmap_markdown, full_session_title, mindmap_data=mindmap_md_data)
                        except Exception as e:
                            task_error = f"Lỗi compile mindmap: {str(e)}"
                            log_task_error(f"[Error] Failed to compile mindmap: {e}")
                    else:
                        task_error = "Không có outline bài học nào ở trạng thái Completed để gộp thành sơ đồ tư duy session."
                else:
                    task_error = "Không tìm thấy bài học nào trong session này."
                            
            elif art.type == "session_reading":
                if lesson_ids:
                    stmt = select(Artifact).where(Artifact.lesson_id.in_(lesson_ids), Artifact.type == "reading", Artifact.status == "Completed")
                    reading_res = await db.execute(stmt)
                    reading_arts = {r.lesson_id: r for r in reading_res.scalars().all()}
                    reading_html_data = []
                    for idx, lesson in enumerate(lessons, 1):
                        read_art = reading_arts.get(lesson.id)
                        if read_art and read_art.content:
                            reading_html_data.append({
                                "title": f"Lesson {idx:02d} - {lesson.title}",
                                "content": read_art.content
                            })
                    if reading_html_data:
                        try:
                            full_session_title = f"{session.name} - {session.title}"
                            generated_content = await asyncio.to_thread(_build_session_reading_html, full_session_title, reading_html_data, is_static=False)
                        except Exception as e:
                            task_error = f"Lỗi compile bài đọc: {str(e)}"
                            log_task_error(f"[Error] Failed to compile reading: {e}")
                    else:
                        task_error = "Không có bài đọc bài học nào ở trạng thái Completed để gộp thành bài đọc tổng hợp session."
                else:
                    task_error = "Không tìm thấy bài học nào trong session này."
                            
            elif art.type == "session_homework":
                try:
                    import sys
                    from pathlib import Path
                    root_path = Path(__file__).resolve().parents[5]
                    if str(root_path) not in sys.path:
                        sys.path.insert(0, str(root_path))
                    
                    is_practice_session = False
                    session_title_lower = session.title.lower() if session.title else ""
                    session_name_lower = session.name.lower() if session.name else ""
                    if "thực hành" in session_title_lower or "thực hành" in session_name_lower or "practice" in session_title_lower:
                        is_practice_session = True
                    
                    temp_output_dir = str(root_path / "output" / f"session_{session_id}")
                    previous_lessons_text = ", ".join([l.title for l in lessons]) if lessons else "FastAPI fundamentals"
                    
                    if is_practice_session:
                        from agents.practice_agents import regenerate_single_practice_exercise, generate_practice_session_exercises
                        if exercise_index:
                            # Regenerate ONLY a single exercise
                            current_json = art.content_json or {}
                            exercises_list = current_json.get("exercises", [])
                            
                            new_ex_data = await asyncio.to_thread(
                                regenerate_single_practice_exercise,
                                session_id=f"Session {session_id:02d}",
                                session_title=session.title,
                                session_dir_path=temp_output_dir,
                                tech_stack=tech_stack,
                                previous_lessons_text=previous_lessons_text,
                                exercise_index=exercise_index
                            )
                            
                            # Replace or append in list
                            updated = False
                            for i, ex in enumerate(exercises_list):
                                if ex.get("index") == exercise_index:
                                    exercises_list[i] = new_ex_data
                                    updated = True
                                    break
                            if not updated:
                                exercises_list.append(new_ex_data)
                            
                            # Sort by index
                            exercises_list.sort(key=lambda x: x.get("index", 0))
                            generated_json = {"exercises": exercises_list}
                        else:
                            # Full practice exercises generation
                            homework_data = await asyncio.to_thread(
                                generate_practice_session_exercises,
                                session_id=f"Session {session_id:02d}",
                                session_title=session.title,
                                session_dir_path=temp_output_dir,
                                tech_stack=tech_stack,
                                previous_lessons_text=previous_lessons_text
                            )
                            generated_json = homework_data
                    else:
                        from agents.homework_agents import generate_session_homework as gen_homework_agent
                        homework_data = await asyncio.to_thread(
                            gen_homework_agent,
                            session_id=f"Session {session_id:02d}",
                            session_title=session.title,
                            session_dir_path=temp_output_dir,
                            tech_stack=tech_stack,
                            previous_lessons_text=previous_lessons_text
                        )
                        generated_json = {"exercises": homework_data}
                except Exception as e:
                    task_error = f"Lỗi tạo bài tập: {str(e)}"
                    log_task_error(f"[Error] Failed to generate homework: {e}")

            elif art.type in ["project_entry_tests", "project_srs", "project_mini_project"]:
                try:
                    import sys
                    from pathlib import Path
                    from app.utils.artifact import get_artifact_path_context
                    root_path = Path(__file__).resolve().parents[5]
                    if str(root_path) not in sys.path:
                        sys.path.insert(0, str(root_path))
                    
                    course_dir_name, session_dir_name, _ = await get_artifact_path_context(db, lesson_id=None, session_id=session_id)
                    actual_session_dir = root_path / "output" / course_dir_name / session_dir_name

                    # Build context from previous sessions
                    prev_sessions_stmt = select(Session).where(
                        Session.course_id == session.course_id,
                        Session.order_index < session.order_index
                    ).order_by(Session.order_index.asc())
                    prev_sessions_res = await db.execute(prev_sessions_stmt)
                    prev_sessions = prev_sessions_res.scalars().all()
                    prev_session_ids = [ps.id for ps in prev_sessions]
                    
                    if prev_session_ids:
                        prev_lessons_stmt = select(Lesson).where(
                            Lesson.session_id.in_(prev_session_ids)
                        ).order_by(Lesson.session_id.asc(), Lesson.order_index.asc())
                        prev_lessons_res = await db.execute(prev_lessons_stmt)
                        prev_lessons = prev_lessons_res.scalars().all()
                        previous_lessons_text = ", ".join([l.title for l in prev_lessons])
                    else:
                        previous_lessons_text = f"{tech_stack} fundamentals"

                    if art.type == "project_entry_tests":
                        from agents.project_agents import project_entry_test_creator
                        if exercise_index:
                            test_idx = exercise_index - 1
                            new_test = await asyncio.to_thread(
                                project_entry_test_creator,
                                session_id=session.name,
                                session_title=session.title,
                                tech_stack=tech_stack,
                                previous_lessons_text=previous_lessons_text,
                                test_idx=test_idx
                            )
                            
                            current_json = art.content_json or {}
                            tests_list = current_json.get("entry_tests", [])
                            
                            updated = False
                            if len(tests_list) > test_idx:
                                tests_list[test_idx] = new_test
                                updated = True
                            if not updated:
                                tests_list.append(new_test)
                                
                            generated_json = {"entry_tests": tests_list}
                            
                            test_dir = actual_session_dir / "Bài kiểm tra đầu giờ"
                            test_dir.mkdir(parents=True, exist_ok=True)
                            from agents.project_agents import sanitize_vietnamese_filename
                            clean_name = sanitize_vietnamese_filename(new_test["title"])
                            filename = f"bai_kiem_tra_{exercise_index:02d}_{clean_name}"
                            with open(test_dir / filename, "w", encoding="utf-8") as f:
                                f.write(new_test["content"])
                        else:
                            from agents.project_agents import project_entry_test_creator
                            tests_list = []
                            test_dir = actual_session_dir / "Bài kiểm tra đầu giờ"
                            test_dir.mkdir(parents=True, exist_ok=True)
                            for idx in range(4):
                                test = await asyncio.to_thread(
                                    project_entry_test_creator,
                                    session_id=session.name,
                                    session_title=session.title,
                                    tech_stack=tech_stack,
                                    previous_lessons_text=previous_lessons_text,
                                    test_idx=idx
                                )
                                tests_list.append(test)
                                from agents.project_agents import sanitize_vietnamese_filename
                                clean_name = sanitize_vietnamese_filename(test["title"])
                                filename = f"bai_kiem_tra_{idx+1:02d}_{clean_name}"
                                with open(test_dir / filename, "w", encoding="utf-8") as f:
                                    f.write(test["content"])
                            generated_json = {"entry_tests": tests_list}

                    elif art.type == "project_srs":
                        from agents.project_agents import project_srs_creator, generate_and_link_srs_diagram
                        srs_doc = await asyncio.to_thread(
                            project_srs_creator,
                            session_id=session.name,
                            session_title=session.title,
                            tech_stack=tech_stack
                        )
                        srs_dir = actual_session_dir / "Tài liệu đặc tả SRS"
                        srs_dir.mkdir(parents=True, exist_ok=True)
                        processed_srs_content = await asyncio.to_thread(
                            generate_and_link_srs_diagram,
                            srs_doc["content"],
                            srs_dir,
                            "so_do_dac_ta_nghiep_vu"
                        )
                        with open(srs_dir / "tai_lieu_dac_ta_yeu_cau_srs.md", "w", encoding="utf-8") as f:
                            f.write(processed_srs_content)
                        generated_content = processed_srs_content
                        generated_json = {"title": srs_doc.get("title", ""), "content": processed_srs_content}

                    elif art.type == "project_mini_project":
                        from agents.project_agents import project_mini_project_creator
                        srs_title = "Enterprise Project"
                        srs_art_stmt = select(Artifact).where(Artifact.session_id == session_id, Artifact.type == "project_srs")
                        srs_art_res = await db.execute(srs_art_stmt)
                        srs_art = srs_art_res.scalars().first()
                        if srs_art and srs_art.content_json:
                            srs_title = srs_art.content_json.get("title", srs_title)
                            
                        mini_project = await asyncio.to_thread(
                            project_mini_project_creator,
                            session_id=session.name,
                            session_title=session.title,
                            tech_stack=tech_stack,
                            srs_title=srs_title
                        )
                        mp_dir = actual_session_dir / "Mini project"
                        mp_dir.mkdir(parents=True, exist_ok=True)
                        with open(mp_dir / "de_bai_mini_project.md", "w", encoding="utf-8") as f:
                            f.write(mini_project["content"])
                        with open(mp_dir / "tieu_chi_cham_diem_ai.md", "w", encoding="utf-8") as f:
                            f.write(mini_project["rubric"])
                            
                        generated_content = mini_project["content"]
                        generated_json = {
                            "title": mini_project.get("title", ""),
                            "content": mini_project.get("content", ""),
                            "rubric": mini_project.get("rubric", "")
                        }
                except Exception as e:
                    task_error = f"Lỗi tạo Project Artifact: {str(e)}"
                    log_task_error(f"[Error] Failed to generate project artifact: {e}")

            # Update database with new version
            if generated_content or generated_json:
                art.status = "Completed"
                versions = art.versions or []
                next_ver = 1
                if versions:
                    next_ver = max(v.get("version_id", 0) for v in versions) + 1
                
                new_version = {
                    "version_id": next_ver,
                    "content": generated_content,
                    "content_json": generated_json,
                    "created_at": datetime.datetime.utcnow().isoformat()
                }
                versions.append(new_version)
                if len(versions) > 3:
                    versions = versions[-3:]
                art.versions = versions
                art.content = generated_content
                art.content_json = generated_json
            else:
                art.status = "Failed"
                art.content = task_error or f"No content was generated by the AI agent for {art.type}."
                
            await db.commit()
            if art.type in ["session_mindmap", "session_reading"]:
                try:
                    from app.utils.artifact import copy_lesson_images_to_session
                    await copy_lesson_images_to_session(db, art.session_id)
                except Exception as img_err:
                    log_task_error(f"[Error] Failed to copy lesson images to session: {img_err}")
            print(f"[AI Regenerate Success] Finished regenerating single artifact {artifact_id} of type {art.type}")
    except Exception as e:
        log_task_error(f"[AI Regenerate Error] Failed to generate single artifact {artifact_id}: {e}")
        try:
            async with AsyncSessionLocal() as db:
                stmt = select(Artifact).where(Artifact.id == artifact_id)
                res = await db.execute(stmt)
                art = res.scalars().first()
                if art:
                    art.status = "Failed"
                    art.content = f"Lỗi hệ thống (System Error): {str(e)}"
                    await db.commit()
        except Exception as db_err:
            print(f"[AI Regenerate DB Error] Failed to mark artifact as Failed: {db_err}")

