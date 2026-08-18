"""
scripts/check_environment.py — Pre-flight Environment & Prerequisites Checker.
Verifies Python version, Node.js, FFmpeg, required Python packages, and .env configuration
before running expensive Multi-Agent pipelines.
"""

import sys
import os
import subprocess
from pathlib import Path

def check_python_version() -> bool:
    print("[1/5] Checking Python Version...")
    v = sys.version_info
    if v.major < 3 or (v.major == 3 and v.minor < 10):
        print(f"  [FAIL] Python 3.10+ required. Current: {v.major}.{v.minor}.{v.micro}")
        return False
    print(f"  [OK] Python {v.major}.{v.minor}.{v.micro}")
    return True

def check_python_packages() -> bool:
    print("[2/5] Checking Required Python Packages...")
    required = ["jinja2", "google.generativeai", "bs4", "openpyxl", "dotenv"]
    missing = []
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    if missing:
        print(f"  [FAIL] Missing Python packages: {', '.join(missing)}")
        print("         Please run: pip install -r requirements.txt")
        return False
    print("  [OK] All required Python packages installed.")
    return True

def check_nodejs() -> bool:
    print("[3/5] Checking Node.js Environment...")
    try:
        res = subprocess.run(["node", "-v"], capture_output=True, text=True, check=True)
        version_str = res.stdout.strip()
        print(f"  [OK] Node.js {version_str} detected.")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("  [WARN] Node.js is not installed or not in PATH.")
        print("         Marp CLI Slide Engine requires Node.js 18+.")
        return False

def check_ffmpeg() -> bool:
    print("[4/5] Checking FFmpeg Multimedia Tool...")
    try:
        res = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        if res.returncode == 0:
            first_line = res.stdout.splitlines()[0] if res.stdout else "FFmpeg installed"
            print(f"  [OK] {first_line[:50]}")
            return True
    except FileNotFoundError:
        pass
    print("  [WARN] FFmpeg not found in PATH.")
    return False

def check_env_config() -> bool:
    print("[5/5] Checking .env Configuration...")
    from dotenv import load_dotenv
    load_dotenv()
    
    gemini_key = os.getenv("GEMINI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if not gemini_key and not openai_key:
        print("  [FAIL] No API keys found in .env (GEMINI_API_KEY or OPENAI_API_KEY).")
        return False
        
    keys_found = []
    if gemini_key:
        keys_found.append("GEMINI_API_KEY")
    if openai_key:
        keys_found.append("OPENAI_API_KEY")
        
    print(f"  [OK] Found API Key(s): {', '.join(keys_found)}")
    return True

def run_all_checks() -> bool:
    print("\nRunning Elearning Content Factory Pre-flight System Check...\n" + "="*60)
    results = [
        check_python_version(),
        check_python_packages(),
        check_nodejs(),
        check_ffmpeg(),
        check_env_config()
    ]
    print("="*60)
    critical_passed = results[0] and results[1] and results[4]
    if critical_passed:
        print("System Ready: Pre-flight checks passed successfully!\n")
        return True
    else:
        print("System Check Failed: Please resolve the critical errors above.\n")
        return False

if __name__ == "__main__":
    success = run_all_checks()
    sys.exit(0 if success else 1)
