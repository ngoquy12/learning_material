import sys
import io

# Reconfigure stdout/stderr encoding for Windows console compatibility immediately
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from dotenv import load_dotenv
load_dotenv()

from cli.curriculum_parser import (
    sanitize_folder_name,
    get_or_rename_sanitized_folder,
    parse_all_sessions,
    get_context_curriculum,
    initialize_skeleton_structure,
    project_structure_reviewer_agent,
    verify_previous_lessons_completed,
)
from cli.runner import main_entry

def main():
    """Main wrapper for CLI execution."""
    main_entry()

if __name__ == "__main__":
    main()