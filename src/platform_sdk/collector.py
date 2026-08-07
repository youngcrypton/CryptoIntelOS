from collections.abc import Sequence
from typing import Protocol

from src.core_intelligence.interfaces.context import ExecutionContext
from src.core_intelligence.models import Observation

from .metadata import IntegrationMetadata


class SourceCollector(Protocol):
    """Canonical collector boundary for any external intelligence source."""

    def collect(self, context: ExecutionContext) -> Sequence[Observation]: ...

    def metadata(self) -> IntegrationMetadata: ...
