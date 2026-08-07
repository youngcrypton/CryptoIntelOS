from ..models import TwitterPost
from .discovery_result import DiscoveredEntity, DiscoveredEntityType
from .entity_extractor import TwitterEntityExtractor


class URLDiscovery:
    def __init__(self, extractor: TwitterEntityExtractor | None = None) -> None:
        self.extractor = extractor or TwitterEntityExtractor()

    def discover(self, post: TwitterPost) -> tuple[DiscoveredEntity, ...]:
        return tuple(value for value in self.extractor.extract(post.text) if value.entity_type in {
            DiscoveredEntityType.URL, DiscoveredEntityType.DOMAIN, DiscoveredEntityType.WEBSITE,
            DiscoveredEntityType.GITHUB_REPOSITORY, DiscoveredEntityType.GITHUB_ORGANIZATION,
            DiscoveredEntityType.DISCORD_INVITE, DiscoveredEntityType.TELEGRAM_LINK,
            DiscoveredEntityType.DOCUMENTATION_LINK, DiscoveredEntityType.GITBOOK_LINK,
        })
