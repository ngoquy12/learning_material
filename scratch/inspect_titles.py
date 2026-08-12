import sys
from pathlib import Path
sys.path.insert(0, '.')
from cli.curriculum_parser import parse_all_sessions

sessions = parse_all_sessions("output/pms/Lập_trình_Python/PM_Python.xlsx")
for s in sessions:
    print(f"[{s['session_id']}] {s['title']}")
    for l in s.get('lessons', []):
        print(f"   - [{l['lesson_id']}] {l['title']}")
