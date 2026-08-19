"""
core/renderers/pptx package init
"""

from core.renderers.pptx.slide_deck_builder import SlideDeckBuilder, slide_deck_builder
from core.renderers.pptx.slide_validator import validate_pptx_file, validate_unpacked_deck

__all__ = [
    "SlideDeckBuilder",
    "slide_deck_builder",
    "validate_pptx_file",
    "validate_unpacked_deck"
]
