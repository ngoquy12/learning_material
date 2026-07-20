from pathlib import Path
import re
import urllib.parse
from typing import List, Dict, Any, Optional, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.lesson import Lesson
from app.models.session import Session
from app.models.course import Course
from app.schemas.artifact import ArtifactResponse

def sanitize_folder_name(name: str) -> str:
    """Loại bỏ các ký tự không hợp lệ cho tên thư mục trên mọi hệ điều hành và an toàn cho URL."""
    name = name.replace("&", "va").replace("%", "").replace("^", "").replace("#", "")
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()

def resolve_physical_paths(course_dir, session_name: str, session_id: int, lesson_name: str, lesson_id: int):
    """
    Scans course directory to find subdirectories starting with session_name/session_id
    and lesson_name/lesson_id to support custom suffix patterns on disk (e.g. 'Session 02 -').
    Prioritizes human-readable prefix matching over numeric ID matching.
    """
    from pathlib import Path
    course_path = Path(course_dir)
    
    session_dir_name = None
    if course_path.exists():
        # Pass 1: Prioritize human-readable prefix (e.g. 'session 02')
        prefix1 = session_name.lower()
        for item in course_path.iterdir():
            if item.is_dir():
                if item.name.lower().startswith(prefix1):
                    session_dir_name = item.name
                    break
                    
        # Pass 2: Fall back to numeric ID prefix (e.g. '94')
        if not session_dir_name:
            prefix2 = f"{session_id}"
            for item in course_path.iterdir():
                if item.is_dir():
                    if item.name.lower().startswith(prefix2):
                        session_dir_name = item.name
                        break
                        
    if not session_dir_name:
        session_dir_name = sanitize_folder_name(session_name)
        
    session_path = course_path / session_dir_name
    
    lesson_dir_name = None
    if session_path.exists():
        # Pass 1: Prioritize human-readable prefix (e.g. 'lesson 01')
        prefix1 = lesson_name.lower()
        for item in session_path.iterdir():
            if item.is_dir():
                if item.name.lower().startswith(prefix1):
                    lesson_dir_name = item.name
                    break
                    
        # Pass 2: Fall back to numeric ID prefix (e.g. '99')
        if not lesson_dir_name:
            prefix2 = f"{lesson_id}"
            for item in session_path.iterdir():
                if item.is_dir():
                    if item.name.lower().startswith(prefix2):
                        lesson_dir_name = item.name
                        break
                        
    if not lesson_dir_name:
        lesson_dir_name = sanitize_folder_name(lesson_name)
        
    return session_dir_name, lesson_dir_name

async def get_artifact_path_context(db: AsyncSession, lesson_id: Optional[int], session_id: Optional[int]):
    """
    Returns (course_dir_name, session_dir_name, lesson_dir_name) by querying DB and scanning disk.
    """
    import os
    from pathlib import Path
    
    course_dir_name = "Database_Course"
    session_dir_name = "Session 01"
    lesson_dir_name = "Lesson 01"
    
    db_lesson: Any = None
    db_session: Any = None
    db_course: Any = None
    
    if lesson_id:
        res = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
        db_lesson = res.scalars().first()
        if db_lesson:
            res = await db.execute(select(Session).where(Session.id == db_lesson.session_id))
            db_session = res.scalars().first()
    elif session_id:
        res = await db.execute(select(Session).where(Session.id == session_id))
        db_session = res.scalars().first()
        
    if db_session:
        res = await db.execute(select(Course).where(Course.id == db_session.course_id))
        db_course = res.scalars().first()
        
    if db_course:
        # Try both formats: replace space/dash with underscore, and sanitized
        name_opts = [
            db_course.name.strip().replace(" ", "_").replace("-", "_"),
            sanitize_folder_name(db_course.name)
        ]
        
        # Resolve project root base path
        current_file = Path(__file__).resolve()
        output_path = current_file.parents[4] / "output"
        
        course_dir_name = None
        if output_path.exists():
            for opt in name_opts:
                opt_sanitized = sanitize_folder_name(opt)
                if (output_path / opt_sanitized).exists():
                    course_dir_name = opt_sanitized
                    break
            
            # If still not found, try case-insensitive or prefix matching in output directory
            if not course_dir_name:
                for item in output_path.iterdir():
                    if item.is_dir():
                        item_name_lower = item.name.lower()
                        # check if matches or contains course ID/name
                        cleaned_db_name = re.sub(r'\W+', '', db_course.name.lower())
                        cleaned_item_name = re.sub(r'\W+', '', item.name.lower())
                        if cleaned_db_name == cleaned_item_name or db_course.name.lower() in item_name_lower:
                            course_dir_name = item.name
                            break
                            
        if not course_dir_name:
            course_dir_name = name_opts[0]
            
        course_path = output_path / course_dir_name
        
        s_name = db_session.name or f"Session {db_session.id}"
        s_id = db_session.id
        
        l_name = db_lesson.name or f"Lesson {db_lesson.id}" if db_lesson else ""
        l_id = db_lesson.id if db_lesson else 0
        
        s_dir, l_dir = resolve_physical_paths(course_path, s_name, s_id, l_name, l_id)
        session_dir_name = s_dir
        if db_lesson:
            lesson_dir_name = l_dir
            
    return course_dir_name, session_dir_name, lesson_dir_name

