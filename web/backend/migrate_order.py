import asyncio
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "elearning")
DB_PORT = int(os.getenv("DB_PORT", "3306"))

def run_migration():
    conn = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE sessions ADD COLUMN order_index INT DEFAULT 0;")
        print("Added order_index to sessions")
    except Exception as e:
        print("Sessions:", e)
        
    try:
        cursor.execute("ALTER TABLE lessons ADD COLUMN order_index INT DEFAULT 0;")
        print("Added order_index to lessons")
    except Exception as e:
        print("Lessons:", e)
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    run_migration()
