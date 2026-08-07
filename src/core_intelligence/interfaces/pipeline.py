"""Canonical intelligence pipeline ordering."""

from enum import IntEnum


class PipelineStage(IntEnum):
    """Stages in their mandatory execution order."""

    COLLECTOR = 1
    OBSERVATION = 2
    ANALYZER = 3
    EVIDENCE = 4
    RESOLVER = 5
    FINDING = 6
    SCORER = 7
    ASSESSMENT = 8
    SIGNAL_GENERATOR = 9
    SIGNAL = 10
