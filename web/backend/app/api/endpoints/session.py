from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from app.db.session import get_db
from app.models.session import Session
from app.schemas.session import SessionResponse, SessionCreate
from app.schemas.artifact import ArtifactResponse

router = APIRouter()

def resolve_session_dir_path(root_path, course_name: str, session_name: str, session_id: int):
    from pathlib import Path
    output_dir = root_path / "output"
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
        
    course_dir = None
    normalized_course = course_name.lower().replace(" ", "_").replace("-", "_")
    for child in output_dir.iterdir():
        if child.is_dir():
            child_clean = child.name.lower().replace(" ", "_").replace("-", "_")
            if normalized_course in child_clean or child_clean in normalized_course:
                course_dir = child
                break
                
    if not course_dir:
        folder_name = course_name.replace(" ", "_").replace("-", "_")
        course_dir = output_dir / folder_name
        course_dir.mkdir(parents=True, exist_ok=True)
        
    session_dir = None
    if course_dir.exists():
        for child in course_dir.iterdir():
            if child.is_dir():
                cname = child.name.lower()
                sname_clean = session_name.lower().strip()
                if cname.startswith(sname_clean) or cname.startswith(f"session_{session_id}") or cname.startswith(str(session_id)):
                    session_dir = child
                    break
                    
    if not session_dir:
        session_dir = course_dir / session_name
        session_dir.mkdir(parents=True, exist_ok=True)
        
    return session_dir

