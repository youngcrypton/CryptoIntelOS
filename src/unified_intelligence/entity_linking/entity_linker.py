from .entity_candidate import EntityCandidate
from .entity_resolution import DeterministicEntityResolution
from .linking_context import LinkingContext
from .linking_registry import LinkingRegistry
from .linking_result import LinkingResult


class EntityLinker:
    def __init__(self, registry: LinkingRegistry | None = None) -> None:
        self.registry = registry or self.default_registry()

    @staticmethod
    def default_registry() -> LinkingRegistry:
        registry = LinkingRegistry()
        registry.register(DeterministicEntityResolution())
        return registry

    def link(self, candidates: tuple[EntityCandidate, ...], context: LinkingContext) -> LinkingResult:
        return self.registry.get("deterministic-identity-v1").link(candidates, context)
