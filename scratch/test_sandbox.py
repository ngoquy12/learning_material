# scratch/test_sandbox.py
import sys
import os

# Put learning material workspace on search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.sandbox import execute_code_safely

def run_tests():
    print("====================================================")
    print("Testing core/sandbox.py Upgraded Execution Engines")
    print("====================================================")
    
    test_code = """
import sys
print("Hello Sandbox World from Python " + sys.version.split()[0])
"""

    # Test 1: Standard Execution (Local Subprocess fallback in dev mode)
    print("\n--- Test 1: Standard Dev Mode Execution (No Strict Mode) ---")
    os.environ["SANDBOX_STRICT"] = "False"
    os.environ["SANDBOX_ENV"] = "development"
    os.environ["SANDBOX_PROVIDER"] = "docker" # will fallback since docker isn't running
    
    result = execute_code_safely(test_code)
    print(f"Status: {result['status']}")
    print(f"Engine used: {result['engine']}")
    if result['status'] == "SUCCESS":
        print(f"Output: {result['output'].strip()}")
    else:
        print(f"Error: {result['error']}")
    assert result['status'] == "SUCCESS", "Dev mode execution should succeed"
    assert result['engine'] == "local_subprocess", "Fallback should occur when Docker is missing"

    # Test 2: Strict/Production Mode Execution
    print("\n--- Test 2: Production Mode Security Guard Execution (Strict Mode) ---")
    os.environ["SANDBOX_STRICT"] = "True"
    os.environ["SANDBOX_ENV"] = "production"
    
    result = execute_code_safely(test_code)
    print(f"Status: {result['status']}")
    print(f"Engine used: {result['engine']}")
    print(f"Expected Error: {result.get('error', '').strip()}")
    assert result['status'] == "FAILED", "Strict mode execution should fail without safe engines"
    assert result['engine'] == "security_guard", "Security guard should block local subprocess"

    # Test 3: Markdown Fenced Code Parsing
    print("\n--- Test 3: Markdown Fenced Code Parsing ---")
    os.environ["SANDBOX_STRICT"] = "False"
    os.environ["SANDBOX_ENV"] = "development"
    
    fenced_code = """
```python
x = 5
y = 10
print(f"Sum is {x + y}")
```
"""
    result = execute_code_safely(fenced_code)
    print(f"Status: {result['status']}")
    print(f"Output: {result.get('output', '').strip()}")
    assert result['status'] == "SUCCESS"
    assert "Sum is 15" in result['output']
    
    print("\n====================================================")
    print("ALL SANDBOX SECURITY TESTS PASSED SUCCESSFULLY!")
    print("====================================================")

if __name__ == "__main__":
    run_tests()
