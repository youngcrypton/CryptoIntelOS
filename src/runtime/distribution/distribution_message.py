from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class DistributionMessage:
    message_id: str
    subject: str | None = None
    body: str | None = None
    payload: Mapping[str, Any] = field(default_factory=dict)
    content_type: str | None = None
