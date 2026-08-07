"""External identifiers associated with an entity."""
from dataclasses import dataclass
from .identifier_type import IdentifierType
from .identity_context import IdentityContext

@dataclass(frozen=True, slots=True)
class Identifier:
    value: str
    identifier_type: IdentifierType
    context: IdentityContext | None = None
