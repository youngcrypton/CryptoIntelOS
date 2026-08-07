from dataclasses import dataclass
@dataclass(frozen=True, slots=True)
class CorrelationPolicy:
    name: str = "default"
    version: str = "1"
    metadata: tuple[tuple[str,str], ...] = ()
