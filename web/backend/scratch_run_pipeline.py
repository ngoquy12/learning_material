import asyncio
import os
import sys

from pathlib import Path
backend_path = Path(__file__).resolve().parent
project_root = backend_path.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(backend_path))
sys.path.insert(0, str(backend_path / "app" / "ai_engine"))

from app.db.session import AsyncSessionLocal
from app.models.lesson import Lesson
from app.api.endpoints.lesson import generate_lesson_task
from sqlalchemy import select

async def main():
    # Make sure we print everything with print
    print("Fetching Lesson 101 details...")
    async with AsyncSessionLocal() as db:
        stmt = select(Lesson).where(Lesson.id == 101)
        res = await db.execute(stmt)
        lesson = res.scalars().first()
        if not lesson:
            print("Lesson 101 not found!")
            return
        
        lesson_id = lesson.id
        session_id = lesson.session_id
        pm_input = lesson.details
        title = lesson.title
        tech_stack = "python/fastapi"
        course_dir_name = "FastAPI_Course"
        
        print(f"Running generate_lesson_task for Lesson {lesson_id}: {title}")
        print(f"Details: {pm_input}")
        
    # Run task
    await generate_lesson_task(lesson_id, session_id, pm_input, title, tech_stack, course_dir_name)
    print("Done!")

if __name__ == "__main__":
    # Ensure correct environment variables (LLM API keys, UTF8 encoding)
    os.environ["PYTHONUTF8"] = "1"
    asyncio.run(main())
