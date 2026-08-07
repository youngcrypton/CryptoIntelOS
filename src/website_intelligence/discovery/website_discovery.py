from ..models import Website
from .discovery_result import DiscoveryResult, canonical_observation
from .entity_extractor import WebsiteEntityExtractor


class WebsiteDiscovery:
    def __init__(self, extractor: WebsiteEntityExtractor | None = None) -> None:
        self.extractor = extractor or WebsiteEntityExtractor()

    def discover(self, website: Website) -> DiscoveryResult:
        text = " ".join(value for value in (website.name, website.description) if value)
        entities = self.extractor.extract(text, urls=(website.url,), base_url=website.url)
        observation = canonical_observation("website", website.website_id, website)
        return DiscoveryResult(observation.observation_id, "website", observation, entities)
