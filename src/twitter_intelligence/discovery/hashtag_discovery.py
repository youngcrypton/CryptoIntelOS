from ..models import TwitterPost
from .discovery_result import DiscoveredEntity, DiscoveredEntityType
from .entity_extractor import TwitterEntityExtractor


class HashtagDiscovery:
    def __init__(self, extractor: TwitterEntityExtractor | None = None) -> None:
        self.extractor = extractor or TwitterEntityExtractor()

    def discover(self, post: TwitterPost) -> tuple[DiscoveredEntity, ...]:
        return tuple(
            value for value in self.extractor.extract(post.text)
            if value.entity_type in {DiscoveredEntityType.HASHTAG, DiscoveredEntityType.CASHTAG}
        )
