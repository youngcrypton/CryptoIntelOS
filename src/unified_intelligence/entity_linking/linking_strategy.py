from typing import Protocol

from .entity_candidate import EntityCandidate
from .linking_context import LinkingContext
from .linking_result import LinkingResult


class EntityLinkingStrategy(Protocol):
    strategy_id: str

    def link(self, candidates: tuple[EntityCandidate, ...], context: LinkingContext) -> LinkingResult: ...
