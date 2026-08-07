from ..models import Page
from .discovery_result import DiscoveryResult, canonical_observation
from .entity_extractor import WebsiteEntityExtractor


class PageDiscovery:
    def __init__(self, extractor: WebsiteEntityExtractor | None = None) -> None:
        self.extractor = extractor or WebsiteEntityExtractor()

    def discover(self, page: Page) -> DiscoveryResult:
        text = " ".join(value for value in (page.title, page.description) if value)
        entities = self.extractor.extract(text, urls=(page.url,), base_url=page.url)
        observation = canonical_observation("page", page.page_id, page)
        return DiscoveryResult(observation.observation_id, "page", observation, entities)
