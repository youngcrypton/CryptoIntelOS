from dataclasses import FrozenInstanceError, asdict
from datetime import UTC, datetime
from src.runtime.reasoning import *
def test_reasoning_chain_confidence_and_explanation():
    step=ReasoningStep("s1", "inspect evidence", ("e1",), "supported")
    chain=ReasoningChain((step,), "rule_based")
    confidence=ReasoningConfidence(.85, "evidence", ("e1",), .15, "well supported")
    explanation=ReasoningExplanation("Conclusion", ("e1",), ("assumption",), ("limitation",))
    result=ReasoningResult(ReasoningStatus.COMPLETED, "Conclusion", chain, confidence, explanation, ("source-1",))
    assert result.chain.steps[0] is step
    assert asdict(result)["confidence"]["confidence"] == .85
def test_request_memory_and_registry_contracts():
    request=ReasoningRequest(reasoning_type=ReasoningType.RISK_ASSESSMENT, inputs=("correlation",))
    memory=ReasoningMemory(("correlation",), (request,), "1")
    assert memory.contents[0] is request
    assert "register_provider" in ReasoningRegistry.__dict__
    assert ReasoningType.TREND_ANALYSIS.value == "trend_analysis"
def test_immutability():
    import pytest
    with pytest.raises(FrozenInstanceError): ReasoningPolicy().version="2"
