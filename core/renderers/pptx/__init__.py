"""
core/renderers/pptx package init

Primary API: deck_engine.build_deck() — fully dynamic, zero hard-coded content.
"""

from core.renderers.pptx.deck_engine import build_deck, build_slide, ShapeIdGenerator
from core.renderers.pptx.slide_validator import validate_pptx_file, validate_unpacked_deck, export_slide_images

__all__ = [
    "build_deck",
    "build_slide",
    "ShapeIdGenerator",
    "validate_pptx_file",
    "validate_unpacked_deck",
    "export_slide_images",
]
