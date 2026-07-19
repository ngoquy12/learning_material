import asyncio
import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root_dir))

from app.db.session import AsyncSessionLocal
from app.models.artifact import Artifact
from sqlalchemy.future import select

async def main():
    sys.stdout.reconfigure(encoding='utf-8')
    async with AsyncSessionLocal() as db:
        res = await db.execute(select(Artifact).where(Artifact.lesson_id == 100, Artifact.type == "outline"))
        art = res.scalars().first()
        if art:
            print("=== LESSON OUTLINE CONTENT ===")
            print(repr(art.content))
        else:
            print("Lesson 100 outline not found")

if __name__ == "__main__":
    asyncio.run(main())
