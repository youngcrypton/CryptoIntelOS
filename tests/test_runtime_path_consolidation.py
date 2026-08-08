from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from src.core_intelligence.models import Observation
from src.github_intelligence.adapters import GitHubRuntimeIntegration
from src.github_intelligence.analysis.repository_analyzer import RepositoryAnalysis
from src.github_intelligence.models import Repository
from src.platform_sdk import LegacyExecutionAdapter
from src.runtime.engine import ExecutionState, PipelineStage


def test_legacy_value_adapter_runs_the_complete_runtime_lifecycle() -> None:
    value = SimpleNamespace(summary="legacy result", signal_type="Website", project="Acme")
    with pytest.warns(DeprecationWarning):
        result = LegacyExecutionAdapter().execute_value(
            value, source="Website Collector", execution_id="legacy:acme"
        )
    assert result.value is value
    assert result.runtime.execution.final_state is ExecutionState.COMPLETED
    assert result.runtime.execution.completed_stages == tuple(
        stage.value for stage in PipelineStage
    )
    node = result.runtime.compilation.projection.nodes[0]
    assert node.node_type == "observation"


def test_legacy_collector_execution_is_redirected_through_platform_sdk() -> None:
    class Collector:
        name = "Legacy Collector"

        def execute(self):
            return SimpleNamespace(summary="collected")

    with pytest.warns(DeprecationWarning):
        result = LegacyExecutionAdapter().execute_collector(Collector())
    assert result.runtime.execution.final_state is ExecutionState.COMPLETED
    assert result.runtime.compilation.context.source == "canonical"


def test_github_compatibility_execution_uses_canonical_runtime() -> None:
    repository = Repository(1, "crypto", "acme/crypto", updated_at="2026-01-01T00:00:00Z")
    analysis = RepositoryAnalysis(repository, ["Python"], {"commits": 4}, {"license": "MIT"})
    score = SimpleNamespace(overall_repository_score=82.0, confidence_score=91.0)
    result = GitHubRuntimeIntegration().process(repository, analysis, score)
    assert result.execution is result.runtime.execution
    assert result.execution.final_state is ExecutionState.COMPLETED
    assert result.execution.completed_stages == tuple(stage.value for stage in PipelineStage)
    assert isinstance(result.observation, Observation)


def test_legacy_processor_runs_once_before_runtime_projection() -> None:
    calls = []
    value = SimpleNamespace(summary="processed")
    with pytest.warns(DeprecationWarning):
        result = LegacyExecutionAdapter().execute_value(
            value,
            source="legacy-pipeline",
            processor=lambda: calls.append("processed"),
        )
    assert calls == ["processed"]
    assert result.runtime.execution.final_state is ExecutionState.COMPLETED
