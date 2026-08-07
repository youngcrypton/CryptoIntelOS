from ..models import Link
from .discovery_result import DiscoveryResult, canonical_observation
from .entity_extractor import WebsiteEntityExtractor


class LinkDiscovery:
    def __init__(self, extractor: WebsiteEntityExtractor | None = None) -> None:
        self.extractor = extractor or WebsiteEntityExtractor()

    def discover(self, link: Link, *, base_url: str | None = None) -> DiscoveryResult:
        entities = self.extractor.extract(link.text or "", urls=(link.target_url,), base_url=base_url)
        observation = canonical_observation("link", link.link_id, link)
        return DiscoveryResult(observation.observation_id, "link", observation, entities)
