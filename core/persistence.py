import sqlite3
import json
import os
import zlib
import queue
import threading
from contextlib import contextmanager
from typing import Dict, Any

DB_PATH = "state_store_v2.db"
_db_initialized = False
_pool = None
_pool_lock = threading.Lock()

class SQLiteConnectionPool:
    """A thread-safe connection pool for SQLite to prevent locking and enable connection reuse."""
    def __init__(self, db_path: str, pool_size: int = 5, max_overflow: int = 10, timeout: float = 30.0):
        self.db_path = db_path
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.timeout = timeout
        self.pool = queue.Queue(maxsize=pool_size)
        self.active_connections = 0
        self.lock = threading.Lock()

    def _create_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=self.timeout, check_same_thread=False)
        try:
            cursor = conn.cursor()
            cursor.execute("PRAGMA journal_mode=WAL;")
            cursor.execute("PRAGMA synchronous=NORMAL;")
            conn.commit()
        except sqlite3.Error as e:
            conn.close()
            raise e
        return conn

    @contextmanager
    def get_connection(self) -> sqlite3.Connection:
        conn = None
        try:
            # Attempt to retrieve an existing connection from the queue
            conn = self.pool.get_nowait()
        except queue.Empty:
            with self.lock:
                if self.active_connections < self.pool_size + self.max_overflow:
                    conn = self._create_connection()
                    self.active_connections += 1

            if conn is None:
                # Pool and overflow limits reached; wait for connection to be returned
                try:
                    conn = self.pool.get(timeout=self.timeout)
                except queue.Empty:
                    raise sqlite3.OperationalError("Database connection pool exhausted.")

        try:
            yield conn
        finally:
            if conn is not None:
                # Return connection to the pool or close it if pool is full
                with self.lock:
                    if self.pool.qsize() < self.pool_size:
                        self.pool.put(conn)
                    else:
                        conn.close()
                        self.active_connections -= 1

    def close_all(self):
        """Closes all connections in the pool and updates active counts."""
        with self.lock:
            while not self.pool.empty():
                try:
                    conn = self.pool.get_nowait()
                    conn.close()
                    self.active_connections -= 1
                except queue.Empty:
                    break

def get_pool() -> SQLiteConnectionPool:
    """Thread-safe access to the global connection pool using double-checked locking."""
    global _pool
    if _pool is None:
        with _pool_lock:
            if _pool is None:
                from config.settings import DB_POOL_SIZE, DB_MAX_OVERFLOW, DB_POOL_TIMEOUT
                _pool = SQLiteConnectionPool(
                    db_path=DB_PATH,
                    pool_size=DB_POOL_SIZE,
                    max_overflow=DB_MAX_OVERFLOW,
                    timeout=DB_POOL_TIMEOUT
                )
    return _pool

def _is_corrupt_error(e: Exception) -> bool:
    """Checks if an SQLite exception indicates database corruption or invalid format."""
    err_msg = str(e).lower()
    return "malformed" in err_msg or "corrupt" in err_msg or "not a database" in err_msg

def _reset_corrupt_db(e: Exception):
    """Closes all connections, deletes the corrupt database files, and triggers recreation."""
    global _db_initialized, _pool
    print(f"\n[Persistence Critical] Database corrupt/invalid: {e}. Initiating self-healing reset...")
    
    # Close pool connections to release file locks
    with _pool_lock:
        if _pool is not None:
            _pool.close_all()
            _pool = None
    _db_initialized = False
    
    # Clean up files on disk
    if os.path.exists(DB_PATH):
        try:
            for suffix in ["", "-wal", "-journal", "-shm"]:
                p = DB_PATH + suffix
                if os.path.exists(p):
                    os.remove(p)
        except Exception as remove_err:
            print(f"  -> Failed to delete database file: {remove_err}")
            
    # Re-initialize the database schema
    init_db()
    print("  -> Database self-healing complete: Fresh SQLite database created successfully.\n")

def init_db():
    """Initializes the SQLite database schema for storing agent states with self-healing recovery."""
    global _db_initialized
    if _db_initialized:
        return
        
    try:
        pool = get_pool()
        with pool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS checkpoints (
                    session_id TEXT PRIMARY KEY,
                    state_data BLOB
                )
            """)
            conn.commit()
        _db_initialized = True
    except sqlite3.Error as e:
        if _is_corrupt_error(e):
            _reset_corrupt_db(e)
        else:
            print(f"  -> SQLite connection warning during init: {e}")

def save_checkpoint(session_id: str, state: Dict[str, Any]):
    """Saves the current AgentState to the database with auto-healing retry support."""
    init_db()
    for attempt in range(2):
        try:
            pool = get_pool()
            with pool.get_connection() as conn:
                cursor = conn.cursor()
                
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
            return  # Success
        except sqlite3.Error as e:
            if _is_corrupt_error(e) and attempt == 0:
                _reset_corrupt_db(e)
                continue
            else:
                print(f"  -> Failed to save checkpoint to database: {e}")
                break

def load_checkpoint(session_id: str) -> Dict[str, Any]:
    """Loads a previously saved AgentState for the given session_id with auto-healing retry support."""
    init_db()
    for attempt in range(2):
        try:
            pool = get_pool()
            with pool.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT state_data FROM checkpoints WHERE session_id = ?", (session_id,))
                row = cursor.fetchone()
                if row:
                    try:
                        decompressed = zlib.decompress(row[0]).decode('utf-8')
                        return json.loads(decompressed)
                    except Exception:
                        try:
                            return json.loads(row[0])
                        except Exception as parse_err:
                            print(f"  -> Failed to parse checkpoint for {session_id}: {parse_err}")
                return None
        except sqlite3.Error as e:
            if _is_corrupt_error(e) and attempt == 0:
                _reset_corrupt_db(e)
                continue
            else:
                print(f"  -> Failed to load checkpoint from database: {e}")
                break
    return None
