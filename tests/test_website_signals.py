from datetime import UTC, datetime

from src.platform_sdk import RuntimeFacade
from src.runtime.engine import ExecutionContext, ExecutionState, ExecutionResult
from src.website_intelligence import Website, WebsiteDiscoveryEngine, WebsiteAnalysisEngine, WebsiteRuntimeIntegration
from src.website_intelligence.signals import DuplicateSignalGeneratorError, SignalRegistry, WebsiteSignalEngine

NOW = datetime(2026, 8, 7, tzinfo=UTC)


def generate(payload: str):
    result = WebsiteDiscoveryEngine().discover_website(Website("site-1", "https://example.com", "example.com", description=payload))
    return WebsiteSignalEngine().generate(WebsiteAnalysisEngine().analyze(result.observation))


def test_website_signals():
    types = {item.signal_type for item in generate("docs roadmap team careers audit security").signals}
    assert {"Official Website Verified", "Documentation Strength", "Roadmap Visibility", "Team Transparency", "Security Readiness", "Active Project Hiring"} <= types


def test_dormant_website_signal():
    assert "Dormant Website Risk" in {item.signal_type for item in generate("").signals}


def test_registry_rejects_duplicates():
    registry = SignalRegistry()
    generator = WebsiteSignalEngine.default_registry().generators()[0]
    registry.register(generator)
    try:
        registry.register(generator)
    except DuplicateSignalGeneratorError:
        return
    raise AssertionError("duplicate signal generator was accepted")


def test_runtime_delegation_includes_signals():
    output = generate("docs roadmap")
    received = []
    context = ExecutionContext("execution-1", "1.0", NOW)
    facade = RuntimeFacade(lambda canonical, ctx: (received.append(canonical) or ExecutionResult(ctx.execution_id, ExecutionState.COMPLETED)))
    result = WebsiteSignalEngine.enter_runtime(output, WebsiteRuntimeIntegration(facade), context)
    assert result.final_state is ExecutionState.COMPLETED
    assert received[0][-1] == output.signals
