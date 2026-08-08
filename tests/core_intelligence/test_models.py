from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

import pytest

from src.core_intelligence import Assessment, Entity, EntityType, Evidence, Finding, Identity, Observation, Signal


NOW = datetime(2026, 8, 7, 12, 0, tzinfo=timezone.utc)


def test_constructs_and_compares_entities_by_value() -> None:
    from uuid import UUID

    values = {"entity_id": UUID(int=1), "entity_type": EntityType.PROJECT, "identity": Identity(canonical_name="Example")}

    assert Entity(**values) == Entity(**values)


def test_models_are_frozen() -> None:
    entity = Entity(entity_type=EntityType.PROJECT, identity=Identity(canonical_name="Example"))

    with pytest.raises(FrozenInstanceError):
        entity.identity = Identity(canonical_name="Changed")  # type: ignore[misc]


def test_observation_serializes_raw_payload_and_timestamps() -> None:
    observation = Observation(
        "observation-1", "source", "source-1", "v1", NOW, NOW,
        "collector-v1", "sha256:value", {"raw": [1, True]},
    )

    serialized = observation.to_dict()

    assert serialized["collected_at"] == NOW.isoformat()
    assert serialized["raw_payload"] == {"raw": [1, True]}


def test_evidence_references_an_observation_and_preserves_provenance() -> None:
    evidence = Evidence(
        "evidence-1", "entity-1", "observation-1", "activity.velocity",
        12, 0.9, "source", {"extractor": "activity-v1"}, NOW,
    )

    assert evidence.observation_reference == "observation-1"
    assert evidence.provenance == {"extractor": "activity-v1"}


@pytest.mark.parametrize("model_type", [Finding, Assessment, Signal])
def test_empty_evidence_references_are_rejected(model_type: type) -> None:
    common = {
        Finding: ("f", "e", "growth", 0.8, (), "explanation", NOW),
        Assessment: ("a", "e", "trust", 80, 0.8, (), "policy", "1", NOW),
        Signal: ("s", "e", "watch", "medium", 0.8, "review", "why", (), NOW),
    }
    with pytest.raises(ValueError):
        model_type(*common[model_type])


def test_lifecycle_models_retain_their_evidence_references() -> None:
    finding = Finding("f", "entity-1", "growth", 0.8, ("evidence-1",), "why", NOW)
    assessment = Assessment(
        "a", "entity-1", "trust", 80, 0.85, ("evidence-1",), "trust-policy", "2.1", NOW
    )
    signal = Signal(
        "s", "entity-1", "watch", "medium", 0.9, "monitor", "why", ("evidence-1",), NOW
    )

    assert finding.supporting_evidence == assessment.evidence == signal.supporting_evidence
    assert assessment.policy_version == "2.1"
