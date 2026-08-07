from ..models import Document
from .discovery_result import (
    DiscoveredEntity,
    DiscoveredEntityType,
    DiscoveryResult,
    canonical_observation,
)
from .entity_extractor import WebsiteEntityExtractor


class DocumentDiscovery:
    def __init__(self, extractor: WebsiteEntityExtractor | None = None) -> None:
        self.extractor = extractor or WebsiteEntityExtractor()

    def discover(self, document: Document) -> DiscoveryResult:
        entities = list(self.extractor.extract(document.title or "", urls=(document.url,)))
        document_types = {
            "whitepaper": DiscoveredEntityType.WHITEPAPER,
            "documentation": DiscoveredEntityType.DOCUMENTATION,
            "docs": DiscoveredEntityType.DOCUMENTATION,
        }
        if entity_type := document_types.get(document.document_type.casefold()):
            entities.append(DiscoveredEntity(entity_type, document.url, document.url))
        observation = canonical_observation("document", document.document_id, document)
        return DiscoveryResult(observation.observation_id, "document", observation, tuple(entities))
