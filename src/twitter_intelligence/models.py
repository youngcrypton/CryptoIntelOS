"""Source-specific Twitter data contracts."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class TwitterProfile:
    user_id: str
    username: str
    display_name: str | None = None
    description: str | None = None
    verified: bool = False
    created_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class TwitterPost:
    post_id: str
    author_id: str
    text: str
    created_at: datetime
    conversation_id: str | None = None
    referenced_post_ids: tuple[str, ...] = ()