async def generate_session_artifacts_task(session_id: int):
    from app.db.session import AsyncSessionLocal
    from app.models.session import Session
    from app.models.course import Course
    from app.models.lesson import Lesson
    from app.models.artifact import Artifact
    from sqlalchemy import select
    from app.ai_engine.agents.creator_agents import get_base_topic_key, get_base_topic_key_for_core
    from app.ai_engine.core.quiz_engine import generate_entrance_quiz, generate_exit_quiz
    from app.ai_engine.core.session_compilers import _build_session_reading_html, compile_session_mindmap_markdown
    import re
    import json
    import asyncio
    import datetime

    print(f"[AI Session Trigger] Start processing session-level artifacts for Session ID {session_id}")
    
    try:
        async with AsyncSessionLocal() as db:
            # Fetch the session along with its course and lessons
            result = await db.execute(select(Session).where(Session.id == session_id))
            session = result.scalars().first()
            if not session:
                print(f"[Error] Session {session_id} not found")
                return
                
            # Fetch all artifacts for this session to check status
            art_stmt = select(Artifact).where(Artifact.session_id == session_id)
            art_res = await db.execute(art_stmt)
            artifacts_map = {art.type: art for art in art_res.scalars().all()}
            
            result = await db.execute(select(Course).where(Course.id == session.course_id))
            course = result.scalars().first()
            raw_tech = course.technology_stack if course else "python/fastapi"
            tech_stack = "python/core" if "python" in raw_tech.lower() and "fastapi" not in raw_tech.lower() else raw_tech
            
            # Determine if it's a practice session vs theory session
            is_practice_session = False
            session_title_lower = session.title.lower() if session.title else ""
            session_name_lower = session.name.lower() if session.name else ""
            if "thực hành" in session_title_lower or "thực hành" in session_name_lower or "practice" in session_title_lower:
                is_practice_session = True
                
            if is_practice_session:
                from sqlalchemy import delete
                await db.execute(
                    delete(Artifact).where(
                        Artifact.session_id == session_id,
                        Artifact.type != "session_homework"
                    )
                )
                await db.commit()
                # Re-fetch artifacts
                art_stmt = select(Artifact).where(Artifact.session_id == session_id)
                art_res = await db.execute(art_stmt)
                artifacts_map = {art.type: art for art in art_res.scalars().all()}
                
                # Ensure session_homework is present
                if "session_homework" not in artifacts_map:
                    art = Artifact(session_id=session_id, type="session_homework", status="Pending")
                    db.add(art)
                    await db.commit()
                    # Re-fetch
                    art_stmt = select(Artifact).where(Artifact.session_id == session_id)
                    art_res = await db.execute(art_stmt)
                    artifacts_map = {art.type: art for art in art_res.scalars().all()}
            
            # Gather completed lesson artifacts of this session for merging if mindmap/reading is pending
            lessons = []
            reading_html_data = []
            mindmap_md_data = []
            
            need_reading = "session_reading" in artifacts_map and artifacts_map["session_reading"].status == "Pending"
            need_mindmap = "session_mindmap" in artifacts_map and artifacts_map["session_mindmap"].status == "Pending"
            
            if need_reading or need_mindmap:
                lessons_result = await db.execute(
                    select(Lesson).where(Lesson.session_id == session_id).order_by(Lesson.order_index.asc(), Lesson.id.asc())
                )
                lessons = lessons_result.scalars().all()
                lesson_ids = [l.id for l in lessons]
                
                if lesson_ids:
                    # Fetch all completed reading artifacts
                    stmt = select(Artifact).where(Artifact.lesson_id.in_(lesson_ids), Artifact.type == "reading", Artifact.status == "Completed")
                    reading_res = await db.execute(stmt)
                    reading_arts = {art.lesson_id: art for art in reading_res.scalars().all()}
                    
                    # Fetch all completed outline (mindmap) artifacts
                    stmt = select(Artifact).where(Artifact.lesson_id.in_(lesson_ids), Artifact.type == "outline", Artifact.status == "Completed")
                    outline_res = await db.execute(stmt)
                    outline_arts = {art.lesson_id: art for art in outline_res.scalars().all()}
                    
                    for idx, lesson in enumerate(lessons, 1):
                        read_art = reading_arts.get(lesson.id)
                        out_art = outline_arts.get(lesson.id)
                        
                        if read_art and read_art.content:
                            reading_html_data.append({
                                "title": f"Lesson {idx:02d} - {lesson.title}",
                                "content": read_art.content
                            })
                        if out_art and out_art.content:
                            mindmap_md_data.append({
                                "title": lesson.title,
                                "content": out_art.content
                            })

            compiled_reading_content = None
            if need_reading and reading_html_data:
                try:
                    full_session_title = f"{session.name} - {session.title}"
                    compiled_reading_content = await asyncio.to_thread(_build_session_reading_html, full_session_title, reading_html_data, is_static=False)
                except Exception as e:
                    print(f"[Error] Failed to compile session HTML reading: {e}")

            compiled_mindmap_content = None
            if need_mindmap and mindmap_md_data:
                try:
                    full_session_title = f"{session.name} - {session.title}"
                    compiled_mindmap_content = await asyncio.to_thread(compile_session_mindmap_markdown, full_session_title, mindmap_data=mindmap_md_data)
                except Exception as e:
                    print(f"[Error] Failed to compile session mindmap: {e}")

            # Determine current and previous topic key
            is_core = "core" in tech_stack.lower()
            if is_core:
                current_topic = get_base_topic_key_for_core(session.name)
            else:
                current_topic = get_base_topic_key(session.name)
                
            # Determine previous session in the same course
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

            # Generate Entrance and Exit Quizzes only if pending
            pre_quiz_json = None
            if "pre_quiz" in artifacts_map and artifacts_map["pre_quiz"].status == "Pending":
                try:
                    pre_quiz_json = await asyncio.to_thread(generate_entrance_quiz, session.name, current_topic, previous_topic, tech_stack)
                except Exception as e:
                    print(f"[Error] Failed to generate pre_quiz: {e}")
                
            post_quiz_json = None
            if "post_quiz" in artifacts_map and artifacts_map["post_quiz"].status == "Pending":
                try:
                    post_quiz_json = await asyncio.to_thread(generate_exit_quiz, session.name, current_topic, tech_stack)
                except Exception as e:
                    print(f"[Error] Failed to generate post_quiz: {e}")

            # Generate Session Homework only if pending
            session_homework_json = None
            if "session_homework" in artifacts_map and artifacts_map["session_homework"].status == "Pending":
                try:
                    import sys
                    from pathlib import Path
                    root_path = Path(__file__).resolve().parents[5]
                    if str(root_path) not in sys.path:
                        sys.path.insert(0, str(root_path))
                    
                    # Reconfigure encoding for Windows console compatibility
                    if sys.platform.startswith('win'):
                        try:
                            sys.stdout.reconfigure(encoding='utf-8')
                            sys.stderr.reconfigure(encoding='utf-8')
                        except Exception:
                            pass

                    # Determine if it's a practice session vs theory session
                    is_practice_session = False
                    session_title_lower = session.title.lower() if session.title else ""
                    session_name_lower = session.name.lower() if session.name else ""
                    if "thực hành" in session_title_lower or "thực hành" in session_name_lower or "practice" in session_title_lower:
                        is_practice_session = True

                    # Resolve the actual session directory path on disk
                    actual_session_dir = resolve_session_dir_path(root_path, course.name, session.name, session.id)

                    if is_practice_session:
                        # Get previous sessions in the same course to build context
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
                    else:
                        if not lessons:
                            lessons_result = await db.execute(
                                select(Lesson).where(Lesson.session_id == session_id).order_by(Lesson.order_index.asc(), Lesson.id.asc())
                            )
                            lessons = lessons_result.scalars().all()
                        previous_lessons_text = ", ".join([l.title for l in lessons]) if lessons else "FastAPI fundamentals"
                    
                    if is_practice_session:
                        print(f"  [AI Session] Triggering PRACTICE exercises generation for Session {session_id}")
                        from agents.practice_agents import generate_practice_session_exercises as gen_practice_agent
                        homework_data = await asyncio.to_thread(
                            gen_practice_agent,
                            session_id=session.name,
                            session_title=session.title,
                            session_dir_path=str(actual_session_dir),
                            tech_stack=tech_stack,
                            previous_lessons_text=previous_lessons_text
                        )
                    else:
                        print(f"  [AI Session] Triggering THEORY homework generation for Session {session_id}")
                        from agents.homework_agents import generate_session_homework as gen_homework_agent
                        homework_data = await asyncio.to_thread(
                            gen_homework_agent,
                            session_id=session.name,
                            session_title=session.title,
                            session_dir_path=str(actual_session_dir),
                            tech_stack=tech_stack,
                            previous_lessons_text=previous_lessons_text
                        )
                    
                    if isinstance(homework_data, dict) and "exercises" in homework_data:
                        session_homework_json = homework_data["exercises"]
                    else:
                        session_homework_json = homework_data
                except Exception as e:
                    print(f"[Error] Failed to generate session homework/practice: {e}")

            # Helper to append version
            def add_artifact_version(art, content, content_json):
                versions = art.versions or []
                next_ver = 1
                if versions:
                    next_ver = max(v.get("version_id", 0) for v in versions) + 1
                
                new_version = {
                    "version_id": next_ver,
                    "content": content,
                    "content_json": content_json,
                    "created_at": datetime.datetime.utcnow().isoformat()
                }
                versions.append(new_version)
                if len(versions) > 3:
                    versions = versions[-3:]
                art.versions = versions
                art.content = content
                art.content_json = content_json

            # Update database records
            # pre_quiz
            art = artifacts_map.get("pre_quiz")
            if art and art.status == "Pending":
                if pre_quiz_json:
                    art.status = "Completed"
                    add_artifact_version(art, None, {"quiz": pre_quiz_json})
                else:
                    art.status = "Failed"
                    
            # post_quiz
            art = artifacts_map.get("post_quiz")
            if art and art.status == "Pending":
                if post_quiz_json:
                    art.status = "Completed"
                    add_artifact_version(art, None, {"quiz": post_quiz_json})
                else:
                    art.status = "Failed"
                    
            # session_mindmap
            art = artifacts_map.get("session_mindmap")
            if art and art.status == "Pending":
                if compiled_mindmap_content:
                    art.status = "Completed"
                    add_artifact_version(art, compiled_mindmap_content, None)
                else:
                    art.status = "Failed"
                    
            # session_reading
            art = artifacts_map.get("session_reading")
            if art and art.status == "Pending":
                if compiled_reading_content:
                    art.status = "Completed"
                    add_artifact_version(art, compiled_reading_content, None)
                else:
                    art.status = "Failed"
                    
            # session_homework
            art = artifacts_map.get("session_homework")
            if art and art.status == "Pending":
                if session_homework_json:
                    art.status = "Completed"
                    add_artifact_version(art, None, {"exercises": session_homework_json})
                else:
                    art.status = "Failed"
                    
            await db.commit()
            try:
                from app.utils.artifact import copy_lesson_images_to_session
                await copy_lesson_images_to_session(db, session_id)
            except Exception as img_err:
                print(f"[Error] Failed to copy lesson images to session: {img_err}")
            print(f"[AI Session Success] Finished generating session-level artifacts for Session ID {session_id}")
    except Exception as e:
        print(f"[AI Session Error] Failed to generate session artifacts: {e}")
        try:
            async with AsyncSessionLocal() as db:
                stmt = select(Artifact).where(Artifact.session_id == session_id, Artifact.status == "Pending")
                res = await db.execute(stmt)
                for art in res.scalars().all():
                    art.status = "Failed"
                await db.commit()
        except Exception as db_err:
            print(f"[AI Session DB Error] Failed to mark artifacts as Failed: {db_err}")
