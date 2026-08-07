from dataclasses import dataclass
@dataclass(frozen=True, slots=True)
class ReasoningMemory:
    references: tuple[str, ...] = ()
    contents: tuple[object, ...] = ()
    version: str | None = None
