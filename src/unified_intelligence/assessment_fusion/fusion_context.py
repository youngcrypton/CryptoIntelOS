from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AssessmentFusionContext:
    execution_id: str
    identity_identifier: str
    source_versions: tuple[tuple[str, str], ...] = ()
