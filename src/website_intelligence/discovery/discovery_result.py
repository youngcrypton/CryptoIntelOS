import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from src.core_intelligence.models import Observation


class DiscoveredEntityType(StrEnum):
    URL = "url"
    DOMAIN = "domain"
    EMAIL = "email"
    INTERNAL_LINK = "internal_link"
    EXTERNAL_LINK = "external_link"
    NAVIGATION = "navigation"
    DOCUMENTATION = "documentation"
    WHITEPAPER = "whitepaper"
    GITBOOK = "gitbook"
    BLOG = "blog"
    ROADMAP = "roadmap"
    CAREERS = "careers"
    TEAM = "team"
    AUDIT = "audit"
    FAQ = "faq"
    CONTACT = "contact"
    GITHUB_REPOSITORY = "github_repository"
    GITHUB_LINK = "github_link"
    TWITTER_ACCOUNT = "twitter_account"
    DISCORD_INVITE = "discord_invite"
    TELEGRAM_LINK = "telegram_link"
    LINKEDIN_LINK = "linkedin_link"
    YOUTUBE_LINK = "youtube_link"
    MEDIUM_LINK = "medium_link"
    LOGO = "logo"
    FAVICON = "favicon"
    METADATA = "metadata"


@dataclass(frozen=True, slots=True)
class DiscoveredEntity:
    entity_type: DiscoveredEntityType
    value: str
    normalized_value: str
    metadata: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True, slots=True)
class DiscoveryResult:
    discovery_id: str
    discovery_type: str
    observation: Observation
    entities: tuple[DiscoveredEntity, ...] = ()
    children: tuple["DiscoveryResult", ...] = ()


def canonical_observation(kind: str, identifier: str, value: Any) -> Observation:
    payload = asdict(value)
    timestamp = next(
        (
            item
            for item in (payload.get("modified_at"), payload.get("published_at"))
            if isinstance(item, datetime)
        ),
        datetime.now(UTC),
    )
    checksum = hashlib.sha256(
        json.dumps(payload, sort_keys=True, default=str).encode()
    ).hexdigest()
    return Observation(
        f"website:{kind}:{identifier}",
        "website",
        identifier,
        "website-source",
        timestamp,
        timestamp,
        "0.4.0",
        checksum,
        payload,
    )
