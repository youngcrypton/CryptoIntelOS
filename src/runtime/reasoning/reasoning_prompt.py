from dataclasses import dataclass
@dataclass(frozen=True, slots=True)
class ReasoningPrompt:
    instruction: str
    context: tuple[str, ...] = ()
    constraints: tuple[str, ...] = ()
    output_schema: str | None = None
