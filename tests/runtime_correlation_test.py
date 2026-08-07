from dataclasses import FrozenInstanceError, asdict
from datetime import UTC, datetime
from src.runtime.correlation import *
def test_correlation_and_bundles():
    ctx=CorrelationContext("x", "runtime", datetime.now(UTC)); evidence=EvidenceBundle(("e1",),("ref-1",)); graph=GraphBundle(("n1",),("e1",),"1")
    corr=Correlation(correlation_type=CorrelationType.FUNDING, participating_evidence=evidence.evidence, provenance=ctx)
    candidate=CorrelationCandidate(corr, confidence=.8); result=CorrelationResult(CorrelationStatus.CANDIDATE,(corr,))
    assert candidate.correlation is corr and result.correlations == (corr,)
    assert asdict(graph)["version"] == "1"
def test_integrity_and_registry():
    with __import__('pytest').raises(FrozenInstanceError): CorrelationPolicy().version="2"
    assert CorrelationType.SECURITY_RISK.value == "security_risk"
    assert "register" in CorrelationRegistry.__dict__
