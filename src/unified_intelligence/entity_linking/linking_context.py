from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LinkingContext:
    execution_id: str
    source_versions: tuple[tuple[str, str], ...] = ()
    explicit_metadata: tuple[tuple[str, str], ...] = ()
