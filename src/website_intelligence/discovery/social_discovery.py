from .discovery_result import DiscoveredEntity, DiscoveredEntityType
from .entity_extractor import WebsiteEntityExtractor


class SocialDiscovery:
    def __init__(self, extractor: WebsiteEntityExtractor | None = None) -> None:
        self.extractor = extractor or WebsiteEntityExtractor()

    def discover(self, urls: tuple[str, ...]) -> tuple[DiscoveredEntity, ...]:
        social_types = {DiscoveredEntityType.TWITTER_ACCOUNT, DiscoveredEntityType.DISCORD_INVITE, DiscoveredEntityType.TELEGRAM_LINK, DiscoveredEntityType.LINKEDIN_LINK, DiscoveredEntityType.YOUTUBE_LINK, DiscoveredEntityType.MEDIUM_LINK}
        return tuple(entity for entity in self.extractor.extract(urls=urls) if entity.entity_type in social_types)
