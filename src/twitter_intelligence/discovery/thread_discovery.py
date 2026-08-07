from datetime import UTC, datetime
import hashlib
import json

from src.core_intelligence.models import Observation

from ..models import TwitterPost
from .discovery_result import DiscoveryResult
from .post_discovery import PostDiscovery


class ThreadDiscovery:
    def __init__(self, post_discovery: PostDiscovery | None = None) -> None:
        self.post_discovery = post_discovery or PostDiscovery()

    def discover(self, posts: tuple[TwitterPost, ...]) -> DiscoveryResult:
        if not posts:
            raise ValueError("a thread requires at least one post")
        children = tuple(self.post_discovery.discover(post) for post in posts)
        thread_id = posts[0].conversation_id or posts[0].post_id
        payload = {"thread_id": thread_id, "post_ids": [post.post_id for post in posts]}
        timestamp = min(post.created_at for post in posts)
        checksum = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        observation = Observation(
            f"twitter:thread:{thread_id}", "twitter", thread_id, "twitter", datetime.now(UTC),
            timestamp, "0.3.0", checksum, payload,
        )
        entities = tuple(entity for child in children for entity in child.entities)
        return DiscoveryResult(observation.observation_id, "thread", observation, entities, children)
