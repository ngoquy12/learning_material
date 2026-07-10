import sqlite3
import json
import os
import zlib
from typing import Dict, Any

DB_PATH = "state_store_v2.db"
_db_initialized = False

def init_db():
    """Initializes the SQLite database schema for storing agent states with self-healing recovery."""
    global _db_initialized
    if _db_initialized:
        return
        
    try:
        conn = sqlite3.connect(DB_PATH, timeout=30.0)
        cursor = conn.conn.cursor() if hasattr(conn, "conn") else conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA synchronous=NORMAL;")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS checkpoints (
                session_id TEXT PRIMARY KEY,
                state_data BLOB
            )
        """)
        conn.commit()
        conn.close()
        _db_initialized = True
    except sqlite3.DatabaseError as e:
        err_msg = str(e).lower()
        if "malformed" in err_msg or "corrupt" in err_msg or "not a database" in err_msg:
            print(f"\n[Persistence Critical] Database corrupt: {e}. Initiating self-healing reset...")
            # Clean up database file
            if os.path.exists(DB_PATH):
                try:
                    for suffix in ["", "-wal", "-journal", "-shm"]:
                        p = DB_PATH + suffix
                        if os.path.exists(p):
                            os.remove(p)
                except Exception as remove_err:
                    print(f"  -> Failed to delete database file: {remove_err}")
                    
            # Rebuild fresh database
            try:
                conn = sqlite3.connect(DB_PATH, timeout=30.0)
                cursor = conn.cursor()
                cursor.execute("PRAGMA journal_mode=WAL;")
                cursor.execute("PRAGMA synchronous=NORMAL;")
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS checkpoints (
                        session_id TEXT PRIMARY KEY,
                        state_data BLOB
                    )
                """)
                conn.commit()
                conn.close()
                _db_initialized = True
                print("  -> Database self-healing complete: Fresh SQLite database created successfully.\n")
            except Exception as rebuild_err:
                print(f"  -> Critical failure rebuilding database: {rebuild_err}")
        else:
            print(f"  -> SQLite connection warning: {e}")

def save_checkpoint(session_id: str, state: Dict[str, Any]):
    """Saves the current AgentState to the database using the session_id as the primary key."""
    init_db()
    try:
        conn = sqlite3.connect(DB_PATH, timeout=30.0)
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA synchronous=NORMAL;")
        
        # Create a serializable copy of the state
        state_copy = {}
        for k, v in state.items():
            try:
                json.dumps({k: v})
                state_copy[k] = v
            except TypeError:
                continue
                
        state_json = json.dumps(state_copy, ensure_ascii=False)
        compressed_data = zlib.compress(state_json.encode('utf-8'), level=6)
        
        cursor.execute("""
            INSERT INTO checkpoints (session_id, state_data)
            VALUES (?, ?)
            ON CONFLICT(session_id) DO UPDATE SET state_data = excluded.state_data
        """, (session_id, sqlite3.Binary(compressed_data)))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"  -> Failed to save checkpoint to database: {e}")

def load_checkpoint(session_id: str) -> Dict[str, Any]:
    """Loads a previously saved AgentState for the given session_id. Returns None if not found."""
    init_db()
    try:
        conn = sqlite3.connect(DB_PATH, timeout=30.0)
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("SELECT state_data FROM checkpoints WHERE session_id = ?", (session_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            # Handle both zlib-compressed data and legacy plaintext json (for backwards-compatibility)
            try:
                decompressed = zlib.decompress(row[0]).decode('utf-8')
                return json.loads(decompressed)
            except Exception:
                try:
                    # Fallback to direct json loading if it was plain text
                    return json.loads(row[0])
                except Exception as parse_err:
                    print(f"  -> Failed to parse checkpoint for {session_id}: {parse_err}")
    except sqlite3.Error as e:
        print(f"  -> Failed to load checkpoint from database: {e}")
    return None
