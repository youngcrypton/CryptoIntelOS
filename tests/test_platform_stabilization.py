import ast
from datetime import UTC, datetime
from io import StringIO
from pathlib import Path

from src.core_intelligence.models import Observation
from src.github_intelligence.adapters import RepositoryObservationAdapter
from src.github_intelligence.models import Repository
from src.github_intelligence.organization_analyzer import OrganizationIntelligence
from src.github_intelligence.vertical_slice import GitHubVerticalSlice
from src.runtime import CorrelationId, ExecutionId, ExecutionMetrics, StageTiming, TraceId


ROOT = Path(__file__).parents[1]


def test_observability_contracts_and_versions() -> None:
    timing = StageTiming("collect", datetime.now(UTC), datetime.now(UTC), 1.0)
    metrics = ExecutionMetrics(ExecutionId("execution-1"), CorrelationId("correlation-1"), TraceId("trace-1"), (timing,))
    assert metrics.execution_id == "execution-1"
    from src.core_intelligence.version import __version__ as kernel_version
    from src.runtime.version import __version__ as runtime_version
    from src.platform_version import __version__ as platform_version
    assert (kernel_version, runtime_version, platform_version) == ("1.0.0", "1.0.0", "1.0.0")


def test_dependency_rules_are_enforced_by_import_graph() -> None:
    forbidden = {"src.runtime", "src.github_intelligence"}
    for path in (ROOT / "src" / "core_intelligence").rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imports = [node.module or "" for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]
        imports.extend(alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names)
        assert not any(value.startswith(tuple(forbidden)) for value in imports), path
    for path in (ROOT / "src" / "runtime").rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imports = [node.module or "" for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]
        imports.extend(alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names)
        assert not any(value.startswith("src.github_intelligence") for value in imports), path


def test_adapter_failure_is_explicit() -> None:
    try:
        RepositoryObservationAdapter().to_observation(Repository(1, "x", "a/x", updated_at="not-a-date"))
    except ValueError:
        pass
    else:
        raise AssertionError("invalid GitHub timestamp must fail explicitly")


def test_missing_metadata_remains_deterministic() -> None:
    result = GitHubVerticalSlice().run(Repository(2, "x", "a/x"), output=StringIO())
    assert isinstance(result.canonical.observation, Observation)
    assert result.runtime.execution.final_state.value == "completed"


def test_legacy_models_are_marked_deprecated() -> None:
    from src.intelligence import finding
    from src.intelligence.core import signal
    from src.models import intelligence_signal
    assert finding.__deprecated__ and signal.__deprecated__ and intelligence_signal.__deprecated__


def test_archived_repository_metadata_is_preserved() -> None:
    result = GitHubVerticalSlice().run(
        Repository(3, "archive", "a/archive"),
        {"archived": True},
        output=StringIO(),
    )
    assert result.canonical.observation.raw_payload["name"] == "archive"
    assert result.runtime.execution.final_state.value == "completed"


def test_organization_repository_produces_organization_evidence() -> None:
    organization = OrganizationIntelligence(
        9, "acme", "Acme", True, 3, 2, 10, 0, None, None, None, None, None, None, None, None, None
    )
    result = GitHubVerticalSlice().run(
        Repository(4, "org", "acme/org"),
        organization=organization,
        output=StringIO(),
    )
    assert any(item.metric == "organization_profile" for item in result.canonical.evidence)


def test_runtime_failure_propagates_deterministically() -> None:
    class FailingRuntime:
        def execute(self, execution_id, objects):
            raise RuntimeError("runtime failed")

    try:
        GitHubVerticalSlice(runtime=FailingRuntime()).run(Repository(5, "x", "a/x"), output=StringIO())
    except RuntimeError as error:
        assert str(error) == "runtime failed"
    else:
        raise AssertionError("runtime failure must propagate")


def test_reasoning_failure_propagates_deterministically() -> None:
    class ReasoningFailureRuntime:
        def execute(self, execution_id, objects):
            raise RuntimeError("reasoning failed")

    try:
        GitHubVerticalSlice(runtime=ReasoningFailureRuntime()).run(Repository(6, "x", "a/x"), output=StringIO())
    except RuntimeError as error:
        assert str(error) == "reasoning failed"
    else:
        raise AssertionError("reasoning failure must propagate")
