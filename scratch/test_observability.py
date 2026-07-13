import os
import sys
import json
import time

# Adjust python path to import core modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.observability import log_agent_call, TRACE_LOG_PATH

def test_local_jsonl_conventions():
    print("[Test] Running local JSONL OpenTelemetry conventions verification...")
    
    # Remove existing trace file if present to make test isolated
    if os.path.exists(TRACE_LOG_PATH):
        try:
            os.remove(TRACE_LOG_PATH)
        except Exception:
            pass
            
    start_time = time.time() - 1.250 # mock 1.25 seconds execution
    mock_tokens = {
        "prompt_tokens": 120,
        "completion_tokens": 45,
        "total_tokens": 165
    }
    
    log_agent_call(
        agent_name="Mock_Agent_Test",
        session_id="Session 99",
        lesson_id="Lesson 01",
        prompt_summary="System: This is a system instruction.\nUser: Hello model!",
        response_summary="Model: Hi user! How can I help you today?",
        start_time=start_time,
        token_cost=mock_tokens
    )
    
    # Verify trace log file exists
    assert os.path.exists(TRACE_LOG_PATH), "Trace log file should have been created"
    
    # Read the entry and parse JSON
    with open(TRACE_LOG_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    assert len(lines) == 1, "There should be exactly one log entry"
    entry = json.loads(lines[0].strip())
    
    # Check regular variables
    assert entry["agent_name"] == "Mock_Agent_Test"
    assert entry["session_id"] == "Session 99"
    assert entry["lesson_id"] == "Lesson 01"
    assert "Mock_Agent_Test" in entry["prompt_summary"] or "System: This is a system instruction." in entry["prompt_summary"]
    assert "Hi user!" in entry["response_summary"]
    
    # Check trace & span id generation
    assert "trace_id" in entry and len(entry["trace_id"]) > 0
    assert "span_id" in entry and len(entry["span_id"]) > 0
    
    # Check OpenTelemetry Semantic Attributes for GenAI
    assert "gen_ai.system" in entry
    assert "gen_ai.request.model" in entry
    assert entry["gen_ai.usage.input_tokens"] == 120
    assert entry["gen_ai.usage.output_tokens"] == 45
    assert entry["gen_ai.usage.total_tokens"] == 165
    assert entry["duration_seconds"] >= 1.25, "Duration should be captured correctly"
    
    print("[Test] Local JSONL OTel conventions verification PASSED!")

if __name__ == "__main__":
    try:
        test_local_jsonl_conventions()
        print("=" * 50)
        print("ALL OBSERVABILITY INTEGRATION TESTS PASSED SUCCESSFULLY!")
    finally:
        # Cleanup
        if os.path.exists(TRACE_LOG_PATH):
            try:
                os.remove(TRACE_LOG_PATH)
            except Exception:
                pass
