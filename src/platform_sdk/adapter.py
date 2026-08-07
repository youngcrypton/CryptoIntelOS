from typing import Protocol, TypeVar

from src.core_intelligence.models import Observation

SourceObject = TypeVar("SourceObject", contravariant=True)


class SourceAdapter(Protocol[SourceObject]):
    """Translate one source-domain object into a canonical Observation."""

    def to_observation(self, value: SourceObject) -> Observation: ...
