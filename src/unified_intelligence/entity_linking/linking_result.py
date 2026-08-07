from dataclasses import dataclass

from .entity_match import EntityMatch
from .identity_bundle import IdentityBundle


@dataclass(frozen=True, slots=True)
class LinkingResult:
    bundle: IdentityBundle
    matches: tuple[EntityMatch, ...]
