import hashlib
import json

from src.core_intelligence.models import Observation
from src.runtime.engine import ExecutionContext, ExecutionResult

from ..models import TwitterPost, TwitterProfile
from ..runtime import TwitterRuntimeIntegration
from .discovery_result import DiscoveryResult
from .post_discovery import PostDiscovery
from .profile_discovery import ProfileDiscovery
from .thread_discovery import ThreadDiscovery


class TwitterDiscoveryEngine:
    """Coordinate deterministic Twitter discovery and SDK Runtime delegation."""

    def __init__(self) -> None:
        self.profiles = ProfileDiscovery()
        self.posts = PostDiscovery()
        self.threads = ThreadDiscovery(self.posts)

    def discover_profile(self, profile: TwitterProfile) -> DiscoveryResult:
        return self.profiles.discover(profile)

    def discover_post(self, post: TwitterPost) -> DiscoveryResult:
        return self.posts.discover(post)

    def discover_thread(self, posts: tuple[TwitterPost, ...]) -> DiscoveryResult:
        return self.threads.discover(posts)

    @staticmethod
    def enter_runtime(
        results: tuple[DiscoveryResult, ...],
        integration: TwitterRuntimeIntegration,
        context: ExecutionContext,
    ) -> ExecutionResult:
        if not results:
            raise ValueError("at least one discovery result is required")
        if len(results) == 1:
            observation = results[0].observation
        else:
            payload = {
                "discovery_type": "batch",
                "results": [TwitterDiscoveryEngine._result_payload(result) for result in results],
            }
            checksum = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
            first = results[0].observation
            observation = Observation(
                f"twitter:discovery:batch:{checksum[:16]}", "twitter", checksum, "twitter-api",
                first.collected_at, max(result.observation.observed_at for result in results),
                "0.3.0", checksum, payload,
            )
        return integration.integrate((observation, (), (), (), ()), context)

    @staticmethod
    def _result_payload(result: DiscoveryResult) -> dict[str, object]:
        return {
            "discovery_id": result.discovery_id,
            "discovery_type": result.discovery_type,
            "observation": result.observation.to_dict(),
            "entities": [
                {
                    "entity_type": entity.entity_type.value,
                    "value": entity.value,
                    "normalized_value": entity.normalized_value,
                    "metadata": dict(entity.metadata),
                }
                for entity in result.entities
            ],
            "children": [TwitterDiscoveryEngine._result_payload(child) for child in result.children],
        }
