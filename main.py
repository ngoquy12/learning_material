"""
main.py — Entry point for Elearning Content Factory CLI workflow.
Re-exports core parser functions for backward compatibility with backend API.
"""

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