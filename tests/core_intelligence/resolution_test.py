from dataclasses import FrozenInstanceError, asdict
from datetime import UTC, datetime
from uuid import UUID

import pytest

from src.core_intelligence.resolution import (
    ResolutionCandidate,
    ResolutionContext,
    ResolutionDecision,
    ResolutionEvidence,
    ResolutionPolicy,
    ResolutionPolicyMode,
    ResolutionRequest,
    ResolutionStatus,
    ResolutionStrategy,
    ResolutionStrategyType,
    ResolutionType,
)

def test_request_candidate_evidence_and_decision_construct() -> None:
    policy = ResolutionPolicy("balanced", ResolutionPolicyMode.BALANCED)
    context = ResolutionContext("exec-1", "github", policy, datetime.now(UTC))
    evidence = ResolutionEvidence("record-1", 0.8, "matching identifier", context)
    candidate = ResolutionCandidate("entity-1", supporting_evidence=(evidence,))
    request = ResolutionRequest(resolution_type=ResolutionType.ENTITY, submitted_objects=("object-1",))
    decision = ResolutionDecision(status=ResolutionStatus.RESOLVED, chosen_candidate=candidate, reasoning="evidence supports candidate", policy_version=policy.version)

    assert isinstance(request.request_id, UUID)
    assert decision.chosen_candidate is candidate
    assert asdict(decision)["status"] is ResolutionStatus.RESOLVED

def test_enums_have_stable_string_values() -> None:
    assert {item.value for item in ResolutionType} >= {"entity", "relationship", "signal"}
    assert {item.value for item in ResolutionStatus} >= {"pending", "resolved", "manual_review"}
    assert ResolutionStrategyType.AI_ASSISTED.value == "ai_assisted"

def test_contracts_are_immutable() -> None:
    with pytest.raises(FrozenInstanceError):
        ResolutionPolicy("strict").name = "changed"

def test_registry_is_protocol_contract() -> None:
    from typing import get_type_hints
    from src.core_intelligence.resolution import ResolutionRegistry
    assert "register_policy" in ResolutionRegistry.__dict__
    assert get_type_hints(ResolutionRequest)["resolution_type"] is ResolutionType
