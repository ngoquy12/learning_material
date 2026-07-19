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
        res = await db.execute(select(Artifact).where(Artifact.id == 19))
        art = res.scalars().first()
        if art:
            out_file = Path(__file__).resolve().parent / "mindmap_output.md"
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(art.content or "")
            print(f"Content written to {out_file.name}")
        else:
            print("Artifact 19 not found")

if __name__ == "__main__":
    asyncio.run(main())
