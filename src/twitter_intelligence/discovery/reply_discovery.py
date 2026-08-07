from ..models import TwitterPost
from .discovery_result import DiscoveryResult
from .post_discovery import PostDiscovery


class ReplyDiscovery:
    def __init__(self, post_discovery: PostDiscovery | None = None) -> None:
        self.post_discovery = post_discovery or PostDiscovery()

    def discover(self, post: TwitterPost) -> DiscoveryResult:
        result = self.post_discovery.discover(post)
        return DiscoveryResult(result.discovery_id, "reply", result.observation, result.entities)
