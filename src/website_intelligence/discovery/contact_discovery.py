from .discovery_result import DiscoveredEntity, DiscoveredEntityType
from .entity_extractor import WebsiteEntityExtractor


class ContactDiscovery:
    def __init__(self, extractor: WebsiteEntityExtractor | None = None) -> None:
        self.extractor = extractor or WebsiteEntityExtractor()

    def discover(self, text: str) -> tuple[DiscoveredEntity, ...]:
        return tuple(entity for entity in self.extractor.extract(text) if entity.entity_type is DiscoveredEntityType.EMAIL)
