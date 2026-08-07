from dataclasses import asdict
from datetime import UTC, datetime
import hashlib
import json

from src.core_intelligence.models import Observation

from ..models import TwitterProfile
from .discovery_result import DiscoveryResult
from .entity_extractor import TwitterEntityExtractor


class ProfileDiscovery:
    def __init__(self, extractor: TwitterEntityExtractor | None = None) -> None:
        self.extractor = extractor or TwitterEntityExtractor()

    def discover(self, profile: TwitterProfile) -> DiscoveryResult:
        payload = asdict(profile)
        timestamp = profile.created_at or datetime.now(UTC)
        checksum = hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()
        observation = Observation(
            f"twitter:profile:{profile.user_id}", "twitter", profile.user_id, "twitter", timestamp,
            timestamp, "0.3.0", checksum, payload,
        )
        text = " ".join(value for value in (profile.display_name, profile.description) if value)
        entities = self.extractor.extract(text, username=profile.username)
        return DiscoveryResult(observation.observation_id, "profile", observation, entities)
