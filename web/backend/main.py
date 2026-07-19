import sys
import os

# Force UTF-8 encoding for standard streams to prevent CP1252/charmap errors on Windows
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, root_dir)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, set this to the specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.api_router import api_router

@app.on_event("startup")
async def startup_event():
    from app.db.session import engine
    from sqlalchemy import text
    async with engine.begin() as conn:
        try:
            await conn.execute(text("ALTER TABLE artifacts ADD COLUMN versions JSON NULL;"))
            print("[DB] Added versions column to artifacts table successfully.")
        except Exception as e:
            print(f"[DB] Attempted to add versions column (may already exist): {e}")

@app.get("/")
def root():
    return {"message": "Welcome to Elearning Agent API"}

app.include_router(api_router, prefix=settings.API_V1_STR)

# Mount static files (locally generated artifacts like mindmaps, diagrams)
from fastapi.staticfiles import StaticFiles
from pathlib import Path

current_file = Path(__file__).resolve()
# backend_dir is web/backend (parents[0])
# project_root is Learning-Material (parents[2])
project_root = current_file.parents[2]

output_dir = project_root / "output"
output_dir.mkdir(parents=True, exist_ok=True)
print(f"[Static] Mounting {output_dir} at /static")
app.mount("/static", StaticFiles(directory=str(output_dir)), name="static")

# Mount shared resources (logo, etc.) from workspace root
resources_dir = project_root / "resources"
resources_dir.mkdir(parents=True, exist_ok=True)
print(f"[Static] Mounting {resources_dir} at /resources")
app.mount("/resources", StaticFiles(directory=str(resources_dir)), name="resources")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

