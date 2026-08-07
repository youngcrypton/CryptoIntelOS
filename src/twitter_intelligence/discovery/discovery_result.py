from dataclasses import dataclass
from enum import StrEnum

from src.core_intelligence.models import Observation


class DiscoveredEntityType(StrEnum):
    URL = "url"
    DOMAIN = "domain"
    USERNAME = "username"
    MENTION = "mention"
    HASHTAG = "hashtag"
    CASHTAG = "cashtag"
    EMAIL = "email"
    GITHUB_REPOSITORY = "github_repository"
    GITHUB_ORGANIZATION = "github_organization"
    WEBSITE = "website"
    DISCORD_INVITE = "discord_invite"
    TELEGRAM_LINK = "telegram_link"
    DOCUMENTATION_LINK = "documentation_link"
    GITBOOK_LINK = "gitbook_link"
    MEDIA = "media"
    IMAGE = "image"
    VIDEO = "video"
    SPACE = "space"


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
