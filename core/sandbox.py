from pathlib import Path
# core/sandbox.py
import os
import tempfile
import subprocess
import shutil
from typing import Dict, Any

def execute_code_safely(code: str) -> Dict[str, Any]:
    """
    Executes Python code safely inside:
    1. E2B cloud sandbox (if configured and E2B_API_KEY is available)
    2. A highly-restricted local Docker container (no network, cpu/mem limits, non-root user, stdin feed)
    3. A local subprocess (blocked if SANDBOX_STRICT=True or in production)
    """
    # Clean code formatting if it contains markdown markers
    if code.strip().startswith("```"):
        lines = code.strip().splitlines()
        if lines[0].startswith("```python") or lines[0].startswith("```py"):
            lines = lines[1:]
        if lines[-1].strip() == "```":
            lines = lines[:-1]
        code = "\n".join(lines)

    # --- Sandbox Security Configuration (Read Dynamically) ---
    sandbox_provider = os.getenv("SANDBOX_PROVIDER", "docker").lower()
    sandbox_strict = os.getenv("SANDBOX_STRICT", "false").lower() == "true"
    sandbox_timeout = int(os.getenv("SANDBOX_TIMEOUT", "5"))
    sandbox_memory = os.getenv("SANDBOX_MEMORY", "256m")
    sandbox_cpus = os.getenv("SANDBOX_CPUS", "0.5")

    e2b_api_key = os.getenv("E2B_API_KEY")
    
    # 1. E2B Cloud Sandbox Execution Path
    if sandbox_provider == "e2b" or (e2b_api_key and sandbox_provider != "local_subprocess"):
        if not e2b_api_key:
            return {
                "status": "FAILED",
                "engine": "e2b",
                "error": "Security Configuration Error: E2B provider selected, but E2B_API_KEY is not set."
            }
        
        print("  [Sandbox] Attempting E2B Cloud Sandbox execution...")
        e2b_result = _execute_via_e2b(code, e2b_api_key, sandbox_timeout)
        if e2b_result:
            return e2b_result
        
        # If strict, do not fallback
        if sandbox_strict:
            return {
                "status": "FAILED",
                "engine": "e2b",
                "error": "E2B Sandbox execution failed, and fallback is blocked in strict mode."
            }

    # 2. Local Docker Container Execution Path
    has_docker = shutil.which("docker") is not None
    if has_docker and sandbox_provider != "local_subprocess":
        # Check if Docker daemon is actually running
        docker_daemon_running = False
        try:
            daemon_check = subprocess.run(["docker", "ps"], capture_output=True, timeout=2)
            if daemon_check.returncode == 0:
                docker_daemon_running = True
        except Exception:
            pass

        if docker_daemon_running:
            print(f"  [Sandbox] Executing code in highly-restricted Docker container (CPUs: {sandbox_cpus}, RAM: {sandbox_memory})...")
            docker_result = _execute_via_docker(code, sandbox_memory, sandbox_cpus, sandbox_timeout)
            if docker_result:
                # If execution succeeded or failed due to student code syntax/runtime error, return it
                if docker_result.get("status") == "SUCCESS" or "error during connect" not in str(docker_result.get("error", "")):
                    return docker_result
        else:
            print("  [Sandbox Warning] Docker CLI found, but Docker daemon is not running or accessible.")

        if sandbox_strict:
            return {
                "status": "FAILED",
                "engine": "docker",
                "error": "Docker sandbox execution failed (or daemon inactive), and fallback is blocked in strict mode."
            }

    # 3. Local Subprocess Fallback Path (Security Guard)
    if sandbox_strict:
        print("  [Sandbox SECURITY ERROR] Local subprocess execution is permanently blocked for security reasons.")
        return {
            "status": "FAILED",
            "engine": "security_guard",
            "error": (
                "Security Block: Local subprocess execution is disabled to prevent malicious code execution. "
                "Please configure Docker or E2B sandbox providers."
            )
        }
    
    print("  [Sandbox] Falling back to local subprocess execution (Dev Mode)...")
    return _execute_via_local_subprocess(code, sandbox_timeout)


def _execute_via_e2b(code: str, api_key: str, timeout: int) -> Dict[str, Any]:
    """Helper to execute code via E2B SDK."""
    try:
        try:
            # Try importing e2b-code-interpreter first
            from e2b_code_interpreter import Sandbox
        except ImportError:
            # Fallback to core e2b sandbox
            from e2b import Sandbox

        with Sandbox(api_key=api_key) as sandbox:
            if hasattr(sandbox, "run_code"):
                # Jupyter notebook execution style (e2b-code-interpreter)
                execution = sandbox.run_code(code)
                if execution.error:
                    return {
                        "status": "FAILED",
                        "engine": "e2b",
                        "error": f"{execution.error.name}: {execution.error.value}\n{execution.error.traceback}"
                    }
                return {
                    "status": "SUCCESS",
                    "engine": "e2b",
                    "output": execution.logs.stdout
                }
            else:
                # Command line execution style (core e2b)
                # Write file in VM and execute
                sandbox.files.write("/home/user/app.py", code)
                result = sandbox.commands.run(f"python /home/user/app.py", timeout=timeout)
                if result.exit_code == 0:
                    return {
                        "status": "SUCCESS",
                        "engine": "e2b",
                        "output": result.stdout
                    }
                return {
                    "status": "FAILED",
                    "engine": "e2b",
                    "error": result.stderr or f"Exit code: {result.exit_code}"
                }
    except Exception as e:
        print(f"  [Sandbox Warning] E2B execution failed: {e}")
        return None


def _execute_via_docker(code: str, memory: str, cpus: str, timeout: int) -> Dict[str, Any]:
    """Helper to execute code in a highly-secured Docker environment without volume mounting."""
    try:
        # We pipe the python code directly to Python stdin inside container
        # Advantages:
        # 1. No host file mapping required (more secure, avoids permission/path issues on Windows/Linux hosts)
        # 2. Custom limits: memory, cpus, disabled network, dropped caps, non-root user
        result = subprocess.run(
            [
                "docker", "run", "--rm", "-i",
                "--network", "none",
                "--memory", memory,
                "--cpus", cpus,
                "--cap-drop", "ALL",
                "--security-opt", "no-new-privileges",
                "--read-only",
                "--tmpfs", "/tmp:rw,noexec,nosuid,size=16m",
                "--user", "1000:1000",
                "python:3.10-slim",
                "python", "-"
            ],
            input=code,
            capture_output=True,
            text=True,
            timeout=timeout
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
            "error": f"TimeoutExpired: Code execution exceeded {timeout} seconds limit."
        }
    except Exception as e:
        print(f"  [Sandbox Warning] Docker execution failed: {e}")
        return None


def _execute_via_local_subprocess(code: str, timeout: int) -> Dict[str, Any]:
    """Helper to run code in standard local subprocess (unrestricted, dev use only)."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file_path = os.path.join(temp_dir, "test_code.py")
        with open(temp_file_path, "w", encoding="utf-8") as f:
            f.write(code)
            
        try:
            result = subprocess.run(
                [shutil.which("python") or "python", temp_file_path],
                capture_output=True,
                text=True,
                timeout=timeout
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
                "error": f"TimeoutExpired: Code execution exceeded {timeout} seconds limit."
            }
        except Exception as e:
            return {
                "status": "FAILED",
                "engine": "local_subprocess",
                "error": f"Internal execution error: {str(e)}"
            }
