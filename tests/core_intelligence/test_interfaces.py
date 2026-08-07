from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
from inspect import isabstract

import pytest

from src.core_intelligence.interfaces import (
    Analyzer,
    Collector,
    ComponentRegistry,
    Correlator,
    ExecutionContext,
    PipelineStage,
    Resolver,
    Scorer,
    SignalGenerator,
)


def test_component_interfaces_are_abstract() -> None:
    interfaces = (Collector, Analyzer, Resolver, Scorer, SignalGenerator, Correlator)

    assert all(isabstract(interface) for interface in interfaces)
    for interface in interfaces:
        with pytest.raises(TypeError):
            interface()


def test_pipeline_stage_declares_canonical_order() -> None:
    assert list(PipelineStage) == [
        PipelineStage.COLLECTOR,
        PipelineStage.OBSERVATION,
        PipelineStage.ANALYZER,
        PipelineStage.EVIDENCE,
        PipelineStage.RESOLVER,
        PipelineStage.FINDING,
        PipelineStage.SCORER,
        PipelineStage.ASSESSMENT,
        PipelineStage.SIGNAL_GENERATOR,
        PipelineStage.SIGNAL,
    ]
    assert PipelineStage.COLLECTOR < PipelineStage.SIGNAL


def test_execution_context_construction_and_immutability() -> None:
    started_at = datetime(2026, 8, 7, 12, 0, tzinfo=timezone.utc)
    context = ExecutionContext(
        execution_id="execution-1",
        pipeline_stage=PipelineStage.ANALYZER,
        source="source-a",
        started_at=started_at,
        metadata={"trace_id": "trace-1"},
    )

    assert context.started_at == started_at
    assert context.metadata["trace_id"] == "trace-1"
    with pytest.raises(FrozenInstanceError):
        context.source = "source-b"  # type: ignore[misc]


def test_registry_protocol_supports_structural_conformance() -> None:
    class Registry:
        def register_collector(self, name: str, component: Collector) -> None: pass
        def register_analyzer(self, name: str, component: Analyzer) -> None: pass
        def register_resolver(self, name: str, component: Resolver) -> None: pass
        def register_scorer(self, name: str, component: Scorer) -> None: pass
        def register_signal_generator(self, name: str, component: SignalGenerator) -> None: pass
        def register_correlator(self, name: str, component: Correlator) -> None: pass
        def get_component(self, component_type: str, name: str) -> object: return object()

    assert isinstance(Registry(), ComponentRegistry)
