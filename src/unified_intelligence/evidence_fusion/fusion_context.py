from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FusionContext:
    execution_id: str
    identity_identifier: str
    source_versions: tuple[tuple[str, str], ...] = ()
