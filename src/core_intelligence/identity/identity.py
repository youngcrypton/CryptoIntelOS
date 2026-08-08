"""Canonical identity contract."""
from dataclasses import dataclass, field
from uuid import UUID, uuid4
from .identifier import Identifier
from .identity_context import IdentityContext

@dataclass(frozen=True, slots=True, kw_only=True)
class Identity:
    identity_id: UUID = field(default_factory=uuid4)
    canonical_name: str | None = None
    identifiers: tuple[Identifier, ...] = ()
    context: IdentityContext | None = None