async def generate_project_session_task(session_id: int):
    from app.db.session import AsyncSessionLocal
    from app.models.session import Session
    from app.models.course import Course
    from app.models.lesson import Lesson
    from app.models.artifact import Artifact
    from sqlalchemy import select, delete
    import asyncio
    import datetime
    import sys
    from pathlib import Path
    from app.utils.artifact import get_artifact_path_context

    print(f"[AI Project Session Trigger] Start generating project for Session ID {session_id}")
    project_types = ["project_entry_tests", "project_srs", "project_mini_project"]
    
    try:
        async with AsyncSessionLocal() as db:
            session = await db.get(Session, session_id)
            if not session:
                print(f"[Error] Session {session_id} not found")
                return

            # Clean up other artifacts
            await db.execute(
                delete(Artifact).where(
                    Artifact.session_id == session_id,
                    Artifact.type.notin_(project_types)
                )
            )
            
            # Fetch or create project artifacts
            artifacts_map = {}
            for art_type in project_types:
                stmt = select(Artifact).where(Artifact.session_id == session_id, Artifact.type == art_type)
                res = await db.execute(stmt)
                art = res.scalars().first()
                if not art:
                    art = Artifact(session_id=session_id, type=art_type, status="Pending")
                    db.add(art)
                else:
                    art.status = "Pending"
                    art.content = None
                    art.content_json = None
                artifacts_map[art_type] = art
            await db.commit()
            
            # Refresh all artifacts to make sure they are attached to session
            for art_type in project_types:
                await db.refresh(artifacts_map[art_type])

            # Get Course Info
            course = await db.get(Course, session.course_id)
            raw_tech = course.technology_stack if course else "python/fastapi"
            tech_stack = "python/core" if "python" in raw_tech.lower() and "fastapi" not in raw_tech.lower() else raw_tech

            # Resolve the actual session directory path on disk
            root_path = Path(__file__).resolve().parents[5]
            if str(root_path) not in sys.path:
                sys.path.insert(0, str(root_path))
            
            # Reconfigure encoding for Windows console compatibility
            if sys.platform.startswith('win'):
                try:
                    sys.stdout.reconfigure(encoding='utf-8')
                    sys.stderr.reconfigure(encoding='utf-8')
                except Exception:
                    pass

            course_dir_name, session_dir_name, _ = await get_artifact_path_context(db, lesson_id=None, session_id=session_id)
            actual_session_dir = root_path / "output" / course_dir_name / session_dir_name

            # Query all lessons of previous sessions in the same course to build context
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

            print(f"  [AI Session] Triggering Project generation for Session {session_id}")
            from agents.project_agents import generate_mini_project_session
            
            project_data = await asyncio.to_thread(
                generate_mini_project_session,
                session_id=session.name,
                session_title=session.title,
                session_dir_path=str(actual_session_dir),
                tech_stack=tech_stack,
                previous_lessons_text=previous_lessons_text
            )

            # Process and update project artifacts
            entry_tests = project_data.get("entry_tests", [])
            srs = project_data.get("srs", {})
            mini_project = project_data.get("mini_project", {})

            def add_version(art, content, content_json):
                versions = art.versions or []
                next_ver = 1
                if versions:
                    next_ver = max(v.get("version_id", 0) for v in versions) + 1
                
                new_version = {
                    "version_id": next_ver,
                    "content": content,
                    "content_json": content_json,
                    "created_at": datetime.datetime.utcnow().isoformat()
                }
                versions.append(new_version)
                if len(versions) > 3:
                    versions = versions[-3:]
                art.versions = versions
                art.content = content
                art.content_json = content_json
                art.status = "Completed"

            if entry_tests:
                add_version(artifacts_map["project_entry_tests"], None, {"entry_tests": entry_tests})
            else:
                artifacts_map["project_entry_tests"].status = "Failed"

            if srs:
                srs_file_path = actual_session_dir / "Tài liệu đặc tả SRS" / "tai_lieu_dac_ta_yeu_cau_srs.md"
                srs_markdown = srs.get("content", "")
                if srs_file_path.exists():
                    try:
                        srs_markdown = srs_file_path.read_text(encoding="utf-8")
                    except Exception:
                        pass
                add_version(artifacts_map["project_srs"], srs_markdown, {"title": srs.get("title", ""), "content": srs_markdown})
            else:
                artifacts_map["project_srs"].status = "Failed"

            if mini_project:
                add_version(artifacts_map["project_mini_project"], mini_project.get("content", ""), {
                    "title": mini_project.get("title", ""),
                    "content": mini_project.get("content", ""),
                    "rubric": mini_project.get("rubric", "")
                })
            else:
                artifacts_map["project_mini_project"].status = "Failed"

            await db.commit()
            print(f"[AI Project Session Success] Finished generating project for Session ID {session_id}")
            
    except Exception as e:
        print(f"[AI Project Session Error] Failed to generate project session: {e}")
        try:
            async with AsyncSessionLocal() as db:
                stmt = select(Artifact).where(Artifact.session_id == session_id, Artifact.type.in_(project_types))
                res = await db.execute(stmt)
                for art in res.scalars().all():
                    if art.status == "Pending":
                        art.status = "Failed"
                await db.commit()
        except Exception as db_err:
            print(f"[AI Project Session DB Error] Failed to mark artifact as Failed: {db_err}")

