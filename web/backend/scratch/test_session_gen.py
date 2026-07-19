import asyncio
import os
import sys

# Add both web/backend and the project root to sys.path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
project_root = os.path.abspath(os.path.join(backend_dir, "..", ".."))

sys.path.insert(0, project_root)
sys.path.insert(0, backend_dir)

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from app.api.endpoints.session import generate_session_artifacts_task

async def main():
    print(f"Project root added to sys.path: {project_root}")
    print("Triggering generate_session_artifacts_task for Session 94...")
    await generate_session_artifacts_task(94)
    print("Done!")

if __name__ == "__main__":
    asyncio.run(main())
