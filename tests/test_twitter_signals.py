from datetime import UTC, datetime

from src.platform_sdk import RuntimeFacade
from src.runtime.engine import ExecutionContext, ExecutionResult, ExecutionState
from src.twitter_intelligence import (
    TwitterAnalysisEngine,
    TwitterDiscoveryEngine,
    TwitterPost,
    TwitterRuntimeIntegration,
    TwitterSignalEngine,
)
from src.twitter_intelligence.signals import (
    DuplicateSignalGeneratorError,
    FounderSignal,
    SignalRegistry,
)


NOW = datetime(2026, 8, 7, tzinfo=UTC)


def generate(text: str):
    observation = TwitterDiscoveryEngine().discover_post(
        TwitterPost("post-1", "project-1", text, NOW)
    ).observation
    analysis = TwitterAnalysisEngine().analyze(observation)
    return TwitterSignalEngine().generate(analysis)


def signal_types(text: str) -> set[str]:
    return {signal.signal_type for signal in generate(text).signals}


def test_hidden_gem_signal() -> None:
    assert "Hidden Gem Candidate" in signal_types("Product launch in the DeFi ecosystem")


def test_early_project_signal() -> None:
    assert "Early Project" in signal_types("Founder announced a product launch")


def test_founder_signal() -> None:
    assert "Founder Worth Watching" in signal_types("Founder and CEO shared the roadmap")


def test_hiring_signal() -> None:
    assert "Hiring Wave" in signal_types("We're hiring; join our team")


def test_funding_signal() -> None:
    assert "Funding Detected" in signal_types("We raised a seed round of funding")


def test_partnership_signal() -> None:
    assert "Partnership Confirmed" in signal_types("Partnership and integration confirmed")


def test_ecosystem_signal() -> None:
    assert "Ecosystem Breakout" in signal_types("Expanding through the DeFi ecosystem")


def test_narrative_signal() -> None:
    assert "Narrative Acceleration" in signal_types("AI and RWA narrative momentum")


def test_launch_signal() -> None:
    assert "Product Launch Imminent" in signal_types("Product launch and beta release")


def test_watchlist_signal() -> None:
    assert "Watchlist Candidate" in signal_types("Founder launch in the DeFi ecosystem")


def test_signal_registry_rejects_duplicate_types() -> None:
    registry = SignalRegistry()
    registry.register(FounderSignal())
    try:
        registry.register(FounderSignal())
    except DuplicateSignalGeneratorError:
        return
    raise AssertionError("duplicate signal generator was accepted")


def test_runtime_delegation_includes_signals() -> None:
    output = generate("Founder launch in the DeFi ecosystem")
    received = []

    def runtime_entrypoint(canonical_output, context):
        received.append(canonical_output)
        return ExecutionResult(context.execution_id, ExecutionState.COMPLETED)

    context = ExecutionContext("execution-1", "1.0", NOW)
    result = TwitterSignalEngine.enter_runtime(
        output, TwitterRuntimeIntegration(RuntimeFacade(runtime_entrypoint)), context
    )
    assert result.final_state is ExecutionState.COMPLETED
    assert received[0] == (
        output.observation, output.evidence, output.findings, output.assessments, output.signals
    )
