"""Evidence primitives shared by all intelligence engines."""

from dataclasses import dataclass
from datetime import datetime

from .enums import IntelligenceSource


@dataclass(frozen=True)
class IntelligenceEvidence:
    """Traceable observation supporting an intelligence signal."""

    source: IntelligenceSource | str
    summary: str
    reference: str | None = None
    observed_at: datetime | None = None
    reliability: float = 1.0

    def __post_init__(self) -> None:
        """Ensure evidence reliability is normalized."""

        if not 0.0 <= self.reliability <= 1.0:
            raise ValueError("evidence reliability must be between 0.0 and 1.0")
