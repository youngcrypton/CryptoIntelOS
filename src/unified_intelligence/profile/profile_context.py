from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProfileContext:
    execution_id: str
    profile_version: str
    generated_at: str
    execution_metadata: tuple[tuple[str, str], ...] = ()