def rewrite_artifact_content_urls(
    content: str,
    course_dir_name: str,
    session_dir_name: str,
    lesson_dir_name: str,
    lesson_id: Optional[int],
    request_base_url: str
) -> str:
    if not content:
        return content
        
    if not request_base_url.endswith("/"):
        request_base_url += "/"
        
    # 1. Replace resources path matching both forward and backslashes case-insensitively
    content = re.sub(r'(?:\.\.[/\\])*resources[/\\]', f"{request_base_url}resources/", content, flags=re.IGNORECASE)
    
    # 2. Replace images path matching both forward and backslashes case-insensitively
    course_quoted = urllib.parse.quote(course_dir_name)
    session_quoted = urllib.parse.quote(session_dir_name)
    lesson_quoted = urllib.parse.quote(lesson_dir_name)
    
    if lesson_id:
        images_base_url = f"{request_base_url}static/{course_quoted}/{session_quoted}/{lesson_quoted}/images/"
    else:
        images_base_url = f"{request_base_url}static/{course_quoted}/{session_quoted}/images/"
        
    content = re.sub(r'(?:\.\.[/\\])*images[/\\]', images_base_url, content, flags=re.IGNORECASE)
    
    return content

def rewrite_json_urls(
    val,
    course_dir_name: str,
    session_dir_name: str,
    lesson_dir_name: str,
    lesson_id: Optional[int],
    request_base_url: str
):
    if isinstance(val, str):
        return rewrite_artifact_content_urls(val, course_dir_name, session_dir_name, lesson_dir_name, lesson_id, request_base_url)
    elif isinstance(val, dict):
        return {k: rewrite_json_urls(v, course_dir_name, session_dir_name, lesson_dir_name, lesson_id, request_base_url) for k, v in val.items()}
    elif isinstance(val, list):
        return [rewrite_json_urls(item, course_dir_name, session_dir_name, lesson_dir_name, lesson_id, request_base_url) for item in val]
    return val

async def rewrite_artifact_response(
    db: AsyncSession,
    artifact,
    request_base_url: str
) -> ArtifactResponse:
    course_dir, session_dir, lesson_dir = await get_artifact_path_context(db, artifact.lesson_id, artifact.session_id)
    
    schema_art = ArtifactResponse.model_validate(artifact)
    
    if schema_art.content:
        schema_art.content = rewrite_artifact_content_urls(
            schema_art.content, course_dir, session_dir, lesson_dir, artifact.lesson_id, request_base_url
        )
    if schema_art.content_json:
        schema_art.content_json = rewrite_json_urls(  # type: ignore
            schema_art.content_json, course_dir, session_dir, lesson_dir, artifact.lesson_id, request_base_url
        )
        
    return schema_art

async def rewrite_artifacts_list(
    db: AsyncSession,
    artifacts: List[Any],
    request_base_url: str
) -> List[ArtifactResponse]:
    return [await rewrite_artifact_response(db, art, request_base_url) for art in artifacts]


async def copy_lesson_images_to_session(db: AsyncSession, session_id: int):
    """
    Copies all images from the lessons of the session to the session-level images directory.
    """
    import shutil
    from pathlib import Path
    
    # 1. Get Course and Session path context
    course_dir, session_dir, _ = await get_artifact_path_context(db, lesson_id=None, session_id=session_id)
    
    current_file = Path(__file__).resolve()
    # current_file is web/backend/app/utils/artifact.py
    # parents[3] is web/backend
    # project_root is Learning-Material
    project_root = current_file.parents[4]
    output_path = project_root / "output"
    
    session_path = output_path / course_dir / session_dir
    session_images_dir = session_path / "images"
    
    # 2. Get lessons for the session
    res = await db.execute(select(Lesson).where(Lesson.session_id == session_id))
    lessons = res.scalars().all()
    
    # 3. For each lesson, check if it has images folder, and copy its contents
    for lesson in lessons:
        try:
            lesson_id: Any = lesson.id
            _, _, lesson_dir = await get_artifact_path_context(db, lesson_id=lesson_id, session_id=session_id)
            lesson_images_dir = session_path / lesson_dir / "images"
            if lesson_images_dir.exists() and lesson_images_dir.is_dir():
                if not session_images_dir.exists():
                    session_images_dir.mkdir(parents=True, exist_ok=True)
                for item in lesson_images_dir.iterdir():
                    if item.is_file():
                        # Prevent self-copying if session_images_dir is somehow the same
                        dest_file = session_images_dir / item.name
                        if dest_file != item:
                            shutil.copy2(item, dest_file)
        except Exception as e:
            print(f"[Warning] Failed to copy images for lesson {lesson.id}: {e}")


