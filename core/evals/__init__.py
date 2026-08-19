"""
core/evals package initialization.
"""

from core.evals.benchmark import (
    MetricScore,
    PedagogicalScorecard,
    PedagogicalBenchmarkEngine,
    evaluate_lesson_pedagogy
)

__all__ = [
    "MetricScore",
    "PedagogicalScorecard",
    "PedagogicalBenchmarkEngine",
    "evaluate_lesson_pedagogy"
]
