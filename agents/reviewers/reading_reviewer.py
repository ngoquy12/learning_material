"""
agents/reviewers/reading_reviewer.py
Reading Material UX/UI & Layout Quality Reviewer Agent.
Audits generated reading.html files for layout integrity, light mode compliance, responsive tables, and typography.
"""

from typing import Dict, Any, List, Optional
from agents.reading_ui_reviewer import (
    review_reading_ui,
    review_and_fix_reading_ui,
    batch_review_session,
    capture_screenshots,
    compress_and_resize_screenshot,
    cleanup_passed_screenshots
)
from agents.reviewer_agents import html_ux_reviewer

# Facade aliases for convenience
reading_ui_reviewer = review_reading_ui

class HTMLReadingUIReviewerAgent:
    """Wrapper class for reading UI reviewer."""
    def __init__(self):
        pass

    def review(self, html_path: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
        return review_reading_ui(html_path, output_dir)

__all__ = [
    "HTMLReadingUIReviewerAgent",
    "reading_ui_reviewer",
    "review_reading_ui",
    "review_and_fix_reading_ui",
    "batch_review_session",
    "capture_screenshots",
    "compress_and_resize_screenshot",
    "cleanup_passed_screenshots",
    "html_ux_reviewer"
]
