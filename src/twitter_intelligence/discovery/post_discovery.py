from dataclasses import asdict
import hashlib
import json

from src.core_intelligence.models import Observation

from ..models import TwitterPost
from .discovery_result import DiscoveryResult
from .entity_extractor import TwitterEntityExtractor


class PostDiscovery:
    def __init__(self, extractor: TwitterEntityExtractor | None = None) -> None:
        self.extractor = extractor or TwitterEntityExtractor()

    def discover(self, post: TwitterPost) -> DiscoveryResult:
        payload = asdict(post)
        checksum = hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()
        observation = Observation(
            f"twitter:post:{post.post_id}", "twitter", post.post_id, "twitter", post.created_at,
            post.created_at, "0.3.0", checksum, payload,
        )
        return DiscoveryResult(observation.observation_id, "post", observation, self.extractor.extract(post.text))
