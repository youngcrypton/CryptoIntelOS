"""Canonical, source-agnostic intelligence domain contracts."""

from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Mapping


JsonValue = None | bool | int | float | str | list["JsonValue"] | dict[str, "JsonValue"]


class SerializableModel:
    """Provide a JSON-compatible representation of a canonical model."""

    def to_dict(self) -> dict[str, Any]:
        """Return the model as a dictionary with ISO-formatted timestamps."""

        return _serialize(asdict(self))


def _serialize(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Mapping):
        return {key: _serialize(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_serialize(item) for item in value]
    return value


@dataclass(frozen=True, slots=True)
class Entity(SerializableModel):
    """A canonical real-world object to which intelligence may be attached."""

    entity_id: str
    entity_type: str
    canonical_name: str
    aliases: tuple[str, ...] = ()
    external_identifiers: Mapping[str, str] = field(default_factory=dict)
    lifecycle_status: str = "unknown"
    confidence: float = 1.0
    metadata: Mapping[str, JsonValue] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass(frozen=True, slots=True)
class Observation(SerializableModel):
    """An immutable record of raw information collected from a source."""

    observation_id: str
    source: str
    source_identifier: str
    source_version: str
    collected_at: datetime
    observed_at: datetime
    collector_version: str
    checksum: str
    raw_payload: JsonValue


@dataclass(frozen=True, slots=True)
class Evidence(SerializableModel):
    """A normalized fact extracted from an originating observation."""

    evidence_id: str
    entity_reference: str
    observation_reference: str
    metric: str
    value: JsonValue
    confidence: float
    source: str
    provenance: Mapping[str, JsonValue]
    timestamp: datetime


@dataclass(frozen=True, slots=True)
class Finding(SerializableModel):
    """A reproducible interpretation of one or more evidence records."""

    finding_id: str
    entity_reference: str
    finding_type: str
    confidence: float
    supporting_evidence: tuple[str, ...]
    explanation: str
    timestamp: datetime

    def __post_init__(self) -> None:
        if not self.supporting_evidence:
            raise ValueError("A finding must reference supporting evidence")


@dataclass(frozen=True, slots=True)
class Assessment(SerializableModel):
    """Versioned, policy-driven scored intelligence about an entity."""

    assessment_id: str
    entity_reference: str
    assessment_type: str
    score: float
    confidence: float
    evidence: tuple[str, ...]
    policy_name: str
    policy_version: str
    generated_at: datetime

    def __post_init__(self) -> None:
        if not self.evidence:
            raise ValueError("An assessment must reference evidence")


@dataclass(frozen=True, slots=True)
class Signal(SerializableModel):
    """Explainable, actionable intelligence supported by evidence."""

    signal_id: str
    entity_reference: str
    signal_type: str
    severity: str
    confidence: float
    recommendation: str
    explanation: str
    supporting_evidence: tuple[str, ...]
    timestamp: datetime

    def __post_init__(self) -> None:
        if not self.supporting_evidence:
            raise ValueError("A signal must reference supporting evidence")
