"""
cli/args.py — Command-line argument parsing for Elearning Content Factory.
"""

import argparse
import os

def parse_cli_arguments():
    """Parses and returns command line arguments for the Elearning Content Factory."""
    parser = argparse.ArgumentParser(description="Multi-Agent Learning Content Factory")
    parser.add_argument(
        "--pm",
        type=str,
        default=r"d:\Rikkei Education\Elearning_Agent\Learning-Material\pms\PM_Web_Application_With_FastAPI.xlsx",
        help="Path to PM Excel sheet"
    )
    parser.add_argument(
        "--session",
        type=str,
        default="all",
        help="Session ID to run (e.g. 'Session 01', 'Session 02', or 'all')"
    )
    parser.add_argument(
        "--parts",
        type=str,
        default="all",
        help="Comma-separated parts to generate (html,slide,quiz,video,mindmap or all)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force rebuild artifacts even if already approved in checkpoint"
    )
    parser.add_argument(
        "--approve-pm",
        action="store_true",
        help="Approve the PM program and bypass the PM review blocker"
    )
    parser.add_argument(
        "--obsidian",
        action="store_true",
        help="Generate Obsidian Vault for the entire course structure"
    )
    parser.add_argument(
        "--scorm",
        action="store_true",
        help="Export compiled lessons to SCORM 1.2 .zip package for LMS import (Moodle, Canvas, etc.)"
    )
    parser.add_argument(
        "--cache-stats",
        action="store_true",
        help="Show Semantic Cache statistics and exit"
    )
    parser.add_argument(
        "--tech-stack",
        type=str,
        default="",
        help="Explicit technology stack (e.g. 'python/core', 'python/fastapi', 'typescript/nestjs', 'typescript/react', 'java/springboot')"
    )
    return parser.parse_args()
