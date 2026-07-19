import asyncio
import os
import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root_dir))

from app.db.session import AsyncSessionLocal
from app.models.course import Course
from app.models.session import Session
from app.models.lesson import Lesson
from app.models.artifact import Artifact
from sqlalchemy.future import select

async def main():
    async with AsyncSessionLocal() as db:
        # Get courses
        res = await db.execute(select(Course))
        courses = res.scalars().all()
        
        # Get sessions
        res = await db.execute(select(Session).limit(30))
        sessions = res.scalars().all()

        # Get artifacts
        res = await db.execute(select(Artifact).limit(50))
        artifacts = res.scalars().all()

        output_path = Path(__file__).resolve().parent / "db_info.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("=== COURSES ===\n")
            for c in courses:
                f.write(f"ID: {c.id}, Name: {c.name}, Tech: {c.technology_stack}\n")

            f.write("\n=== SESSIONS ===\n")
            for s in sessions:
                f.write(f"ID: {s.id}, Name: {s.name}, Title: {s.title}, Course ID: {s.course_id}, Order: {s.order_index}\n")

            f.write("\n=== ARTIFACTS ===\n")
            for a in artifacts:
                f.write(f"ID: {a.id}, Session ID: {a.session_id}, Lesson ID: {a.lesson_id}, Type: {a.type}, Status: {a.status}\n")

        print("Database info successfully written to scratch/db_info.txt")

if __name__ == "__main__":
    asyncio.run(main())