async def write_artifact_to_disk(db: AsyncSession, artifact) -> None:
    """
    Writes the content or content_json of the artifact to its physical file location on disk.
    Supports both lesson-level and session-level artifacts.
    """
    import json
    from pathlib import Path

    try:
        # 1. Resolve path context (course_dir, session_dir, lesson_dir)
        course_dir, session_dir, lesson_dir = await get_artifact_path_context(db, artifact.lesson_id, artifact.session_id)
        
        current_file = Path(__file__).resolve()
        # current_file is web/backend/app/utils/artifact.py
        # parents[4] is the Learning-Material root directory
        project_root = current_file.parents[4]
        output_path = project_root / "output"
        
        if artifact.lesson_id:
            target_dir = output_path / course_dir / session_dir / lesson_dir
        else:
            target_dir = output_path / course_dir / session_dir
            
        # 2. Determine file path based on artifact type
        file_path = None
        if artifact.type == "reading":
            file_path = target_dir / "Bài đọc" / "reading.html"
        elif artifact.type == "outline":
            file_path = target_dir / "Sơ đồ tư duy" / "outline.md"
        elif artifact.type == "quiz":
            file_path = target_dir / "Câu hỏi Quizz" / "quiz.json"
        elif artifact.type == "pre_quiz":
            file_path = target_dir / "Câu hỏi Quizz" / "quiz_entrance.json"
        elif artifact.type == "post_quiz":
            file_path = target_dir / "Câu hỏi Quizz" / "quiz_exit.json"
        elif artifact.type == "session_reading":
            file_path = target_dir / "Bài đọc" / "reading_all.html"
        elif artifact.type == "session_mindmap":
            file_path = target_dir / "Sơ đồ tư duy" / "mindmap_all.md"
        elif artifact.type in ["session_homework", "session_practice"]:
            file_path = target_dir / "Bài tập về nhà" / "homework.json"
        elif artifact.type == "project_entry_tests":
            file_path = target_dir / "Bài kiểm tra đầu giờ"
        elif artifact.type == "project_srs":
            file_path = target_dir / "Tài liệu đặc tả SRS" / "tai_lieu_dac_ta_yeu_cau_srs.md"
        elif artifact.type == "project_mini_project":
            file_path = target_dir / "Mini project" / "de_bai_mini_project.md"

        if not file_path:
            print(f"[Sync Disk Info] Unknown or unsupported artifact type: {artifact.type}. Skipping disk sync.")
            return

        # 3. Write content/JSON back to disk
        if artifact.type == "project_entry_tests":
            # Special handling for project entry tests (multiple files)
            file_path.mkdir(parents=True, exist_ok=True)
            entry_tests = (artifact.content_json or {}).get("entry_tests") or []
            from app.ai_engine.agents.project_agents import sanitize_vietnamese_filename
            for idx, test in enumerate(entry_tests, 1):
                clean_name = sanitize_vietnamese_filename(test.get("title", f"test_{idx}"))
                filename = f"bai_kiem_tra_{idx:02d}_{clean_name}"
                with open(file_path / filename, "w", encoding="utf-8") as f:
                    f.write(test.get("content", ""))
            print(f"[Sync Disk Success] Saved project entry tests to {file_path}")
            
        elif artifact.type == "project_mini_project":
            # Special handling for project mini project (writes main md and scoring criteria rubric)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(artifact.content or (artifact.content_json or {}).get("content", ""))
            
            rubric_content = (artifact.content_json or {}).get("rubric", "")
            if rubric_content:
                rubric_path = file_path.parent / "tieu_chi_cham_diem_ai.md"
                with open(rubric_path, "w", encoding="utf-8") as f:
                    f.write(rubric_content)
            print(f"[Sync Disk Success] Saved project mini project to {file_path}")

        else:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            if artifact.content is not None:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(str(artifact.content))
            elif artifact.content_json is not None:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(artifact.content_json, f, ensure_ascii=False, indent=2)
            print(f"[Sync Disk Success] Saved artifact {artifact.id} ({artifact.type}) to {file_path}")
            
    except Exception as e:
        print(f"[Sync Disk Error] Failed to write artifact {artifact.id} to disk: {e}")


