import threading
import time
import random
import os
import sys
import sqlite3

# Adjust python path to import core modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.persistence import (
    init_db,
    save_checkpoint,
    load_checkpoint,
    get_pool,
    DB_PATH
)

def clean_database():
    """Removes all database files before/after tests."""
    for suffix in ["", "-wal", "-journal", "-shm"]:
        p = DB_PATH + suffix
        if os.path.exists(p):
            try:
                os.remove(p)
            except Exception as e:
                print(f"Failed to remove {p}: {e}")

def reset_test_env():
    """Resets the pool and persistence module variables to guarantee clean file states on Windows."""
    try:
        pool = get_pool()
        pool.close_all()
    except Exception:
        pass
    
    import core.persistence as cp
    cp._db_initialized = False
    with cp._pool_lock:
        cp._pool = None
        
    clean_database()

def test_basic_save_and_load():
    print("[Test] Running basic save and load test...")
    reset_test_env()
    
    init_db()
    test_state = {
        "html_content": "<h1>Test Header</h1>",
        "approved": True,
        "counter": 42,
        "meta": {"nested": "value"}
    }
    
    # Save checkpoint
    save_checkpoint("session_basic", test_state)
    
    # Load checkpoint
    loaded = load_checkpoint("session_basic")
    assert loaded is not None, "Loaded state should not be None"
    assert loaded["html_content"] == test_state["html_content"], "html_content mismatch"
    assert loaded["approved"] == test_state["approved"], "approved mismatch"
    assert loaded["counter"] == test_state["counter"], "counter mismatch"
    assert loaded["meta"] == test_state["meta"], "nested meta mismatch"
    
    print("[Test] Basic save and load test PASSED!")

def test_concurrency():
    print("[Test] Running concurrency test (simulating parallel graph execution)...")
    reset_test_env()
    init_db()
    
    num_threads = 15
    write_loops = 10
    errors = []
    
    def worker(thread_idx):
        try:
            for loop in range(write_loops):
                session_id = f"session_thread_{thread_idx}"
                state = {
                    "thread_idx": thread_idx,
                    "loop": loop,
                    "random_val": random.randint(1000, 9999),
                    "timestamp": time.time()
                }
                
                # Interleaved reads and writes
                save_checkpoint(session_id, state)
                time.sleep(random.uniform(0.01, 0.05))
                
                loaded = load_checkpoint(session_id)
                if loaded is None:
                    errors.append(f"Thread {thread_idx} loop {loop}: Loaded state is None")
                elif loaded["random_val"] != state["random_val"]:
                    errors.append(f"Thread {thread_idx} loop {loop}: Value mismatch")
        except Exception as e:
            errors.append(f"Thread {thread_idx} encountered exception: {e}")

    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    assert len(errors) == 0, f"Concurrency errors occurred: {errors}"
    print(f"[Test] Concurrency test PASSED! {num_threads} threads executed without locks or errors.")

def test_self_healing():
    print("[Test] Running database self-healing recovery test...")
    reset_test_env()
    init_db()
    
    # Save a valid checkpoint first
    save_checkpoint("session_pre_corrupt", {"status": "ok"})
    
    # Close pool connections first so Windows unlocks the file
    pool = get_pool()
    pool.close_all()
    
    print("  -> Corrupting the database file...")
    try:
        with open(DB_PATH, "w") as f:
            f.write("Definitely not an SQLite database file. Just random junk text.")
    except Exception as e:
        print(f"  -> Could not write corrupt file: {e}")
        raise e
        
    # Attempting to load or save should trigger self-healing, rebuild the DB, and continue
    print("  -> Attempting to save new checkpoint to corrupted database...")
    save_checkpoint("session_post_corrupt", {"status": "healed"})
    
    # Check if loaded correctly
    loaded = load_checkpoint("session_post_corrupt")
    assert loaded is not None, "Loaded state after healing should not be None"
    assert loaded["status"] == "healed", "Loaded state status mismatch"
    
    # The pre-corrupt one is gone because DB was reset, which is correct self-healing behavior
    pre_loaded = load_checkpoint("session_pre_corrupt")
    assert pre_loaded is None, "Pre-corrupt state should be cleared on database reset"
    
    print("[Test] Self-healing recovery test PASSED!")

if __name__ == "__main__":
    try:
        test_basic_save_and_load()
        print("-" * 50)
        test_concurrency()
        print("-" * 50)
        test_self_healing()
        print("-" * 50)
        print("ALL DATABASE POOL TESTS PASSED SUCCESSFULLY!")
    finally:
        reset_test_env()
