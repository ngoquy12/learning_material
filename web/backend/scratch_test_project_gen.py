import asyncio
import os
import sys

# Add backend directory to sys.path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

# Add parent directory to sys.path
parent_dir = os.path.dirname(backend_dir)
sys.path.insert(0, parent_dir)

from app.api.endpoints.session import generate_project_session_task

async def main():
    print("Running project session generation task synchronously...")
    await generate_project_session_task(101)
    print("Finished.")

if __name__ == "__main__":
    asyncio.run(main())
