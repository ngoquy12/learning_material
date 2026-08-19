"""
cli/runner.py — Main orchestration runner for Elearning Content Factory CLI workflow.
Delegates command execution to modular handlers in cli.commands package.
"""

import sys
import io
from pathlib import Path

# Ensure project root is in sys.path
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from cli.args import parse_cli_arguments
from cli.commands import (
    handle_init_config,
    handle_generate_pm,
    execute_course_workflow,
)

def main_entry():
    """Main CLI execution entry point."""
    try:
        sys.stdout.reconfigure(line_buffering=True, encoding='utf-8')
        sys.stderr.reconfigure(line_buffering=True, encoding='utf-8')
    except Exception:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', write_through=True)
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', write_through=True)

    print("=====================================================================")
    print("Starting Multi-Agent Learning Content Factory (Antigravity Workflow)")
    print("=====================================================================")

    # Run Pre-flight Environment & Prerequisites Check
    from scripts.check_environment import run_all_checks
    if not run_all_checks():
        print("[CLI Warning] Pre-flight system check flagged warnings. Proceeding with caution...\n")

    args = parse_cli_arguments()

    # 1. Handle course config template generation (--init-config)
    if args.init_config:
        handle_init_config(args.init_config)
        return

    # 2. Handle AI PM syllabus automated design (--generate-pm)
    if args.generate_pm:
        handle_generate_pm(args)
        return

    # 3. Handle main course material generation workflow
    execute_course_workflow(args)

if __name__ == '__main__':
    main_entry()
