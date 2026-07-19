import asyncio
import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(root_dir / "web" / "backend"))

from app.api.endpoints.session import generate_session_artifacts_task
from app.db.session import AsyncSessionLocal

async def main():
    session_id = 94
    print(f"Resetting session_homework status to Pending for Session {session_id}...")
    from app.models.artifact import Artifact
    from sqlalchemy import update
    async with AsyncSessionLocal() as db:
        await db.execute(
            update(Artifact)
            .where(Artifact.session_id == session_id, Artifact.type == "session_homework")
            .values(status="Pending")
        )
        await db.commit()
        
    print(f"Triggering sync generate_session_artifacts_task for Session {session_id}...")
    try:
        await generate_session_artifacts_task(session_id)
        print("Done!")
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
