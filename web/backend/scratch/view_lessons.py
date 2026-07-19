import asyncio
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root_dir))

from app.db.session import AsyncSessionLocal
from app.models.lesson import Lesson
from app.models.artifact import Artifact
from sqlalchemy.future import select

async def main():
    async with AsyncSessionLocal() as db:
        # Get lessons for session 94
        res = await db.execute(select(Lesson).where(Lesson.session_id == 94))
        lessons = res.scalars().all()
        
        output_file = Path(__file__).resolve().parent / "lessons_info.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("=== LESSONS FOR SESSION 94 ===\n")
            for l in lessons:
                f.write(f"Lesson ID: {l.id}, Name: {l.name}, Title: {l.title}\n")
                # Get outline artifact for this lesson
                art_res = await db.execute(select(Artifact).where(Artifact.lesson_id == l.id, Artifact.type == "outline"))
                art = art_res.scalar_one_or_none()
                if art:
                    f.write(f"  Outline Artifact ID: {art.id}, Status: {art.status}\n")
                    f.write(f"  Outline Content Snippet:\n{art.content[:500] if art.content else 'None'}\n\n")
                else:
                    f.write("  No Outline Artifact found\n\n")

if __name__ == "__main__":
    asyncio.run(main())
