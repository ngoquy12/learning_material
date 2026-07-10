# core/sandbox.py
import os
import tempfile
import subprocess
import shutil
from typing import Dict, Any

def execute_code_safely(code: str) -> Dict[str, Any]:
    """
    Executes Python code safely inside a local Docker container if available,
    otherwise falls back to a sandboxed local subprocess with timeout.
    """
    # Clean code formatting if it contains markdown markers
    if code.strip().startswith("```"):
        lines = code.strip().splitlines()
        if lines[0].startswith("```python") or lines[0].startswith("```py"):
            lines = lines[1:]
        if lines[-1].strip() == "```":
            lines = lines[:-1]
        code = "\n".join(lines)

    # 1. Try Docker execution if docker command is available
    has_docker = shutil.which("docker") is not None
    
    # Create temp directory and write the script
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file_path = os.path.join(temp_dir, "test_code.py")
        with open(temp_file_path, "w", encoding="utf-8") as f:
            f.write(code)
            
        if has_docker:
            try:
                print("  [Sandbox] Executing code in local Docker container...")
                # Run script in a slim python docker container with 5s timeout
                # Map host temporary file into container
                container_path = "/usr/src/app/test_code.py"
                result = subprocess.run(
                    [
                        "docker", "run", "--rm",
                        "-v", f"{os.path.abspath(temp_file_path)}:{container_path}",
                        "python:3.10-slim",
                        "python", container_path
                    ],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    return {
                        "status": "SUCCESS",
                        "engine": "docker",
                        "output": result.stdout
                    }
                else:
                    return {
                        "status": "FAILED",
                        "engine": "docker",
                        "error": result.stderr or result.stdout or f"Exit code: {result.returncode}"
                    }
            except subprocess.TimeoutExpired:
                return {
                    "status": "FAILED",
                    "engine": "docker",
                    "error": "TimeoutExpired: Code execution exceeded 5 seconds limit."
                }
            except Exception as e:
                print(f"  [Sandbox Warning] Docker execution failed: {e}. Falling back to local subprocess...")
                # Fall through to local subprocess if docker daemon is not running

        # 2. Local Subprocess Fallback
        print("  [Sandbox] Executing code in local sandboxed subprocess...")
        try:
            result = subprocess.run(
                [shutil.which("python") or "python", temp_file_path],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return {
                    "status": "SUCCESS",
                    "engine": "local_subprocess",
                    "output": result.stdout
                }
            else:
                return {
                    "status": "FAILED",
                    "engine": "local_subprocess",
                    "error": result.stderr or f"Exit code: {result.returncode}"
                }
        except subprocess.TimeoutExpired:
            return {
                "status": "FAILED",
                "engine": "local_subprocess",
                "error": "TimeoutExpired: Code execution exceeded 5 seconds limit."
            }
        except Exception as e:
            return {
                "status": "FAILED",
                "engine": "local_subprocess",
                "error": f"Internal execution error: {str(e)}"
            }