async def generate_practice_session_task(session_id: int):
    from app.db.session import AsyncSessionLocal
    from app.models.session import Session
    from app.models.course import Course
    from app.models.lesson import Lesson
    from app.models.artifact import Artifact
    from sqlalchemy import select, delete
    import asyncio
    import datetime
    import sys
    from pathlib import Path
    from app.utils.artifact import get_artifact_path_context

    print(f"[AI Practice Session Trigger] Start generating exercises for Session ID {session_id}")
    
    try:
        async with AsyncSessionLocal() as db:
            session = await db.get(Session, session_id)
            if not session:
                print(f"[Error] Session {session_id} not found")
                return

            # Clean up any non-practice artifacts for this session
            await db.execute(
                delete(Artifact).where(
                    Artifact.session_id == session_id,
                    Artifact.type != "session_homework"
                )
            )
            
            # Fetch or create the session_homework artifact
            stmt = select(Artifact).where(Artifact.session_id == session_id, Artifact.type == "session_homework")
            res = await db.execute(stmt)
            art = res.scalars().first()
            if not art:
                art = Artifact(session_id=session_id, type="session_homework", status="Pending")
                db.add(art)
            else:
                art.status = "Pending"
                art.content = None
                art.content_json = None
            await db.commit()
            await db.refresh(art)

            # Get Course Info
            course = await db.get(Course, session.course_id)
            raw_tech = course.technology_stack if course else "python/fastapi"
            tech_stack = "python/core" if "python" in raw_tech.lower() and "fastapi" not in raw_tech.lower() else raw_tech

            # Resolve the actual session directory path on disk
            root_path = Path(__file__).resolve().parents[5]
            if str(root_path) not in sys.path:
                sys.path.insert(0, str(root_path))
            
            # Reconfigure encoding for Windows console compatibility
            if sys.platform.startswith('win'):
                try:
                    sys.stdout.reconfigure(encoding='utf-8')
                    sys.stderr.reconfigure(encoding='utf-8')
                except Exception:
                    pass

            course_dir_name, session_dir_name, _ = await get_artifact_path_context(db, lesson_id=None, session_id=session_id)
            actual_session_dir = root_path / "output" / course_dir_name / session_dir_name

            # Query all lessons of previous sessions in the same course to build context
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

            print(f"  [AI Session] Triggering PRACTICE exercises generation for Session {session_id}")
            from agents.practice_agents import generate_practice_session_exercises as gen_practice_agent
            homework_data = await asyncio.to_thread(
                gen_practice_agent,
                session_id=session.name,
                session_title=session.title,
                session_dir_path=str(actual_session_dir),
                tech_stack=tech_stack,
                previous_lessons_text=previous_lessons_text
            )

            session_homework_json = None
            if isinstance(homework_data, dict) and "exercises" in homework_data:
                session_homework_json = homework_data["exercises"]
            else:
                session_homework_json = homework_data

            if session_homework_json:
                art.status = "Completed"
                
                # Helper to append version
                versions = art.versions or []
                next_ver = 1
                if versions:
                    next_ver = max(v.get("version_id", 0) for v in versions) + 1
                
                new_version = {
                    "version_id": next_ver,
                    "content": None,
                    "content_json": {"exercises": session_homework_json},
                    "created_at": datetime.datetime.utcnow().isoformat()
                }
                versions.append(new_version)
                if len(versions) > 3:
                    versions = versions[-3:]
                art.versions = versions
                art.content = None
                art.content_json = {"exercises": session_homework_json}
            else:
                art.status = "Failed"

            await db.commit()
            print(f"[AI Practice Session Success] Finished generating exercises for Session ID {session_id}")
            
    except Exception as e:
        print(f"[AI Practice Session Error] Failed to generate practice session exercises: {e}")
        try:
            async with AsyncSessionLocal() as db:
                stmt = select(Artifact).where(Artifact.session_id == session_id, Artifact.type == "session_homework")
                res = await db.execute(stmt)
                art = res.scalars().first()
                if art:
                    art.status = "Failed"
                    await db.commit()
        except Exception as db_err:
            print(f"[AI Practice Session DB Error] Failed to mark artifact as Failed: {db_err}")

