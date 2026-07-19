import asyncio
from sqlalchemy import text
from app.db.session import engine

async def run_migration():
    async with engine.begin() as conn:
        try:
            await conn.execute(text("ALTER TABLE sessions ADD COLUMN order_index INT DEFAULT 0;"))
            print("Added order_index to sessions")
        except Exception as e:
            print("Sessions error:", e)
            
        try:
            await conn.execute(text("ALTER TABLE lessons ADD COLUMN order_index INT DEFAULT 0;"))
            print("Added order_index to lessons")
        except Exception as e:
            print("Lessons error:", e)

if __name__ == "__main__":
    asyncio.run(run_migration())
