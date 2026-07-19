import asyncio
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root_dir))

from app.db.session import AsyncSessionLocal
from app.models.artifact import Artifact
from sqlalchemy.future import select

async def main():
    async with AsyncSessionLocal() as db:
        res = await db.execute(select(Artifact).where(Artifact.session_id == 94, Artifact.type == "session_mindmap"))
        art = res.scalar_one_or_none()
        
        output_file = Path(__file__).resolve().parent / "session_mindmap_info.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            if art:
                f.write("=== SESSION 94 MINDMAP ARTIFACT ===\n")
                f.write(f"Status: {art.status}\n")
                f.write(f"Content:\n")
                f.write(art.content)
            else:
                f.write("No session_mindmap artifact found for Session 94\n")

if __name__ == "__main__":
    asyncio.run(main())