@router.get("/", response_model=List[SessionResponse])
async def get_sessions(course_id: Optional[int] = None, db: AsyncSession = Depends(get_db)):
    query = select(Session).order_by(Session.order_index.asc(), Session.id.asc())
    if course_id:
        query = query.where(Session.course_id == course_id)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/", response_model=SessionResponse)
async def create_session(session_in: SessionCreate, db: AsyncSession = Depends(get_db)):
    query = select(Session.order_index).where(Session.course_id == session_in.course_id).order_by(Session.order_index.desc())
    res = await db.execute(query)
    max_order = res.scalars().first()
    next_order = (max_order or 0) + 1
    
    new_session = Session(**session_in.model_dump(), order_index=next_order)
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    return new_session

from pydantic import BaseModel

class ReorderPayload(BaseModel):
    item_ids: List[int]

@router.put("/reorder")
async def reorder_sessions(payload: ReorderPayload, db: AsyncSession = Depends(get_db)):
    for idx, s_id in enumerate(payload.item_ids):
        sess = await db.get(Session, s_id)
        if sess:
            sess.order_index = idx
    await db.commit()
    return {"status": "success"}

@router.delete("/{session_id}")
async def delete_session(session_id: int, db: AsyncSession = Depends(get_db)):
    sess = await db.get(Session, session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found")
        
    from app.models.lesson import Lesson
    from app.models.artifact import Artifact
    from sqlalchemy import delete
    
    lessons = await db.execute(select(Lesson).where(Lesson.session_id == session_id))
    lesson_ids = [l.id for l in lessons.scalars().all()]
    if lesson_ids:
        await db.execute(delete(Artifact).where(Artifact.lesson_id.in_(lesson_ids)))
        await db.execute(delete(Lesson).where(Lesson.session_id == session_id))
        
    # Also delete session-level artifacts
    await db.execute(delete(Artifact).where(Artifact.session_id == session_id))
        
    await db.delete(sess)
    await db.commit()
    return {"status": "success"}

@router.post("/{session_id}/generate")
async def generate_session_artifacts(
    session_id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    sess = await db.get(Session, session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found")
        
    from app.models.artifact import Artifact
    from sqlalchemy import delete
    
    is_practice_session = False
    is_project_session = False
    session_title_lower = sess.title.lower() if sess.title else ""
    session_name_lower = sess.name.lower() if sess.name else ""
    if "thực hành" in session_title_lower or "thực hành" in session_name_lower or "practice" in session_title_lower:
        is_practice_session = True
    elif "mini project" in session_title_lower or "mini project" in session_name_lower or "dự án" in session_title_lower or "dự án" in session_name_lower or "project" in session_title_lower or "project" in session_name_lower:
        is_project_session = True
        
    if is_practice_session:
        # Delete any other artifacts to keep only session_homework
        await db.execute(
            delete(Artifact).where(
                Artifact.session_id == session_id,
                Artifact.type != "session_homework"
            )
        )
        await db.commit()
        artifact_types = ["session_homework"]
    elif is_project_session:
        project_types = ["project_entry_tests", "project_srs", "project_mini_project"]
        await db.execute(
            delete(Artifact).where(
                Artifact.session_id == session_id,
                Artifact.type.notin_(project_types)
            )
        )
        await db.commit()
        artifact_types = project_types
    else:
        artifact_types = ["pre_quiz", "post_quiz", "session_mindmap", "session_reading", "session_homework"]
        
    has_pending = False
    for art_type in artifact_types:
        stmt = select(Artifact).where(Artifact.session_id == session_id, Artifact.type == art_type)
        res = await db.execute(stmt)
        art = res.scalars().first()
        if not art:
            art = Artifact(session_id=session_id, type=art_type, status="Pending")
            db.add(art)
            has_pending = True
        elif art.status != "Completed":
            art.status = "Pending"
            art.content = None
            art.content_json = None
            has_pending = True
    await db.commit()
    
    if has_pending:
        if is_project_session:
            background_tasks.add_task(generate_project_session_task, session_id)
        elif is_practice_session:
            background_tasks.add_task(generate_practice_session_task, session_id)
        else:
            background_tasks.add_task(generate_session_artifacts_task, session_id)
        return {"status": "success", "message": "Session artifacts generation triggered"}
    else:
        return {"status": "success", "message": "All artifacts are already completed, skipping generation"}

@router.post("/{session_id}/generate-practice")
async def generate_practice_session_artifacts(
    session_id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    sess = await db.get(Session, session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found")
        
    from app.models.artifact import Artifact
    from sqlalchemy import delete
    
    # Force practice session: clean up other artifacts, keep only session_homework
    await db.execute(
        delete(Artifact).where(
            Artifact.session_id == session_id,
            Artifact.type != "session_homework"
        )
    )
    await db.commit()
    
    # Ensure session_homework is Pending
    stmt = select(Artifact).where(Artifact.session_id == session_id, Artifact.type == "session_homework")
    res = await db.execute(stmt)
    art = res.scalars().first()
    if not art:
        art = Artifact(session_id=session_id, type="session_homework", status="Pending")
        db.add(art)
    else:
        art.status = "Pending"
        art.content = None
        art.content_json = None
    await db.commit()
    
    background_tasks.add_task(generate_practice_session_task, session_id)
    return {"status": "success", "message": "Practice session exercises generation triggered"}

@router.post("/{session_id}/generate-project")
async def generate_project_session_artifacts(
    session_id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    sess = await db.get(Session, session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found")
        
    from app.models.artifact import Artifact
    from sqlalchemy import delete
    
    project_types = ["project_entry_tests", "project_srs", "project_mini_project"]
    await db.execute(
        delete(Artifact).where(
            Artifact.session_id == session_id,
            Artifact.type.notin_(project_types)
        )
    )
    await db.commit()
    
    for art_type in project_types:
        stmt = select(Artifact).where(Artifact.session_id == session_id, Artifact.type == art_type)
        res = await db.execute(stmt)
        art = res.scalars().first()
        if not art:
            art = Artifact(session_id=session_id, type=art_type, status="Pending")
            db.add(art)
        else:
            art.status = "Pending"
            art.content = None
            art.content_json = None
    await db.commit()
    
    background_tasks.add_task(generate_project_session_task, session_id)
    return {"status": "success", "message": "Mini Project generation triggered"}

@router.get("/{session_id}/artifacts", response_model=List[ArtifactResponse])
async def get_session_artifacts(session_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    from app.models.artifact import Artifact
    from app.utils.artifact import rewrite_artifacts_list
    stmt = select(Artifact).where(Artifact.session_id == session_id)
    res = await db.execute(stmt)
    artifacts = res.scalars().all()
    return await rewrite_artifacts_list(db, artifacts, str(request.base_url))
