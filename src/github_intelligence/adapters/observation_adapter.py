from dataclasses import asdict
from datetime import UTC, datetime
import hashlib
import json

from src.core_intelligence.models import Observation
from src.github_intelligence.models import Repository

from ._time import utc


class RepositoryObservationAdapter:
    """Translate GitHub repository metadata into a canonical Observation."""

    def to_observation(self, repository: Repository, *, collector_version: str = "github-1.0") -> Observation:
        payload = asdict(repository)
        encoded = json.dumps(payload, sort_keys=True, default=str).encode()
        observed_at = utc(repository.updated_at)
        return Observation(
            observation_id=f"github:repository:{repository.id}",
            source="github",
            source_identifier=repository.full_name,
            source_version="github-api",
            collected_at=datetime.now(UTC),
            observed_at=observed_at,
            collector_version=collector_version,
            checksum=hashlib.sha256(encoded).hexdigest(),
            raw_payload=payload,
        )
