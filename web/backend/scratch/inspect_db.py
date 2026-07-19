import sqlite3
import os
from pathlib import Path

db_path = Path(__file__).resolve().parents[1] / "app.db"
print("DB path:", db_path)

if not db_path.exists():
    print("Database file does not exist!")
    exit(1)

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Get tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

# Get courses
cursor.execute("SELECT id, name, technology_stack FROM courses;")
print("\nCourses:", cursor.fetchall())

# Get sessions
cursor.execute("SELECT id, name, title, course_id, order_index FROM sessions LIMIT 5;")
print("\nSessions:", cursor.fetchall())

# Get artifacts
cursor.execute("SELECT id, session_id, lesson_id, type, status FROM artifacts LIMIT 10;")
print("\nArtifacts:", cursor.fetchall())

conn.close()
