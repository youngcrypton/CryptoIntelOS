from dataclasses import dataclass
@dataclass(frozen=True, slots=True)
class ReasoningPolicy:
    name: str = "default"
    version: str = "1"
    provider_preferences: tuple[str, ...] = ()
    metadata: tuple[tuple[str,str], ...] = ()
