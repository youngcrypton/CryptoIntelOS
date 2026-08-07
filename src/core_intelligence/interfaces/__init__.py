"""Canonical execution contracts for CryptoIntel OS intelligence components."""

from .components import Analyzer, Collector, Correlator, Resolver, Scorer, SignalGenerator
from .context import ExecutionContext
from .pipeline import PipelineStage
from .registry import ComponentRegistry

__all__ = (
    "Analyzer",
    "Collector",
    "ComponentRegistry",
    "Correlator",
    "ExecutionContext",
    "PipelineStage",
    "Resolver",
    "Scorer",
    "SignalGenerator",
)
